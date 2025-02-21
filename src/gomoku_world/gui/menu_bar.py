"""
Menu bar implementation
鑿滃崟鏍忓疄鐜?
"""

import tkinter as tk
from tkinter import messagebox
from typing import TYPE_CHECKING

# 浣跨敤鐩稿瀵煎叆
from ..utils.logger import get_logger

if TYPE_CHECKING:
    from .main_window import GomokuGUI

logger = get_logger(__name__)

class MenuBar(tk.Menu):
    """
    Menu bar for the game window
    娓告垙绐楀彛鐨勮彍鍗曟爮
    """
    
    def __init__(self, parent, main_window: 'GomokuGUI'):
        """
        Initialize menu bar
        鍒濆鍖栬彍鍗曟爮
        
        Args:
            parent: Parent widget
            main_window: Main window instance
        """
        super().__init__(parent)
        
        self.main_window = main_window
        
        self._create_menus()
        
        logger.info("Menu bar initialized")
    
    def _create_menus(self):
        """
        Create all menus
        鍒涘缓鎵€鏈夎彍鍗?
        """
        # Game menu
        game_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Game", menu=game_menu)
        
        game_menu.add_command(
            label="New Game",
            command=self.main_window.new_game
        )
        game_menu.add_command(
            label="Undo",
            command=self.main_window.undo_move
        )
        game_menu.add_separator()
        game_menu.add_command(
            label="Exit",
            command=self._on_exit
        )
        
        # Settings menu
        settings_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Settings", menu=settings_menu)
        
        # Theme submenu
        theme_menu = tk.Menu(settings_menu, tearoff=0)
        settings_menu.add_cascade(label="Theme", menu=theme_menu)
        
        self.theme_var = tk.StringVar(value="light")
        theme_menu.add_radiobutton(
            label="Light",
            variable=self.theme_var,
            value="light",
            command=self._on_theme_change
        )
        theme_menu.add_radiobutton(
            label="Dark",
            variable=self.theme_var,
            value="dark",
            command=self._on_theme_change
        )
        
        # Language submenu
        lang_menu = tk.Menu(settings_menu, tearoff=0)
        settings_menu.add_cascade(label="Language", menu=lang_menu)
        
        self.lang_var = tk.StringVar(value="en")
        lang_menu.add_radiobutton(
            label="English",
            variable=self.lang_var,
            value="en",
            command=self._on_language_change
        )
        lang_menu.add_radiobutton(
            label="涓枃",
            variable=self.lang_var,
            value="zh",
            command=self._on_language_change
        )
        
        # Sound settings
        settings_menu.add_separator()
        self.sound_var = tk.BooleanVar(value=True)
        settings_menu.add_checkbutton(
            label="Sound Effects",
            variable=self.sound_var,
            command=self._on_sound_change
        )
        
        # Help menu
        help_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="Help", menu=help_menu)
        
        help_menu.add_command(
            label="How to Play",
            command=self._show_help
        )
        help_menu.add_command(
            label="About",
            command=self._show_about
        )
        
        logger.debug("All menus created")
    
    def _on_exit(self):
        """
        Handle exit menu command
        澶勭悊閫€鍑鸿彍鍗曞懡浠?
        """
        if messagebox.askokcancel("Exit", "Do you want to quit?"):
            self.main_window.root.quit()
            logger.info("Application exit requested")
    
    def _on_theme_change(self):
        """
        Handle theme change
        澶勭悊涓婚鍙樻洿
        """
        # TODO: Implement theme change
        theme = self.theme_var.get()
        logger.info(f"Theme changed to {theme}")
    
    def _on_language_change(self):
        """
        Handle language change
        澶勭悊璇█鍙樻洿
        """
        # TODO: Implement language change
        lang = self.lang_var.get()
        logger.info(f"Language changed to {lang}")
    
    def _on_sound_change(self):
        """
        Handle sound settings change
        澶勭悊澹伴煶璁剧疆鍙樻洿
        """
        # TODO: Implement sound settings
        enabled = self.sound_var.get()
        logger.info(f"Sound {'enabled' if enabled else 'disabled'}")
    
    def _show_help(self):
        """
        Show help dialog
        鏄剧ず甯姪瀵硅瘽妗?
        """
        messagebox.showinfo(
            "How to Play",
            "1. Black plays first\n"
            "2. Players take turns placing pieces\n"
            "3. Get five in a row to win\n"
            "4. Pieces can be placed horizontally, vertically, or diagonally"
        )
        logger.debug("Help dialog shown")
    
    def _show_about(self):
        """
        Show about dialog
        鏄剧ず鍏充簬瀵硅瘽妗?
        """
        messagebox.showinfo(
            "About Gomoku World",
            "Gomoku World v1.0\n"
            "A classic board game implementation\n"
            "漏 2024 Gomoku World Team"
        )
        logger.debug("About dialog shown") 
