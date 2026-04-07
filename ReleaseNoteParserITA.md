# aiml_parser.py — Release Notes

## Versione 1.3.0

- normalizzazione pattern in MAIUSCOLO
- Tag `<template>` supportati

---

#### Predicati utente

| Tag | Sintassi | Descrizione |
|-----|----------|-------------|
| `<get>` | `<get name="x"/>` | Legge il valore del predicato utente `x` |
| `<set>` | `<set name="x">...</set>` | Scrive il predicato utente `x` (non emette testo nella risposta) |

I predicati utente si inizializzano dall'esterno con `set_predicato("nome", "valore")`.
Il predicato speciale `topic` aggiorna automaticamente il topic della conversazione.

---

#### Predicati bot

| Tag | Sintassi | Descrizione |
|-----|----------|-------------|
| `<bot>` | `<bot name="x"/>` | Legge il valore del predicato bot `x` (sola lettura nei template) |

I predicati bot si configurano con `set_bot_predicato("nome", "valore")`.  
Predefiniti disponibili: `name`, `version`, `master`, `dateformat`.

---

#### Wildcard e input

| Tag | Sintassi | Descrizione |
|-----|----------|-------------|
| `<star>` | `<star/>` oppure `<star index="N"/>` | Prima (o N-esima) wildcard catturata dal pattern |
| `<input>` | `<input/>` oppure `<input index="N"/>` | Input corrente dell'utente; con `index` recupera i turni precedenti |
| `<that>` | `<that/>` oppure `<that index="N"/>` | Ultima risposta del bot (normalizzata); con `index` recupera le precedenti |
| `<topicstar>` | `<topicstar/>` | Wildcard del topic corrente *(novità v1.2.0)* |

---

#### Redirect

| Tag | Sintassi | Descrizione |
|-----|----------|-------------|
| `<srai>` | `<srai>TESTO</srai>` | Ricerca ricorsiva di un pattern (max 20 livelli) |

---

#### Logica e selezione

| Tag | Sintassi | Descrizione |
|-----|----------|-------------|
| `<random>` | `<random><li>A</li><li>B</li></random>` | Restituisce casualmente uno degli elementi `<li>` |
| `<condition>` | vedi esempi sotto | Ramificazione condizionale basata su predicati |

**Forme di `<condition>` supportate:**

```xml
<!-- Forma compatta -->
<condition name="x" value="y">testo se x == y</condition>

<!-- Forma a lista con default -->
<condition name="x">
    <li value="a">testo se x == a</li>
    <li value="b">testo se x == b</li>
    <li>testo default</li>       <!-- <li> senza value = ramo else -->
</condition>
```

---

#### Trasformazioni testo

| Tag | Sintassi | Descrizione |
|-----|----------|-------------|
| `<uppercase>` | `<uppercase>...</uppercase>` | Converte il contenuto in MAIUSCOLO |
| `<lowercase>` | `<lowercase>...</lowercase>` | Converte il contenuto in minuscolo |
| `<formal>` | `<formal>...</formal>` | Prima Lettera Di Ogni Parola Maiuscola *(da v1.2.0)* |
| `<sentence>` | `<sentence>...</sentence>` | Prima lettera della frase maiuscola *(da v1.2.0)* |
| `<explode>` | `<explode>...</explode>` | I n s e r i s c e   s p a z i   t r a   o g n i   c a r a t t e r e *(novità v1.2.0)* |

---

#### Tag di sistema *(tutti da v1.1)*

| Tag | Sintassi | Descrizione |
|-----|----------|-------------|
| `<date>` | `<date/>` oppure `<date format="%d/%m/%Y"/>` | Data/ora locale. Il formato segue `strftime`; se omesso usa il bot-predicato `dateformat` |
| `<size>` | `<size/>` | Numero di categorie AIML attualmente caricate |
| `<version>` | `<version/>` | Versione del parser (bot-predicato `version`, default `1.3.0`) |
| `<id>` | `<id/>` | Identificatore UUID della sessione corrente (o bot-predicato `id`) |

---

#### Punteggiatura e spazio *(da v1.1)*

| Tag | Sintassi | Output |
|-----|----------|--------|
| `<br>` | `<br/>` | Interruzione di riga `\n` |
| `<p>` | `<p/>` | Paragrafo `\n\n` |

---

#### Attributi speciali su `<template>`

| Attributo | Esempio | Descrizione |
|-----------|---------|-------------|
| `avatar` | `<template avatar="sorridente">` | Passa il nome dell'espressione avatar nel dict di ritorno di `rispondi()` |
| `comando` | `<template comando="apri_menu">` | Passa un comando arbitrario al programma principale nel dict di ritorno |
| `menu` | `<template menu="1111">` | Apre o chiude i 4 menu laterali (COMANDI, MEMORIA, SHORTCUT, LINGUA)

Il dict restituito da `rispondi()` ha sempre la struttura:
```python
{
    "testo":   "...",   # testo della risposta
    "avatar":  "...",   # valore di avatar= (o None)
    "comando": "...",   # valore di comando= (o None)
    "menu":    "...",   # valore di menu= (o None)
}
```

---

#### Tag di esecuzione silenziosa *(da v1.1)*

| Tag | Sintassi | Descrizione |
|-----|----------|-------------|
| `<think>` | `<think>...</think>` | Esegue il contenuto senza emettere alcun testo nella risposta. Tipicamente usato per racchiudere `<set>` e `<condition>` che devono aggiornare lo stato interno senza produrre output visibile. |

**Esempio:**
```xml
<template avatar="coniglio2">
    Quale coniglio?
    <think><set name="step">2</set></think>
</template>
```

---

#### Fix v1.1.0 — Avatar propagato via `<srai>`

In precedenza, se una categoria veniva raggiunta tramite una catena di `<srai>`, l'attributo `avatar=` (e `comando=`) del template finale era perso. 
Ora viene propagato correttamente fino alla risposta restituita da `rispondi()`.

Fix su testConiglio.aiml:

```xml
<category>
    <pattern>* CONIGLIO *</pattern>
    <template><srai>CONIGLIO.GESTORE</srai></template>
</category>
<category>
    <pattern>CONIGLIO.GESTORE</pattern>
    <template><srai>CONIGLIO.STEP.1</srai></template>
</category>
<category>
    <pattern>CONIGLIO.STEP.1</pattern>
    <template avatar="coniglio2">Quale coniglio?</template>
</category>
```
---

### API Python

| Metodo | Descrizione |
|--------|-------------|
| `set_predicato(nome, valore)` | Imposta un predicato utente |
| `get_predicato(nome)` | Legge un predicato utente |
| `set_bot_predicato(nome, valore)` | Imposta un predicato bot *(novità v1.2.0)* |
| `get_bot_predicato(nome)` | Legge un predicato bot *(novità v1.2.0)* |
| `set_topic(topic)` | Imposta il topic corrente |
| `carica_file(path)` | Carica un file `.aiml` |
| `carica_cartella(cartella)` | Carica tutti i `.aiml` in una cartella |
| `scarica_tutto()` | Rimuove tutte le categorie e azzera lo stato |
| `rispondi(testo_utente)` | Elabora l'input e restituisce il dict risposta |
| `info()` | Stringa di diagnostica sullo stato corrente |
| `dump_categorie(n)` | Stampa le prime `n` categorie caricate |

---

### Note di compatibilità

Il parser implementa un sottoinsieme di **AIML 1.x**. I tag non riconosciuti vengono
attraversati ricorsivamente senza errore, quindi file AIML che usano tag non supportati
rimangono caricabili: il tag sconosciuto viene ignorato e il contenuto testuale comunque valutato.
