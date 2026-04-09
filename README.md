# fastMCP – Template Server MCP

Progetto base (PoC) per creare server [MCP](https://modelcontextprotocol.io/) con **FastMCP** e **Uvicorn**.  
Pensato come punto di partenza: clona, modifica i tool in `server.py` e avvia il tuo server personalizzato.

## Struttura del progetto

```
fastMCP/
├── main.py                          ← entry point (non serve modificarlo)
├── pyproject.toml                   ← dipendenze e metadati progetto
├── requirements.txt                 ← versioni esatte dei pacchetti (per ricreare il venv)
├── .gitignore
├── README.md
│
├── scripts/
│   └── setup.ps1                    ← script per ricreare il venv da zero
│
├── src/
│   └── desktop_mcp/                 ← 👉 package del server MCP
│       ├── __init__.py              ←    versione del package
│       └── server.py                ← ⭐ MODIFICA QUI: tool, nome, config
│
└── .venv/                           ← ambiente virtuale (uv, non versionato)
```

### Cosa modificare per un nuovo server MCP

| File | Cosa cambiare |
|------|---------------|
| `src/desktop_mcp/server.py` | **Nome** e **instructions** dell'istanza `FastMCP`, le **costanti**, e i **tool** (funzioni `@mcp.tool()`) |
| `src/desktop_mcp/` | Rinomina il package se vuoi un nome diverso (aggiorna anche `pyproject.toml` e `main.py`) |
| `pyproject.toml` | Nome progetto, versione, descrizione, dipendenze aggiuntive |

## Requisiti

- Python ≥ 3.12
- [uv](https://docs.astral.sh/uv/) (package manager)

## Installazione

### Opzione A – Script automatico (consigliata)

Lo script ricrea il `.venv` da zero e installa tutti i pacchetti da `requirements.txt`:

```powershell
# Windows PowerShell
.\scripts\setup.ps1
```

> **Nota proxy aziendale:** lo script gestisce automaticamente i problemi di certificato SSL provando prima `--native-tls` e poi `--allow-insecure-host`.

### Opzione B – Manuale

```bash
# 1. Crea l'ambiente virtuale
uv venv .venv

# 2. Installa i pacchetti (versioni esatte)
uv pip install -r requirements.txt --native-tls

# 3. (oppure solo le dipendenze principali, senza versioni fissate)
#    uv pip install fastmcp uvicorn pylint --native-tls
```

### Aggiornare requirements.txt

Dopo aver aggiunto o aggiornato pacchetti, rigenera il file:

```bash
uv pip freeze > requirements.txt
```

## Avvio

```powershell
# Windows PowerShell
$env:PYTHONPATH = "src"; python main.py
```

```bash
# Linux / macOS
PYTHONPATH=src python main.py
```

Il server sarà disponibile su `http://localhost:8000/mcp`.

## Tool di esempio

Il server di esempio (**Desktop File Manager**) espone 4 tool per manipolare file sul Desktop:

| Tool | Descrizione |
|------|-------------|
| `list_desktop_files` | Elenca i file sul Desktop |
| `create_desktop_file` | Crea un file di testo |
| `read_desktop_file` | Legge il contenuto di un file |
| `delete_desktop_file` | Elimina un file |

## Come aggiungere un tool

In `src/desktop_mcp/server.py`:

```python
@mcp.tool()
def my_new_tool(param: str) -> str:
    """Descrizione del tool (visibile ai client MCP)."""
    # logica del tool
    return "risultato"
```

La **docstring** viene usata come descrizione del tool e i **type hints** definiscono lo schema di input.