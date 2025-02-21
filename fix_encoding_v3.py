import os
import sys
from pathlib import Path
import codecs
import chardet

def detect_encoding(file_path):
    """Detect the encoding of a file using chardet"""
    with open(file_path, 'rb') as f:
        raw = f.read()
    result = chardet.detect(raw)
    return result['encoding']

def fix_file_encoding(file_path):
    try:
        # First detect the encoding
        detected_encoding = detect_encoding(file_path)
        print(f"Detected encoding for {file_path}: {detected_encoding}")
        
        # Read the file content in binary mode
        with open(file_path, 'rb') as f:
            content = f.read()
            
        # Try to decode with the detected encoding first
        try:
            decoded_content = content.decode(detected_encoding) if detected_encoding else None
        except (UnicodeDecodeError, TypeError):
            decoded_content = None
            
        # If that fails, try other encodings
        if decoded_content is None:
            encodings = ['utf-8-sig', 'utf-8', 'gbk', 'gb2312', 'gb18030', 'big5', 'cp936']
            for encoding in encodings:
                try:
                    decoded_content = content.decode(encoding)
                    print(f"Successfully decoded with {encoding}")
                    break
                except UnicodeDecodeError:
                    continue
                    
        if decoded_content is None:
            print(f"Failed to decode {file_path} with any encoding")
            return
            
        # Clean up the content
        # Remove BOM if present
        if decoded_content.startswith('\ufeff'):
            decoded_content = decoded_content[1:]
            
        # Normalize line endings
        decoded_content = decoded_content.replace('\r\n', '\n').replace('\r', '\n')
        
        # Replace problematic characters
        replacements = {
            '\u20ac': '',  # Euro sign
            '\ufffd': '',  # Replacement character
        }
        for old, new in replacements.items():
            decoded_content = decoded_content.replace(old, new)
            
        # Write back with UTF-8 encoding
        with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(decoded_content)
            
        print(f"Successfully processed {file_path}")
            
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