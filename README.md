# Personal Assistant — Quick Guide (v2.1)

## Requirements

Python 3.9+  
pip install pillow imageio imageio-ffmpeg   (optional, for images/video)

For the VOICE version (TTS/STT):  
pip install SpeechRecognition sounddevice numpy opencv-python Pillow pywin32

**Compatibility: TTS Windows only**  
TTS The voice engine uses Windows SAPI (win32com).  
STT (speech recognition) is cross‑platform.

---

## Folder structure

assistente.py  
_dati/  
• configurazione.json  
• memoria.json  
• lang_it.json  
• lang_en.json  
• asset/  
 • avatar/  
  • benvenuto.jpg  
  • sorridente.jpg  
  • soddisfatto.jpg  
  • triste.jpg  
  • magazziniere.jpg  
  • ciao.mp4  

---

## Configuration ( _dati/configurazione.json )

{  
"avatar_name": "Assistant",  
"user_name": "Emanuele",  
"initial_avatar": "benvenuto",  
"random_avatars": ["sorridente", "soddisfatto"],  
"final_avatar": "ciao.mp4",  
"language": "it"  
}

• Change user_name to your name  
• Add as many images as you want to random_avatars  
• Names must match the files in _dati/asset/avatar/  
• The language key defines the active language (v2.1+)

---

# What’s new in release 2.0 — VOICE

## Voice features

### STT — Speech To Text
• Based on SpeechRecognition + sounddevice  
• Uses Google Speech API (free, requires internet)  
• Automatic stop on silence  
• Runs in a separate thread to keep the UI responsive  

### TTS — Text To Speech (Windows only)
• Based on Windows SAPI (win32com)  
• Works offline  
• Every assistant reply can be spoken aloud  
• Can be interrupted instantly by clicking mute or saying/typing “OK”  

### VOICE interface
• 🎤 to speak (turns red while listening)  
• 🔊 / 🔇 to enable or mute TTS  
• If libraries are missing, buttons appear disabled  

---

# What’s new in release 2.1 — Localization system (i18n)

## Separate language files

All UI strings are now stored in dedicated JSON files:

_dati/lang_it.json  
_dati/lang_en.json  

To add a new language: copy lang_it.json, translate it, and save as lang_XX.json.

## Change language via command

language en  
language it  

The change is immediate and saved in the configuration file.

## Automatic STT language

Speech recognition automatically uses the locale defined in the active language file (e.g., it-IT, en-US).

## Adaptive TTS voice (Windows)

The program tries to use a system voice matching the selected language; if unavailable, it falls back to the default system voice.

## Cascading fallback

1. _dati/lang_XX.json  
2. Executable folder  
3. Built‑in Italian fallback  

---

# What’s new in release 2.2 — Language selector in the UI

## Graphical language selector in the command panel

At the bottom of the side panel, a LINGUA section appears with one button for each lang_XX.json file found.

• Active language: ● with highlighted background  
• Other languages: ○  

Languages are detected automatically at startup.

## Language label mapping

it — Italian  
en — English  
de — German  
es — Spanish  
pt — Portuguese  
fr — French  

For unknown codes, the uppercase code is shown (e.g., JA).

---

# Main commands

### remember
Saves information to memory.  
Examples:  
remember my TV data  
remember Roberta’s tax code  
remember the bank statement link  
remember this image  

### give
Retrieves saved information.  
give my TV data  
give Roberta’s tax code  

### open
Opens saved files, folders, or URLs.  
open bank statement  

### search
Partial search across all fields.  
search TV  
search Roberta  

### list
Shows all saved entries.

### edit
Updates a field of a saved entry.

### delete
Removes an entry (with confirmation).

### copy
Copies a value to the clipboard.  
copy Roberta tax code  

### help
Shows the list of commands.

---

# Technical notes

• Without Pillow: avatar shown as a colored box  
• With Pillow: real images  
• With imageio: .mp4 video support  
• memoria.json can be edited manually  
• AI API integration ready (see # TODO: API_INTEGRATION)

---

# Optional dependencies installation

pip install pillow  
pip install imageio imageio-ffmpeg  
pip install SpeechRecognition sounddevice numpy opencv-python Pillow pywin32  

---

**Emanuele Cassani**  
[https://www.steppa.net/cassani/business_card.htm](https://www.steppa.net/cassani/business_card.htm)