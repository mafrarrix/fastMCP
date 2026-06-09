"""Server MCP per la gestione dei file sul Desktop dell'utente.

Questo modulo è il cuore del server MCP. Per creare un nuovo server
personalizzato:

1. Modifica `name` e `instructions` dell'istanza FastMCP.
2. Sostituisci o aggiungi funzioni decorate con `@mcp.tool()`.
   - La **docstring** della funzione diventa la descrizione del tool
     visibile ai client MCP.
   - I **type hints** dei parametri definiscono lo schema di input.
3. Aggiorna le costanti (es. DESKTOP) in base al dominio del nuovo server.
"""

from pathlib import Path
from fastmcp import FastMCP

# ── Costanti ──────────────────────────────────────────────────────────────────
# 👉 PERSONALIZZA: cambia questo path per puntare alle risorse del tuo server.
DESKTOP: Path = Path.home() 

# ── Istanza FastMCP ───────────────────────────────────────────────────────────
# 👉 PERSONALIZZA: modifica `name` e `instructions` per descrivere il tuo server.
#    - `name`:         nome visibile ai client MCP.
#    - `instructions`: descrizione di cosa fa il server (usata dai LLM).
mcp = FastMCP(
    name="Desktop File Manager",
    instructions=(
        "Server MCP che permette di creare, leggere, elencare ed eliminare "
        "file di testo sul Desktop dell'utente."
    ),
)


# ══════════════════════════════════════════════════════════════════════════════
#  TOOL DEFINITIONS
#  👉 Ogni funzione decorata con @mcp.tool() viene esposta come tool MCP.
#     - La docstring diventa la descrizione del tool.
#     - I parametri tipizzati diventano lo schema JSON di input.
#     - Il valore di ritorno è la risposta inviata al client.
#
#  Per aggiungere un nuovo tool: crea una funzione, decorala con @mcp.tool()
#  e aggiungi una docstring descrittiva.
# ══════════════════════════════════════════════════════════════════════════════


@mcp.tool()
def list_desktop_files() -> list[str]:
    """Elenca tutti i file (non cartelle) presenti sul Desktop.

    Returns:
        Lista di nomi di file presenti sul Desktop.
    """
    if not DESKTOP.exists():
        return []
    return sorted(
        entry.name for entry in DESKTOP.iterdir() if entry.is_file()
    )


@mcp.tool()
def create_desktop_file(filename: str, content: str = "") -> str:
    """Crea un nuovo file di testo sul Desktop.

    Args:
        filename: Nome del file da creare (es. "note.txt").
        content:  Contenuto testuale del file (default: stringa vuota).

    Returns:
        Messaggio di conferma o di errore.
    """
    target = DESKTOP / filename
    if target.exists():
        return f"❌ Il file '{filename}' esiste già sul Desktop."
    try:
        target.write_text(content, encoding="utf-8")
        return f"✅ File '{filename}' creato sul Desktop."
    except OSError as exc:
        return f"❌ Errore durante la creazione: {exc}"


@mcp.tool()
def read_desktop_file(filename: str) -> str:
    """Legge e restituisce il contenuto di un file sul Desktop.

    Args:
        filename: Nome del file da leggere (es. "note.txt").

    Returns:
        Contenuto del file oppure messaggio di errore.
    """
    target = DESKTOP / filename
    if not target.exists():
        return f"❌ Il file '{filename}' non esiste sul Desktop."
    if not target.is_file():
        return f"❌ '{filename}' è una cartella, non un file."
    try:
        return target.read_text(encoding="utf-8")
    except OSError as exc:
        return f"❌ Errore durante la lettura: {exc}"


@mcp.tool()
def delete_desktop_file(filename: str) -> str:
    """Elimina un file dal Desktop.

    Args:
        filename: Nome del file da eliminare (es. "note.txt").

    Returns:
        Messaggio di conferma o di errore.
    """
    target = DESKTOP / filename
    if not target.exists():
        return f"❌ Il file '{filename}' non esiste sul Desktop."
    if not target.is_file():
        return f"❌ '{filename}' è una cartella; questa operazione gestisce solo file."
    try:
        target.unlink()
        return f"✅ File '{filename}' eliminato dal Desktop."
    except OSError as exc:
        return f"❌ Errore durante l'eliminazione: {exc}"


# ── Entrypoint ────────────────────────────────────────────────────────────────
# 👉 PERSONALIZZA: modifica transport, host e port se necessario.
#    Trasporti disponibili: "streamable-http", "sse", "stdio"
def main() -> None:
    """Avvia il server MCP (usato da main.py e da pyproject.toml scripts)."""
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
