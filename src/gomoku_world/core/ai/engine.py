"""
AI engine implementation
AI引擎实现
"""

from typing import Tuple, List, Optional
from ..board import Board
from .strategies import MinMaxStrategy, MCTSStrategy
from .evaluation import PositionEvaluator
from ...utils.logger import get_logger

logger = get_logger(__name__)

class AI:
    """
    AI engine that manages game strategies and move generation
    管理游戏策略和移动生成的AI引擎
    """
    
    def __init__(self, difficulty: str = "medium"):
        """
        Initialize AI engine
        初始化AI引擎
        
        Args:
            difficulty: AI difficulty level ("easy", "medium", "hard")
        """
        self.difficulty = difficulty
        self.minmax_strategy = MinMaxStrategy()
        self.mcts_strategy = MCTSStrategy()
        self.evaluator = PositionEvaluator()
        
        # Set depth based on difficulty
        self.depth = self._get_depth_for_difficulty()
        
        logger.info(f"AI engine initialized with {difficulty} difficulty")
    
    def _get_depth_for_difficulty(self) -> int:
        """
        Get search depth based on difficulty
        根据难度获取搜索深度
        
        Returns:
            int: Search depth
        """
        depths = {
            "easy": 2,
            "medium": 4,
            "hard": 6
        }
        return depths.get(self.difficulty, 4)
    
    def get_move(self, board: Board, player: int) -> Tuple[int, int]:
        """
        Get next move for the AI
        获取AI的下一步移动
        
        Args:
            board: Current game board
            player: Current player (1 or 2)
            
        Returns:
            Tuple[int, int]: Row and column of the move
        """
        # Use different strategies based on difficulty
        if self.difficulty == "hard":
            # Use MCTS for hard difficulty
            move = self.mcts_strategy.get_move(board, player)
        else:
            # Use MinMax with alpha-beta pruning for easy/medium
            move = self.minmax_strategy.get_move(
                board, 
                player, 
                self.depth
            )
        
        logger.debug(f"AI selected move: {move}")
        return move
    
    def set_difficulty(self, difficulty: str):
        """
        Set AI difficulty level
        设置AI难度等级
        
        Args:
            difficulty: New difficulty level
        """
        self.difficulty = difficulty
        self.depth = self._get_depth_for_difficulty()
        logger.info(f"AI difficulty set to {difficulty}")
    
    def evaluate_position(self, board: Board, player: int) -> float:
        """
        Evaluate current board position
        评估当前棋盘局面
        
        Args:
            board: Current game board
            player: Player to evaluate for
            
        Returns:
            float: Position score
        """
        return self.evaluator.evaluate(board, player)
    
    def get_best_moves(self, board: Board, player: int, 
                      num_moves: int = 3) -> List[Tuple[int, int]]:
        """
        Get top N best moves
        获取前N个最佳移动
        
        Args:
            board: Current game board
            player: Current player
            num_moves: Number of moves to return
            
        Returns:
            List[Tuple[int, int]]: List of best moves
        """
        moves = []
        scores = []
        
        # Evaluate all valid moves
        for move in board.get_empty_cells():
            # Try move
            board.place_piece(move[0], move[1], player)
            score = self.evaluate_position(board, player)
            board.clear_cell(move[0], move[1])
            
            # Add to sorted list
            moves.append(move)
            scores.append(score)
        
        # Sort by score and return top N
        sorted_moves = [x for _, x in sorted(
            zip(scores, moves),
            reverse=True
        )]
        
        return sorted_moves[:num_moves] 