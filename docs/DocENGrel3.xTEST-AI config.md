# AI Integration Guide

This document explains how to configure AI integration in the Personal Desktop Assistant Toolkit.  
Two main providers are supported: **OpenAI (GPT)** and **Google Gemini**.

---

## 1. Basic Configuration in `config.json`

Add or edit the following section inside your `config.json`:

```json
"ai_config": {
    "enabled": false,
    "provider": "openai",
    "api_key": "",
    "model": "gpt-3.5-turbo",
    "temperature": 0.5,
    "max_tokens": 500,
    "fallback_to_ai": true
}
```

### Parameter Description

- **enabled**  
  `true` to activate AI, `false` to disable it.

- **provider**  
  `"openai"` or `"gemini"`.

- **api_key**  
  Your API key for the selected provider.

- **model**  
  - OpenAI: `"gpt-3.5-turbo"`, `"gpt-4"`, etc.  
  - Gemini: `"gemini-pro"`.

- **temperature**  
  Creativity level (0.0 = precise, 1.0 = creative).

- **max_tokens**  
  Maximum length of the AI response.

- **fallback_to_ai**  
  If `true`, the assistant uses AI when it cannot understand a command.

---

## 2. Installing IA Dependencies

### OpenAI
```bash
pip install openai
```

### Google Gemini
```bash
pip install google-generativeai
```

---

## 3. Getting API Keys

### OpenAI API Key
1. Visit https://platform.openai.com  
2. Log in or create an account  
3. Go to **API Keys** → **Create new secret key**  
4. Copy the key (starts with `sk-...`)

### Google Gemini API Key
1. Visit https://makersuite.google.com/app/apikey  
2. Log in with your Google account  
3. Click **Create API Key**  
4. Copy the key

---

## 4. Full Configuration Examples

### Example 1 — OpenAI GPT‑3.5
```json
"ai_config": {
    "enabled": true,
    "provider": "openai",
    "api_key": "sk-1234567890abcdefghijklmnopqrstuvwxyz",
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 500,
    "fallback_to_ai": true
}
```

### Example 2 — OpenAI GPT‑4
```json
"ai_config": {
    "enabled": true,
    "provider": "openai",
    "api_key": "sk-1234567890abcdefghijklmnopqrstuvwxyz",
    "model": "gpt-4",
    "temperature": 0.5,
    "max_tokens": 800,
    "fallback_to_ai": true
}
```

### Example 3 — Google Gemini
```json
"ai_config": {
    "enabled": true,
    "provider": "gemini",
    "api_key": "AIzaSyB1234567890abcdefghijklmnopqrstuvwxyz",
    "model": "gemini-pro",
    "temperature": 0.7,
    "max_tokens": 500,
    "fallback_to_ai": true
}
```

---

## 5. How AI Works in the Program

Once AI is enabled:

1. **Local commands** (open, remember, search, etc.) always have priority.  
2. If a command is not recognized **and** `fallback_to_ai = true`, the assistant sends the question to the AI provider.  
3. The AI responds to general questions.

### Examples

```
User: Who was Leonardo da Vinci?
Assistant: [contacts OpenAI/Gemini]
           Leonardo da Vinci was an Italian Renaissance polymath...
```

```
User: open chrome
Assistant: [local command] Opening chrome.exe
```

```
User: give me email password
Assistant: [searches memory] password123
```

---

## 6. Quick Test

To verify that AI integration works:

1. Start the assistant  
2. Ask a general question such as:  
   **"What is the capital of Italy?"**  
3. The assistant should display “Thinking…” and then provide the answer.

---

## 7. Troubleshooting

### Error: “Communication error with AI”
- Check your API key  
- Verify your internet connection  
- Ensure the correct library is installed  

### Error: “AI function not available”
- Make sure `"enabled": true` in `config.json`  
- Verify dependencies are installed  

### AI responds in the wrong language
- The assistant uses the language set in `config.json`  
- You can force the language in the system prompt  

---

## 8. Advanced Customization

To modify AI behavior, edit the `_chiedi_ai_thread()` function and adjust the system prompt:

```python
messages=[
    {"role": "system", "content": f"You are {self.cfg['nome_avatar']}, a personal assistant. Respond concisely and helpfully."},
    {"role": "user", "content": question}
]
```

### Example customization

```python
messages=[
    {"role": "system", "content": f"You are {self.cfg['nome_avatar']}, a friendly personal assistant. Always reply in {self.cfg['lingua']} using no more than 3 sentences."},
    {"role": "user", "content": question}
]
```

---

## 9. Costs

- **OpenAI GPT‑3.5**: ~$0.002 per 1000 tokens (cheap)  
- **OpenAI GPT‑4**: ~$0.03 per 1000 tokens (more expensive)  
- **Google Gemini**: Free (currently, with usage limits)

**Recommendation:** Start with a free AI for testing.

---