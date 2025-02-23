"""
YAML translation loader implementation.

YAML翻译加载器实现。
"""

import os
import logging
from pathlib import Path
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
        Initialize YAML loader.
        初始化YAML加载器。

        Args:
            base_dir: Base directory for translation files
                     翻译文件的基础目录
        """
        self.base_dir = Path(base_dir)
        
    def load(self, path: Path) -> Dict[str, Any]:
        """
        Load translations from YAML file.
        从YAML文件加载翻译。

        Args:
            path: Path to translation file
                 翻译文件路径
                 
        Returns:
            Dict[str, Any]: Dictionary of translations
                           翻译字典
                           
        Raises:
            TranslationFileNotFoundError: If file doesn't exist
                                        如果文件不存在
            InvalidTranslationFormatError: If file format is invalid
                                         如果文件格式无效
            InvalidTranslationValueError: If translation value is invalid
                                        如果翻译值无效
        """
        if not path.exists():
            raise TranslationFileNotFoundError(str(path), "yaml")
            
        try:
            with path.open("r", encoding="utf-8") as f:
                translations = yaml.safe_load(f)
                
            if not isinstance(translations, dict):
                raise InvalidTranslationFormatError(
                    str(path),
                    "Root element must be a dictionary"
                )
                
            self._validate_translations(translations, path)
            return translations
            
        except yaml.YAMLError as e:
            raise InvalidTranslationFormatError(str(path), str(e))
            
        except Exception as e:
            logger.error(f"Error loading translations from {path}: {e}")
            raise
    
    def _validate_translations(self, translations: Dict[str, Any], path: Path) -> None:
        """
        Validate translation values.
        验证翻译值。
        
        Args:
            translations: Dictionary of translations
                        翻译字典
            path: Path to translation file
                 翻译文件路径
                 
        Raises:
            InvalidTranslationValueError: If translation value is invalid
                                        如果翻译值无效
        """
        for key, value in translations.items():
            if isinstance(value, dict):
                self._validate_translations(value, path)
            elif not isinstance(value, str):
                raise InvalidTranslationValueError(
                    key,
                    str(value),
                    "Translation value must be a string"
                )
        
    def save(self, language: str, translations: Dict[str, str]) -> None:
        """
        Save translations to YAML file.
        将翻译保存到YAML文件。
        
        Args:
            language: Language code
                     语言代码
            translations: Dictionary of translations
                        翻译字典
        """
        file_path = self.base_dir / f"{language}.yaml"
        
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(
                    translations,
                    f,
                    allow_unicode=True,
                    default_flow_style=False,
                    sort_keys=False
                )
        except Exception as e:
            logger.error(f"Error saving translations to {file_path}: {e}")
            raise 