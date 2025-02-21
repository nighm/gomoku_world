"""
Status bar implementation
状态栏实现
"""

import tkinter as tk
from tkinter import ttk

# 使用相对导入
from ..utils.logger import get_logger

logger = get_logger(__name__)

class StatusBar(ttk.Frame):
    """
    Status bar for displaying game information
    用于显示游戏信息的状态栏
    """
    
    def __init__(self, parent):
        """
        Initialize status bar
        初始化状态栏
        
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
        创建状态栏组件
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
        设置组件的布局
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
        设置状态消息
        
        Args:
            message: Message to display
        """
        self.message_label.configure(text=message)
        logger.debug(f"Status message set to: {message}")
    
    def start_progress(self):
        """
        Start progress bar animation
        启动进度条动画
        """
        self.progress_bar.pack(side=tk.RIGHT, padx=5)
        self.progress_bar.start()
        logger.debug("Progress bar started")
    
    def stop_progress(self):
        """
        Stop progress bar animation
        停止进度条动画
        """
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        logger.debug("Progress bar stopped") 