"""
Configuration manager implementation
配置管理器实现

This module provides centralized configuration management for the application.
The ConfigManager class is implemented as a singleton to ensure consistent
configuration across the entire application.

Lifecycle:
1. Initialization: The manager is initialized when first accessed
2. Loading: Configuration is loaded from files or environment
3. Runtime: Configuration can be modified during runtime
4. Cleanup: Resources are released during shutdown

Example:
    >>> from gomoku_world.config.instances import config_manager
    >>> config_manager.set_value('DEBUG', True)
    >>> debug_enabled = config_manager.get_value('DEBUG')
"""

import os
import json
import atexit
from pathlib import Path
from typing import Dict, Any, Optional

from ..utils.logger import get_logger
from ..config import RESOURCES_DIR

logger = get_logger(__name__)

class ConfigManager:
    """
    Configuration manager class
    配置管理器类
    
    This class manages application configuration, providing:
    - Singleton pattern implementation
    - Configuration loading and saving
    - Runtime configuration modification
    - Environment variable integration
    - Configuration validation
    - Automatic cleanup on shutdown
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize configuration manager"""
        if not self._initialized:
            self._config: Dict[str, Any] = {}
            self._config_file = RESOURCES_DIR / "config" / "config.json"
            self._backup_file = RESOURCES_DIR / "config" / "config.backup.json"
            self._load_config()
            self._register_cleanup()
            self._initialized = True
            logger.info("Configuration manager initialized")
    
    def _register_cleanup(self):
        """Register cleanup handler"""
        atexit.register(self.cleanup)
    
    def _load_config(self):
        """Load configuration from file"""
        try:
            if self._config_file.exists():
                with open(self._config_file, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
                logger.info("Configuration loaded from file")
            else:
                self._load_defaults()
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            self._load_defaults()
    
    def _load_defaults(self):
        """Load default configuration"""
        self._config = {
            'BOARD_SIZE': 15,
            'WIN_LENGTH': 5,
            'DEFAULT_THEME': 'light',
            'DEFAULT_LANGUAGE': 'en'
        }
        logger.info("Default configuration loaded")
    
    def get_value(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value
        获取配置值
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Any: Configuration value or default
        """
        return self._config.get(key, default)
    
    def set_value(self, key: str, value: Any):
        """
        Set configuration value
        设置配置值
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config[key] = value
        self._auto_save()
        logger.debug(f"Configuration value set: {key}={value}")
    
    def save_config(self, config: Dict[str, Any]):
        """
        Save configuration
        保存配置
        
        Args:
            config: Configuration dictionary
        """
        try:
            # Create backup of current config
            if self._config_file.exists():
                import shutil
                shutil.copy(self._config_file, self._backup_file)
            
            # Save new config
            self._config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self._config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            self._config = config
            logger.info("Configuration saved")
            
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            # Restore from backup if available
            if self._backup_file.exists():
                self._restore_from_backup()
    
    def _restore_from_backup(self):
        """Restore configuration from backup"""
        try:
            import shutil
            shutil.copy(self._backup_file, self._config_file)
            self._load_config()
            logger.info("Configuration restored from backup")
        except Exception as e:
            logger.error(f"Error restoring configuration: {e}")
    
    def _auto_save(self):
        """Auto save configuration"""
        try:
            self.save_config(self._config)
        except Exception as e:
            logger.error(f"Error auto-saving configuration: {e}")
    
    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration
        加载配置
        
        Returns:
            Dict[str, Any]: Current configuration
        """
        self._load_config()
        return self._config.copy()
    
    def reset(self):
        """Reset configuration to defaults"""
        self._load_defaults()
        self._auto_save()
        logger.info("Configuration reset to defaults")
    
    def cleanup(self):
        """Cleanup resources"""
        try:
            self._auto_save()
            logger.info("Configuration manager cleaned up")
        except Exception as e:
            logger.error(f"Error during configuration cleanup: {e}")
    
    def validate_config(self) -> bool:
        """
        Validate configuration
        验证配置
        
        Returns:
            bool: True if configuration is valid
        """
        required_keys = ['BOARD_SIZE', 'WIN_LENGTH', 'DEFAULT_THEME', 'DEFAULT_LANGUAGE']
        return all(key in self._config for key in required_keys)

# Create global instance
# 创建全局实例
config_manager = ConfigManager() 