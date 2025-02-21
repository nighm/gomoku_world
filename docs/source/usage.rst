Usage
=====

Basic Game
---------

To start a basic game against another player::

    from gomoku_world.gui import GomokuGUI
    
    game = GomokuGUI()
    game.run()

Playing Against AI
----------------

To play against the AI::

    from gomoku_world.gui import GomokuGUI
    
    game = GomokuGUI(game_mode="pvc")  # Player vs Computer
    game.run()

Online Game
----------

To play online::

    import asyncio
    from gomoku_world.network import NetworkManager
    from gomoku_world.gui import GomokuGUI
    
    async def main():
        network = NetworkManager()
        await network.connect()
        
        game = GomokuGUI(game_mode="online")
        game.run()
        
        await network.disconnect()
    
    asyncio.run(main())

Configuration
------------

You can configure various aspects of the game through the configuration manager::

    from gomoku_world.config.instances import config_manager
    
    # Set AI difficulty
    config_manager.set_value('AI_DIFFICULTY', 'hard')
    
    # Enable debug mode
    config_manager.set_value('DEBUG_MODE', True)

For more configuration options, see the API documentation. 