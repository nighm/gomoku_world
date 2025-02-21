"""
Web platform implementation
Web骞冲彴瀹炵幇
""" 

import os
from pathlib import Path
from typing import Optional

from .base import PlatformBase
from ...utils.logger import get_logger

logger = get_logger(__name__)

class WebPlatform(PlatformBase):
    """
    Web platform class
    """
    
    def __init__(self):
        """Initialize web platform"""
        super().__init__()
        self.name = "web"
        logger.info("Web platform initialized")
    
    def _get_config_dir(self) -> Path:
        """
        Get configuration directory
        
        Returns:
            Path: Configuration directory path
        """
        # Web platform uses current directory for configuration
        return Path.cwd() / "config"
    
    def get_font_path(self, font_name: str) -> Optional[str]:
        """
        Get system font path
        
        Args:
            font_name: Font name
            
        Returns:
            Optional[str]: Font path if found
        """
        # Web platform uses bundled fonts
        font_path = Path(__file__).parent.parent.parent.parent / "resources" / "fonts" / font_name
        return str(font_path) if font_path.exists() else None 
