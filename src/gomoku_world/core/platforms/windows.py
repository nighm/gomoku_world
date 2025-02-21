"""
Windows platform implementation
Windows骞冲彴瀹炵幇
""" 

import os
from pathlib import Path
from typing import Optional

from .base import PlatformBase
from ...utils.logger import get_logger

logger = get_logger(__name__)

class WindowsPlatform(PlatformBase):
    """
    Windows platform class
    """
    
    def __init__(self):
        """Initialize Windows platform"""
        super().__init__()
        self.name = "windows"
        self.fonts_dir = Path(os.environ["WINDIR"]) / "Fonts"
        logger.info(f"Windows platform initialized with fonts directory: {self.fonts_dir}")
    
    def _get_config_dir(self) -> Path:
        """
        Get configuration directory
        
        Returns:
            Path: Configuration directory path
        """
        return Path(os.environ["APPDATA"]) / "Gomoku World"
    
    def get_font_path(self, font_name: str) -> Optional[str]:
        """
        Get system font path
        
        Args:
            font_name: Font name
            
        Returns:
            Optional[str]: Font path if found
        """
        font_path = self.fonts_dir / font_name
        return str(font_path) if font_path.exists() else None 
