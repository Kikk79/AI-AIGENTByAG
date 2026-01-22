@echo off
TITLE J.A.R.V.I.S. Installer

echo ===================================================
echo      J.A.R.V.I.S. INSTALLATION (WINDOWS)
echo ===================================================

REM Check for Python
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.10+ from python.org
    pause
    exit /b
)


echo [1/4] Creating Virtual Environment...
python -m venv venv
call venv\Scripts\activate.ps1

echo [2/4] Upgrading pip...
python -m pip install --upgrade pip

echo [3/4] Installing Dependencies...
pip install -r requirements.txt

IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b
)

echo [3/3] Checking Configuration...
if not exist .env (
    echo Creating .env file template...
    echo GEMINI_API_KEY=YOUR_KEY_HERE > .env
    echo ELEVENLABS_API_KEY=YOUR_KEY_HERE >> .env
    echo [WARN] Please edit .env and add your API keys!
) else (
    echo .env file found.
)

echo.
echo ===================================================
echo      INSTALLATION COMPLETE
echo ===================================================
echo to start Jarvis, run: python jarvis.py
echo.
pause
