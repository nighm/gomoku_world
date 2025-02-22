"""
Game rules implementation module.

游戏规则实现模块。

This module implements the core game rules for Gomoku, including:
- Win condition checking
- Draw condition checking
- Move validation
- Valid move generation

本模块实现五子棋的核心游戏规则，包括：
- 胜利条件检查
- 平局条件检查
- 移动验证
- 有效移动生成
"""

from typing import List, Tuple

# 浣跨敤鐩稿瀵煎叆
from .board import Board
from ..utils.logger import get_logger

logger = get_logger(__name__)

class Rules:
    """
    Game rules and win condition checking.
    
    游戏规则和胜负判定。
    
    This class provides static methods for:
    - Checking if a move results in a win
    - Checking if the game is a draw
    - Validating moves
    - Generating valid moves
    
    此类提供以下静态方法：
    - 检查一步是否导致胜利
    - 检查游戏是否平局
    - 验证移动
    - 生成有效移动
    """
    
    @staticmethod
    def check_win(board: Board, last_row: int, last_col: int) -> bool:
        """
        Check if the last move resulted in a win.
        
        检查最后一步是否导致胜利。
        
        Args:
            board (Board): Game board instance.
                         游戏棋盘实例。
            last_row (int): Row of the last move.
                          最后一步的行号。
            last_col (int): Column of the last move.
                          最后一步的列号。
            
        Returns:
            bool: True if the move resulted in a win, False otherwise.
                 如果这步导致胜利则为True，否则为False。
        """
        player = board.get_piece(last_row, last_col)
        directions = [
            [(0, 1), (0, -1)],   # Horizontal / 水平
            [(1, 0), (-1, 0)],   # Vertical / 垂直
            [(1, 1), (-1, -1)],  # Diagonal / 对角线
            [(1, -1), (-1, 1)]   # Anti-diagonal / 反对角线
        ]
        
        for dir_pair in directions:
            count = 1  # Count the piece itself / 计数当前棋子
            
            # Check both directions / 检查两个方向
            for dx, dy in dir_pair:
                x, y = last_row + dx, last_col + dy
                while (0 <= x < board.size and 
                       0 <= y < board.size and 
                       board.get_piece(x, y) == player):
                    count += 1
                    if count >= 5:
                        logger.info(f"Win detected for player {player}")
                        return True
                    x, y = x + dx, y + dy
                    
        return False
    
    @staticmethod
    def is_draw(board: Board) -> bool:
        """
        Check if the game is a draw.
        
        检查游戏是否平局。
        
        Args:
            board (Board): Game board instance.
                         游戏棋盘实例。
            
        Returns:
            bool: True if the game is a draw, False otherwise.
                 如果游戏是平局则为True，否则为False。
        """
        return board.is_full()
    
    @staticmethod
    def get_valid_moves(board: Board) -> List[Tuple[int, int]]:
        """
        Get all valid moves on the board.
        
        获取棋盘上所有有效的移动。
        
        Args:
            board (Board): Game board instance.
                         游戏棋盘实例。
            
        Returns:
            List[Tuple[int, int]]: List of valid move coordinates (row, col).
                                  有效移动坐标列表（行号，列号）。
        """
        return board.get_empty_cells()
    
    @staticmethod
    def is_valid_move(board: Board, row: int, col: int) -> bool:
        """
        Check if a move is valid.
        
        检查移动是否有效。
        
        Args:
            board (Board): Game board instance.
                         游戏棋盘实例。
            row (int): Row of the move.
                      移动的行号。
            col (int): Column of the move.
                      移动的列号。
            
        Returns:
            bool: True if the move is valid, False otherwise.
                 如果移动有效则为True，否则为False。
        """
        return board.is_valid_move(row, col) 
