#!/bin/bash

source "$(dirname "$0")/common.sh"

# Execute the Python script, passing along any command line arguments
python "$SCRIPT_DIR/pattern.py" "$@"

# Capture the exit code of the Python script
PYTHON_EXIT_CODE=$?

# Optionally, deactivate the virtual environment and exit
cleanup_and_exit $PYTHON_EXIT_CODE