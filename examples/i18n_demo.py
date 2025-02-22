"""
国际化系统示例程序。

此示例展示了：
1. 基本的翻译使用
2. 语言切换
3. 格式化和错误处理
4. 缓存控制
5. 自定义加载器和格式化器
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from pathlib import Path

from gomoku_world.i18n import (
    i18n_manager,
    JsonLoader,
    YamlLoader,
    SafeFormatter,
    MemoryCache,
    TranslationNotFoundError
)
from gomoku_world.utils.logger import setup_logging

# 设置日志
setup_logging()
logger = logging.getLogger(__name__)

class I18nDemo(tk.Tk):
    """
    国际化演示程序。
    """
    
    def __init__(self):
        """
        初始化演示程序。
        """
        super().__init__()
        
        # 配置窗口
        self.title("I18n Demo")
        self.geometry("800x600")
        
        # 初始化i18n
        self._init_i18n()
        
        # 创建界面
        self._create_widgets()
        
        # 更新显示
        self._update_ui()
        
    def _init_i18n(self):
        """
        初始化国际化系统。
        """
        # 设置自定义加载器
        loader = JsonLoader("resources/i18n")
        
        # 设置自定义格式化器
        formatter = SafeFormatter(fallback_template="[Missing: {key}]")
        
        # 设置自定义缓存
        cache = MemoryCache(max_size=1000, ttl=3600)
        
        # 初始化管理器
        i18n_manager.initialize(
            loader=loader,
            formatter=formatter,
            cache=cache
        )
        
    def _create_widgets(self):
        """
        创建界面组件。
        """
        # 创建主框架
        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # 语言选择
        lang_frame = ttk.LabelFrame(main_frame, text="Language / 语言")
        lang_frame.pack(fill='x', pady=5)
        
        self.lang_var = tk.StringVar(value="en")
        for lang in ["en", "zh-CN"]:
            ttk.Radiobutton(
                lang_frame,
                text=lang,
                value=lang,
                variable=self.lang_var,
                command=self._on_language_change
            ).pack(side='left', padx=5)
            
        # 基本翻译示例
        basic_frame = ttk.LabelFrame(main_frame, text="Basic Translation / 基本翻译")
        basic_frame.pack(fill='x', pady=5)
        
        self.basic_label = ttk.Label(basic_frame)
        self.basic_label.pack(pady=5)
        
        # 带参数的翻译示例
        format_frame = ttk.LabelFrame(main_frame, text="Formatted Translation / 格式化翻译")
        format_frame.pack(fill='x', pady=5)
        
        self.format_label = ttk.Label(format_frame)
        self.format_label.pack(pady=5)
        
        # 双语显示示例
        bilingual_frame = ttk.LabelFrame(main_frame, text="Bilingual Text / 双语文本")
        bilingual_frame.pack(fill='x', pady=5)
        
        self.bilingual_label = ttk.Label(bilingual_frame)
        self.bilingual_label.pack(pady=5)
        
        # 错误处理示例
        error_frame = ttk.LabelFrame(main_frame, text="Error Handling / 错误处理")
        error_frame.pack(fill='x', pady=5)
        
        ttk.Button(
            error_frame,
            text="Test Error / 测试错误",
            command=self._test_error
        ).pack(pady=5)
        
        # 缓存控制
        cache_frame = ttk.LabelFrame(main_frame, text="Cache Control / 缓存控制")
        cache_frame.pack(fill='x', pady=5)
        
        ttk.Button(
            cache_frame,
            text="Clear Cache / 清除缓存",
            command=self._clear_cache
        ).pack(pady=5)
        
    def _update_ui(self):
        """
        更新界面显示。
        """
        try:
            # 更新基本翻译
            self.basic_label['text'] = i18n_manager.get_text("game.new")
            
            # 更新格式化翻译
            self.format_label['text'] = i18n_manager.get_text(
                "game.player.turn",
                player=i18n_manager.get_text("player.black")
            )
            
            # 更新双语文本
            self.bilingual_label['text'] = i18n_manager.get_bilingual("game.new")
            
        except Exception as e:
            logger.error(f"Error updating UI: {e}")
            messagebox.showerror("Error", str(e))
            
    def _on_language_change(self):
        """
        处理语言切换。
        """
        try:
            i18n_manager.set_language(self.lang_var.get())
            self._update_ui()
        except Exception as e:
            logger.error(f"Error changing language: {e}")
            messagebox.showerror("Error", str(e))
            
    def _test_error(self):
        """
        测试错误处理。
        """
        try:
            text = i18n_manager.get_text("invalid.key")
            messagebox.showinfo("Success", text)
        except TranslationNotFoundError as e:
            logger.warning(f"Translation not found: {e}")
            messagebox.showwarning("Warning", str(e))
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            messagebox.showerror("Error", str(e))
            
    def _clear_cache(self):
        """
        清除翻译缓存。
        """
        try:
            i18n_manager.clear_cache()
            messagebox.showinfo(
                "Success",
                i18n_manager.get_text("cache.cleared")
            )
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            messagebox.showerror("Error", str(e))

def main():
    """
    主函数。
    """
    try:
        app = I18nDemo()
        app.mainloop()
    except Exception as e:
        logger.error(f"Application error: {e}")
        messagebox.showerror("Error", str(e))

if __name__ == '__main__':
    main() 