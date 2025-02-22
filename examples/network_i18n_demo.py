import tkinter as tk
from gomoku_world.i18n import i18n_manager
from gomoku_world.utils.network import network_monitor

class Demo(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Network I18n Demo")
        
        # 状态标签
        self.status_label = tk.Label(self)
        self.status_label.pack()
        
        # 语言按钮
        self.lang_button = tk.Button(self, command=self.toggle_language)
        self.lang_button.pack()
        
        # 示例文本
        self.text_label = tk.Label(self)
        self.text_label.pack()
        
        # 注册网络状态回调
        network_monitor.add_callback(self.on_network_change)
        network_monitor.start()
        
        self.update_ui()
        
    def toggle_language(self):
        current = i18n_manager.current_language
        new_lang = "zh" if current == "en" else "en"
        i18n_manager.set_language(new_lang)
        self.update_ui()
        
    def on_network_change(self, is_online):
        self.update_ui()
        
    def update_ui(self):
        # 更新状态
        status = "Online" if network_monitor.is_online() else "Offline"
        self.status_label["text"] = f"Network Status: {status}"
        
        # 更新按钮
        current = i18n_manager.current_language
        self.lang_button["text"] = f"Switch to {'Chinese' if current == 'en' else 'English'}"
        
        # 更新示例文本
        self.text_label["text"] = i18n_manager.get_text("game.new")

if __name__ == "__main__":
    demo = Demo()
    demo.mainloop() 