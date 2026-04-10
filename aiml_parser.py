"""
aiml_parser.py -- Parser AIML 1.31 per myAssistente
2026 - Licenza: stessa del progetto myAssistente

normalizzazione pattern in MAIUSCOLO

Tag <template> supportati
──────────────────────────
Variabili e predicati
  <get name="x"/>            legge un predicato utente
  <set name="x">...</set>    scrive un predicato utente (non emette testo)
  <bot name="x"/>            legge un predicato del bot (sola lettura)

Wildcard e input
  <star/>  <star index="N"/> cattura la N-esima wildcard del pattern
  <input/>                   input originale dell'utente (turno corrente)
  <input index="N"/>         N-esimo turno precedente (stored in _input_history)
  <that/>                    ultima risposta del bot (normalizzata)
  <that index="N"/>          N-esima risposta precedente (stored in _that_history)
  <topicstar/>               wildcard del topic corrente

Redirect
  <srai>...</srai>           ricerca ricorsiva di un pattern

Logica e selezione
  <random><li>...</li></random>
  <condition name="x" value="y">...</condition>
  <condition name="x"><li value="y">...</li><li>...</li></condition>

Trasformazioni testo
  <uppercase>...</uppercase>
  <lowercase>...</lowercase>
  <formal>...</formal>       prima lettera di ogni parola maiuscola
  <sentence>...</sentence>   prima lettera della frase maiuscola
  <explode>...</explode>     inserisce spazi tra ogni carattere

Sistema
  <date/>                    data/ora locali (formato configurabile via bot-predicato "dateformat")
  <date format="%d/%m/%Y"/>  formato strftime esplicito sull'attributo
  <size/>                    numero di categorie caricate
  <version/>                 versione del parser (bot-predicato "version" o default)
  <id/>                      identificatore sessione (bot-predicato "id" o uuid4)

Punteggiatura / spazio
  <br/>                      inserisce \n
  <p/>                       inserisce \n\n

Attributi speciali su <template>
  avatar="..."               passato nel dict di ritorno di rispondi()
  comando="..."              passato nel dict di ritorno di rispondi()
  menu="XXXX"                stringa 4 cifre (0/1) per aprire/chiudere sezioni UI
                             [comandi][memoria][shortcut][lingua]
                             passato nel dict di ritorno di rispondi()
                             
Uniformizza accenti (problema differenza e congiunzione o verbo essere)
"""

import re
import random
import uuid
import unicodedata
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path


# ─────────────────────────────────────────────
#  Versione del parser
# ─────────────────────────────────────────────
_PARSER_VERSION = "1.2.0"

# Profondità massima ricorsione SRAI
_MAX_SRAI_DEPTH = 20

# Lunghezza massima dello storico input/that
_MAX_HISTORY = 10


class Categoria:
    __slots__ = ("pattern", "that", "topic", "template", "avatar", "menu", "file")

    def __init__(self, pattern, that, topic, template, avatar, menu, file):
        self.pattern  = pattern
        self.that     = that
        self.topic    = topic
        self.template = template
        self.avatar   = avatar
        self.menu     = menu
        self.file     = file

    def __repr__(self):
        return (f"<Categoria pattern={self.pattern!r} "
                f"that={self.that!r} topic={self.topic!r}>")


