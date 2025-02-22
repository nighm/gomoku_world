"""
AI implementation for Gomoku.

五子棋AI实现。

This module implements an AI player for Gomoku using:
- MinMax algorithm with alpha-beta pruning
- Position evaluation
- Move prioritization
- Multiple difficulty levels

本模块使用以下技术实现五子棋AI玩家：
- 带有alpha-beta剪枝的极小化极大算法
- 位置评估
- 移动优先级
- 多个难度级别
"""

import time
import random
from typing import Tuple, List, Optional
import numpy as np

from .board import Board
from ..utils.logger import get_logger
from ..config import AI_THINKING_TIME, BOARD_SIZE

logger = get_logger(__name__)

class AI:
    """
    AI player implementation using MinMax algorithm with alpha-beta pruning.
    
    使用带有alpha-beta剪枝的极小化极大算法的AI玩家实现。
    
    This class provides:
    - Multiple difficulty levels
    - Position evaluation
    - Move prioritization
    - Time-limited search
    
    此类提供：
    - 多个难度级别
    - 位置评估
    - 移动优先级
    - 时间限制搜索
    """
    
    def __init__(self, difficulty: str = "medium"):
        """
        Initialize AI player.
        
        初始化AI玩家。
        
        Args:
            difficulty (str): AI difficulty level ('easy', 'medium', 'hard').
                            AI难度级别（'easy'、'medium'、'hard'）。
        """
        self.difficulty = difficulty
        self.max_depth = self._get_depth_for_difficulty()
        self.time_limit = AI_THINKING_TIME
        self.cache = {}
        self.nodes_evaluated = 0
        logger.info(f"AI initialized with {difficulty} difficulty / AI已初始化，难度为{difficulty}")
        
    def _clear_cache(self):
        """Clear evaluation cache to prevent memory bloat / 清除评估缓存以防止内存膨胀"""
        if len(self.cache) > 10000:  # Prevent excessive memory usage
            self.cache.clear()
            logger.debug("Evaluation cache cleared / 评估缓存已清除")
    
    def _get_depth_for_difficulty(self) -> int:
        """
        Get search depth based on difficulty level.
        
        根据难度级别获取搜索深度。
        
        Returns:
            int: Search depth for the current difficulty level.
                 当前难度级别的搜索深度。
        """
        return {
            "easy": 2,    # 2 moves ahead / 提前2步
            "medium": 3,  # 3 moves ahead / 提前3步
            "hard": 4     # 4 moves ahead / 提前4步
        }.get(self.difficulty, 3)
    
    def get_move(self, board: Board, player: int) -> Tuple[int, int]:
        """
        Get the best move for the current position.
        
        获取当前位置的最佳移动。
        
        Args:
            board (Board): Current board state.
                         当前棋盘状态。
            player (int): Current player (1 for black, 2 for white).
                        当前玩家（1为黑棋，2为白棋）。
                        
        Returns:
            Tuple[int, int]: Row and column of the best move.
                            最佳移动的行和列。
                            
        Raises:
            RuntimeError: If no valid moves are available.
                        如果没有有效的移动。
        """
        start_time = time.time()
        best_score = float('-inf')
        best_move = None
        
        # Get prioritized moves / 获取优先级移动
        moves = self._get_prioritized_moves(board)
        if not moves:
            raise RuntimeError("No valid moves available / 没有有效的移动")
            
        # For easy difficulty, just return a random move / 对于简单难度，返回随机移动
        if self.difficulty == "easy":
            return self._get_random_move(board)
            
        # Try each move with MinMax / 使用极小化极大算法尝试每个移动
        for row, col in moves:
            if time.time() - start_time > self.time_limit:
                logger.warning("AI move time limit reached / AI移动时间限制已到")
                break
                
            # Make move / 进行移动
            board.place_piece(row, col, player)
            
            # Evaluate move / 评估移动
            score = self._minmax(
                board,
                self.max_depth - 1,
                False,
                3 - player,  # Switch player / 切换玩家
                float('-inf'),
                float('inf')
            )
            
            # Undo move / 撤销移动
            board.clear_cell(row, col)
            
            # Update best move / 更新最佳移动
            if score > best_score:
                best_score = score
                best_move = (row, col)
                
        if best_move is None:
            logger.warning("Using fallback random move / 使用后备随机移动")
            return self._get_random_move(board)
            
        logger.info(f"AI chose move at {best_move} with score {best_score} / AI选择了位置{best_move}，分数为{best_score}")
        return best_move
        
    def _minmax(self, board: Board, depth: int, is_maximizing: bool, 
                player: int, alpha: float, beta: float) -> float:
        """
        MinMax algorithm with alpha-beta pruning.
        
        带有alpha-beta剪枝的极小化极大算法。
        
        Args:
            board (Board): Current board state.
                         当前棋盘状态。
            depth (int): Current search depth.
                       当前搜索深度。
            is_maximizing (bool): Whether this is a maximizing node.
                                是否是最大化节点。
            player (int): Current player.
                        当前玩家。
            alpha (float): Alpha value for pruning.
                         用于剪枝的alpha值。
            beta (float): Beta value for pruning.
                        用于剪枝的beta值。
                        
        Returns:
            float: Score for this position.
                  此位置的分数。
        """
        # Terminal conditions / 终止条件
        if depth == 0 or self._is_terminal(board):
            return self._evaluate_position(board, player)
            
        moves = self._get_prioritized_moves(board)
        
        if is_maximizing:
            max_eval = float('-inf')
            for row, col in moves:
                board.place_piece(row, col, player)
                eval = self._minmax(board, depth - 1, False, 3 - player, alpha, beta)
                board.clear_cell(row, col)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for row, col in moves:
                board.place_piece(row, col, player)
                eval = self._minmax(board, depth - 1, True, 3 - player, alpha, beta)
                board.clear_cell(row, col)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
            
    def _evaluate_position(self, board: Board, player: int) -> float:
        """
        Evaluate the current board position.
        
        评估当前棋盘位置。
        
        Args:
            board (Board): Current board state.
                         当前棋盘状态。
            player (int): Player to evaluate for.
                        要评估的玩家。
                        
        Returns:
            float: Position score (higher is better for the player).
                  位置分数（对玩家来说越高越好）。
        """
        score = 0.0
        
        # Check all directions / 检查所有方向
        directions = [(1,0), (0,1), (1,1), (1,-1)]
        
        for i in range(board.size):
            for j in range(board.size):
                if board.get_piece(i, j) == 0:
                    continue
                    
                for dx, dy in directions:
                    count = self._count_consecutive(board, i, j, dx, dy, player)
                    score += self._score_sequence(count, player)
                    
        return score
        
    def _count_consecutive(self, board: Board, row: int, col: int, 
                          dx: int, dy: int, player: int) -> int:
        """
        Count consecutive pieces in a direction.
        
        计算一个方向上连续的棋子。
        
        Args:
            board (Board): Current board state.
                         当前棋盘状态。
            row (int): Starting row.
                      起始行。
            col (int): Starting column.
                      起始列。
            dx (int): Row direction (0, 1, or -1).
                     行方向（0、1或-1）。
            dy (int): Column direction (0, 1, or -1).
                     列方向（0、1或-1）。
            player (int): Player to count for.
                        要计数的玩家。
                        
        Returns:
            int: Number of consecutive pieces.
                 连续棋子的数量。
        """
        count = 0
        x, y = row, col
        
        while (0 <= x < board.size and 
               0 <= y < board.size and 
               board.get_piece(x, y) == player):
            count += 1
            x, y = x + dx, y + dy
            
        return count
        
    def _score_sequence(self, count: int, player: int) -> float:
        """
        Score a sequence of consecutive pieces.
        
        对连续棋子序列评分。
        
        Args:
            count (int): Number of consecutive pieces.
                       连续棋子的数量。
            player (int): Player who owns the sequence.
                        拥有该序列的玩家。
                        
        Returns:
            float: Score for this sequence.
                  此序列的分数。
        """
        # Scoring weights / 评分权重
        weights = {
            5: 1000000,  # Win / 胜利
            4: 10000,    # Four in a row / 四子连珠
            3: 1000,     # Three in a row / 三子连珠
            2: 100,      # Two in a row / 两子连珠
            1: 10        # Single piece / 单子
        }
        
        return weights.get(count, 0)
        
    def _is_terminal(self, board: Board) -> bool:
        """
        Check if the position is terminal (game over).
        
        检查位置是否为终局（游戏结束）。
        
        Args:
            board (Board): Current board state.
                         当前棋盘状态。
                         
        Returns:
            bool: True if the game is over, False otherwise.
                 如果游戏结束则为True，否则为False。
        """
        # Check for win / 检查胜利
        for i in range(board.size):
            for j in range(board.size):
                if board.get_piece(i, j) != 0:
                    if self._check_win(board, i, j):
                        return True
                        
        # Check for draw / 检查平局
        return board.is_full()
        
    def _check_win(self, board: Board, row: int, col: int) -> bool:
        """Check if there's a win at the given position"""
        piece = board.get_piece(row, col)
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        
        for dx, dy in directions:
            count = 1
            
            # Check forward
            x, y = row + dx, col + dy
            while (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and 
                   board.get_piece(x, y) == piece):
                count += 1
                x += dx
                y += dy
            
            # Check backward
            x, y = row - dx, col - dy
            while (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and 
                   board.get_piece(x, y) == piece):
                count += 1
                x -= dx
                y -= dy
            
            if count >= 5:
                return True
        
        return False
        
    def _get_prioritized_moves(self, board: Board) -> List[Tuple[int, int]]:
        """
        Get moves sorted by priority.
        
        获取按优先级排序的移动。
        
        Args:
            board (Board): Current board state.
                         当前棋盘状态。
                         
        Returns:
            List[Tuple[int, int]]: List of moves sorted by priority.
                                  按优先级排序的移动列表。
        """
        moves = []
        for i in range(board.size):
            for j in range(board.size):
                if board.get_piece(i, j) == 0:
                    score = self._score_move_position(board, i, j)
                    moves.append((score, i, j))
                    
        # Sort by score in descending order / 按分数降序排序
        moves.sort(reverse=True)
        return [(i, j) for _, i, j in moves]
        
    def _score_move_position(self, board: Board, row: int, col: int) -> float:
        """
        Score a potential move position.
        
        对潜在的移动位置评分。
        
        Args:
            board (Board): Current board state.
                         当前棋盘状态。
            row (int): Row of the move.
                      移动的行号。
            col (int): Column of the move.
                      移动的列号。
                      
        Returns:
            float: Position score.
                  位置分数。
        """
        # Distance from center bonus / 距离中心的奖励
        center = board.size // 2
        distance = abs(row - center) + abs(col - center)
        center_score = 1.0 / (distance + 1)
        
        # Adjacency bonus / 相邻奖励
        adjacent_score = 0.0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                x, y = row + dx, col + dy
                if (0 <= x < board.size and 
                    0 <= y < board.size and 
                    board.get_piece(x, y) != 0):
                    adjacent_score += 0.1
                    
        return center_score + adjacent_score
        
    def _get_random_move(self, board: Board) -> Tuple[int, int]:
        """
        Get a random valid move.
        
        获取随机有效移动。
        
        Args:
            board (Board): Current board state.
                         当前棋盘状态。
                         
        Returns:
            Tuple[int, int]: Random valid move coordinates.
                            随机有效移动坐标。
                            
        Raises:
            RuntimeError: If no valid moves are available.
                        如果没有有效的移动。
        """
        empty_cells = board.get_empty_cells()
        if not empty_cells:
            raise RuntimeError("No valid moves available / 没有有效的移动")
        return random.choice(empty_cells)
