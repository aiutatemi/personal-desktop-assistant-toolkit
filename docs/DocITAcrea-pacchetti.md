# 📦 Creare pacchetti distribuibili

## 🪟 Distribuibile Windows

### Creare il pacchetto con exe dalla linea comando (consigliato usare Thonny)
strumenti-> apri shell di sistema e naviga nella directory corretta

*** Comandi PyInstaller
```bash
D: ^
--cd ProgettiPython\\progetto-assistente\\sorgente

pyinstaller --onedir --noconsole --clean ^
--icon=iconWIN.ico ^
--collect-all PIL ^
--collect-all cv2 ^
--name myAssistente myAssistente4_1.py
```
👉 sovrascrive cartella /dist se precedentemente compilato con linux
per Windows, l'icona deve essere in formato .ico

---

## Distribuibile 🐧 Linux / 🍎 macOS
Creare il pacchetto con eseguibile dalla linea comando (consigliato usare Thonny)

per directory corretta: scrivere :>CD e trascinare la cartella del progetto

```bash
pyinstaller --onedir --noconsole --clean  
--icon=iconLINUX.png  
--collect-all PIL  
--collect-all cv2  
--collect-all sounddevice  
--collect-all speech\_recognition  
--hidden-import numpy  
--name myAssistente myAssistente4_1.py
```

👉 sovrascrive cartella /dist  se precedentemente compilato con Windows
per linux, l'icona deve essere in formato .png

---

## 📁 Struttura cartelle del programma da distribuire in archivio ZIP unico

```
dist/Assistente/
assistente.exe
_dati/		← la cartella dati
config.json
memory.json
lang_it.json
lang_en.json
lang_xx.json 	← altre lingue opzionali
aiml_IT.json 	← linguaggio opzionale italiano avanzato
aiml_EN.json 	← linguaggio opzionale inglese avanzato
asset/avatar/ 	← avatar jpg and mp4
_internal/	← cartella di PyInstaller, non modificare
[altre DLL PyInstaller]
```
👉 Importante
Distribuire tutto il contenuto della cartella in un singolo archivio ZIP.
Distribuire e non modificare la cartella _internal creata da PyInstaller.

---

## ✅ Riepilogo

Usare icone .ico icons per Windows, .png per Linux/macOS.
PyInstaller sovrascrive sempre la cartella /dist nel build
Distribuire il contenuto della cartella dist/Assistente/ come file ZIP.
La cartella \_dati deve essere distribuita. Contiene file JSON: config, memory, lang, immagini avatar.
La cartella \_internal/	deve essere distribuita. Contiene file di PyInstaller.
---

