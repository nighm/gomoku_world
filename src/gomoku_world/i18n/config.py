"""
Internationalization (i18n) configuration.

国际化（i18n）配置。
"""
from pathlib import Path
from typing import Dict, Any, Optional

# Default settings / 默认设置
DEFAULT_SETTINGS: Dict[str, Any] = {
    # General settings / 常规设置
    "DEFAULT_LANGUAGE": "en",
    "FALLBACK_LANGUAGE": "en",
    "TRANSLATIONS_DIR": "resources/i18n",
    
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
        Initialize configuration with default values.
        使用默认值初始化配置。
        """
        self._settings = DEFAULT_SETTINGS.copy()
        self._load_user_config()
    
    def _load_user_config(self) -> None:
        """
        Load user configuration from file if exists.
        如果存在用户配置文件则加载。
        """
        config_file = Path("config/i18n.yaml")
        if config_file.exists():
            import yaml
            with config_file.open("r", encoding="utf-8") as f:
                user_config = yaml.safe_load(f)
                if user_config:
                    self._settings.update(user_config)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        获取配置值。
        """
        return self._settings.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.
        设置配置值。
        """
        self._settings[key] = value
    
    def update(self, settings: Dict[str, Any]) -> None:
        """
        Update multiple settings at once.
        一次更新多个设置。
        """
        self._settings.update(settings)
    
    def reset(self) -> None:
        """
        Reset settings to default values.
        将设置重置为默认值。
        """
        self._settings = DEFAULT_SETTINGS.copy()

# Create global config instance / 创建全局配置实例
config = I18nConfig()

__all__ = ["config", "I18nConfig"] 