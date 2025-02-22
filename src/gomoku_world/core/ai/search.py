"""AI search module for Gomoku.

五子棋AI搜索模块。

此模块负责搜索系统：
- 极小化极大算法
- Alpha-Beta剪枝
- 移动生成
- 时间控制
"""

from typing import Tuple, List, Optional
import time
from ..board import Board
from .strategy import AIStrategy
from .evaluation import AIEvaluation
from ...utils.logger import get_logger

logger = get_logger(__name__)

class AISearch:
    """AI search system class.
    
    AI搜索系统类。
    
    负责：
    - 搜索算法实现
    - 移动选择
    - 时间管理
    """
    
    def __init__(self, strategy: AIStrategy, evaluation: AIEvaluation):
        """Initialize AI search system.
        
        初始化AI搜索系统。
        
        Args:
            strategy (AIStrategy): Strategy manager.
                                策略管理器。
            evaluation (AIEvaluation): Evaluation system.
                                    评估系统。
        """
        self.strategy = strategy
        self.evaluation = evaluation
        self.start_time = 0
        self.nodes_evaluated = 0
        logger.info("AI search system initialized / AI搜索系统已初始化")
    
    def get_best_move(self, board: Board, player: int) -> Tuple[int, int]:
        """Get the best move using MinMax with alpha-beta pruning.
        
        使用带Alpha-Beta剪枝的极小化极大算法获取最佳移动。
        
        Args:
            board (Board): Current board state.
                         当前棋盘状态。
            player (int): Current player (1 for black, 2 for white).
                        当前玩家（1为黑棋，2为白棋）。
                        
        Returns:
            Tuple[int, int]: Best move coordinates (x, y).
                            最佳移动坐标(x, y)。
        """
        self.start_time = time.time()
        self.nodes_evaluated = 0
        
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        
        # 获取所有可能的移动
        valid_moves = self._get_valid_moves(board)
        
        # 按优先级排序移动
        valid_moves.sort(key=lambda m: self.strategy.get_move_priority(board, m[0], m[1]), reverse=True)
        
        for move in valid_moves:
            if self._is_time_up():
                break
                
            # 尝试移动
            board.place_piece(move[0], move[1], player)
            score = self._minmax(board, self.strategy.max_depth - 1, alpha, beta, False, player)
            board.remove_piece(move[0], move[1])
            
            if score > best_score:
                best_score = score
                best_move = move
            
            alpha = max(alpha, best_score)
        
        logger.info(f"Search completed, evaluated {self.nodes_evaluated} nodes / 搜索完成，评估了{self.nodes_evaluated}个节点")
        return best_move if best_move else valid_moves[0]
    
    def _minmax(self, board: Board, depth: int, alpha: float, beta: float, 
                maximizing: bool, player: int) -> float:
        """MinMax algorithm with alpha-beta pruning.
        
        带有Alpha-Beta剪枝的极小化极大算法。
        
        Args:
            board (Board): Current board state.
                         当前棋盘状态。
            depth (int): Current search depth.
                       当前搜索深度。
            alpha (float): Alpha value for pruning.
                         用于剪枝的alpha值。
            beta (float): Beta value for pruning.
                        用于剪枝的beta值。
            maximizing (bool): Whether this is a maximizing node.
                             是否为最大化节点。
            player (int): Original player.
                        原始玩家。
                        
        Returns:
            float: Position score.
                  局势分数。
        """
        self.nodes_evaluated += 1
        
        if depth == 0 or board.is_game_over() or self._is_time_up():
            return self.evaluation.evaluate_position(board, player)
        
        current_player = player if maximizing else 3 - player
        valid_moves = self._get_valid_moves(board)
        
        if maximizing:
            value = float('-inf')
            for move in valid_moves:
                board.place_piece(move[0], move[1], current_player)
                value = max(value, self._minmax(board, depth - 1, alpha, beta, False, player))
                board.remove_piece(move[0], move[1])
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = float('inf')
            for move in valid_moves:
                board.place_piece(move[0], move[1], current_player)
                value = min(value, self._minmax(board, depth - 1, alpha, beta, True, player))
                board.remove_piece(move[0], move[1])
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value
    
    def _get_valid_moves(self, board: Board) -> List[Tuple[int, int]]:
        """Get all valid moves on the board.
        
        获取棋盘上所有有效的移动。
        
        Args:
            board (Board): Current board state.
                         当前棋盘状态。
                         
        Returns:
            List[Tuple[int, int]]: List of valid move coordinates.
                                  有效移动坐标列表。
        """
        moves = []
        for x in range(board.size):
            for y in range(board.size):
                if board.is_valid_move(x, y):
                    moves.append((x, y))
        return moves
    
    def _is_time_up(self) -> bool:
        """Check if search time limit is reached.
        
        检查是否达到搜索时间限制。
        
        Returns:
            bool: True if time limit is reached, False otherwise.
                 如果达到时间限制则为True，否则为False。
        """
        return time.time() - self.start_time >= self.strategy.time_limit