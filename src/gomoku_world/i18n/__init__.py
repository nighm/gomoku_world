"""
Internationalization (i18n) package.

国际化（i18n）包。

This package provides internationalization support with:
- Multiple language support
- Translation loading and caching
- String formatting
- Error handling
- Bilingual text support
- Translation management tools

本包提供国际化支持，具有：
- 多语言支持
- 翻译加载和缓存
- 字符串格式化
- 错误处理
- 双语文本支持
- 翻译管理工具
"""

from .base import (
    TranslationLoader,
    StringFormatter,
    TranslationCache,
    TranslationKey,
    TranslationValue,
    TranslationDict,
    LanguageCode
)
from .cache import MemoryCache
from .formatters.string import (
    DefaultFormatter,
    SafeFormatter,
    NamedFormatter
)
from .loaders import (
    JsonLoader,
    YamlLoader
)
from .manager import I18nManager
from .exceptions import (
    I18nError,
    TranslationNotFoundError,
    LanguageNotSupportedError,
    TranslationFileError,
    FormatterError,
    ValidationError,
    CacheError
)
from .tools import TranslationManager

# Create default i18n manager instance
from ..config.settings import TRANSLATIONS_DIR, DEFAULT_LANGUAGE, FALLBACK_LANGUAGE
i18n_manager = I18nManager(
    translations_dir=str(TRANSLATIONS_DIR),
    default_language=DEFAULT_LANGUAGE,
    fallback_language=FALLBACK_LANGUAGE
)

__all__ = [
    # Base interfaces
    'TranslationLoader',
    'StringFormatter',
    'TranslationCache',
    # Type definitions
    'TranslationKey',
    'TranslationValue',
    'TranslationDict',
    'LanguageCode',
    # Implementations
    'MemoryCache',
    'DefaultFormatter',
    'SafeFormatter',
    'NamedFormatter',
    'JsonLoader',
    'YamlLoader',
    'I18nManager',
    'TranslationManager',
    # Exceptions
    'I18nError',
    'TranslationNotFoundError',
    'LanguageNotSupportedError',
    'TranslationFileError',
    'FormatterError',
    'ValidationError',
    'CacheError',
    # Global instance
    'i18n_manager'
] 