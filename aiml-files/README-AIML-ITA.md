# File AIML aggiuntivi in italiano

Puoi usare qualsiasi file AIML standard in italiano

Inseriscili nella directory _dati/aiml/EN/_.  
Quando viene selezionata la lingua itliana, l’assistente utilizzerà automaticamente questi file.

---

## Note

Gli attributi all’interno del tag `template` sono estensioni proprietarie di **myAssistente**.  
Aggiungile ai file standard per specificare:
- quale avatar dell’assistente deve essere visualizzato
- quale comando far eseruire a myAssistente
- quale pannello laterale aprire (1)/chiudere (0)
Quando l'attributo avatar manca, sarà scelto casualmente uno degli avatar definiti nel file `config.json`.

Gli altri parser AIML ignoreranno semplicemente questo attributo.

---

### Esempio

       <template avatar="positivo" comando="apri posta"  menu="0010">
---