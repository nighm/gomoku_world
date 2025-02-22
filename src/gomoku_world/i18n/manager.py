"""
Internationalization manager implementation
国际化管理器实现
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import requests
from urllib.parse import urljoin
import locale
import socket
from threading import Lock

from .constants import (
    LANGUAGE_CODES, REGION_CODES, DEFAULT_LANGUAGE,
    DEFAULT_REGION, FALLBACK_LANGUAGE, DATE_FORMATS,
    TIME_FORMATS, NUMBER_FORMATS, FONT_FAMILIES
)
from ..utils.logger import get_logger
from ..utils.network import network_monitor
from ..config.settings import (
    TRANSLATION_SERVICE_URL,
    TRANSLATION_API_KEY,
    TRANSLATION_CACHE_DIR,
    TRANSLATION_TIMEOUT
)

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
        self._lock = Lock()
        self._initialized = False
        
        # Create cache directory
        os.makedirs(TRANSLATION_CACHE_DIR, exist_ok=True)
        
        # Register network callback
        network_monitor.add_callback(self._on_network_status_change)
        
    def _on_network_status_change(self, is_online: bool):
        """Handle network status change"""
        if is_online:
            logger.info("Network connection restored, reloading translations")
            self.load_translations()
            
    def load_translations(self):
        """Load translations based on network status"""
        with self._lock:
            # Try loading from cache first
            if self._load_from_cache():
                logger.info("Translations loaded from cache")
                return
                
            # If online, try loading from service
            if network_monitor.is_online():
                if self._load_from_service():
                    logger.info("Translations loaded from service")
                    return
                    
            # Fallback to bundled translations
            self._load_bundled_translations()
            logger.info("Using bundled translations")
            
    def _load_from_cache(self) -> bool:
        """Load translations from cache"""
        try:
            cache_file = TRANSLATION_CACHE_DIR / f"{self._language}_{self._region}.json"
            if cache_file.exists():
                with open(cache_file, "r", encoding="utf-8") as f:
                    self._translations = json.load(f)
                return True
        except Exception as e:
            logger.error(f"Failed to load translations from cache: {e}")
        return False
        
    def _load_from_service(self) -> bool:
        """Load translations from remote service"""
        try:
            url = urljoin(TRANSLATION_SERVICE_URL, f"/api/translations/{self._language}/{self._region}")
            headers = {"Authorization": f"Bearer {TRANSLATION_API_KEY}"} if TRANSLATION_API_KEY else {}
            
            response = requests.get(
                url,
                headers=headers,
                timeout=TRANSLATION_TIMEOUT
            )
            
            if response.status_code == 200:
                translations = response.json()
                self._translations = translations
                self._save_to_cache(translations)
                return True
                
            logger.warning(f"Failed to load translations from service: {response.status_code}")
            
        except requests.RequestException as e:
            logger.error(f"Error loading translations from service: {e}")
            
        return False
        
    def _save_to_cache(self, translations: Dict):
        """Save translations to cache"""
        try:
            cache_file = TRANSLATION_CACHE_DIR / f"{self._language}_{self._region}.json"
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(translations, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Failed to save translations to cache: {e}")
            
    def _load_bundled_translations(self):
        """Load bundled translations"""
        try:
            base_dir = Path(__file__).parent.parent.parent.parent
            file_path = base_dir / "resources" / "i18n" / self._language / "common.json"
            
            with open(file_path, "r", encoding="utf-8") as f:
                self._translations = json.load(f)
                
        except Exception as e:
            logger.error(f"Failed to load bundled translations: {e}")
            self._translations = {}
            
    def set_language(self, language: str, region: Optional[str] = None, force_reload: bool = False):
        """Set current language"""
        if language not in LANGUAGE_CODES:
            logger.error(f"Unsupported language: {language}")
            return
            
        if region and region not in REGION_CODES:
            logger.error(f"Unsupported region: {region}")
            return
            
        self._language = language
        self._region = region or DEFAULT_REGION
        
        if force_reload or not self._translations:
            self.load_translations()
            
    def get_text(self, key: str, category: str = "common", **kwargs) -> str:
        """Get translated text"""
        try:
            if not self._translations:
                self.load_translations()
                
            text = self._translations.get(key, key)
            return text.format(**kwargs) if kwargs else text
            
        except Exception as e:
            logger.error(f"Error getting translation for {key}: {e}")
            return key
            
    def format_date(self, date: datetime) -> str:
        """Format date according to current locale"""
        return date.strftime(DATE_FORMATS.get(self._language, "%Y-%m-%d"))
        
    def format_time(self, time: datetime) -> str:
        """Format time according to current locale"""
        return time.strftime(TIME_FORMATS.get(self._language, "%H:%M:%S"))
        
    def format_number(self, number: float) -> str:
        """Format number according to current locale"""
        formats = NUMBER_FORMATS.get(self._language, {"decimal": ".", "thousands": ","})
        return f"{number:,.2f}".replace(",", formats["thousands"]).replace(".", formats["decimal"])
        
    def get_font_family(self) -> str:
        """Get appropriate font family for current language"""
        char_set = "cjk" if self._language in ["zh", "ja", "ko"] else "latin"
        return FONT_FAMILIES[char_set][0]
        
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
        
    def detect_system_language(self) -> str:
        """Detect system language"""
        try:
            # Get system locale
            system_locale, _ = locale.getdefaultlocale()
            
            if system_locale:
                # Extract language code
                lang_code = system_locale.split("_")[0].lower()
                
                # Check if supported
                if lang_code in LANGUAGE_CODES:
                    return lang_code
                    
            logger.warning(f"Unsupported system language: {system_locale}")
            
        except Exception as e:
            logger.error(f"Error detecting system language: {e}")
            
        return DEFAULT_LANGUAGE
        
    def initialize(self):
        """Initialize the manager"""
        if self._initialized:
            return
            
        try:
            # Detect and set system language
            detected_lang = self.detect_system_language()
            self.set_language(detected_lang)
            
            # Load translations
            self.load_translations()
            
            self._initialized = True
            logger.info(f"I18n manager initialized with language: {self._language}")
            
        except Exception as e:
            logger.error(f"Failed to initialize i18n manager: {e}")
            # Use defaults
            self._language = DEFAULT_LANGUAGE
            self._region = DEFAULT_REGION

# Create global i18n manager instance
i18n_manager = I18nManager() 