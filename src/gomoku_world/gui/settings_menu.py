"""
Settings menu implementation
设置菜单实现
"""

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

from ..i18n import i18n_manager
from ..theme import theme
from ..utils.logger import get_logger

if TYPE_CHECKING:
    from .main_window import GomokuGUI

logger = get_logger(__name__)

class SettingsMenu(tk.Toplevel):
    """Settings menu window"""
    
    def __init__(self, parent: tk.Tk, main_window: 'GomokuGUI'):
        """Initialize settings menu"""
        super().__init__(parent)
        self.main_window = main_window
        
        self.title(i18n_manager.get_text("menu.settings"))
        self.geometry("400x300")
        
        self._create_widgets()
        self._setup_layout()
        
        logger.info("Settings menu initialized")
        
    def _create_widgets(self):
        """Create menu widgets"""
        # Language settings
        self.language_frame = ttk.LabelFrame(
            self,
            text=i18n_manager.get_text("menu.language")
        )
        
        self.language_var = tk.StringVar(value=i18n_manager.current_language)
        
        for lang_code, lang_info in i18n_manager.available_languages.items():
            ttk.Radiobutton(
                self.language_frame,
                text=f"{lang_info['native_name']} ({lang_info['name']})",
                value=lang_code,
                variable=self.language_var,
                command=lambda code=lang_code: self._change_language(code)
            ).pack(anchor=tk.W, padx=10, pady=5)
            
        # Theme settings
        self.theme_frame = ttk.LabelFrame(
            self,
            text=i18n_manager.get_text("menu.theme")
        )
        
        self.theme_var = tk.StringVar(value=theme.current_theme)
        
        for theme_name in theme.available_themes:
            ttk.Radiobutton(
                self.theme_frame,
                text=theme_name.capitalize(),
                value=theme_name,
                variable=self.theme_var,
                command=lambda name=theme_name: self._change_theme(name)
            ).pack(anchor=tk.W, padx=10, pady=5)
            
    def _setup_layout(self):
        """Setup widget layout"""
        self.language_frame.pack(fill=tk.X, padx=10, pady=5)
        self.theme_frame.pack(fill=tk.X, padx=10, pady=5)
        
    def _change_language(self, language_code: str):
        """Change application language"""
        try:
            i18n_manager.set_language(language_code)
            self.main_window.update_language()
            logger.info(f"Language changed to {language_code}")
        except Exception as e:
            logger.error(f"Failed to change language: {e}")
            
    def _change_theme(self, theme_name: str):
        """Change application theme"""
        try:
            theme.set_theme(theme_name)
            self.main_window.update_theme()
            logger.info(f"Theme changed to {theme_name}")
        except Exception as e:
            logger.error(f"Failed to change theme: {e}")
            
    def update_language(self):
        """Update menu texts when language changes"""
        self.title(i18n_manager.get_text("menu.settings"))
        self.language_frame.configure(text=i18n_manager.get_text("menu.language"))
        self.theme_frame.configure(text=i18n_manager.get_text("menu.theme")) 
