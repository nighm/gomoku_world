"""
Font management module for the Gomoku World game.

五子棋世界游戏的字体管理模块。

This module provides font management functionality:
- Font registration and loading
- Fallback font support
- Script-specific font handling (Latin, CJK)
- Platform-specific font paths

本模块提供字体管理功能：
- 字体注册和加载
- 后备字体支持
- 特定文字系统的字体处理（拉丁文、中日韩文）
- 特定平台的字体路径
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
from ..core.platforms import PLATFORM
from .logger import get_logger

logger = get_logger(__name__)

class FontManager:
    """
    Font manager class for handling font loading and fallback.
    
    字体管理器类，用于处理字体加载和后备字体。
    
    This class provides:
    - Font registration and path management
    - Script-specific font fallbacks
    - Font preloading
    - Platform-specific font handling
    
    此类提供：
    - 字体注册和路径管理
    - 特定文字系统的后备字体
    - 字体预加载
    - 特定平台的字体处理
    """
    
    def __init__(self):
        """
        Initialize font manager.
        
        初始化字体管理器。
        """
        self._fonts: Dict[str, Dict[str, str]] = {}
        self._fallbacks: Dict[str, List[str]] = {
            "latin": ["Arial", "Helvetica", "sans-serif"],  # Latin script fonts / 拉丁文字体
            "cjk": ["Microsoft YaHei", "SimHei", "Noto Sans CJK", "sans-serif"]  # CJK fonts / 中日韩文字体
        }
        self._preloaded: Dict[str, bool] = {}
        
    def register_font(self, name: str, path: str, script: str = "latin"):
        """
        Register a font with the manager.
        
        向管理器注册字体。
        
        Args:
            name (str): Font name.
                       字体名称。
            path (str): Font file path.
                       字体文件路径。
            script (str): Script type ('latin' or 'cjk', default: 'latin').
                        文字系统类型（'latin'或'cjk'，默认：'latin'）。
        """
        if not os.path.exists(path):
            logger.warning(f"Font file not found / 未找到字体文件: {path}")
            return
            
        self._fonts[name] = {
            "path": path,
            "script": script
        }
        logger.info(f"Registered font / 已注册字体: {name} ({script})")
        
    def get_font(self, name: str) -> Optional[str]:
        """
        Get font path by name.
        
        通过名称获取字体路径。
        
        Args:
            name (str): Font name.
                       字体名称。
                       
        Returns:
            Optional[str]: Font file path if found, None otherwise.
                          如果找到则返回字体文件路径，否则返回None。
        """
        if name in self._fonts:
            return self._fonts[name]["path"]
            
        # Try platform-specific font paths / 尝试特定平台的字体路径
        platform_paths = PLATFORM.get_font_paths(name)
        for path in platform_paths:
            if os.path.exists(path):
                return path
                
        logger.warning(f"Font not found / 未找到字体: {name}")
        return None
        
    def get_fallback_fonts(self, script: str = "latin") -> List[str]:
        """
        Get fallback fonts for a script.
        
        获取文字系统的后备字体。
        
        Args:
            script (str): Script type ('latin' or 'cjk', default: 'latin').
                        文字系统类型（'latin'或'cjk'，默认：'latin'）。
                        
        Returns:
            List[str]: List of fallback font names.
                      后备字体名称列表。
        """
        return self._fallbacks.get(script, self._fallbacks["latin"])
        
    def preload_fonts(self):
        """
        Preload registered fonts.
        
        预加载已注册的字体。
        
        This ensures fonts are available when needed and
        prevents loading delays during gameplay.
        
        这确保字体在需要时可用，并防止
        在游戏过程中出现加载延迟。
        """
        for name, font_info in self._fonts.items():
            if name not in self._preloaded:
                try:
                    # Platform-specific font loading / 特定平台的字体加载
                    PLATFORM.load_font(font_info["path"])
                    self._preloaded[name] = True
                    logger.info(f"Preloaded font / 已预加载字体: {name}")
                except Exception as e:
                    logger.error(f"Failed to preload font / 预加载字体失败 {name}: {e}")

# Create global font manager instance / 创建全局字体管理器实例
font_manager = FontManager()

__all__ = ['font_manager', 'FontManager'] 