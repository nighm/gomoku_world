"""
Game rules implementation
游戏规则实现
"""

from typing import List, Tuple

# 使用相对导入
from .board import Board
from ..utils.logger import get_logger

logger = get_logger(__name__)

class Rules:
    """
    Game rules and win condition checking
    游戏规则和胜负判定
    """
    
    @staticmethod
    def check_win(board: Board, last_row: int, last_col: int) -> bool:
        """
        Check if the last move resulted in a win
        检查最后一步是否导致胜利
        
        Args:
            board: Game board
            last_row: Row of last move
            last_col: Column of last move
            
        Returns:
            bool: True if the move resulted in a win
        """
        player = board.get_piece(last_row, last_col)
        directions = [
            [(0, 1), (0, -1)],  # Horizontal
            [(1, 0), (-1, 0)],  # Vertical
            [(1, 1), (-1, -1)], # Diagonal
            [(1, -1), (-1, 1)]  # Anti-diagonal
        ]
        
        for dir_pair in directions:
            count = 1  # Count the piece itself
            
            # Check both directions
            for dx, dy in dir_pair:
                x, y = last_row + dx, last_col + dy
                while (0 <= x < board.size and 
                       0 <= y < board.size and 
                       board.get_piece(x, y) == player):
                    count += 1
                    x += dx
                    y += dy
                    
            if count >= 5:
                logger.info(f"Win detected for player {player}")
                return True
                
        return False
    
    @staticmethod
    def is_draw(board: Board) -> bool:
        """
        Check if the game is a draw
        检查游戏是否平局
        
        Args:
            board: Game board
            
        Returns:
            bool: True if game is a draw
        """
        return board.is_full()
    
    @staticmethod
    def get_valid_moves(board: Board) -> List[Tuple[int, int]]:
        """
        Get all valid moves on the board
        获取棋盘上所有有效的移动
        
        Args:
            board: Game board
            
        Returns:
            List[Tuple[int, int]]: List of valid move coordinates
        """
        return board.get_empty_cells()
    
    @staticmethod
    def is_valid_move(board: Board, row: int, col: int) -> bool:
        """
        Check if a move is valid according to game rules
        根据游戏规则检查移动是否有效
        
        Args:
            board: Game board
            row: Row number
            col: Column number
            
        Returns:
            bool: True if move is valid
        """
        return board.is_valid_move(row, col) 