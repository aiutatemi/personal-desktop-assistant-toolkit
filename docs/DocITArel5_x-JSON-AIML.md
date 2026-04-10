# 📦 Connettere memory.json e file AIML

Come usare dati interni memory.json per fare intervenire un file AIML specifico.

---

## FLUSSO

utente:  "dammi visita"
         ↓
Python:  trova entry con dati="visita.aiml"
         → carica il file se non già caricato
         → self._aiml.set_topic("VISITA")
         → self._aiml_topic_dialogo = "VISITA"   ← segnaposto per sapere che siamo in dialogo
         → self.stato = "dialogo_aiml"
         → manda trigger "AVVIA VISITA" al parser
         ↓
AIML:    risponde "Che tipo di visita?"
         ↓
utente:  "medica"
         ↓
Python:  in stato "dialogo_aiml" → passa tutto all'AIML senza interpretare
         ↓
AIML:    that="CHE TIPO DI VISITA" → risponde "Per quale data?"
         ↓
utente:  "15 giugno"
         ↓
AIML:    that="PER QUALE DATA" → risponde "Perfetto! ..."
         → <set name="topic">*</set>   ← segnale di fine dialogo
         ↓
Python:  dopo ogni risposta controlla self._aiml.get_predicato("topic")
         se topic == "" o "*" → self.stato = "idle"
                                self._aiml_topic_dialogo = None

---

## file memory 
```json
{
  "nome": "visita",
  "alias": "prenotazione",
  "soggetto": "",
  "dati": "visita.aiml",
  "tag": ["visita", "medica", "agenda"],
  "avatar": "segretaria"
}
```

---

## file AIML
```aiml
<aiml>
  <topic name="VISITA">

    <category>
      <pattern>AVVIA VISITA</pattern>
      <template>Che tipo di visita? (medica / specialistica / controllo)</template>
    </category>

    <category>
      <pattern>*</pattern>
      <that>CHE TIPO DI VISITA *</that>
      <template>
        <set name="tipo_visita"><star/></set>Per quale data?
      </template>
    </category>

    <category>
      <pattern>*</pattern>
      <that>PER QUALE DATA</that>
      <template>
        Perfetto! Visita <get name="tipo_visita"/> per il <star/>. Confermato.
        <set name="topic">*</set>
      </template>
    </category>

    <category>
      <pattern>*</pattern>
      <template>Non ho capito, riprova.</template>
    </category>

  </topic>
</aiml>
```

---

