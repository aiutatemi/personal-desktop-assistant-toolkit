# 🤖 **myAssistente** Personal Desktop Assistant
[![Support via PayPal](https://img.shields.io/badge/Support-PayPal-00457C?logo=paypal&logoColor=white)](https://www.paypal.com/pool/9nyLoeBeq8?sr=wccr)

A lightweight, privacy-first desktop assistant that lives on your machine.
No cloud subscriptions, no data sent anywhere — except for the optional
voice recognition, which uses Google Speech API only when you press the
microphone button.

Built with Python and Tkinter, it runs on **Windows** (full features) and
**Linux / macOS** (from release 3.x full features)

## 📘 Documentation
Access the documentation release 4.x (ENG/ITA) here:  
**[Open rel.4.x Documentation](https://www.steppa.net/cassani/articoli/assistente/docs/index.html)**
Access the full documentation folder (ENG/ITA) here:  
👉 **[Open folder](https://gitlab.com/EmanueleCAS/assistente/-/tree/master/docs)**
---

## ✨  Test Release 5.x Features 🛠In Progress🛠️

- Full compatibility with the AIML standard
- New aiml_parser.py
All features of previous releases except:
- Removed: optional external engine similar to AIML used in release 4

---
## ✨ Release 4.x Features

- External engine with AIML‑like syntax, configurable via JSON file
- Rebranding: **myAssistente** Personal Desktop Assistant
- New Header UI
- updated **configure** command
- New **search media** command (search music, video, picture inside -dati/asset/)
- Flexibility in understandin commands
- Bug fixig
- Distribuibile 🪟 **Windows** and 🐧 **Linux** ready ZIP archives
All features of previous releases

---
## ✨ Release 3.x Features

- **Multi-platform Voice output** TTS (pyttsx3)
- Configurable **STT parameters**
- **Natural language parsing** with **stop-words**
- **Internationalization** improvements (config.json memory.json and localization files)
- New command with **interactive wizard**, to configure config.json
- Optional **AI Integration**
- Localized in **12 languages** [Open localization folder](https://gitlab.com/EmanueleCAS/assistente/-/tree/master/localization-file)
- Distribuibile 🪟 **Windows** ready ZIP archive
All features of previous releases

---

## ✨ Features Release 2.x

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
- **Avatar support** — display images or MP4 animations as the assistant's face
- **Automatic backup** — memory file is backed up before every save
- Distribuibile 🪟 **Windows** and 🐧**Linux** ready ZIP archives

---

## 🖥️ Requirements

### Quick installation per platform

Windows (minimum working dependencies):
```bash
pip install pillow pyttsx3 pywin32
```

Windows (complete with STT and AI):
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

## 🚀 Quick start

```bash
python assistente.py
```

On first run, a `_dati/` folder is created next to the script containing:

```
_dati/
  config.json	← all settings
  memory.json	← your saved data
  lang_it.json	← Italian language file
  lang_en.json	← English language file
  asset/avatar/	← put your avatar images/videos here
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

Edit `_dati/config.json` to personalise the assistant:

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

1. Copy `_dati/lang_it.json` to `_dati/lang_en.json` (or any language code)
2. Translate all values — **never translate the keys**
3. Set `"lingua_stt"` to the correct Google Speech code (e.g. `"en-US"`)
4. Add command aliases in the `"alias_comandi"` section for natural
   input in that language
5. Restart the assistant — the new language appears automatically
   in the language selector panel

Please check if your language is already present in the repository /localization-file folder.

---

### 🌍 Available Languages

| ISO Code | Language (EN)            | File name          | Native name | Flag |
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

## 📦 Building a distributable package

PyInstaller **bundles** the interpreter, all dependencies 
and script into a single distributable folder that runs 
on machines without Python installed.

### Windows (replace assistenteX.X.py with release number)
```bash
pyinstaller --onedir --noconsole --clean ^
  --icon=assistente.ico ^
  --collect-all PIL ^
  --collect-all cv2 ^
  --name Assistente assistenteX.X.py
```

### Linux / macOS (replace assistenteX.X.py with release number)
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

After bundling, copy `lang_it.json`, `lang_en.json` and your `_dati/`
folder next to the executable before running.

## 📋 Dependencies releases >3.0

| Library | Purpose | Required | Note |
|---------|---------|----------|------|
| `tkinter` | GUI | ✅ included in Python | — |
| `json`, `os`, `re`, `shutil`, `subprocess`, `sys`, `random`, `threading`, `platform`, `pathlib`, `datetime` | Core functions | ✅ included in Python | — |
| `pillow` | Avatar images (jpg/png/gif) | ⚠️ recommended | Without: Just color placeholder |
| `opencv-python` | Video avatar MP4 | ⚠️ optional | Needs also `pillow` |
| `pyttsx3` | multiplatform TTS voice | ⚠️ recommended | Wrapper for following engines |
| `pywin32` | TTS SAPI5 engine | ⚠️ Windows only | Used by `pyttsx3` on Windows — often already included |
| `espeak` / `espeak-ng` | TTS engine | ⚠️ Linux only | System bundle: `sudo apt install espeak` |
| — | TTS NSSpeechSynthesizer engine | ✅ macOS only | already present in macOS, no installation required |
| `SpeechRecognition` | Input STT voice | ⚠️ optional | Uses Google Speech API (online) |
| `sounddevice` | Microphone | ⚠️ opzional | Needs PortAudio |
| `numpy` | audio STT | ⚠️ optional | Reqiured by `sounddevice` |
| `portaudio` | Driver audio for sounddevice | ⚠️ Linux/macOS only | `sudo apt install portaudio19-dev` / `brew install portaudio` |
| `openai` | AI integration (ChatGPT) | ⚠️ optional | Only if `ai_config.provider = "openai"` |
| `google-generativeai` | AI integration (Gemini) | ⚠️ optional | Only if `ai_config.provider = "gemini"` |


```

## 📁 Project structure

```
assistenteX.X.py      ← main script (Release X.X)
assistente.ico        ← Windows icon
assistente.png        ← Linux icon
_dati/
  config.json
  memory.json
  memory.json.bak      ← automatic backup
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

---

