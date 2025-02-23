"""
Control panel implementation.

控制面板实现。
"""

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING, Optional

from ..i18n import i18n_manager
from ..utils.logger import get_logger

if TYPE_CHECKING:
    from .main_window import GomokuGUI

logger = get_logger(__name__)

class ControlPanel(ttk.Frame):
    """Control panel widget"""
    
    def __init__(self, parent, main_window: 'GomokuGUI'):
        """
        Initialize control panel.
        
        Args:
            parent: Parent widget
            main_window: Main window instance
        """
        super().__init__(parent)
        self.main_window = main_window
        
        # Create variables
        self.mode_var = tk.StringVar(value="pvp")
        self.difficulty_var = tk.StringVar(value="medium")
        
        # Create widgets
        self._create_widgets()
        
        # Setup layout
        self._setup_layout()
        
        logger.info("Control panel initialized")
    
    def _create_widgets(self):
        """Create control panel widgets"""
        # Game control buttons
        self.new_game_btn = ttk.Button(
            self,
            text=i18n_manager.get_text("game.new"),
            command=self.main_window.start_new_game
        )
        
        self.undo_btn = ttk.Button(
            self,
            text=i18n_manager.get_text("game.undo"),
            command=self.main_window.undo_move
        )
        
        # Game mode selection
        self.mode_frame = ttk.LabelFrame(
            self,
            text=i18n_manager.get_text("game.mode")
        )
        
        self.pvp_radio = ttk.Radiobutton(
            self.mode_frame,
            text=i18n_manager.get_text("game.mode.pvp"),
            variable=self.mode_var,
            value="pvp",
            command=self._on_mode_change
        )
        
        self.pvc_radio = ttk.Radiobutton(
            self.mode_frame,
            text=i18n_manager.get_text("game.mode.pvc"),
            variable=self.mode_var,
            value="pvc",
            command=self._on_mode_change
        )
        
        # Difficulty selection
        self.difficulty_frame = ttk.LabelFrame(
            self,
            text=i18n_manager.get_text("game.difficulty")
        )
        
        self.easy_radio = ttk.Radiobutton(
            self.difficulty_frame,
            text=i18n_manager.get_text("game.difficulty.easy"),
            variable=self.difficulty_var,
            value="easy",
            command=self._on_difficulty_change
        )
        
        self.medium_radio = ttk.Radiobutton(
            self.difficulty_frame,
            text=i18n_manager.get_text("game.difficulty.medium"),
            variable=self.difficulty_var,
            value="medium",
            command=self._on_difficulty_change
        )
        
        self.hard_radio = ttk.Radiobutton(
            self.difficulty_frame,
            text=i18n_manager.get_text("game.difficulty.hard"),
            variable=self.difficulty_var,
            value="hard",
            command=self._on_difficulty_change
        )
        
        # Update difficulty state
        self._update_difficulty_state()
    
    def _setup_layout(self):
        """Setup the layout of all widgets"""
        # Game control buttons
        self.new_game_btn.pack(fill=tk.X, padx=5, pady=5)
        self.undo_btn.pack(fill=tk.X, padx=5, pady=5)
        
        # Game mode selection
        self.mode_frame.pack(fill=tk.X, padx=5, pady=5)
        self.pvp_radio.pack(anchor=tk.W, padx=5, pady=2)
        self.pvc_radio.pack(anchor=tk.W, padx=5, pady=2)
        
        # Difficulty selection
        self.difficulty_frame.pack(fill=tk.X, padx=5, pady=5)
        self.easy_radio.pack(anchor=tk.W, padx=5, pady=2)
        self.medium_radio.pack(anchor=tk.W, padx=5, pady=2)
        self.hard_radio.pack(anchor=tk.W, padx=5, pady=2)
        
        logger.debug("Layout setup completed")
    
    def _on_mode_change(self):
        """Handle game mode change"""
        self._update_difficulty_state()
        logger.info(f"Game mode changed to {self.mode_var.get()}")
    
    def _on_difficulty_change(self):
        """Handle difficulty change"""
        logger.info(f"AI difficulty changed to {self.difficulty_var.get()}")
    
    def _update_difficulty_state(self):
        """Update difficulty selection state"""
        state = 'normal' if self.mode_var.get() == 'pvc' else 'disabled'
        self.easy_radio.configure(state=state)
        self.medium_radio.configure(state=state)
        self.hard_radio.configure(state=state)
    
    def update_language(self):
        """Update all text elements when language changes"""
        # Update mode selection
        self.mode_frame["text"] = i18n_manager.get_text("game.mode")
        self.pvp_radio["text"] = i18n_manager.get_text("game.mode.pvp")
        self.pvc_radio["text"] = i18n_manager.get_text("game.mode.pvc")
        
        # Update difficulty selection
        self.difficulty_frame["text"] = i18n_manager.get_text("game.difficulty")
        self.easy_radio["text"] = i18n_manager.get_text("game.difficulty.easy")
        self.medium_radio["text"] = i18n_manager.get_text("game.difficulty.medium")
        self.hard_radio["text"] = i18n_manager.get_text("game.difficulty.hard")
        
        # Update buttons
        self.new_game_btn["text"] = i18n_manager.get_text("game.new")
        self.undo_btn["text"] = i18n_manager.get_text("game.undo") 
