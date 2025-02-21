"""
Base platform implementation
鍩虹骞冲彴瀹炵幇
""" 

from typing import Optional, Dict, Any
import os
import sys
import logging
from pathlib import Path

from ...utils.logger import get_logger

logger = get_logger(__name__)

class PlatformBase:
    """
    Base platform class
    """
    
    def __init__(self):
        """Initialize platform"""
        self.name = "base"
        self.config_dir = self._get_config_dir()
        logger.info(f"Platform {self.name} initialized")
    
    def _get_config_dir(self) -> Path:
        """
        Get configuration directory
        
        Returns:
            Path: Configuration directory path
        """
        # Default to user home directory
        return Path.home() / ".gomoku_world"
    
    def get_font_path(self, font_name: str) -> Optional[str]:
        """
        Get system font path
        
        Args:
            font_name: Font name
            
        Returns:
            Optional[str]: Font path if found
        """
        return None
    
    def get_resource_path(self, resource_name: str) -> Path:
        """
        Get resource path
        
        Args:
            resource_name: Resource name
            
        Returns:
            Path: Resource path
        """
        return Path(__file__).parent.parent.parent.parent / "resources" / resource_name
    
    def get_config_path(self) -> Path:
        """
        Get configuration file path
        
        Returns:
            Path: Configuration file path
        """
        return self.config_dir / "config.json"
    
    def get_log_path(self) -> Path:
        """
        Get log file path
        
        Returns:
            Path: Log file path
        """
        return self.config_dir / "gomoku_world.log"
    
    def setup(self):
        """Setup platform-specific requirements"""
        # Create config directory if not exists
        os.makedirs(self.config_dir, exist_ok=True)
        logger.info(f"Created config directory: {self.config_dir}")
    
    def cleanup(self):
        """Cleanup platform-specific resources"""
        pass 