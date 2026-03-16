# 🤖 Personal Desktop Voice Assistant

A lightweight, privacy-first desktop assistant that lives on your machine.
No cloud subscriptions, no data sent anywhere — except for the optional
voice recognition, which uses Google Speech API only when you press the
microphone button.

Built with Python and Tkinter, it runs on **Windows** (full features) and
**Linux / macOS** (without text-to-speech).

## 📘 Documentation
Access the full documentation (ENG/ITA) here:  
👉 **[Open Documentation](https://www.steppa.net/cassani/articoli/assistente/docs/index.html)**

---

## ✨ Features

- **Voice input (STT)** — speak your commands via microphone, powered by
  Google Speech Recognition
- **Voice output (TTS)** — the assistant reads responses aloud
  *(Windows only — SAPI)*
- **Persistent memory** — save, retrieve, edit and delete named entries
  (contacts, codes, links, notes, anything)
- **Open files and links** — launch URLs, local files or applications
  directly by name
- **Multilanguage UI** — switch language at runtime with a single click,
  no restart needed
- **Configurable aliases** — define your own command synonyms
  (e.g. `launch` → `open`, `tell me` → `get`)
- **Fixed responses** — configure custom replies for greetings and
  small talk
- **Shortcut panel** — one-click buttons for your most used commands,
  fully configurable
- **Avatar support** — display images or MP4 animations as the
  assistant's face
- **Automatic backup** — memory file is backed up before every save

---

## 🖥️ Requirements

### Windows
```
pip install pillow opencv-python SpeechRecognition sounddevice numpy pywin32
```

### Linux / macOS
```bash
# System dependency (Linux only)
sudo apt install portaudio19-dev ffmpeg

# Python packages
pip install pillow opencv-python SpeechRecognition sounddevice numpy
```

> `pillow` and `opencv-python` are optional but recommended.
> Without them the assistant shows colored placeholders instead of
> avatar images and videos, and everything else works normally.

---

## 🚀 Quick start

```bash
python assistenteVOICE.py
```

On first run, a `_dati/` folder is created next to the script containing:

```
_dati/
  configurazione.json   ← all settings
  memoria.json          ← your saved data
  lang_it.json          ← Italian language file
  lang_en.json          ← English language file
  asset/avatar/         ← put your avatar images/videos here
```

---

## 🗣️ Commands (language_en)

| Command | Description |
|---------|-------------|
| `get <name>` | Retrieve saved information |
| `open <name>` | Open a saved link, file or application |
| `search <query>` | Search memory |
| `list memory` | Show all saved entries |
| `help` | Show available commands |
| `exit` | Close the assistant |
| `learn` | Guided step-by-step entry |
| `remember <name> <data>` | Save information to memory |
| `remember image <name> <data>` | Save image to memory |
| `edit <name>` | Edit a saved entry |
| `delete <name>` | Remove an entry from memory |
| `copy <name>` | Copy data to clipboard |
| `SHORTCUTS` | personalized shortcut commands |
| `LANGUAGE <code>` | Switch language (e.g. `language_it`) |

> All commands also work in Italian regardless of the active language.

---

## ⚙️ Configuration

Edit `_dati/configurazione.json` to personalise the assistant:

```json
{
  "nome_avatar":   "Alice",
  "nome_utente":   "Emanuele",
  "lingua":        "it",
  "frase_finale":  "See you soon!",
  "alias_comandi": {
    "apri": ["launch"],
    "esci": ["bye", "quit"]
  },
  "risposte_fisse": {
    "thanks": "You're welcome, {nome_utente}!",
    "hello":  "Hello, {nome_utente}!"
  },
  "shortcut": [
    { "etichetta": "Bank statement", "comando": "open statement" },
    { "etichetta": "Mail",           "comando": "open mail" }
  ]
}
```

---

## 🌍 Adding a new language

1. Copy `_dati/lang_en.json` to `_dati/lang_fr.json` (or any language code)
2. Translate all values — **never translate the keys**
3. Set `"lingua_stt"` to the correct Google Speech code (e.g. `"fr-FR"`)
4. Add command aliases in the `"alias_comandi"` section for natural
   input in that language
5. Restart the assistant — the new language appears automatically
   in the language selector panel

---

## 📦 Building a distributable package

PyInstaller does not compile Python to machine code — it **bundles** the
interpreter, all dependencies and your script into a single distributable
folder that runs on machines without Python installed.

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

After bundling, copy `lang_it.json`, `lang_en.json` and your `_dati/`
folder next to the executable before running.

## 📋 Dependencies

| Library | Purpose | Required |
|---------|---------|----------|
| `tkinter` | GUI | ✅ included in Python |
| `pillow` | Avatar images | ❌ recommended |
| `opencv-python` | Avatar MP4 video | ❌ recommended |
| `SpeechRecognition` | Voice input (STT) | ❌ recommended |
| `sounddevice` | Microphone capture | ❌ recommended |
| `numpy` | Audio processing | ❌ recommended |
| `pywin32` | Voice output (TTS) | ❌ Windows only |
| `portaudio` | Audio driver | ❌ Linux system package |

---

## 📁 Project structure

```
assistenteVOICE.py      ← main script
assistente.ico          ← Windows icon
assistente.png          ← Linux icon
_dati/
  configurazione.json
  memoria.json
  memoria.json.bak      ← automatic backup
  lang_it.json
  lang_en.json
  asset/
    avatar/             ← .jpg .png .gif .mp4 avatar files
```

---

## 📜 License

MIT

---

## 👤 Author

**[Emanuele Cassani](https://www.steppa.net/cassani/business_cardENG.htm)**  
Creator and maintainer of the *Personal Desktop Assistant Toolkit*.

