# myAssistente v4.1 — Release Notes  
# Desktop Personal Assistant  
# `https://www.steppa.net/cassani/articoli/myAssistente/myAssistente.htm` [(steppa.net in Bing)](https://www.bing.com/search?q="https%3A%2F%2Fwww.steppa.net%2Fcassani%2Farticoli%2FmyAssistente%2FmyAssistente.htm")

---

## New Features

### 1. Rebranding: myAssistente

The program has been renamed **myAssistente** (formerly “Assistente personale desktop”).  
The name and URL are now configurable directly in the `.py` file through two constants:

```python
APP_NAME = "myAssistente"
APP_URL  = "https://www.steppa.net/cassani/..."
```

---

### 2. Header UI with program name and clickable link

A header bar has been added at the top of the window (top-left) with:
- Program name (`APP_NAME`) highlighted
- Clickable URL (`APP_URL`) that opens the browser when clicked
- Hover effect with color change and underline

To customize name and link, simply edit the two constants  
`APP_NAME` and `APP_URL` at the top of the `.py` file.  
No changes to JSON files are required.

---

### 3. External AIML engine (conversational phrases)

A conversational response system has been added, based on external JSON files,  
one per language, supporting:

- **Exact match** — literal trigger (e.g., `"ciao"`)
- **Wildcard `*`** — matches zero or more characters anywhere  
  (e.g., `"*rabbit*"` matches “I saw a white rabbit”)
- **Placeholders** — `{nome_utente}`, `{nome_avatar}`, `{ora}`, `{data}`,  
  `{data_breve}`, `{giorno}`
- **Response avatar** — optional `"avatar"` field without extension (= .jpg)  
  or with explicit extension (e.g., `"avatar": "smile.png"`)
- **Contextual followup** — each rule may define a `"followup"` block with  
  responses for the user’s immediate next message.  
  The catch‑all `"*"` handles unexpected replies.
- **Ignore characters** — `"ignora_caratteri"` field to normalize input  
  (e.g., `"!?,.:;\"'"` removes punctuation before matching)

**Response priority (top to bottom):**
1. AIML (`aiml_XX.json`) — highest priority  
2. Fixed responses (`risposte_fisse` in `config.json`) — fallback  
3. Commands (`apri`, `dammi`, `cerca`, etc.)  
4. External AI (OpenAI / Gemini) — final fallback if enabled

**File to create:** `_dati/aiml_IT.json` (or `_EN`, `_DE`, etc.)  
Language is detected automatically from the `"lingua"` key in `config.json`.  
If the file does not exist, the program works normally without errors.  
When changing language, the AIML file is reloaded and followup context reset.

**Format of `aiml_XX.json`:**

```json
{
  "ignora_caratteri": "!?,.:;\"'",
  "regole": [
    {
      "trigger": "ciao",
      "risposta": "Hello {nome_utente}!",
      "avatar": "sorridente",
      "followup": {
        "bene":  "Great!",
        "male":  "I'm sorry.",
        "*":     "Alright, go ahead."
      }
    },
    {
      "trigger": "*rabbit*",
      "risposta": "Which rabbit?",
      "avatar": "dubbio"
    }
  ]
}
```

Wildcard triggers have lower priority than exact triggers  
(automatic sorting at startup).

---

### 4. Completely rewritten `configura` command — dynamic from config.json

The configuration wizard now reads keys **directly from `config.json`**,  
with no hardcoded values in the code.  
Every key in the file becomes automatically configurable, including nested keys  
(using dot notation: `tts_config.rate`).

**Behavior:**
- `configura` — starts the wizard: shows all keys with current values  
  and lets the user choose which one to modify
- `configura lista` — shows the full list with current values
- `configura tts_config.rate` — directly configures a single parameter

**Automatic type conversion:**  
The entered value is converted to the original parameter type  
(int, float, bool, CSV list).

**Validation:**  
Range 0.0–1.0 for volume, integer required for rate, etc.

**Only exclusion:** `shortcut` (structure too complex for inline editing;  
must be edited directly in `config.json`).

**Robust interruption:**
- Empty ENTER → asks for confirmation (“Do you want to stop?”)
- `stop` / `annulla` / `fine` → stops immediately
- Confirmation message is localizable via `lang_XX.json` (`elimina_si`)

---

### 5. Cross‑flexibility between `apri` and `dammi`

The two commands now “help” each other when they find the wrong type of data:

**`dammi <name>`** finds a link (URL or file path):  
> `I found a link for '<name>'. Do you want me to open it?`  
> Reply `s / si / ok / apri` → opens the link; anything else → shows the text data

