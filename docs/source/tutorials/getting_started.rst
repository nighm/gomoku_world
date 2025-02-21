入门指南
========

本教程将帮助您快速开始使用五子棋世界（Gomoku World）。

安装
----

1. 使用pip安装::

    pip install gomoku-world

2. 或者从源码安装::

    git clone https://github.com/nighm/gomoku_world.git
    cd gomoku_world
    pip install -e .

快速开始
--------

1. 启动游戏
~~~~~~~~~

最简单的方式是直接运行游戏::

    python -m gomoku_world

或者在代码中使用::

    from gomoku_world.gui import GomokuGUI
    
    game = GomokuGUI()
    game.run()

2. 游戏模式
~~~~~~~~~

游戏支持以下模式：

* 玩家对战（PvP）
* 人机对战（PvC）
* 在线对战
* 观战模式

切换游戏模式::

    # 人机对战
    game = GomokuGUI(game_mode="pvc")
    
    # 在线对战
    game = GomokuGUI(game_mode="online")

3. 基本操作
~~~~~~~~~

* 左键点击：放置棋子
* 右键点击：（调试模式）显示位置信息
* ESC：打开菜单
* Ctrl+Z：悔棋
* Ctrl+N：新游戏

4. AI难度设置
~~~~~~~~~~~

在人机对战模式下，可以设置AI难度::

    game.set_ai_difficulty("easy")    # 简单
    game.set_ai_difficulty("medium")  # 中等
    game.set_ai_difficulty("hard")    # 困难

5. 在线功能
~~~~~~~~~

连接服务器::

    from gomoku_world.network import NetworkManager
    
    network = NetworkManager()
    await network.connect()

加入游戏::

    # 创建新游戏
    game_id = await network.create_game()
    
    # 或加入现有游戏
    await network.join_game(game_id)

观战模式::

    # 获取可观战的游戏列表
    games = await network.list_games()
    
    # 开始观战
    await network.spectate_game(game_id)

下一步
------

* 查看 :ref:`advanced_tutorial` 了解更多高级功能
* 阅读 :ref:`api_reference` 获取详细的API文档
* 访问 :ref:`examples` 获取更多示例代码 