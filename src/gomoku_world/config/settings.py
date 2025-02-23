"""
Global settings and constants.
全局设置和常量。
"""

import logging
from pathlib import Path

# Package information / 包信息
PACKAGE_NAME = "gomoku_world"
VERSION = "2.1.0"

# Paths / 路径
BASE_DIR = Path(__file__).parent.parent.parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "gomoku_world.log"
SAVE_DIR = BASE_DIR / "saves"

# Logging / 日志
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = logging.INFO

# Game settings / 游戏设置
BOARD_SIZE = 15
WIN_LENGTH = 5
CELL_SIZE = 40  # Size of each board cell in pixels / 棋盘每个格子的像素大小
PIECE_RADIUS = 15  # Radius of game pieces in pixels / 棋子半径（像素）

# Network settings / 网络设置
SPECTATOR_CHAT_ENABLED = True  # Enable chat in spectator mode / 启用观战模式聊天功能
SPECTATOR_CHAT_HISTORY = 100  # Number of chat messages to keep in history / 保留的聊天记录数量
SPECTATOR_FEATURES = {
    "chat": True,           # Enable chat / 启用聊天
    "analysis": True,       # Enable game analysis / 启用游戏分析
    "replay": True,         # Enable replay controls / 启用回放控制
    "statistics": True,     # Enable statistics display / 启用统计显示
    "notifications": True   # Enable notifications / 启用通知
}

# Display settings / 显示设置
DEFAULT_THEME = "light"
DEFAULT_LANGUAGE = "en"  # English / 英语
FALLBACK_LANGUAGE = "zh-CN"  # Chinese (Simplified) / 简体中文
WINDOW_SIZE = (800, 600)  # Default window size / 默认窗口大小

# Resource paths / 资源路径
RESOURCES_DIR = BASE_DIR / "resources"
TRANSLATIONS_DIR = RESOURCES_DIR / "i18n"
THEMES_DIR = RESOURCES_DIR / "themes"
SOUNDS_DIR = RESOURCES_DIR / "sounds"
IMAGES_DIR = RESOURCES_DIR / "images"

# Create directories if they don't exist / 如果目录不存在则创建
for directory in [LOG_DIR, SAVE_DIR, RESOURCES_DIR, TRANSLATIONS_DIR, THEMES_DIR, SOUNDS_DIR, IMAGES_DIR]:
    directory.mkdir(parents=True, exist_ok=True) 