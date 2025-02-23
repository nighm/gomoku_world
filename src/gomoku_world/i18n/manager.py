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
from typing import Dict, Optional, List, Any, Callable
from pathlib import Path

from .config import config
from .base import TranslationLoader, StringFormatter, TranslationCache
from .base import TranslationDict, LanguageCode
from .cache import MemoryCache
from .formatters.string import DefaultFormatter
from .loaders import JsonLoader, YamlLoader
from .exceptions import (
    TranslationNotFoundError,
    LanguageNotSupportedError,
    FormatterError,
    I18nError
)

logger = logging.getLogger(__name__)

# Language code mappings / 语言代码映射
LANGUAGE_CODES = {
    "zh": "zh-CN",  # Map 'zh' to 'zh-CN'
    "en": "en"
}

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
    ):
        """
        Initialize i18n manager.
        初始化i18n管理器。

        Args:
            translations_dir: Directory containing translation files
                            包含翻译文件的目录
            default_language: Default language code
                            默认语言代码
            fallback_language: Fallback language code
                             回退语言代码
            loader: Translation loader instance
                   翻译加载器实例
            formatter: String formatter instance
                      字符串格式化器实例
            cache: Translation cache instance
                  翻译缓存实例
        """
        # Initialize storage
        self._translations = {}
        self._available_languages = {}
        self._initialized = False
        self._online_features = config.get("ONLINE_FEATURES_ENABLED", True)
        self._change_listeners = []  # Add change listeners list
        
        # Set paths and languages
        self.translations_dir = Path(translations_dir or config.translations_dir)
        self.default_language = default_language or config.default_language
        self.fallback_language = fallback_language or config.fallback_language
        
        # Initialize components
        self.loader = loader or JsonLoader(str(self.translations_dir))
        self.formatter = formatter or DefaultFormatter()
        self.cache = cache or MemoryCache()
        
        # Load translations for default and fallback languages
        self._load_translations(self.default_language)
        if self.fallback_language != self.default_language:
            self._load_translations(self.fallback_language)
            
        self._initialized = True
        logger.info(f"I18n manager initialized with default language '{self.default_language}' "
                   f"and fallback language '{self.fallback_language}'")
    
    def add_change_listener(self, listener: Callable[[], None]):
        """
        Add a language change listener.
        添加语言变更监听器。
        
        Args:
            listener: Callback function to be called when language changes
                     当语言变更时要调用的回调函数
        """
        if listener not in self._change_listeners:
            self._change_listeners.append(listener)
    
    def remove_change_listener(self, listener: Callable[[], None]):
        """
        Remove a language change listener.
        移除语言变更监听器。
        
        Args:
            listener: Callback function to remove
                     要移除的回调函数
        """
        if listener in self._change_listeners:
            self._change_listeners.remove(listener)
    
    def _notify_listeners(self):
        """
        Notify all listeners about language change.
        通知所有监听器语言已变更。
        """
        for listener in self._change_listeners:
            try:
                listener()
            except Exception as e:
                logger.error(f"Error in language change listener: {e}")
    
    def _get_file_language_code(self, language: str) -> str:
        """
        Get the correct language code for file loading.
        获取用于文件加载的正确语言代码。
        
        Args:
            language: Language code to convert
                     要转换的语言代码
                     
        Returns:
            str: Correct language code for file loading
                 用于文件加载的正确语言代码
        """
        return LANGUAGE_CODES.get(language, language)
    
    def _load_translations(self, language: str) -> None:
        """
        Load translations for a language.
        加载指定语言的翻译。
        
        Args:
            language: Language code to load
                     要加载的语言代码
        """
        try:
            file_language = self._get_file_language_code(language)
            self._translations[language] = self.loader.load(file_language)
            self._available_languages[language] = language
            logger.debug(f"Loaded translations for language: {language}")
        except Exception as e:
            logger.error(f"Failed to load translations for {language}: {e}")
            if language == self.default_language:
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
        
        lang = language or self.default_language
        cache_key = f"{lang}:{key}"
        
        # Try cache first
        if config.get("CACHE_ENABLED"):
            cached = self.cache.get(cache_key)
            if cached is not None:
                return self.formatter.format(cached, **kwargs)
        
        # Try current language
        text = self._get_nested_value(self._translations.get(lang, {}), key)
        if text is None and fallback and lang != self.fallback_language:
            # Try fallback language
            text = self._get_nested_value(self._translations.get(self.fallback_language, {}), key)
            if text is None:
                logger.warning(f"Translation not found for key: {key}")
                text = key
        
        if config.get("CACHE_ENABLED") and text is not None:
            self.cache.set(cache_key, text)
        
        return self.formatter.format(text, **kwargs)
    
    def _get_nested_value(self, data: Dict[str, Any], key: str) -> Optional[str]:
        """
        Get value from nested dictionary using dot notation.
        使用点号表示法从嵌套字典中获取值。
        
        Args:
            data: Dictionary to search in
                 要搜索的字典
            key: Key in dot notation (e.g. 'menu.file')
                 以点号分隔的键（例如'menu.file'）
                
        Returns:
            str: Value if found, None otherwise
                 如果找到则返回值，否则返回None
        """
        parts = key.split('.')
        value = data
        
        for part in parts:
            if not isinstance(value, dict):
                return None
            value = value.get(part)
            
        return value if isinstance(value, str) else None
    
    def get_bilingual(self, key: str, **kwargs: Any) -> str:
        """
        Get bilingual text (current language + fallback language).
        获取双语文本（当前语言+后备语言）。
        """
        current = self.get_text(key, fallback=False, **kwargs)
        if current == key or self.default_language == self.fallback_language:
            return current
        
        fallback = self.get_text(key, language=self.fallback_language, **kwargs)
        if current == fallback:
            return current
        
        return f"{current} / {fallback}"
    
    def set_language(self, language: str, force_reload: bool = False) -> None:
        """
        Set current language.
        设置当前语言。
        """
        if language not in self._available_languages or force_reload:
            self._load_translations(language)
        self.default_language = language
        logger.info(f"Language set to: {language}")
        self._notify_listeners()
    
    def get_language(self) -> str:
        """
        Get current language.
        获取当前语言。
        """
        return self.default_language
    
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
        self.cache.clear()
        logger.debug("Translation cache cleared")
    
    def reload_translations(self) -> None:
        """
        Reload all translations.
        重新加载所有翻译。
        """
        self._translations.clear()
        self._available_languages.clear()
        self._load_translations(self.default_language)
        if self.fallback_language != self.default_language:
            self._load_translations(self.fallback_language)
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

    def get_font_family(self) -> str:
        """
        Get font family for current language.
        获取当前语言的字体系列。
        
        Returns:
            str: Font family name
                 字体系列名称
        """
        # TODO: Add font family configuration for each language
        # 默认使用系统默认字体
        return "Arial"

# Create default instance / 创建默认实例
i18n_manager = I18nManager()

__all__ = ["I18nManager", "i18n_manager"] 