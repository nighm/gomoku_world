"""
AI game example
AI瀵规垬绀轰緥
"""

from gomoku_world.core import Board, Rules, AI
from gomoku_world.gui import GomokuGUI

def main():
    """Run an AI game"""
    # Create game with AI opponent
    game = GomokuGUI(game_mode="pvc")
    game.run()

if __name__ == '__main__':
    main() 
