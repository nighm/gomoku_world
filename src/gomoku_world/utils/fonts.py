"""
Font management module
字体管理模块
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
from ..core.platforms import PLATFORM
from .logger import get_logger

logger = get_logger(__name__)

class FontManager:
    """Font manager class for handling font loading and fallback"""
    
    def __init__(self):
        """Initialize font manager"""
        self._fonts: Dict[str, Dict[str, str]] = {}
        self._fallbacks: Dict[str, List[str]] = {
            "latin": ["Arial", "Helvetica", "sans-serif"],
            "cjk": ["Microsoft YaHei", "SimHei", "Noto Sans CJK", "sans-serif"]
        }
        self._preloaded: Dict[str, bool] = {}
        
    def register_font(self, name: str, path: str, script: str = "latin"):
        """
        Register a font
        
        Args:
            name: Font name
            path: Font file path
            script: Script type (latin, cjk)
        """
        if not os.path.exists(path):
            logger.warning(f"Font file not found: {path}")
            return
            
        self._fonts[name] = {
            "path": path,
            "script": script
        }
        logger.info(f"Registered font: {name} ({script})")
        
    def get_font(self, name: str) -> Optional[str]:
        """
        Get font path by name
        
        Args:
            name: Font name
            
        Returns:
            Optional[str]: Font path if found
        """
        # Check registered fonts
        if name in self._fonts:
            return self._fonts[name]["path"]
            
        # Try system font
        system_font = PLATFORM.get_font_path(name)
        if system_font:
            return system_font
            
        return None
        
    def get_fallback_fonts(self, script: str = "latin") -> List[str]:
        """
        Get fallback fonts for script
        
        Args:
            script: Script type
            
        Returns:
            List[str]: List of fallback font names
        """
        return self._fallbacks.get(script, self._fallbacks["latin"])
        
    def preload_fonts(self):
        """Preload registered fonts"""
        for name, font_info in self._fonts.items():
            if name not in self._preloaded:
                try:
                    # Here we would actually preload the font
                    # Implementation depends on the GUI framework
                    self._preloaded[name] = True
                    logger.info(f"Preloaded font: {name}")
                except Exception as e:
                    logger.error(f"Failed to preload font {name}: {e}")

# Create global font manager instance
font_manager = FontManager() 