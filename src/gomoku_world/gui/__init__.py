"""
Gomoku Game GUI Package
浜斿瓙妫嬫父鎴忓浘褰㈢晫闈㈠寘
"""

from .gui import GomokuGUI
from .settings_menu import SettingsMenu

def main():
    """Start the game"""
    gui = GomokuGUI()
    gui.run()

__all__ = ['GomokuGUI', 'SettingsMenu', 'main'] 
