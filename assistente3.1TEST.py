"""
Personal Desktop Assistant v3.1 STT/TTS + multiLANGUAGE + AI Integration
Assistente personale desktop v3.1 STT/TTS + multiLINGUA + Integrazione IA

    STT (microphone) multiplatform
    TTS (voice) multiplatform using pyttsx3
"""

import tkinter as tk
from tkinter import scrolledtext, filedialog
import json
import os
import re
import shutil
import subprocess
import sys
import random
import threading
import platform
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# STT / TTS / AI — importazioni opzionali (graceful degradation)
# ---------------------------------------------------------------------------
STT_DISPONIBILE = False
try:
    print("[STT] Importazione speech_recognition...")
    import speech_recognition as sr
    print("[STT] OK speech_recognition")

    print("[STT] Importazione sounddevice...")
    import sounddevice as sd
    print("[STT] OK sounddevice")

    print("[STT] Importazione numpy...")
    import numpy as np
    print("[STT] OK numpy")

    print("[STT] Verifica dispositivi audio...")
    _devs = sd.query_devices()
    print(f"[STT] OK dispositivi audio: {len(_devs)} trovati")

    STT_DISPONIBILE = True
    print("[STT] STT ABILITATO")
except ImportError as _e:
    print(f"[STT] Libreria mancante: {_e}")
except Exception as _e:
    print(f"[STT] Errore runtime: {type(_e).__name__}: {_e}")

# TTS con pyttsx3 (multipiattaforma)
TTS_DISPONIBILE = False
try:
    print("[TTS] Importazione pyttsx3...")
    import pyttsx3
    print("[TTS] OK pyttsx3")
    TTS_DISPONIBILE = True
except ImportError as _e:
    print(f"[TTS] Libreria pyttsx3 non disponibile: {_e}")

# AI Integration (opzionale)
AI_DISPONIBILE = False
try:
    print("[AI] Importazione openai...")
    import openai
    print("[AI] OK openai")
    AI_DISPONIBILE = True
except ImportError:
    try:
        print("[AI] Tentativo importazione google.generativeai...")
        import google.generativeai as genai
        print("[AI] OK google.generativeai")
        AI_DISPONIBILE = True
    except ImportError:
        print("[AI] Nessuna libreria AI trovata")

# ---------------------------------------------------------------------------
# PERCORSI — compatibile con script Python e con eseguibile PyInstaller
# ---------------------------------------------------------------------------
def _base_dir() -> Path:
    """
    Restituisce la cartella dell'eseguibile (o dello script).
    Con PyInstaller --onedir:  cartella dist/Assistente/
    Con PyInstaller --onefile: cartella temporanea sys._MEIPASS (NON usare)
    Con script Python normale: cartella del file .py
    """
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent

BASE_DIR     = _base_dir()
INTERNAL_DIR = BASE_DIR / "_dati"
ASSET_DIR    = INTERNAL_DIR / "asset" / "avatar"
MEM_FILE     = INTERNAL_DIR / "memory.json"      # Rinominato in inglese
CFG_FILE     = INTERNAL_DIR / "config.json"      # Rinominato in inglese

for d in [INTERNAL_DIR, ASSET_DIR, INTERNAL_DIR / "asset"]:
    d.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# CONFIGURAZIONE DEFAULT (con nuove sezioni)
# ---------------------------------------------------------------------------
DEFAULT_CONFIG = {
    "nome_avatar":   "Assistente",
    "nome_utente":   "utente",
    "avatar_iniziale": "benvenuto",
    "avatar_random": ["sorridente", "soddisfatto"],
    "avatar_finale": "ciao.mp4",
    "frase_finale":  "Ci vediamo presto!",
    "lingua":        "it",
    
    # Nuova sezione TTS
    "tts_config": {
        "engine": "auto",      # auto, sapi5, nsss, espeak
        "rate": 150,           # velocità di lettura (parole/minuto)
        "volume": 0.9,         # volume 0.0-1.0
        "pitch": 50,           # tono (non supportato da tutti i motori)
        "voice_gender": "auto" # auto, male, female
    },
    
    # Nuova sezione STT
    "stt_config": {
        "soglia_rumore": 200,      # STT_SOGLIA (200 per Windows, 2000 per Linux)
        "sample_rate": 16000,      # STT_SAMPLERATE
        "max_secondi": 10,         # STT_MAX_SECONDI
        "silenzio_secondi": 0.5,   # STT_SILENZIO_S
        "lingua": "it-IT"          # Lingua per il riconoscimento
    },
    
    # Nuova sezione AI
    "ai_config": {
        "enabled": False,
        "provider": "openai",      # openai, gemini
        "api_key": "",
        "model": "gpt-3.5-turbo",  # o "gemini-pro"
        "temperature": 0.7,
        "max_tokens": 500,
        "fallback_to_ai": True     # Usa AI quando comando non riconosciuto
    },
    
    "alias_comandi": {
        "dammi":  ["dimmi"],
        "apri":   ["lancia"],
        "cerca":  [],
        "ricorda": [],
        "impara":  [],
        "elenca":  [],
        "modifica": [],
        "elimina":  [],
        "copia":    [],
        "configura": ["config", "impostazioni", "settings"],
        "aiuto":    ["help"],
        "esci":     ["chiudi", "arrivederci"]
    },
    
    "risposte_fisse": {
        "grazie":  "Prego, {nome_utente}!",
        "ciao":    "Ciao, {nome_utente}!",
        "come stai": "Sto benissimo, grazie!"
    },
    
    "shortcut": [
        {"etichetta": "Aiuto", "comando": "aiuto"},
        {"etichetta": "Elenca memoria", "comando": "elenca"},
        {"etichetta": "Configura", "comando": "configura"},
        {"etichetta": "Chiudi assistente", "comando": "esci"}
    ]
}

def carica_config() -> dict:
    if CFG_FILE.exists():
        try:
            with open(CFG_FILE, encoding="utf-8") as f:
                cfg = json.load(f)
            for k, v in DEFAULT_CONFIG.items():
                if k not in cfg:
                    cfg[k] = v
                elif isinstance(v, dict) and k in cfg:
                    # Merge dizionari nidificati
                    for sub_k, sub_v in v.items():
                        if sub_k not in cfg[k]:
                            cfg[k][sub_k] = sub_v
            return cfg
        except Exception:
            pass
    
    with open(CFG_FILE, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)
    return DEFAULT_CONFIG.copy()

