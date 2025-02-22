"""AI strategy module for Gomoku.

五子棋AI策略模块。

此模块负责AI的策略选择和决策控制：
- 难度级别管理
- 移动优先级
- 时间控制
"""

from typing import Dict
from ..board import Board
from ...utils.logger import get_logger
from ...config import AI_THINKING_TIME

logger = get_logger(__name__)

class AIStrategy:
    """AI strategy management class.
    
    AI策略管理类。
    
    负责：
    - 难度级别设置
    - 时间限制控制
    - 移动优先级管理
    """
    
    def __init__(self, difficulty: str = "medium"):
        """Initialize AI strategy.
        
        初始化AI策略。
        
        Args:
            difficulty (str): AI difficulty level ('easy', 'medium', 'hard').
                            AI难度级别（'easy'、'medium'、'hard'）。
        """
        self.difficulty = difficulty
        self.max_depth = self._get_depth_for_difficulty()
        self.time_limit = AI_THINKING_TIME
        logger.info(f"AI strategy initialized with {difficulty} difficulty / AI策略已初始化，难度为{difficulty}")
    
    def _get_depth_for_difficulty(self) -> int:
        """Get search depth based on difficulty level.
        
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
    
    def get_move_priority(self, board: Board, x: int, y: int) -> float:
        """Calculate priority score for a move.
        
        计算移动的优先级分数。
        
        Args:
            board (Board): Current board state.
                         当前棋盘状态。
            x (int): X coordinate.
                    X坐标。
            y (int): Y coordinate.
                    Y坐标。
                    
        Returns:
            float: Priority score for the move.
                  移动的优先级分数。
        """
        # 基于中心距离计算优先级
        center = board.size // 2
        distance = ((x - center) ** 2 + (y - center) ** 2) ** 0.5
        priority = 1.0 / (1.0 + distance)
        
        # 根据难度调整优先级
        if self.difficulty == "hard":
            priority *= 1.5
        elif self.difficulty == "easy":
            priority *= 0.5
            
        return priority