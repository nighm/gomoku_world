"""AI implementation for Gomoku.

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

from typing import Tuple
from .board import Board
from .ai.strategy import AIStrategy
from .ai.search import AISearch
from .ai.evaluation import AIEvaluation
from .ai.cache import AICache
from ..utils.logger import get_logger

logger = get_logger(__name__)

class AI:
    """AI player implementation using MinMax algorithm with alpha-beta pruning.
    
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
        """Initialize AI player.
        
        初始化AI玩家。
        
        Args:
            difficulty (str): AI difficulty level ('easy', 'medium', 'hard').
                            AI难度级别（'easy'、'medium'、'hard'）。
        """
        self.strategy = AIStrategy(difficulty)
        self.evaluation = AIEvaluation()
        self.search = AISearch(self.strategy, self.evaluation)
        self.cache = AICache()
        logger.info(f"AI initialized with {difficulty} difficulty / AI已初始化，难度为{difficulty}")
    
    def get_move(self, board: Board, player: int) -> Tuple[int, int]:
        """Get the best move for the current position.
        
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
        # 尝试从缓存获取最佳移动
        cached_move = self.cache.get_best_move(board, player)
        if cached_move is not None:
            return cached_move
            
        # 使用搜索系统获取最佳移动
        best_move = self.search.get_best_move(board, player)
        
        # 缓存结果
        self.cache.set_best_move(board, player, best_move)
        
        return best_move
    
    def set_difficulty(self, difficulty: str):
        """Set AI difficulty level.
        
        设置AI难度级别。
        
        Args:
            difficulty (str): New difficulty level ('easy', 'medium', 'hard').
                            新的难度级别（'easy'、'medium'、'hard'）。
        """
        self.strategy = AIStrategy(difficulty)
        self.search = AISearch(self.strategy, self.evaluation)
        self.cache.clear()
        logger.info(f"AI difficulty set to {difficulty} / AI难度设置为{difficulty}")
