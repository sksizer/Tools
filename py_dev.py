#!/usr/bin/env python3
import subprocess
import sys
import yaml
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# List of directories and files to ignore during file change detection
IGNORED_PATHS = [
    '.mypy_cache',  # Cache directory for mypy type checker
    '__pycache__',  # Compiled Python bytecode directory
    '.git',         # Git version control directory
    'venv',         # Virtual environment directory
    # Add any other directories or files you want to ignore
]

def load_python_config():
    """Loads Python configuration from a YAML config file."""
    with open('dev.config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        return config['python']

class ChangeHandler(FileSystemEventHandler):
    """Handles file change events."""
    def __init__(self, ignore_paths):
        self.ignore_paths = ignore_paths

    def on_any_event(self, event):
        # Check if the event's source path should be ignored
        if any(event.src_path.startswith(f'./{ignore_path}') for ignore_path in self.ignore_paths):
            return
        # Ignore changes in system directories or files
        if any(ignored_path in event.src_path for ignored_path in IGNORED_PATHS):
            return
        if event.is_directory:
            return
        print(f"Detected changes in: {event.src_path}")
        run_tools(self.ignore_paths)

def run_command(command):
    """Run a command and stream output in real-time."""
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    stderr = process.communicate()[1]
    if stderr:
        print("STDERR:", stderr.strip())

def run_tools(ignore_paths):
    """Runs static analysis tools with real-time output."""
    python_config = load_python_config()
    entrance_files = python_config['pylint']['entrance']
    ignore_paths_str = ','.join(ignore_paths)
    
    print("Running mypy...")
    mypy_command = ["mypy", ".", f"--exclude=({ignore_paths_str})"]
    run_command(mypy_command)
    
    print("Running flake8...")
    flake8_command = ["flake8", ".", f"--exclude={ignore_paths_str}"]
    run_command(flake8_command)
    
    print("Running pylint...")
    pylint_command = ["pylint", *entrance_files, f"--ignore={ignore_paths_str}"]
    # Modification to capture and print pylint output in real-time
    result = subprocess.run(pylint_command, capture_output=True, text=True)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

def main():
    python_config = load_python_config()
    ignore_paths = python_config['ignore_paths']
    
    # Run tools initially before starting to watch
    run_tools(ignore_paths)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--watch':
        path = '.'  # Set the directory to watch
        event_handler = ChangeHandler(ignore_paths)
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
        print("Watching for file changes. Press Ctrl+C to stop.")
        try:
            while True:
                pass
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
    else:
        run_tools(ignore_paths)

if __name__ == "__main__":
    main()
