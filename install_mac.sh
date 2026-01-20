#!/bin/bash

echo "==================================================="
echo "      J.A.R.V.I.S. INSTALLATION (MACOS/LINUX)"
echo "==================================================="

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 is not installed."
    exit 1
fi

# Check for Homebrew (often needed for portaudio)
if command -v brew &> /dev/null; then
    echo "[1/4] Checking System Dependencies (PortAudio)..."
    brew install portaudio || echo "PortAudio already installed or brew failed (ignoring)"
else
    echo "[WARN] Homebrew not found. Ensure 'portaudio' is installed if you have audio issues."
fi

echo "[2/4] Upgrading pip..."
python3 -m pip install --upgrade pip

echo "[3/4] Installing Python Dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies."
    exit 1
fi

echo "[4/4] Checking Configuration..."
if [ ! -f .env ]; then
    echo "Creating .env file template..."
    echo "GEMINI_API_KEY=YOUR_KEY_HERE" > .env
    echo "ELEVENLABS_API_KEY=YOUR_KEY_HERE" >> .env
    echo "[WARN] Please edit .env and add your API keys!"
else
    echo ".env file found."
fi

echo ""
echo "==================================================="
echo "      INSTALLATION COMPLETE"
echo "==================================================="
echo "To start Jarvis, run: python3 jarvis.py"
echo ""
