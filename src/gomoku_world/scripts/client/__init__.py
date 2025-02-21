"""
Game client launcher module
游戏客户端启动模块
"""

import sys

from ...gui.main_window import GomokuGUI
from ...utils.logger import setup_logging

def main():
    """Main entry point"""
    try:
        # Setup logging
        setup_logging()
        
        # Start the game
        game = GomokuGUI()
        game.run()
        
    except Exception as e:
        print(f"Error starting game: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 