# 🤖 **myAssistente** Assistente personale desktop
[![Supporto via PayPal](https://img.shields.io/badge/Support-PayPal-00457C?logo=paypal&logoColor=white)](https://www.paypal.com/pool/9nyLoeBeq8?sr=wccr)

Un assistente desktop leggero e rispettoso della privacy, che vive
interamente sul tuo computer.
Nessun abbonamento cloud, nessun dato inviato altrove — ad eccezione del
riconoscimento vocale opzionale, che usa Google Speech API solo quando
premi il pulsante del microfono.

Scritto in Python con Tkinter, funziona su **Windows** (funzionalità
complete) e **Linux / macOS** (dalla release 3.x funzionalità complete).

## 📘 Documentazione
Documentazione release 2.x (ITA/ENG):  
**[Apri documentazione rel.2.2](https://www.steppa.net/cassani/articoli/assistente/docs/index.html)**
Documentazione completa (ITA/ENG):  
👉 **[Apri la cartella](https://gitlab.com/EmanueleCAS/assistente/-/tree/master/docs)**

---
## ✨ Funzionalità release  4.x

- Nuovo nome: **myAssistente** Assistente personale desktop
- **motore AIML** esterno (opzionale)
- nuova intestazione UI
- aggiornato comando **configura**
- nuovo comando **cerca media** (cerca music, video, picture inside -dati/asset/)
- maggiore flessibilità nella comprensione dei comandi
- Pacchetti distribuibili: Archivio ZIP pronto per 🪟 **Windows** (e presto per 🐧 Linux)
Tutte le funzionalità delle release precedenti

---

## ✨ Funzionalità release  3.x

- Voce Multi-piattaforma TTS (pyttsx3)
- Parametri **STT configurabili** dall'utente
- **Natural language parsing** con funzione **stop-words**
- Migliorie **internazionalizzazione** (config.json memory.json e file lang)
- Comando con **wizard interattivo** per configurare config.json
- **Integrazione con IA** opzionale
- Disponibile in **12 lingue** [Apri cartella localization](https://gitlab.com/EmanueleCAS/assistente/-/tree/master/localization-file)
- Pacchetti distribuibili: Archivio ZIP pronto per 🪟 **Windows**
Tutte le funzionalità delle release precedenti

---

## ✨ Funzionalità release 2.x

- **Input vocale (STT)** — dai comandi con la voce tramite microfono,
  con riconoscimento Google Speech
- **Output vocale (TTS)** — l'assistente legge le risposte ad alta voce
  *(solo Windows — SAPI)*
- **Memoria persistente** — salva, recupera, modifica ed elimina voci
  (contatti, codici, link, note, qualsiasi cosa)
- **Apri file e link** — avvia URL, file locali o applicazioni
  direttamente per nome
- **Interfaccia multilingua** — cambia lingua con un click, senza
  riavviare
- **Alias configurabili** — definisci i tuoi sinonimi per i comandi
  (es. `lancia` → `apri`, `dimmi` → `dammi`)
- **Risposte fisse** — configura risposte personalizzate per saluti e
  frasi ricorrenti
- **Pannello shortcut** — pulsanti a un click per i comandi più usati,
  completamente configurabili
- **Supporto avatar** — mostra immagini o animazioni MP4 come volto
  dell'assistente
- **Backup automatico** — il file memoria viene salvato prima di ogni
  modifica
- Pacchetti distribuibili: Archivi ZIP pronti per 🪟 **Windows** e 🐧 **Linux**

---

## 🖥️ Requisiti

### Installazione rapida per piattaforma

Windows (minima funzionante):
```bash
pip install pillow pyttsx3 pywin32
```

Windows (completa con STT e AI):
```bash
pip install pillow opencv-python pyttsx3 pywin32 SpeechRecognition sounddevice numpy openai
```

Linux:
```bash
sudo apt install espeak portaudio19-dev
pip install pillow pyttsx3 SpeechRecognition sounddevice numpy
```

macOS:
```bash
brew install portaudio
pip install pillow pyttsx3 SpeechRecognition sounddevice numpy
```

---

## 🚀 Avvio rapido

```bash
python assistente.py
```

Al primo avvio viene creata una cartella `_dati/` accanto allo script:

```
_dati/
  config.json   	← tutte le impostazioni
  memory.json		← i tuoi dati salvati
  lang_it.json          ← file lingua italiano
  lang_en.json          ← file lingua inglese
  asset/avatar/         ← inserisci qui le immagini/video avatar
```

---

## 🗣️ Comandi (nomi default)

| Comando | Descrizione |
|---------|-------------|
| `dammi <nome>` | Recupera un'informazione salvata |
| `apri <nome>` | Apre un link, file o applicazione salvata |
| `cerca <query>` | Cerca nella memoria |
| `elenca memoria` | Mostra tutte le voci salvate |
| `aiuto` | Mostra i comandi disponibili |
| `esci` | Chiude l'assistente |
| `impara` | Inserimento guidato campo per campo |
| `ricorda <nome> <dati>` | Salva un'informazione in memoria |
| `ricorda immagine <nome> <dati>` | Salva un'immagine in memoria |
| `modifica <nome>` | Modifica una voce salvata |
| `elimina <nome>` | Rimuove una voce dalla memoria |
| `copia <nome>` | Copia un dato negli appunti |
| `SHORTCUTS` | comandi personalizzati |
| `LINGUA <code>` | Cambia lingua (es `language_en`) |

> Tutti i comandi funzionano anche in italiano indipendentemente dalla
> lingua attiva.

---

## ⚙️ Configurazione

Modifica `_dati/config.json` per personalizzare l'assistente:

```json
{
  "nome_avatar":   "Alice",
  "nome_utente":   "Emanuele",
  "lingua":        "it",
  "frase_finale":  "Ci vediamo presto!",
  "alias_comandi": {
    "apri": ["lancia"],
    "esci": ["arrivederci", "chiudi"]
  },
  "risposte_fisse": {
    "grazie":    "Prego, {nome_utente}!",
    "ciao":      "Ciao, {nome_utente}!",
    "come stai": "Benissimo, grazie!"
  },
  "shortcut": [
    { "etichetta": "Estratto conto", "comando": "apri estratto" },
    { "etichetta": "Mail",           "comando": "apri posta" }
  ]
}
```

---

## 🌍 Aggiungere una nuova lingua

1. Copia `_dati/lang_it.json` in `_dati/lang_en.json`
   (o qualsiasi codice lingua)
2. Traduci tutti i valori — **non tradurre mai le chiavi**
3. Imposta `"lingua_stt"` con il codice Google Speech corretto
   (es. `"en-US"`)
4. Aggiungi gli alias dei comandi nella sezione `"alias_comandi"`
   per un input naturale nella nuova lingua
5. Riavvia l'assistente — la nuova lingua compare automaticamente
   nel selettore del pannello

Controllare se la vostra lingua è già presente nella cartella nel repository /localization-file.


---

### 🌍 Lingue disponibili

| ISO Code | Lingua (EN)              | nome file          | Nome orig.  | Flag |
|---------|---------------------------|--------------------|-------------|------|
| **AR**  | Arabic                    | lang_AR.json       | العربية            | 🇸🇦 |
| **DE**  | German                    | lang_DE.json       | Deutsch     | 🇩🇪 |
| **EN**  | English                   | lang_EN.json       | English     | 🇬🇧 |
| **ES**  | Spanish                   | lang_ES.json       | español     | 🇪🇸 |
| **FR**  | French                    | lang_FR.json       | français    | 🇫🇷 |
| **IT**  | Italian                   | lang_IT.json       | italiano    | 🇮🇹 |
| **JA**  | Japanese                  | lang_JA.json       | 日本語             | 🇯🇵 |
| **KO**  | Korean                    | lang_KO.json       | 한국어           | 🇰🇷 |
| **NL**  | Dutch                     | lang_NL.json       | Nederlands  | 🇳🇱 |
| **PL**  | Polish                    | lang_PL.json       | polski      | 🇵🇱 |
| **PT-BR** | Portuguese (Brazil)     | lang_PT-BR.json    | português (Brasil) | 🇧🇷 |
| **PT-PT** | Portuguese (Portugal)   | lang_PT-PT.json    | português (Portugal) | 🇵🇹 |
| **RU**  | Russian                   | lang_RU.json       | русский     | 🇷🇺 |
| **TR**  | Turkish                   | lang_TR.json       | Türkçe      | 🇹🇷 |
| **ZH-CN** | Chinese (Simplified)    | lang_ZH-CN.json    | 简体中文     | 🇨🇳 |

---

## 📦 Creare un pacchetto distribuibile

PyInstaller crea un **bundle** contenente l'interprete, 
tutte le dipendenze e lo script, in una cartella autonoma 
che funziona anche su macchine senza Python installato.

### Windows (modifica assistenteX.X.py col numero release)
```bash
pyinstaller --onedir --noconsole --clean ^
  --icon=assistente.ico ^
  --collect-all PIL ^
  --collect-all cv2 ^
  --name Assistente assistenteX.X.py
```

### Linux / macOS (modifica assistenteX.X.py col numero release)
```bash
pyinstaller --onedir --noconsole --clean \
  --icon=assistente.png \
  --collect-all PIL \
  --collect-all cv2 \
  --collect-all sounddevice \
  --collect-all speech_recognition \
  --hidden-import numpy \
  --name Assistente assistenteX.X.py
```

Dopo il bundle, copia `lang_it.json`, `lang_en.json` e la cartella
`_dati/` accanto all'eseguibile prima di avviarlo.


## 📋 Dipendenze release >3.0

| Libreria | Scopo | Richiesta | Note |
|---------|-------|-----------|------|
| `tkinter` | GUI | ✅ inclusa in Python | — |
| `json`, `os`, `re`, `shutil`, `subprocess`, `sys`, `random`, `threading`, `platform`, `pathlib`, `datetime` | Funzioni core | ✅ incluse in Python | — |
| `pillow` | Immagini avatar (jpg/png/gif) | ⚠️ raccomandata | Senza: solo placeholder colorato |
| `opencv-python` | Video avatar MP4 | ⚠️ opzionale | Richiede anche `pillow` |
| `pyttsx3` | Voce TTS multipiattaforma | ⚠️ raccomandata | Wrapper per i motori sotto |
| `pywin32` | Motore TTS SAPI5 | ⚠️ solo Windows | Usato da `pyttsx3` su Windows — spesso già presente |
| `espeak` / `espeak-ng` | Motore TTS | ⚠️ solo Linux | Pacchetto di sistema: `sudo apt install espeak` |
| — | Motore TTS NSSpeechSynthesizer | ✅ solo macOS | Nativo macOS, nessuna installazione |
| `SpeechRecognition` | Input voce STT | ⚠️ opzionale | Usa Google Speech API (online) |
| `sounddevice` | Acquisizione microfono | ⚠️ opzionale | Richiede PortAudio |
| `numpy` | Elaborazione audio STT | ⚠️ opzionale | Richiesto da `sounddevice` |
| `portaudio` | Driver audio per sounddevice | ⚠️ solo Linux/macOS | `sudo apt install portaudio19-dev` / `brew install portaudio` |
| `openai` | AI integration (ChatGPT) | ⚠️ opzionale | Solo se `ai_config.provider = "openai"` |
| `google-generativeai` | AI integration (Gemini) | ⚠️ opzionale | Solo se `ai_config.provider = "gemini"` |


---

## 📁 Struttura del progetto

```
assistenteX.X.py      	← script principale (release X.X)
assistente.ico          ← icona Windows
assistente.png          ← icona Linux
_dati/
  config.json
  memory.json
  memory.json.bak      ← backup automatico
  lang_it.json
  lang_en.json
  asset/
    avatar/             ← file avatar .jpg .png .gif .mp4
```

---

## 📜 Licenza

MIT

---

## 👤 Author

**[Emanuele Cassani](https://www.steppa.net/cassani/business_cardENG.htm)**  
Creatore e manutentore *Personal Desktop Assistant Toolkit*.

---