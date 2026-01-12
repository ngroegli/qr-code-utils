#!/bin/bash

###############################################################################
# QR Code Utils - Wrapper Script
# Activates virtual environment and runs src/main.py
###############################################################################

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Path to virtual environment
VENV_DIR="$SCRIPT_DIR/venv"

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Error: Virtual environment not found at $VENV_DIR"
    echo "Please run ./install.sh first to set up the environment."
    exit 1
fi

# Activate virtual environment and run src/main.py
source "$VENV_DIR/bin/activate"
python "$SCRIPT_DIR/src/main.py" "$@"
exit_code=$?

# Deactivate is not needed as the script will exit
exit $exit_code