# ---------------------------------------------------------------------------
# LOCALIZZAZIONE (aggiornata con articoli/stop-words)
# ---------------------------------------------------------------------------
def carica_lingua(codice: str) -> dict:
    """
    Carica il file lang_XX.json corrispondente al codice lingua.
    Se non trovato restituisce il fallback italiano embedded.
    """
    path = INTERNAL_DIR / f"lang_{codice}.json"
    if path.exists():
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[LINGUA] Errore caricamento {path.name}: {e}")
    
    path2 = BASE_DIR / f"lang_{codice}.json"
    if path2.exists():
        try:
            with open(path2, encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[LINGUA] Errore caricamento {path2.name}: {e}")
    
    print(f"[LINGUA] File lang_{codice}.json non trovato, uso italiano embedded.")
    return _LANG_IT_FALLBACK.copy()

# Fallback minimo italiano — usato solo se lang_it.json manca del tutto
_LANG_IT_FALLBACK = {
    "btn_invia": "Invia", 
    "titolo_finestra": "Assistente – {nome_avatar}",
    "label_comandi": "COMANDI", 
    "label_shortcut": "SHORTCUT",
    "panel_dammi": "dammi ...", 
    "panel_apri": "apri ...",
    "panel_cerca": "cerca ...", 
    "panel_elenca": "elenca memoria",
    "panel_aiuto": "aiuto", 
    "panel_esci": "esci",
    "panel_configura": "configura",
    "panel_sep_memoria": "── GESTISCI MEMORIA ──", 
    "panel_impara": "impara",
    "panel_ricorda": "ricorda ...", 
    "panel_ricorda_img": "ricorda immagine",
    "panel_modifica": "modifica ...", 
    "panel_elimina": "elimina ...",
    "panel_copia": "copia ...",
    
    # Articoli/stop-words per parsing più naturale
    "articoli": ["il", "lo", "la", "i", "gli", "le", "un", "una", "uno", 
                 "del", "della", "dei", "degli", "delle", "al", "allo", 
                 "alla", "ai", "agli", "alle", "dal", "dallo", "dalla", 
                 "dai", "dagli", "dalle", "col", "coi", "su", "per", "con"],
    
    "avvio_saluto": "Ciao {nome_utente}! Sono {nome_avatar}.\nDigita 'aiuto' per vedere cosa posso fare.",
    "avvio_memoria_vuota": "Purtroppo la mia memoria è vuota.",
    "apri_subito": "Apro subito", 
    "apri_cosa": "Che cosa devo aprire?",
    "apri_non_trovato": "Non ho trovato '{q}' in memoria.",
    "apri_errore": "Non riesco ad aprire: {err}",
    "dammi_cosa": "Cosa devo darti? Dimmi il nome.",
    "dammi_non_trovato": "Non ho trovato nulla per '{q}'.",
    "dammi_risultato_1": "I dati di '{nome}' ({soggetto}):",
    "dammi_risultati_n": "Ho trovato {n} voci:",
    "cerca_cosa": "Cosa devo cercare?", 
    "cerca_non_trovato": "Nessun risultato per '{q}'.",
    "cerca_trovato": "Ho trovato {n} risultato/i per '{q}':",
    "elimina_cosa": "Cosa devo eliminare?", 
    "elimina_non_trovato": "Non ho trovato '{q}'.",
    "elimina_conferma": "Vuoi eliminare:\n{entry}\nScrivi 'sì' per confermare.",
    "elimina_ok": "'{nome}' eliminato.", 
    "elimina_annullato": "Eliminazione annullata.",
    "elimina_si": ["sì", "si", "s", "yes"],
    "modifica_cosa": "Quale voce devo modificare?", 
    "modifica_non_trovato": "Non ho trovato '{q}'.",
    "modifica_trovata": "Voce trovata:\n{entry}\nQuale campo?",
    "modifica_campo_no": "Campo non riconosciuto: '{campo}'.\nScegli tra: {campi}",
    "modifica_valore_chiedi": "Inserisci il nuovo valore per '{campo}':",
    "modifica_ok": "Modificato! '{campo}' = {valore}", 
    "modifica_errore": "Errore: voce non trovata.",
    "elenca_vuota": "La memoria è vuota.", 
    "elenca_intestazione": "Ho {n} voce/i in memoria:",
    "copia_cosa": "Cosa devo copiare?", 
    "copia_non_trovato": "Non ho trovato '{q}'.",
    "copia_ok": "Copiato:\n  {dati}",
    "ricorda_chiedi_nome": "Che cosa devo ricordare? Dimmi il nome:",
    "ricorda_chiedi_dati": "Dimmi i dati per '{nome}':", 
    "ricorda_ok": "Fatto! '{nome}' salvato.",
    "ricorda_img_titolo": "Seleziona immagine", 
    "ricorda_img_nessuna": "Nessuna immagine selezionata.",
    "ricorda_img_nome": "Nome per l'immagine?", 
    "ricorda_img_tag": "Descrizione (tag)?",
    "ricorda_img_ok": "Immagine '{nome}' salvata.",
    "impara_intro": "Inserimento guidato.\nScrivi 'salta' per i campi opzionali, 'fine' per annullare.",
    "impara_annullato": "Inserimento annullato.", 
    "impara_obbligatorio": "Il campo '{campo}' è obbligatorio.",
    "impara_salvato": "Salvato! '{nome}'.\n\nAltro elemento? (sì / no)",
    "impara_completato": "Inserimento completato.", 
    "impara_si": ["sì", "si", "s", "yes"],
    "impara_fine": "fine", 
    "impara_salta": "salta",
    "impara_prompt_nome": "Nome (obbligatorio):",
    "impara_prompt_alias": "Alias (opzionale — 'salta' per saltare):",
    "impara_prompt_soggetto": "Soggetto (opzionale — 'salta' per usare il tuo nome):",
    "impara_prompt_dati": "Dati da memorizzare (obbligatorio):",
    "impara_prompt_tag": "Tag (opzionale — 'salta' per saltare):",
    "impara_prompt_avatar": "Avatar (opzionale — 'salta' per 'sorridente'):",
    
    # Nuove stringhe per comando configura
    "configura_intro": "Configurazione guidata. Parametri disponibili:",
    "configura_chiedi_valore": "Inserisci il nuovo valore per '{param}':",
    "configura_mostra_valore": "{param} attuale = '{valore}'",
    "configura_aggiornato": "Parametro '{param}' aggiornato a '{valore}'",
    "configura_lista": "Parametri configurabili:",
    "configura_parametro_non_trovato": "Parametro '{param}' non trovato.",
    "configura_proseguire": "Vuoi configurare altri parametri? (sì/no)",
    "configura_fine": "Configurazione completata.",
    "configura_annullato": "Configurazione annullata.",
    "configura_cosa": "Cosa vuoi configurare? Usa 'configura lista' per vedere i parametri.",
    "configura_nome_avatar": "nome assistente",
    "configura_nome_utente": "nome utente",
    "configura_lingua": "lingua",
    "configura_tts_rate": "velocità voce TTS",
    "configura_tts_volume": "volume TTS",
    
    # Stringhe AI
    "ai_pensando": "Sto pensando...",
    "ai_errore": "Errore nella comunicazione con l'IA: {errore}",
    "ai_non_disponibile": "Funzione IA non disponibile o non configurata.",
    "ai_chiedi_chiave": "Inserisci la chiave API per {provider}:",
    
    "aiuto_testo": "Comandi: ricorda · impara · apri · dammi · cerca · elenca · modifica · elimina · copia · configura · lingua · esci · aiuto",
    "non_capito": "Non ho capito. Parole chiave: ricorda · impara · apri · dammi · cerca · elenca · modifica · elimina · copia · configura · esci · aiuto",
    "lingua_ok": "Lingua impostata su: {lingua}", 
    "lingua_non_trovata": "File lingua '{file}' non trovato.",
    "lingua_uso": "Uso: lingua <codice>  (es: lingua en)",
    "stt_nessun_audio": "Nessun audio rilevato.", 
    "stt_non_capito": "Non ho capito, riprova.",
    "stt_errore": "Errore STT: {err}", 
    "stt_mic_errore": "Microfono non disponibile: {err}",
    "shortcut_nessuno": "Nessuno shortcut configurato.",
    "label_lingua": "LINGUA", 
    "lingua_nessuna": "Nessun file lingua\ntrovato in _dati/",
    "lingua_stt": "it-IT",
}

# ---------------------------------------------------------------------------
# MEMORIA
# ---------------------------------------------------------------------------
def carica_memoria() -> list:
    if MEM_FILE.exists():
        try:
            with open(MEM_FILE, encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            backup = MEM_FILE.with_suffix(".json.bak")
            shutil.copy2(MEM_FILE, backup)
            with open(MEM_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)
            print(f"[AVVISO] memory.json corrotto — backup in {backup.name}.")
            return []
    return []

def salva_memoria(mem: list):
    if MEM_FILE.exists():
        shutil.copy2(MEM_FILE, MEM_FILE.with_suffix(".json.bak"))
    with open(MEM_FILE, "w", encoding="utf-8") as f:
        json.dump(mem, f, indent=2, ensure_ascii=False)

def cerca_in_memoria(mem: list, query: str) -> list:
    """Ricerca su nome e alias prima, poi su soggetto, dati e tag."""
    q = query.lower()

    prioritari = [
        e for e in mem
        if q in e.get("nome", "").lower()
        or q in e.get("alias", "").lower()
    ]
    if prioritari:
        return prioritari

    secondari = [
        e for e in mem
        if q in " ".join([
            e.get("soggetto", ""), str(e.get("dati", "")),
            " ".join(e.get("tag", [])) if isinstance(e.get("tag"), list)
            else str(e.get("tag", ""))
        ]).lower()
    ]
    return secondari

def cerca_per_tag(mem: list, tag: str) -> list:
    """Restituisce tutte le voci che hanno esattamente questo tag."""
    t = tag.lower()
    risultati = []
    for e in mem:
        tags = e.get("tag", [])
        if isinstance(tags, list):
            if any(t in tg.lower() for tg in tags):
                risultati.append(e)
        elif isinstance(tags, str) and t in tags.lower():
            risultati.append(e)
    return risultati

# ---------------------------------------------------------------------------
# PARSING COMANDI (con rimozione articoli)
# ---------------------------------------------------------------------------
COMANDI = ["ricorda", "apri", "dammi", "cerca", "elimina", "modifica",
           "elenca", "aiuto", "copia", "impara", "esci", "lingua", "configura"]

def rimuovi_articoli(testo: str, articoli: list) -> str:
    """Rimuove gli articoli/stop-words dal testo."""
    parole = testo.split()
    parole_filtrate = [p for p in parole if p.lower() not in articoli]
    return " ".join(parole_filtrate)

def estrai_alias(testo: str):
    m = re.search(r'\(([^)]+)\)', testo)
    if m:
        return m.group(1).strip(), testo.replace(m.group(0), "").strip()
    return None, testo

def estrai_soggetto(testo: str, nome_utente: str) -> tuple:
    # "mio" / "mia" → nome utente
    t = re.sub(r'\b(mio|mia)\b', '', testo, flags=re.IGNORECASE).strip()
    if t != testo:
        return nome_utente, t

    # "di Nome" → soggetto esplicito
    m = re.search(r'\bdi\s+([A-Z][a-z]+)', testo)
    if m:
        return m.group(1), testo.replace(m.group(0), "").strip()

    # Nome proprio alla fine della frase (es. "codice fiscale Roberta")
    m = re.search(r'\b([A-Z][a-z]{2,})\s*$', testo)
    if m:
        nome_proprio = m.group(1)
        parole_comuni = {"Fatto", "Link", "Cose", "Note", "Dati", "File",
                         "Cartella", "Salute", "Casa", "Lavoro", nome_utente}
        if nome_proprio not in parole_comuni:
            return nome_proprio, testo[:m.start()].strip()

    return nome_utente, testo

def parse_comando(testo: str, nome_utente: str, alias_comandi: dict = None, articoli: list = None) -> dict:
    testo = testo.strip()
    
    # Rimuovi articoli se forniti
    if articoli:
        testo = rimuovi_articoli(testo, articoli)
    
    parole = testo.split()
    if not parole:
        return {"comando": None, "confidenza": 0}

    cmd = parole[0].lower()

    # Risolve alias configurabili (es. "dimmi" → "dammi")
    if alias_comandi:
        for comando_base, alias_list in alias_comandi.items():
            if cmd in [a.lower() for a in alias_list]:
                cmd = comando_base
                break

    if cmd not in COMANDI:
        return {"comando": "sconosciuto", "testo_originale": testo, "confidenza": 0}

    resto = " ".join(parole[1:]).strip()
    alias, resto = estrai_alias(resto)
    soggetto, resto = estrai_soggetto(resto, nome_utente)

    dati_inline = None
    parti_nome, parti_dati = [], []
    for tok in resto.split():
        e_codice   = bool(re.match(r'^[A-Z0-9]{5,}$', tok))
        e_percorso = ('\\' in tok or ('/' in tok and len(tok) > 5) or
                      (tok.count('.') >= 1 and len(tok) > 6))
        if e_codice or e_percorso:
            parti_dati.append(tok)
        else:
            (parti_nome if not parti_dati else parti_dati).append(tok)

    if parti_dati:
        dati_inline = " ".join(parti_dati)
        resto = " ".join(parti_nome)

    nome = re.sub(r'\b(il|la|lo|i|gli|le|per|del|della|di|un|una)\b',
                  '', resto, flags=re.IGNORECASE).strip()
    nome = re.sub(r'\s+', ' ', nome).strip()

    return {
        "comando":         cmd,
        "nome":            nome,
        "alias":           alias,
        "soggetto":        soggetto,
        "dati_inline":     dati_inline,
        "confidenza":      1 if nome else 0.5,
        "testo_originale": testo
    }

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------
def avatar_random(cfg: dict) -> str:
    return random.choice(cfg.get("avatar_random", ["sorridente"]))

def formatta_entry(entry: dict) -> str:
    righe = []
    for campo in ["nome", "alias", "soggetto"]:
        if entry.get(campo):
            righe.append(f"  {campo}: {entry[campo]}")
    dati = entry.get("dati", "")
    for riga in str(dati).split("\n"):
        righe.append(f"  {riga}")
    tags = entry.get("tag")
    if tags:
        tag_str = ", ".join(tags) if isinstance(tags, list) else str(tags)
        righe.append(f"  tag: {tag_str}")
    righe.append(f"  [avatar: {entry.get('avatar','')}]")
    return "\n".join(righe)

# ---------------------------------------------------------------------------
# PANNELLO COMANDI LATERALE (aggiornato)
# ---------------------------------------------------------------------------
COMANDI_PANEL = [
    ("dammi ...",         "dammi "),
    ("apri ...",          "apri "),
    ("cerca ...",         "cerca "),
    ("elenca memoria",     "elenca"),
    ("configura",         "configura"),
    ("aiuto",             "aiuto"),
    ("esci",              "esci"),
    ("── GESTISCI MEMORIA ──", None),
    ("impara",            "impara"),
    ("ricorda ...",       "ricorda "),
    ("ricorda immagine",  "ricorda questa immagine"),
    ("modifica ...",      "modifica "),
    ("elimina ...",       "elimina "),
    ("copia ...",         "copia "),
]

# ---------------------------------------------------------------------------
# CLASSE PRINCIPALE
# ---------------------------------------------------------------------------
class Assistente:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.cfg  = carica_config()
        self.mem  = carica_memoria()
        self.L    = carica_lingua(self.cfg.get("lingua", "it"))
        self.stato     = "idle"
        self.dati_temp = {}
        self._video_after_id  = None
        self._video_frames    = []
        self._pannello_aperto = True

        # Cronologia comandi (stile shell)
        self._history: list[str] = []
        self._history_idx: int   = -1

        # TTS con pyttsx3
        self._tts_attivo  = True
        self._tts_engine  = None
        self._inizializza_tts()

        # STT
        self._stt_ascolto    = False
        self._stt_recognizer = sr.Recognizer() if STT_DISPONIBILE else None
        self._inizializza_stt()

        # AI
        self._ai_client = None
        self._inizializza_ai()

        self._costruisci_ui()
        self._mostra_avatar(self.cfg.get("avatar_iniziale", "benvenuto"))
        self._messaggio_avvio()

    # ------------------------------------------------------------------
    # INIZIALIZZAZIONE COMPONENTI
    # ------------------------------------------------------------------
    def _inizializza_tts(self):
        """Inizializza pyttsx3 con i parametri dal config."""
        if not TTS_DISPONIBILE:
            print("[TTS] pyttsx3 non disponibile")
            return
        
        try:
            tts_cfg = self.cfg.get("tts_config", {})
            engine_type = tts_cfg.get("engine", "auto")
            
            # Su macOS, pyttsx3 usa automaticamente NSSpeechSynthesizer
            # Su Linux, richiede espeak installato
            self._tts_engine = pyttsx3.init(driverName=engine_type if engine_type != "auto" else None)
            
            # Imposta velocità (rate)
            rate = tts_cfg.get("rate", 150)
            self._tts_engine.setProperty('rate', rate)
            
            # Imposta volume
            volume = tts_cfg.get("volume", 0.9)
            self._tts_engine.setProperty('volume', volume)
            
            # Seleziona voce in base alla lingua e genere
            self._seleziona_voce_tts()
            
            print(f"[TTS] Inizializzato: rate={rate}, volume={volume}")
        except Exception as e:
            print(f"[TTS] Errore inizializzazione: {e}")
            self._tts_engine = None

    def _seleziona_voce_tts(self):
        """Seleziona la voce TTS più adatta alla lingua configurata."""
        if not self._tts_engine:
            return
        
        try:
            voci = self._tts_engine.getProperty('voices')
            lingua = self.cfg.get("lingua", "it")
            tts_cfg = self.cfg.get("tts_config", {})
            gender = tts_cfg.get("voice_gender", "auto")
            
            voce_selezionata = None
            
            for voce in voci:
                nome = voce.name.lower()
                id_voce = voce.id.lower()
                
                # Criteri di selezione per lingua
                if lingua == "it" and ("italian" in nome or "italiano" in nome or "it-" in id_voce):
                    voce_selezionata = voce
                    break
                elif lingua == "en" and ("english" in nome or "en-" in id_voce or "us-" in id_voce):
                    voce_selezionata = voce
                    break
                elif lingua == "fr" and ("french" in nome or "fr-" in id_voce):
                    voce_selezionata = voce
                    break
                elif lingua == "de" and ("german" in nome or "de-" in id_voce):
                    voce_selezionata = voce
                    break
                elif lingua == "es" and ("spanish" in nome or "es-" in id_voce):
                    voce_selezionata = voce
                    break
            
            if voce_selezionata:
                self._tts_engine.setProperty('voice', voce_selezionata.id)
                print(f"[TTS] Voce selezionata: {voce_selezionata.name}")
        except Exception as e:
            print(f"[TTS] Errore selezione voce: {e}")

    def _inizializza_stt(self):
        """Inizializza STT con parametri dal config."""
        if not STT_DISPONIBILE:
            return
        
        stt_cfg = self.cfg.get("stt_config", {})
        
        # Imposta soglia in base al sistema operativo se non specificata
        if "soglia_rumore" not in stt_cfg:
            if platform.system() == "Linux":
                stt_cfg["soglia_rumore"] = 2000
            else:
                stt_cfg["soglia_rumore"] = 200
        
        self._STT_SOGLIA = stt_cfg.get("soglia_rumore", 200)
        self._STT_SAMPLERATE = stt_cfg.get("sample_rate", 16000)
        self._STT_MAX_SECONDI = stt_cfg.get("max_secondi", 10)
        self._STT_SILENZIO_S = stt_cfg.get("silenzio_secondi", 0.5)
        
        print(f"[STT] Config: soglia={self._STT_SOGLIA}, sample_rate={self._STT_SAMPLERATE}")

    def _inizializza_ai(self):
        """Inizializza il client AI se configurato."""
        if not AI_DISPONIBILE:
            return
        
        ai_cfg = self.cfg.get("ai_config", {})
        if not ai_cfg.get("enabled", False):
            return
        
        provider = ai_cfg.get("provider", "openai")
        api_key = ai_cfg.get("api_key", "")
        
        if not api_key:
            print("[AI] Chiave API non configurata")
            return
        
        try:
            if provider == "openai":
                openai.api_key = api_key
                self._ai_client = {"provider": "openai", "model": ai_cfg.get("model", "gpt-3.5-turbo")}
                print("[AI] OpenAI configurato")
            elif provider == "gemini":
                genai.configure(api_key=api_key)
                model = ai_cfg.get("model", "gemini-pro")
                self._ai_client = genai.GenerativeModel(model)
                print("[AI] Google Gemini configurato")
        except Exception as e:
            print(f"[AI] Errore inizializzazione: {e}")

    # ------------------------------------------------------------------
    # LOCALIZZAZIONE
    # ------------------------------------------------------------------
    def _t(self, chiave: str, **kw) -> str:
        """Restituisce la stringa localizzata, con eventuali sostituzioni."""
        testo = self.L.get(chiave, chiave)
        if kw:
            try:
                testo = testo.format(**kw)
            except KeyError:
                pass
        return testo

    # ------------------------------------------------------------------
    # ESPANSIONE SEGNAPOSTO RISPOSTE FISSE
    # ------------------------------------------------------------------
    def _espandi_segnaposto(self, testo: str) -> str:
        """
        Sostituisce i segnaposto nelle risposte fisse del config.
        Segnaposto supportati:
          {nome_utente}  → nome utente dalla configurazione
          {nome_avatar}  → nome avatar dalla configurazione
          {ora}          → ora corrente  (es. 14:35)
          {data}         → data corrente (es. lunedì 17 marzo 2025)
          {giorno}       → solo il giorno della settimana
          {data_breve}   → data in formato gg/mm/aaaa
        """
        now = datetime.now()

        # Nomi dei giorni e mesi in base alla lingua configurata
        lingua = self.cfg.get("lingua", "it")
        if lingua == "it":
            giorni  = ["lunedì","martedì","mercoledì","giovedì",
                       "venerdì","sabato","domenica"]
            mesi    = ["gennaio","febbraio","marzo","aprile","maggio",
                       "giugno","luglio","agosto","settembre",
                       "ottobre","novembre","dicembre"]
            data_estesa = f"{giorni[now.weekday()]} {now.day} {mesi[now.month-1]} {now.year}"
        elif lingua == "en":
            data_estesa = now.strftime("%A, %B %d %Y")
        elif lingua == "fr":
            giorni = ["lundi","mardi","mercredi","jeudi",
                      "vendredi","samedi","dimanche"]
            mesi   = ["janvier","février","mars","avril","mai",
                      "juin","juillet","août","septembre",
                      "octobre","novembre","décembre"]
            data_estesa = f"{giorni[now.weekday()]} {now.day} {mesi[now.month-1]} {now.year}"
        else:
            data_estesa = now.strftime("%A %d %B %Y")

        valori = {
            "nome_utente": self.cfg.get("nome_utente", ""),
            "nome_avatar":  self.cfg.get("nome_avatar", ""),
            "ora":          now.strftime("%H:%M"),
            "data":         data_estesa,
            "giorno":       data_estesa.split()[0],   # solo il giorno della settimana
            "data_breve":   now.strftime("%d/%m/%Y"),
        }

        try:
            return testo.format(**valori)
        except KeyError as e:
            # Segnaposto sconosciuto: lascia la stringa originale e logga
            print(f"[RISPOSTE_FISSE] Segnaposto non riconosciuto: {e} — controlla config.json")
            return testo
        except Exception as e:
            print(f"[RISPOSTE_FISSE] Errore espansione: {e}")
            return testo

    # ------------------------------------------------------------------
    # MESSAGGIO AVVIO
    # ------------------------------------------------------------------
    def _messaggio_avvio(self):
        self._scrivi_risposta(
            self._t("avvio_saluto",
                    nome_utente=self.cfg["nome_utente"],
                    nome_avatar=self.cfg["nome_avatar"])
        )
        if not self.mem:
            self._scrivi_risposta(self._t("avvio_memoria_vuota"))
            self._mostra_avatar("triste")

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------
    def _costruisci_ui(self):
        self.root.title(self._t("titolo_finestra", nome_avatar=self.cfg["nome_avatar"]))
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(True, True)

        # Frame principale orizzontale
        self.frame_main = tk.Frame(self.root, bg="#1e1e2e")
        self.frame_main.pack(fill=tk.BOTH, expand=True)

        # ── Colonna sinistra: chat ──────────────────────────────────────
        self.frame_chat = tk.Frame(self.frame_main, bg="#1e1e2e")
        self.frame_chat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.avatar_label = tk.Label(self.frame_chat, bg="#1e1e2e",
                                     width=300, height=300)
        self.avatar_label.pack(pady=(16, 4))

        tk.Label(self.frame_chat, text=self.cfg["nome_avatar"],
                 bg="#1e1e2e", fg="#cdd6f4",
                 font=("Segoe UI", 11, "bold")).pack()

        self.output = scrolledtext.ScrolledText(
            self.frame_chat, width=52, height=10,
            bg="#313244", fg="#cdd6f4",
            font=("Segoe UI", 10), wrap=tk.WORD,
            state=tk.DISABLED, relief=tk.FLAT,
            padx=8, pady=8
        )
        self.output.pack(padx=12, pady=8, fill=tk.BOTH, expand=True)

        frame_in = tk.Frame(self.frame_chat, bg="#1e1e2e")
        frame_in.pack(padx=12, pady=(0, 12), fill=tk.X)

        self.input_var = tk.StringVar()
        self.entry = tk.Entry(frame_in, textvariable=self.input_var,
                              bg="#45475a", fg="#cdd6f4",
                              font=("Segoe UI", 10),
                              insertbackground="#cdd6f4",
                              relief=tk.FLAT)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6, padx=(0, 6))
        self.entry.bind("<Return>",  lambda e: self._on_invia())
        self.entry.bind("<Up>",      lambda e: self._history_su())
        self.entry.bind("<Down>",    lambda e: self._history_giu())
        self.entry.focus_set()

        # Pulsante Invia localizzato
        tk.Button(frame_in, text=self._t("btn_invia"),
                  bg="#89b4fa", fg="#1e1e2e",
                  font=("Segoe UI", 10, "bold"),
                  relief=tk.FLAT, cursor="hand2",
                  command=self._on_invia
                  ).pack(side=tk.LEFT, ipady=6, ipadx=12)

        # Pulsante microfono STT
        self._btn_mic = tk.Button(
            frame_in, text="🎤",
            bg="#313244", fg="#cdd6f4",
            font=("Segoe UI", 11),
            relief=tk.FLAT, cursor="hand2",
            command=self._toggle_ascolto,
            state=tk.NORMAL if STT_DISPONIBILE else tk.DISABLED
        )
        self._btn_mic.pack(side=tk.LEFT, ipady=4, ipadx=8, padx=(6, 0))

        # Pulsante attiva/disattiva TTS
        self._btn_tts = tk.Button(
            frame_in, text="🔊",
            bg="#313244", fg="#cdd6f4",
            font=("Segoe UI", 11),
            relief=tk.FLAT, cursor="hand2",
            command=self._toggle_tts,
            state=tk.NORMAL if TTS_DISPONIBILE else tk.DISABLED
        )
        self._btn_tts.pack(side=tk.LEFT, ipady=4, ipadx=8, padx=(4, 0))

        self.btn_toggle = tk.Button(frame_in, text="▶",
                                    bg="#313244", fg="#cdd6f4",
                                    font=("Segoe UI", 10),
                                    relief=tk.FLAT, cursor="hand2",
                                    command=self._toggle_pannello)
        self.btn_toggle.pack(side=tk.LEFT, ipady=6, ipadx=8, padx=(6, 0))

        # ── Colonna destra: pannello comandi ───────────────────────────
        self.frame_pannello = tk.Frame(self.frame_main,
                                       bg="#181825", width=160)
        self.frame_pannello.pack(side=tk.RIGHT, fill=tk.Y)
        self.frame_pannello.pack_propagate(False)
        self._costruisci_pannello()

    def _costruisci_pannello(self):
        tk.Label(self.frame_pannello, text=self._t("label_comandi"),
                 bg="#181825", fg="#89b4fa",
                 font=("Segoe UI", 9, "bold")).pack(pady=(12, 4))

        # Pannello comandi localizzato dinamicamente
        comandi_panel = [
            (self._t("panel_dammi"),       "dammi "),
            (self._t("panel_apri"),        "apri "),
            (self._t("panel_cerca"),       "cerca "),
            (self._t("panel_elenca"),      "elenca"),
            (self._t("panel_configura"),   "configura"),
            (self._t("panel_aiuto"),       "aiuto"),
            (self._t("panel_esci"),        "esci"),
            (self._t("panel_sep_memoria"), None),
            (self._t("panel_impara"),      "impara"),
            (self._t("panel_ricorda"),     "ricorda "),
            (self._t("panel_ricorda_img"), "ricorda questa immagine"),
            (self._t("panel_modifica"),    "modifica "),
            (self._t("panel_elimina"),     "elimina "),
            (self._t("panel_copia"),       "copia "),
        ]

        for etichetta, valore in comandi_panel:
            if valore is None:
                tk.Label(self.frame_pannello, text=etichetta,
                         bg="#181825", fg="#6c7086",
                         font=("Segoe UI", 8)).pack(pady=(8, 2), padx=8, anchor="w")
            else:
                btn = tk.Button(
                    self.frame_pannello, text=etichetta,
                    bg="#313244", fg="#cdd6f4",
                    font=("Segoe UI", 9),
                    relief=tk.FLAT, cursor="hand2", anchor="w",
                    command=lambda c=valore: self._inserisci_comando(c)
                )
                btn.pack(fill=tk.X, padx=8, pady=2, ipady=3)
                btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#45475a"))
                btn.bind("<Leave>", lambda e, b=btn: b.configure(bg="#313244"))

        # ── Sezione SHORTCUT collassabile ──────────────────────────────
        self._shortcut_aperto = False

        lbl_shortcut = f"▶  {self._t('label_shortcut')}"
        self._btn_shortcut_toggle = tk.Button(
            self.frame_pannello,
            text=lbl_shortcut,
            bg="#181825", fg="#cba6f7",
            font=("Segoe UI", 8, "bold"),
            relief=tk.FLAT, cursor="hand2", anchor="w",
            command=self._toggle_shortcut
        )
        self._btn_shortcut_toggle.pack(fill=tk.X, padx=8, pady=(10, 2), ipady=2)
        self._btn_shortcut_toggle.bind(
            "<Enter>", lambda e: self._btn_shortcut_toggle.configure(fg="#f5c2e7"))
        self._btn_shortcut_toggle.bind(
            "<Leave>", lambda e: self._btn_shortcut_toggle.configure(fg="#cba6f7"))

        self._frame_shortcut = tk.Frame(self.frame_pannello, bg="#181825")

        shortcuts = self.cfg.get("shortcut", [])
        if shortcuts:
            for sc in shortcuts:
                etichetta = sc.get("etichetta", "")
                comando   = sc.get("comando", "")
                if not etichetta or not comando:
                    continue
                btn = tk.Button(
                    self._frame_shortcut, text=etichetta,
                    bg="#2a273f", fg="#cba6f7",
                    font=("Segoe UI", 9),
                    relief=tk.FLAT, cursor="hand2", anchor="w",
                    command=lambda c=comando: self._inserisci_comando(c)
                )
                btn.pack(fill=tk.X, padx=8, pady=2, ipady=3)
                btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#45475a"))
                btn.bind("<Leave>", lambda e, b=btn: b.configure(bg="#2a273f"))
        else:
            tk.Label(
                self._frame_shortcut,
                text=self._t("shortcut_nessuno"),
                bg="#181825", fg="#6c7086",
                font=("Segoe UI", 7),
                justify="left"
            ).pack(padx=12, pady=4, anchor="w")

        # ── Sezione LINGUA ─────────────────────────────────────────────
        tk.Label(self.frame_pannello, text=self._t("label_lingua"),
                 bg="#181825", fg="#94e2d5",
                 font=("Segoe UI", 8, "bold")).pack(
                     fill=tk.X, padx=8, pady=(12, 2), anchor="w")

        lingue = self._lingue_disponibili()
        if lingue:
            lingua_attiva = self.cfg.get("lingua", "it")
            for codice, etichetta in lingue:
                attiva   = (codice == lingua_attiva)
                bg_color = "#1a3a2a" if attiva else "#181825"
                fg_color = "#94e2d5" if attiva else "#6c7086"
                prefisso = "● " if attiva else "○ "
                btn = tk.Button(
                    self.frame_pannello,
                    text=f"{prefisso}{etichetta}",
                    bg=bg_color, fg=fg_color,
                    font=("Segoe UI", 9),
                    relief=tk.FLAT, cursor="hand2", anchor="w",
                    command=lambda c=codice: self._cambia_lingua_ui(c)
                )
                btn.pack(fill=tk.X, padx=8, pady=1, ipady=3)
                btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#45475a"))
                btn.bind("<Leave>",
                         lambda e, b=btn, a=attiva, bg=bg_color:
                             b.configure(bg=bg))
        else:
            tk.Label(self.frame_pannello,
                     text=self._t("lingua_nessuna"),
                     bg="#181825", fg="#6c7086",
                     font=("Segoe UI", 7),
                     justify="left").pack(padx=12, pady=4, anchor="w")

    def _lingue_disponibili(self) -> list:
        """Scansiona _dati/ e la cartella base alla ricerca di file lang_XX.json."""
        NOMI_LINGUA = {
            "it": "Italiano 🇮🇹",
            "en": "English 🇬🇧",
            "fr": "Français 🇫🇷",
            "de": "Deutsch 🇩🇪",
            "es": "Español 🇪🇸",
            "pt": "Português 🇵🇹",
        }
        trovati = {}
        for cartella in [INTERNAL_DIR, BASE_DIR]:
            for f in sorted(cartella.glob("lang_*.json")):
                codice = f.stem[5:]
                if codice not in trovati:
                    nome = NOMI_LINGUA.get(codice, codice.upper())
                    trovati[codice] = nome
        return sorted(trovati.items())

    def _cambia_lingua_ui(self, codice: str):
        """Chiamato dai pulsanti lingua nel pannello — esegue il cambio."""
        parsed = {"comando": "lingua", "nome": codice, "alias": None,
                  "soggetto": "", "dati_inline": None,
                  "confidenza": 1, "testo_originale": f"lingua {codice}"}
        self._cmd_lingua(parsed)

    def _toggle_shortcut(self):
        lbl = self._t("label_shortcut")
        if self._shortcut_aperto:
            self._frame_shortcut.pack_forget()
            self._btn_shortcut_toggle.configure(text=f"▶  {lbl}")
        else:
            self._frame_shortcut.pack(fill=tk.X, after=self._btn_shortcut_toggle)
            self._btn_shortcut_toggle.configure(text=f"▼  {lbl}")
        self._shortcut_aperto = not self._shortcut_aperto

    def _inserisci_comando(self, testo: str):
        self.input_var.set(testo)
        self.entry.focus_set()
        self.entry.icursor(tk.END)
        if not testo.endswith(" "):
            self.root.after(50, self._on_invia)

    def _toggle_pannello(self):
        if self._pannello_aperto:
            self.frame_pannello.pack_forget()
            self.btn_toggle.configure(text="◀")
        else:
            self.frame_pannello.pack(side=tk.RIGHT, fill=tk.Y)
            self.btn_toggle.configure(text="▶")
        self._pannello_aperto = not self._pannello_aperto

    # ------------------------------------------------------------------
    # AVATAR (invariato)
    # ------------------------------------------------------------------
    def _mostra_avatar(self, nome: str):
        if not nome:
            return
        if self._video_after_id:
            self.root.after_cancel(self._video_after_id)
            self._video_after_id = None

        for ext in [".jpg", ".jpeg", ".png", ".gif"]:
            path = ASSET_DIR / (nome + ext)
            if path.exists():
                self._mostra_immagine(path)
                return

        stem = nome if nome.endswith(".mp4") else nome + ".mp4"
        path_mp4 = ASSET_DIR / stem
        if path_mp4.exists():
            self._riproduci_video(path_mp4)
            return

        self._placeholder_avatar(nome)

    def _reset_avatar_label(self):
        """
        Riporta avatar_label a uno stato pulito e neutro prima di ogni cambio.
        Il bug: tkinter usa unita diverse per width/height a seconda che il Label
        contenga un image (pixel) o solo testo (caratteri). Mischiare le due
        modalita senza reset causa immagini schiacciate o invisibili.
        La soluzione e azzerare sempre image, text e dimensioni prima di ogni
        cambio di contenuto, cosi tkinter riparte da zero.
        """
        # Azzera tutto: image=empty string, dimensioni minime
        self.avatar_label.configure(
            image="", text="",
            bg="#1e1e2e",
            width=0, height=0,
            font=("Segoe UI", 1),
        )
        self.avatar_label.image = None
        self.root.update_idletasks()   # forza ricalcolo layout

    def _mostra_immagine(self, path: Path):
        try:
            from PIL import Image, ImageTk
            img   = Image.open(path).resize((300, 300), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self._reset_avatar_label()   # reset PRIMA di impostare image
            self.avatar_label.configure(image=photo, text="", bg="#1e1e2e",
                                        width=0, height=0)
            self.avatar_label.image = photo  # mantieni riferimento (anti GC)
        except Exception as e:
            print(f"[AVATAR] Errore immagine {path}: {e}")
            self._placeholder_avatar(path.stem)

    def _placeholder_avatar(self, nome: str):
        colori = {"benvenuto": "#89b4fa", "sorridente": "#a6e3a1",
                  "soddisfatto": "#fab387", "triste": "#f38ba8",
                  "magazziniere": "#cba6f7", "ciao": "#94e2d5"}
        col = colori.get(nome.lower().replace(".mp4", ""), "#6c7086")
        testo = nome.upper().replace(".MP4", "")
        self._reset_avatar_label()   # reset PRIMA di impostare testo
        # In modalita testo, width/height sono in caratteri: usiamo valori
        # ragionevoli (non 300 che causerebbe un blocco enorme).
        self.avatar_label.configure(
            image="", text=testo,
            bg=col, fg="#1e1e2e",
            font=("Segoe UI", 16, "bold"),
            width=18, height=6,
            wraplength=260,
            justify="center"
        )
        self.avatar_label.image = None

    def _riproduci_video(self, path: Path, callback=None):
        try:
            import cv2
            from PIL import Image, ImageTk

            cap = cv2.VideoCapture(str(path))
            if not cap.isOpened():
                raise ValueError(f"cv2 non riesce ad aprire: {path}")
            fps = cap.get(cv2.CAP_PROP_FPS) or 25
            delay = int(1000 / fps)

            frames = []
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb).resize((300, 300), Image.LANCZOS)
                frames.append(ImageTk.PhotoImage(img))
            cap.release()

            if not frames:
                raise ValueError("Nessun frame letto dal video")

            self._video_frames = frames

            self._reset_avatar_label()   # reset prima del primo frame video

            def _play(idx=0):
                if not self._video_frames:
                    return
                if idx < len(self._video_frames):
                    self.avatar_label.configure(image=self._video_frames[idx], text="",
                                                width=0, height=0)
                    self.avatar_label.image = self._video_frames[idx]
                    self._video_after_id = self.root.after(delay, _play, idx + 1)
                else:
                    self._video_after_id = None
                    self._video_frames   = []
                    if callback:
                        callback()
                    else:
                        self._mostra_avatar(self.cfg.get("avatar_iniziale", "benvenuto"))
            _play()
        except Exception as e:
            print(f"[VIDEO ERROR] {path.name}: {e}")
            self._placeholder_avatar(path.stem)
            if callback:
                self.root.after(500, callback)

    # ------------------------------------------------------------------
    # OUTPUT
    # ------------------------------------------------------------------
    def _scrivi_risposta(self, testo: str):
        self.output.configure(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M")
        self.output.insert(tk.END, f"\n[{timestamp}] {self.cfg['nome_avatar']}:> {testo}\n")
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)
        self._parla(testo)

    def _scrivi_utente(self, testo: str):
        self.output.configure(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M")
        self.output.insert(tk.END, f"\n[{timestamp}] {self.cfg['nome_utente']}:> {testo}\n")
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)

    # ------------------------------------------------------------------
    # TTS (pyttsx3)
    # ------------------------------------------------------------------
    def _parla(self, testo: str):
        """Esegue la sintesi vocale in modo asincrono."""
        if not self._tts_attivo or not self._tts_engine or not testo:
            return
        
        # Esegui in thread separato per non bloccare l'UI
        threading.Thread(target=self._parla_thread, args=(testo,), daemon=True).start()

    def _parla_thread(self, testo: str):
        """Thread per la sintesi vocale."""
        try:
            self._tts_engine.say(testo)
            self._tts_engine.runAndWait()
        except Exception as e:
            print(f"[TTS] Errore: {e}")

    def _toggle_tts(self):
        self._tts_attivo = not self._tts_attivo
        if self._tts_attivo:
            self._btn_tts.configure(text="🔊", fg="#cdd6f4")
        else:
            self._btn_tts.configure(text="🔇", fg="#6c7086")
            # Ferma qualsiasi sintesi in corso
            if self._tts_engine:
                try:
                    self._tts_engine.stop()
                except:
                    pass

    # ------------------------------------------------------------------
    # STT (aggiornato con configurazione)
    # ------------------------------------------------------------------
    def _toggle_ascolto(self):
        if self._stt_ascolto:
            return
        self._stt_ascolto = True
        self._btn_mic.configure(bg="#f38ba8", fg="#1e1e2e")
        self.entry.configure(state=tk.DISABLED)
        threading.Thread(target=self._ascolta_thread, daemon=True).start()

    def _ascolta_thread(self):
        """Registra con sounddevice fino al silenzio, poi invia a Google STT."""
        testo  = None
        errore = None
        try:
            blocco      = int(self._STT_SAMPLERATE * 0.1)
            max_blocchi = int(self._STT_MAX_SECONDI / 0.1)
            sil_blocchi = int(self._STT_SILENZIO_S  / 0.1)

            buffer          = []
            blocchi_silenzio = 0
            parlato_iniziato = False

            with sd.InputStream(samplerate=self._STT_SAMPLERATE,
                                 channels=1, dtype="int16") as stream:
                for _ in range(max_blocchi):
                    chunk, _ = stream.read(blocco)
                    ampiezza = int(np.abs(chunk.astype(np.float32)).mean())
                    buffer.append(chunk.copy())

                    if ampiezza > self._STT_SOGLIA:
                        parlato_iniziato = True
                        blocchi_silenzio = 0
                    elif parlato_iniziato:
                        blocchi_silenzio += 1
                        if blocchi_silenzio >= sil_blocchi:
                            break

            if not parlato_iniziato:
                errore = self._t("stt_nessun_audio")
            else:
                campioni  = np.concatenate(buffer, axis=0)
                raw_bytes = campioni.tobytes()
                audio     = sr.AudioData(raw_bytes, self._STT_SAMPLERATE, 2)
                
                # Usa lingua STT dal config
                lingua_stt = self.cfg.get("stt_config", {}).get("lingua", "it-IT")
                testo = self._stt_recognizer.recognize_google(audio, language=lingua_stt)

        except sr.UnknownValueError:
            errore = self._t("stt_non_capito")
        except sr.RequestError as e:
            errore = self._t("stt_errore", err=e)
        except Exception as e:
            errore = self._t("stt_mic_errore", err=e)
        self.root.after(0, self._dopo_ascolto, testo, errore)

    def _dopo_ascolto(self, testo, errore):
        self._stt_ascolto = False
        self._btn_mic.configure(bg="#313244", fg="#cdd6f4")
        self.entry.configure(state=tk.NORMAL)
        self.entry.focus_set()
        if testo:
            self.input_var.set(testo)
            self.entry.icursor(tk.END)
            self._on_invia()
        elif errore:
            self._scrivi_risposta(errore)

    # ------------------------------------------------------------------
    # CRONOLOGIA
    # ------------------------------------------------------------------
    def _history_su(self):
        if not self._history:
            return
        if self._history_idx == -1:
            self._history_idx = len(self._history) - 1
        elif self._history_idx > 0:
            self._history_idx -= 1
        self.input_var.set(self._history[self._history_idx])
        self.entry.icursor(tk.END)

    def _history_giu(self):
        if self._history_idx == -1:
            return
        if self._history_idx < len(self._history) - 1:
            self._history_idx += 1
            self.input_var.set(self._history[self._history_idx])
        else:
            self._history_idx = -1
            self.input_var.set("")
        self.entry.icursor(tk.END)

    # ------------------------------------------------------------------
    # INPUT (con integrazione AI)
    # ------------------------------------------------------------------
    def _on_invia(self):
        testo = self.input_var.get().strip()
        if not testo:
            return
        if not self._history or self._history[-1] != testo:
            self._history.append(testo)
        self._history_idx = -1
        self._scrivi_utente(testo)
        self.input_var.set("")
        self._gestisci_input(testo)

    def _gestisci_input(self, testo: str):
        # Parola chiave per interrompere la sintesi vocale
        if testo.strip().lower() in ("ok", "stop", "basta", "silenzio",
                                     "quiet", "enough") and self._tts_engine:
            try:
                self._tts_engine.stop()
            except:
                pass
            return

        # Stati di dialogo esistenti
        if self.stato != "idle":
            self._gestisci_stati_dialogo(testo)
            return

        # ── Risposte fisse configurabili ────────────────────────────────
        risposte_fisse = self.cfg.get("risposte_fisse", {})
        testo_lower = testo.strip().lower()
        for trigger, risposta in risposte_fisse.items():
            if testo_lower == trigger.lower():
                testo_risposta = self._espandi_segnaposto(risposta)
                self._scrivi_risposta(testo_risposta)
                self._mostra_avatar(avatar_random(self.cfg))
                return

        # Unisce alias dal config con alias dal file lingua attivo
        alias_merged = {}
        for fonte in [self.cfg.get("alias_comandi", {}),
                      self.L.get("alias_comandi", {})]:
            for cmd, lista in fonte.items():
                alias_merged.setdefault(cmd, [])
                for a in lista:
                    if a not in alias_merged[cmd]:
                        alias_merged[cmd].append(a)

        # Ottieni articoli/stop-words dalla lingua attuale
        articoli = self.L.get("articoli", [])

        parsed = parse_comando(testo, self.cfg["nome_utente"], alias_merged, articoli)
        cmd    = parsed.get("comando")

        dispatch = {
            "ricorda":  self._cmd_ricorda,
            "apri":     self._cmd_apri,
            "dammi":    self._cmd_dammi,
            "cerca":    self._cmd_cerca,
            "elimina":  self._cmd_elimina,
            "modifica": self._cmd_modifica,
            "elenca":   self._cmd_elenca,
            "aiuto":    self._cmd_aiuto,
            "copia":    self._cmd_copia,
            "impara":   self._cmd_impara,
            "esci":     self._cmd_esci,
            "lingua":   self._cmd_lingua,
            "configura": self._cmd_configura,
        }

        if cmd in dispatch:
            dispatch[cmd](parsed)
        else:
            # Se il comando non è riconosciuto, prova con l'AI (se abilitata)
            ai_cfg = self.cfg.get("ai_config", {})
            if ai_cfg.get("enabled", False) and ai_cfg.get("fallback_to_ai", True) and self._ai_client:
                self._chiedi_ai(testo)
            else:
                self._non_capito()

    def _gestisci_stati_dialogo(self, testo: str):
        """Gestisce i vari stati di dialogo (ricorda, impara, elimina, modifica, configura)."""
        if self.stato == "attesa_nome_ricorda":
            self._ricorda_step_nome(testo); return
        if self.stato == "attesa_dati_ricorda":
            self._ricorda_step2_dati(testo); return
        if self.stato == "attesa_nome_img":
            self._img_step2_nome(testo); return
        if self.stato == "attesa_tag_img":
            self._img_step3_tag(testo); return
        if self.stato == "attesa_elimina_conferma":
            self._elimina_conferma(testo); return
        if self.stato == "attesa_modifica_campo":
            self._modifica_campo(testo); return
        if self.stato == "attesa_modifica_valore":
            self._modifica_valore(testo); return
        if self.stato == "impara_nome":
            self._impara_campo("nome", testo); return
        if self.stato == "impara_alias":
            self._impara_campo("alias", testo); return
        if self.stato == "impara_soggetto":
            self._impara_campo("soggetto", testo); return
        if self.stato == "impara_dati":
            self._impara_campo("dati", testo); return
        if self.stato == "impara_tag":
            self._impara_campo("tag", testo); return
        if self.stato == "impara_avatar":
            self._impara_campo("avatar", testo); return
        if self.stato == "impara_altro":
            self._impara_altro(testo); return
        if self.stato.startswith("configura_"):
            self._configura_step(testo); return

    # ------------------------------------------------------------------
    # INTEGRAZIONE AI
    # ------------------------------------------------------------------
    def _chiedi_ai(self, domanda: str):
        """Invia una domanda all'IA e mostra la risposta."""
        self._scrivi_risposta(self._t("ai_pensando"))
        
        # Esegui in thread separato
        threading.Thread(target=self._chiedi_ai_thread, args=(domanda,), daemon=True).start()

    def _chiedi_ai_thread(self, domanda: str):
        """Thread per la chiamata API all'IA."""
        try:
            ai_cfg = self.cfg.get("ai_config", {})
            provider = ai_cfg.get("provider", "openai")
            risposta = ""
            
            if provider == "openai" and self._ai_client:
                import openai
                response = openai.ChatCompletion.create(
                    model=ai_cfg.get("model", "gpt-3.5-turbo"),
                    messages=[
                        {"role": "system", "content": f"Sei {self.cfg['nome_avatar']}, un assistente personale. Rispondi in modo conciso e utile."},
                        {"role": "user", "content": domanda}
                    ],
                    temperature=ai_cfg.get("temperature", 0.7),
                    max_tokens=ai_cfg.get("max_tokens", 500)
                )
                risposta = response.choices[0].message.content
                
            elif provider == "gemini" and self._ai_client:
                response = self._ai_client.generate_content(
                    domanda,
                    generation_config={
                        "temperature": ai_cfg.get("temperature", 0.7),
                        "max_output_tokens": ai_cfg.get("max_tokens", 500),
                    }
                )
                risposta = response.text
            
            if risposta:
                self.root.after(0, self._scrivi_risposta, risposta)
            else:
                self.root.after(0, self._non_capito)
                
        except Exception as e:
            self.root.after(0, self._scrivi_risposta, 
                           self._t("ai_errore", errore=str(e)))

    # ------------------------------------------------------------------
    # COMANDO CONFIGURA (nuovo)
    # ------------------------------------------------------------------
    def _cmd_configura(self, parsed: dict):
        """Gestisce il comando configura in tutte le sue forme."""
        parametro = parsed.get("nome", "").strip().lower()
        
        # Se non c'è parametro, avvia la configurazione guidata
        if not parametro:
            self._configura_wizard_inizio()
            return
        
        # Comando "configura lista"
        if parametro == "lista":
            self._configura_lista()
            return
        
        # Configura un parametro specifico
        self._configura_parametro(parametro)

    def _configura_wizard_inizio(self):
        """Avvia la configurazione guidata completa."""
        self.stato = "configura_wizard"
        self.dati_temp = {"parametri_configurati": []}
        
        # Lista dei parametri principali da configurare
        self._configura_queue = [
            ("nome_avatar", self._t("configura_nome_avatar")),
            ("nome_utente", self._t("configura_nome_utente")),
            ("lingua", self._t("configura_lingua")),
            ("tts_config.rate", self._t("configura_tts_rate")),
            ("tts_config.volume", self._t("configura_tts_volume")),
        ]
        
        self._configura_prossimo()

    def _configura_prossimo(self):
        """Passa al prossimo parametro nella coda di configurazione."""
        if not self._configura_queue:
            self._configura_fine()
            return
        
        param_key, param_label = self._configura_queue[0]
        
        # Ottieni il valore attuale
        valore_attuale = self._get_nested_config(param_key)
        
        self.stato = f"configura_{param_key}"
        self.dati_temp["param_key"] = param_key
        self.dati_temp["param_label"] = param_label
        
        self._scrivi_risposta(
            f"{param_label} attuale = '{valore_attuale}'\n" +
            self._t("configura_chiedi_valore", param=param_label)
        )

    def _get_nested_config(self, key: str):
        """Ottiene un valore annidato dal config (es. 'tts_config.rate')."""
        parts = key.split('.')
        value = self.cfg
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part, "")
            else:
                return ""
        return value

    def _set_nested_config(self, key: str, value):
        """Imposta un valore annidato nel config."""
        parts = key.split('.')
        target = self.cfg
        for part in parts[:-1]:
            if part not in target:
                target[part] = {}
            target = target[part]
        target[parts[-1]] = value

    def _configura_step(self, testo: str):
        """Gestisce i passi della configurazione guidata."""
        if not self.stato.startswith("configura_"):
            return
        
        if testo.lower() in ["stop", "annulla", "fine"]:
            self.stato = "idle"
            self._configura_queue = []
            self._scrivi_risposta(self._t("configura_annullato"))
            return
        
        if self.stato == "configura_wizard":
            # Gestione risposta sì/no per proseguire
            if testo.lower() in self._t("impara_si"):
                self._configura_prossimo()
            else:
                self._configura_fine()
            return
        
        # Estrai il parametro corrente dallo stato
        param_key = self.stato.replace("configura_", "")
        param_label = self.dati_temp.get("param_label", param_key)
        
        # Converti il valore se necessario
        valore = testo.strip()
        
        # Conversione per tipi numerici
        if param_key == "tts_config.rate":
            try:
                valore = int(valore)
            except ValueError:
                self._scrivi_risposta("Inserisci un numero valido (es. 150)")
                return
        elif param_key == "tts_config.volume":
            try:
                valore = float(valore)
                if valore < 0 or valore > 1:
                    self._scrivi_risposta("Il volume deve essere tra 0 e 1")
                    return
            except ValueError:
                self._scrivi_risposta("Inserisci un numero valido (es. 0.9)")
                return
        
        # Salva il valore
        self._set_nested_config(param_key, valore)
        salva_config = self.cfg
        with open(CFG_FILE, "w", encoding="utf-8") as f:
            json.dump(salva_config, f, indent=2, ensure_ascii=False)
        
        self._scrivi_risposta(
            self._t("configura_aggiornato", param=param_label, valore=valore)
        )
        
        # Rimuovi dalla coda e passa al prossimo
        if hasattr(self, "_configura_queue") and self._configura_queue:
            self._configura_queue.pop(0)
            
            if self._configura_queue:
                self._scrivi_risposta(self._t("configura_proseguire"))
                self.stato = "configura_wizard"
            else:
                self._configura_fine()

    def _configura_lista(self):
        """Mostra la lista dei parametri configurabili."""
        msg = self._t("configura_lista") + "\n"
        
        # Parametri principali
        msg += "\n• nome_avatar"
        msg += "\n• nome_utente"
        msg += "\n• lingua"
        msg += "\n• tts_config.rate (velocità voce)"
        msg += "\n• tts_config.volume (volume)"
        msg += "\n• tts_config.pitch (tono)"
        msg += "\n• stt_config.soglia_rumore (sensibilità microfono)"
        msg += "\n• stt_config.lingua (lingua riconoscimento)"
        msg += "\n• ai_config.enabled (abilita IA)"
        
        self._scrivi_risposta(msg)

    def _configura_parametro(self, parametro: str):
        """Configura un singolo parametro specificato."""
        # Mappa nomi comuni a chiavi di configurazione
        mappa_parametri = {
            "nome assistente": "nome_avatar",
            "nome utente": "nome_utente",
            "lingua": "lingua",
            "velocita voce": "tts_config.rate",
            "volume": "tts_config.volume",
            "tono": "tts_config.pitch",
            "soglia rumore": "stt_config.soglia_rumore",
            "lingua stt": "stt_config.lingua",
            "abilita ia": "ai_config.enabled",
        }
        
        param_key = mappa_parametri.get(parametro, parametro)
        
        # Verifica se il parametro esiste
        try:
            valore_attuale = self._get_nested_config(param_key)
        except:
            self._scrivi_risposta(
                self._t("configura_parametro_non_trovato", param=parametro)
            )
            return
        
        self.stato = f"configura_{param_key}"
        self.dati_temp["param_key"] = param_key
        self.dati_temp["param_label"] = parametro
        
        self._scrivi_risposta(
            self._t("configura_mostra_valore", param=parametro, valore=valore_attuale) + "\n" +
            self._t("configura_chiedi_valore", param=parametro)
        )

    def _configura_fine(self):
        """Termina la configurazione."""
        self.stato = "idle"
        self._configura_queue = []
        self._scrivi_risposta(self._t("configura_fine"))
        
        # Riavvia TTS con nuove impostazioni se necessario
        if self._tts_engine:
            try:
                self._tts_engine.stop()
            except:
                pass
        self._inizializza_tts()

    # ------------------------------------------------------------------
    # COMANDI ESISTENTI (invariati)
    # ------------------------------------------------------------------
    def on_close(self):
        self._cmd_esci()

    def _cmd_esci(self, parsed=None):
        if getattr(self, "_esci_in_corso", False):
            return
        self._esci_in_corso = True

        frase      = self.cfg.get("frase_finale", "Ci vediamo presto!")
        avatar_fin = self.cfg.get("avatar_finale", "ciao.mp4")
        path_video = ASSET_DIR / avatar_fin

        self.entry.configure(state=tk.DISABLED)
        self._scrivi_risposta(frase)

        if not hasattr(self, "_lbl_frase_finale"):
            self._lbl_frase_finale = tk.Label(
                self.frame_chat,
                text="", bg="#1e1e2e", fg="#cdd6f4",
                font=("Segoe UI", 13, "italic"),
                wraplength=320
            )
            self._lbl_frase_finale.pack(after=self.avatar_label, pady=(4, 0))
        self._lbl_frase_finale.configure(text=frase)

        def _chiudi():
            if self._video_after_id:
                try:
                    self.root.after_cancel(self._video_after_id)
                except Exception:
                    pass
            self._video_frames = []
            try:
                self.root.destroy()
            except Exception:
                pass

        if path_video.exists():
            self._riproduci_video(path_video, callback=_chiudi)
        else:
            self._placeholder_avatar(avatar_fin.replace(".mp4", ""))
            self.root.after(2000, _chiudi)

    def _cmd_ricorda(self, parsed: dict):
        nome = parsed.get("nome", "").strip()

        if "immagine" in parsed["testo_originale"].lower():
            self._ricorda_immagine()
            return

        dati_inline = parsed.get("dati_inline")

        if nome and dati_inline:
            av    = avatar_random(self.cfg)
            entry = {k: v for k, v in {
                "nome":     nome,
                "alias":    parsed.get("alias"),
                "soggetto": parsed.get("soggetto", self.cfg["nome_utente"]),
                "dati":     dati_inline,
                "avatar":   av
            }.items() if v is not None}
            self.mem.append(entry)
            salva_memoria(self.mem)
            self._mostra_avatar(av)
            self._scrivi_risposta(self._t("ricorda_ok", nome=nome))
            return

        if nome:
            self.stato = "attesa_dati_ricorda"
            self.dati_temp = {
                "nome":     nome,
                "alias":    parsed.get("alias"),
                "soggetto": parsed.get("soggetto", self.cfg["nome_utente"])
            }
            self._scrivi_risposta(self._t("ricorda_chiedi_dati", nome=nome))
            return

        self.stato = "attesa_nome_ricorda"
        self.dati_temp = {
            "soggetto": parsed.get("soggetto", self.cfg["nome_utente"]),
            "alias":    parsed.get("alias")
        }
        self._scrivi_risposta(self._t("ricorda_chiedi_nome"))

    def _ricorda_step_nome(self, testo: str):
        self.dati_temp["nome"] = testo
        self.stato = "attesa_dati_ricorda"
        self._scrivi_risposta(self._t("ricorda_chiedi_dati", nome=testo))

    def _ricorda_step2_dati(self, testo: str):
        self.stato = "idle"
        self.dati_temp["dati"]   = testo
        self.dati_temp["avatar"] = avatar_random(self.cfg)
        entry = {k: v for k, v in self.dati_temp.items() if v is not None}
        self.mem.append(entry)
        salva_memoria(self.mem)
        self._mostra_avatar(entry["avatar"])
        self._scrivi_risposta(self._t("ricorda_ok", nome=entry.get("nome", "")))
        self.dati_temp = {}

    def _ricorda_immagine(self):
        path = filedialog.askopenfilename(
            title=self._t("ricorda_img_titolo"),
            filetypes=[("Immagini", "*.jpg *.jpeg *.png *.gif *.bmp *.webp")]
        )
        if not path:
            self._scrivi_risposta(self._t("ricorda_img_nessuna"))
            return
        self.dati_temp = {"_img_src": path}
        self.stato = "attesa_nome_img"
        self._scrivi_risposta(self._t("ricorda_img_nome"))

    def _img_step2_nome(self, nome: str):
        self.dati_temp["nome"] = nome
        self.stato = "attesa_tag_img"
        self._scrivi_risposta(self._t("ricorda_img_tag"))

    def _img_step3_tag(self, tag: str):
        self.stato = "idle"
        src  = Path(self.dati_temp["_img_src"])
        nome = self.dati_temp["nome"]
        dest = ASSET_DIR.parent / (nome.lower().replace(" ", "_") + src.suffix)
        shutil.copy2(src, dest)
        entry = {
            "nome":     nome,
            "dati":     str(dest),
            "tag":      tag,
            "soggetto": self.cfg["nome_utente"],
            "avatar":   "magazziniere"
        }
        self.mem.append(entry)
        salva_memoria(self.mem)
        self._mostra_avatar("magazziniere")
        self._scrivi_risposta(self._t("ricorda_img_ok", nome=nome))
        self.dati_temp = {}

    def _cmd_impara(self, parsed=None):
        self.dati_temp = {}
        self.stato = "impara_nome"
        self._scrivi_risposta(
            self._t("impara_intro") + "\n\n" + self._t("impara_prompt_nome")
        )

    _IMPARA_SEQUENZA  = ["nome", "alias", "soggetto", "dati", "tag", "avatar"]
    _IMPARA_OPZIONALI = {"alias", "soggetto", "tag", "avatar"}

    def _impara_prompt(self, campo: str) -> str:
        return self._t(f"impara_prompt_{campo}")

    def _impara_campo(self, campo: str, valore: str):
        t = valore.strip()
        if t.lower() == self._t("impara_fine"):
            self.stato = "idle"
            self.dati_temp = {}
            self._scrivi_risposta(self._t("impara_annullato"))
            return

        if t.lower() == self._t("impara_salta"):
            if campo not in self._IMPARA_OPZIONALI:
                self._scrivi_risposta(self._t("impara_obbligatorio", campo=campo))
                return
            if campo == "soggetto":
                self.dati_temp["soggetto"] = self.cfg["nome_utente"]
            elif campo == "avatar":
                self.dati_temp["avatar"] = "sorridente"
        else:
            if campo == "tag":
                self.dati_temp["tag"] = [x.strip() for x in t.split(",") if x.strip()]
            else:
                self.dati_temp[campo] = t

        idx = self._IMPARA_SEQUENZA.index(campo)
        if idx + 1 < len(self._IMPARA_SEQUENZA):
            prossimo = self._IMPARA_SEQUENZA[idx + 1]
            self.stato = f"impara_{prossimo}"
            self._scrivi_risposta(self._impara_prompt(prossimo))
        else:
            self._impara_salva()

    def _impara_salva(self):
        self.stato = "impara_altro"
        entry = {k: v for k, v in self.dati_temp.items() if v is not None}
        entry.setdefault("soggetto", self.cfg["nome_utente"])
        entry.setdefault("avatar",   "sorridente")
        self.mem.append(entry)
        salva_memoria(self.mem)
        self._mostra_avatar(entry.get("avatar", "sorridente"))
        self._scrivi_risposta(self._t("impara_salvato", nome=entry.get("nome", "")))
        self.dati_temp = {}

    def _impara_altro(self, testo: str):
        if testo.lower().strip() in self._t("impara_si"):
            self._cmd_impara()
        else:
            self.stato = "idle"
            self._scrivi_risposta(self._t("impara_completato"))
            self._mostra_avatar(avatar_random(self.cfg))

    def _cmd_apri(self, parsed: dict):
        q = parsed.get("nome") or parsed.get("alias") or ""
        if not q:
            self._scrivi_risposta(self._t("apri_cosa"))
            self._mostra_avatar("dubbio")
            return
        risultati = cerca_in_memoria(self.mem, q)
        if not risultati:
            self._scrivi_risposta(self._t("apri_non_trovato", q=q))
            self._mostra_avatar("triste")
            return
        link      = risultati[0].get("dati", "").split("\n")[0].strip()
        nome_voce = risultati[0].get("nome", link)
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END,
            f"\n{self.cfg['nome_avatar']}:> {self._t('apri_subito')}: {link}\n")
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)
        self._parla(f"{self._t('apri_subito')}: {nome_voce}")
        try:
            if sys.platform == "win32":
                os.startfile(link)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", link])
            else:
                subprocess.Popen(["xdg-open", link])
        except Exception as e:
            self._scrivi_risposta(self._t("apri_errore", err=e))
        self._mostra_avatar(risultati[0].get("avatar") or avatar_random(self.cfg))

    def _cmd_dammi(self, parsed: dict):
        chiavi = [k for k in [parsed.get("nome"), parsed.get("alias")] if k]
        sogg   = parsed.get("soggetto", "")
        if not chiavi:
            self._scrivi_risposta(self._t("dammi_cosa"))
            return
        risultati = []
        for chiave in chiavi:
            for r in cerca_in_memoria(self.mem, chiave):
                if r not in risultati:
                    risultati.append(r)
        for chiave in chiavi:
            for r in cerca_per_tag(self.mem, chiave):
                if r not in risultati:
                    risultati.append(r)
        if sogg and sogg != self.cfg["nome_utente"]:
            filtrati = [r for r in risultati
                        if r.get("soggetto","").lower() == sogg.lower()]
            if filtrati:
                risultati = filtrati
        if not risultati:
            q = " ".join(chiavi + ([sogg] if sogg and sogg != self.cfg["nome_utente"] else []))
            self._scrivi_risposta(self._t("dammi_non_trovato", q=q))
            self._mostra_avatar("triste")
            return
        if len(risultati) == 1:
            entry = risultati[0]
            dati  = entry.get("dati", "")
            self._scrivi_risposta(
                self._t("dammi_risultato_1",
                        nome=entry.get("nome",""),
                        soggetto=entry.get("soggetto","")) +
                f"\n  {dati.replace(chr(10), chr(10)+'  ')}"
            )
            self._mostra_avatar(entry.get("avatar") or avatar_random(self.cfg))
        else:
            msg = self._t("dammi_risultati_n", n=len(risultati)) + "\n"
            for i, r in enumerate(risultati, 1):
                dati = r.get("dati","")
                msg += f"\n  {i}. {r.get('nome','')} ({r.get('soggetto','')}):\n"
                msg += f"     {dati.replace(chr(10), chr(10)+'     ')}\n"
            self._scrivi_risposta(msg)
            self._mostra_avatar(risultati[0].get("avatar") or avatar_random(self.cfg))

    def _cmd_cerca(self, parsed: dict):
        q = parsed.get("nome", "")
        if not q:
            self._scrivi_risposta(self._t("cerca_cosa"))
            return
        risultati = cerca_in_memoria(self.mem, q)
        if not risultati:
            self._scrivi_risposta(self._t("cerca_non_trovato", q=q))
            self._mostra_avatar("triste")
            return
        msg = self._t("cerca_trovato", n=len(risultati), q=q) + "\n"
        for i, r in enumerate(risultati, 1):
            msg += f"\n[{i}] {formatta_entry(r)}"
        self._scrivi_risposta(msg)
        self._mostra_avatar(risultati[0].get("avatar") or avatar_random(self.cfg))

    def _cmd_elimina(self, parsed: dict):
        q = parsed.get("nome", "")
        if not q:
            self._scrivi_risposta(self._t("elimina_cosa"))
            return
        risultati = cerca_in_memoria(self.mem, q)
        if not risultati:
            self._scrivi_risposta(self._t("elimina_non_trovato", q=q))
            self._mostra_avatar("triste")
            return
        entry = risultati[0]
        self.dati_temp = {"entry_da_eliminare": entry}
        self.stato = "attesa_elimina_conferma"
        self._scrivi_risposta(
            self._t("elimina_conferma", entry=formatta_entry(entry))
        )

    def _elimina_conferma(self, testo: str):
        self.stato = "idle"
        if testo.lower().strip() in self._t("elimina_si"):
            entry = self.dati_temp.get("entry_da_eliminare")
            self.mem = [m for m in self.mem if m != entry]
            salva_memoria(self.mem)
            self._scrivi_risposta(self._t("elimina_ok", nome=entry.get("nome","")))
            self._mostra_avatar(avatar_random(self.cfg))
        else:
            self._scrivi_risposta(self._t("elimina_annullato"))
        self.dati_temp = {}

    def _cmd_modifica(self, parsed: dict):
        q = parsed.get("nome", "")
        if not q:
            self._scrivi_risposta(self._t("modifica_cosa"))
            return
        risultati = cerca_in_memoria(self.mem, q)
        if not risultati:
            self._scrivi_risposta(self._t("modifica_non_trovato", q=q))
            self._mostra_avatar("triste")
            return
        entry = risultati[0]
        self.dati_temp = {"entry_originale": entry, "idx": self.mem.index(entry)}
        self.stato = "attesa_modifica_campo"
        self._scrivi_risposta(self._t("modifica_trovata", entry=formatta_entry(entry)))

    def _modifica_campo(self, testo: str):
        campi_validi = ["nome", "alias", "soggetto", "dati", "avatar"]
        parti = testo.strip().split(None, 1)
        campo = parti[0].lower() if parti else ""
        if campo not in campi_validi:
            self._scrivi_risposta(
                self._t("modifica_campo_no",
                        campo=campo, campi=", ".join(campi_validi)))
            return
        if len(parti) == 2:
            self._esegui_modifica(campo, parti[1].strip())
        else:
            self.dati_temp["campo"] = campo
            self.stato = "attesa_modifica_valore"
            self._scrivi_risposta(self._t("modifica_valore_chiedi", campo=campo))

    def _modifica_valore(self, testo: str):
        self._esegui_modifica(self.dati_temp.get("campo"), testo.strip())

    def _esegui_modifica(self, campo: str, valore: str):
        self.stato = "idle"
        idx = self.dati_temp.get("idx")
        if idx is None or idx >= len(self.mem):
            self._scrivi_risposta(self._t("modifica_errore"))
            self.dati_temp = {}
            return
        self.mem[idx][campo] = valore
        salva_memoria(self.mem)
        self._scrivi_risposta(self._t("modifica_ok", campo=campo, valore=valore))
        self._mostra_avatar(avatar_random(self.cfg))
        self.dati_temp = {}

    def _cmd_elenca(self, parsed=None):
        if not self.mem:
            self._scrivi_risposta(self._t("elenca_vuota"))
            self._mostra_avatar("triste")
            return
        msg = self._t("elenca_intestazione", n=len(self.mem)) + "\n"
        for i, entry in enumerate(self.mem, 1):
            alias = f" [{entry['alias']}]" if entry.get("alias") else ""
            msg += f"\n  {i}. {entry.get('nome','')}{alias} — {entry.get('soggetto','')}"
        self._scrivi_risposta(msg)
        self._mostra_avatar(avatar_random(self.cfg))

    def _cmd_copia(self, parsed: dict):
        q = parsed.get("nome") or parsed.get("alias") or ""
        if not q:
            self._scrivi_risposta(self._t("copia_cosa"))
            return
        risultati = cerca_in_memoria(self.mem, q)
        if not risultati:
            self._scrivi_risposta(self._t("copia_non_trovato", q=q))
            self._mostra_avatar("triste")
            return
        dati = str(risultati[0].get("dati", ""))
        self.root.clipboard_clear()
        self.root.clipboard_append(dati)
        self._scrivi_risposta(self._t("copia_ok", dati=dati))
        self._mostra_avatar(risultati[0].get("avatar") or avatar_random(self.cfg))

    def _cmd_aiuto(self, parsed=None):
        self._scrivi_risposta(self._t("aiuto_testo"))
        self._mostra_avatar(self.cfg.get("avatar_iniziale", "benvenuto"))

    def _cmd_lingua(self, parsed: dict):
        codice = parsed.get("nome", "").strip().lower()
        if not codice:
            self._scrivi_risposta(self._t("lingua_uso"))
            return
        file_lingua = INTERNAL_DIR / f"lang_{codice}.json"
        file_base   = BASE_DIR / f"lang_{codice}.json"
        if not file_lingua.exists() and not file_base.exists():
            self._scrivi_risposta(
                self._t("lingua_non_trovata",
                        file=f"lang_{codice}.json",
                        cartella=str(INTERNAL_DIR)))
            return
        self.L = carica_lingua(codice)
        self.cfg["lingua"] = codice
        with open(CFG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.cfg, f, indent=2, ensure_ascii=False)
        self.root.title(self._t("titolo_finestra", nome_avatar=self.cfg["nome_avatar"]))
        for widget in self.frame_pannello.winfo_children():
            widget.destroy()
        self._costruisci_pannello()
        self._scrivi_risposta(self._t("lingua_ok", lingua=codice.upper()))
        self._mostra_avatar(avatar_random(self.cfg))
        
        # Riavvio TTS con nuova lingua
        if self._tts_engine:
            try:
                self._tts_engine.stop()
            except:
                pass
        self._inizializza_tts()

    def _non_capito(self):
        self._mostra_avatar("triste")
        self._scrivi_risposta(self._t("non_capito"))

# ---------------------------------------------------------------------------
# AVVIO
# ---------------------------------------------------------------------------
def main():
    root = tk.Tk()
    root.geometry("560x700")
    root.minsize(420, 500)
    app = Assistente(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()

if __name__ == "__main__":
    main()