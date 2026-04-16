# 🌍 Aggiungere una Nuova Lingua

Questa guida spiega come aggiungere il supporto per una nuova lingua all'assistente.
Il flusso di lavoro è semplice, modulare e progettato per mantenere coerenti tutti i file di localizzazione.
Valido per tutte le versioni di myAssistant.

---

### 0. Verifica se la lingua esiste già
Prima di creare qualcosa di nuovo, verifica se il file della lingua è già disponibile nella [cartella dei file di localizzazione](https://gitlab.com/EmanueleCAS/assistente/-/tree/master/localization-file).

Se esiste, puoi comunque contribuire: scaricalo, miglioralo e invia la tua versione aggiornata.

### 1. Crea il nuovo file della lingua
Copia il modello italiano:

```
_dati/lang_it.json → _dati/lang_XX.json
```
Sostituisci XX con il codice della lingua corretto (es. en, de, es, pt).

### 2. Traduci solo i valori
Traduci ogni valore nel file JSON, ma **non tradurre mai le chiavi**.
Questo garantisce la compatibilità con la logica interna dell'assistente.

### 3. Controlla la corretta "lingua_stt"
Imposta il codice Google Speech‑to‑Text corretto in "lingua_stt" (obbligatorio per il corretto riconoscimento vocale).

Configura gli alias dei comandi in linguaggio naturale in "alias_comandi" per fare in modo che l'assistente comprenda meglio i comandi nella nuova lingua.

### 4. Riavvia l'assistente
Dopo il riavvio, la nuova lingua apparirà automaticamente in fondo al pannello laterale destro.

---

## Esempio: ./_dati/config.json
```json
{
  "nome_avatar": "Assistant", 		<- nome dell'assistente
  "nome_utente": "utente", 		<- nome utente
  "avatar_iniziale": "benvenuto",	<- immagine .jpg usata all'avvio
  "avatar_random": [
    "sorridente",
    "coniglio",
    "soddisfatto"
  ],
  "avatar_finale": "ciao.mp4",		<- video .mp4 usato alla fine
  "frase_finale": "Ciao!",		<- frase finale
  "lingua": "it",  			<- Lingua all'avvio
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
    "lingua": "it-IT"   		<- Codice Google Speech per la tua lingua
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
  "shortcut": [   			<- Modifica i comandi che appaiono sotto SHORCUT
    {
      "etichetta": "Silenzio per favore",	<- Comando utile, tradotto nella tua lingua
      "comando": "ok"
    },
    {
      "etichetta": "Gestione attività",	<- Funziona solo su Windows
      "comando": "apri task"
    },
    {
      "etichetta": "Pannello di controllo",	<- Funziona solo su Windows
      "comando": "apri pannello"
    },
    {
      "etichetta": "Configura",		<- Funziona solo su Windows
      "comando": "configura"
    }
  ]
}
```

---