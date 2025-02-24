"""
Global settings and constants.
全局设置和常量。
"""

import logging
from pathlib import Path

# Package information / 包信息
PACKAGE_NAME = "gomoku_world"
VERSION = "2.1.2"

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

# AI settings / AI设置
AI_THINKING_TIME = 5.0  # Maximum thinking time in seconds / AI最大思考时间（秒）
AI_CACHE_SIZE = 100000  # Maximum number of cached positions / 最大缓存局面数量
AI_DEPTH_EASY = 2      # Search depth for easy difficulty / 简单难度的搜索深度
AI_DEPTH_MEDIUM = 4    # Search depth for medium difficulty / 中等难度的搜索深度
AI_DEPTH_HARD = 6      # Search depth for hard difficulty / 困难难度的搜索深度

# Network settings / 网络设置
NETWORK_CHECK_TIMEOUT = 5.0  # Network check timeout in seconds / 网络检查超时时间（秒）
NETWORK_CHECK_INTERVAL = 60.0  # Network check interval in seconds / 网络检查间隔时间（秒）
NETWORK_RETRY_INTERVAL = 1.0  # Retry interval in seconds / 重试间隔时间（秒）
NETWORK_MAX_RETRIES = 3      # Maximum number of retries / 最大重试次数
NETWORK_CHECK_HOSTS = [      # Hosts to check for network connectivity / 用于检查网络连接的主机
    "www.google.com",
    "www.github.com",
    "www.baidu.com"
]

# Debug settings / 调试设置
DEBUG_ENABLED = True         # Enable debug mode / 启用调试模式
DEBUG_LOG_LEVEL = "DEBUG"    # Debug log level / 调试日志级别

# Create directories if they don't exist / 如果目录不存在则创建
for directory in [LOG_DIR, SAVE_DIR, RESOURCES_DIR, TRANSLATIONS_DIR, THEMES_DIR, SOUNDS_DIR, IMAGES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)