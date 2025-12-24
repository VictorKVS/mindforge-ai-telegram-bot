# bootstrap.ps1
$ErrorActionPreference = "Stop"

$PROJECT_ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $PROJECT_ROOT

$LOG_DIR = Join-Path $PROJECT_ROOT "logs"
$LOG_FILE = Join-Path $LOG_DIR "demo_run.log"

if (-not (Test-Path $LOG_DIR)) {
    New-Item -ItemType Directory -Path $LOG_DIR | Out-Null
}

Start-Transcript -Path $LOG_FILE -Append

Write-Host "======================================"
Write-Host "MindForge bootstrap starting (DEMO)"
Write-Host "Project root: $PROJECT_ROOT"
Write-Host "Log file: $LOG_FILE"
Write-Host "======================================"

Write-Host "Checking Python..."
python --version

if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
} else {
    Write-Host "Virtual environment already exists"
}

$VENV_PYTHON = ".\.venv\Scripts\python.exe"

Write-Host "Upgrading pip..."
& $VENV_PYTHON -m pip install --upgrade pip

Write-Host "Installing dependencies..."
& $VENV_PYTHON -m pip install aiogram pydantic-settings

Write-Host "Starting bot in DEMO mode..."
& $VENV_PYTHON -m src.bot.bot --demo

Write-Host "Done"
Stop-Transcript
