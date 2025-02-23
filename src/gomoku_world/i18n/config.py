"""
Internationalization (i18n) configuration.

国际化（i18n）配置。
"""
from pathlib import Path
from typing import Dict, Any, Optional

from ..config.settings import TRANSLATIONS_DIR

# Default settings / 默认设置
DEFAULT_SETTINGS: Dict[str, Any] = {
    # General settings / 常规设置
    "DEFAULT_LANGUAGE": "en",
    "FALLBACK_LANGUAGE": "en",
    "TRANSLATIONS_DIR": str(TRANSLATIONS_DIR),
    
    # Cache settings / 缓存设置
    "CACHE_ENABLED": True,
    "CACHE_TTL": 3600,  # seconds / 秒
    "CACHE_MAX_SIZE": 1000,
    
    # Network settings / 网络设置
    "ONLINE_FEATURES_ENABLED": True,
    "UPDATE_CHECK_INTERVAL": 3600,  # seconds / 秒
    "NETWORK_TIMEOUT": 10,  # seconds / 秒
    
    # Format settings / 格式设置
    "DEFAULT_FORMAT": "json",
    "SUPPORTED_FORMATS": ["json", "yaml", "ini"],
    
    # Debug settings / 调试设置
    "DEBUG": False,
    "LOG_LEVEL": "INFO",
}

class I18nConfig:
    """
    Configuration manager for i18n settings.
    国际化设置配置管理器。
    """
    _instance: Optional["I18nConfig"] = None
    _settings: Dict[str, Any] = {}
    
    def __new__(cls) -> "I18nConfig":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self) -> None:
        """
        Initialize configuration with default settings.
        使用默认设置初始化配置。
        """
        self._settings = DEFAULT_SETTINGS.copy()
    
    @property
    def translations_dir(self) -> str:
        """
        Get translations directory path.
        获取翻译目录路径。
        """
        return self._settings["TRANSLATIONS_DIR"]
    
    @property
    def default_language(self) -> str:
        """
        Get default language code.
        获取默认语言代码。
        """
        return self._settings["DEFAULT_LANGUAGE"]
    
    @property
    def fallback_language(self) -> str:
        """
        Get fallback language code.
        获取回退语言代码。
        """
        return self._settings["FALLBACK_LANGUAGE"]
    
    @property
    def cache_enabled(self) -> bool:
        """
        Check if cache is enabled.
        检查是否启用缓存。
        """
        return self._settings["CACHE_ENABLED"]
    
    @property
    def cache_ttl(self) -> int:
        """
        Get cache TTL in seconds.
        获取缓存TTL（秒）。
        """
        return self._settings["CACHE_TTL"]
    
    @property
    def cache_max_size(self) -> int:
        """
        Get maximum cache size.
        获取最大缓存大小。
        """
        return self._settings["CACHE_MAX_SIZE"]
    
    @property
    def online_features_enabled(self) -> bool:
        """
        Check if online features are enabled.
        检查是否启用在线功能。
        """
        return self._settings["ONLINE_FEATURES_ENABLED"]
    
    @property
    def debug(self) -> bool:
        """
        Check if debug mode is enabled.
        检查是否启用调试模式。
        """
        return self._settings["DEBUG"]
    
    @property
    def log_level(self) -> str:
        """
        Get log level.
        获取日志级别。
        """
        return self._settings["LOG_LEVEL"]
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.
        通过键获取配置值。
        
        Args:
            key: Configuration key
                 配置键
            default: Default value if key not found
                    如果未找到键则返回的默认值
        """
        return self._settings.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value by key.
        通过键设置配置值。
        
        Args:
            key: Configuration key
                 配置键
            value: Configuration value
                  配置值
        """
        self._settings[key] = value

# Create singleton instance / 创建单例实例
config = I18nConfig()

__all__ = ["config", "I18nConfig"] 