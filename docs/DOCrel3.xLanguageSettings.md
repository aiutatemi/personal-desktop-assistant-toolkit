# 🌍 Adding a New Language
This guide explains how to add support for a new language to the assistant.
The workflow is simple, modular, and designed to keep all localization files consistent.

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
Replace XX with the correct language code (e.g., en, fr, de, pt).

2. Translate only the values
Translate every value in the JSON file, but never translate the keys.
This ensures compatibility with the assistant’s internal logic.

3. Update config.json
Inside ./_dati/config.json:

Set the correct Google Speech‑to‑Text code in "lingua_stt"  
(mandatory for correct voice recognition)

Optionally add natural‑language command aliases in "alias_comandi"  
to make the assistant a better understand of commands in the new language

4. Restart the assistant
After restarting, the new language will automatically appear
at the bottom of the right‑side panel.

---

## Example: ./_dati/config.json
```json
  "stt_config": {
    "soglia_rumore": 200,
    "sample_rate": 16000,
    "max_secondi": 10,
    "silenzio_secondi": 0.5,
    "lingua": "it-IT"   <- Google Speech code for your language
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
  "alias_comandi": {
    "dammi": [      <- keep the key in Italian; customize the aliases
      "dimmi",
      "mostrami",
      "visualizza"  <- example with three alias names for the same key word
    ],
    "aiuto": [
      "help"        <- example with one alias name
    ],
    "esci": []      <- leave empty when no alias needed
```

---