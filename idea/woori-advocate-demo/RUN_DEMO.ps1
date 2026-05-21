Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$backend = Join-Path $repoRoot "backend"
$venv = Join-Path $backend ".venv"

Set-Location $backend

if (-not (Test-Path $venv)) {
    python -m venv .venv
}

& (Join-Path $venv "Scripts\python.exe") -m pip install -r requirements.txt

Write-Host "Starting Woori Advocate at http://127.0.0.1:8000"
& (Join-Path $venv "Scripts\python.exe") -m uvicorn main:app --host 127.0.0.1 --port 8000
