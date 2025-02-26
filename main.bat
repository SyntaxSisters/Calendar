@echo off
cd /d "%~dp0"
if not exist ".venv\" (
    echo Creating virtual environment...
    python -m venv .venv
    echo Virtual environment created.
    call .venv\Scripts\activate
    echo Installing Flet...
    python -m pip install -r requirements.txt
) else (
    call .venv\Scripts\activate
    python -m pip install -r requirements.txt
)

python app.py
