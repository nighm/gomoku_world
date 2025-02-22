"""
INI translation loader implementation.

INI翻译加载器实现。
"""

import os
import logging
from configparser import ConfigParser
from typing import Dict, Any

from ..base import TranslationLoader
from ..exceptions import (
    TranslationFileNotFoundError,
    InvalidTranslationFormatError,
    InvalidTranslationValueError
)

logger = logging.getLogger(__name__)


class IniLoader(TranslationLoader):
    """
    INI translation loader.
    
    INI翻译加载器。
    """
    
    def __init__(self, base_dir: str, section: str = "translations"):
        """
        Initialize the INI loader.
        
        初始化INI加载器。

        Args:
            base_dir: Base directory containing translation files
                     包含翻译文件的基础目录
            section: INI section name containing translations
                    包含翻译的INI节名称
        """
        self.base_dir = base_dir
        self.section = section
        
    def load(self, language: str) -> Dict[str, str]:
        """
        Load translations for a language from an INI file.
        
        从INI文件加载指定语言的翻译。

        Args:
            language: Language code (e.g. 'en', 'zh-CN')
                     语言代码（如'en'、'zh-CN'）

        Returns:
            Dictionary of translation strings
            翻译字符串字典

        Raises:
            TranslationFileNotFoundError: If translation file not found
                                        如果翻译文件未找到
            InvalidTranslationFormatError: If INI format is invalid
                                         如果INI格式无效
            InvalidTranslationValueError: If translation values are not strings
                                        如果翻译值不是字符串
        """
        file_path = os.path.join(self.base_dir, f"{language}.ini")
        
        if not os.path.exists(file_path):
            raise TranslationFileNotFoundError(
                f"Translation file not found: {file_path}"
            )
            
        parser = ConfigParser()
        try:
            parser.read(file_path, encoding='utf-8')
        except Exception as e:
            raise InvalidTranslationFormatError(
                f"Invalid INI format in {file_path}: {e}"
            )
            
        if not parser.has_section(self.section):
            raise InvalidTranslationFormatError(
                f"Missing required section '{self.section}' in {file_path}"
            )
            
        translations = dict(parser[self.section])
        
        # Validate all values are strings
        invalid_keys = [
            key for key, value in translations.items()
            if not isinstance(value, str)
        ]
        if invalid_keys:
            raise InvalidTranslationValueError(
                f"Non-string translation values found for keys: {invalid_keys}"
            )
            
        return translations
        
    def save(self, language: str, translations: Dict[str, str]) -> None:
        """
        Save translations for a language to an INI file.
        
        将指定语言的翻译保存到INI文件。

        Args:
            language: Language code (e.g. 'en', 'zh-CN')
                     语言代码（如'en'、'zh-CN'）
            translations: Dictionary of translation strings
                        翻译字符串字典

        Raises:
            InvalidTranslationValueError: If translation values are not strings
                                        如果翻译值不是字符串
        """
        # Validate all values are strings
        invalid_keys = [
            key for key, value in translations.items()
            if not isinstance(value, str)
        ]
        if invalid_keys:
            raise InvalidTranslationValueError(
                f"Non-string translation values found for keys: {invalid_keys}"
            )
            
        # Create directory if it doesn't exist
        os.makedirs(self.base_dir, exist_ok=True)
        
        file_path = os.path.join(self.base_dir, f"{language}.ini")
        
        parser = ConfigParser()
        parser[self.section] = translations
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                parser.write(f)
        except Exception as e:
            logger.error(f"Failed to save translations to {file_path}: {e}")
            raise 