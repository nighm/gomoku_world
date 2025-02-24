"""
Game board module for the Gomoku game.

五子棋游戏的棋盘模块。

This module contains the core game board mechanics and state management,
including board representation, move validation, and game state tracking.

本模块包含核心游戏棋盘机制和状态管理，
包括棋盘表示、移动验证和游戏状态跟踪。
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass
import logging
import numpy as np
from ..utils.logger import get_logger

# Configure logging / 配置日志
logging.basicConfig(level=logging.INFO)
logger = get_logger(__name__)

@dataclass
class Position:
    """
    Represents a position on the game board.
    
    表示棋盘上的一个位置。
    
    Attributes:
        row (int): Row index (0-based).
                  行索引（从0开始）。
        col (int): Column index (0-based).
                  列索引（从0开始）。
    """
    row: int
    col: int

class GameError(Exception):
    """
    Base exception class for game-related errors.
    
    游戏相关错误的基础异常类。
    """
    pass

class InvalidMoveError(GameError):
    """
    Exception raised for invalid moves.
    
    无效移动时抛出的异常。
    """
    pass

class Game:
    """
    Main game class that handles the game logic and board state.
    
    Attributes:
        size (int): The size of the game board (size x size)
        board (np.ndarray): The game board represented as a numpy array
        current_player (int): The current player (1 for black, 2 for white)
        move_history (List[Position]): History of moves made in the game
        winner (Optional[int]): The winner of the game (None if game is not over)
        _game_over (bool): Indicates if the game is over
    """
    
    def __init__(self, size: int = 15):
        """
        Initialize the game board.
        
        Initialize the game board.
        
        Args:
            size (int): The size of the board (default: 15)
        
        Raises:
            ValueError: If size is less than 5
        """
        if size < 5:
            raise ValueError("Board size must be at least 5")
        
        self.size = size
        self.board = np.zeros((size, size), dtype=np.int8)
        self.current_player = 1  # 1 represents black, 2 represents white
        self.move_history = []
        self.winner = None
        self._game_over = False
        logger.info(f"New game started with board size {size}")
    
    def make_move(self, row: int, col: int) -> bool:
        """Try to place a piece at the specified position"""
        if not (0 <= row < self.size and 0 <= col < self.size):
            raise InvalidMoveError("Move is outside the board")
            
        if self.board[row, col] != 0:
            raise InvalidMoveError("Position is already occupied")
            
        self.board[row, col] = self.current_player
        self.move_history.append(Position(row, col))
        logger.info(f"Player {self.current_player} moved to position ({row}, {col})")
        
        if self.check_winner(row, col):
            self.winner = self.current_player
        
        self.current_player = 3 - self.current_player  # Switch players: 1->2 or 2->1
        return True
    
    def check_winner(self, row: int, col: int) -> bool:
        """Check if any player has won"""
        directions = [
            [(0, 1), (0, -1)],   # Horizontal
            [(1, 0), (-1, 0)],   # Vertical
            [(1, 1), (-1, -1)],  # Main diagonal
            [(1, -1), (-1, 1)]   # Anti-diagonal
        ]
        
        piece = self.board[row, col]
        
        for dir_pair in directions:
            count = 1
            
            for dx, dy in dir_pair:
                x, y = row + dx, col + dy
                while (0 <= x < self.size and 
                       0 <= y < self.size and 
                       self.board[x, y] == piece):
                    count += 1
                    x += dx
                    y += dy
            
            if count >= 5:
                logger.info(f"Player {piece} won the game!")
                return True
                
        return False
    
    def reset(self):
        """Reset the game"""
        self.board.fill(0)
        self.current_player = 1
        self.move_history.clear()
        self.winner = None
        self._game_over = False
        logger.info("Game reset")
    
    def get_valid_moves(self) -> List[Position]:
        """
        Get a list of all valid moves.
        
        Returns:
            List[Position]: List of valid move positions
        """
        empty_cells = np.where(self.board == 0)
        return [Position(row, col) for row, col in zip(empty_cells[0], empty_cells[1])]
    
    def is_board_full(self) -> bool:
        """
        Check if the board is full (draw condition).
        
        Returns:
            bool: True if the board is full
        """
        return len(self.get_valid_moves()) == 0
    
    def is_game_over(self) -> bool:
        """
        Check if the game is over.
        
        Returns:
            bool: True if the game is over (win or draw)
        """
        return self.winner is not None or self.is_board_full()
    
    def get_winner(self) -> Optional[int]:
        """
        Get the winner of the game.
        
        Returns:
            Optional[int]: Player number of winner, or None if no winner
        """
        return self.winner 

class Board:
    """
    Game board class that manages the board state and move validation.
    
    Management board state and move validation game board class.
    
    Attributes:
        size (int): The size of the game board (size x size).
                    Game board size (size x size).
        board (numpy.ndarray): The game board represented as a 2D array.
                              Game board represented as a 2D array.
        move_history (List[Position]): History of moves made in the game.
                                      Game moves history.
        shape (Tuple[int, int]): The shape of the board (rows, columns).
    """
    
    def __init__(self, size: int = 15):
        """
        Initialize the game board.
        
        Initialize the game board.
        
        Args:
            size (int): The size of the board (default: 15).
                        Game board size (default: 15).
        
        Raises:
            ValueError: If size is less than 5 or greater than 19.
                       If size is less than 5 or greater than 19.
        """
        if not 5 <= size <= 19:
            raise ValueError("Board size must be between 5 and 19 / Game board size must be between 5 and 19")
            
        self.size = size
        self.board = np.zeros((size, size), dtype=np.int8)
        self.move_history = []
        
    @property
    def shape(self) -> Tuple[int, int]:
        """Get the shape of the board"""
        return self.board.shape
        
    def copy(self) -> 'Board':
        """Create a deep copy of the board"""
        new_board = Board(self.size)
        new_board.board = self.board.copy()
        new_board.move_history = self.move_history.copy()
        return new_board
        
    def is_valid_move(self, row: int, col: int) -> bool:
        """
        Check if a move is valid.
        
        Check if a move is valid.
        
        Args:
            row (int): Row index of the move.
                       Move row index.
            col (int): Column index of the move.
                       Move column index.
                      
        Returns:
            bool: True if the move is valid, False otherwise.
                  If the move is valid then return True, otherwise return False.
                  
        Raises:
            ValueError: If coordinates are out of board bounds.
        """
        if not (0 <= row < self.size and 0 <= col < self.size):
            raise ValueError(f"Coordinates ({row}, {col}) are out of board bounds")
            
        return self.board[row, col] == 0
                
    def place_piece(self, row: int, col: int, player: int) -> bool:
        """
        Place a piece on the board.
        
        Place a piece on the board.
        
        Args:
            row (int): Row index.
                       Move row index.
            col (int): Column index.
                       Move column index.
            player (int): Player number (1 for black, 2 for white).
                          Player number (1 for black, 2 for white).
                         
        Returns:
            bool: True if the piece was placed successfully, False otherwise.
            
        Raises:
            ValueError: If coordinates are out of board bounds.
        """
        if not (0 <= row < self.size and 0 <= col < self.size):
            raise ValueError(f"Coordinates ({row}, {col}) are out of board bounds")
            
        if self.board[row, col] != 0:
            return False
                
        self.board[row, col] = player
        self.move_history.append(Position(row, col))
        return True
        
    def clear_cell(self, row: int, col: int):
        """
        Clear a cell on the board.
        
        Clear a cell on the board.
        
        Args:
            row (int): Row index.
                       Move row index.
            col (int): Column index.
                       Move column index.
        """
        self.board[row, col] = 0
        
    def clear(self):
        """
        Clear the entire board.
        
        Clear the entire board.
        """
        self.board.fill(0)
        self.move_history.clear()
        
    def get_piece(self, row: int, col: int) -> int:
        """
        Get the piece at a specific position.
        
        Get the piece at a specific position.
        
        Args:
            row (int): Row index.
                       Move row index.
            col (int): Column index.
                       Move column index.
                      
        Returns:
            int: The piece value (0 for empty, 1 for black, 2 for white).
                  The piece value (0 for empty, 1 for black, 2 for white).
        """
        return self.board[row, col]
        
    def is_full(self) -> bool:
        """
        Check if the board is full.
        
        Check if the board is full.
        
        Returns:
            bool: True if the board is full, False otherwise.
                  If the board is full then return True, otherwise return False.
        """
        return np.all(self.board != 0)
        
    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """
        Get all empty cells on the board.
        
        Get all empty cells on the board.
        
        Returns:
            List[Tuple[int, int]]: List of (row, col) tuples for empty cells.
                                   List of (row, col) tuples for empty cells.
        """
        return list(zip(*np.where(self.board == 0)))
        
    def __str__(self) -> str:
        """
        Get string representation of the board.
        
        Get string representation of the board.
        
        Returns:
            str: ASCII representation of the board.
                  ASCII representation of the board.
        """
        return str(self.board)
