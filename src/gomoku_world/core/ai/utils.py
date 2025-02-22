"""AI utilities module for Gomoku.

五子棋AI工具模块。

此模块提供AI系统中常用的辅助函数和工具类：
- 局面转换
- 坐标变换
- 性能监控
- 调试工具
"""

from typing import List, Tuple, Dict
from ..board import Board
from ...utils.logger import get_logger

logger = get_logger(__name__)

class AIUtils:
    """AI utilities class.
    
    AI工具类。
    
    提供：
    - 局面转换函数
    - 坐标变换函数
    - 性能监控工具
    - 调试辅助函数
    """
    
    @staticmethod
    def board_to_matrix(board: Board) -> List[List[int]]:
        """Convert board to matrix representation.
        
        将棋盘转换为矩阵表示。
        
        Args:
            board (Board): Game board.
                         游戏棋盘。
                         
        Returns:
            List[List[int]]: Matrix representation of the board.
                            棋盘的矩阵表示。
        """
        return [[board.get_piece(i, j) for j in range(board.size)] 
                for i in range(board.size)]
    
    @staticmethod
    def get_move_coordinates(move: str) -> Tuple[int, int]:
        """Convert move string to coordinates.
        
        将移动字符串转换为坐标。
        
        Args:
            move (str): Move in string format (e.g. 'A1', 'B2').
                       字符串格式的移动（如'A1'、'B2'）。
                       
        Returns:
            Tuple[int, int]: Move coordinates.
                            移动坐标。
        """
        col = ord(move[0].upper()) - ord('A')
        row = int(move[1:]) - 1
        return row, col
    
    @staticmethod
    def get_move_notation(row: int, col: int) -> str:
        """Convert coordinates to move notation.
        
        将坐标转换为移动符号。
        
        Args:
            row (int): Row coordinate.
                      行坐标。
            col (int): Column coordinate.
                      列坐标。
                      
        Returns:
            str: Move in string format.
                 字符串格式的移动。
        """
        return f"{chr(col + ord('A'))}{row + 1}"
    
    @staticmethod
    def get_symmetrical_moves(move: Tuple[int, int], board_size: int) -> List[Tuple[int, int]]:
        """Get symmetrical moves for a given move.
        
        获取给定移动的对称移动。
        
        Args:
            move (Tuple[int, int]): Original move.
                                   原始移动。
            board_size (int): Size of the board.
                            棋盘大小。
                            
        Returns:
            List[Tuple[int, int]]: List of symmetrical moves.
                                  对称移动列表。
        """
        row, col = move
        center = board_size // 2
        
        # 计算对称位置
        symmetrical = [
            (row, col),  # 原始位置
            (row, board_size - 1 - col),  # 水平对称
            (board_size - 1 - row, col),  # 垂直对称
            (board_size - 1 - row, board_size - 1 - col),  # 中心对称
        ]
        
        return list(set(symmetrical))  # 去除重复位置
    
    @staticmethod
    def get_move_distance(move1: Tuple[int, int], move2: Tuple[int, int]) -> float:
        """Calculate distance between two moves.
        
        计算两个移动之间的距离。
        
        Args:
            move1 (Tuple[int, int]): First move.
                                    第一个移动。
            move2 (Tuple[int, int]): Second move.
                                    第二个移动。
                                    
        Returns:
            float: Euclidean distance between moves.
                  移动之间的欧几里得距离。
        """
        row1, col1 = move1
        row2, col2 = move2
        return ((row1 - row2) ** 2 + (col1 - col2) ** 2) ** 0.5
    
    @staticmethod
    def get_move_direction(move1: Tuple[int, int], move2: Tuple[int, int]) -> Tuple[int, int]:
        """Get direction vector between two moves.
        
        获取两个移动之间的方向向量。
        
        Args:
            move1 (Tuple[int, int]): First move.
                                    第一个移动。
            move2 (Tuple[int, int]): Second move.
                                    第二个移动。
                                    
        Returns:
            Tuple[int, int]: Direction vector (dx, dy).
                            方向向量(dx, dy)。
        """
        row1, col1 = move1
        row2, col2 = move2
        
        dx = 0 if row1 == row2 else (row2 - row1) // abs(row2 - row1)
        dy = 0 if col1 == col2 else (col2 - col1) // abs(col2 - col1)
        
        return dx, dy