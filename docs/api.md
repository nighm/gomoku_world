# API Documentation

This document provides detailed information about the Gomoku game's API.

## Game Module (`game.py`)

### Class: `Game`

The main game logic class that handles the game state and rules.

#### Attributes

- `size` (int): The size of the game board (size x size)
- `board` (List[List[int]]): The game board represented as a 2D list
- `current_player` (int): The current player (1 for black, 2 for white)
- `move_history` (List[Position]): History of moves made in the game

#### Methods

##### `__init__(size: int = 15)`
Initialize a new game with specified board size.

Parameters:
- `size`: Board size (default: 15)

Raises:
- `ValueError`: If size is less than 5

##### `make_move(row: int, col: int) -> bool`
Attempt to make a move at the specified position.

Parameters:
- `row`: Row index
- `col`: Column index

Returns:
- `bool`: True if move was successful

Raises:
- `InvalidMoveError`: If the move is invalid

##### `check_winner(row: int, col: int) -> bool`
Check if the last move resulted in a win.

Parameters:
- `row`: Row index of last move
- `col`: Column index of last move

Returns:
- `bool`: True if the move resulted in a win

##### `reset()`
Reset the game to its initial state.

##### `get_valid_moves() -> List[Position]`
Get a list of all valid moves.

Returns:
- List of valid move positions

##### `is_board_full() -> bool`
Check if the board is full.

Returns:
- `bool`: True if the board is full

### Class: `Position`

Represents a position on the game board.

#### Attributes

- `row` (int): Row index
- `col` (int): Column index

### Exceptions

#### `GameError`
Base exception class for game-related errors.

#### `InvalidMoveError`
Exception raised for invalid moves.

## GUI Module (`gui.py`)

### Class: `GomokuGUI`

Handles the graphical interface and user interaction.

#### Attributes

- `WINDOW_SIZE` (int): Size of the game window
- `BOARD_SIZE` (int): Number of board intersections
- `GRID_SIZE` (int): Size of each grid cell
- `PIECE_SIZE` (int): Size of game pieces

#### Methods

##### `__init__(window_size: int = 800, board_size: int = 15)`
Initialize the GUI.

Parameters:
- `window_size`: Window size in pixels
- `board_size`: Number of board intersections

##### `run()`
Start the game loop.

##### `draw_board()`
Draw the game board and grid lines.

##### `draw_pieces()`
Draw all pieces on the board.

##### `handle_click(pos: Tuple[int, int]) -> bool`
Handle mouse click events.

Parameters:
- `pos`: Mouse position in pixels

Returns:
- `bool`: True if a valid move was made

## Configuration

### Settings (`config/settings.py`)

Contains game configuration constants:

- Board size and rules
- Display settings
- Colors
- Timing
- Logging settings
- Development options

### Logging (`config/logging_config.py`)

Configures the logging system:

- Log file location and format
- Console and file handlers
- Log levels
- Timestamp formatting

## Network Module (`network.py`)

### Class: `NetworkMonitor`

Monitors network connectivity and provides status updates.

#### Attributes

- `_callbacks` (List[Callable]): List of status change callbacks
- `_is_running` (bool): Whether monitoring is active
- `_check_interval` (int): Interval between checks in seconds

#### Methods

##### `__init__(check_interval: int = 60)`
Initialize the network monitor.

Parameters:
- `check_interval`: Time between checks in seconds

##### `start()`
Start network monitoring.

##### `stop()`
Stop network monitoring.

##### `is_online() -> bool`
Check if network is available.

Returns:
- `bool`: True if network is available

##### `add_callback(callback: Callable[[bool], None])`
Add a status change callback.

Parameters:
- `callback`: Function to call on status change

##### `remove_callback(callback: Callable[[bool], None])`
Remove a status change callback.

Parameters:
- `callback`: Callback to remove

##### `get_quality_metrics() -> Dict[str, float]`
Get network quality metrics.

Returns:
- Dictionary with metrics (latency, packet loss, bandwidth)

### Class: `NetworkConfig`

Manages network configuration settings.

#### Methods

##### `load_config()`
Load network configuration.

