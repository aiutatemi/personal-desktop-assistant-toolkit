Release 2.1 — Voice Features & Multilingual Support
Version 2.1 introduces major upgrades that transform the Personal Assistant into a fully voice‑enabled and multilingual desktop application. This release adds both speech recognition (STT) and text‑to‑speech (TTS) capabilities, along with a complete internationalization system and several UI improvements.

✨ New Features
Speech‑to‑Text (STT)
Voice input using Google Speech Recognition

Automatic silence detection

Runs in a separate thread to keep the UI responsive

Microphone button added to the interface

Text‑to‑Speech (TTS) (Windows only)
Voice output using Windows SAPI

Offline, fast, and integrated into the UI

Speech can be interrupted instantly by clicking mute or typing “OK”

Automatic selection of a system voice matching the active language

Multilingual Support (i18n)
All UI strings moved to external lang_XX.json files

Italian and English included by default

Easy to add new languages without modifying the code

Automatic fallback if a language file is missing

🖥️ UI Improvements
Language Selector
New LANGUAGE section in the side panel

One button per available language file

Active language highlighted

Switching language updates the UI instantly

Runtime Language Switching
Change language via UI or command:

language en

language it

STT and TTS adapt automatically to the selected language

🔧 Other Enhancements
Updated configuration file with new "language" field

Improved startup detection of available language packs

Better handling of missing or invalid language files

General UI refinements and stability improvements

📦 Summary
Release 2.1 adds:

Voice input (STT)

Voice output (TTS)

Full multilingual support

New language selector UI

Improved configuration and fallback system

This update significantly enhances accessibility, usability, and international reach.