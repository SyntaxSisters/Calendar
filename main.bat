@echo off
cd /d "%~dp0"
if not exist ".venv\" (
    echo Creating virtual environment...
    python -m venv .venv
    echo Virtual environment created.
    call .venv\Scripts\activate
    echo Installing Flet...
    python -m pip install -r requirements.txt
    echo Installing python-dateutil...
    python -m pip install python-dateutil
) else (
    call .venv\Scripts\activate
    python3 -m pip install -r requirements.txt
    echo Installing python-dateutil...
    pip install python-dateutil
)

python YourBestie\main.py
