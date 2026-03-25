"""
aiml_parser.py -- Parser AIML 1.x per myAssistente
2026 - Licenza: stessa del progetto myAssistente
"""

import re
import random
import xml.etree.ElementTree as ET
from pathlib import Path


class Categoria:
    __slots__ = ("pattern", "that", "topic", "template", "avatar", "file")
    def __init__(self, pattern, that, topic, template, avatar, file):
        self.pattern  = pattern
        self.that     = that
        self.topic    = topic
        self.template = template
        self.avatar   = avatar
        self.file     = file
    def __repr__(self):
        return f"<Categoria pattern={self.pattern!r} that={self.that!r} topic={self.topic!r}>"


class AIMLParser:
    def __init__(self):
        self._categorie  = []
        self._predicati  = {}
        self._topic      = "*"
        self._that       = "*"
        self._srai_depth = 0

    def set_predicato(self, nome, valore):
        self._predicati[nome.lower()] = str(valore)

    def get_predicato(self, nome):
        return self._predicati.get(nome.lower(), "")

    def set_topic(self, topic):
        self._topic = self._normalizza(topic)

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
        self._that  = "*"
        self._topic = "*"

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
            self._testo_completo(that_elem).strip() if that_elem is not None else "*"
        )
        return Categoria(
            pattern  = self._normalizza(pattern_testo),
            that     = that,
            topic    = topic_contenitore,
            template = template_elem,
            avatar   = template_elem.attrib.get("avatar", None),
            file     = str(path)
        )

    def rispondi(self, testo_utente):
        self._srai_depth = 0
        return self._match_e_rispondi(testo_utente)

    def _match_e_rispondi(self, testo_utente):
        if self._srai_depth > 10:
            print("[AIML] Ricorsione srai troppo profonda")
            return None
        input_norm = self._normalizza(testo_utente)
        cat, stars = self._trova_categoria(input_norm, testo_utente)
        if cat is None:
            return None
        testo = self._valuta_template(cat.template, stars, testo_utente)
        testo = testo.strip()
        self._that = self._normalizza(testo) if testo else "*"
        return {
            "testo":   testo,
            "avatar":  cat.avatar,
            "comando": cat.template.attrib.get("comando", None)
        }

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

    def _valuta_template(self, template, stars, input_originale):
        risultato = []
        if template.text:
            risultato.append(template.text)
        for child in template:
            tag = child.tag.lower()
            if tag == "star":
                risultato.append(self._valuta_star(child, stars))
            elif tag == "srai":
                risultato.append(self._valuta_srai(child, stars, input_originale))
            elif tag == "get":
                risultato.append(self.get_predicato(child.attrib.get("name", "").lower()))
            elif tag == "set":
                nome   = child.attrib.get("name", "").lower()
                valore = self._valuta_template(child, stars, input_originale)
                self._predicati[nome] = valore.strip()
                if nome == "topic":
                    v = valore.strip()
                    self._topic = self._normalizza(v) if v else "*"
                # set NON aggiunge testo alla risposta
            elif tag == "random":
                risultato.append(self._valuta_random(child, stars, input_originale))
            elif tag == "condition":
                risultato.append(self._valuta_condition(child, stars, input_originale))
            elif tag == "uppercase":
                risultato.append(self._valuta_template(child, stars, input_originale).upper())
            elif tag == "lowercase":
                risultato.append(self._valuta_template(child, stars, input_originale).lower())
            elif tag == "that":
                risultato.append(self._that)
            elif tag == "input":
                risultato.append(input_originale)
            else:
                risultato.append(self._valuta_template(child, stars, input_originale))
            if child.tail:
                risultato.append(child.tail)
        return "".join(risultato)

    def _valuta_star(self, elem, stars):
        try:
            idx = int(elem.attrib.get("index", "1")) - 1
        except ValueError:
            idx = 0
        return stars[idx] if 0 <= idx < len(stars) else ""

    def _valuta_srai(self, elem, stars, input_originale):
        testo = self._valuta_template(elem, stars, input_originale).strip()
        if not testo:
            return ""
        self._srai_depth += 1
        risposta = self._match_e_rispondi(testo)
        self._srai_depth -= 1
        return risposta["testo"] if risposta else ""

    def _valuta_random(self, elem, stars, input_originale):
        items = [c for c in elem if c.tag.lower() == "li"]
        if not items:
            return ""
        return self._valuta_template(random.choice(items), stars, input_originale)

    def _valuta_condition(self, elem, stars, input_originale):
        nome  = elem.attrib.get("name", "").lower()
        value = elem.attrib.get("value", None)
        if nome and value is not None:
            if self.get_predicato(nome).lower() == value.lower():
                return self._valuta_template(elem, stars, input_originale)
            return ""
        for li in (c for c in elem if c.tag.lower() == "li"):
            li_nome  = li.attrib.get("name", nome).lower()
            li_value = li.attrib.get("value", None)
            if li_value is None:
                return self._valuta_template(li, stars, input_originale)
            if self.get_predicato(li_nome).lower() == li_value.lower():
                return self._valuta_template(li, stars, input_originale)
        return ""

    def _normalizza(self, testo):
        testo = testo.lower()
        testo = re.sub(r"[.,!?;:]", " ", testo)
        return re.sub(r"\s+", " ", testo).strip()

    def _testo_completo(self, elem):
        return "".join(elem.itertext())

    def info(self):
        return (f"Categorie caricate : {len(self._categorie)}\n"
                f"Predicati          : {list(self._predicati.keys())}\n"
                f"Topic corrente     : {self._topic!r}\n"
                f"That corrente      : {self._that!r}")

    def dump_categorie(self, n=20):
        for i, cat in enumerate(self._categorie[:n]):
            print(f"  [{i+1}] {cat}")
        if len(self._categorie) > n:
            print(f"  ... e altre {len(self._categorie) - n} categorie")


if __name__ == "__main__":
    print("=== Test AIMLParser ===\n")
    aiml_test = """<?xml version="1.0" encoding="UTF-8"?>
<aiml>
    <category>
        <pattern>CIAO</pattern>
        <template avatar="sorridente">Ciao <get name="nome_utente"/>! Come stai?</template>
    </category>
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
    <category>
        <pattern>COME TI CHIAMI</pattern>
        <template avatar="soddisfatto">Mi chiamo <get name="nome_avatar"/>.</template>
    </category>
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
    <category>
        <pattern>CIAO *</pattern>
        <template><srai>CIAO</srai></template>
    </category>
    <category>
        <pattern>*</pattern>
        <template>Non ho capito: "<star/>".</template>
    </category>
</aiml>"""
    tmp = Path("_test_temp.aiml")
    tmp.write_text(aiml_test, encoding="utf-8")
    p = AIMLParser()
    p.set_predicato("nome_utente", "Mario")
    p.set_predicato("nome_avatar", "Assistente")
    p.carica_file(tmp)
    tmp.unlink()
    print(p.info())
    print()
    tests = [
        "ciao", "ciao amico", "mi chiamo Luigi", "come mi chiamo",
        "come ti chiami", "come stai", "bene",
        "parliamo di meteo", "piove", "c e il sole", "oggi piove forte",
    ]
    for inp in tests:
        r = p.rispondi(inp)
        if r:
            av = f"  [avatar: {r['avatar']}]" if r["avatar"] else ""
            print(f"U: {inp}\nA: {r['testo'].strip()}{av}")
        else:
            print(f"U: {inp}\nA: (nessun match)")
        print()
