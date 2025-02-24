"""
Gomoku World - A modern implementation of the classic Gomoku (Five in a Row) game
"""

from ._version import version as __version__

if not __version__:
    __version__ = "2.1.2"

__author__ = "Gomoku World Team"
__email__ = "team@gomokuworld.com"

from .core import Board, Rules, AI, SaveManager, GameSave
from .gui import GomokuGUI
from .utils import get_logger, setup_logging, resource_manager, sound_manager
from .core.platforms import get_platform, PLATFORM
from .config import (
    PACKAGE_NAME, VERSION,
    BOARD_SIZE, WIN_LENGTH,
    DEFAULT_THEME, DEFAULT_LANGUAGE
)

__all__ = [
    # Core components
    'Board', 'Rules', 'AI', 'SaveManager', 'GameSave',
    # GUI components
    'GomokuGUI',
    # Utilities
    'get_logger', 'setup_logging',
    'resource_manager', 'sound_manager',
    # Platform
    'get_platform', 'PLATFORM',
    # Configuration
    'PACKAGE_NAME', 'VERSION',
    'BOARD_SIZE', 'WIN_LENGTH',
    'DEFAULT_THEME', 'DEFAULT_LANGUAGE'
]
