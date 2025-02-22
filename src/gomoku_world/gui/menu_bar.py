"""
Menu bar implementation with language selection
带有语言选择功能的菜单栏实现
"""

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING, Dict

from ..i18n import i18n_manager
from ..i18n.constants import LANGUAGE_CODES
from ..theme import theme
from ..utils.logger import get_logger

if TYPE_CHECKING:
    from .main_window import GomokuGUI

logger = get_logger(__name__)

class MenuBar(tk.Menu):
    """Menu bar with language selection"""
    
    def __init__(self, master: tk.Tk, main_window: 'GomokuGUI'):
        """Initialize menu bar"""
        super().__init__(master)
        self.main_window = main_window
        
        # Create menus
        self._create_file_menu()
        self._create_settings_menu()
        self._create_help_menu()
        
        logger.info("Menu bar initialized")
        
    def _create_file_menu(self):
        """Create file menu"""
        file_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(
            label=i18n_manager.get_text("menu.file"),
            menu=file_menu
        )
        
        file_menu.add_command(
            label=i18n_manager.get_text("game.new"),
            command=self.main_window.new_game
        )
        
        file_menu.add_separator()
        
        file_menu.add_command(
            label=i18n_manager.get_text("game.quit"),
            command=self.main_window.root.quit
        )
        
    def _create_settings_menu(self):
        """Create settings menu"""
        settings_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(
            label=i18n_manager.get_text("menu.settings"),
            menu=settings_menu
        )
        
        # Create language submenu
        language_menu = tk.Menu(settings_menu, tearoff=0)
        settings_menu.add_cascade(
            label=i18n_manager.get_text("menu.language"),
            menu=language_menu
        )
        
        # Add language options
        self.language_var = tk.StringVar(value=i18n_manager.current_language)
        
        for lang_code, lang_info in LANGUAGE_CODES.items():
            language_menu.add_radiobutton(
                label=f"{lang_info['native_name']} ({lang_info['name']})",
                value=lang_code,
                variable=self.language_var,
                command=lambda code=lang_code: self._change_language(code)
            )
            
        # Create theme submenu
        theme_menu = tk.Menu(settings_menu, tearoff=0)
        settings_menu.add_cascade(
            label=i18n_manager.get_text("menu.theme"),
            menu=theme_menu
        )
        
        # Add theme options
        self.theme_var = tk.StringVar(value=theme.current_theme)
        for theme_name in theme.available_themes:
            theme_menu.add_radiobutton(
                label=theme_name.capitalize(),
                value=theme_name,
                variable=self.theme_var,
                command=lambda name=theme_name: theme.set_theme(name)
            )
            
    def _create_help_menu(self):
        """Create help menu"""
        help_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(
            label=i18n_manager.get_text("menu.help"),
            menu=help_menu
        )
        
        help_menu.add_command(
            label=i18n_manager.get_text("menu.about"),
            command=self._show_about
        )
        
    def _change_language(self, language_code: str):
        """Change application language"""
        try:
            i18n_manager.set_language(language_code)
            self.main_window.update_language()
            logger.info(f"Language changed to {language_code}")
        except Exception as e:
            logger.error(f"Failed to change language: {e}")
            
    def _show_about(self):
        """Show about dialog"""
        from tkinter import messagebox
        messagebox.showinfo(
            i18n_manager.get_text("menu.about"),
            i18n_manager.get_text("app.description")
        )
        
    def update_language(self):
        """Update menu texts when language changes"""
        # Update menu labels
        self.entryconfig(
            1,  # File menu index
            label=i18n_manager.get_text("menu.file")
        )
        self.entryconfig(
            2,  # Settings menu index
            label=i18n_manager.get_text("menu.settings")
        )
        self.entryconfig(
            3,  # Help menu index
            label=i18n_manager.get_text("menu.help")
        ) 
