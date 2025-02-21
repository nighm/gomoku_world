import os
import sys
from pathlib import Path

def fix_file_encoding(file_path):
    try:
        # First try to read with UTF-8
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # If UTF-8 fails, try with another encoding (e.g., cp1252)
        with open(file_path, 'r', encoding='cp1252') as f:
            content = f.read()
    
    # Write back with UTF-8 encoding (without BOM)
    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

def main():
    # Get all Python files in the project
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                file_path = Path(root) / file
                print(f"Processing {file_path}")
                fix_file_encoding(file_path)

if __name__ == '__main__':
    main() 