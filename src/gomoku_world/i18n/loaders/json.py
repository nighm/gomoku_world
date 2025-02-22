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
from typing import Dict, Optional, Any

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
            language (LanguageCode): Language code (e.g. 'en', 'zh-CN')
                                   语言代码（如'en'、'zh-CN'）
                          
        Returns:
            TranslationDict: Dictionary of translation strings
                           翻译字符串字典
                           
        Raises:
            TranslationFileError: If file cannot be read or is invalid
                                如果文件无法读取或无效
            ValidationError: If translations are invalid
                           如果翻译无效
        """
        file_path = self._get_file_path(language)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                translations = json.load(f)
        except FileNotFoundError:
            raise TranslationFileError(str(file_path), "File not found")
        except json.JSONDecodeError as e:
            raise TranslationFileError(str(file_path), f"Invalid JSON: {e}")
        except Exception as e:
            raise TranslationFileError(str(file_path), str(e))
            
        # Validate translations
        self._validate_translations(translations, language)
            
        return translations
        
    def save(self, language: LanguageCode, translations: TranslationDict) -> None:
        """
        Save translations for a language to JSON file.
        将指定语言的翻译保存到JSON文件。
        
        Args:
            language (LanguageCode): Language code (e.g. 'en', 'zh-CN')
                                   语言代码（如'en'、'zh-CN'）
            translations (TranslationDict): Dictionary of translation strings
                                         翻译字符串字典
                                         
        Raises:
            TranslationFileError: If file cannot be written
                                如果文件无法写入
            ValidationError: If translations are invalid
                           如果翻译无效
        """
        # Validate translations before saving
        self._validate_translations(translations, language)
        
        file_path = self._get_file_path(language)
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(translations, f, ensure_ascii=False, indent=2)
                
            logger.info(f"Saved translations for language: {language}")
            
        except Exception as e:
            raise TranslationFileError(str(file_path), f"Failed to save: {e}")
            
    def _get_file_path(self, language: LanguageCode) -> Path:
        """
        Get file path for a language.
        获取指定语言的文件路径。
        
        Args:
            language (LanguageCode): Language code
                                   语言代码
                                   
        Returns:
            Path: Path to translation file
                 翻译文件路径
        """
        return self._base_dir / f"{language}.json"
        
    def _validate_translations(self, translations: Dict[str, Any], language: LanguageCode) -> None:
        """
        Validate translation dictionary.
        验证翻译字典。
        
        Args:
            translations (Dict[str, Any]): Translations to validate
                                         要验证的翻译
            language (LanguageCode): Language code
                                   语言代码
                                   
        Raises:
            ValidationError: If translations are invalid
                           如果翻译无效
        """
        if not isinstance(translations, dict):
            raise ValidationError(
                f"Translations for {language} must be a dictionary",
                {"type": type(translations).__name__}
            )
            
        invalid = {k: type(v).__name__ for k, v in translations.items() 
                  if not isinstance(v, str)}
                  
        if invalid:
            raise ValidationError(
                f"Invalid translation values in {language}",
                {"invalid_entries": invalid}
            ) 