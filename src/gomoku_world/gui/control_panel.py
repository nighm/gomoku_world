"""
Control panel implementation
鎺у埗闈㈡澘瀹炵幇
"""

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

# 浣跨敤鐩稿瀵煎叆
from ..utils.logger import get_logger

if TYPE_CHECKING:
    from .main_window import GomokuGUI

logger = get_logger(__name__)

class ControlPanel(ttk.Frame):
    """
    Control panel for game operations
    娓告垙鎿嶄綔鎺у埗闈㈡澘
    """
    
    def __init__(self, parent, main_window: 'GomokuGUI'):
        """
        Initialize control panel
        鍒濆鍖栨帶鍒堕潰鏉?
        
        Args:
            parent: Parent widget
            main_window: Main window instance
        """
        super().__init__(parent)
        
        self.main_window = main_window
        
        self._create_widgets()
        self._setup_layout()
        
        logger.info("Control panel initialized")
    
    def _create_widgets(self):
        """
        Create all control widgets
        鍒涘缓鎵€鏈夋帶鍒剁粍浠?
        """
        # Game control buttons
        self.new_game_btn = ttk.Button(
            self,
            text="New Game",
            command=self.main_window.new_game
        )
        
        self.undo_btn = ttk.Button(
            self,
            text="Undo",
            command=self.main_window.undo_move
        )
        
        # Game mode selection
        self.mode_frame = ttk.LabelFrame(self, text="Game Mode")
        self.mode_var = tk.StringVar(value="pvp")
        
        self.pvp_radio = ttk.Radiobutton(
            self.mode_frame,
            text="Player vs Player",
            variable=self.mode_var,
            value="pvp",
            command=self._on_mode_change
        )
        
        self.pvc_radio = ttk.Radiobutton(
            self.mode_frame,
            text="Player vs Computer",
            variable=self.mode_var,
            value="pvc",
            command=self._on_mode_change
        )
        
        # Difficulty selection
        self.difficulty_frame = ttk.LabelFrame(self, text="AI Difficulty")
        self.difficulty_var = tk.StringVar(value="medium")
        
        self.easy_radio = ttk.Radiobutton(
            self.difficulty_frame,
            text="Easy",
            variable=self.difficulty_var,
            value="easy",
            command=self._on_difficulty_change
        )
        
        self.medium_radio = ttk.Radiobutton(
            self.difficulty_frame,
            text="Medium",
            variable=self.difficulty_var,
            value="medium",
            command=self._on_difficulty_change
        )
        
        self.hard_radio = ttk.Radiobutton(
            self.difficulty_frame,
            text="Hard",
            variable=self.difficulty_var,
            value="hard",
            command=self._on_difficulty_change
        )
        
        # Initially disable difficulty selection
        self._update_difficulty_state()
        
        logger.debug("Control widgets created")
    
    def _setup_layout(self):
        """
        Setup the layout of all widgets
        璁剧疆鎵€鏈夌粍浠剁殑甯冨眬
        """
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
        """
        Handle game mode change
        澶勭悊娓告垙妯″紡鍙樻洿
        """
        self._update_difficulty_state()
        # TODO: Implement mode change logic
        logger.info(f"Game mode changed to {self.mode_var.get()}")
    
    def _on_difficulty_change(self):
        """
        Handle difficulty change
        澶勭悊闅惧害鍙樻洿
        """
        # TODO: Implement difficulty change logic
        logger.info(f"AI difficulty changed to {self.difficulty_var.get()}")
    
    def _update_difficulty_state(self):
        """
        Update difficulty selection state
        鏇存柊闅惧害閫夋嫨鐘舵€?
        """
        state = 'normal' if self.mode_var.get() == 'pvc' else 'disabled'
        self.difficulty_frame.configure(state=state)
        self.easy_radio.configure(state=state)
        self.medium_radio.configure(state=state)
        self.hard_radio.configure(state=state) 
