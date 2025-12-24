@echo off
set LOG_DIR=logs
set LOG_FILE=logs\demo_run.log

if not exist %LOG_DIR% mkdir %LOG_DIR%

echo ====================================== >> %LOG_FILE%
echo MindForge Telegram Bot - DEMO MODE >> %LOG_FILE%
echo %DATE% %TIME% >> %LOG_FILE%
echo ====================================== >> %LOG_FILE%

cd /d %~dp0

echo Checking Python... | tee -a %LOG_FILE%
python --version >> %LOG_FILE% 2>&1

if not exist .venv (
    echo Creating virtual environment... | tee -a %LOG_FILE%
    python -m venv .venv >> %LOG_FILE% 2>&1
)

set VENV_PYTHON=.venv\Scripts\python.exe

echo Installing dependencies... | tee -a %LOG_FILE%
%VENV_PYTHON% -m pip install aiogram pydantic-settings >> %LOG_FILE% 2>&1

echo Starting bot in DEMO mode... | tee -a %LOG_FILE%
%VENV_PYTHON% -m src.bot.bot --demo >> %LOG_FILE% 2>&1

pause
