"""
Internationalization (i18n) manager implementation.

国际化（i18n）管理器实现。

This module provides the main i18n manager with:
- Multiple language support
- Fallback language handling
- Translation caching
- String formatting
- Error handling

本模块提供主要的i18n管理器，具有：
- 多语言支持
- 回退语言处理
- 翻译缓存
- 字符串格式化
- 错误处理
"""

import logging
from typing import Dict, Optional, List, Any
from pathlib import Path

from .config import config
from .base import TranslationLoader, StringFormatter, TranslationCache
from .base import TranslationDict, LanguageCode
from .cache import MemoryCache
from .formatters.string import DefaultFormatter
from .loaders.json import JsonLoader
from .exceptions import (
    TranslationNotFoundError,
    LanguageNotSupportedError,
    FormatterError,
    I18nError
)

logger = logging.getLogger(__name__)

class I18nManager:
    """
    Main internationalization manager that handles translations, formatting, and caching.
    主要的国际化管理器，处理翻译、格式化和缓存。
    """
    
    def __init__(
        self,
        translations_dir: Optional[str] = None,
        default_language: Optional[str] = None,
        fallback_language: Optional[str] = None,
        loader: Optional[TranslationLoader] = None,
        formatter: Optional[StringFormatter] = None,
        cache: Optional[TranslationCache] = None
    ) -> None:
        """
        Initialize i18n manager.
        初始化i18n管理器。
        """
        self._translations_dir = translations_dir or config.get("TRANSLATIONS_DIR")
        self._default_language = default_language or config.get("DEFAULT_LANGUAGE")
        self._fallback_language = fallback_language or config.get("FALLBACK_LANGUAGE")
        
        self._loader = loader or JsonLoader(self._translations_dir)
        self._formatter = formatter or DefaultFormatter()
        self._cache = cache or MemoryCache(
            ttl=config.get("CACHE_TTL"),
            max_size=config.get("CACHE_MAX_SIZE")
        )
        
        self._current_language = self._default_language
        self._translations: Dict[str, Dict[str, str]] = {}
        self._available_languages: Dict[str, str] = {}
        self._initialized = False
        
        self._online_features = config.get("ONLINE_FEATURES_ENABLED")
        self._debug = config.get("DEBUG")
        
        if self._debug:
            logger.setLevel(config.get("LOG_LEVEL"))
    
    def initialize(self) -> None:
        """
        Initialize the i18n system.
        初始化国际化系统。
        """
        try:
            self._load_language(self._default_language)
            if self._fallback_language != self._default_language:
                self._load_language(self._fallback_language)
            self._initialized = True
            logger.info(
                f"I18n manager initialized with language: {self._current_language}"
            )
        except Exception as e:
            logger.error(f"Failed to initialize i18n manager: {e}")
            raise I18nError(f"Initialization failed: {e}") from e
    
    def _load_language(self, language: str) -> None:
        """
        Load translations for a specific language.
        加载指定语言的翻译。
        """
        try:
            translations = self._loader.load(language)
            self._translations[language] = translations
            self._available_languages[language] = language
            logger.debug(f"Loaded translations for language: {language}")
        except Exception as e:
            logger.error(f"Failed to load translations for {language}: {e}")
            if language == self._default_language:
                raise
    
    def get_text(
        self,
        key: str,
        language: Optional[str] = None,
        fallback: bool = True,
        **kwargs: Any
    ) -> str:
        """
        Get translated text for a key.
        获取指定键的翻译文本。
        """
        if not self._initialized:
            raise I18nError("I18n manager not initialized")
        
        lang = language or self._current_language
        cache_key = f"{lang}:{key}"
        
        # Try cache first
        if config.get("CACHE_ENABLED"):
            cached = self._cache.get(cache_key)
            if cached is not None:
                return self._formatter.format(cached, **kwargs)
        
        # Try current language
        text = self._translations.get(lang, {}).get(key)
        if text is None and fallback and lang != self._fallback_language:
            # Try fallback language
            text = self._translations.get(self._fallback_language, {}).get(key)
            if text is None:
                logger.warning(f"Translation not found for key: {key}")
                text = key
        
        if config.get("CACHE_ENABLED") and text is not None:
            self._cache.set(cache_key, text)
        
        return self._formatter.format(text, **kwargs)
    
    def get_bilingual(self, key: str, **kwargs: Any) -> str:
        """
        Get bilingual text (current language + fallback language).
        获取双语文本（当前语言+后备语言）。
        """
        current = self.get_text(key, fallback=False, **kwargs)
        if current == key or self._current_language == self._fallback_language:
            return current
        
        fallback = self.get_text(key, language=self._fallback_language, **kwargs)
        if current == fallback:
            return current
        
        return f"{current} / {fallback}"
    
    def set_language(self, language: str, force_reload: bool = False) -> None:
        """
        Set current language.
        设置当前语言。
        """
        if language not in self._available_languages or force_reload:
            self._load_language(language)
        self._current_language = language
        logger.info(f"Language set to: {language}")
    
    def get_language(self) -> str:
        """
        Get current language.
        获取当前语言。
        """
        return self._current_language
    
    def get_available_languages(self) -> List[str]:
        """
        Get list of available languages.
        获取可用语言列表。
        """
        return list(self._available_languages.keys())
    
    def clear_cache(self) -> None:
        """
        Clear translation cache.
        清除翻译缓存。
        """
        self._cache.clear()
        logger.debug("Translation cache cleared")
    
    def reload_translations(self) -> None:
        """
        Reload all translations.
        重新加载所有翻译。
        """
        self._translations.clear()
        self._available_languages.clear()
        self._load_language(self._current_language)
        if self._fallback_language != self._current_language:
            self._load_language(self._fallback_language)
        logger.info("Translations reloaded")
    
    @property
    def online_features_enabled(self) -> bool:
        """
        Check if online features are enabled.
        检查是否启用在线功能。
        """
        return self._online_features
    
    @online_features_enabled.setter
    def online_features_enabled(self, value: bool) -> None:
        """
        Enable or disable online features.
        启用或禁用在线功能。
        """
        self._online_features = value
        config.set("ONLINE_FEATURES_ENABLED", value)
        logger.info(f"Online features {'enabled' if value else 'disabled'}")

# Create default instance / 创建默认实例
i18n_manager = I18nManager()

__all__ = ["I18nManager", "i18n_manager"] 