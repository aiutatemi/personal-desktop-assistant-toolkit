# 📦 Building Distributable Packages

How to create distributable packages 
for Windows, Linux and macOS
from the *source Python file*

## Pre requisite

Download all necessary files from the repository
[Open project folder](https://gitlab.com/EmanueleCAS/assistente/)

- myAssistenteX_X.py
- aiml_parser.py
- complete _dati folder

Optional

- lang_EN.json and lang_IT.json are included inside _dati folder,
if additional languages are needed, downlod them from the localization-file folder
and insert it inside the _dati folder
- some AIML files are included inside _dati folder, 
add any AIML compatible file under your language folder i.e _dati/aiml/EN/
- documentation from project doc folder (User Manual and/or QuickStartUp)

## 🪟 Windows Distributable

### Create the executable from the command line  
(Recommended: use Thonny → Tools → Open system shell, then navigate to the correct directory)

Example path:
```bash
D:\ProgettiPython\progetto-assistente\sorgente
```

*** PyInstaller command
```bash
pyinstaller --onedir --noconsole --clean ^
  --icon=iconWIN.ico ^
  --collect-all PIL ^
  --collect-all cv2 ^
  --name myAssistente myAssistente.py
```
👉 This will overwrite the /dist folder if it was previously created from Linux.
Windows icons must be in .ico format.

---

## 🐧 Linux / 🍎 macOS Distributable
Create the executable from the command line
(Recommended: use Thonny → Tools → Open system shell.
To reach the correct directory: type cd and drag the project folder into the terminal.)

PyInstaller command
```bash
pyinstaller --onedir --noconsole --clean \
  --icon=iconLINUX.png \
  --collect-all PIL \
  --collect-all cv2 \
  --collect-all sounddevice \
  --collect-all speech_recognition \
  --hidden-import numpy \
  --name myAssistente myAssistente.py
```
👉 This will overwrite the /dist folder if it was previously created from Windows.
Linux/macOS icons must be in .png format.

---

## 📁 Program Folder Structure (for ZIP distribution)
When packaging the program insert the file downloaded from repository:
- complete -dati folder
Optional
- additional lang_XX.json
- documentation
for distribution, the structure inside the ZIP file should be:

```
dist/Assistente/
       assistente.exe
       QuickSetUp.txt or UserManual.pdf  ← optinal
       _dati/                 ← compete data folder
            config.json
            memory.json
            lang_it.json
            lang_en.json
            lang_xx.json      ← optional additional language
            aiml_IT.json      ← optional advanced phrases
            aiml_EN.json      ← optional advanced phrases
            asset/avatar/      ← avatar JPG and MP4 files already included in _dati folder
       _internal/              ← PyInstaller internal folder (do not modify)
                [other PyInstaller DLLs]
```
👉 Important
Always distribute the entire package as a single ZIP archive.
Distribute and do not modify the _internal directory created by PyInstaller.
Optional: insert your own documentation

---

## ✅ Summary
Use .ico icons for Windows, .png for Linux/macOS.
PyInstaller will always overwrite the /dist folder when building from different OS.
Distribute the entire dist/myAssistente/ folder as a ZIP file.
The _dati folder must always be included (config, memory, languages, avatars, aiml).
The _internal folder must always be included (PyInstaller mandatory files).
---