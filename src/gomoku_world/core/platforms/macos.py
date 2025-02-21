"""
macOS platform implementation
macOS骞冲彴瀹炵幇
""" 

import os
from pathlib import Path
from typing import Optional

from .base import PlatformBase
from ...utils.logger import get_logger

logger = get_logger(__name__)

class MacOSPlatform(PlatformBase):
    """
    macOS platform class
    """
    
    def __init__(self):
        """Initialize macOS platform"""
        super().__init__()
        self.name = "macos"
        self.fonts_dir = Path.home() / "Library" / "Fonts"
        logger.info(f"macOS platform initialized with fonts directory: {self.fonts_dir}")
    
    def _get_config_dir(self) -> Path:
        """
        Get configuration directory
        
        Returns:
            Path: Configuration directory path
        """
        return Path.home() / "Library" / "Application Support" / "Gomoku World"
    
    def get_font_path(self, font_name: str) -> Optional[str]:
        """
        Get system font path
        
        Args:
            font_name: Font name
            
        Returns:
            Optional[str]: Font path if found
        """
        # Check user fonts directory
        font_path = self.fonts_dir / font_name
        if font_path.exists():
            return str(font_path)
            
        # Check system fonts directory
        system_font_path = Path("/System/Library/Fonts") / font_name
        return str(system_font_path) if system_font_path.exists() else None 
