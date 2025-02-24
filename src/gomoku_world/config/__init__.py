"""
Configuration management system.

配置管理系统。

This package provides a unified configuration management system for the Gomoku World project.
Features:
- YAML-based configuration files
- Default configurations for game and i18n
- Dot notation for accessing nested configuration values
- Configuration persistence
- Automatic merging of user configurations with defaults
- Type hints and bilingual documentation

本包为五子棋世界项目提供统一的配置管理系统。
特性：
- 基于YAML的配置文件
- 游戏和国际化的默认配置
- 使用点号表示法访问嵌套配置值
- 配置持久化
- 自动合并用户配置和默认配置
- 类型提示和双语文档
"""

from .base import ConfigManager, game_config, i18n_config
from .settings import (
    PACKAGE_NAME, VERSION,
    LOG_DIR, LOG_FILE, LOG_FORMAT, LOG_LEVEL,
    BOARD_SIZE, WIN_LENGTH, CELL_SIZE, PIECE_RADIUS,
    DEFAULT_THEME, DEFAULT_LANGUAGE, FALLBACK_LANGUAGE,
    RESOURCES_DIR, TRANSLATIONS_DIR, THEMES_DIR, SOUNDS_DIR, IMAGES_DIR,
    SAVE_DIR, WINDOW_SIZE, 
    # Network settings
    SPECTATOR_CHAT_ENABLED, SPECTATOR_CHAT_HISTORY, SPECTATOR_FEATURES,
    # AI settings
    AI_THINKING_TIME, AI_CACHE_SIZE,
    AI_DEPTH_EASY, AI_DEPTH_MEDIUM, AI_DEPTH_HARD,
    # Network settings
    NETWORK_CHECK_TIMEOUT, NETWORK_RETRY_INTERVAL, NETWORK_MAX_RETRIES,
    # Debug settings
    DEBUG_ENABLED, DEBUG_LOG_LEVEL
)

__all__ = [
    # Configuration managers
    "ConfigManager", "game_config", "i18n_config",
    # Package information
    "PACKAGE_NAME", "VERSION",
    # Logging
    "LOG_DIR", "LOG_FILE", "LOG_FORMAT", "LOG_LEVEL",
    # Game settings
    "BOARD_SIZE", "WIN_LENGTH", "CELL_SIZE", "PIECE_RADIUS",
    # Display settings
    "DEFAULT_THEME", "DEFAULT_LANGUAGE", "FALLBACK_LANGUAGE", "WINDOW_SIZE",
    # Network settings
    "SPECTATOR_CHAT_ENABLED", "SPECTATOR_CHAT_HISTORY", "SPECTATOR_FEATURES",
    # Resource paths
    "RESOURCES_DIR", "TRANSLATIONS_DIR", "THEMES_DIR", "SOUNDS_DIR", "IMAGES_DIR",
    "SAVE_DIR",
    # AI settings
    "AI_THINKING_TIME", "AI_CACHE_SIZE",
    "AI_DEPTH_EASY", "AI_DEPTH_MEDIUM", "AI_DEPTH_HARD",
    # Network settings
    "NETWORK_CHECK_TIMEOUT", "NETWORK_RETRY_INTERVAL", "NETWORK_MAX_RETRIES",
    # Debug settings
    "DEBUG_ENABLED", "DEBUG_LOG_LEVEL"
]
