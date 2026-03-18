# Fix - TTS pyttsx3 compatible Windows
one thread, one queue, one direct stop handle

- Bug releases 3.0, 3.1
Fix implemented from Release 3.2 

---

## **The problem: pyttsx3 on Windows is not thread-safe**

Every time the assistant needed to speak, the code created a new background thread and called `engine.runAndWait()`. On Windows, pyttsx3 uses Microsoft's SAPI5 voice engine under the hood, which runs a COM "event loop". Once that loop is running in one thread, any other thread trying to start it crashes with `run loop already started`. After that crash, the engine was broken for the rest of the session.

---

## **The fix: one dedicated worker thread with a queue**

Instead of creating a new thread for every message, we now have one single worker thread that stays alive for the whole session. When the assistant wants to speak, it just drops the text into a queue. The worker picks messages up one at a time, creates a fresh engine instance, speaks, then clears the pyttsx3 singleton so the next message can create a clean engine again.

---

## **The interrupt problem**

When the user typed a new command while the assistant was speaking, the old code tried to set a flag and hoped the worker would notice. But the worker was stuck inside `runAndWait()` and couldn't check any flags. The fix was to keep a live reference to the engine currently speaking (`_tts_engine_live`), so that `_ferma_tts()` can call `engine.stop()` directly on it from outside — exactly like pulling the plug — regardless of what the worker thread is doing.

---