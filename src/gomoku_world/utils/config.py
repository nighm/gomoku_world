"""
Configuration module for the Gomoku game.
五子棋游戏配置模块
"""

import json
import os
import logging
from typing import Dict, Any
from .i18n import i18n

logger = logging.getLogger(__name__)

class Config:
    """
    Configuration manager class
    配置管理器类
    """
    
    DEFAULT_CONFIG = {
        'game': {
            'board_size': 15,          # Board size (棋盘大小)
            'win_condition': 5,        # Number of pieces to win (获胜条件)
            'ai_enabled': False,       # Enable AI opponent (启用AI对手)
            'ai_difficulty': 'medium', # AI difficulty (AI难度)
            'network_mode': False,     # Enable network play (启用网络对战)
        },
        'display': {
            'window_size': 800,        # Window size in pixels (窗口大小)
            'show_coordinates': True,  # Show board coordinates (显示坐标)
            'highlight_last': True,    # Highlight last move (高亮最后一手)
            'theme': 'classic',        # UI theme (界面主题)
            'language': 'zh',          # Interface language (界面语言)
        },
        'sound': {
            'enabled': True,           # Enable sound effects (启用音效)
            'volume': 50,              # Sound volume (音量)
            'music_enabled': True,     # Enable background music (启用背景音乐)
            'music_volume': 30,        # Music volume (音乐音量)
        },
        'debug': {
            'enabled': False,          # Enable debug mode (启用调试模式)
            'show_fps': False,         # Show FPS counter (显示帧率)
            'log_level': 'INFO',       # Logging level (日志级别)
        },
        'network': {
            'server': 'localhost',     # Server address (服务器地址)
            'port': 5000,             # Server port (服务器端口)
            'username': '',           # Player username (玩家用户名)
        }
    }
    
    def __init__(self):
        """Initialize configuration manager"""
        self.config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config')
        self.config_file = os.path.join(self.config_dir, 'settings.json')
        self.config = self.DEFAULT_CONFIG.copy()
        self.load_config()
        
        logger.info(i18n.get('config_initialized'))
    
    def load_config(self) -> bool:
        """
        Load configuration from file
        从文件加载配置
        
        Returns:
            bool: True if loaded successfully
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    self._merge_config(saved_config)
                logger.info(i18n.get('config_loaded'))
                return True
        except Exception as e:
            logger.error(f"Error loading config: {e}")
        return False
    
    def save_config(self) -> bool:
        """
        Save configuration to file
        保存配置到文件
        
        Returns:
            bool: True if saved successfully
        """
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            logger.info(i18n.get('config_saved'))
            return True
        except Exception as e:
            logger.error(f"Error saving config: {e}")
        return False
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get configuration value
        获取配置值
        
        Args:
            section: Configuration section (配置部分)
            key: Configuration key (配置键)
            default: Default value if not found (默认值)
        
        Returns:
            Configuration value (配置值)
        """
        try:
            return self.config[section][key]
        except KeyError:
            logger.warning(f"Config key not found: {section}.{key}")
            return default
    
    def set(self, section: str, key: str, value: Any) -> bool:
        """
        Set configuration value
        设置配置值
        
        Args:
            section: Configuration section (配置部分)
            key: Configuration key (配置键)
            value: Configuration value (配置值)
        
        Returns:
            bool: True if set successfully
        """
        try:
            if section not in self.config:
                self.config[section] = {}
            self.config[section][key] = value
            logger.info(i18n.get('config_updated', section, key))
            return True
        except Exception as e:
            logger.error(f"Error setting config: {e}")
            return False
    
    def _merge_config(self, saved_config: Dict[str, Any]):
        """
        Merge saved configuration with defaults
        合并保存的配置与默认配置
        
        Args:
            saved_config: Saved configuration (保存的配置)
        """
        for section, values in saved_config.items():
            if section in self.config:
                self.config[section].update(values)

# Create global instance
config = Config() 