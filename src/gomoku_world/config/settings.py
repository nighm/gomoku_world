"""
Global configuration settings module for the Gomoku World game.

五子棋世界游戏的全局配置设置模块。

This module defines all global configuration settings including:
- Package information and versioning
- File system paths and directories
- Network and API configurations
- Game rules and parameters
- GUI settings and dimensions
- Logging configuration
- Resource paths and defaults

本模块定义所有全局配置设置，包括：
- 包信息和版本控制
- 文件系统路径和目录
- 网络和API配置
- 游戏规则和参数
- 图形界面设置和尺寸
- 日志配置
- 资源路径和默认值
"""

from pathlib import Path
import os
from .. import __version__

# Package information / 包信息
PACKAGE_NAME = "Gomoku World"
VERSION = __version__

# Translation service settings / 翻译服务设置
TRANSLATION_SERVICE_URL = "https://api.translations.gomokuworld.org"
TRANSLATION_API_KEY = None  # Set this in local_settings.py / 在local_settings.py中设置
TRANSLATION_CACHE_DIR = Path.home() / ".gomoku_world" / "cache" / "translations"
TRANSLATION_TIMEOUT = 5  # seconds / 秒
TRANSLATION_CACHE_TTL = 86400  # 24 hours in seconds / 24小时（秒）

# Network settings / 网络设置
NETWORK_CHECK_TIMEOUT = 1  # seconds / 秒
NETWORK_CHECK_INTERVAL = 30  # seconds / 秒
NETWORK_MAX_RETRIES = 3
NETWORK_RETRY_DELAY = 5  # seconds / 秒
NETWORK_CHECK_HOSTS = [
    "api.translations.gomokuworld.org",  # Primary service / 主要服务
    "8.8.8.8"  # Google DNS as fallback / Google DNS作为后备
]
NETWORK_PROXY_SETTINGS = {
    "http": os.getenv("HTTP_PROXY"),
    "https": os.getenv("HTTPS_PROXY")
}

# Directory paths / 目录路径
ROOT_DIR = Path(__file__).parent.parent.parent.parent  # Project root / 项目根目录
SRC_DIR = ROOT_DIR / "src"  # Source code / 源代码
RESOURCES_DIR = ROOT_DIR / "resources"  # Game resources / 游戏资源
LOG_DIR = ROOT_DIR / "logs"  # Log files / 日志文件
SAVE_DIR = ROOT_DIR / "saves"  # Game saves / 游戏存档
CONFIG_DIR = ROOT_DIR / "config"  # Configuration files / 配置文件
CACHE_DIR = ROOT_DIR / "cache"  # Cache directory / 缓存目录

# Game settings / 游戏设置
BOARD_SIZE = 15  # Standard board size / 标准棋盘大小
WIN_LENGTH = 5  # Number of pieces to win / 获胜所需棋子数
MAX_GAME_TIME = 3600  # Maximum game duration (seconds) / 最大游戏时长（秒）
MOVE_TIME_LIMIT = 30  # Time limit per move (seconds) / 每步时间限制（秒）

# Resource defaults / 资源默认值
DEFAULT_THEME = "light"  # Default UI theme / 默认界面主题
DEFAULT_LANGUAGE = "en"  # Default language / 默认语言
SUPPORTED_LANGUAGES = ["en", "zh", "ja", "ko"]  # Supported languages / 支持的语言
SUPPORTED_THEMES = ["light", "dark", "classic"]  # Supported themes / 支持的主题

# Logging configuration / 日志配置
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"  # Default log level / 默认日志级别
LOG_FILE = LOG_DIR / "gomoku_world.log"  # Log file path / 日志文件路径
LOG_BACKUP_COUNT = 5  # Number of backup log files / 备份日志文件数量
LOG_MAX_BYTES = 1024 * 1024  # 1MB per log file / 每个日志文件1MB

# GUI settings / 图形界面设置
WINDOW_SIZE = "800x600"  # Default window size / 默认窗口大小
CELL_SIZE = 40  # Board cell size (pixels) / 棋盘格子大小（像素）
PIECE_RADIUS = 18  # Game piece radius (pixels) / 棋子半径（像素）
ANIMATION_SPEED = 200  # Animation duration (ms) / 动画持续时间（毫秒）
FONT_SIZE = 12  # Default font size / 默认字体大小

# AI settings / AI设置
AI_THINKING_TIME = 2.0  # Maximum AI thinking time (seconds) / 最大AI思考时间（秒）
AI_DEPTH_LIMIT = 4  # Maximum search depth / 最大搜索深度
AI_DIFFICULTY_LEVELS = ["easy", "medium", "hard"]  # Difficulty levels / 难度级别

# Try to load local settings / 尝试加载本地设置
try:
    from .local_settings import *  # noqa
except ImportError:
    pass  # Use defaults if no local settings / 如果没有本地设置则使用默认值

# Ensure required directories exist / 确保必需的目录存在
for directory in [LOG_DIR, SAVE_DIR, CACHE_DIR, CONFIG_DIR]:
    directory.mkdir(parents=True, exist_ok=True) 
