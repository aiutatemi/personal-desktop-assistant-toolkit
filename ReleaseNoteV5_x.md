# myAssistente v5.1 — Release Notes  
# Desktop Personal Assistant  
# `https://www.steppa.net/cassani/articoli/myAssistente/myAssistente.htm` [(steppa.net in Bing)](https://www.bing.com/search?q="https%3A%2F%2Fwww.steppa.net%2Fcassani%2Farticoli%2FmyAssistente%2FmyAssistente.htm")

---

## Overview

Version 5.0 introduces a full **AIML 1.x standard engine**, replacing the proprietary  
`aiml_XX.json` format used in v4.x. The new engine is implemented as a standalone  
module (`aiml_parser.py`) and supports standard `.aiml` files, making it compatible  
with the large ecosystem of existing AIML knowledge bases.

Two additional features have been added: a **response source indicator** visible  
in the UI, and support for **AIML-triggered commands** that the engine can  
forward directly to the assistant for execution.

---

## New Features

### 1. AIML 1.x Standard Engine (`aiml_parser.py`)

The conversational engine has been completely rewritten as an independent module  
that parses and executes standard AIML 1.x files.

**Supported tags:**

| Tag | Description |
|-----|-------------|
| `<pattern>` | Input pattern with `*` and `_` wildcards (case-insensitive) |
| `<template>` | Response text, with optional `avatar="..."` attribute (see §2) |
| `<star/>` | Inserts text captured by wildcard; supports `index="N"` for multiple wildcards |
| `<srai>` | Redirects input to another pattern (alias / normalization) |
| `<set name="x">` | Sets a session variable |
| `<get name="x"/>` | Reads a session variable |
| `<random>` | Returns a random response from a list of `<li>` items |
| `<condition>` | If/else logic based on variable values (forms 1 and 2) |
| `<that>` | Contextual matching on the bot's last response |
| `<topic>` | Groups categories by topic; activated via `<set name="topic">` |

**Wildcard priority (high to low):**
1. Exact match (no wildcard)
2. `_` wildcard (high priority)
3. `*` wildcard (low priority)

Within each level: specific `<that>` beats `<that>*`, specific `<topic>` beats `<topic>*`.

**Matching behavior:**
- Case-insensitive — patterns do not need to be uppercase (unlike original AIML 1.x)
- Punctuation (`.,!?;:`) is removed before matching
- Wildcards match zero or more words including spaces

**Session variables:**  
The following predicates are pre-initialized from `config.json` at startup  
and after each configuration change:

```xml
<get name="nome_utente"/>   <!-- user name from config.json -->
<get name="nome_avatar"/>   <!-- assistant name from config.json -->
```

Any additional variable can be set freely with `<set name="...">`.

**File structure:**
```
_dati/
  aiml/
    it/
      saluti.aiml
      (any number of .aiml files)
    en/
      greetings.aiml
    (other language codes)
```

All `.aiml` files in the active language folder are loaded alphabetically at startup  
and reloaded automatically when the language is changed.  
If the folder does not exist, the program works normally without errors.

---

### 2. Avatar from AIML files

The `<template>` tag supports a custom `avatar` attribute — an extension of  
the myAssistente project, silently ignored by standard AIML parsers:

```xml
<category>
    <pattern>CIAO</pattern>
    <template avatar="sorridente">Ciao <get name="nome_utente"/>!</template>
</category>
```

If the `avatar` attribute is absent, the assistant uses a random avatar as before.  
The value is the image filename without extension (same convention as v4.x).

---

### 3. AIML-triggered commands

A `comando` attribute on `<template>` allows an AIML rule to trigger any  
assistant command directly, as if the user had typed it:

```xml
<category>
    <pattern>PUOI APRIRE IL PROGRAMMA DI POSTA</pattern>
    <template comando="apri posta">Sure, opening your mail app!</template>
</category>

<category>
    <pattern>* APRI * POSTA *</pattern>
    <template comando="apri posta">Opening mail!</template>
</category>
```

The template text is shown to the user, then the value of `comando` is passed  
to the assistant's input handler and executed normally — including memory lookup,  
link opening, etc.

This makes AIML a **natural language translator** for assistant commands:  
users can phrase requests freely and AIML maps them to the correct command.

---

### 4. Configurable response mode

A new `risposta_config` section in `config.json` controls how the assistant  
chooses between AIML and external AI:

