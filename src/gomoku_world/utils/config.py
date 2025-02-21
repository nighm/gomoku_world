"""
Configuration module for the Gomoku game.
浜斿瓙妫嬫父鎴忛厤缃ā鍧?
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
    閰嶇疆绠＄悊鍣ㄧ被
    """
    
    DEFAULT_CONFIG = {
        'game': {
            'board_size': 15,          # Board size (妫嬬洏澶у皬)
            'win_condition': 5,        # Number of pieces to win (鑾疯儨鏉′欢)
            'ai_enabled': False,       # Enable AI opponent (鍚敤AI瀵规墜)
            'ai_difficulty': 'medium', # AI difficulty (AI闅惧害)
            'network_mode': False,     # Enable network play (鍚敤缃戠粶瀵规垬)
        },
        'display': {
            'window_size': 800,        # Window size in pixels (绐楀彛澶у皬)
            'show_coordinates': True,  # Show board coordinates (鏄剧ず鍧愭爣)
            'highlight_last': True,    # Highlight last move (楂樹寒鏈鍚庝竴鎵?
            'theme': 'classic',        # UI theme (鐣岄潰涓婚)
            'language': 'zh',          # Interface language (鐣岄潰璇█)
        },
        'sound': {
            'enabled': True,           # Enable sound effects (鍚敤闊虫晥)
            'volume': 50,              # Sound volume (闊抽噺)
            'music_enabled': True,     # Enable background music (鍚敤鑳屾櫙闊充箰)
            'music_volume': 30,        # Music volume (闊充箰闊抽噺)
        },
        'debug': {
            'enabled': False,          # Enable debug mode (鍚敤璋冭瘯妯″紡)
            'show_fps': False,         # Show FPS counter (鏄剧ず甯х巼)
            'log_level': 'INFO',       # Logging level (鏃ュ織绾у埆)
        },
        'network': {
            'server': 'localhost',     # Server address (鏈嶅姟鍣ㄥ湴鍧)
            'port': 5000,             # Server port (鏈嶅姟鍣ㄧ鍙?
            'username': '',           # Player username (鐜╁鐢ㄦ埛鍚?
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
        浠庢枃浠跺姞杞介厤缃?
        
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
        淇濆瓨閰嶇疆鍒版枃浠?
        
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
        鑾峰彇閰嶇疆鍊?
        
        Args:
            section: Configuration section (閰嶇疆閮ㄥ垎)
            key: Configuration key (閰嶇疆閿?
            default: Default value if not found (榛樿鍊?
        
        Returns:
            Configuration value (閰嶇疆鍊?
        """
        try:
            return self.config[section][key]
        except KeyError:
            logger.warning(f"Config key not found: {section}.{key}")
            return default
    
    def set(self, section: str, key: str, value: Any) -> bool:
        """
        Set configuration value
        璁剧疆閰嶇疆鍊?
        
        Args:
            section: Configuration section (閰嶇疆閮ㄥ垎)
            key: Configuration key (閰嶇疆閿?
            value: Configuration value (閰嶇疆鍊?
        
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
        鍚堝苟淇濆瓨鐨勯厤缃笌榛樿閰嶇疆
        
        Args:
            saved_config: Saved configuration (淇濆瓨鐨勯厤缃?
        """
        for section, values in saved_config.items():
            if section in self.config:
                self.config[section].update(values)

# Create global instance
config = Config() 
