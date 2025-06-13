#!/bin/bash

cd "$(dirname "$0")"

# Request admin privileges
if [ "$EUID" -ne 0 ]; then
  echo "Requesting administrator privileges..."
  exec sudo "$0" "$@"
  exit
fi

# Check and install Python 3.12 + venv + pip
echo "Checking Python installation..."
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3.12-full python3.12-distutils python3.12-dev tk

# Create venv if not present
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3.12 -m venv venv
fi

# Ensure pip is installed in the venv
echo "Ensuring pip inside virtual environment..."
./venv/bin/python -m ensurepip --upgrade
./venv/bin/python -m pip install --upgrade pip

# Install dependencies
echo "Installing Python packages..."
./venv/bin/pip install -r requirements.txt --break-system-packages

# Launch the app
echo "Launching the Document Search Tool..."
./venv/bin/python main.py

