@echo off
cd /d "%~dp0"
cd src
if not exist ".venv\" (
    echo Creating virtual environment...
    python -m venv .venv
    echo Virtual environment created.
    call .venv\Scripts\activate
    echo Installing Flet...
    python3 -m pip install -r ../requirements.txt
    echo Installing python-dateutil...
    pip install python-dateutil
    pip install flet
    pip install typing_extensions
) else (
    call .venv\Scripts\activate
    python3 -m pip install -r ../requirements.txt
    pip install python-dateutil
    pip install flet
    pip install typing_extensions
)

python app.py
