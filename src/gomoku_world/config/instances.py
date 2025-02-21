"""
Global instances for configuration
配置全局实例
"""

from .manager import ConfigManager

# Create global instance
config_manager = ConfigManager()

__all__ = ['config_manager'] 