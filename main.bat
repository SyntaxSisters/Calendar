@echo off
cd /d "%~dp0"
cd src
if not exist ".venv\" (
    echo Creating virtual environment...
    python -m venv .venv
    echo Virtual environment created.
    call .venv\Scripts\activate.bat
    echo Installing requirements...
    pip install -r ../requirements.txt
) else (
    call .venv\Scripts\activate.bat
    echo Installing requirements...
    pip install -r ../requirements.txt
)

python app.py
