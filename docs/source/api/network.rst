.. _api_network:

网络模块
=======

本节介绍五子棋世界的网络模块API。

NetworkManager 类
--------------

.. py:class:: gomoku_world.network.NetworkManager

    网络管理器类。

    .. py:method:: __init__(host: str = "localhost", port: int = 5000)
    
        初始化网络管理器。
        
        :param host: 服务器地址
        :param port: 服务器端口

    .. py:method:: async connect() -> bool
    
        连接到服务器。
        
        :return: 是否连接成功
        :rtype: bool

    .. py:method:: async disconnect()
    
        断开连接。

    .. py:method:: async send_message(message: dict) -> dict
    
        发送消息到服务器。
        
        :param message: 消息数据
        :return: 服务器响应
        :rtype: dict

GameServer 类
-----------

.. py:class:: gomoku_world.network.GameServer

    游戏服务器类。

    .. py:method:: __init__(host: str = "localhost", port: int = 5000)
    
        初始化游戏服务器。
        
        :param host: 监听地址
        :param port: 监听端口

    .. py:method:: async start()
    
        启动服务器。

    .. py:method:: async _handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter)
    
        处理客户端连接。
        
        :param reader: 读取流
        :param writer: 写入流

GameClient 类
-----------

.. py:class:: gomoku_world.network.GameClient

    游戏客户端类。

    .. py:method:: __init__(host: str = "localhost", port: int = 5000)
    
        初始化游戏客户端。
        
        :param host: 服务器地址
        :param port: 服务器端口

    .. py:method:: async connect() -> bool
    
        连接到服务器。
        
        :return: 是否连接成功
        :rtype: bool

    .. py:method:: async list_games() -> List[Dict]
    
        获取可用游戏列表。
        
        :return: 游戏列表
        :rtype: List[Dict]

    .. py:method:: async spectate_game(game_id: str) -> bool
    
        开始观战游戏。
        
        :param game_id: 游戏ID
        :return: 是否成功
        :rtype: bool

SpectatorManager 类
----------------

.. py:class:: gomoku_world.network.SpectatorManager

    观战管理器类。

    .. py:method:: __init__()
    
        初始化观战管理器。

    .. py:method:: add_spectator(spectator_id: str, name: str, game_id: str) -> bool
    
        添加观战者。
        
        :param spectator_id: 观战者ID
        :param name: 观战者名称
        :param game_id: 游戏ID
        :return: 是否成功
        :rtype: bool

    .. py:method:: remove_spectator(spectator_id: str) -> bool
    
        移除观战者。
        
        :param spectator_id: 观战者ID
        :return: 是否成功
        :rtype: bool

    .. py:method:: get_game_spectators(game_id: str) -> Set[str]
    
        获取游戏的所有观战者。
        
        :param game_id: 游戏ID
        :return: 观战者ID集合
        :rtype: Set[str]

NetworkError 类
------------

.. py:class:: gomoku_world.network.NetworkError

    网络错误基类。

ConnectionError 类
---------------

.. py:class:: gomoku_world.network.ConnectionError

    连接错误类。

MessageError 类
------------

.. py:class:: gomoku_world.network.MessageError

    消息错误类。 