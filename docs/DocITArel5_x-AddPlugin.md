# * Plugin a myAssistente*

I plugin disponibili dalla release 5.31 sono: myAgenda, myNote e myTodo, mini APP HTML con javascript.

## Come aggiungerne altri

Il sistema è modulare: ogni plugin richiede esattamente 4 interventi nel file, tutti localizzati.

---

**1. Costante del file** — nessuna modifica necessaria, basta creare il file nella cartella già monitorata `_dati/plugins/`. myAssistente la scannerizza automaticamente all'avvio e su comando `aggiorna`.

**2. Metodo `_salva_NomePlugin_plugin()`** — aggiungilo nella sezione *PLUGIN* della classe, vicino agli altri metodi `_salva_*`. Deve costruire il dizionario con i campi standard (`nome`, `dati`, `soggetto`, `tag`, `_plugin`, ecc.), aprire `PLUGINS_DIR / "myNomePlugin.json"`, appendere o aggiornare la voce e chiamare `self._carica_plugin_tutti()` alla fine.

**3. Wizard `_ricorda_NomePlugin_plugin()` + step** — uno o più metodi `_NomePlugin_plugin_step_X()` che guidano l'utente attraverso i campi necessari, salvando i dati intermedi in `self.dati_temp`. L'ultimo step chiama il metodo al punto 2 e riporta lo stato a `"idle"`.

**4. Due aggiunte in `_cmd_ricorda`** — un blocco `if nome.lower().startswith("nomeplugin"):` che intercetta il comando e chiama il wizard, esattamente come già fatto per `nota`, `todo` e `agenda`.

**5. Registrazione degli stati in `_gestisci_stati_dialogo`** — un `if self.stato == "attesa_X_nomeplugin": self._step_X(testo); return` per ogni passo del wizard.

---

In sintesi: copia il blocco di `myAgenda` (circa 80 righe in tutto), rinomina le funzioni e adatta i campi del dizionario alla struttura dati del nuovo plugin. Il resto — caricamento, ricerca, elenca, aggiorna — funziona già senza toccare nulla.