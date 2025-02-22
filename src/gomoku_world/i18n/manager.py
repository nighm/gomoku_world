"""
Internationalization manager implementation
国际化管理器实现
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Set
from datetime import datetime
import requests
from urllib.parse import urljoin
import locale
import socket
from threading import Lock
import hashlib
import time

from .constants import (
    LANGUAGE_CODES, REGION_CODES, DEFAULT_LANGUAGE,
    DEFAULT_REGION, FALLBACK_LANGUAGE, DATE_FORMATS,
    TIME_FORMATS, NUMBER_FORMATS, FONT_FAMILIES
)
from ..utils.logger import get_logger
from ..utils.network import network_monitor
from ..utils.fonts import font_manager
from ..config.settings import (
    TRANSLATION_SERVICE_URL,
    TRANSLATION_API_KEY,
    TRANSLATION_CACHE_DIR,
    TRANSLATION_TIMEOUT,
    TRANSLATION_CACHE_TTL
)
from .validator import TranslationValidator

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
        self._cache_info: Dict[str, Dict[str, Any]] = {}
        self._stats: Dict[str, Dict[str, int]] = {}
        
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
            if self._is_cache_valid(self._language, self._region):
                cache_path = self._get_cache_path(self._language, self._region)
                try:
                    with open(cache_path, "r", encoding="utf-8") as f:
                        self._translations = json.load(f)
                    logger.info("Translations loaded from cache")
                    return
                except Exception as e:
                    logger.error(f"Failed to load translations from cache: {e}")
            
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
                self._save_to_cache(translations, self._language, self._region)
                return True
                
            logger.warning(f"Failed to load translations from service: {response.status_code}")
            
        except requests.RequestException as e:
            logger.error(f"Error loading translations from service: {e}")
            
        return False
        
    def _save_to_cache(self, translations: Dict, lang: str, region: str):
        """Save translations to cache with metadata"""
        try:
            # Save translations
            cache_path = self._get_cache_path(lang, region)
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(translations, f, ensure_ascii=False, indent=2)
                
            # Save metadata
            meta_path = self._get_cache_meta_path(lang, region)
            meta = {
                "timestamp": datetime.now().isoformat(),
                "version": self._get_translation_version(),
                "key_count": len(translations)
            }
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(meta, f, ensure_ascii=False, indent=2)
                
            self._cache_info[f"{lang}_{region}"] = meta
            
        except Exception as e:
            logger.error(f"Failed to save translations to cache: {e}")
            
    def _load_bundled_translations(self):
        """Load bundled translations"""
        try:
            base_dir = Path(__file__).parent.parent.parent.parent
            i18n_dir = base_dir / "resources" / "i18n" / self._language
            
            translations = {}
            for file_path in i18n_dir.glob("*.json"):
                with open(file_path, "r", encoding="utf-8") as f:
                    translations.update(json.load(f))
                    
            self._translations = translations
                
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
        """
        Get translated text from specified category
        从指定类别获取翻译文本
        
        Args:
            key: Translation key / 翻译键
            category: Resource category (common/game/ui/error/help/tutorial) / 资源类别
            **kwargs: Format arguments / 格式化参数
            
        Returns:
            str: Translated text / 翻译后的文本
        """
        try:
            if not self._translations:
                self.load_translations()
                
            # Get category-specific translations
            category_key = f"{category}.{key}" if not key.startswith(f"{category}.") else key
            
            # Try to get translation from specified category
            text = self._translations.get(category_key)
            
            # If not found, try without category prefix
            if text is None:
                text = self._translations.get(key, key)
                
            # Update usage statistics
            self._update_stats(self._language, category_key)
                
            return text.format(**kwargs) if kwargs and text != key else text
            
        except Exception as e:
            logger.error(f"Error getting translation for {key} in category {category}: {e}")
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
            # 获取当前locale设置
            current_locale = locale.getlocale()[0]
            if current_locale:
                # 提取语言代码（例如从'zh_CN'中提取'zh'）
                lang_code = current_locale.split('_')[0].lower()
                if lang_code in LANGUAGE_CODES:
                    return lang_code
            
            # 如果无法获取或不支持，返回默认语言
            return DEFAULT_LANGUAGE
            
        except Exception as e:
            logger.error(f"Failed to detect system language: {e}")
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

    def check_translations(self) -> Dict[str, Dict[str, bool]]:
        """
        Check translation completeness for all categories
        检查所有类别的翻译完整性
        
        Returns:
            Dict with categories and their completion status
            包含各类别及其完成状态的字典
        """
        try:
            base_dir = Path(__file__).parent.parent.parent.parent
            i18n_dir = base_dir / "resources" / "i18n"
            
            # Get all available languages
            languages = [d.name for d in i18n_dir.iterdir() if d.is_dir()]
            
            # Get all translation files
            categories = ["common", "game", "ui", "error", "help", "tutorial"]
            
            results = {}
            for lang in languages:
                results[lang] = {}
                for category in categories:
                    file_path = i18n_dir / lang / f"{category}.json"
                    results[lang][category] = file_path.exists()
                    
            return results
            
        except Exception as e:
            logger.error(f"Error checking translations: {e}")
            return {}

    def validate_translations(self) -> Dict[str, Any]:
        """
        Validate all translations
        验证所有翻译
        
        Returns:
            Dict with validation results
        """
        try:
            base_dir = Path(__file__).parent.parent.parent.parent
            i18n_dir = base_dir / "resources" / "i18n"
            
            # Validate each language directory
            results = {}
            for lang_dir in i18n_dir.iterdir():
                if lang_dir.is_dir():
                    results[lang_dir.name] = TranslationValidator.validate_directory(lang_dir)
                    
            # Check format consistency across languages
            all_files = []
            for lang_dir in i18n_dir.iterdir():
                if lang_dir.is_dir():
                    all_files.extend(lang_dir.glob("*.json"))
                    
            format_check = TranslationValidator.check_format_consistency(all_files)
            results["format_consistency"] = format_check
            
            # Compare translations with English base
            en_dir = i18n_dir / "en"
            if en_dir.exists():
                for lang_dir in i18n_dir.iterdir():
                    if lang_dir.is_dir() and lang_dir.name != "en":
                        comparison_results = {}
                        for file in en_dir.glob("*.json"):
                            target_file = lang_dir / file.name
                            if target_file.exists():
                                comparison_results[file.name] = TranslationValidator.compare_translations(file, target_file)
                        results[f"compare_{lang_dir.name}"] = comparison_results
                        
            return results
            
        except Exception as e:
            logger.error(f"Translation validation error: {e}")
            return {
                "valid": False,
                "error": str(e)
            }

    def _get_cache_path(self, lang: str, region: str) -> Path:
        """Get cache file path"""
        return Path(TRANSLATION_CACHE_DIR) / f"{lang}_{region}.json"
        
    def _get_cache_meta_path(self, lang: str, region: str) -> Path:
        """Get cache metadata file path"""
        return Path(TRANSLATION_CACHE_DIR) / f"{lang}_{region}.meta.json"
        
    def _is_cache_valid(self, lang: str, region: str) -> bool:
        """Check if cache is valid"""
        meta_path = self._get_cache_meta_path(lang, region)
        if not meta_path.exists():
            return False
            
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
                
            # Check TTL
            cache_time = datetime.fromisoformat(meta["timestamp"])
            if (datetime.now() - cache_time).total_seconds() > TRANSLATION_CACHE_TTL:
                return False
                
            # Check version
            if meta.get("version") != self._get_translation_version():
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Failed to read cache metadata: {e}")
            return False
            
    def _get_translation_version(self) -> str:
        """Get translation version hash"""
        try:
            base_dir = Path(__file__).parent.parent.parent.parent
            i18n_dir = base_dir / "resources" / "i18n"
            
            hasher = hashlib.sha256()
            for file_path in sorted(i18n_dir.rglob("*.json")):
                with open(file_path, "rb") as f:
                    hasher.update(f.read())
                    
            return hasher.hexdigest()[:8]
            
        except Exception as e:
            logger.error(f"Failed to calculate translation version: {e}")
            return str(int(time.time()))
            
    def _update_stats(self, lang: str, key: str):
        """Update translation usage statistics"""
        if lang not in self._stats:
            self._stats[lang] = {}
        if key not in self._stats[lang]:
            self._stats[lang][key] = 0
        self._stats[lang][key] += 1
        
    def get_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get translation usage statistics"""
        stats = {}
        for lang, lang_stats in self._stats.items():
            total_uses = sum(lang_stats.values())
            most_used = sorted(
                lang_stats.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
            
            stats[lang] = {
                "total_keys": len(lang_stats),
                "total_uses": total_uses,
                "most_used": most_used
            }
        return stats
        
    def get_cache_info(self) -> Dict[str, Dict[str, Any]]:
        """Get cache information"""
        return self._cache_info
        
    def clear_cache(self):
        """Clear translation cache"""
        try:
            for file in Path(TRANSLATION_CACHE_DIR).glob("*.json"):
                file.unlink()
            self._cache_info.clear()
            logger.info("Translation cache cleared")
        except Exception as e:
            logger.error(f"Failed to clear cache: {e}")

# Create global i18n manager instance
i18n_manager = I18nManager() 