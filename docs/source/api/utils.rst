.. _api_utils:

工具模块
=======

本节介绍五子棋世界的工具模块API。

日志模块
-------

.. py:function:: gomoku_world.utils.setup_logging(level: int = logging.INFO)

    设置日志系统。
    
    :param level: 日志级别
    :type level: int

.. py:function:: gomoku_world.utils.get_logger(name: str) -> logging.Logger

    获取日志记录器。
    
    :param name: 记录器名称
    :return: 日志记录器实例
    :rtype: logging.Logger

资源管理
-------

.. py:class:: gomoku_world.utils.ResourceManager

    资源管理器类。

    .. py:method:: load_theme(theme_name: str)
    
        加载主题。
        
        :param theme_name: 主题名称

    .. py:method:: get_text(key: str, lang: Optional[str] = None) -> str
    
        获取本地化文本。
        
        :param key: 文本键
        :param lang: 语言代码
        :return: 本地化文本
        :rtype: str

声音管理
-------

.. py:class:: gomoku_world.utils.SoundManager

    声音管理器类。

    .. py:method:: play(sound_name: str)
    
        播放音效。
        
        :param sound_name: 音效名称

    .. py:method:: set_volume(volume: float)
    
        设置音量。
        
        :param volume: 音量(0.0-1.0)

调试工具
-------

.. py:class:: gomoku_world.utils.DebugManager

    调试管理器类。

    .. py:method:: toggle_debug_mode()
    
        切换调试模式。

    .. py:method:: toggle_fps_display()
    
        切换FPS显示。

性能监控
-------

.. py:class:: gomoku_world.utils.monitoring.MetricsCollector

    性能指标收集器类。

    .. py:method:: measure_time(name: str)
    
        测量代码块执行时间。
        
        :param name: 指标名称

    .. py:method:: get_report() -> Dict
    
        获取性能报告。
        
        :return: 性能指标数据
        :rtype: Dict

.. py:class:: gomoku_world.utils.monitoring.Profiler

    性能分析器类。

    .. py:method:: start()
    
        开始性能分析。

    .. py:method:: stop()
    
        停止性能分析。

国际化
-----

.. py:class:: gomoku_world.utils.i18n.Translator

    翻译器类。

    .. py:method:: translate(key: str, lang: str) -> str
    
        翻译文本。
        
        :param key: 文本键
        :param lang: 目标语言
        :return: 翻译后的文本
        :rtype: str

.. py:class:: gomoku_world.utils.i18n.LocaleManager

    本地化管理器类。

    .. py:method:: set_locale(locale: str)
    
        设置当前语言环境。
        
        :param locale: 语言代码

    .. py:method:: get_available_locales() -> List[str]
    
        获取可用的语言列表。
        
        :return: 语言代码列表
        :rtype: List[str]

导入管理
-------

.. py:class:: gomoku_world.utils.ImportManager

    导入管理器类。

    .. py:method:: import_module(module_path: str) -> Optional[Any]
    
        动态导入模块。
        
        :param module_path: 模块路径
        :return: 导入的模块
        :rtype: Optional[Any]

    .. py:method:: get_class(module_path: str, class_name: str) -> Optional[type]
    
        从模块中获取类。
        
        :param module_path: 模块路径
        :param class_name: 类名
        :return: 类型对象
        :rtype: Optional[type] 