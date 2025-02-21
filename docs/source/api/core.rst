.. _api_core:

核心模块
=======

本节介绍五子棋世界的核心模块API。

Board 类
-------

.. py:class:: gomoku_world.core.Board

    棋盘类，管理游戏棋盘状态。

    .. py:method:: __init__(size: int = 15)
    
        初始化棋盘。
        
        :param size: 棋盘大小，默认为15x15
        :type size: int

    .. py:method:: place_piece(row: int, col: int, player: int) -> bool
    
        在指定位置放置棋子。
        
        :param row: 行号
        :param col: 列号
        :param player: 玩家编号(1或2)
        :return: 是否放置成功
        :rtype: bool

    .. py:method:: get_piece(row: int, col: int) -> int
    
        获取指定位置的棋子。
        
        :param row: 行号
        :param col: 列号
        :return: 棋子类型(0:空, 1:黑, 2:白)
        :rtype: int

    .. py:method:: clear()
    
        清空棋盘。

Rules 类
-------

.. py:class:: gomoku_world.core.Rules

    规则类，处理游戏规则和胜负判定。

    .. py:method:: check_win(board: Board, last_row: int, last_col: int) -> bool
    
        检查最后一步是否导致胜利。
        
        :param board: 棋盘对象
        :param last_row: 最后落子的行号
        :param last_col: 最后落子的列号
        :return: 是否获胜
        :rtype: bool

    .. py:method:: is_draw(board: Board) -> bool
    
        检查是否和局。
        
        :param board: 棋盘对象
        :return: 是否和局
        :rtype: bool

    .. py:method:: get_valid_moves(board: Board) -> List[Tuple[int, int]]
    
        获取所有有效的移动位置。
        
        :param board: 棋盘对象
        :return: 有效位置列表
        :rtype: List[Tuple[int, int]]

AI 类
----

.. py:class:: gomoku_world.core.AI

    AI类，实现人工智能对手。

    .. py:method:: __init__(difficulty: str = "medium")
    
        初始化AI。
        
        :param difficulty: 难度级别("easy", "medium", "hard")
        :type difficulty: str

    .. py:method:: get_move(board: Board, player: int) -> Tuple[int, int]
    
        获取AI的下一步移动。
        
        :param board: 棋盘对象
        :param player: 玩家编号
        :return: 移动位置(行,列)
        :rtype: Tuple[int, int]

    .. py:method:: set_difficulty(difficulty: str)
    
        设置AI难度。
        
        :param difficulty: 难度级别
        :type difficulty: str

SaveManager 类
------------

.. py:class:: gomoku_world.core.SaveManager

    存档管理类，处理游戏存档。

    .. py:method:: save_game(game_data: GameSave) -> bool
    
        保存游戏。
        
        :param game_data: 游戏存档数据
        :return: 是否保存成功
        :rtype: bool

    .. py:method:: load_game(save_id: str) -> Optional[GameSave]
    
        加载游戏。
        
        :param save_id: 存档ID
        :return: 游戏存档数据
        :rtype: Optional[GameSave]

    .. py:method:: list_saves() -> List[Dict]
    
        列出所有存档。
        
        :return: 存档列表
        :rtype: List[Dict]

GameSave 类
---------

.. py:class:: gomoku_world.core.GameSave

    游戏存档数据类。

    .. py:attribute:: id
        :type: str
        
        存档ID

    .. py:attribute:: timestamp
        :type: float
        
        保存时间戳

    .. py:attribute:: black_player
        :type: str
        
        黑方玩家名称

    .. py:attribute:: white_player
        :type: str
        
        白方玩家名称

    .. py:attribute:: moves
        :type: List[Dict]
        
        移动历史记录

    .. py:attribute:: board_size
        :type: int
        
        棋盘大小

    .. py:attribute:: game_mode
        :type: str
        
        游戏模式

    .. py:attribute:: winner
        :type: Optional[int]
        
        获胜者(如果有) 