class AIMLParser:

    def __init__(self):
        self._categorie     = []
        self._predicati     = {}          # predicati utente  (get/set)
        self._bot_predicati = {           # predicati bot     (bot name="...")
            "version": _PARSER_VERSION,
            "name":    "Assistente",
            "master":  "unknown",
            "dateformat": "%d/%m/%Y %H:%M",
        }
        self._topic         = "*"
        self._that          = "*"
        self._that_history  = []          # storico risposte bot (normalizzate)
        self._input_history = []          # storico input utente (originali)
        self._srai_depth    = 0
        self._srai_avatar   = None   # avatar propagato dall'ultimo <srai> risolto
        self._srai_comando  = None   # comando propagato dall'ultimo <srai> risolto
        self._srai_menu     = None   # menu propagato dall'ultimo <srai> risolto
        self._session_id    = str(uuid.uuid4())

    # ── Predicati utente ──────────────────────────────────────────────────

    def set_predicato(self, nome, valore):
        self._predicati[nome.lower()] = str(valore)

    def get_predicato(self, nome):
        return self._predicati.get(nome.lower(), "")

    # ── Predicati bot ─────────────────────────────────────────────────────

    def set_bot_predicato(self, nome, valore):
        """Imposta un predicato del bot (name, version, dateformat, ecc.)."""
        self._bot_predicati[nome.lower()] = str(valore)

    def get_bot_predicato(self, nome):
        return self._bot_predicati.get(nome.lower(), "")

    # ── Topic ─────────────────────────────────────────────────────────────

    def set_topic(self, topic):
        self._topic = self._normalizza(topic)

    @property
    def topic(self) -> str:
        """Topic corrente (sola lettura)."""
        return self._topic

    @property
    def categorie(self) -> list:
        """Lista delle categorie caricate (sola lettura)."""
        return self._categorie

    # ── Caricamento file ──────────────────────────────────────────────────

    def carica_file(self, path):
        path = Path(path)
        if not path.exists():
            print(f"[AIML] File non trovato: {path}")
            return 0
        try:
            tree = ET.parse(path)
            root = tree.getroot()
        except ET.ParseError as e:
            print(f"[AIML] Errore XML in {path.name}: {e}")
            return 0
        count = [0]

        def _processa(nodo, topic_corrente):
            tag = nodo.tag.lower()
            if tag == "topic":
                nuovo_topic = self._normalizza(nodo.attrib.get("name", "*"))
                for figlio in nodo:
                    _processa(figlio, nuovo_topic)
            elif tag == "category":
                cat = self._parse_categoria(nodo, topic_corrente, path)
                if cat:
                    self._categorie.append(cat)
                    count[0] += 1
            else:
                for figlio in nodo:
                    _processa(figlio, topic_corrente)

        _processa(root, "*")
        print(f"[AIML] Caricato {path.name}: {count[0]} categorie")
        return count[0]

    def carica_cartella(self, cartella):
        cartella = Path(cartella)
        if not cartella.exists():
            print(f"[AIML] Cartella non trovata: {cartella}")
            return 0
        totale = 0
        for path in sorted(cartella.glob("*.aiml")):
            totale += self.carica_file(path)
        print(f"[AIML] Totale categorie caricate: {totale}")
        return totale

    def scarica_tutto(self):
        self._categorie.clear()
        self._that         = "*"
        self._topic        = "*"
        self._that_history.clear()
        self._input_history.clear()

    # ── Parsing categoria ─────────────────────────────────────────────────

    def _parse_categoria(self, elem, topic_contenitore, path):
        pattern_elem  = elem.find("pattern")
        template_elem = elem.find("template")
        if pattern_elem is None or template_elem is None:
            return None
        pattern_testo = self._testo_completo(pattern_elem).strip()
        if not pattern_testo:
            return None
        that_elem = elem.find("that")
        that = self._normalizza(
            self._testo_completo(that_elem).strip()
            if that_elem is not None else "*"
        )
        return Categoria(
            pattern  = self._normalizza(pattern_testo),
            that     = that,
            topic    = topic_contenitore,
            template = template_elem,
            avatar   = template_elem.attrib.get("avatar", None),
            menu     = template_elem.attrib.get("menu",   None),
            file     = str(path),
        )

    # ── Risposta pubblica ─────────────────────────────────────────────────

    def rispondi(self, testo_utente):
        self._srai_depth   = 0
        self._srai_avatar  = None
        self._srai_comando = None
        self._srai_menu    = None
        # Aggiorna storico input
        self._input_history.insert(0, testo_utente)
        if len(self._input_history) > _MAX_HISTORY:
            self._input_history.pop()
        return self._match_e_rispondi(testo_utente)

    # ── Match e risposta ──────────────────────────────────────────────────

    def _match_e_rispondi(self, testo_utente):
        if self._srai_depth > _MAX_SRAI_DEPTH:
            print("[AIML] Ricorsione srai troppo profonda")
            return None
        input_norm = self._normalizza(testo_utente)
        cat, stars = self._trova_categoria(input_norm, testo_utente)
        if cat is None:
            return None
        testo = self._valuta_template(cat.template, stars, testo_utente)
        testo = testo.strip()
        # Aggiorna storico that
        that_norm = self._normalizza(testo) if testo else "*"
        self._that = that_norm
        self._that_history.insert(0, that_norm)
        if len(self._that_history) > _MAX_HISTORY:
            self._that_history.pop()
        return {
            "testo":   testo,
            "avatar":  cat.avatar or self._srai_avatar,
            "comando": cat.template.attrib.get("comando", None) or self._srai_comando,
            "menu":    cat.menu or self._srai_menu,
        }

    # ── Ricerca categoria ─────────────────────────────────────────────────

    def _trova_categoria(self, input_norm, input_originale=None):
        candidati = []
        for cat in self._categorie:
            if not self._match_that(cat.that):
                continue
            if not self._match_topic(cat.topic):
                continue
            stars = self._pattern_match(cat.pattern, input_norm, input_originale)
            if stars is None:
                continue
            candidati.append((self._priorita(cat), cat, stars))
        if not candidati:
            return None, []
        candidati.sort(key=lambda x: x[0])
        return candidati[0][1], candidati[0][2]

    def _priorita(self, cat):
        pattern = cat.pattern
        if "*" not in pattern and "_" not in pattern:
            tipo = 0
        elif "_" in pattern and "*" not in pattern:
            tipo = 1
        elif "*" in pattern and "_" not in pattern:
            tipo = 2
        else:
            tipo = 1 if pattern.index("_") < pattern.index("*") else 2
        return (tipo,
                0 if cat.that  != "*" else 1,
                0 if cat.topic != "*" else 1,
                -len(pattern))

    def _pattern_match(self, pattern, testo, testo_originale=None):
        """
        Matcha pattern contro testo.
        - Wildcard intermedi non-greedy, ultimo greedy
        - Spazi nel pattern diventano \\s* per gestire confini con wildcard
        """
        parti = re.split(r"([*_])", pattern)
        n_wc  = sum(1 for p in parti if p in ("*", "_"))
        wc_i  = 0
        rp    = []
        for parte in parti:
            if parte in ("*", "_"):
                wc_i += 1
                rp.append("(.*?)" if wc_i < n_wc else "(.*)")
            else:
                qp = ""
                for ch in parte:
                    if ch in "\\.+^${}()|[]":
                        qp += "\\" + ch
                    elif ch == " ":
                        qp += r"\s*"
                    else:
                        qp += ch
                rp.append(qp)
        regex = "^" + "".join(rp) + "$"
        stars_match = re.match(regex, testo, re.IGNORECASE | re.DOTALL)
        if not stars_match:
            return None
        if testo_originale is not None:
            m2 = re.match(regex, testo_originale, re.IGNORECASE | re.DOTALL)
            if m2:
                return list(m2.groups())
        return list(stars_match.groups())

    def _match_that(self, that_pattern):
        if that_pattern == "*":
            return True
        return self._pattern_match(that_pattern, self._that) is not None

    def _match_topic(self, topic_pattern):
        if topic_pattern == "*":
            return True
        return self._pattern_match(topic_pattern, self._topic) is not None

    # ── Valutazione template ──────────────────────────────────────────────

    def _valuta_template(self, template, stars, input_originale):
        risultato = []
        if template.text:
            risultato.append(template.text)
        for child in template:
            tag = child.tag.lower()

            # ── Wildcard / input / that ──────────────────────────────────
            if tag == "star":
                risultato.append(self._valuta_star(child, stars))

            elif tag == "topicstar":
                # wildcard del topic corrente (semplificato: restituisce il topic)
                risultato.append(self._topic)

            elif tag == "input":
                risultato.append(self._valuta_input(child, input_originale))

            elif tag == "that":
                risultato.append(self._valuta_that(child))

            # ── Predicati utente ─────────────────────────────────────────
            elif tag == "get":
                risultato.append(
                    self.get_predicato(child.attrib.get("name", "").lower())
                )

            elif tag == "set":
                nome   = child.attrib.get("name", "").lower()
                valore = self._valuta_template(child, stars, input_originale)
                self._predicati[nome] = valore.strip()
                if nome == "topic":
                    v = valore.strip()
                    self._topic = self._normalizza(v) if v else "*"
                # set NON aggiunge testo alla risposta

            # ── Predicati bot ────────────────────────────────────────────
            elif tag == "bot":
                nome = child.attrib.get("name", "").lower()
                risultato.append(self.get_bot_predicato(nome))

            # ── Think: esegue senza emettere testo ──────────────────────
            elif tag == "think":
                self._valuta_template(child, stars, input_originale)
                # think NON aggiunge nulla alla risposta

            # ── Redirect ─────────────────────────────────────────────────
            elif tag == "srai":
                risultato.append(self._valuta_srai(child, stars, input_originale))

            # ── Logica e selezione ───────────────────────────────────────
            elif tag == "random":
                risultato.append(self._valuta_random(child, stars, input_originale))

            elif tag == "condition":
                risultato.append(self._valuta_condition(child, stars, input_originale))

            # ── Trasformazioni testo ─────────────────────────────────────
            elif tag == "uppercase":
                risultato.append(
                    self._valuta_template(child, stars, input_originale).upper()
                )

            elif tag == "lowercase":
                risultato.append(
                    self._valuta_template(child, stars, input_originale).lower()
                )

            elif tag == "formal":
                risultato.append(
                    self._valuta_template(child, stars, input_originale).title()
                )

            elif tag == "sentence":
                t = self._valuta_template(child, stars, input_originale)
                risultato.append(t[:1].upper() + t[1:] if t else "")

            elif tag == "explode":
                t = self._valuta_template(child, stars, input_originale)
                risultato.append(" ".join(t))

            # ── Tag di sistema ───────────────────────────────────────────
            elif tag == "date":
                risultato.append(self._valuta_date(child))

            elif tag == "size":
                risultato.append(str(len(self._categorie)))

            elif tag == "version":
                risultato.append(self.get_bot_predicato("version"))

            elif tag == "id":
                risultato.append(
                    self.get_bot_predicato("id") or self._session_id
                )

            # ── Punteggiatura / spazio ───────────────────────────────────
            elif tag == "br":
                risultato.append("\n")

            elif tag == "p":
                risultato.append("\n\n")

            # ── Fallback: ricorsione su tag sconosciuti ───────────────────
            else:
                risultato.append(
                    self._valuta_template(child, stars, input_originale)
                )

            if child.tail:
                risultato.append(child.tail)

        return "".join(risultato)

    # ── Helper tag specifici ──────────────────────────────────────────────

    def _valuta_star(self, elem, stars):
        try:
            idx = int(elem.attrib.get("index", "1")) - 1
        except ValueError:
            idx = 0
        return stars[idx] if 0 <= idx < len(stars) else ""

    def _valuta_input(self, elem, input_corrente):
        """
        <input/>          → input corrente
        <input index="2"/> → secondo input precedente (1 = corrente)
        """
        try:
            idx = int(elem.attrib.get("index", "1")) - 1
        except ValueError:
            idx = 0
        if idx == 0:
            return input_corrente
        # idx 1 = turno precedente, ecc.
        hist_idx = idx - 1
        if 0 <= hist_idx < len(self._input_history):
            return self._input_history[hist_idx]
        return ""

    def _valuta_that(self, elem):
        """
        <that/>           → ultima risposta bot
        <that index="N"/> → N-esima risposta precedente (1 = ultima)
        """
        try:
            idx = int(elem.attrib.get("index", "1")) - 1
        except ValueError:
            idx = 0
        if idx == 0:
            return self._that
        hist_idx = idx - 1
        if 0 <= hist_idx < len(self._that_history):
            return self._that_history[hist_idx]
        return "*"

    def _valuta_date(self, elem):
        """
        <date/>                    → usa bot-predicato "dateformat"
        <date format="%d/%m/%Y"/>  → usa il formato sull'attributo
        """
        fmt = (elem.attrib.get("format")
               or self.get_bot_predicato("dateformat")
               or "%d/%m/%Y %H:%M")
        return datetime.now().strftime(fmt)

    def _valuta_srai(self, elem, stars, input_originale):
        testo = self._valuta_template(elem, stars, input_originale).strip()
        if not testo:
            return ""
        self._srai_depth += 1
        risposta = self._match_e_rispondi(testo)
        self._srai_depth -= 1
        if risposta:
            # Propaga avatar, comando e menu dalla risposta ricorsiva, se presenti
            if risposta.get("avatar"):
                self._srai_avatar = risposta["avatar"]
            if risposta.get("comando"):
                self._srai_comando = risposta["comando"]
            if risposta.get("menu"):
                self._srai_menu = risposta["menu"]
            return risposta["testo"]
        return ""

    def _valuta_random(self, elem, stars, input_originale):
        items = [c for c in elem if c.tag.lower() == "li"]
        if not items:
            return ""
        return self._valuta_template(random.choice(items), stars, input_originale)

    def _valuta_condition(self, elem, stars, input_originale):
        nome  = elem.attrib.get("name", "").lower()
        value = elem.attrib.get("value", None)
        # Forma compatta: <condition name="x" value="y">
        if nome and value is not None:
            if self.get_predicato(nome).upper() == value.upper():
                return self._valuta_template(elem, stars, input_originale)
            return ""
        # Forma a lista: <condition name="x"><li value="y">...</li><li>...</li>
        for li in (c for c in elem if c.tag.lower() == "li"):
            li_nome  = li.attrib.get("name", nome).lower()
            li_value = li.attrib.get("value", None)
            if li_value is None:
                # <li> senza value → ramo default
                return self._valuta_template(li, stars, input_originale)
            if self.get_predicato(li_nome).upper() == li_value.upper():
                return self._valuta_template(li, stars, input_originale)
        return ""

    # ── Utilità ───────────────────────────────────────────────────────────

    def _normalizza(self, testo):
        testo = testo.upper()
        # Normalizza apostrofo tipografico (' curly) in apostrofo dritto
        testo = testo.replace("\u2019", "'").replace("\u2018", "'")
        # Apostrofo usato come sostituto dell'accento a fine parola
        # es. "si'" → "si", "po'" → "po", "e'" → "e"
        testo = re.sub(r"([aeiou])'(?=\s|$)", r"\1", testo)
        # Rimuove i segni diacritici (accenti): sì→si, è→e, à→a, ù→u, ecc.
        testo = unicodedata.normalize("NFD", testo)
        testo = "".join(c for c in testo if unicodedata.category(c) != "Mn")
        # Punteggiatura e apostrofi residui → spazio
        testo = re.sub(r"[.,!?;:']", " ", testo)
        return re.sub(r"\s+", " ", testo).strip()

    def _testo_completo(self, elem):
        return "".join(elem.itertext())

    def info(self):
        return (
            f"Categorie caricate : {len(self._categorie)}\n"
            f"Predicati utente   : {list(self._predicati.keys())}\n"
            f"Predicati bot      : {list(self._bot_predicati.keys())}\n"
            f"Topic corrente     : {self._topic!r}\n"
            f"That corrente      : {self._that!r}\n"
            f"Session ID         : {self._session_id}"
        )

    def dump_categorie(self, n=20):
        for i, cat in enumerate(self._categorie[:n]):
            print(f"  [{i+1}] {cat}")
        if len(self._categorie) > n:
            print(f"  ... e altre {len(self._categorie) - n} categorie")


