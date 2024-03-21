#!/usr/bin/env python3
import os
import shutil
import subprocess
from pathlib import Path

def copy_dev_tools():
    source_dir = Path(__file__).parent
    dest_dir = source_dir.parent / '._dev_tools'

    # Ensure the destination directory exists
    os.makedirs(dest_dir, exist_ok=True)

    # Copy all files from source to destination
    for item in source_dir.rglob('*'):
        if item.is_file():
            relative_path = item.relative_to(source_dir)
            dest_file = dest_dir / relative_path
            os.makedirs(dest_file.parent, exist_ok=True)
            shutil.copy2(item, dest_file)

def git_add_and_commit():
    dev_tools_dir = Path(__file__).parent.parent / '._dev_tools'
    os.chdir(dev_tools_dir)

    # Add all changes to git
    subprocess.run(['git', 'add', '.'], check=True)

    # Commit with a prompt for commit message
    commit_message = input("Enter a commit message: ")
    subprocess.run(['git', 'commit', '-m', commit_message], check=True)

if __name__ == '__main__':
    copy_dev_tools()
    git_add_and_commit()
