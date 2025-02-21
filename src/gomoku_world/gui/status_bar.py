"""
Status bar implementation
鐘舵€佹爮瀹炵幇
"""

import tkinter as tk
from tkinter import ttk

# 浣跨敤鐩稿瀵煎叆
from ..utils.logger import get_logger

logger = get_logger(__name__)

class StatusBar(ttk.Frame):
    """
    Status bar for displaying game information
    鐢ㄤ簬鏄剧ず娓告垙淇℃伅鐨勭姸鎬佹爮
    """
    
    def __init__(self, parent):
        """
        Initialize status bar
        鍒濆鍖栫姸鎬佹爮
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        self._create_widgets()
        self._setup_layout()
        
        # Set initial message
        self.set_message("Ready")
        
        logger.info("Status bar initialized")
    
    def _create_widgets(self):
        """
        Create status bar widgets
        鍒涘缓鐘舵€佹爮缁勪欢
        """
        # Message label
        self.message_label = ttk.Label(
            self,
            text="",
            anchor=tk.W
        )
        
        # Progress bar (for future use)
        self.progress_bar = ttk.Progressbar(
            self,
            mode='indeterminate',
            length=100
        )
        
        logger.debug("Status bar widgets created")
    
    def _setup_layout(self):
        """
        Setup the layout of widgets
        璁剧疆缁勪欢鐨勫竷灞€
        """
        # Add border
        self.configure(relief=tk.SUNKEN, borderwidth=1)
        
        # Layout widgets
        self.message_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        # Progress bar is packed only when needed
        
        logger.debug("Status bar layout completed")
    
    def set_message(self, message: str):
        """
        Set status message
        璁剧疆鐘舵€佹秷鎭?
        
        Args:
            message: Message to display
        """
        self.message_label.configure(text=message)
        logger.debug(f"Status message set to: {message}")
    
    def start_progress(self):
        """
        Start progress bar animation
        鍚姩杩涘害鏉″姩鐢?
        """
        self.progress_bar.pack(side=tk.RIGHT, padx=5)
        self.progress_bar.start()
        logger.debug("Progress bar started")
    
    def stop_progress(self):
        """
        Stop progress bar animation
        鍋滄杩涘害鏉″姩鐢?
        """
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        logger.debug("Progress bar stopped") 
