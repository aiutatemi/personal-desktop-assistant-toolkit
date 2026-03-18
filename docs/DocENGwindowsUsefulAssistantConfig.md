# 🖥️ Windows Quick Commands for `dati` field

---

These commands can be entered directly in the `dati` field of your `memory.json` file and launched via the `apri` command (or correspondent word in lang_XX.json file) in the assistant. 
No special syntax or configuration needed — just type the command as shown and Windows will handle the rest.

**Example settings·

```json
  {
    "nome": "display",
    "alias": "video",
    "soggetto": "Comando",
    "dati": "ms-settings:display",
    "tag": "comandi",
    "avatar": "informatica"
  },
  {
    "nome": "task manager",
    "alias": "",
    "soggetto": "Comando",
    "dati": "taskmgr.exe",
    "tag": "comandi",
    "avatar": "informatica"
  }
```

---

**Example usage:**
```
`open display` · 
`open task manager`
```
---

## 📁 Special Folders (`shell:`)
| Action | Command |
|--------|---------|
| Desktop | `shell:desktop` |
| Downloads | `shell:downloads` |
| Documents | `shell:documents` |
| Pictures | `shell:pictures` |
| Videos | `shell:videos` |
| Music | `shell:music` |
| Recycle Bin | `shell:RecycleBinFolder` |
| Startup Programs | `shell:startup` |
| Installed Apps | `shell:AppsFolder` |

## ⚙️ Settings (`ms-settings:`)
| Setting | Command |
|---------|---------|
| Windows Update | `ms-settings:windowsupdate` |
| Network & Internet | `ms-settings:network` |
| Bluetooth | `ms-settings:bluetooth` |
| Display | `ms-settings:display` |
| Sound | `ms-settings:sound` |
| Installed Apps | `ms-settings:appsfeatures` |
| Privacy | `ms-settings:privacy` |
| Battery | `ms-settings:batterysaver` |

## 🔒 Lock PC
| Action | Command |
|--------|---------|
| Lock Workstation | `rundll32.exe user32.dll,LockWorkStation` |
| Suspend | `rundll32.exe powrprof.dll,SetSuspendState 0,1,0` |

## 🧹 Maintenance & System Tools
| Tool | Command |
|------|---------|
| Disk Cleanup | `cleanmgr.exe` |
| Defragmentation | `dfrgui.exe` |
| Task Manager | `taskmgr.exe` |
| Resource Monitor | `resmon.exe` |
| Device Manager | `devmgmt.msc` |
| Services | `services.msc` |
| Command Prompt | `cmd.exe` |
| PowerShell | `powershell.exe` |
| Registry Editor | `regedit.exe` |
| Control Panel | `control.exe` |
| File Explorer | `explorer.exe` |
| System Information | `msinfo32.exe` |