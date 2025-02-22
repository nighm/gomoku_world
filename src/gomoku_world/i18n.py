"""
Internationalization module
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path
from .utils.resources import resource_manager
from .utils.logger import get_logger

logger = get_logger(__name__)

class I18n:
    """
    Internationalization manager class
    """
    
    def __init__(self):
        """Initialize i18n manager"""
        self._language = "en"
        self._texts: Dict[str, Dict[str, str]] = {}
        self._cache: Dict[str, str] = {}
        self._initialized = False
        
        # Get the project root directory
        self._root_dir = Path(__file__).parent.parent.parent
        logger.info("Project root directory: %s", self._root_dir)
    
    def initialize(self):
        """Initialize the i18n system"""
        if self._initialized:
            return
        self._load_translations(self._language)
        self._initialized = True
        logger.info("I18n manager initialized with language: %s", self._language)
    
    def _load_translations(self, language: str):
        """Load translations for the specified language"""
        self._texts[language] = {}
        
        # Try different possible resource paths
        resource_paths = [
            self._root_dir / "resources" / "i18n" / language,  # Development path
            Path(__file__).parent / "resources" / "i18n" / language,  # Package path
        ]
        
        for resource_dir in resource_paths:
            logger.info("Trying resource directory: %s", resource_dir)
            if not resource_dir.exists():
                continue
                
            for file in resource_dir.glob("*.json"):
                category = file.stem
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        translations = json.load(f)
                        for key, value in translations.items():
                            full_key = f"{category}.{key}"
                            self._texts[language][full_key] = value
                    logger.info("Loaded translations from %s", file)
                except Exception as e:
                    logger.error("Failed to load translation file %s: %s", file, e)
            
            # If we found and loaded translations, we're done
            if self._texts[language]:
                logger.info("Successfully loaded translations from %s", resource_dir)
                return
                
        logger.warning("No translation files found for language: %s", language)
    
    def get_text(self, key: str) -> str:
        """
        Get text by key
        
        Args:
            key: Text key
            
        Returns:
            str: Text value
        """
        if not self._initialized:
            self.initialize()
            
        cache_key = f"{self._language}:{key}"
        if cache_key in self._cache:
            return self._cache[cache_key]
            
        if self._language in self._texts and key in self._texts[self._language]:
            text = self._texts[self._language][key]
            self._cache[cache_key] = text
            return text
            
        logger.warning("Translation not found for key: %s", key)
        return key
    
    def get_bilingual(self, key: str) -> str:
        """
        Get bilingual text by key
        
        Args:
            key: Text key
            
        Returns:
            str: Text value
        """
        text = self.get_text(key)
        if self._language != "en":
            en_text = self.get_text(key)
            if text != key:  # If translation exists
                return f"{text} / {en_text}"
        return text
    
    def set_language(self, language: str, force_reload: bool = False):
        """
        Set current language
        
        Args:
            language: Language code
            force_reload: Force reload translations
        """
        if language == self._language and not force_reload:
            return
            
        self._language = language
        if force_reload:
            self._texts = {}
            self._cache = {}
            self._initialized = False
        self.initialize()
        logger.info("Language changed to: %s", language)

# Create global i18n instance
i18n = I18n()

__all__ = ['i18n'] 