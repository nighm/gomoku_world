"""
Basic game example
基本游戏示例
"""

from gomoku_world.core import Board, Rules
from gomoku_world.gui import GomokuGUI

def main():
    """Run a basic game"""
    # Create and run the game
    game = GomokuGUI()
    game.run()

if __name__ == '__main__':
    main() 