<# 
.SYNOPSIS
    Ricrea l'ambiente virtuale .venv e installa tutti i pacchetti.

.DESCRIPTION
    Questo script:
    1. Rimuove il vecchio .venv (se esiste)
    2. Crea un nuovo ambiente virtuale con uv
    3. Installa tutti i pacchetti da requirements.txt

.NOTES
    Requisiti: uv (https://docs.astral.sh/uv/)
    Uso:       .\scripts\setup.ps1
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$VenvPath    = Join-Path $ProjectRoot ".venv"
$ReqFile     = Join-Path $ProjectRoot "requirements.txt"

Write-Host ""
Write-Host "=== Desktop MCP - Setup Ambiente ===" -ForegroundColor Cyan
Write-Host ""

# ── 1. Verifica prerequisiti ──────────────────────────────────────────────────
Write-Host "[1/4] Verifica uv..." -ForegroundColor Yellow
try {
    $uvVersion = & uv --version 2>&1
    Write-Host "      OK: $uvVersion" -ForegroundColor Green
} catch {
    Write-Host "      ERRORE: uv non trovato. Installalo da https://docs.astral.sh/uv/" -ForegroundColor Red
    exit 1
}

# ── 2. Rimuovi vecchio venv ───────────────────────────────────────────────────
if (Test-Path $VenvPath) {
    Write-Host "[2/4] Rimozione vecchio .venv..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $VenvPath
    Write-Host "      OK: rimosso" -ForegroundColor Green
} else {
    Write-Host "[2/4] Nessun .venv esistente" -ForegroundColor Yellow
}

# ── 3. Crea nuovo venv ───────────────────────────────────────────────────────
Write-Host "[3/4] Creazione .venv..." -ForegroundColor Yellow
Push-Location $ProjectRoot
uv venv .venv
Pop-Location
Write-Host "      OK: .venv creato" -ForegroundColor Green

# ── 4. Installa pacchetti ─────────────────────────────────────────────────────
Write-Host "[4/4] Installazione pacchetti da requirements.txt..." -ForegroundColor Yellow

# Tenta con --native-tls; se fallisce, riprova con --allow-insecure-host (proxy aziendale)
Push-Location $ProjectRoot
try {
    uv pip install -r $ReqFile --native-tls 2>&1 | Out-Null
    Write-Host "      OK: pacchetti installati" -ForegroundColor Green
} catch {
    Write-Host "      Tentativo con allow-insecure-host (proxy aziendale)..." -ForegroundColor Yellow
    uv pip install -r $ReqFile --native-tls --allow-insecure-host pypi.org --allow-insecure-host files.pythonhosted.org
    Write-Host "      OK: pacchetti installati (via insecure host)" -ForegroundColor Green
}
Pop-Location

# ── Done ──────────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "=== Setup completato! ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Prossimi passi:" -ForegroundColor White
Write-Host "  1. Attiva il venv:  .venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "  2. Avvia il server: `$env:PYTHONPATH = 'src'; python main.py" -ForegroundColor Gray
Write-Host ""
