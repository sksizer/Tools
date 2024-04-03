#!/usr/bin/env python3
import os
import sys
import json
import shutil
import re  # Import the regex module
from pathlib import Path

def find_vue_files(directory):
    """
    Recursively find all .vue files in the specified directory.
    """
    vue_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".vue"):
                relative_path = os.path.relpath(os.path.join(root, file), directory)
                vue_files.append(relative_path.replace(os.path.sep, '/'))
    return vue_files

def split_camel_case(name):
    """
    Split a camelCase or CamelCase string into words.
    """
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', name)
    return [m.group(0) for m in matches]

def format_name(file_name):
    """
    Format the file name by handling underscores and camelCase as word breaks.
    """
    # Replace underscores with spaces and split on space to handle underscores
    parts = file_name.replace('_', ' ').split(' ')
    formatted_parts = []
    for part in parts:
        # For each part, further split on camelCase boundaries and capitalize each word
        camel_case_parts = split_camel_case(part)
        formatted_parts.extend(camel_case_parts)
    # Capitalize each word and join with spaces
    return ' '.join(word.capitalize() for word in formatted_parts)

def generate_json(vue_files):
    """
    Generate a JSON object from the list of Vue files, formatting names as specified.
    """
    data = []
    for file in vue_files:
        # Split the path into parts
        parts = file.split('/')
        # Remove the '.vue' extension for the file name
        file_name = parts[-1][:-4]
        # Format the file name to handle underscores and camelCase
        formatted_file_name = format_name(file_name)
        # Capitalize and format directory names, replace underscores with spaces
        directory_names = [format_name(part) for part in parts[:-1]]
        # Combine directory names and formatted file name
        name = " - ".join(directory_names + [formatted_file_name])
        # Construct the URL
        url = "/dev/" + "/".join(parts).replace('.vue', '')
        # Append the formatted data
        data.append({"name": name, "url": url})
    return json.dumps(data, indent=4)

def copy_template(source, target):
    """
    Copy the template file from source to target directory, overwriting any existing file.
    """
    shutil.copyfile(source, target)

def main(target_directory=None):
    if target_directory is None:
        target_directory = os.getcwd()
    else:
        target_directory = Path(target_directory).resolve()

    source_directory = Path(__file__).parent
    template_source = source_directory / "vue/template/public/dev.html"
    template_target = target_directory / "public/dev.html"

    # Copy the template file
    copy_template(template_source, template_target)

    # Find all Vue files
    vue_files_directory = target_directory / "pages/dev"
    vue_files = find_vue_files(vue_files_directory)

    # Generate JSON
    json_data = generate_json(vue_files)

    # Write JSON to file in the target/public directory
    json_file_path = target_directory / "public/dev_pages.json"
    with open(json_file_path, "w") as json_file:
        json_file.write(json_data)

    print(f"JSON file generated successfully at {json_file_path}.")

if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else None
    main(target_dir)
