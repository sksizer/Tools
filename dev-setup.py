#!/usr/bin/env python3
import shutil
import os

def copy_config_file(source_path, target_directory):
    """
    Copies the specified source file to the target directory.
    """
    # Ensure the target directory exists
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    
    # Define the target file path
    target_path = os.path.join(target_directory, os.path.basename(source_path))
    
    # Copy the file
    shutil.copy2(source_path, target_path)
    print(f"File '{source_path}' has been copied to '{target_path}'.")

if __name__ == "__main__":
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.realpath(__file__))
    
    # Define the source path of the dev.config.yaml file relative to the script location
    source_file_path = os.path.join(script_dir, 'template/pattern/dev.config.yaml')
    
    # Define the target directory (current working directory)
    target_dir = os.getcwd()
    
    # Copy the file
    copy_config_file(source_file_path, target_dir)