##### `save_config()`
Save network configuration.

##### `get_proxy_settings() -> Dict[str, Any]`
Get proxy configuration.

Returns:
- Dictionary with proxy settings

##### `set_proxy_settings(settings: Dict[str, Any])`
Set proxy configuration.

Parameters:
- `settings`: Proxy settings dictionary

## I18n Module (`i18n.py`)

### Class: `I18nManager`

Manages internationalization and translations.

#### Attributes

- `_translations` (Dict[str, Dict]): Translation data
- `_current_language` (str): Current language code
- `_fallback_language` (str): Fallback language code
- `_callbacks` (List[Callable]): Language change callbacks

#### Methods

##### `__init__()`
Initialize the i18n manager.

##### `initialize()`
Initialize the i18n system.

##### `set_language(language_code: str)`
Switch to specified language.

Parameters:
- `language_code`: Language code to switch to

##### `get_text(key: str, category: str = "common", **kwargs) -> str`
Get translated text for key.

Parameters:
- `key`: Translation key
- `category`: Resource category
- `**kwargs`: Format parameters

Returns:
- Translated text

##### `on_language_change(callback: Callable[[str], None])`
Register language change callback.

Parameters:
- `callback`: Function to call on language change

##### `get_available_languages() -> List[str]`
Get list of available languages.

Returns:
- List of language codes

### Class: `ResourceManager`

Manages i18n resources and fonts.

#### Methods

##### `load_resources()`
Load all i18n resources.

##### `get_resource(path: str) -> Dict`
Get resource by path.

Parameters:
- `path`: Resource path

Returns:
- Resource data

##### `validate_resource(path: str) -> bool`
Validate resource file.

Parameters:
- `path`: Resource path

Returns:
- True if valid

### Class: `FontManager`

Manages fonts for different languages.

#### Methods

##### `get_font(language: str) -> str`
Get font for language.

Parameters:
- `language`: Language code

Returns:
- Font name

##### `set_font(language: str, font: str)`
Set font for language.

Parameters:
- `language`: Language code
- `font`: Font name

##### `get_cjk_font() -> str`
Get CJK font.

Returns:
- CJK font name

## Usage Examples

### Basic Game Usage

```python
from gomoku.game import Game

# Create a new game
game = Game(size=15)

# Make moves
game.make_move(7, 7)  # Black's move
game.make_move(8, 8)  # White's move

# Check for winner
if game.check_winner(8, 8):
    print("White wins!")
```

### GUI Usage

```python
from gomoku.gui import GomokuGUI

# Create and start the game
gui = GomokuGUI()
gui.run()
```

### Custom Board Size

```python
from gomoku.game import Game
from gomoku.gui import GomokuGUI

# Create a smaller board
game = Game(size=9)
gui = GomokuGUI(board_size=9)
gui.run()
```

### Network Monitoring

```python
from gomoku.network import network_monitor

# Start monitoring
network_monitor.start()

# Add status callback
def on_status_change(is_online):
    print(f"Network status: {'online' if is_online else 'offline'}")

network_monitor.add_callback(on_status_change)

# Check status
if network_monitor.is_online():
    print("Network is available")

# Get quality metrics
metrics = network_monitor.get_quality_metrics()
print(f"Latency: {metrics['latency']}ms")
```

### Internationalization

```python
from gomoku.i18n import i18n_manager

# Initialize i18n
i18n_manager.initialize()

# Get translated text
title = i18n_manager.get_text("game.title")
status = i18n_manager.get_text("game.status.your_turn")

# Switch language
i18n_manager.set_language("zh")

# Add language change callback
def on_language_change(language):
    print(f"Language changed to: {language}")

i18n_manager.on_language_change(on_language_change)
```

### Network-Aware I18n

```python
from gomoku.network import network_monitor
from gomoku.i18n import i18n_manager

# Initialize systems
i18n_manager.initialize()
network_monitor.start()

# Update status with translations
def update_status(is_online):
    status = "online" if is_online else "offline"
    text = i18n_manager.get_text(f"network.status.{status}")
    print(f"Network status: {text}")

network_monitor.add_callback(update_status)
``` 