"""
Test internationalization system's network awareness functionality.

测试国际化系统的网络感知功能。
"""

import pytest
from gomoku_world.i18n import i18n_manager
from gomoku_world.utils.network import network_monitor

def test_i18n_network_integration():
    """
    Test the integration between i18n system and network monitoring.
    
    测试国际化系统和网络监控之间的集成。
    """
    # Initialize / 初始化
    network_monitor.start()
    i18n_manager.initialize()
    
    # Test online loading / 测试在线加载
    i18n_manager.set_language("zh", force_reload=True)
    assert i18n_manager.get_text("new", "game") == "新游戏"
    
    # Simulate network disconnection / 模拟网络断开
    network_monitor._is_online = False
    network_monitor._callbacks[0](False)  # Trigger callback / 触发回调
    
    # Test offline loading / 测试离线加载
    i18n_manager.set_language("en", force_reload=True)
    assert i18n_manager.get_text("new", "game") == "New Game"
    
    # Cleanup / 清理
    network_monitor.stop() 