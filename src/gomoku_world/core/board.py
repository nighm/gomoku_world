"""
Game logic module for the Gomoku game.
This module contains the core game mechanics and board state management.
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass
import logging
import numpy as np
from ..utils.logger import get_logger

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = get_logger(__name__)

@dataclass
class Position:
    """Represents a position on the game board"""
    row: int
    col: int

class GameError(Exception):
    """Base exception class for game-related errors"""
    pass

class InvalidMoveError(GameError):
    """Exception raised for invalid moves"""
    pass

class Game:
    """
    Main game class that handles the game logic and board state.
    
    Attributes:
        size (int): The size of the game board (size x size)
        board (List[List[int]]): The game board represented as a 2D list
        current_player (int): The current player (1 for black, 2 for white)
        move_history (List[Position]): History of moves made in the game
        winner (Optional[int]): The winner of the game (None if game is not over)
        _game_over (bool): Indicates if the game is over
    """
    
    def __init__(self, size: int = 15):
        """
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
        self.current_player = 1  # 1浠ｈ〃榛戝瓙锛?浠ｈ〃鐧藉瓙
        self.move_history = []
        self.winner = None
        self._game_over = False
        logger.info(f"New game started with board size {size}")
    
    def make_move(self, row: int, col: int) -> bool:
        """灏濊瘯鍦ㄦ寚瀹氫綅缃惤瀛?""
        if not (0 <= row < self.size and 0 <= col < self.size):
            raise InvalidMoveError("Move is outside the board")
            
        if self.board[row, col] != 0:
            raise InvalidMoveError("Position is already occupied")
            
        self.board[row, col] = self.current_player
        self.move_history.append(Position(row, col))
        logger.info(f"Player {self.current_player} moved to position ({row}, {col})")
        
        if self.check_winner(row, col):
            self.winner = self.current_player
        
        self.current_player = 3 - self.current_player  # 鍒囨崲鐜╁锛?->2鎴?->1锛?        return True
    
    def check_winner(self, row: int, col: int) -> bool:
        """妫€鏌ユ槸鍚︽湁鐜╁鑾疯儨"""
        directions = [
            [(0, 1), (0, -1)],   # 姘村钩
            [(1, 0), (-1, 0)],   # 鍨傜洿
            [(1, 1), (-1, -1)],  # 涓诲瑙掔嚎
            [(1, -1), (-1, 1)]   # 鍓瑙掔嚎
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
        """閲嶇疆娓告垙"""
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
    Represents the game board
    琛ㄧず娓告垙妫嬬洏
    """
    
    def __init__(self, size: int = 15):
        """
        Initialize board
        鍒濆鍖栨鐩?        
        Args:
            size: Board size (default: 15)
        """
        self.size = size
        self.board = np.zeros((size, size), dtype=np.int8)
        logger.info(f"Board initialized with size {size}")
    
    def is_valid_move(self, row: int, col: int) -> bool:
        """
        Check if a move is valid
        妫€鏌ョЩ鍔ㄦ槸鍚︽湁鏁?        
        Args:
            row: Row number
            col: Column number
            
        Returns:
            bool: True if move is valid
        """
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False
        return self.board[row, col] == 0
    
    def place_piece(self, row: int, col: int, player: int):
        """
        Place a piece on the board
        鍦ㄦ鐩樹笂鏀剧疆妫嬪瓙
        
        Args:
            row: Row number
            col: Column number
            player: Player number (1 or 2)
        """
        if not self.is_valid_move(row, col):
            raise ValueError(f"Invalid move at ({row}, {col})")
        self.board[row, col] = player
        logger.debug(f"Piece placed at ({row}, {col}) by player {player}")
    
    def clear_cell(self, row: int, col: int):
        """
        Clear a cell on the board
        娓呴櫎妫嬬洏涓婄殑涓€涓綅缃?        
        Args:
            row: Row number
            col: Column number
        """
        self.board[row, col] = 0
        logger.debug(f"Cell cleared at ({row}, {col})")
    
    def clear(self):
        """
        Clear the entire board
        娓呯┖鏁翠釜妫嬬洏
        """
        self.board.fill(0)
        logger.info("Board cleared")
    
    def get_piece(self, row: int, col: int) -> int:
        """
        Get the piece at a position
        鑾峰彇鎸囧畾浣嶇疆鐨勬瀛?        
        Args:
            row: Row number
            col: Column number
            
        Returns:
            int: 0 for empty, 1 for black, 2 for white
        """
        return self.board[row, col]
    
    def is_full(self) -> bool:
        """
        Check if board is full
        妫€鏌ユ鐩樻槸鍚﹀凡婊?        
        Returns:
            bool: True if board is full
        """
        return np.all(self.board != 0)
    
    def get_empty_cells(self) -> List[Tuple[int, int]]:
        """
        Get all empty cells
        鑾峰彇鎵€鏈夌┖浣嶇疆
        
        Returns:
            List[Tuple[int, int]]: List of empty cell coordinates
        """
        empty = np.where(self.board == 0)
        return list(zip(empty[0], empty[1]))
    
    def __str__(self) -> str:
        """
        String representation of the board
        妫嬬洏鐨勫瓧绗︿覆琛ㄧず
        
        Returns:
            str: Board representation
        """
        return str(self.board) 
