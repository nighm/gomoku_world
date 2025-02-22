"""
Internationalization (i18n) management module.

国际化（i18n）管理模块。
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
    Internationalization manager class.
    
    国际化管理类。
    """
    
    def __init__(self):
        """
        Initialize i18n manager.
        
        初始化国际化管理器。
        """
        self._language = "en"
        self._texts: Dict[str, Dict[str, str]] = {}
        self._cache: Dict[str, str] = {}
        self._initialized = False
        
        # Get the project root directory / 获取项目根目录
        self._root_dir = Path(__file__).parent.parent.parent
        logger.info("Project root directory / 项目根目录: %s", self._root_dir)
    
    def initialize(self):
        """
        Initialize the i18n system.
        
        初始化国际化系统。
        """
        if self._initialized:
            return
        self._load_translations(self._language)
        self._initialized = True
        logger.info("I18n manager initialized with language / 国际化管理器已初始化，语言为: %s", self._language)
    
    def _load_translations(self, language: str):
        """
        Load translations for the specified language.
        
        加载指定语言的翻译。
        """
        self._texts[language] = {}
        
        # Try different possible resource paths / 尝试不同的可能资源路径
        resource_paths = [
            self._root_dir / "resources" / "i18n" / language,  # Development path / 开发路径
            Path(__file__).parent / "resources" / "i18n" / language,  # Package path / 包路径
        ]
        
        for resource_dir in resource_paths:
            logger.info("Trying resource directory / 尝试资源目录: %s", resource_dir)
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
                    logger.info("Loaded translations from / 已从以下位置加载翻译: %s", file)
                except Exception as e:
                    logger.error("Failed to load translation file / 加载翻译文件失败 %s: %s", file, e)
            
            # If we found and loaded translations, we're done / 如果找到并加载了翻译，就完成了
            if self._texts[language]:
                logger.info("Successfully loaded translations from / 成功从以下位置加载翻译: %s", resource_dir)
                return
                
        logger.warning("No translation files found for language / 未找到该语言的翻译文件: %s", language)
    
    def get_text(self, key: str) -> str:
        """
        Get text by key.
        
        通过键获取文本。
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
            
        logger.warning("Translation not found for key / 未找到该键的翻译: %s", key)
        return key
    
    def get_bilingual(self, key: str) -> str:
        """
        Get bilingual text by key.
        
        通过键获取双语文本。
        """
        text = self.get_text(key)
        if self._language != "en":
            en_text = self.get_text(key)
            if text != key:  # If translation exists / 如果翻译存在
                return f"{text} / {en_text}"
        return text
    
    def set_language(self, language: str, force_reload: bool = False):
        """
        Set current language.
        
        设置当前语言。
        
        Args:
            language: Language code / 语言代码
            force_reload: Force reload translations / 强制重新加载翻译
        """
        if language == self._language and not force_reload:
            return
            
        self._language = language
        if force_reload:
            self._texts = {}
            self._cache = {}
            self._initialized = False
        self.initialize()
        logger.info("Language changed to / 语言已更改为: %s", language)

# Create global i18n instance / 创建全局国际化实例
i18n = I18n()

__all__ = ['i18n'] 