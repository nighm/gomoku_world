"""Game module for Gomoku.

五子棋游戏模块。
"""

from typing import Tuple, List, Optional
from .config import BOARD_SIZE, WIN_LENGTH

class InvalidMoveError(Exception):
    """Invalid move error.
    
    无效移动错误。
    """
    pass

class Position:
    """Position on the board.
    
    棋盘上的位置。
    """
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        
    def __eq__(self, other) -> bool:
        if not isinstance(other, Position):
            return False
        return self.x == other.x and self.y == other.y
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

class Game:
    """Game logic implementation.
    
    游戏逻辑实现。
    """
    def __init__(self, board_size: int = BOARD_SIZE):
        """Initialize game.
        
        初始化游戏。
        
        Args:
            board_size: Board size (棋盘大小)
        """
        self.board_size = board_size
        self.board = [[0] * board_size for _ in range(board_size)]
        self.current_player = 1  # 1 for black, 2 for white
        self.moves: List[Position] = []
        self.game_over = False
        self.winner = None
    
    def make_move(self, x: int, y: int) -> bool:
        """Make a move.
        
        落子。
        
        Args:
            x: X coordinate (X坐标)
            y: Y coordinate (Y坐标)
            
        Returns:
            bool: True if move is valid and made
            
        Raises:
            InvalidMoveError: If move is invalid
        """
        if not self.is_valid_move(x, y):
            raise InvalidMoveError(f"Invalid move at position ({x}, {y})")
            
        self.board[x][y] = self.current_player
        self.moves.append(Position(x, y))
        
        if self.check_win(x, y):
            self.game_over = True
            self.winner = self.current_player
            return True
            
        if len(self.moves) == self.board_size * self.board_size:
            self.game_over = True
            return True
            
        self.current_player = 3 - self.current_player  # Switch player
        return True
    
    def is_valid_move(self, x: int, y: int) -> bool:
        """Check if move is valid.
        
        检查移动是否有效。
        
        Args:
            x: X coordinate (X坐标)
            y: Y coordinate (Y坐标)
            
        Returns:
            bool: True if move is valid
        """
        return (
            0 <= x < self.board_size and
            0 <= y < self.board_size and
            self.board[x][y] == 0
        )
    
    def check_win(self, x: int, y: int) -> bool:
        """Check if current player wins.
        
        检查当前玩家是否获胜。
        
        Args:
            x: Last move X coordinate (最后一步X坐标)
            y: Last move Y coordinate (最后一步Y坐标)
            
        Returns:
            bool: True if current player wins
        """
        player = self.board[x][y]
        directions = [(1,0), (0,1), (1,1), (1,-1)]
        
        for dx, dy in directions:
            count = 1
            # Check forward
            tx, ty = x + dx, y + dy
            while (
                0 <= tx < self.board_size and
                0 <= ty < self.board_size and
                self.board[tx][ty] == player
            ):
                count += 1
                tx += dx
                ty += dy
            
            # Check backward
            tx, ty = x - dx, y - dy
            while (
                0 <= tx < self.board_size and
                0 <= ty < self.board_size and
                self.board[tx][ty] == player
            ):
                count += 1
                tx -= dx
                ty -= dy
            
            if count >= WIN_LENGTH:
                return True
                
        return False
    
    def get_winner(self) -> Optional[int]:
        """Get winner.
        
        获取获胜者。
        
        Returns:
            Optional[int]: Winner (1 for black, 2 for white, None if no winner)
        """
        return self.winner
    
    def is_game_over(self) -> bool:
        """Check if game is over.
        
        检查游戏是否结束。
        
        Returns:
            bool: True if game is over
        """
        return self.game_over
    
    def get_board(self) -> List[List[int]]:
        """Get current board state.
        
        获取当前棋盘状态。
        
        Returns:
            List[List[int]]: Current board state
        """
        return self.board
    
    def get_current_player(self) -> int:
        """Get current player.
        
        获取当前玩家。
        
        Returns:
            int: Current player (1 for black, 2 for white)
        """
        return self.current_player