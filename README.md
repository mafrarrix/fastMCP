# fastMCP – Desktop File Manager

Server [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) costruito con **FastMCP** e **Uvicorn** che permette ai client compatibili (es. Claude Desktop, VS Code Copilot, MCP Inspector, ecc.) di **gestire file di testo nella home dell'utente** tramite tool esposti via HTTP.

Il progetto nasce come **template/PoC**: puoi usarlo così com'è oppure modificare i tool in [src/desktop_mcp/server.py](src/desktop_mcp/server.py) per costruire il tuo server MCP personalizzato.

---

## Cosa fa il progetto

Espone un server MCP all'indirizzo `http://localhost:8000/mcp` con 4 tool pronti all'uso che operano sulla directory home dell'utente:

| Tool | Descrizione |
|------|-------------|
| `list_desktop_files` | Elenca tutti i file presenti nella home |
| `create_desktop_file` | Crea un nuovo file di testo |
| `read_desktop_file` | Legge il contenuto di un file esistente |
| `delete_desktop_file` | Elimina un file |

Trasporto utilizzato: **streamable-http** (configurabile nella funzione `main()` di [server.py](src/desktop_mcp/server.py)).

---

## Struttura del progetto

```
fastMCP/
├── pyproject.toml          # metadati e dipendenze del progetto
├── requirements.txt        # versioni esatte dei pacchetti (lock)
├── README.md
├── LICENSE
│
├── scripts/
│   └── setup.ps1           # script automatico per creare il .venv
│
└── src/
    └── desktop_mcp/        # package principale
        ├── __init__.py     # versione del package
        ├── main.py         # entry point (avvia il server)
        └── server.py       # ⭐ istanza FastMCP + definizione dei tool
```

---

## Requisiti

- **Python ≥ 3.12**
- **[uv](https://docs.astral.sh/uv/)** come package manager (consigliato)
- Sistema operativo: Windows / Linux / macOS

---

## Guida passo passo per l'avvio

### 1. Clona il repository

```powershell
git clone <url-del-repo> fastMCP
cd fastMCP
```

### 2. Installa `uv` (se non già presente)

Su Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Su Linux / macOS:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verifica l'installazione:

```powershell
uv --version
```

### 3. Crea l'ambiente virtuale e installa le dipendenze

#### Opzione A – Script automatico (consigliata su Windows)

Lo script [scripts/setup.ps1](scripts/setup.ps1) elimina il vecchio `.venv` (se presente), ne crea uno nuovo e installa tutti i pacchetti da [requirements.txt](requirements.txt):

```powershell
.\scripts\setup.ps1
```

> **Nota proxy aziendale:** lo script gestisce automaticamente i problemi di certificato SSL: prova prima con `--native-tls` e in caso di errore ripiega su `--allow-insecure-host`.

#### Opzione B – Manuale (cross-platform)

```powershell
# 1. Crea il virtual environment
uv venv .venv

# 2. Installa le dipendenze esatte
uv pip install -r requirements.txt --native-tls
```

In alternativa puoi installare il progetto come package editabile (usa le dipendenze dichiarate in [pyproject.toml](pyproject.toml)):

```powershell
uv pip install -e . --native-tls
```

### 4. Attiva l'ambiente virtuale

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

### 5. Avvia il server

**Windows (PowerShell):**

```powershell
$env:PYTHONPATH = "src"; python src\desktop_mcp\main.py
```

**Linux / macOS:**

```bash
PYTHONPATH=src python src/desktop_mcp/main.py
```

Se hai installato il progetto come package (Opzione B alternativa), puoi anche usare lo script registrato in [pyproject.toml](pyproject.toml):

```powershell
desktop-mcp
```

### 6. Verifica che il server sia attivo

Il server è in ascolto su:

```
http://localhost:8000/mcp
```

A questo indirizzo puoi collegare qualsiasi client MCP compatibile (Claude Desktop, MCP Inspector, VS Code, ecc.).

---

## Personalizzazione

Per trasformare questo template nel tuo server MCP, modifica [src/desktop_mcp/server.py](src/desktop_mcp/server.py):

| Cosa modificare | Dove |
|-----------------|------|
| Nome e descrizione del server | `FastMCP(name=..., instructions=...)` |
| Costanti (es. percorsi) | `DESKTOP = Path.home()` |
| Tool esistenti / nuovi tool | Funzioni decorate con `@mcp.tool()` |
| Trasporto, host, porta | Funzione `main()` |

### Esempio: aggiungere un nuovo tool

```python
@mcp.tool()
def my_new_tool(param: str) -> str:
    """Descrizione del tool (visibile ai client MCP)."""
    return f"Risultato per {param}"
```

La **docstring** diventa la descrizione del tool e i **type hints** definiscono lo schema JSON di input.

---

## Aggiornare requirements.txt

Dopo aver aggiunto o aggiornato pacchetti, rigenera il lock file:

```powershell
uv pip freeze > requirements.txt
```

---

## Troubleshooting

| Problema | Soluzione |
|----------|-----------|
| `uv` non riconosciuto | Riavvia il terminale dopo l'installazione, oppure aggiungi `uv` al PATH |
| Errore SSL durante `uv pip install` | Usa lo script [scripts/setup.ps1](scripts/setup.ps1) oppure aggiungi `--allow-insecure-host pypi.org --allow-insecure-host files.pythonhosted.org` |
| `ModuleNotFoundError: desktop_mcp` | Verifica di aver impostato `PYTHONPATH=src` prima di lanciare `python` |
| Porta 8000 occupata | Modifica `port=8000` nella funzione `main()` di [server.py](src/desktop_mcp/server.py) |

---

## Licenza

Vedi [LICENSE](LICENSE).
