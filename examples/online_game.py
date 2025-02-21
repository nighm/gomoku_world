"""
Online game example
鍦ㄧ嚎瀵规垬绀轰緥
"""

import asyncio
from gomoku_world.network import NetworkManager
from gomoku_world.gui import GomokuGUI

async def main():
    """Run an online game"""
    # Connect to server
    network = NetworkManager()
    await network.connect()
    
    # Create and run online game
    game = GomokuGUI(game_mode="online")
    game.run()
    
    # Cleanup
    await network.disconnect()

if __name__ == '__main__':
    asyncio.run(main()) 
