#!/usr/bin/env python3
"""
This module searches for specified patterns in files based on a YAML configuration.
It allows for including and excluding directories in the search.
"""

import argparse
import glob
import os
import re
import sys
import yaml

def load_config(config_path):
    """Load YAML configuration from a file."""
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def find_files(include_patterns, exclude_dirs, base_dir):
    """Find files matching include patterns and not in exclude directories."""
    all_files = set()
    for pattern in include_patterns:
        full_pattern = os.path.join(base_dir, pattern)
        for file in glob.glob(full_pattern, recursive=True):
            if not any(excluded in file for excluded in exclude_dirs):
                all_files.add(file)
    return all_files

def check_pattern_in_files(files, pattern):
    """Check if a pattern is present in the given files."""
    matched_files = []
    compiled_pattern = re.compile(pattern)
    for file in files:
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            if compiled_pattern.search(f.read()):
                matched_files.append(file)
    return matched_files

def main(config_file, base_dir):
    """Main function to load config, find and check files for patterns."""
    config = load_config(config_file)
    pattern_found = False
    for pattern_config in config['patterns']:
        pattern = pattern_config['pattern']
        include_patterns = pattern_config['include']
        exclude_dirs = pattern_config['exclude']
        files = find_files(include_patterns, exclude_dirs, base_dir)
        matched_files = check_pattern_in_files(files, pattern)
        if matched_files:
            pattern_found = True
            print(f"Pattern '{pattern}' found in:")
            for file in matched_files:
                print(f"- {file}")
        else:
            print(f"No matches found for pattern '{pattern}'.")
    return pattern_found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Search for patterns in files based on a YAML configuration.")
    parser.add_argument("-c", "--config", type=str, default="dev.config.yaml",
                        help="Path to the YAML configuration file. Defaults to 'dev.config.yaml'.")
    parser.add_argument("-d", "--directory", type=str, default=os.getcwd(),
                        help="Base directory to work from. Defaults to the " +
                        "current working directory.")
    args = parser.parse_args()

    if main(args.config, args.directory):
        sys.exit(1)  # Exit with a non-zero exit code if a pattern is found
    else:
        sys.exit(0)  # Exit with 0 if no pattern is found
