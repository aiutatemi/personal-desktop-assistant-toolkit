#Il *test* nel aiml_parser.py

Il blocco `if __name__ == "__main__":` in fondo al file — è un **test autonomo** 
si esegue solo quando lanci il parser direttamente dalla riga di comando, 
*mai quando importato da myAssistente*.

##**Come si usa:**

```bash
python aiml_parser.py
```

Questo comando fa partire il test senza aprire l'interfaccia grafica, 
senza TTS, senza memoria — solo il motore AIML puro.

Utile per:

- **Sviluppare nuove regole** `.aiml` e verificare se matchano
- **Debuggare** perché vedi esattamente che cosa restituisce ogni categoria (testo, avatar, comando, menu)
- **Testare regressioni** dopo aver modificato il parser

---

##**Esempio pratico** 

se scrivi un nuovo file `.aiml` e vuoi testarlo senza aprire myAssistente, 
aggiungi in fondo al test:

```python
p2 = AIMLParser()
p2.carica_file("_dati/aiml/it/mie_regole.aiml")
r = p2.rispondi("apri la posta")
print(r)
# → {'testo': 'Apro la posta!', 'avatar': 'positivo', 'comando': 'apri posta', 'menu': '0010'}
```

---

**Da myAssistente non si vede** perché Python importa il file come modulo (`from aiml_parser import AIMLParser`) 
e il blocco `if __name__ == "__main__"` è saltato completamente — come da una convenzione standard di Python 
per separare "codice riutilizzabile" da "codice di test/avvio".

