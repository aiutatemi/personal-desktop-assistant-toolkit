# 🌍 Adding a New Language

This guide explains how to add support for a new language to the assistant.
The workflow is simple, modular, and designed to keep all localization files consistent.
Valid for all releases of myAssistant

---

0. Check if the language already exists
Before creating anything new, verify whether the language file is already available:
[Localization files folder](https://gitlab.com/EmanueleCAS/assistente/-/tree/master/localization-file)

If it exists, you can still contribute: download it, improve it, and submit your updated version.

1. Create the new language file
Copy the Italian template:

```
_dati/lang_it.json → _dati/lang_XX.json
```
Replace XX with the correct language code (e.g., en, de, es, pt).

2. Translate only the values
Translate every value in the JSON file, but never translate the keys.
This ensures compatibility with the assistant’s internal logic.

3. Check correct "lingua_stt"
Set the correct Google Speech‑to‑Text code in "lingua_stt"  
(mandatory for correct voice recognition)

Important natural‑language command aliases in "alias_comandi"  
to make the assistant a better understand of commands in the new language

4. Restart the assistant
After restarting, the new language will automatically appear
at the bottom of the right‑side panel.

---

## Example: ./_dati/config.json
```json
{
  "nome_avatar": "Assistant", 		<- assistant name
  "nome_utente": "user", 		<- username
  "avatar_iniziale": "benvenuto",	<- .jpg picture used at startup
  "avatar_random": [
    "sorridente",
    "coniglio",
    "soddisfatto"
  ],
  "avatar_finale": "ciao.mp4",		<- .mp4 video used at the end
  "frase_finale": "Ciao!",		<- final phrase
  "lingua": "en",  			<- Language at startup
  "tts_config": {
    "engine": "auto",
    "rate": 150,
    "volume": 0.9,
    "pitch": 50,
    "voice_gender": "auto"
  },
  "stt_config": {
    "soglia_rumore": 200,
    "sample_rate": 16000,
    "max_secondi": 10,
    "silenzio_secondi": 0.5,
    "lingua": "en-US"   		<- Google Speech code for your language
  },
  "ai_config": {
    "enabled": false,
    "provider": "openai",
    "api_key": "",
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 500,
    "fallback_to_ai": true
  },
  "shortcut": [   			<- Modify the commands that appear under SHORCUT
    {
      "etichetta": "Quiet please",	<- Usefull command, translat in your language
      "comando": "ok"
    },
    {
      "etichetta": "Task manager",	<- Works on Windows OS only
      "comando": "open task"
    },
    {
      "etichetta": "Control panel",	<- Works on Windows OS only
      "comando": "open panel"
    },
    {
      "etichetta": "Configure",		<- Works on Windows OS only
      "comando": "configura"
    }
  ]

```

---