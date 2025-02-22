"""
这是一个演示网络感知国际化系统的示例程序。
它展示了如何：
1. 初始化和使用i18n管理器
2. 监控网络状态变化
3. 动态切换语言
4. 处理错误和异常情况

使用方法：
1. 运行程序后会显示一个窗口，包含网络状态、语言切换按钮和示例文本
2. 点击语言切换按钮可以在中文和英文之间切换
3. 程序会自动监控网络状态，并在状态变化时更新显示
4. 所有错误都会以对话框的形式显示给用户

依赖：
- tkinter：用于GUI
- gomoku_world.i18n：国际化支持
- gomoku_world.utils.network：网络监控
"""

import tkinter as tk
from tkinter import messagebox
import logging
from gomoku_world.i18n import i18n_manager  # 使用正确的i18n_manager实例
from gomoku_world.utils.network import network_monitor
from gomoku_world.utils.logger import get_logger

# 设置日志级别为INFO，以显示更多信息
logger = get_logger(__name__)
logging.getLogger('gomoku_world').setLevel(logging.INFO)

def test_translations():
    """测试翻译是否正确加载"""
    test_keys = {
        "common": ["app.name", "button.ok", "dialog.error"],
        "game": ["new", "mode.single", "difficulty.medium"],
        "network": ["status.online", "status.offline"],
        "error": ["error.network.connection_failed", "error.system.initialization"],
        "ui": ["title", "header", "button.settings"]
    }
    
    for lang in ["en", "zh"]:
        logger.info(f"\nTesting translations for language: {lang}")
        i18n_manager.set_language(lang)
        
        for category, keys in test_keys.items():
            logger.info(f"\nCategory: {category}")
            for key in keys:
                try:
                    text = i18n_manager.get_text(key, category=category)
                    logger.info(f"  {key}: {text}")
                except Exception as e:
                    logger.error(f"  Failed to get translation for {key}: {e}")

def initialize_systems():
    """初始化必要的系统"""
    try:
        logger.info("Starting system initialization...")
        
        # 初始化i18n系统
        logger.info("Initializing i18n system...")
        if not i18n_manager._initialized:
            i18n_manager.initialize()
            if not i18n_manager._initialized:
                logger.error("Failed to initialize i18n system")
                raise RuntimeError("Failed to initialize i18n system")
        logger.info("I18n system initialized successfully")
        
        # 加载翻译文件
        logger.info("Loading translations...")
        i18n_manager.load_translations()
        if not i18n_manager._translations:
            logger.error("Failed to load translations")
            raise RuntimeError("Failed to load translations")
            
        # 打印已加载的翻译信息
        logger.info("Translation status:")
        logger.info(f"Current language: {i18n_manager.current_language}")
        logger.info(f"Available languages: {', '.join(i18n_manager.available_languages.keys())}")
        
        # 测试翻译
        test_translations()
        
        logger.info("Translations loaded successfully")
            
        # 确保网络监控器没有在运行
        if hasattr(network_monitor, '_monitor_thread') and network_monitor._monitor_thread and network_monitor._monitor_thread.is_alive():
            try:
                logger.info("Stopping existing network monitor...")
                network_monitor.stop()
                logger.info("Stopped existing network monitor")
            except Exception as e:
                logger.warning(f"Failed to stop network monitor: {e}")
            
        # 启动网络监控
        try:
            logger.info("Starting network monitor...")
            network_monitor.start()
            logger.info("Network monitor started successfully")
        except Exception as e:
            logger.error(f"Failed to start network monitor: {e}")
            raise RuntimeError(i18n_manager.get_text("network.connection_failed", category="error")) from e
        
        logger.info("System initialization completed successfully")
        return True
    except Exception as e:
        logger.error(f"System initialization failed: {e}")
        return False

class Demo(tk.Tk):
    """
    演示程序的主窗口类。
    继承自tk.Tk，实现了网络状态监控和语言切换功能。
    """
    
    def __init__(self):
        try:
            super().__init__()
            
            # 初始化系统
            if not initialize_systems():
                raise RuntimeError(i18n_manager.get_text("system.initialization", category="error"))
            
            self.title("Network I18n Demo")
            
            # 创建UI元素
            self._create_widgets()
            
            # 设置窗口
            self.geometry("400x300")
            self.center_window()
            
            # 注册网络状态回调
            network_monitor.add_callback(self.on_network_change)
            
            # 初始更新UI
            self.update_ui()
            
            # 绑定关闭事件
            self.protocol("WM_DELETE_WINDOW", self.on_closing)
            
        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            messagebox.showerror("Error", f"Initialization failed: {str(e)}")
            self.destroy()
    
    def _create_widgets(self):
        """创建UI元素"""
        # 状态框架
        self.status_frame = tk.Frame(self)
        self.status_frame.pack(pady=20, fill=tk.X)
        
        # 网络状态标签
        self.status_label = tk.Label(
            self.status_frame,
            text="Checking network status...",
            font=('Arial', 12),
            wraplength=350
        )
        self.status_label.pack()
        
        # 语言切换框架
        self.lang_frame = tk.Frame(self)
        self.lang_frame.pack(pady=20)
        
        # 当前语言标签
        self.lang_label = tk.Label(
            self.lang_frame,
            text="Current Language",
            font=('Arial', 12)
        )
        self.lang_label.pack()
        
        # 语言切换按钮
        self.lang_button = tk.Button(
            self.lang_frame,
            text="Switch Language",
            command=self.toggle_language,
            font=('Arial', 12)
        )
        self.lang_button.pack(pady=10)
        
        # 示例文本框架
        self.text_frame = tk.Frame(self)
        self.text_frame.pack(pady=20)
        
        # 示例文本标签
        self.text_label = tk.Label(
            self.text_frame,
            text="Loading...",
            font=('Arial', 12),
            wraplength=350
        )
        self.text_label.pack()
    
    def center_window(self):
        """将窗口居中显示"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def toggle_language(self):
        """切换语言"""
        try:
            current = i18n_manager.current_language
            new_lang = "zh" if current == "en" else "en"
            i18n_manager.set_language(new_lang, force_reload=True)
            self.update_ui()
        except Exception as e:
            logger.error(f"Language toggle failed: {e}")
            messagebox.showerror("Error", f"Failed to switch language: {str(e)}")
    
    def on_network_change(self, is_online):
        """处理网络状态变化"""
        try:
            self.update_ui()
        except Exception as e:
            logger.error(f"Failed to handle network change: {e}")
    
    def update_ui(self):
        """更新UI显示"""
        try:
            # 更新网络状态
            is_online = network_monitor.is_online()
            status_key = "network.status.online" if is_online else "network.status.offline"
            self.status_label["text"] = i18n_manager.get_text(status_key)
            
            # 更新语言信息
            current = i18n_manager.current_language
            self.lang_label["text"] = f"Current Language: {current.upper()}"
            
            # 更新切换按钮
            target = "zh" if current == "en" else "en"
            self.lang_button["text"] = f"Switch to {target.upper()}"
            
            # 更新示例文本
            self.text_label["text"] = i18n_manager.get_text("app.name")
            
        except Exception as e:
            logger.error(f"UI update failed: {e}")
            messagebox.showerror("Error", f"Failed to update UI: {str(e)}")
    
    def on_closing(self):
        """处理窗口关闭事件"""
        try:
            network_monitor.remove_callback(self.on_network_change)
            network_monitor.stop()
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
        finally:
            self.destroy()

if __name__ == "__main__":
    demo = Demo()
    demo.mainloop() 