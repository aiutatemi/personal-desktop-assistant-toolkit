# 🖥️ Comandi Utili di Windows da inserire nel campo `dati`

Comandi per interagire con il sistema operativo Windows
Funziona con tutte le versioni di myAssistant
Testato con Windows 11

---

Questi comandi possono essere inseriti direttamente nel campo `dati` del tuo file `memory.json` e avviati tramite il comando `apri` (o la parola corrispondente nel file lang_XX.json) nell'assistente.
Non è necessaria alcuna sintassi o configurazione speciale: basta digitare il comando come mostrato e Windows gestirà il resto.

**Esempio impostazioni:**

```json
  {
    "nome": "schermo",
    "alias": "video",
    "soggetto": "Comando",
    "dati": "ms-settings:display",
    "tag": "comandi",
    "avatar": "informatica"
  },
  {
    "nome": "task manager",
    "alias": "gestione attività",
    "soggetto": "Comando",
    "dati": "taskmgr.exe",
    "tag": "comandi",
    "avatar": "informatica"
  }
```

---

**Esempio di utilizzo:**
```
`apri schermo` · 
`apri task manager`
```
---

## 📁 Cartelle Speciali (`shell:`)
| Azione | Comando |
|--------|---------|
| Desktop | `shell:desktop` |
| Download | `shell:downloads` |
| Documenti | `shell:documents` |
| Immagini | `shell:pictures` |
| Video | `shell:videos` |
| Musica | `shell:music` |
| Cestino | `shell:RecycleBinFolder` |
| Esecuzione automatica | `shell:startup` |
| App Installate | `shell:AppsFolder` |

## ⚙️ Impostazioni (`ms-settings:`)
| Impostazione | Comando |
|---------|---------|
| Windows Update | `ms-settings:windowsupdate` |
| Rete e Internet | `ms-settings:network` |
| Bluetooth | `ms-settings:bluetooth` |
| Schermo | `ms-settings:display` |
| Audio | `ms-settings:sound` |
| App Installate | `ms-settings:appsfeatures` |
| Privacy | `ms-settings:privacy` |
| Batteria | `ms-settings:batterysaver` |

## 🔒 Blocco PC
| Azione | Comando |
|--------|---------|
| Blocca Postazione | `rundll32.exe user32.dll,LockWorkStation` |
| Sospendi | `rundll32.exe powrprof.dll,SetSuspendState 0,1,0` |

## 🧹 Manutenzione e Strumenti di Sistema
| Strumento | Comando |
|------|---------|
| Pulizia Disco | `cleanmgr.exe` |
| Deframmentazione | `dfrgui.exe` |
| Gestione Attività (Task Manager) | `taskmgr.exe` |
| Monitoraggio Risorse | `resmon.exe` |
| Gestione Dispositivi | `devmgmt.msc` |
| Servizi | `services.msc` |
| Prompt dei Comandi | `cmd.exe` |
| PowerShell | `powershell.exe` |
| Editor del Registro di Sistema | `regedit.exe` |
| Pannello di Controllo | `control.exe` |
| Esplora File | `explorer.exe` |
| System Information | `msinfo32.exe` |

---