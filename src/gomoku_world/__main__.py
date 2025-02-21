"""
Main entry point for the Gomoku World game
五子棋世界游戏的主入口点
"""

import sys
import logging
from pathlib import Path

from .gui.main_window import GomokuGUI
from .utils.logger import setup_logging
from .config import LOG_DIR

def main():
    """
    Main entry point
    主入口点
    """
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Create log directory if it doesn't exist
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        
        # Start the game
        logger.info("Starting Gomoku World")
        game = GomokuGUI()
        game.run()
        
    except Exception as e:
        logger.error(f"Error running game: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main() 