**`apri <name>`** finds non‑openable data (plain text):  
> `I only found data (not a link) for '<name>': … Do you want to see it?`  
> Reply `s / si / ok / vedi` → shows the data; anything else → cancels

Link detection recognizes:  
HTTP/HTTPS/FTP URLs, `mailto:`, `file://`, Windows paths (`C:\...`),  
Unix paths (`/...`, `./...`), executable and document extensions  
(`.exe`, `.bat`, `.pdf`, `.docx`, `.html`, etc.).

Both use the states `attesa_conferma_apri` / `attesa_conferma_dammi`,  
consistent with other commands (delete, modify, etc.).  
Strings are localizable in `lang_XX.json`:  
`dammi_trovato_link`, `apri_trovato_dato`, `conferma_si`.

---

### 6. New `media` command + extension of `cerca`

Added media file search in the `_dati/asset/` folder.

**Syntax:**
```
cerca immagine     (alias: cerca foto, cerca immagini)
cerca musica       (alias: cerca audio, cerca canzone/canzoni)
cerca video        (alias: cerca film)
media immagine     (short alternative)
media musica
media video
```

**Flow:**
1. Scans `_dati/asset/` for extensions of the requested type  
2. If found: `I found {n} images in the asset/ folder. Do you want the list?`  
3. If empty/missing: `Unfortunately I have no images in my memory`  
4. On confirmation, shows the numbered list of found files

**Recognized extensions:**
- Images: `.jpg .jpeg .png .gif .webp .bmp`
- Music: `.mp3 .wav .ogg .flac .aac`
- Video: `.mp4 .avi .mov .mkv .webm`

A **search media** button has been added to the side panel.  
All strings are localizable in `lang_XX.json` (`cerca_media_*`).

---

## Bug Fix

### Automatic backup of `config.json`

Added centralized `salva_config(cfg)` function:  
before each write to `config.json`, a `config.json.bak` backup is created.  
Previously, some writes (language change, configuration wizard) occurred inline  
without backup, risking loss of customizations  
(especially `alias_comandi`).

---

## Technical Changes

### File structure
```
_dati/
  config.json        — configuration (with automatic .bak backup)
  memory.json        — memory (with automatic .bak backup)
  aiml_IT.json       — NEW: Italian conversational phrases (optional)
  aiml_EN.json       — NEW: English conversational phrases (optional)
  lang_IT.json       — Italian UI strings
  lang_EN.json       — English UI strings
  asset/             — images, music, videos searchable via “cerca media”
    avatar/          — assistant avatars
```

### New strings in `lang_XX.json`

Added to previous release language files for the new features:

```json
"dammi_trovato_link":     "I found a link for '{nome}'. Do you want me to open it?",
"apri_trovato_dato":      "I only found data (not a link) for '{nome}': {dati}\nDo you want to see it?",
"conferma_si":            ["y", "ok", "yes", "open", "go", "see"],
"cerca_media_immagini":   "images",
"cerca_media_musica":     "music",
"cerca_media_video":      "videos",
"cerca_media_trovati":    "I found {n} {tipo} in the asset/ folder. Do you want the list?",
"cerca_media_vuoto":      "Unfortunately I have no {tipo} in my memory (asset/ empty or missing).",
"cerca_media_lista":      "List of {tipo} in asset/ ({n}):",
"cerca_media_lista_si":   ["y", "ok", "yes", "open", "go", "see", "list", "show"],
"panel_media":            "search media",
"configura_vuoi_interrompere": "Do you want to stop the configuration? (yes/no)"
```

### Notes for `config.json`

The `risposte_fisse` key remains supported as fallback but can be gradually  
emptied in favor of `aiml_XX.json`, which offers greater flexibility  
(wildcards, avatars, followup).

---

## Dependencies

No new dependencies compared to v3.x.  
The AIML engine uses only standard Python libraries (`json`, `re`, `pathlib`).

---

## Migration from v3.x

1. Replace the `.py` file with `myAssistente.py`  
2. Download and replace all the `lang_XX.json` files in use, updated in the repositoy with new strings   
3. Download or create `_dati/aiml_IT.json` (optional) using the provided example  
4. Existing `config.json` and `memory.json` are fully compatible  
5. The `alias_comandi` key in `config.json` is now correctly preserved  
   by all automatic saves thanks to `salva_config()`

---

## Known Issues (unchanged from v3.x)

- Linux TTS: eSpeak quality varies; MBROLA voices recommended  
- AI fallback: requires Internet connection and valid API key  
- Video playback: requires OpenCV with codec support

---