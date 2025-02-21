"""
Gomoku Game GUI Package
五子棋游戏图形界面包
"""

from .gui import GomokuGUI
from .settings_menu import SettingsMenu

def main():
    """Start the game"""
    gui = GomokuGUI()
    gui.run()

__all__ = ['GomokuGUI', 'SettingsMenu', 'main'] 