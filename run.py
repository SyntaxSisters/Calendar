#!/usr/bin/env python3

import os
import sys
import subprocess

PYTHON_EXE = "python3" if sys.platform != "win32" else "py -3.13"

venv_dir = ".venv"
venv_activate = os.path.join(venv_dir, "Scripts", "activate") if sys.platform == "win32" else os.path.join(venv_dir, "bin", "activate")

def run_command(command, shell=True):
    """ Runs a command in the system shell. """
    subprocess.run(command, shell=shell, check=True)

if not os.path.exists(venv_dir):
    print("Creating virtual environment...")
    run_command(f"{PYTHON_EXE} -m venv {venv_dir}")
    print("Virtual environment created.")

if sys.platform == "win32":
    run_command(f"call {venv_activate} && {PYTHON_EXE} -m pip install -r requirements.txt && {PYTHON_EXE} -m pip install python-dateutil")
else:
    run_command(f"source {venv_activate} && {PYTHON_EXE} -m pip install -r requirements.txt && {PYTHON_EXE} -m pip install python-dateutil")

print("Running YourBestie/main.py...")
run_command(f"{PYTHON_EXE} YourBestie/main.py")
