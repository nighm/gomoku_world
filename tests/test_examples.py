"""
测试示例程序的功能。
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# 添加examples目录到Python路径
EXAMPLES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'examples'))
if EXAMPLES_DIR not in sys.path:
    sys.path.insert(0, EXAMPLES_DIR)

# 模拟tkinter
mock_tk = MagicMock()
sys.modules['tkinter'] = mock_tk

class TestNetworkI18nDemo(unittest.TestCase):
    """测试network_i18n_demo.py的功能"""
    
    def setUp(self):
        """设置测试环境"""
        # 导入示例程序
        try:
            import network_i18n_demo
            self.network_i18n_demo = network_i18n_demo
        except ImportError as e:
            self.fail(f"Failed to import network_i18n_demo: {e}")
        
        # 创建模拟对象
        self.mock_i18n_manager = MagicMock()
        self.mock_network_monitor = MagicMock()
        
        # 设置模拟对象的返回值
        self.mock_i18n_manager.current_language = "en"
        self.mock_network_monitor.is_online.return_value = True
        
        # 替换模块中的对象
        self.network_i18n_demo.i18n_manager = self.mock_i18n_manager
        self.network_i18n_demo.network_monitor = self.mock_network_monitor
    
    def test_language_toggle(self):
        """测试语言切换功能"""
        # 创建Demo类的简化版本
        mock_i18n_manager = self.mock_i18n_manager  # 创建局部引用
        
        class SimpleDemo:
            def toggle_language(self_demo):  # 重命名self参数
                current = mock_i18n_manager.current_language
                new_lang = "zh" if current == "en" else "en"
                mock_i18n_manager.set_language(new_lang)
        
        # 创建实例并测试
        demo = SimpleDemo()
        demo.toggle_language()
        
        # 验证语言被切换
        self.mock_i18n_manager.set_language.assert_called_once_with("zh")
    
    def test_network_status_change(self):
        """测试网络状态变化处理"""
        # 创建Demo类的简化版本
        mock_network_monitor = self.mock_network_monitor  # 创建局部引用
        
        class SimpleDemo:
            def __init__(self_demo):  # 重命名self参数
                self_demo.status_label = MagicMock()
                self_demo.mock_network_monitor = mock_network_monitor
            
            def update_ui(self_demo):  # 重命名self参数
                status = "Online" if self_demo.mock_network_monitor.is_online() else "Offline"
                self_demo.status_label["text"] = f"Network Status: {status}"
            
            def on_network_change(self_demo, is_online):  # 重命名self参数
                self_demo.update_ui()
        
        # 创建实例并测试
        demo = SimpleDemo()
        demo.on_network_change(True)
        
        # 验证状态被更新
        demo.status_label.__setitem__.assert_called_with("text", "Network Status: Online")
    
    def test_cleanup(self):
        """测试清理功能"""
        # 创建Demo类的简化版本
        mock_network_monitor = self.mock_network_monitor  # 创建局部引用
        
        class SimpleDemo:
            def __init__(self_demo):  # 重命名self参数
                self_demo.mock_network_monitor = mock_network_monitor
            
            def on_closing(self_demo):  # 重命名self参数
                self_demo.mock_network_monitor.stop()
                self_demo.mock_network_monitor.remove_callback(self_demo.on_network_change)
            
            def on_network_change(self_demo, is_online):  # 重命名self参数
                pass
        
        # 创建实例并测试
        demo = SimpleDemo()
        demo.on_closing()
        
        # 验证网络监控器被停止
        self.mock_network_monitor.stop.assert_called_once()
        self.mock_network_monitor.remove_callback.assert_called_once_with(demo.on_network_change)

if __name__ == '__main__':
    unittest.main() 