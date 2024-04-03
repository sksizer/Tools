#!/usr/bin/env python3
import os, json, re
import sys
import shutil
from pathlib import Path

def camel_case_to_title(camel_str):
    # Split camelCase and PascalCase into words and capitalize them
    words = re.sub('([a-z0-9])([A-Z])', r'\1 \2', camel_str).split()
    return ' '.join(word.capitalize() for word in words)

def title_from_path(path):
    parts = path.parts[path.parts.index('dev')+1:-1]  # Get all parts after 'dev' and before the file name
    title_parts = [camel_case_to_title(part) for part in parts]  # Convert camel case to title
    script_dir = os.path.dirname(os.path.realpath(__file__))
    dev_dir = Path(script_dir) / 'pages/dev'
    public_dir = Path(script_dir) / 'public'
    json_file = os.path.join(public_dir, 'component-links.json')

    # Ensure the JSON file exists
    os.makedirs(public_dir, exist_ok=True)
    if not os.path.exists(json_file):
        with open(json_file, 'w') as file:
            json.dump([], file)

def title_from_path(path):
    parts = path.parts[path.parts.index('pages')+1:-1]  # Get all parts after 'pages' and before the file name
    title_parts = [camel_case_to_title(part) for part in parts]  # Convert camel case to title
    title_parts.append(camel_case_to_title(path.stem))  # Add the file name (without extension) as the last part
    return ' - '.join(title_parts)

def update_vue_links():
    script_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    dev_dir = Path(script_dir) / 'pages/dev'
    json_file = os.path.join(script_dir, 'public/component-links.json')

    # Initialize an empty list for vue links
    vue_links = []

    # Scan for .vue files in the dev directory and subdirectories
    for vue_file in dev_dir.rglob('*.vue'):
        title = title_from_path(vue_file.relative_to(script_dir))
        url = f'/{vue_file.relative_to(dev_dir.parent).as_posix()}'.replace('.vue', '').replace(' ', '-')
        vue_links.append({'name': title or 'Unnamed Component', 'url': url})

    vue_links.sort(key=lambda x: x['name'])
    # Write updated components back to the JSON file
    with open(json_file, 'w') as file:
        json.dump(vue_links, file, indent=2)

if __name__ == '__main__':
    print("Vue component link update complete.")

def copy_vue_templates():
    template_dir = Path(__file__).resolve().parent / 'vue/template'
    web_dir = template_dir.parents[2]

    for item in template_dir.rglob('*'):
        relative_path = item.relative_to(template_dir)
        dest = web_dir / relative_path

        if item.is_dir():
            os.makedirs(dest, exist_ok=True)
        else:
            shutil.copy2(item, dest)

def main(target_dir):
    copy_vue_templates(target_dir)
    update_vue_links(target_dir)
    print(f"Vue component link update complete for {target_dir}.")

if __name__ == '__main__':
    target_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    main(target_dir)
