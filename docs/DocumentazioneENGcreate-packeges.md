* 📦 Building Distributable Packages

** 🪟 Windows Distributable

*** Create the executable from the command line  
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
  --name assistente assistente3.0TEST.py
```
Notes
This will overwrite the /dist folder if it was previously created on Linux.

Windows icons must be in .ico format.

** 🐧 Linux / 🍎 macOS Distributable
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
  --name assistente assistente3.0TEST.py
```
Notes
This will overwrite the /dist folder if it was previously created on Windows.

Linux/macOS icons must be in .png format.

** 📁 Program Folder Structure (for ZIP distribution)
When packaging the program for distribution, the structure inside the ZIP file should be:

```
dist/Assistente/
       assistente.exe
       _dati/                 ← data folder
            config.json
            memory.json
            lang_it.json
            lang_en.json
            lang_xx.json
            asset/avatar/      ← avatar JPG and MP4 files
       _internal/              ← PyInstaller internal folder (do not modify)
            [other PyInstaller DLLs]
```
Important
Always distribute the entire folder as a single ZIP archive.

Do not modify the _internal directory created by PyInstaller.

** ✅ Summary
Use .ico icons for Windows, .png for Linux/macOS.

PyInstaller will always overwrite the /dist folder when rebuilding.

Distribute the entire dist/Assistente/ folder as a ZIP file.

The _dati folder must always be included (config, memory, languages, avatars).
The _internal folder must always be included (PyInstaller mandatory files).