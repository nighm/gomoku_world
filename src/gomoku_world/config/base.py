"""
Base configuration management system.

基础配置管理系统。
"""

from pathlib import Path
from typing import Dict, Any, Optional, Union
import logging
import yaml
import json

logger = logging.getLogger(__name__)

class ConfigManager:
    """
    Base configuration manager.
    基础配置管理器。
    """
    
    def __init__(self, name: str, default_config: Dict[str, Any]):
        """
        Initialize configuration manager.
        初始化配置管理器。
        
        Args:
            name: Configuration name (e.g., 'game', 'i18n')
                 配置名称（如'game'、'i18n'）
            default_config: Default configuration values
                          默认配置值
        """
        self.name = name
        self.default_config = default_config
        self.config = default_config.copy()
        self.config_dir = Path("config")
        self.config_file = self.config_dir / f"{name}.yaml"
        
        self._load_config()
    
    def _load_config(self) -> None:
        """
        Load configuration from file.
        从文件加载配置。
        """
        try:
            if self.config_file.exists():
                with self.config_file.open("r", encoding="utf-8") as f:
                    user_config = yaml.safe_load(f)
                    if user_config:
                        self._merge_config(user_config)
                logger.debug(f"Loaded configuration from {self.config_file}")
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
    
    def _save_config(self) -> None:
        """
        Save configuration to file.
        保存配置到文件。
        """
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with self.config_file.open("w", encoding="utf-8") as f:
                yaml.dump(self.config, f, allow_unicode=True, indent=2)
            logger.debug(f"Saved configuration to {self.config_file}")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
    
    def _merge_config(self, user_config: Dict[str, Any]) -> None:
        """
        Merge user configuration with defaults.
        合并用户配置和默认配置。
        """
        def merge_dict(base: Dict[str, Any], update: Dict[str, Any]) -> None:
            for key, value in update.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    merge_dict(base[key], value)
                else:
                    base[key] = value
        
        merge_dict(self.config, user_config)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        获取配置值。
        
        Args:
            key: Configuration key (using dot notation for nested keys)
                配置键（使用点号表示嵌套键）
            default: Default value if key not found
                    键不存在时的默认值
        """
        try:
            value = self.config
            for part in key.split("."):
                value = value[part]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any, save: bool = True) -> None:
        """
        Set configuration value.
        设置配置值。
        
        Args:
            key: Configuration key (using dot notation for nested keys)
                配置键（使用点号表示嵌套键）
            value: Configuration value
                   配置值
            save: Whether to save to file after setting
                 设置后是否保存到文件
        """
        try:
            parts = key.split(".")
            config = self.config
            for part in parts[:-1]:
                if part not in config:
                    config[part] = {}
                config = config[part]
            config[parts[-1]] = value
            
            if save:
                self._save_config()
        except Exception as e:
            logger.error(f"Failed to set configuration: {e}")
    
    def update(self, updates: Dict[str, Any], save: bool = True) -> None:
        """
        Update multiple configuration values.
        更新多个配置值。
        """
        for key, value in updates.items():
            self.set(key, value, save=False)
        
        if save:
            self._save_config()
    
    def reset(self, save: bool = True) -> None:
        """
        Reset configuration to defaults.
        重置配置为默认值。
        """
        self.config = self.default_config.copy()
        if save:
            self._save_config()

# Default game configuration / 默认游戏配置
DEFAULT_GAME_CONFIG = {
    "game": {
        "board_size": 15,
        "win_length": 5,
        "ai_enabled": False,
        "ai_difficulty": "medium",
        "network_enabled": False
    },
    "display": {
        "window_size": 800,
        "show_coordinates": True,
        "theme": "light",
        "language": "en"
    },
    "sound": {
        "enabled": True,
        "volume": 0.5,
        "music_enabled": True,
        "music_volume": 0.3
    },
    "debug": {
        "enabled": False,
        "log_level": "INFO"
    }
}

# Default i18n configuration / 默认国际化配置
DEFAULT_I18N_CONFIG = {
    "general": {
        "default_language": "en",
        "fallback_language": "en",
        "translations_dir": "resources/i18n"
    },
    "cache": {
        "enabled": True,
        "ttl": 3600,
        "max_size": 1000
    },
    "network": {
        "enabled": True,
        "update_interval": 3600,
        "timeout": 10
    },
    "format": {
        "default": "json",
        "supported": ["json", "yaml", "ini"]
    },
    "debug": {
        "enabled": False,
        "log_level": "INFO"
    }
}

# Create global instances / 创建全局实例
game_config = ConfigManager("game", DEFAULT_GAME_CONFIG)
i18n_config = ConfigManager("i18n", DEFAULT_I18N_CONFIG)

__all__ = ["ConfigManager", "game_config", "i18n_config"] 