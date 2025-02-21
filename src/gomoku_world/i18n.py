"""
Internationalization module
"""

from typing import Dict, Any
from .utils.resources import resource_manager

class I18n:
    """
    Internationalization manager class
    """
    
    def __init__(self):
        """Initialize i18n manager"""
        self._language = "en"
        self._texts = resource_manager._texts
    
    def get_text(self, key: str) -> str:
        """
        Get text by key
        
        Args:
            key: Text key
            
        Returns:
            str: Text value
        """
        return resource_manager.get_text(key)
    
    def get_bilingual(self, key: str) -> str:
        """
        Get bilingual text by key
        
        Args:
            key: Text key
            
        Returns:
            str: Text value
        """
        return self.get_text(key)
    
    def set_language(self, language: str):
        """
        Set current language
        
        Args:
            language: Language code
        """
        self._language = language

# Create global i18n instance
i18n = I18n()

__all__ = ['i18n'] 