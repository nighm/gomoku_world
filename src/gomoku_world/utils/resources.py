"""
Resource management module
资源管理模块
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

from ..config import RESOURCES_DIR, DEFAULT_THEME, DEFAULT_LANGUAGE
from .logger import get_logger

logger = get_logger(__name__)

class ResourceManager:
    """
    Manages game resources like themes, translations, and sounds
    管理游戏资源，如主题、翻译和音效
    """
    
    def __init__(self):
        """Initialize resource manager"""
        self.themes: Dict[str, Dict] = {}
        self.translations: Dict[str, Dict] = {}
        self.current_theme = DEFAULT_THEME
        self.current_language = DEFAULT_LANGUAGE
        
        # Initialize resource directories
        self._init_directories()
        # Load resources
        self._load_resources()
        
        logger.info("Resource manager initialized")
    
    def _init_directories(self):
        """Initialize resource directories"""
        # Create resource subdirectories
        (RESOURCES_DIR / "themes").mkdir(exist_ok=True)
        (RESOURCES_DIR / "translations").mkdir(exist_ok=True)
        (RESOURCES_DIR / "sounds").mkdir(exist_ok=True)
        
        # Create default theme if it doesn't exist
        self._create_default_theme()
        # Create default translations if they don't exist
        self._create_default_translations()
    
    def _create_default_theme(self):
        """Create default theme file"""
        default_theme = {
            "window": {
                "background": "#FFFFFF",
                "foreground": "#000000"
            },
            "board": {
                "background": "#EEEEEE",
                "grid_color": "#000000",
                "star_point_color": "#000000"
            },
            "pieces": {
                "black": "#000000",
                "white": "#FFFFFF",
                "black_outline": "#FFFFFF",
                "white_outline": "#000000"
            }
        }
        
        theme_file = RESOURCES_DIR / "themes" / "light.json"
        if not theme_file.exists():
            with open(theme_file, 'w', encoding='utf-8') as f:
                json.dump(default_theme, f, indent=4)
    
    def _create_default_translations(self):
        """Create default translation files"""
        translations = {
            "en": {
                "game": {
                    "title": "Gomoku World",
                    "new_game": "New Game",
                    "undo": "Undo",
                    "black_turn": "Black's turn",
                    "white_turn": "White's turn",
                    "black_wins": "Black wins!",
                    "white_wins": "White wins!",
                    "draw": "Game is a draw!"
                },
                "menu": {
                    "game": "Game",
                    "settings": "Settings",
                    "help": "Help",
                    "exit": "Exit"
                }
            },
            "zh": {
                "game": {
                    "title": "五子棋世界",
                    "new_game": "新游戏",
                    "undo": "悔棋",
                    "black_turn": "黑方回合",
                    "white_turn": "白方回合",
                    "black_wins": "黑方胜利！",
                    "white_wins": "白方胜利！",
                    "draw": "游戏平局！"
                },
                "menu": {
                    "game": "游戏",
                    "settings": "设置",
                    "help": "帮助",
                    "exit": "退出"
                }
            }
        }
        
        for lang, trans in translations.items():
            trans_file = RESOURCES_DIR / "translations" / f"{lang}.json"
            if not trans_file.exists():
                with open(trans_file, 'w', encoding='utf-8') as f:
                    json.dump(trans, f, indent=4, ensure_ascii=False)
    
    def _load_resources(self):
        """Load all resources"""
        self._load_themes()
        self._load_translations()
    
    def _load_themes(self):
        """Load theme files"""
        theme_dir = RESOURCES_DIR / "themes"
        for theme_file in theme_dir.glob("*.json"):
            try:
                with open(theme_file, 'r', encoding='utf-8') as f:
                    theme_name = theme_file.stem
                    self.themes[theme_name] = json.load(f)
                    logger.debug(f"Loaded theme: {theme_name}")
            except Exception as e:
                logger.error(f"Error loading theme {theme_file}: {e}")
    
    def _load_translations(self):
        """Load translation files"""
        trans_dir = RESOURCES_DIR / "translations"
        for trans_file in trans_dir.glob("*.json"):
            try:
                with open(trans_file, 'r', encoding='utf-8') as f:
                    lang = trans_file.stem
                    self.translations[lang] = json.load(f)
                    logger.debug(f"Loaded translation: {lang}")
            except Exception as e:
                logger.error(f"Error loading translation {trans_file}: {e}")
    
    def get_theme(self, theme_name: Optional[str] = None) -> Dict:
        """
        Get theme settings
        获取主题设置
        
        Args:
            theme_name: Theme name (default: current theme)
            
        Returns:
            Dict: Theme settings
        """
        theme = theme_name or self.current_theme
        return self.themes.get(theme, self.themes[DEFAULT_THEME])
    
    def get_text(self, key: str, lang: Optional[str] = None) -> str:
        """
        Get translated text
        获取翻译文本
        
        Args:
            key: Text key (e.g. 'game.title')
            lang: Language code (default: current language)
            
        Returns:
            str: Translated text
        """
        lang = lang or self.current_language
        trans = self.translations.get(lang, self.translations[DEFAULT_LANGUAGE])
        
        # Split key into parts
        parts = key.split('.')
        value = trans
        
        # Navigate through the dictionary
        for part in parts:
            value = value.get(part, part)
            if not isinstance(value, dict):
                break
        
        return str(value)
    
    def set_theme(self, theme_name: str):
        """
        Set current theme
        设置当前主题
        
        Args:
            theme_name: Theme name
        """
        if theme_name in self.themes:
            self.current_theme = theme_name
            logger.info(f"Theme changed to: {theme_name}")
        else:
            logger.warning(f"Theme not found: {theme_name}")
    
    def set_language(self, lang: str):
        """
        Set current language
        设置当前语言
        
        Args:
            lang: Language code
        """
        if lang in self.translations:
            self.current_language = lang
            logger.info(f"Language changed to: {lang}")
        else:
            logger.warning(f"Language not found: {lang}")

# Create global instance
resource_manager = ResourceManager() 