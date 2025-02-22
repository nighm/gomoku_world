"""
Global configuration module
鍏ㄥ眬閰嶇疆妯″潡
"""

from pathlib import Path

# Package information
PACKAGE_NAME = "Gomoku World"
VERSION = "1.4.0"

# Directory paths
ROOT_DIR = Path(__file__).parent.parent.parent.parent
SRC_DIR = ROOT_DIR / "src"
RESOURCES_DIR = ROOT_DIR / "resources"
LOG_DIR = ROOT_DIR / "logs"
SAVE_DIR = ROOT_DIR / "saves"

# Game settings
BOARD_SIZE = 15
WIN_LENGTH = 5

# Resource defaults
DEFAULT_THEME = "light"
DEFAULT_LANGUAGE = "en"

# Logging configuration
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"
LOG_FILE = LOG_DIR / "gomoku_world.log"

# GUI settings
WINDOW_SIZE = "800x600"
CELL_SIZE = 40
PIECE_RADIUS = 18

# Network settings
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 5000

# AI settings
AI_DIFFICULTY_LEVELS = ["easy", "medium", "hard"]
DEFAULT_AI_DIFFICULTY = "medium"
AI_THINKING_TIME = 2.0  # seconds

# Save settings
AUTO_SAVE_INTERVAL = 5  # minutes
MAX_AUTO_SAVES = 5
MAX_SAVE_FILES = 100
SAVE_FILE_FORMAT = "json"

# Leaderboard settings
INITIAL_RATING = 1500
K_FACTOR = 32
RATING_FLOOR = 100
RATING_CHANGES = {
    "win": 25,
    "loss": -20,
    "draw": 5
}
LEADERBOARD_CATEGORIES = ["rating", "wins", "streak"]
LEADERBOARD_LIMIT = 100
ACTIVE_DAYS = 30
INACTIVE_PENALTY = 5  # rating points per day

# Spectator settings
MAX_SPECTATORS_PER_GAME = 50
SPECTATOR_UPDATE_INTERVAL = 1.0  # seconds
SPECTATOR_CHAT_ENABLED = True
SPECTATOR_CHAT_HISTORY = 100
SPECTATOR_FEATURES = {
    "chat": True,
    "game_info": True,
    "player_stats": True,
    "move_history": True
}

# Create necessary directories
LOG_DIR.mkdir(exist_ok=True)
RESOURCES_DIR.mkdir(exist_ok=True)
SAVE_DIR.mkdir(exist_ok=True) 
