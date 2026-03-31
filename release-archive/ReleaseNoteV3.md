# v3.x — Major update: Multi-platform TTS, AI integration, and natural language commands

## New Features

### 1. **Multi-platform TTS (pyttsx3)**

Replaced Windows-only `win32com` with `pyttsx3` for cross-platform voice synthesis.
- **Windows**: SAPI5 (same as before)
- **macOS**: NSSpeechSynthesizer
- **Linux**: eSpeak (requires `sudo apt-get install espeak`)
- **New config section** in `config.json`:

```json
  "tts_config": {
      "engine": "auto",
      "rate": 150,
      "volume": 0.9,
      "pitch": 50,
      "voice_gender": "auto"
  }
```


### 2. Configurable STT parameters

Moved all speech recognition settings to config.json for user tuning:

```json
"stt_config": {
    "soglia_rumore": 200,
    "sample_rate": 16000,
    "max_secondi": 10,
    "silenzio_secondi": 0.5,
    "lingua": "it-IT"
}
```

Auto-detects optimal noise threshold based on OS (2000 for Linux, 200 for others)

Users can now adjust microphone sensitivity without code changes

### 3. Natural language parsing with stop-words
Added article/stop-word filtering for more natural commands:

New "articoli" section in language files (lang_XX.json)

Removes words like "il", "la", "the", "der" before command parsing

Example: "dammi il codice" now works identically to "dammi codice"

### 4. Internationalization improvements
Renamed config files to English standards: config.json, memory.json

"Send" button now localized via self._t("btn_invia")

Full language packs in addition to Italian and English:
German (lang_de.json), Spanish (lang_es.json), French (lang_fr.json),
Russian (lang_ru.json), Portugese (lang_pt.json), Brasilian (lang_br.json),
Chinese (lang_cn.json), Japanese (lang_jp.json), Korean (lang_kr.json),
Arabian (lang_ar.json).

Each language file includes region-specific STT codes (pt-PT, pt-BR, zh-CN, ar-SA)

### 5. New "configura" command with interactive wizard
Three modes for easy configuration:

configura lista - Lists all available parameters

configura [parametro] - Modify a single parameter

configura (no args) - Launches guided wizard through main settings

Supports nested parameters (e.g., tts_config.rate)

Wizard proposes parameters one by one with current value display

### 6. AI Integration (optional)
Added fallback AI support for unrecognized commands:

Providers: OpenAI (GPT-3.5/4) and Google Gemini

Config section in config.json:

```json
"ai_config": {
    "enabled": false,
    "provider": "openai",
    "api_key": "",
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 500,
    "fallback_to_ai": true
}
```

Priority: Local commands always first, AI only as fallback

Threaded execution to prevent UI freezing

---

## Bug Fixes
TTS interruption: Fixed _toggle_tts() to properly stop ongoing speech

Config migration: Automatic merge of new config keys with existing files

Language fallback: Improved fallback chain when language files are missing

STT threading: Better thread safety for microphone access

---

## Technical Improvements
Modular initialization: Separate methods for TTS, STT, and AI setup

Better error handling: Graceful degradation when components fail

Config validation: Automatic backup before saving corrupted files

Cross-platform paths: Consistent Pathlib usage for all file operations

New Language Files Structure
Each language file (lang_XX.json) now includes:

```json
{
    "articoli": ["the", "a", "an", ...],  // Stop-words for parsing
    "configura_*": "...",                   // Configuration wizard strings
    "ai_*": "...",                          // AI-related messages
    // ... all existing translations
}
```

Breaking Changes
File names: configurazione.json → config.json, memoria.json → memory.json
(Automatic fallback maintains backward compatibility)

TTS: Windows users no longer need win32com (now uses pyttsx3)

---

## Dependencies: pyttsx3 required for voice (cross-platform)

## Installation

### Base requirements (same as v2.2)
```bash
pip install tkinter speechrecognition sounddevice numpy pillow opencv-python
```

### New dependencies
```bash
pip install pyttsx3             # Required for TTS
pip install openai              # Optional: for OpenAI support
pip install google-generativeai # Optional: for Google Gemini
```

### Linux users need eSpeak for TTS
```bash
sudo apt-get install espeak    # Debian/Ubuntu
sudo dnf install espeak        # Fedora
```

### PyInstaller build for Linux and macOS
```bash
pyinstaller --onedir --noconsole --clean \
  --icon=iconLINUX.png \
  --collect-all PIL \
  --collect-all cv2 \
  --collect-all sounddevice \
  --collect-all speech_recognition \
  --collect-all pyttsx3 \
  --hidden-import numpy \
  --name assistente assistente3_x.py
```

### Windows build
```bash
pyinstaller --onedir --noconsole --clean ^
  --icon=iconWIN.ico ^
  --collect-all PIL ^
  --collect-all cv2 ^
  --collect-all pyttsx3 ^
  --name assistente assistente3_x.py
```

---

## Migration from v2.2
Existing configurazione.json and memoria.json will be automatically migrated

Old lang_it.json files will work but lack new features (add articoli section manually)

TTS now uses pyttsx3 - no action needed, works out of the box

---

## Known Issues
Linux TTS: eSpeak quality varies; consider installing MBROLA voices for better results

AI fallback: Requires Internet connection and valid API key

Video playback: Still requires OpenCV with codec support

---