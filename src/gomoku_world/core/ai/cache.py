"""AI cache module for Gomoku.

五子棋AI缓存模块。

此模块负责管理AI的缓存系统：
- 局面缓存
- 评估结果缓存
- 最佳移动缓存
- 缓存清理策略
"""

from typing import Dict, Tuple, Optional
from ..board import Board
from ...utils.logger import get_logger

logger = get_logger(__name__)

class AICache:
    """AI cache management class.
    
    AI缓存管理类。
    
    负责：
    - 局面状态缓存
    - 评估结果缓存
    - 最佳移动缓存
    - 缓存清理
    """
    
    def __init__(self, max_size: int = 100000):
        """Initialize AI cache.
        
        初始化AI缓存。
        
        Args:
            max_size (int): Maximum number of cached positions.
                           最大缓存局面数量。
        """
        self.max_size = max_size
        self.position_cache: Dict[str, float] = {}
        self.best_move_cache: Dict[str, Tuple[int, int]] = {}
        logger.info(f"AI cache initialized with max size {max_size} / AI缓存已初始化，最大容量为{max_size}")
    
    def get_position_score(self, board: Board, player: int) -> Optional[float]:
        """Get cached position score.
        
        获取缓存的局面分数。
        
        Args:
            board (Board): Current board state.
                         当前棋盘状态。
            player (int): Current player.
                        当前玩家。
                        
        Returns:
            Optional[float]: Cached score if exists, None otherwise.
                           如果存在则返回缓存的分数，否则返回None。
        """
        key = self._get_position_key(board, player)
        return self.position_cache.get(key)
    
    def set_position_score(self, board: Board, player: int, score: float):
        """Cache position score.
        
        缓存局面分数。
        
        Args:
            board (Board): Current board state.
                         当前棋盘状态。
            player (int): Current player.
                        当前玩家。
            score (float): Position score.
                         局面分数。
        """
        if len(self.position_cache) >= self.max_size:
            self._clear_oldest_entries()
            
        key = self._get_position_key(board, player)
        self.position_cache[key] = score
    
    def get_best_move(self, board: Board, player: int) -> Optional[Tuple[int, int]]:
        """Get cached best move.
        
        获取缓存的最佳移动。
        
        Args:
            board (Board): Current board state.
                         当前棋盘状态。
            player (int): Current player.
                        当前玩家。
                        
        Returns:
            Optional[Tuple[int, int]]: Cached best move if exists, None otherwise.
                                      如果存在则返回缓存的最佳移动，否则返回None。
        """
        key = self._get_position_key(board, player)
        return self.best_move_cache.get(key)
    
    def set_best_move(self, board: Board, player: int, move: Tuple[int, int]):
        """Cache best move.
        
        缓存最佳移动。
        
        Args:
            board (Board): Current board state.
                         当前棋盘状态。
            player (int): Current player.
                        当前玩家。
            move (Tuple[int, int]): Best move coordinates.
                                   最佳移动坐标。
        """
        if len(self.best_move_cache) >= self.max_size:
            self._clear_oldest_entries()
            
        key = self._get_position_key(board, player)
        self.best_move_cache[key] = move
    
    def _get_position_key(self, board: Board, player: int) -> str:
        """Generate unique key for board position.
        
        为棋盘局面生成唯一键值。
        
        Args:
            board (Board): Current board state.
                         当前棋盘状态。
            player (int): Current player.
                        当前玩家。
                        
        Returns:
            str: Unique position key.
                 唯一的局面键值。
        """
        # 使用棋盘状态和当前玩家生成唯一键值
        board_str = ''.join(str(cell) for row in board.board for cell in row)
        return f"{board_str}_{player}"
    
    def _clear_oldest_entries(self):
        """Clear oldest cache entries when cache is full.
        
        当缓存满时清除最旧的缓存条目。
        """
        # 移除一半的缓存条目
        num_to_remove = len(self.position_cache) // 2
        
        # 清理局面分数缓存
        position_items = list(self.position_cache.items())
        self.position_cache = dict(position_items[num_to_remove:])
        
        # 清理最佳移动缓存
        best_move_items = list(self.best_move_cache.items())
        self.best_move_cache = dict(best_move_items[num_to_remove:])
        
        logger.debug(f"Cleared {num_to_remove} cache entries / 清除了{num_to_remove}个缓存条目")
    
    def clear(self):
        """Clear all cache.
        
        清除所有缓存。
        """
        self.position_cache.clear()
        self.best_move_cache.clear()
        logger.info("Cache cleared / 缓存已清除")