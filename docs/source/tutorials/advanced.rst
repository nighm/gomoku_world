.. _advanced_tutorial:

高级功能教程
==========

本教程将介绍五子棋世界（Gomoku World）的高级功能和使用技巧。

自定义配置
--------

1. 配置管理器
~~~~~~~~~~

使用配置管理器修改游戏设置::

    from gomoku_world.config import config_manager
    
    # 修改棋盘大小
    config_manager.set_value('BOARD_SIZE', 19)
    
    # 修改主题
    config_manager.set_value('DEFAULT_THEME', 'dark')
    
    # 修改语言
    config_manager.set_value('DEFAULT_LANGUAGE', 'zh')

2. 资源管理
~~~~~~~~~

自定义主题和音效::

    from gomoku_world.utils.resources import resource_manager
    from gomoku_world.utils.sound import sound_manager
    
    # 加载自定义主题
    resource_manager.load_theme('custom_theme.json')
    
    # 添加自定义音效
    sound_manager.add_sound('custom_move', 'path/to/sound.wav')

游戏扩展
-------

1. 自定义AI策略
~~~~~~~~~~~~

创建自己的AI策略::

    from gomoku_world.core.ai import Strategy
    
    class MyStrategy(Strategy):
        def get_move(self, board, player):
            # 实现你的策略
            return row, col
    
    # 使用自定义策略
    ai.set_strategy(MyStrategy())

2. 事件处理
~~~~~~~~~

注册游戏事件处理器::

    def on_piece_placed(row, col, player):
        print(f"Piece placed at ({row}, {col}) by player {player}")
    
    game.on('piece_placed', on_piece_placed)

调试功能
-------

1. 调试模式
~~~~~~~~~

启用调试模式::

    from gomoku_world.utils.debug import debug_manager
    
    # 启用调试模式
    debug_manager.toggle_debug_mode()
    
    # 显示FPS
    debug_manager.toggle_fps_display()
    
    # 显示网格坐标
    debug_manager.toggle_grid_coords()

2. 日志系统
~~~~~~~~~

配置日志记录::

    from gomoku_world.utils.logger import setup_logging
    import logging
    
    # 设置日志级别
    setup_logging(level=logging.DEBUG)
    
    # 获取日志记录器
    logger = logging.getLogger(__name__)
    logger.debug("Debug message")

性能优化
-------

1. 性能监控
~~~~~~~~~

使用性能监控工具::

    from gomoku_world.utils.monitoring import metrics_collector
    
    # 记录性能指标
    with metrics_collector.measure_time('move_calculation'):
        ai.get_move(board, player)
    
    # 获取性能报告
    metrics_collector.get_report()

2. 缓存管理
~~~~~~~~~

管理AI计算缓存::

    from gomoku_world.core.ai import ai_engine
    
    # 清除缓存
    ai_engine.clear_cache()
    
    # 设置缓存大小
    ai_engine.set_cache_size(1000)

网络功能
-------

1. 自定义协议
~~~~~~~~~~

扩展网络协议::

    from gomoku_world.network import NetworkManager
    
    class CustomNetworkManager(NetworkManager):
        async def handle_custom_message(self, data):
            # 处理自定义消息
            pass
    
    # 使用自定义网络管理器
    network = CustomNetworkManager()

2. 网络参数
~~~~~~~~~

优化网络设置::

    # 设置连接超时
    network.set_timeout(30)
    
    # 设置重连间隔
    network.set_reconnect_interval(5)
    
    # 设置心跳间隔
    network.set_heartbeat_interval(10)

高级示例
-------

1. 回放系统
~~~~~~~~~

记录和回放游戏::

    from gomoku_world.core import SaveManager
    
    # 保存游戏
    save_manager = SaveManager()
    save_id = save_manager.save_game(game_data)
    
    # 加载回放
    replay = save_manager.load_game(save_id)
    replay.play()

2. 观战系统
~~~~~~~~~

实现高级观战功能::

    # 获取对局信息
    game_info = await network.get_game_info(game_id)
    
    # 订阅实时更新
    await network.subscribe_to_game(game_id)
    
    # 发送观战评论
    await network.send_spectator_message(game_id, "Good move!")

3. 排行系统
~~~~~~~~~

使用排行榜功能::

    from gomoku_world.utils import LeaderboardManager
    
    # 获取排行榜
    leaderboard = LeaderboardManager()
    top_players = leaderboard.get_top_players(limit=10)
    
    # 更新玩家统计
    leaderboard.update_player_stats(player_id, game_result)

下一步
------

* 查看 :ref:`api_reference` 了解完整的API文档
* 访问 :ref:`examples` 获取更多示例代码
* 加入我们的 :ref:`community` 分享你的想法 
 