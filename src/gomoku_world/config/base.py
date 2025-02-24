"""
Base configuration management.
基础配置管理。
"""

from pathlib import Path
from typing import Any, Dict, Optional, Union
import yaml

from .defaults import GAME_DEFAULTS, I18N_DEFAULTS
from .exceptions import ConfigError, ConfigKeyError, ConfigValueError, ConfigTypeError, ConfigRangeError, ConfigEnumError

class ConfigManager:
    """
    Base configuration manager class.
    基础配置管理器类。
    """
    
    def __init__(self, name: str, defaults: Dict[str, Any]):
        """
        Initialize configuration manager.
        初始化配置管理器。
        
        Args:
            name: Configuration name (e.g., 'game', 'i18n')
                 配置名称（例如'game'、'i18n'）
            defaults: Default configuration values
                     默认配置值
        """
        self.name = name
        self._config = defaults.copy()
        self._defaults = defaults.copy()
        self._load_config()
    
    def _load_config(self) -> None:
        """
        Load configuration from file.
        从文件加载配置。
        """
        config_file = Path(f"config/{self.name}.yaml")
        if config_file.exists():
            try:
                with config_file.open("r", encoding="utf-8") as f:
                    user_config = yaml.safe_load(f)
                if user_config:
                    self._merge_config(user_config)
            except Exception as e:
                raise ConfigError(f"Failed to load config: {e}")
    
    def _save_config(self) -> None:
        """
        Save configuration to file.
        保存配置到文件。
        """
        config_file = Path(f"config/{self.name}.yaml")
        config_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            with config_file.open("w", encoding="utf-8") as f:
                yaml.safe_dump(self._config, f, allow_unicode=True)
        except Exception as e:
            raise ConfigError(f"Failed to save config: {e}")
    
    def _merge_config(self, user_config: Dict[str, Any]) -> None:
        """
        Merge user configuration with defaults.
        合并用户配置和默认配置。
        """
        def merge_dict(base: Dict[str, Any], update: Dict[str, Any], prefix: str = "") -> None:
            for key, value in update.items():
                full_key = f"{prefix}.{key}" if prefix else key
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    merge_dict(base[key], value, full_key)
                else:
                    try:
                        if key in base:
                            # Validate the value before merging
                            if isinstance(base[key], (int, float, str, bool)):
                                self.validate(full_key, value)
                        base[key] = value
                    except Exception as e:
                        raise ConfigValueError(key, value, str(e))
        
        merge_dict(self._config, user_config)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        获取配置值。
        
        Args:
            key: Configuration key in dot notation
                 以点号分隔的配置键
            default: Default value if key not found
                     键不存在时的默认值
                     
        Returns:
            Configuration value
            配置值
        """
        try:
            value = self._config
            for part in key.split("."):
                value = value[part]
            return value
        except (KeyError, TypeError):
            if default is not None:
                return default
            raise ConfigKeyError(key)
    
    def set(self, key: str, value: Any, save: bool = True) -> None:
        """
        Set configuration value.
        设置配置值。
        
        Args:
            key: Configuration key in dot notation
                 以点号分隔的配置键
            value: Configuration value
                   配置值
            save: Whether to save to file
                  是否保存到文件
        """
        try:
            # Validate value before setting
            self.validate(key, value)
            
            parts = key.split(".")
            config = self._config
            for part in parts[:-1]:
                if part not in config:
                    config[part] = {}
                config = config[part]
            config[parts[-1]] = value
            if save:
                self._save_config()
        except Exception as e:
            raise ConfigValueError(key, value, str(e))
    
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
        self._config = self._defaults.copy()
        if save:
            self._save_config()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        将配置转换为字典。
        """
        return self._config.copy()
    
    def export(self, file_path: Union[str, Path]) -> None:
        """
        Export configuration to a file.
        导出配置到文件。
        
        Args:
            file_path: Path to export the configuration
                      导出配置的文件路径
        """
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with file_path.open("w", encoding="utf-8") as f:
                yaml.safe_dump(self._config, f, allow_unicode=True)
        except Exception as e:
            raise ConfigError(f"Failed to export config: {e}")
    
    def validate(self, key: str, value: Any) -> bool:
        """
        Validate configuration value.
        验证配置值。
        
        Args:
            key: Configuration key
                 配置键
            value: Configuration value to validate
                   要验证的配置值
                   
        Returns:
            bool: True if valid, False otherwise
            
        Raises:
            ConfigValueError: If validation fails
        """
        try:
            parts = key.split(".")
            current = self._defaults
            for part in parts:
                current = current[part]
            
            # Type validation
            if not isinstance(value, type(current)):
                raise ConfigTypeError(key, value, type(current))
            
            # Range validation for numeric values
            if isinstance(value, (int, float)):
                if key == "sound.volume" and not (0 <= value <= 100):
                    raise ConfigRangeError(key, value, 0, 100)
                elif key == "board.size" and not (5 <= value <= 19):
                    raise ConfigRangeError(key, value, 5, 19)
            
            # Enum validation for string values
            if isinstance(value, str):
                if key == "display.theme" and value not in ["light", "dark"]:
                    raise ConfigEnumError(key, value, ["light", "dark"])
                elif key == "ai.difficulty" and value not in ["easy", "medium", "hard"]:
                    raise ConfigEnumError(key, value, ["easy", "medium", "hard"])
                elif key == "debug.log_level" and value not in ["DEBUG", "INFO", "WARNING", "ERROR"]:
                    raise ConfigEnumError(key, value, ["DEBUG", "INFO", "WARNING", "ERROR"])
            
            return True
        except KeyError:
            raise ConfigKeyError(key)
        except (ConfigTypeError, ConfigRangeError, ConfigEnumError) as e:
            raise ConfigValueError(key, value, str(e))
        except Exception as e:
            raise ConfigValueError(key, value, str(e))

# Create global instances
game_config = ConfigManager("game", GAME_DEFAULTS)
i18n_config = ConfigManager("i18n", I18N_DEFAULTS)

__all__ = ["ConfigManager", "game_config", "i18n_config"]