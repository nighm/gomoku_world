"""
Translation management tool.

翻译管理工具。

This tool provides functionality for:
- Checking translation completeness
- Finding missing translations
- Validating translation files
- Generating translation templates

本工具提供以下功能：
- 检查翻译完整性
- 查找缺失的翻译
- 验证翻译文件
- 生成翻译模板
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Dict, Set, List

from ..loaders import JsonLoader
from ..exceptions import TranslationFileError
from ...utils.logger import setup_logging

logger = logging.getLogger(__name__)

class TranslationManager:
    """
    Translation file management tool.
    翻译文件管理工具。
    """
    
    def __init__(self, base_dir: str):
        """
        Initialize translation manager.
        初始化翻译管理器。
        
        Args:
            base_dir: Base directory containing translation files
                     包含翻译文件的基础目录
        """
        self.base_dir = Path(base_dir)
        self.loader = JsonLoader(base_dir)
        
    def check_completeness(self, source_lang: str = "en") -> Dict[str, List[str]]:
        """
        Check translation completeness against source language.
        根据源语言检查翻译完整性。
        
        Args:
            source_lang: Source language code
                        源语言代码
                        
        Returns:
            Dictionary of missing keys by language
            按语言分类的缺失键字典
        """
        # Load source language translations
        source_trans = self.loader.load(source_lang)
        source_keys = set(self._flatten_dict(source_trans))
        
        # Check each language
        missing = {}
        for lang_file in self.base_dir.glob("*.json"):
            lang = lang_file.stem
            if lang != source_lang:
                trans = self.loader.load(lang)
                lang_keys = set(self._flatten_dict(trans))
                missing_keys = source_keys - lang_keys
                if missing_keys:
                    missing[lang] = sorted(missing_keys)
                    
        return missing
        
    def validate_files(self) -> Dict[str, List[str]]:
        """
        Validate all translation files.
        验证所有翻译文件。
        
        Returns:
            Dictionary of validation errors by file
            按文件分类的验证错误字典
        """
        errors = {}
        for lang_file in self.base_dir.glob("*.json"):
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Validate structure
                if not isinstance(data, dict):
                    errors[lang_file.name] = ["Root must be a dictionary"]
                    continue
                    
                # Validate values
                invalid = []
                for key, value in self._flatten_dict(data).items():
                    if not isinstance(value, str):
                        invalid.append(f"Non-string value for key: {key}")
                        
                if invalid:
                    errors[lang_file.name] = invalid
                    
            except json.JSONDecodeError as e:
                errors[lang_file.name] = [f"Invalid JSON: {e}"]
            except Exception as e:
                errors[lang_file.name] = [f"Error: {e}"]
                
        return errors
        
    def generate_template(self, output_file: str):
        """
        Generate translation template from existing files.
        从现有文件生成翻译模板。
        
        Args:
            output_file: Output template file path
                        输出模板文件路径
        """
        # Collect all keys
        all_keys = set()
        for lang_file in self.base_dir.glob("*.json"):
            trans = self.loader.load(lang_file.stem)
            all_keys.update(self._flatten_dict(trans).keys())
            
        # Create template
        template = {}
        for key in sorted(all_keys):
            parts = key.split('.')
            current = template
            for part in parts[:-1]:
                current = current.setdefault(part, {})
            current[parts[-1]] = ""
            
        # Save template
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=4, ensure_ascii=False)
            
    def _flatten_dict(self, d: Dict, prefix: str = "") -> Dict[str, str]:
        """
        Flatten nested dictionary with dot notation.
        使用点号展平嵌套字典。
        """
        items = {}
        for k, v in d.items():
            key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, dict):
                items.update(self._flatten_dict(v, key))
            else:
                items[key] = v
        return items

def main():
    """
    Main entry point.
    主入口点。
    """
    parser = argparse.ArgumentParser(description="Translation management tool")
    parser.add_argument('--dir', required=True, help="Translation directory")
    parser.add_argument('--action', required=True,
                       choices=['check', 'validate', 'template'],
                       help="Action to perform")
    parser.add_argument('--source-lang', default="en",
                       help="Source language for completeness check")
    parser.add_argument('--output', help="Output file for template")
    
    args = parser.parse_args()
    
    try:
        setup_logging()
        manager = TranslationManager(args.dir)
        
        if args.action == 'check':
            missing = manager.check_completeness(args.source_lang)
            if missing:
                for lang, keys in missing.items():
                    print(f"\nMissing translations in {lang}:")
                    for key in keys:
                        print(f"  - {key}")
            else:
                print("All translations are complete!")
                
        elif args.action == 'validate':
            errors = manager.validate_files()
            if errors:
                for file, error_list in errors.items():
                    print(f"\nErrors in {file}:")
                    for error in error_list:
                        print(f"  - {error}")
            else:
                print("All files are valid!")
                
        elif args.action == 'template':
            if not args.output:
                parser.error("--output required for template action")
            manager.generate_template(args.output)
            print(f"Template generated: {args.output}")
            
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 