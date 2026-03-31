# Come modificare i comandi di myAssistente

Prerequisiti: il file myAssistente.py
Applicabile: tutte le release

---

## Come aggiungere un comando nuovo (es. `"traduci"`)

Servono **4 interventi** nel codice Python:

**1.** Aggiungerlo a `COMANDI`:
```python
COMANDI = [..., "traduci"]
```

**2.** Scrivere la funzione che lo esegue:
```python
def _cmd_traduci(self, parsed: dict):
    ...
```

**3.** Registrarla nel dizionario `dispatch`:
```python
dispatch = {
    ...
    "traduci": self._cmd_traduci,
}
```

**4.** Aggiungere gli alias nei file lingua (`lang_it.json`, `lang_en.json`):
```json
"alias_comandi": {
    "traduci": ["translate", "traduzione"]
}
```

---

## Rinominare un comando esistente (es. `"dammi"` → `"trova"`)

**Attenzione**: i nomi interni come `"dammi"` sono usati ovunque nel codice — 
nella funzione `_cmd_dammi`, nel `dispatch`, nei messaggi di errore 
(`"dammi_cosa"`, `"dammi_non_trovato"` ecc.). 
Rinominarlo in `COMANDI` senza cambiare tutto il resto rompe silenziosamente l'esecuzione.

Una strada semplificata — e che non richiede toccare tutto il codice — 
**lasciare i nomi interni com'erano** (`"dammi"`, `"ricorda"`, ecc.) 
e gestire la rinomina esclusivamente tramite gli alias nei file lingua. 
Il nome in `COMANDI` rimane il nome tecnico, invisibile all'utente.

---

## Che cosa è possibile modificare

| Cosa | Dove | Rischio |
|---|---|---|
| Aggiungere alias a comandi esistenti | `lang_it.json` / `lang_en.json` | Nessuno |
| Cambiare etichette pulsanti (`panel_XXX`) | file lingua | Nessuno |
| Aggiungere un comando nuovo completo | `.py` (4 punti) + file lingua | Basso se segui tutti e 4 i passi |
| Rinominare un comando interno | `.py` (molti punti) | Alto — meglio usare gli alias |