@echo off
cd /d "%~dp0"
set PYTHON_EXE=py -3.13
if not exist ".venv\" (
    echo Creating virtual environment with Python 3.13...
    %PYTHON_EXE% -m venv .venv
    echo Virtual environment created.
    call .venv\Scripts\activate
    echo Installing dependencies...
    %PYTHON_EXE% -m pip install -r requirements.txt
    echo Installing python-dateutil...
    %PYTHON_EXE% -m pip install python-dateutil
) else (
    call .venv\Scripts\activate
    echo Installing dependencies...
    %PYTHON_EXE% -m pip install -r requirements.txt
    echo Installing python-dateutil...
    %PYTHON_EXE% -m pip install python-dateutil
)

%PYTHON_EXE% YourBestie\main.py
