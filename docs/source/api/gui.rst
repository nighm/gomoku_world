.. _api_gui:

GUI模块
======

本节介绍五子棋世界的图形界面模块API。

GomokuGUI 类
----------

.. py:class:: gomoku_world.gui.GomokuGUI

    主游戏窗口类。

    .. py:method:: __init__(game_mode: str = "pvp")
    
        初始化游戏窗口。
        
        :param game_mode: 游戏模式("pvp", "pvc", "online")
        :type game_mode: str

    .. py:method:: run()
    
        运行游戏。

    .. py:method:: new_game()
    
        开始新游戏。

    .. py:method:: undo_move()
    
        悔棋。

BoardCanvas 类
------------

.. py:class:: gomoku_world.gui.BoardCanvas

    棋盘画布类。

    .. py:method:: __init__(parent, game: Game)
    
        初始化棋盘画布。
        
        :param parent: 父窗口
        :param game: 游戏对象

    .. py:method:: redraw()
    
        重绘棋盘。

ControlPanel 类
-------------

.. py:class:: gomoku_world.gui.ControlPanel

    控制面板类。

    .. py:method:: __init__(parent, main_window: GomokuGUI)
    
        初始化控制面板。
        
        :param parent: 父窗口
        :param main_window: 主窗口对象

    .. py:method:: update_difficulty_state()
    
        更新难度设置状态。

StatusBar 类
----------

.. py:class:: gomoku_world.gui.StatusBar

    状态栏类。

    .. py:method:: __init__(parent)
    
        初始化状态栏。
        
        :param parent: 父窗口

    .. py:method:: set_message(message: str)
    
        设置状态消息。
        
        :param message: 消息内容
        :type message: str

MenuBar 类
--------

.. py:class:: gomoku_world.gui.MenuBar

    菜单栏类。

    .. py:method:: __init__(parent, main_window: GomokuGUI)
    
        初始化菜单栏。
        
        :param parent: 父窗口
        :param main_window: 主窗口对象

SpectatorWindow 类
---------------

.. py:class:: gomoku_world.gui.SpectatorWindow

    观战窗口类。

    .. py:method:: __init__(parent: tk.Tk, game_id: str, on_close: Optional[Callable] = None)
    
        初始化观战窗口。
        
        :param parent: 父窗口
        :param game_id: 游戏ID
        :param on_close: 关闭回调函数

    .. py:method:: update_game_state(game_state: Dict)
    
        更新游戏状态。
        
        :param game_state: 游戏状态数据
        :type game_state: Dict

    .. py:method:: add_chat_message(sender: str, message: str)
    
        添加聊天消息。
        
        :param sender: 发送者
        :param message: 消息内容

GameListWindow 类
--------------

.. py:class:: gomoku_world.gui.GameListWindow

    游戏列表窗口类。

    .. py:method:: __init__(parent: tk.Tk, on_spectate: Optional[Callable[[str], None]] = None)
    
        初始化游戏列表窗口。
        
        :param parent: 父窗口
        :param on_spectate: 观战回调函数

    .. py:method:: update_game_list(games: List[Dict])
    
        更新游戏列表。
        
        :param games: 游戏列表数据
        :type games: List[Dict] 