```json
"risposta_config": {
    "modalita": "aiml_then_ai"
}
```

| Mode | Behavior |
|------|----------|
| `aiml_then_ai` | AIML first; if no match, falls back to AI (default) |
| `aiml_only` | AIML only; if no match, shows "not understood" message |
| `ai_only` | External AI only; AIML is ignored |

The mode can be changed at runtime with the `configura` command:  
`configura risposta_config.modalita`

**Updated response priority:**
1. Fixed responses (`risposte_fisse` in `config.json`)
2. Commands (`apri`, `dammi`, `cerca`, etc.)
3. AIML engine (if mode allows)
4. External AI — OpenAI / Gemini (if mode allows and configured)
5. "Not understood" message

---

### 5. Response source indicator

A small colored dot with label is displayed above the avatar (bottom-left),  
showing where the last response came from:

| Color | Label | Source |
|-------|-------|--------|
| 🟢 Green | `memory` | Data retrieved from `memory.json` (`dammi`, `cerca`, `apri`) |
| 🔵 Blue | `AIML` | Response from a `.aiml` file |
| 🔴 Red | `AI` | Response from external AI (OpenAI / Gemini) |
| ⚫ Grey | `—` | System messages (startup, help, not understood, configuration) |

---

## Bug Fix

### Scroll position in the output area (Windows + Python 3.14)

On Windows with Python 3.14, the output text area did not scroll to the bottom  
after each response, or scrolled upward unexpectedly.

**Root cause:** a race condition between `update_idletasks()` called inside  
`_reset_avatar_label()` and the scroll operation. The avatar layout update  
was resetting the scroll position before it could stabilize.

**Fix:** removed `update_idletasks()` from `_reset_avatar_label()` and replaced  
the immediate `see(tk.END)` call with `root.after(10, ...)`, giving the avatar  
update 10ms to complete before scrolling. The delay is imperceptible to the user.

---

## Technical Changes

### New file
- `aiml_parser.py` — standalone AIML 1.x parser, no external dependencies.  
  Must be placed in the same folder as `myAssistente5_0.py`.  
  Can be run directly (`python aiml_parser.py`) for a self-test.

### Removed
- `carica_aiml()` function — replaced by `AIMLParser.carica_cartella()`
- `aiml_match()` function — replaced by `AIMLParser.rispondi()`
- `_aiml_rispondi()` method — logic now inline in `_gestisci_input()`
- `_aiml_regole`, `_aiml_ignora`, `_aiml_contesto` instance variables

### Modified
- `_gestisci_input()` — AIML/AI dispatch now respects `risposta_config.modalita`
- `_cmd_lingua()` — calls `AIMLParser.scarica_tutto()` then reloads the new language folder
- `_configura_fine()` — updates AIML predicates (`nome_utente`, `nome_avatar`) after configuration changes

### File structure
```
_dati/
  config.json          — now includes "risposta_config" section
  memory.json          — unchanged
  aiml/                — NEW: replaces aiml_XX.json
    it/
      saluti.aiml
    en/
      (future files)
  lang_IT.json         — unchanged
  lang_EN.json         — unchanged
  asset/               — unchanged
    avatar/
```

### New key in `config.json`
```json
"risposta_config": {
    "modalita": "aiml_then_ai"
}
```

---

## Dependencies

No new external dependencies.  
`aiml_parser.py` uses only standard Python libraries (`re`, `random`, `xml.etree.ElementTree`, `pathlib`).

---

## Migration from v4.x

1. Replace `myAssistente4_x.py` with `myAssistente5_0.py`
2. Add `aiml_parser.py` to the same folder as the `.py` file
3. Create the folder `_dati/aiml/it/` (or the language code in use)
4. Move or rewrite conversational rules from `_dati/aiml_IT.json` into `.aiml` files  
   — see `saluti.aiml` for annotated examples of all supported tags
5. Existing `config.json` and `memory.json` are fully compatible;  
   `risposta_config` will be added automatically with default value `aiml_then_ai`  
   on first run if not present
6. The old `aiml_XX.json` files are no longer loaded and can be archived or deleted

---

## Known Issues (unchanged from v4.x)

- Linux TTS: eSpeak quality varies; MBROLA voices recommended
- AI fallback: requires Internet connection and valid API key
- Video playback: requires OpenCV with codec support

---
