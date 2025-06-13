#!/bin/bash

# -------------------------------
# Step 0: Go to script directory
# -------------------------------
cd "$(dirname "$0")"

# -------------------------------
# Step 1: Check for sudo/admin rights
# -------------------------------
if [ "$EUID" -ne 0 ]; then
  echo "Requesting administrator privileges..."
  exec sudo "$0" "$@"
  exit
fi

# -------------------------------
# Step 2: Check for Python 3
# -------------------------------
if ! command -v python3 &> /dev/null; then
    echo "Python3 not found. Installing Python 3.10..."
    sudo apt update
    sudo apt install -y python3.10 python3.10-venv python3-pip
else
    echo "Python3 found: $(python3 --version)"
fi

# -------------------------------
# Step 3: Create venv if needed
# -------------------------------
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# -------------------------------
# Step 4: Activate and install dependencies
# -------------------------------
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# -------------------------------
# Step 5: Run the Python app
# -------------------------------
python main.py
