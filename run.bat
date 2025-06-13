@echo off
setlocal

:: -------------------------------
:: Step 0: Return to this script's folder
:: -------------------------------
cd /d "%~dp0"

:: -------------------------------
:: Step 1: Elevate to admin if not already
:: -------------------------------
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -NoProfile -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: -------------------------------
:: Step 2: Check for Python
:: -------------------------------
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Installing Python 3.10...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe -OutFile python-installer.exe"
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python-installer.exe
)

:: -------------------------------
:: Step 3: Create venv if needed
:: -------------------------------
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: -------------------------------
:: Step 4: Activate and install dependencies
:: -------------------------------
call venv\Scripts\activate
pip install -r requirements.txt

:: -------------------------------
:: Step 5: Run the Python app
:: -------------------------------
python main.py

pause
