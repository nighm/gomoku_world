import os
import sys
from pathlib import Path

def fix_file_encoding(file_path):
    try:
        # First try to read with UTF-8
        with open(file_path, 'rb') as f:
            content = f.read()
            
        # Try to decode with different encodings
        encodings = ['utf-8-sig', 'utf-8', 'gbk', 'gb2312', 'gb18030']
        decoded_content = None
        used_encoding = None
        
        for encoding in encodings:
            try:
                decoded_content = content.decode(encoding)
                used_encoding = encoding
                break
            except UnicodeDecodeError:
                continue
        
        if decoded_content is None:
            print(f"Failed to decode {file_path} with any encoding")
            return
            
        # Remove any BOM and ensure proper line endings
        if decoded_content.startswith('\ufeff'):
            decoded_content = decoded_content[1:]
            
        # Normalize line endings to \n
        decoded_content = decoded_content.replace('\r\n', '\n').replace('\r', '\n')
        
        # Write back with UTF-8 encoding (without BOM)
        with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(decoded_content)
            
        print(f"Successfully processed {file_path} (original encoding: {used_encoding})")
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    # Process all Python files in the project
    for root, dirs, files in os.walk('.'):
        if '.venv' in dirs:  # Skip virtual environment directory
            dirs.remove('.venv')
        if '.git' in dirs:   # Skip git directory
            dirs.remove('.git')
            
        for file in files:
            if file.endswith('.py'):
                file_path = Path(root) / file
                fix_file_encoding(file_path)

if __name__ == '__main__':
    main() 