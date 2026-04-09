"""Entry point del progetto.

Avvia il server MCP definito in src/desktop_mcp/server.py.
Per implementazioni custom, non serve modificare questo file:
tutta la logica dei tool va in server.py.

Uso:
    $env:PYTHONPATH = "src"; python main.py
"""

from desktop_mcp.server import main

if __name__ == "__main__":
    main()
