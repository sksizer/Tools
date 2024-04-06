#!/bin/bash

# Navigate to the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Activate the virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

# Execute the Python script, passing along any command line arguments
python "$SCRIPT_DIR/pattern.py" "$@"

# Optionally, deactivate the virtual environment
deactivate