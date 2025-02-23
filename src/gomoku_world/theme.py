"""
Theme management module.

主题管理模块。

This module provides functionality for managing and switching between different UI themes.
The themes control colors, styles, and other visual aspects of the application.

本模块提供管理和切换不同UI主题的功能。主题控制应用程序的颜色、样式和其他视觉方面。
"""

from typing import Dict, Any, List, Callable
from .utils.resources import resource_manager
from .utils.logger import get_logger

logger = get_logger(__name__)

class Theme:
    """
    Theme manager class.
    
    主题管理类。
    
    This class handles loading and applying themes to the application UI.
    It provides methods for getting theme colors and switching between themes.
    
    此类处理加载和应用主题到应用程序UI。
    它提供获取主题颜色和切换主题的方法。
    """
    
    def __init__(self):
        """
        Initialize theme manager.
        
        初始化主题管理器。
        """
        self._theme = resource_manager.get_theme()
        self._current_theme = "default"
        self._available_themes = ["default", "dark", "light"]
        self._change_listeners = []  # Add change listeners list
    
    def add_change_listener(self, listener: Callable[[], None]):
        """
        Add a theme change listener.
        添加主题变更监听器。
        
        Args:
            listener: Callback function to be called when theme changes
                     当主题变更时要调用的回调函数
        """
        if listener not in self._change_listeners:
            self._change_listeners.append(listener)
    
    def remove_change_listener(self, listener: Callable[[], None]):
        """
        Remove a theme change listener.
        移除主题变更监听器。
        
        Args:
            listener: Callback function to remove
                     要移除的回调函数
        """
        if listener in self._change_listeners:
            self._change_listeners.remove(listener)
    
    def _notify_listeners(self):
        """
        Notify all listeners about theme change.
        通知所有监听器主题已变更。
        """
        for listener in self._change_listeners:
            try:
                listener()
            except Exception as e:
                logger.error(f"Error in theme change listener: {e}")
    
    @property
    def current_theme(self) -> str:
        """
        Get current theme name.
        
        获取当前主题名称。
        
        Returns:
            str: Current theme name.
                 当前主题名称。
        """
        return self._current_theme
    
    @property
    def available_themes(self) -> List[str]:
        """
        Get list of available themes.
        
        获取可用主题列表。
        
        Returns:
            List[str]: List of available theme names.
                       可用主题名称列表。
        """
        return self._available_themes
    
    def get_color(self, key: str) -> str:
        """
        Get color by key.
        
        通过键获取颜色。
        
        Args:
            key: Color key in dot notation (e.g. 'board.background').
                 以点号分隔的颜色键（例如'board.background'）。
                
        Returns:
            str: Color value in hex format (e.g. '#FFFFFF').
                 十六进制格式的颜色值（例如'#FFFFFF'）。
        """
        # Split key by dots / 按点号分割键
        parts = key.split('.')
        value = self._theme
        
        # Navigate through nested dictionary / 遍历嵌套字典
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return "#000000"  # Default color / 默认颜色
                
        return value if isinstance(value, str) else "#000000"
    
    def set_theme(self, theme_name: str):
        """
        Set current theme.
        
        设置当前主题。
        
        Args:
            theme_name: Name of the theme to apply.
                       要应用的主题名称。
        """
        if theme_name in self._available_themes:
            self._current_theme = theme_name
            # TODO: Load theme colors from resource manager
            # TODO: 从资源管理器加载主题颜色
            self._notify_listeners()  # Notify listeners about theme change

# Create global theme instance / 创建全局主题实例
theme = Theme()

__all__ = ['theme', 'Theme'] 