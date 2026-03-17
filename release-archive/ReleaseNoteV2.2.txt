## v2.2 — Bug fix: STT and avatar rendering for Linux

### Problem
When running the PyInstaller compiled binary on Linux, the avatar area
displayed an unusable colored screen instead of images or videos.
STT default parameters adapted for Linux users.

### Root cause
`_mostra_immagine` only caught `ImportError`, which handles the case
where Pillow is not installed at all. On Linux PyInstaller bundles,
Pillow is included but may fail to initialize due to unresolved native
dependencies (`libjpeg`, `libpng`, etc.) or incorrect internal bundle
paths. These failures raise a generic `Exception`, which was not caught,
leaving the avatar widget in a broken state with no fallback.

### Fix
- **`_mostra_immagine`**: broadened `except ImportError` to
  `except Exception` — any Pillow failure now correctly falls back to
  the colored placeholder
- **`_riproduci_video`**: added explicit `cap.isOpened()` check
  immediately after `cv2.VideoCapture()`, and improved the error log to
  include the filename for easier debugging

### Behavior after fix
| Condition | Result |
|---|---|
| Pillow / cv2 working | images and video play normally |
| Pillow / cv2 unavailable or broken | colored placeholder shown, all other features unaffected |

### Windows build
No functional changes. Windows behavior as previous versions.
```bash
pyinstaller --onedir --noconsole --clean ^
  --icon=iconWIN.ico ^
  --collect-all PIL ^
  --collect-all cv2 ^
  --name AssistenteVOICE assistenteVOICE2.2.py
```

### Recommended PyInstaller flags for Linux
```bash
pyinstaller --onedir --noconsole --clean \
  --icon=iconLINUX.png \
  --collect-all PIL \
  --collect-all cv2 \
  --collect-all sounddevice \
  --collect-all speech_recognition \
  --hidden-import numpy \
  --name AssistenteVOICE assistenteVOICE2.2.py
```
`--collect-all PIL` ensures all Pillow image format plugins are bundled,
which PyInstaller often omits by default.