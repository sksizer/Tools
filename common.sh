#!/bin/bash

# Navigate to the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[1]}" )" &> /dev/null && pwd )"
VENV_PATH="$SCRIPT_DIR/venv"

# Check if the virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv "$VENV_PATH"
    
    # Activate the virtual environment
    source "$VENV_PATH/bin/activate"
    
    echo "Installing dependencies from requirements.txt..."
    pip install -r "$SCRIPT_DIR/requirements.txt"
else
    # Activate the virtual environment
    source "$VENV_PATH/bin/activate"
fi

# Function to deactivate the virtual environment and exit with the provided exit code
function cleanup_and_exit {
    deactivate
    exit $1
}