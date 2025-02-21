"""
Configuration settings for the Gomoku game.
"""

# Game settings
BOARD_SIZE = 15  # Standard board size
MIN_BOARD_SIZE = 5  # Minimum allowed board size
WIN_CONDITION = 5  # Number of pieces in a row needed to win

# Display settings
WINDOW_SIZE = 800  # Window size in pixels
GRID_LINE_WIDTH = 1  # Width of grid lines
PIECE_SCALE = 0.8  # Scale factor for piece size relative to grid size

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOARD_COLOR = (222, 184, 135)  # Light wood color
GRID_COLOR = (0, 0, 0)  # Black
HIGHLIGHT_COLOR = (255, 0, 0)  # Red

# Timing
WIN_DISPLAY_TIME = 2000  # Time to display win message (milliseconds)
FPS = 60  # Frames per second

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Development settings
DEBUG = False  # Enable debug mode 
