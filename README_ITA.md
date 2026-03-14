# Assistente Personale — Guida rapida (v2.1)

## Requisiti

Python 3.9+  
pip install pillow imageio imageio-ffmpeg   (opzionale, per immagini/video)  

Per la versione VOICE (TTS/STT):  
pip install SpeechRecognition sounddevice numpy opencv-python Pillow pywin32  

**Compatibilità TTS: solo Windows**  
Il motore vocale usa le API SAPI di Windows (win32com).  
Lo STT è invece cross‑platform.

---

## Struttura cartelle

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

## Configurazione ( _dati/configurazione.json )

{  
"nome_avatar": "Assistente",  
"nome_utente": "Emanuele",  
"avatar_iniziale": "benvenuto",  
"avatar_random": ["sorridente", "soddisfatto"],  
"avatar_finale": "ciao.mp4",  
"lingua": "it"  
}

• Cambia nome_utente con il tuo nome  
• Aggiungi quante immagini vuoi in avatar_random  
• I nomi devono corrispondere ai file in _dati/asset/avatar/  
• La chiave lingua definisce la lingua attiva (v2.1+)

---

# Novità dalla release 2.0 — VOICE

## Funzionalità vocali

### STT — Speech To Text
• Basato su SpeechRecognition + sounddevice  
• Usa Google Speech API (gratuita, richiede internet)  
• Registrazione automatica con stop al silenzio  
• Thread separato per non bloccare la UI  

### TTS — Text To Speech (solo Windows)
• Basato su Windows SAPI (win32com)  
• Funziona offline  
• Ogni risposta può essere letta ad alta voce  
• Interrompibile cliccando 🔇 o dicendo/scrivendo “OK”  

### Interfaccia VOICE
• 🎤 per parlare (rosso mentre ascolta)  
• 🔊 / 🔇 per attivare o silenziare la voce  
• Se le librerie non sono installate, i pulsanti appaiono disabilitati  

---

# Novità dalla release 2.1 — Sistema di localizzazione (i18n)

## File lingua separati

Tutte le stringhe della UI sono ora in file dedicati:

_dati/lang_it.json  
_dati/lang_en.json  

Per aggiungere una lingua: copia lang_it.json, traduci e salva come lang_XX.json.

## Cambio lingua da comando

lingua en  
lingua it  

Il cambio è immediato e salvato nel file di configurazione.

## Lingua STT automatica

Il riconoscimento vocale usa automaticamente il locale definito nel file lingua (es. it-IT, en-US).

## Voce TTS adattiva (Windows)

Il programma tenta di usare una voce di sistema nella lingua selezionata; se non disponibile, usa quella predefinita.

## Fallback a cascata

1. _dati/lang_XX.json  
2. Cartella dell’eseguibile  
3. Italiano integrato nel codice  

---

# Novità dalla release 2.2 — Selettore lingua nella UI

## Selettore grafico nel pannello comandi

In fondo al pannello laterale compare una sezione LINGUA con un pulsante per ogni file lang_XX.json trovato.

• Lingua attiva: ● con sfondo evidenziato  
• Altre lingue: ○  

Rilevamento automatico a ogni avvio.

## Mappatura etichette lingue

it — Italiano  
en — English  
de — Deutsch  
es — Español  
pt — Português  
fr — Français  

Per codici non riconosciuti viene mostrato il codice in maiuscolo (es. JA).

---

# Comandi principali

### ricorda
Salva informazioni in memoria.  
Esempi:  
ricorda i dati della mia TV  
ricorda il cf di Roberta  
ricorda il link per l'estratto conto  
ricorda questa immagine  

### dammi
Restituisce informazioni salvate.  
dammi i dati della mia TV  
dammi il cf di Roberta  

### apri
Apre file, cartelle o URL salvati.  
apri estratto conto  

### cerca
Ricerca parziale su tutti i campi.  
cerca TV  
cerca Roberta  

### elenca
Mostra tutte le voci salvate.

### modifica
Aggiorna un campo di una voce.

### elimina
Rimuove una voce (con conferma).

### copia
Copia un dato negli appunti.  
copia cf Roberta  

### aiuto
Mostra la lista dei comandi.

---

# Note tecniche

• Senza Pillow: avatar come riquadro colorato  
• Con Pillow: immagini reali  
• Con imageio: supporto video .mp4  
• memoria.json è modificabile a mano  
• Integrazione API AI predisposta (vedi # TODO: API_INTEGRATION)

---

# Installazione dipendenze opzionali

pip install pillow  
pip install imageio imageio-ffmpeg  
pip install SpeechRecognition sounddevice numpy opencv-python Pillow pywin32  

---

**Emanuele Cassani**  
[https://www.steppa.net/cassani/business_card.htm](https://www.steppa.net/cassani/business_card.htm)