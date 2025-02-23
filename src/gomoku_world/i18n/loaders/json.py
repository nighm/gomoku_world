"""
JSON translation loader implementation.

JSON翻译加载器实现。

This module provides a JSON-based translation loader with:
- Automatic directory creation
- UTF-8 encoding support
- Validation of translation values
- Pretty-printed JSON output

本模块提供基于JSON的翻译加载器，具有：
- 自动创建目录
- UTF-8编码支持
- 翻译值验证
- 美化的JSON输出
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, Optional, Any, Union

from ..base import TranslationLoader, TranslationDict, LanguageCode
from ..exceptions import TranslationFileError, ValidationError

logger = logging.getLogger(__name__)

class JsonLoader(TranslationLoader):
    """
    Load translations from JSON files.
    从JSON文件加载翻译。
    """
    
    def __init__(self, base_dir: str):
        """
        Initialize JSON loader.
        初始化JSON加载器。
        
        Args:
            base_dir (str): Base directory containing translation files
                          包含翻译文件的基础目录
        """
        self._base_dir = Path(base_dir)
        
    def load(self, language: LanguageCode) -> TranslationDict:
        """
        Load translations for a language from JSON file.
        从JSON文件加载指定语言的翻译。
        
        Args:
            language (LanguageCode): Language code to load
                                   要加载的语言代码
                                   
        Returns:
            TranslationDict: Dictionary of translations
                           翻译字典
                           
        Raises:
            TranslationFileError: If file cannot be read or has invalid format
                                如果文件无法读取或格式无效
            ValidationError: If translation values are invalid
                           如果翻译值无效
        """
        file_path = self._base_dir / f"{language}.json"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                translations = json.load(f)
        except FileNotFoundError:
            raise TranslationFileError(str(file_path), "File not found")
        except json.JSONDecodeError as e:
            raise TranslationFileError(str(file_path), f"Invalid JSON: {e}")
        except Exception as e:
            raise TranslationFileError(str(file_path), str(e))
            
        if not isinstance(translations, dict):
            raise ValidationError(
                f"Invalid translation format in {language}",
                {"error": "Root must be a dictionary"}
            )
            
        self._validate_translations(translations, language)
        return translations
    
    def _validate_translations(self, translations: Dict[str, Any], language: str) -> None:
        """
        Validate translation values recursively.
        递归验证翻译值。
        
        Args:
            translations (Dict[str, Any]): Dictionary of translations
                                         翻译字典
            language (str): Language code being validated
                          正在验证的语言代码
                          
        Raises:
            ValidationError: If translation values are invalid
                           如果翻译值无效
        """
        invalid_entries = {}
        
        def validate_value(value: Any, path: str) -> None:
            if isinstance(value, dict):
                for key, val in value.items():
                    validate_value(val, f"{path}.{key}" if path else key)
            elif not isinstance(value, str):
                invalid_entries[path] = type(value).__name__
        
        for key, value in translations.items():
            validate_value(value, key)
            
        if invalid_entries:
            raise ValidationError(
                f"Invalid translation values in {language}",
                {"invalid_entries": invalid_entries}
            )
    
    def save(self, language: LanguageCode, translations: TranslationDict) -> None:
        """
        Save translations for a language to JSON file.
        将指定语言的翻译保存到JSON文件。
        
        Args:
            language (LanguageCode): Language code to save
                                   要保存的语言代码
            translations (TranslationDict): Dictionary of translations
                                         翻译字典
                                         
        Raises:
            TranslationFileError: If file cannot be written
                                如果文件无法写入
        """
        os.makedirs(self._base_dir, exist_ok=True)
        file_path = self._base_dir / f"{language}.json"
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(
                    translations,
                    f,
                    ensure_ascii=False,
                    indent=4,
                    sort_keys=True
                )
        except Exception as e:
            raise TranslationFileError(str(file_path), str(e)) 