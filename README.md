# Dev Tooling

This project is dedicated to gathering and formalizing my development practices, standards, templates, and related resources into a single, accessible repository.

## How To Use
- Download repository
- Add to Path

## Tools Overview

Below is a table summarizing the tools included in this suite:

| Tool Name       | Description                                                                                   |
|-----------------|-----------------------------------------------------------------------------------------------|
| `py-dev.py`     | Automates running static analysis tools (`mypy`, `flake8`, `pylint`) on a Python codebase.    |
| `pattern.py`    | Searches for specified patterns within the codebase, as defined in a YAML configuration file. |
| `check-committed.sh` | Checks for unstaged or uncommitted changes in the git repository.                             |
| `vue-build.py`  | Automates the generation of a JSON file listing Vue components and copies a template HTML file. |

### Detailed Tool Descriptions

#### py-dev.py

Runs static analysis tools (`mypy`, `flake8`, `pylint`) on your Python codebase to ensure code quality. It supports a watch mode that monitors the codebase for changes and reruns the analysis tools automatically, providing real-time feedback on code quality issues.

#### pattern.py

Searches for specified patterns within the codebase, as defined in a YAML configuration file. Useful for identifying occurrences of deprecated functions, patterns that violate coding standards, or any custom patterns you wish to monitor.

#### check-committed.sh

This script checks the current git repository for unstaged or uncommitted changes. It's useful for ensuring that all changes are committed before performing operations that require a clean working directory, such as deployments or builds.

#### vue-build.py

The `vue-build.py` script is a utility designed to facilitate the development and maintenance of Vue.js projects. It automates the process of generating a JSON file that lists all Vue components within a specified directory, typically used for documentation or development purposes. Additionally, it copies a template HTML file to a target directory, providing a scaffold for further customization.

## How They Work

1. **Common Setup (`common.sh`)**: Both `py-dev.sh` and `pattern.sh` source `common.sh`, which sets up a Python virtual environment if it doesn't exist and installs dependencies specified in `requirements.txt`. This ensures that the Python scripts are executed in a consistent and isolated environment.

2. **Running the Tools**:
   - To run `py-dev.py`, execute `./py-dev.sh`. Use `./py-dev.sh --watch` to enable watch mode.
   - To run `pattern.py`, execute `./pattern.sh -c <config_file> -d <directory>`, where `<config_file>` is the path to your YAML configuration file, and `<directory>` is the base directory to search.
   - To check for unstaged or uncommitted changes, execute `./check-committed.sh`.
   - To use `vue-build.py`, run the script from the command line, optionally specifying the target directory as an argument. If no directory is provided, the script uses the current working directory as the target.

Ensure you have Python 3 and Bash available in your environment to use these tools.
