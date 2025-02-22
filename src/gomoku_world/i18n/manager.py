"""
Internationalization manager
国际化管理器
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from .constants import (
    LANGUAGE_CODES, REGION_CODES, DEFAULT_LANGUAGE,
    DEFAULT_REGION, FALLBACK_LANGUAGE, DATE_FORMATS,
    TIME_FORMATS, NUMBER_FORMATS, FONT_FAMILIES
)
from ..utils.logger import get_logger

logger = get_logger(__name__)

class I18nManager:
    """
    Internationalization manager class
    国际化管理器类
    """
    
    def __init__(self):
        """Initialize i18n manager"""
        self._language = DEFAULT_LANGUAGE
        self._region = DEFAULT_REGION
        self._translations: Dict[str, Dict[str, Any]] = {}
        self._resources_dir = Path(__file__).parent.parent.parent.parent / "resources" / "i18n"
        self._resources_dir.mkdir(parents=True, exist_ok=True)
        logger.info("I18n manager initialized")
        
    def load_translations(self):
        """Load all translation files"""
        try:
            # Load base language
            self._load_language(self._language)
            
            # Load region-specific translations if available
            region_code = f"{self._language}-{self._region}"
            self._load_language(region_code)
            
            logger.info(f"Loaded translations for {self._language} ({self._region})")
        except Exception as e:
            logger.error(f"Failed to load translations: {e}")
            
    def _load_language(self, lang_code: str):
        """
        Load translations for a specific language code
        
        Args:
            lang_code: Language code (e.g., 'en', 'zh-CN')
        """
        lang_dir = self._resources_dir / lang_code
        if not lang_dir.exists():
            logger.warning(f"No translations found for {lang_code}")
            return
            
        for file_path in lang_dir.glob("*.json"):
            try:
                category = file_path.stem
                with open(file_path, "r", encoding="utf-8") as f:
                    translations = json.load(f)
                    
                if category not in self._translations:
                    self._translations[category] = {}
                    
                self._translations[category].update(translations)
                logger.debug(f"Loaded {category} translations for {lang_code}")
            except Exception as e:
                logger.error(f"Failed to load {file_path}: {e}")
                
    def set_language(self, language: str, region: Optional[str] = None):
        """
        Set current language and region
        
        Args:
            language: Language code
            region: Optional region code
        """
        if language not in LANGUAGE_CODES:
            raise ValueError(f"Unsupported language: {language}")
            
        self._language = language
        self._region = region or DEFAULT_REGION
        self.load_translations()
        
    def get_text(self, key: str, category: str = "common", **kwargs) -> str:
        """
        Get translated text
        
        Args:
            key: Translation key
            category: Resource category
            **kwargs: Format arguments
            
        Returns:
            str: Translated text
        """
        try:
            if category in self._translations and key in self._translations[category]:
                text = self._translations[category][key]
            else:
                # Fallback to English
                self._load_language(FALLBACK_LANGUAGE)
                text = self._translations.get(category, {}).get(key, key)
                
            return text.format(**kwargs) if kwargs else text
        except Exception as e:
            logger.error(f"Failed to get translation for {key}: {e}")
            return key
            
    def format_date(self, date: datetime) -> str:
        """Format date according to current locale"""
        date_format = DATE_FORMATS.get(self._language, DATE_FORMATS[DEFAULT_LANGUAGE])
        return date.strftime(date_format)
        
    def format_time(self, time: datetime) -> str:
        """Format time according to current locale"""
        time_format = TIME_FORMATS.get(self._language, TIME_FORMATS[DEFAULT_LANGUAGE])
        return time.strftime(time_format)
        
    def format_number(self, number: float) -> str:
        """Format number according to current locale"""
        formats = NUMBER_FORMATS.get(self._language, NUMBER_FORMATS[DEFAULT_LANGUAGE])
        return f"{number:,}".replace(",", formats["thousands"]).replace(".", formats["decimal"])
        
    def get_font_family(self) -> str:
        """Get appropriate font family for current language"""
        char_set = CHAR_SETS.get(self._language, "latin")
        return ", ".join(FONT_FAMILIES[char_set])
        
    @property
    def current_language(self) -> str:
        """Get current language code"""
        return self._language
        
    @property
    def current_region(self) -> str:
        """Get current region code"""
        return self._region
        
    @property
    def available_languages(self) -> Dict[str, Dict[str, str]]:
        """Get available languages"""
        return LANGUAGE_CODES

# Create global i18n manager instance
i18n_manager = I18nManager() 