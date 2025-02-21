"""
Global instances for configuration
閰嶇疆鍏ㄥ眬瀹炰緥
"""

from .manager import ConfigManager

# Create global instance
config_manager = ConfigManager()

__all__ = ['config_manager'] 
