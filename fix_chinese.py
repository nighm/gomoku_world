import os
import sys
from pathlib import Path

def fix_chinese_encoding(file_path):
    try:
        # Try different encodings
        encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030']
        content = None
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print(f"Failed to decode {file_path} with any encoding")
            return
        
        # Write back with UTF-8 encoding
        with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
            
        print(f"Successfully processed {file_path}")
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    # Process all Python files in the project
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                file_path = Path(root) / file
                fix_chinese_encoding(file_path)

if __name__ == '__main__':
    main() 