# ═════════════════════════════════════════════════════════════════════════════
#  Test
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=== Test AIMLParser ===\n")
    aiml_test = """<?xml version="1.0" encoding="UTF-8"?>
<aiml>
    <!-- ── Saluti ── -->
    <category>
        <pattern>CIAO</pattern>
        <template avatar="sorridente">Ciao <get name="nome_utente"/>! Come stai?</template>
    </category>
    <category>
        <pattern>CIAO *</pattern>
        <template><srai>CIAO</srai></template>
    </category>

    <!-- ── Predicati utente ── -->
    <category>
        <pattern>MI CHIAMO *</pattern>
        <template>Piacere <star/>!<set name="nome_ospite"><star/></set></template>
    </category>
    <category>
        <pattern>COME MI CHIAMO</pattern>
        <template><condition name="nome_ospite">
            <li value="">Non me lo hai ancora detto.</li>
            <li>Ti chiami <get name="nome_ospite"/>!</li>
        </condition></template>
    </category>

    <!-- ── Predicati bot ── -->
    <category>
        <pattern>COME TI CHIAMI</pattern>
        <template avatar="soddisfatto">Mi chiamo <bot name="name"/>.</template>
    </category>
    <category>
        <pattern>CHE VERSIONE SEI</pattern>
        <template>Sono la versione <version/> del parser.</template>
    </category>
    <category>
        <pattern>QUAL E IL TUO ID</pattern>
        <template>Il mio ID di sessione è <id/>.</template>
    </category>
    <category>
        <pattern>QUANTE CATEGORIE CONOSCI</pattern>
        <template>Ho <size/> categorie caricate.</template>
    </category>
    <category>
        <pattern>CHE ORA E</pattern>
        <template>Sono le <date format="%H:%M"/> del <date format="%d/%m/%Y"/>.</template>
    </category>
    <category>
        <pattern>CHE GIORNO E</pattern>
        <template>Oggi è <date format="%A %d %B %Y"/>.</template>
    </category>

    <!-- ── Trasformazioni testo ── -->
    <category>
        <pattern>MAIUSCOLO *</pattern>
        <template><uppercase><star/></uppercase></template>
    </category>
    <category>
        <pattern>MINUSCOLO *</pattern>
        <template><lowercase><star/></lowercase></template>
    </category>
    <category>
        <pattern>FORMALE *</pattern>
        <template><formal><star/></formal></template>
    </category>
    <category>
        <pattern>ESPLODI *</pattern>
        <template><explode><star/></explode></template>
    </category>
    <category>
        <pattern>FRASE *</pattern>
        <template><sentence><star/></sentence></template>
    </category>

    <!-- ── Storico input/that ── -->
    <category>
        <pattern>COSA HO DETTO</pattern>
        <template>Hai appena detto: "<input/>".</template>
    </category>
    <category>
        <pattern>COSA HO DETTO PRIMA</pattern>
        <template>Prima avevi detto: "<input index="2"/>".</template>
    </category>
    <category>
        <pattern>COSA HAI RISPOSTO</pattern>
        <template>Ho risposto: "<that/>".</template>
    </category>

    <!-- ── Topic ── -->
    <category>
        <pattern>COME STAI</pattern>
        <template avatar="sorridente">Bene grazie! E tu come stai?</template>
    </category>
    <category>
        <pattern>BENE</pattern>
        <that>* E TU COME STAI *</that>
        <template avatar="sorridente">Sono contento!</template>
    </category>
    <category>
        <pattern>PARLIAMO DI METEO</pattern>
        <template>Certo! Che tempo fa?<set name="topic">meteo</set></template>
    </category>
    <topic name="meteo">
        <category>
            <pattern>PIOVE</pattern>
            <template avatar="triste">Che peccato, tieniti al coperto!</template>
        </category>
        <category>
            <pattern>C E IL SOLE</pattern>
            <template avatar="sorridente">Ottimo, bella giornata!</template>
        </category>
    </topic>

    <!-- ── Newline ── -->
    <category>
        <pattern>DUE RIGHE</pattern>
        <template>Prima riga.<br/>Seconda riga.</template>
    </category>

    <!-- ── Fallback ── -->
    <category>
        <pattern>*</pattern>
        <template>Non ho capito: "<star/>".</template>
    </category>
</aiml>"""

    tmp = Path("_test_temp.aiml")
    tmp.write_text(aiml_test, encoding="utf-8")

    p = AIMLParser()
    p.set_predicato("nome_utente", "Emanuele")
    p.set_bot_predicato("name", "Assistente")
    p.carica_file(tmp)
    tmp.unlink()

    print(p.info())
    print()

    tests = [
        # Saluti / predicati utente
        "ciao",
        "ciao amico",
        "mi chiamo Emanuele",
        "come mi chiamo",
        # Predicati bot / sistema
        "come ti chiami",
        "che versione sei",
        "qual e il tuo id",
        "quante categorie conosci",
        "che ora e",
        "che giorno e",
        # Trasformazioni
        "maiuscolo ciao mondo",
        "minuscolo CIAO MONDO",
        "formale andrea rossi",
        "esplodi ciao",
        "frase buongiorno a tutti",
        # Storico
        "cosa ho detto",
        "cosa ho detto prima",
        "cosa hai risposto",
        # Topic / that
        "come stai",
        "bene",
        "parliamo di meteo",
        "piove",
        "c e il sole",
        # Newline
        "due righe",
        # Fallback
        "oggi piove forte",
    ]

    for inp in tests:
        r = p.rispondi(inp)
        if r:
            av = f"  [avatar: {r['avatar']}]" if r["avatar"] else ""
            print(f"U: {inp}\nA: {r['testo'].strip()}{av}")
        else:
            print(f"U: {inp}\nA: (nessun match)")
        print()
