# 🤖 Assistente personale vocale desktop

Un assistente desktop leggero e rispettoso della privacy, che vive
interamente sul tuo computer.
Nessun abbonamento cloud, nessun dato inviato altrove — ad eccezione del
riconoscimento vocale opzionale, che usa Google Speech API solo quando
premi il pulsante del microfono.

Scritto in Python con Tkinter, funziona su **Windows** (funzionalità
complete) e **Linux / macOS** (senza sintesi vocale).

---

## ✨ Funzionalità

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

---

## 🖥️ Requisiti

### Windows
```
pip install pillow opencv-python SpeechRecognition sounddevice numpy pywin32
```

### Linux / macOS
```bash
# Dipendenza di sistema (solo Linux)
sudo apt install portaudio19-dev ffmpeg

# Pacchetti Python
pip install pillow opencv-python SpeechRecognition sounddevice numpy
```

> `pillow` e `opencv-python` sono opzionali ma consigliati.
> Senza di essi l'assistente mostra riquadri colorati al posto di
> immagini e video avatar, ma tutto il resto funziona normalmente.

---

## 🚀 Avvio rapido

```bash
python assistenteVOICE.py
```

Al primo avvio viene creata una cartella `_dati/` accanto allo script:

```
_dati/
  configurazione.json   ← tutte le impostazioni
  memoria.json          ← i tuoi dati salvati
  lang_it.json          ← file lingua italiano
  lang_en.json          ← file lingua inglese
  asset/avatar/         ← inserisci qui le immagini/video avatar
```

---

## 🗣️ Comandi

| Comando | Descrizione |
|---------|-------------|
| `ricorda <nome> <dati>` | Salva un'informazione in memoria |
| `impara` | Inserimento guidato campo per campo |
| `dammi <nome>` | Recupera un'informazione salvata |
| `apri <nome>` | Apre un link, file o applicazione salvata |
| `cerca <query>` | Cerca nella memoria |
| `elenca` | Mostra tutte le voci salvate |
| `modifica <nome>` | Modifica una voce salvata |
| `elimina <nome>` | Rimuove una voce dalla memoria |
| `copia <nome>` | Copia un dato negli appunti |
| `lingua <codice>` | Cambia lingua (es. `lingua en`) |
| `aiuto` | Mostra i comandi disponibili |
| `esci` | Chiude l'assistente |

> Tutti i comandi funzionano anche in italiano indipendentemente dalla
> lingua attiva.

---

## ⚙️ Configurazione

Modifica `_dati/configurazione.json` per personalizzare l'assistente:

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

1. Copia `_dati/lang_en.json` in `_dati/lang_fr.json`
   (o qualsiasi codice lingua)
2. Traduci tutti i valori — **non tradurre mai le chiavi**
3. Imposta `"lingua_stt"` con il codice Google Speech corretto
   (es. `"fr-FR"`)
4. Aggiungi gli alias dei comandi nella sezione `"alias_comandi"`
   per un input naturale nella nuova lingua
5. Riavvia l'assistente — la nuova lingua compare automaticamente
   nel selettore del pannello

---

## 📦 Creare un pacchetto distribuibile

PyInstaller non compila il codice Python in codice macchina — crea un
**bundle** contenente l'interprete, tutte le dipendenze e lo script,
in una cartella autonoma che funziona anche su macchine senza Python
installato.

### Windows
```bash
pyinstaller --onedir --noconsole --clean ^
  --icon=assistente.ico ^
  --collect-all PIL ^
  --collect-all cv2 ^
  --name AssistenteVOICE assistenteVOICE.py
```

### Linux / macOS
```bash
pyinstaller --onedir --noconsole --clean \
  --icon=assistente.png \
  --collect-all PIL \
  --collect-all cv2 \
  --collect-all sounddevice \
  --collect-all speech_recognition \
  --hidden-import numpy \
  --name AssistenteVOICE assistenteVOICE.py
```

Dopo il bundle, copia `lang_it.json`, `lang_en.json` e la cartella
`_dati/` accanto all'eseguibile prima di avviarlo.


## 📋 Dipendenze

| Libreria | Utilizzo | Obbligatoria |
|---------|---------|----------|
| `tkinter` | Interfaccia grafica | ✅ inclusa in Python |
| `pillow` | Immagini avatar | ❌ consigliata |
| `opencv-python` | Video MP4 avatar | ❌ consigliata |
| `SpeechRecognition` | Input vocale (STT) | ❌ consigliata |
| `sounddevice` | Acquisizione microfono | ❌ consigliata |
| `numpy` | Elaborazione audio | ❌ consigliata |
| `pywin32` | Sintesi vocale (TTS) | ❌ solo Windows |
| `portaudio` | Driver audio | ❌ pacchetto di sistema Linux |

---

## 📁 Struttura del progetto

```
assistenteVOICE.py      ← script principale
assistente.ico          ← icona Windows
assistente.png          ← icona Linux
_dati/
  configurazione.json
  memoria.json
  memoria.json.bak      ← backup automatico
  lang_it.json
  lang_en.json
  asset/
    avatar/             ← file avatar .jpg .png .gif .mp4
```

---

## 📜 Licenza

MIT
```