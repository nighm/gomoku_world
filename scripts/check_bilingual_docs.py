#!/usr/bin/env python
"""
Script to check bilingual documentation requirements.

检查双语文档要求的脚本。
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple

def check_docstring(content: str) -> Tuple[bool, List[str]]:
    """
    Check if docstrings contain both English and Chinese text.
    
    检查文档字符串是否同时包含英文和中文文本。
    """
    issues = []
    docstring_pattern = r'"""[\s\S]*?"""'
    docstrings = re.findall(docstring_pattern, content)
    
    for docstring in docstrings:
        has_english = bool(re.search(r'[a-zA-Z]{3,}', docstring))
        has_chinese = bool(re.search(r'[\u4e00-\u9fff]', docstring))
        
        if not (has_english and has_chinese):
            issues.append(f"Docstring missing {'English' if not has_english else 'Chinese'}")
    
    return len(issues) == 0, issues

def check_comments(content: str) -> Tuple[bool, List[str]]:
    """
    Check if comments follow bilingual format.
    
    检查注释是否遵循双语格式。
    """
    issues = []
    comment_lines = re.findall(r'#.*$', content, re.MULTILINE)
    
    for line in comment_lines:
        if len(line) > 3:  # Ignore empty comments
            has_english = bool(re.search(r'[a-zA-Z]{3,}', line))
            has_chinese = bool(re.search(r'[\u4e00-\u9fff]', line))
            
            if not (has_english and has_chinese) and not line.strip('#').strip().startswith('noqa'):
                issues.append(f"Comment missing {'English' if not has_english else 'Chinese'}: {line}")
    
    return len(issues) == 0, issues

def check_markdown(content: str) -> Tuple[bool, List[str]]:
    """
    Check if markdown headers and content are bilingual.
    
    检查 Markdown 标题和内容是否双语。
    """
    issues = []
    header_pattern = r'^#{1,6}\s+.*$'
    headers = re.findall(header_pattern, content, re.MULTILINE)
    
    for header in headers:
        has_english = bool(re.search(r'[a-zA-Z]{3,}', header))
        has_chinese = bool(re.search(r'[\u4e00-\u9fff]', header))
        
        if not (has_english and has_chinese):
            issues.append(f"Header missing {'English' if not has_english else 'Chinese'}: {header}")
    
    return len(issues) == 0, issues

def check_file(file_path: Path) -> Tuple[bool, List[str]]:
    """
    Check a file for bilingual documentation requirements.
    
    检查文件是否符合双语文档要求。
    """
    content = file_path.read_text(encoding='utf-8')
    issues = []
    success = True
    
    if file_path.suffix == '.py':
        docstring_success, docstring_issues = check_docstring(content)
        comment_success, comment_issues = check_comments(content)
        success = docstring_success and comment_success
        issues.extend(docstring_issues)
        issues.extend(comment_issues)
    elif file_path.suffix == '.md':
        markdown_success, markdown_issues = check_markdown(content)
        success = markdown_success
        issues.extend(markdown_issues)
    
    return success, issues

def main():
    """
    Main function to check files.
    
    检查文件的主函数。
    """
    success = True
    for file_path in sys.argv[1:]:
        path = Path(file_path)
        if not path.exists():
            print(f"File not found: {file_path}")
            continue
            
        file_success, issues = check_file(path)
        success = success and file_success
        
        if issues:
            print(f"\nIssues in {file_path}:")
            for issue in issues:
                print(f"  - {issue}")
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main() 