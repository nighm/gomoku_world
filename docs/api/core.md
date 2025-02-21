# Core Module API Reference / 核心模块 API 参考

## Board Class / 棋盘类

The `Board` class represents the game board and provides methods for piece placement and board state management.
`Board` 类表示游戏棋盘，提供放置棋子和管理棋盘状态的方法。

### Methods / 方法

#### `__init__(size: int = 15)`
Initialize a new game board.
初始化新的游戏棋盘。
- `size`: Board size (default: 15x15) / 棋盘大小（默认：15x15）

#### `place_piece(row: int, col: int, player: int) -> bool`
Place a piece on the board.
在棋盘上放置棋子。
- `row`: Row number (0-based) / 行号（从0开始）
- `col`: Column number (0-based) / 列号（从0开始）
- `player`: Player number (1 for black, 2 for white) / 玩家编号（1为黑子，2为白子）
- Returns / 返回值: `True` if placement successful, `False` otherwise / 放置成功返回`True`，否则返回`False`

#### `get_piece(row: int, col: int) -> int`
Get the piece at the specified position.
获取指定位置的棋子。
- Returns / 返回值: 0 for empty, 1 for black, 2 for white / 0表示空位，1表示黑子，2表示白子

#### `clear()`
Clear the board to its initial state.
清空棋盘至初始状态。

## Rules Class / 规则类

The `Rules` class implements game rules and victory conditions.
`Rules` 类实现游戏规则和胜利条件。

### Methods / 方法

#### `check_win(board: Board, row: int, col: int) -> bool`
Check if the current move results in a win.
检查当前落子是否获胜。
- `board`: Game board / 游戏棋盘
- `row`: Row of last move / 最后一步的行号
- `col`: Column of last move / 最后一步的列号
- Returns / 返回值: `True` if the move wins the game / 如果该步获胜则返回`True`

#### `get_valid_moves(board: Board) -> List[Tuple[int, int]]`
Get all valid moves on the current board.
获取当前棋盘上所有有效的落子位置。
- Returns / 返回值: List of (row, col) tuples representing valid moves / 表示有效落子位置的(行号,列号)元组列表

#### `is_draw(board: Board) -> bool`
Check if the game is a draw.
检查游戏是否平局。
- Returns / 返回值: `True` if the game is a draw / 如果游戏为平局则返回`True`

## AI Class / AI类

The `AI` class implements the computer player using minimax algorithm with alpha-beta pruning.
`AI` 类使用带有alpha-beta剪枝的极小化极大算法实现电脑玩家。

### Methods / 方法

#### `get_move(board: Board, player: int) -> Tuple[int, int]`
Get the AI's next move.
获取AI的下一步落子。
- `board`: Current game board / 当前游戏棋盘
- `player`: AI player number (1 or 2) / AI玩家编号（1或2）
- Returns / 返回值: (row, col) tuple representing the chosen move / 表示所选落子位置的(行号,列号)元组

#### `evaluate_position(board: Board, player: int) -> int`
Evaluate the current board position.
评估当前棋盘局势。
- Returns / 返回值: Positive score for favorable positions, negative for unfavorable ones / 有利局势为正分，不利局势为负分 