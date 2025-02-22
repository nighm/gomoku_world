"""
Base interfaces for internationalization.

国际化基础接口。

This module defines the core interfaces for the internationalization system:
- TranslationLoader: Interface for loading translations
- StringFormatter: Interface for string formatting
- TranslationCache: Interface for translation caching

本模块定义了国际化系统的核心接口：
- TranslationLoader: 翻译加载接口
- StringFormatter: 字符串格式化接口
- TranslationCache: 翻译缓存接口
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional, Any, Protocol, TypeVar, Union

# Type definitions
TranslationKey = str
TranslationValue = str
TranslationDict = Dict[TranslationKey, TranslationValue]
LanguageCode = str

class TranslationLoader(ABC):
    """
    Abstract base class for translation loaders.
    翻译加载器的抽象基类。
    """
    
    @abstractmethod
    def load(self, language: LanguageCode) -> TranslationDict:
        """
        Load translations for a language.
        加载指定语言的翻译。
        
        Args:
            language (LanguageCode): Language code (e.g. 'en', 'zh-CN')
                                   语言代码（如'en'、'zh-CN'）
                          
        Returns:
            TranslationDict: Dictionary of translation strings
                           翻译字符串字典
                           
        Raises:
            FileNotFoundError: If translation file not found
                             如果未找到翻译文件
            ValueError: If translation format is invalid
                       如果翻译格式无效
        """
        pass
        
    @abstractmethod
    def save(self, language: LanguageCode, translations: TranslationDict) -> None:
        """
        Save translations for a language.
        保存指定语言的翻译。
        
        Args:
            language (LanguageCode): Language code (e.g. 'en', 'zh-CN')
                                   语言代码（如'en'、'zh-CN'）
            translations (TranslationDict): Dictionary of translation strings
                                         翻译字符串字典
                                         
        Raises:
            IOError: If unable to save translations
                    如果无法保存翻译
            ValueError: If translations are invalid
                       如果翻译无效
        """
        pass

class StringFormatter(ABC):
    """
    Abstract base class for string formatters.
    字符串格式化器的抽象基类。
    """
    
    @abstractmethod
    def format(self, template: str, **kwargs: Any) -> str:
        """
        Format a string template with the given arguments.
        使用给定参数格式化字符串模板。
        
        Args:
            template (str): String template to format
                          要格式化的字符串模板
            **kwargs: Format arguments
                     格式化参数
                     
        Returns:
            str: Formatted string
                 格式化后的字符串
                 
        Raises:
            ValueError: If template format is invalid
                       如果模板格式无效
        """
        pass

class TranslationCache(ABC):
    """
    Abstract base class for translation caches.
    翻译缓存的抽象基类。
    """
    
    @abstractmethod
    def get(self, key: TranslationKey) -> Optional[TranslationValue]:
        """
        Get a value from cache.
        从缓存获取值。
        
        Args:
            key (TranslationKey): Cache key
                                缓存键
                      
        Returns:
            Optional[TranslationValue]: Cached value if exists, None otherwise
                                      如果存在则返回缓存的值，否则返回None
        """
        pass
        
    @abstractmethod
    def set(self, key: TranslationKey, value: TranslationValue) -> None:
        """
        Set a value in cache.
        在缓存中设置值。
        
        Args:
            key (TranslationKey): Cache key
                                缓存键
            value (TranslationValue): Value to cache
                                    要缓存的值
                                    
        Raises:
            ValueError: If value is invalid
                       如果值无效
        """
        pass
        
    @abstractmethod
    def clear(self) -> None:
        """
        Clear all entries from cache.
        清除缓存中的所有条目。
        """
        pass

    @abstractmethod
    def remove(self, key: TranslationKey) -> None:
        """
        Remove a specific entry from cache.
        从缓存中移除特定条目。
        
        Args:
            key (TranslationKey): Cache key to remove
                                要移除的缓存键
        """
        pass 