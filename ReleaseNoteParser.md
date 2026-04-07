# aiml_parser.py — Release Notes
# to be used with myAssistente5
# `https://www.steppa.net/cassani/articoli/myAssistente/myAssistente.htm` [(steppa.net)](https://www.bing.com/search?q="https%3A%2F%2Fwww.steppa.net%2Fcassani%2Farticoli%2FmyAssistente%2FmyAssistente.htm")

## Version 1.3.0

### Features
- pattern normalization to UPPERCASE
- `<template>` tags supported

---

#### User predicates

| Tag | Syntax | Description |
|-----|--------|-------------|
| `<get>` | `<get name="x"/>` | Reads the value of user predicate `x` |
| `<set>` | `<set name="x">...</set>` | Writes user predicate `x` (does not emit text in the reply) |

User predicates are initialized externally with `set_predicato("nome", "valore")`.
The special predicate `topic` automatically updates the conversation topic.

---

#### Bot predicates

| Tag | Syntax | Description |
|-----|--------|-------------|
| `<bot>` | `<bot name="x"/>` | Reads the value of bot predicate `x` (read-only in templates) |

Bot predicates are configured with `set_bot_predicato("nome", "valore")`.  
Predefined ones available: `name`, `version`, `master`, `dateformat`.

---

#### Wildcards and input

| Tag | Syntax | Description |
|-----|--------|-------------|
| `<star>` | `<star/>` or `<star index="N"/>` | First (or N‑th) wildcard captured by the pattern |
| `<input>` | `<input/>` or `<input index="N"/>` | Current user input; with `index` retrieves previous turns |
| `<that>` | `<that/>` or `<that index="N"/>` | Last bot reply (normalized); with `index` retrieves previous ones |
| `<topicstar>` | `<topicstar/>` | Wildcard of the current topic *(new in v1.2.0)* |

---

#### Redirect

| Tag | Syntax | Description |
|-----|--------|-------------|
| `<srai>` | `<srai>TEXT</srai>` | Recursive pattern lookup (max 20 levels) |

---

#### Logic and selection

| Tag | Syntax | Description |
|-----|--------|-------------|
| `<random>` | `<random><li>A</li><li>B</li></random>` | Randomly returns one of the `<li>` elements |
| `<condition>` | see examples below | Conditional branching based on predicates |

**Supported `<condition>` forms:**

```xml
<!-- Compact form -->
<condition name="x" value="y">text if x == y</condition>

<!-- List form with default -->
<condition name="x">
    <li value="a">text if x == a</li>
    <li value="b">text if x == b</li>
    <li>default text</li>       <!-- <li> without value = else branch -->
</condition>
```

---

#### Text Transformations

| Tag | Syntax | Description |
|-----|----------|-------------|
| `<uppercase>` | `<uppercase>...</uppercase>` | Converts content to UPPERCASE |
| `<lowercase>` | `<lowercase>...</lowercase>` | Converts content to lowercase |
| `<formal>` | `<formal>...</formal>` | Capitalizes The First Letter Of Each Word (since v1.2.0)* |
| `<sentence>` | `<sentence>...</sentence>` | Capitalizes the first letter of the sentence (since v1.2.0)* |
| `<explode>` | `<explode>...</explode>` | I n s e r t s s p a c e s b e t w e e n c h a r a c t e r s (since v1.2.0) |

---

#### System Tags *(since v1.1)*

| Tag | Syntax | Description |
|-----|----------|-------------|
| `<date>` | `<date/>` or `<date format="%d/%m/%Y"/>` | Local date/time. Format follows strftime; if omitted, uses bot predicate `dateformat` |
| `<size>` | `<size/>` | Number of AIML categories currently loaded |
| `<version>` | `<version/>` | Parser version (bot predicate version, default 1.3.0) |
| `<id>` | `<id/>` | UUID identifier of the current session (or bot predicate id) |

---

#### Punctuation and Spacing *(since v1.1)*

| Tag | Syntax | Output |
|-----|----------|--------|
| `<br>` | `<br/>` | Line break `\n` |
| `<p>` | `<p/>` | Paragraph `\n\n` |

---

#### Special Attributes on `<template>`

| Attribute | Example | Description |
|-----------|---------|-------------|
| `avatar` | `<template avatar="sorridente">` | Passes the avatar expression name in the dict returned by `rispondi()` |
| `comando` | `<template comando="apri_menu">` | Passes an arbitrary command to the main program in the returned dict |
| `menu` | `<template menu="1111">` | Opens or closes the 4 side menus (COMMANDS, MEMORY, SHORTCUT, LANGUAGE)

The dict returned by rispondi() always has the structure:
```python
{
    "testo":   "...",   # reply text
    "avatar":  "...",   # value of avatar= (or None)
    "comando": "...",   # value of comando= (or None)
    "menu":    "...",   # value of menu= (or None)
}
```

---

#### Silent Execution Tags *(since v1.1)*

| Tag | Syntax | Description |
|-----|----------|-------------|
| `<think>` | `<think>...</think>` | Executes content without emitting any text in the reply. Typically used to wrap `<set>` and `<condition>` that must update internal state without visible output. |

**Example::**
```xml
<template avatar="coniglio2">
    Which rabbit?
    <think><set name="step">2</set></think>
</template>
```

---

#### Fix v1.1.0 — Avatar propagated through `<srai>`

Previously, if a category was reached through a chain of  `<srai>`, the final template’s `avatar=` (and `comando=`) attribute was lost.
It is now correctly propagated to the reply returned by `rispondi()`.

Fix in testConiglio.aiml:

```xml
<category>
    <pattern>* RABBIT *</pattern>
    <template><srai>CONIGLIO.GESTORE</srai></template>
</category>
<category>
    <pattern>CONIGLIO.GESTORE</pattern>
    <template><srai>CONIGLIO.STEP.1</srai></template>
</category>
<category>
    <pattern>CONIGLIO.STEP.1</pattern>
    <template avatar="coniglio2">WHICH RABBIT?</template>
</category>
```
---

### Python API 

| Method | Description |
|--------|-------------|
| `set_predicato(name, value)` | Sets a user predicate |
| `get_predicato(name)` | Reads a user predicate |
| `set_bot_predicato(name, value)` | Sets a bot predicate *(since v1.2.0)* |
| `get_bot_predicato(name)` |	Reads a bot predicate *(since v1.2.0)* |
| `set_topic(topic)` | Sets the current topic |
| `carica_file(path)` | Loads an `.aiml` file |
| `carica_cartella(folder)` | Loads all `.aiml` files in a folder |
| `scarica_tutto()` | Removes all categories and resets state |
| `rispondi(text, user)` | Processes input and returns the reply dict |
| `info()` | Diagnostic string about current state |
| `dump_categorie(n)` | Prints the first n loaded categories |

---

### Compatibility Notes

The parser implements a subset of AIML 1.x.
Unrecognized tags are traversed recursively without error, 
so AIML files using unsupported tags remain loadable: 
the unknown tag is ignored and the textual content is still evaluated.