"""
Resource management module for the Gomoku World game.

五子棋世界游戏的资源管理模块。

This module provides functionality for managing game resources:
- Theme management (colors, styles)
- Translation management
- Sound effects
- Image resources
- Configuration files

本模块提供游戏资源管理功能：
- 主题管理（颜色、样式）
- 翻译管理
- 音效
- 图像资源
- 配置文件
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

from ..config import (
    RESOURCES_DIR,
    DEFAULT_THEME,
    DEFAULT_LANGUAGE,
    SUPPORTED_LANGUAGES,
    SUPPORTED_THEMES
)
from .logger import get_logger

logger = get_logger(__name__)

class ResourceManager:
    """
    Resource manager for handling game assets and configurations.
    
    游戏资源和配置的管理器。
    
    This class manages:
    - Theme loading and switching
    - Translation management
    - Sound effect handling
    - Image resource loading
    - Resource directory structure
    
    此类管理：
    - 主题加载和切换
    - 翻译管理
    - 音效处理
    - 图像资源加载
    - 资源目录结构
    """
    
    def __init__(self):
        """
        Initialize the resource manager.
        
        初始化资源管理器。
        
        Sets up:
        - Resource directories
        - Default themes
        - Default translations
        - Initial resource loading
        
        设置：
        - 资源目录
        - 默认主题
        - 默认翻译
        - 初始资源加载
        """
        self.themes: Dict[str, Dict] = {}
        self.translations: Dict[str, Dict] = {}
        self.current_theme = DEFAULT_THEME
        self.current_language = DEFAULT_LANGUAGE
        
        # Initialize resource directories / 初始化资源目录
        self._init_directories()
        # Load all resources / 加载所有资源
        self._load_resources()
        
        logger.info("Resource manager initialized / 资源管理器已初始化")
    
    def _init_directories(self):
        """
        Initialize resource directory structure.
        
        初始化资源目录结构。
        
        Creates:
        - Theme directory
        - Translation directory
        - Sound effects directory
        - Image resources directory
        
        创建：
        - 主题目录
        - 翻译目录
        - 音效目录
        - 图像资源目录
        """
        # Create resource subdirectories / 创建资源子目录
        (RESOURCES_DIR / "themes").mkdir(exist_ok=True)
        (RESOURCES_DIR / "translations").mkdir(exist_ok=True)
        (RESOURCES_DIR / "sounds").mkdir(exist_ok=True)
        (RESOURCES_DIR / "images").mkdir(exist_ok=True)
        
        # Create default resources if they don't exist / 如果默认资源不存在则创建
        self._create_default_theme()
        self._create_default_translations()
    
    def _create_default_theme(self):
        """
        Create default theme configuration.
        
        创建默认主题配置。
        
        Creates a light theme with:
        - Window colors
        - Board colors
        - Piece colors
        - Text colors
        
        创建包含以下内容的明亮主题：
        - 窗口颜色
        - 棋盘颜色
        - 棋子颜色
        - 文本颜色
        """
        default_theme = {
            "window": {
                "background": "#FFFFFF",
                "foreground": "#000000",
                "border": "#CCCCCC"
            },
            "board": {
                "background": "#F0F0F0",
                "grid": "#000000",
                "highlight": "#FFD700"
            },
            "pieces": {
                "black": "#000000",
                "white": "#FFFFFF",
                "border": "#000000"
            },
            "text": {
                "primary": "#000000",
                "secondary": "#666666",
                "accent": "#0066CC"
            }
        }
        
        theme_file = RESOURCES_DIR / "themes" / "light.json"
        if not theme_file.exists():
            with open(theme_file, "w", encoding="utf-8") as f:
                json.dump(default_theme, f, indent=4)
                logger.info("Created default theme / 已创建默认主题")
    
    def _create_default_translations(self):
        """
        Create default translation files.
        
        创建默认翻译文件。
        
        Creates translation files for:
        - English (en)
        - Chinese (zh)
        - Japanese (ja)
        - Korean (ko)
        
        为以下语言创建翻译文件：
        - 英语 (en)
        - 中文 (zh)
        - 日语 (ja)
        - 韩语 (ko)
        """
        default_translations = {
            "en": {
                "game.title": "Gomoku World",
                "game.new": "New Game",
                "game.load": "Load Game",
                "game.save": "Save Game",
                "game.quit": "Quit"
            },
            "zh": {
                "game.title": "五子棋世界",
                "game.new": "新游戏",
                "game.load": "加载游戏",
                "game.save": "保存游戏",
                "game.quit": "退出"
            }
        }
        
        for lang, translations in default_translations.items():
            trans_file = RESOURCES_DIR / "translations" / f"{lang}.json"
            if not trans_file.exists():
                with open(trans_file, "w", encoding="utf-8") as f:
                    json.dump(translations, f, indent=4, ensure_ascii=False)
                    logger.info(f"Created {lang} translations / 已创建{lang}翻译")
    
    def _load_resources(self):
        """
        Load all game resources.
        
        加载所有游戏资源。
        """
        self._load_themes()
        self._load_translations()
        logger.info("All resources loaded / 所有资源已加载")
    
    def _load_themes(self):
        """
        Load all theme configurations.
        
        加载所有主题配置。
        """
        theme_dir = RESOURCES_DIR / "themes"
        for theme_file in theme_dir.glob("*.json"):
            theme_name = theme_file.stem
            try:
                with open(theme_file, encoding="utf-8") as f:
                    self.themes[theme_name] = json.load(f)
                logger.info(f"Loaded theme: {theme_name} / 已加载主题：{theme_name}")
            except Exception as e:
                logger.error(f"Failed to load theme {theme_name}: {e} / 加载主题{theme_name}失败：{e}")
    
    def _load_translations(self):
        """
        Load all translation files.
        
        加载所有翻译文件。
        """
        trans_dir = RESOURCES_DIR / "translations"
        for trans_file in trans_dir.glob("*.json"):
            lang = trans_file.stem
            try:
                with open(trans_file, encoding="utf-8") as f:
                    self.translations[lang] = json.load(f)
                logger.info(f"Loaded translations: {lang} / 已加载翻译：{lang}")
            except Exception as e:
                logger.error(f"Failed to load translations {lang}: {e} / 加载翻译{lang}失败：{e}")
    
    def get_theme(self, theme_name: Optional[str] = None) -> Dict:
        """
        Get theme configuration.
        
        获取主题配置。
        
        Args:
            theme_name (Optional[str]): Theme name to get. Uses current theme if None.
                                      要获取的主题名称。如果为None则使用当前主题。
                                      
        Returns:
            Dict: Theme configuration dictionary.
                 主题配置字典。
                 
        Raises:
            KeyError: If theme does not exist.
                     如果主题不存在。
        """
        theme = theme_name or self.current_theme
        if theme not in self.themes:
            logger.warning(f"Theme {theme} not found, using default / 未找到主题{theme}，使用默认主题")
            theme = DEFAULT_THEME
        return self.themes[theme]
    
    def get_text(self, key: str, lang: Optional[str] = None) -> str:
        """
        Get translated text.
        
        获取翻译文本。
        
        Args:
            key (str): Translation key.
                      翻译键。
            lang (Optional[str]): Language code. Uses current language if None.
                                语言代码。如果为None则使用当前语言。
                                
        Returns:
            str: Translated text, or key if translation not found.
                 翻译文本，如果未找到翻译则返回键。
        """
        language = lang or self.current_language
        try:
            return self.translations[language][key]
        except KeyError:
            logger.warning(f"Translation not found: {key} ({language}) / 未找到翻译：{key}（{language}）")
            return key
    
    def set_theme(self, theme_name: str):
        """
        Set current theme.
        
        设置当前主题。
        
        Args:
            theme_name (str): Name of theme to set.
                            要设置的主题名称。
                            
        Raises:
            ValueError: If theme is not supported.
                       如果主题不受支持。
        """
        if theme_name not in SUPPORTED_THEMES:
            raise ValueError(f"Unsupported theme: {theme_name} / 不支持的主题：{theme_name}")
        self.current_theme = theme_name
        logger.info(f"Theme set to: {theme_name} / 主题已设置为：{theme_name}")
    
    def set_language(self, lang: str):
        """
        Set current language.
        
        设置当前语言。
        
        Args:
            lang (str): Language code to set.
                       要设置的语言代码。
                       
        Raises:
            ValueError: If language is not supported.
                       如果语言不受支持。
        """
        if lang not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {lang} / 不支持的语言：{lang}")
        self.current_language = lang
        logger.info(f"Language set to: {lang} / 语言已设置为：{lang}")

# Create global resource manager instance / 创建全局资源管理器实例
resource_manager = ResourceManager()

__all__ = ['resource_manager', 'ResourceManager'] 
