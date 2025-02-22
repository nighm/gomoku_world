# Examples / 示例

## Game Examples / 游戏示例

### Basic Game / 基础游戏
```python
from gomoku_world.core import Game, Board
from gomoku_world.gui import GomokuGUI

# Create game instance
game = Game()

# Create GUI
gui = GomokuGUI(game)

# Start game
gui.run()
```

### AI Game / AI对战
```python
from gomoku_world.core import Game
from gomoku_world.core.ai import AI, MinMaxStrategy

# Create game with AI
game = Game()
ai = AI(strategy=MinMaxStrategy())
game.set_ai(ai)

# Make moves
game.make_move(7, 7)  # Player move
ai_row, ai_col = ai.get_move(game.board)  # AI move
```

### Network Game / 网络对战
```python
from gomoku_world.network import NetworkManager
from gomoku_world.core import Game

# Create network manager
network = NetworkManager()

# Connect to server
network.connect()

# Create or join room
room_id = network.create_room()
# Or: network.join_room("room_id")

# Handle moves
@network.on_move
def handle_move(row, col):
    game.make_move(row, col)
```

## Theme Examples / 主题示例

### Custom Theme / 自定义主题
```python
from gomoku_world.theme import theme

# Load custom theme
theme.load_theme("custom_theme.json")

# Get theme colors
board_color = theme.get_color("board.background")
piece_color = theme.get_color("board.black_piece")
```

### Network Status Theme / 网络状态主题
```python
from gomoku_world.utils.network import network_monitor
from gomoku_world.theme import theme

# Update theme based on network status
def update_theme(is_online):
    if is_online:
        theme.set_color("status.background", "#4CAF50")
        theme.set_color("status.text", "#FFFFFF")
    else:
        theme.set_color("status.background", "#F44336")
        theme.set_color("status.text", "#FFFFFF")

# Register callback
network_monitor.add_callback(update_theme)
```

### I18n Theme / 国际化主题
```python
from gomoku_world.i18n import i18n_manager
from gomoku_world.theme import theme

# Update theme based on language
def update_theme_for_language(language):
    if language in ["zh", "ja", "ko"]:
        theme.set_font_family("text", theme.get_cjk_font())
    else:
        theme.set_font_family("text", theme.get_latin_font())

# Register callback
i18n_manager.on_language_change(update_theme_for_language)
```

## I18n Examples / 国际化示例

### Basic I18n / 基础国际化
```python
from gomoku_world.i18n import i18n_manager

# Initialize i18n system
i18n_manager.initialize()

# Get translated text
title = i18n_manager.get_text("game.title")
status = i18n_manager.get_text("game.status.your_turn")

# Switch language
i18n_manager.set_language("zh")
```

### Network I18n Demo / 网络国际化示例
```python
from tkinter import Tk, Label, Button
from gomoku_world.i18n import i18n_manager
from gomoku_world.utils.network import network_monitor

class Demo(Tk):
    def __init__(self):
        super().__init__()
        
        # Initialize systems
        i18n_manager.initialize()
        network_monitor.start()
        
        # Create UI
        self.status_label = Label(self)
        self.status_label.pack()
        
        self.lang_button = Button(
            self,
            command=self.toggle_language
        )
        self.lang_button.pack()
        
        # Register callbacks
        network_monitor.add_callback(self.on_network_change)
        
        # Update UI
        self.update_ui()
    
    def toggle_language(self):
        current = i18n_manager.current_language
        new_lang = "zh" if current == "en" else "en"
        i18n_manager.set_language(new_lang)
        self.update_ui()
    
    def on_network_change(self, is_online):
        self.update_ui()
    
    def update_ui(self):
        status = "Online" if network_monitor.is_online() else "Offline"
        self.status_label["text"] = i18n_manager.get_text(
            f"network.status.{status.lower()}",
            category="network"
        )
        self.lang_button["text"] = i18n_manager.get_text(
            "button.switch_language",
            language=i18n_manager.get_text(
                f"language.{i18n_manager.current_language}"
            )
        )

if __name__ == "__main__":
    demo = Demo()
    demo.mainloop()
```

## Configuration Examples / 配置示例

### Game Config / 游戏配置
```python
from gomoku_world.config import config_manager

# Load configuration
config_manager.load_config()

# Get settings
board_size = config_manager.get("game", "board_size", 15)
win_length = config_manager.get("game", "win_length", 5)

# Save settings
config_manager.set("game", "difficulty", "hard")
config_manager.save_config()
```

### Network Config / 网络配置
```python
from gomoku_world.config import config_manager

# Configure network settings
config_manager.set("network", "check_interval", 60)
config_manager.set("network", "timeout", 5)
config_manager.set("network", "max_retries", 3)

# Configure proxy
config_manager.set("network", "proxy", {
    "enabled": True,
    "host": "proxy.example.com",
    "port": 8080
})
```

### I18n Config / 国际化配置
```python
from gomoku_world.config import config_manager

# Configure i18n settings
config_manager.set("i18n", "default_language", "en")
config_manager.set("i18n", "fallback_language", "en")
config_manager.set("i18n", "available_languages", ["en", "zh", "ja", "ko"])

# Configure translation service
config_manager.set("i18n", "translation_service", {
    "url": "https://api.translations.gomokuworld.org",
    "timeout": 5,
    "cache_ttl": 86400
})
```

## Integration Examples / 集成示例

### API Usage / API使用
```python
from gomoku_world.core import Game
from gomoku_world.i18n import i18n_manager
from gomoku_world.utils.network import network_monitor

# Initialize components
i18n_manager.initialize()
network_monitor.start()

# Create game with network status
game = Game()

def update_status():
    if network_monitor.is_online():
        status = i18n_manager.get_text("network.status.online")
    else:
        status = i18n_manager.get_text("network.status.offline")
    game.set_status(status)

network_monitor.add_callback(update_status)
```

### Event Handling / 事件处理
```python
from gomoku_world.core import Game
from gomoku_world.i18n import i18n_manager
from gomoku_world.utils.network import network_monitor

# Create event handlers
def on_language_change(language):
    print(f"Language changed to: {language}")

def on_network_change(is_online):
    status = "online" if is_online else "offline"
    print(i18n_manager.get_text(f"network.status.{status}"))

# Register handlers
i18n_manager.on_language_change(on_language_change)
network_monitor.add_callback(on_network_change)
```

### Resource Management / 资源管理
```python
from gomoku_world.utils.resources import resource_manager
from gomoku_world.i18n import i18n_manager
from gomoku_world.theme import theme

# Load resources
resource_manager.load_resources()

# Get translations
texts = resource_manager.get_texts(i18n_manager.current_language)

# Get theme
current_theme = resource_manager.get_theme(theme.current_theme)
```

## Plugin Examples / 插件示例

### Game Plugin / 游戏插件

### UI Plugin / 界面插件

### AI Plugin / AI插件 