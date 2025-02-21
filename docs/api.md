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