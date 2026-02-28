# CBT Software - Run script for PowerShell
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  CBT Online Examination Portal" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Set-Location $PSScriptRoot

# Resolve python launcher reliably (python3 -> python -> py -3)
$pythonExe = $null
$pythonArgs = @()
if (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonExe = "python3"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonExe = "python"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonExe = "py"
    $pythonArgs = @("-3")
}

if (-not $pythonExe) {
    Write-Host "[ERROR] Python not found. Install Python 3.8+ from https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}

# Create venv if missing
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    & $pythonExe @pythonArgs -m venv venv
}

# Use venv python directly (do not rely on PATH/global python)
$venvPython = Join-Path $PSScriptRoot "venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "[ERROR] venv python not found at $venvPython" -ForegroundColor Red
    exit 1
}

Write-Host "Using virtual environment python: $venvPython" -ForegroundColor Yellow
Write-Host "Installing dependencies..." -ForegroundColor Yellow
& $venvPython -m pip install -r requirements.txt -q

Write-Host "`nRunning migrations..." -ForegroundColor Yellow
& $venvPython manage.py migrate

Write-Host "`nStarting server at http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop`n" -ForegroundColor Gray
& $venvPython manage.py runserver
