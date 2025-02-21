# GUI Module API Reference

## GomokuGUI Class

The `GomokuGUI` class implements the main game window and user interface.

### Methods

#### `__init__()`
Initialize the game window and GUI components.

#### `run()`
Start the game loop and handle events.

#### `draw()`
Render the game board and UI elements.

#### `handle_click(pos: Tuple[int, int])`
Handle mouse click events.
- `pos`: Mouse position (x, y)

## SettingsMenu Class

The `SettingsMenu` class provides a settings interface for game configuration.

### Methods

#### `__init__(screen: pygame.Surface)`
Initialize the settings menu.
- `screen`: Pygame surface to draw on

#### `show()`
Display the settings menu.
- Returns: Dictionary of updated settings

#### `handle_event(event: pygame.Event)`
Handle user input events.
- Returns: `True` if settings were changed

### Settings Options

- Game Mode:
  - Player vs Player
  - Player vs AI
  - AI vs AI
- Board Size: 15x15 (standard)
- Theme Selection:
  - Classic
  - Modern
  - Dark
- Sound Settings:
  - Effects Volume
  - Background Music Volume
- Language Selection:
  - English
  - 简体中文
  - 繁體中文

## Theme Management

The theme system allows customization of game appearance.

### Available Themes

Each theme defines:
- Colors:
  - Background
  - Grid Lines
  - Pieces (Black/White)
  - UI Elements
- Fonts:
  - Default Font
  - Title Font
- Sizes:
  - Piece Size
  - Button Dimensions
  - Grid Spacing

### Customization

Themes can be modified through JSON configuration files in the `config` directory. 