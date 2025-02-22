"""
YAML translation loader implementation.

YAML翻译加载器实现。
"""

import os
import logging
from typing import Dict, Any

import yaml

from ..base import TranslationLoader
from ..exceptions import (
    TranslationFileNotFoundError,
    InvalidTranslationFormatError,
    InvalidTranslationValueError
)

logger = logging.getLogger(__name__)


class YamlLoader(TranslationLoader):
    """
    YAML translation loader.
    
    YAML翻译加载器。
    """
    
    def __init__(self, base_dir: str):
        """
        Initialize the YAML loader.
        
        初始化YAML加载器。

        Args:
            base_dir: Base directory containing translation files
                     包含翻译文件的基础目录
        """
        self.base_dir = base_dir
        
    def load(self, language: str) -> Dict[str, str]:
        """
        Load translations for a language from a YAML file.
        
        从YAML文件加载指定语言的翻译。

        Args:
            language: Language code (e.g. 'en', 'zh-CN')
                     语言代码（如'en'、'zh-CN'）

        Returns:
            Dictionary of translation strings
            翻译字符串字典

        Raises:
            TranslationFileNotFoundError: If translation file not found
                                        如果翻译文件未找到
            InvalidTranslationFormatError: If YAML format is invalid
                                         如果YAML格式无效
            InvalidTranslationValueError: If translation values are not strings
                                        如果翻译值不是字符串
        """
        file_path = os.path.join(self.base_dir, f"{language}.yaml")
        
        if not os.path.exists(file_path):
            raise TranslationFileNotFoundError(
                f"Translation file not found: {file_path}"
            )
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                translations = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise InvalidTranslationFormatError(
                f"Invalid YAML format in {file_path}: {e}"
            )
            
        if not isinstance(translations, dict):
            raise InvalidTranslationFormatError(
                f"Invalid translation format in {file_path}: "
                "root must be a dictionary"
            )
            
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
        Save translations for a language to a YAML file.
        
        将指定语言的翻译保存到YAML文件。

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
        
        file_path = os.path.join(self.base_dir, f"{language}.yaml")
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(
                    translations,
                    f,
                    allow_unicode=True,
                    default_flow_style=False
                )
        except Exception as e:
            logger.error(f"Failed to save translations to {file_path}: {e}")
            raise 