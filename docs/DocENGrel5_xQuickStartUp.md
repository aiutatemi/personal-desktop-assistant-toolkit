# **🚀 Quick Start Up Guide release 4.x**

### 👉 1. **Download the ZIP file.**  
### 👉 2. **Unzip the `./myAssistente` folder** anywhere you prefer (USB drives are supported too).

---

## 📁 **Program structure**
```
assistente.exe
_internal
_dati/
  config.json   ← all settings
  memory.json   ← your saved data
  lang_it.json  ← Italian language file
  lang_en.json  ← English language file
  aiml/IT       ← insert here Italian AIML standard language file
       EN       ← insert here English AIML standard language file
  asset/        ← your saved images (initially empty)
    avatar/     ← avatar images/video
```

---

### 👉 3. **Check if your language file is available.**  
Default languages included: **English (ENG)** and **Italian (ITA)**.  
15 additional languages are available. If needed, download yours from here:  
🔗 **Open localization folder**  
([https://gitlab.com/EmanueleCAS/assistente/-/tree/master/localization-file](https://gitlab.com/EmanueleCAS/assistente/-/tree/master/localization-file))

---

### 👉 4. **Place your language file inside the `_dati/` folder.**

#### Example:
```
assistente.exe
_internal
_dati/
  config.json
  memory.json   ← your information; includes example data to get you started
  lang_sp.json  ← your new language file (example for Spanish)
  lang_it.json  ← optional, delete if not needed
  lang_en.json  ← optional, use as reference to translate in your language
      aiml/IT/  ← optional, delete if you do not use it
      aiml/EN/  ← optional, delete if you do not use it
  asset/
    avatar/
```

---

### 👉 5. **Run `myAssistente.exe`.**  
At startup, select your language from the **bottom‑right corner** of the panel.

---

## 🎛️ 6. **Customize the assistant**
You can personalize actions such as:
- launching your own programs  
- opening your files  
- opening web pages  
- saving any information you want the assistant to remember  

You can do this:
- directly from the program (commands **remember** or **learn**)  
- or by editing **memory.json**

- create or use existing AIML files for advanced conversation 

---

## 🔒 **Privacy note**
All your personal information stays on your **LOCAL PC**.  
Exceptions:
- 🎤 optional voice recognition uses Google Speech API, but **only** when you press the microphone button (disabled by default)  
- 🤖 AI integration, if you manually enable it (disabled by default)

---

## 📚 **Documentation (ENG/ITA)**
👉 **Open documentation folder**  
(`https://gitlab.com/EmanueleCAS/assistente/-/tree/master/docs` [(gitlab.com in Bing)](https://www.bing.com/search?q="https%3A%2F%2Fgitlab.com%2FEmanueleCAS%2Fassistente%2F-%2Ftree%2Fmaster%2Fdocs"))

Suggested manuals:
- **User Manual** 
- **AI config.md** (for AI integration)

---

## 🛠️ **What you can customize**
- **lang_XX.json:** command names, assistant replies  
- **config.json:**  
  - assistant and user name  
  - assistant avatar (`_dati/asset/avatar/`)  
  - assistant responses  
  - assistant final video (`_dati/asset/avatar/`)  
  - microphone/voice settings  
  - AI integration  
  - alias commands (optional)  
  - assistant FX responses (optional)  
  - **Shortcuts** → buttons at the bottom‑right of the assistant (above Language)
- **aiml_XX.json:** AIML conversation  

---

## 💙 7. **Optional but appreciated**
If you want to support the project:  
👉 [https://www.paypal.com/pool/9nyLoeBeq8?sr=wccr](https://www.paypal.com/pool/9nyLoeBeq8?sr=wccr)

---

**Emanuele Cassani**  
[https://www.steppa.net/cassani/business_card.htm](https://www.steppa.net/cassani/business_card.htm)

---