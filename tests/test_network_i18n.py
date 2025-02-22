"""
Test internationalization system's network awareness functionality.

测试国际化系统的网络感知功能。

This module tests the integration between the i18n system and network monitoring,
ensuring proper behavior in both online and offline scenarios.

本模块测试国际化系统和网络监控之间的集成，确保在在线和离线场景下的正确行为。
"""

import pytest
from gomoku_world.i18n import i18n_manager
from gomoku_world.utils.network import network_monitor

def test_i18n_network_integration():
    """
    Test the integration between i18n system and network monitoring.
    
    测试国际化系统和网络监控之间的集成。
    
    This test verifies:
    - Translation loading in online mode
    - Fallback behavior in offline mode
    - Network status change handling
    
    本测试验证：
    - 在线模式下的翻译加载
    - 离线模式下的回退行为
    - 网络状态变化处理
    """
    # Initialize components / 初始化组件
    network_monitor.start()
    i18n_manager.initialize()
    
    try:
        # Test online translation loading / 测试在线翻译加载
        i18n_manager.set_language("zh", force_reload=True)
        assert i18n_manager.get_text("new.game") == "新游戏", "Online Chinese translation failed / 在线中文翻译失败"
        
        # Simulate network disconnection / 模拟网络断开
        network_monitor._is_online = False
        network_monitor._notify_callbacks()
        
        # Test offline fallback / 测试离线回退
        i18n_manager.set_language("en", force_reload=True)
        assert i18n_manager.get_text("new.game") == "New Game", "Offline English fallback failed / 离线英文回退失败"
        
        # Test network recovery / 测试网络恢复
        network_monitor._is_online = True
        network_monitor._notify_callbacks()
        i18n_manager.set_language("zh", force_reload=True)
        assert i18n_manager.get_text("new.game") == "新游戏", "Network recovery translation failed / 网络恢复后翻译失败"
        
    finally:
        # Cleanup / 清理
        network_monitor.stop() 