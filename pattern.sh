#!/bin/bash

# Navigate to the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Activate the virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

# Execute the Python script, passing along any command line arguments
python "$SCRIPT_DIR/pattern.py" "$@"

# Capture the exit code of the Python script
PYTHON_EXIT_CODE=$?

# Optionally, deactivate the virtual environment
deactivate

# Exit the shell script with the Python script's exit code
exit $PYTHON_EXIT_CODE