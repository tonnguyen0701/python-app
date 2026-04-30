@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    set "PYTHON=.venv\Scripts\python.exe"
) else if exist "venv\Scripts\python.exe" (
    set "PYTHON=venv\Scripts\python.exe"
) else (
    echo No Python executable found in .venv or venv.
    echo Please install the virtual environment or run from an active Python environment.
    pause
    exit /b 1
)

set "CLEAR_DB_ON_START=1"
set "SEED_DB_ON_START=1"
"%PYTHON%" main.py
if errorlevel 1 pause
