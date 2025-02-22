"""
Core game logic module.

核心游戏逻辑模块。

This module implements the main game logic for Gomoku, including:
- Game state management
- Move handling
- Player turn management
- Game mode control
- AI integration

本模块实现五子棋的主要游戏逻辑，包括：
- 游戏状态管理
- 移动处理
- 玩家回合管理
- 游戏模式控制
- AI集成
"""

from typing import Optional, Tuple, List
from dataclasses import dataclass

# 浣跨敤鐩稿瀵煎叆
from .board import Board
from .rules import Rules
from .ai import AI
from ..utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class Move:
    """
    Represents a game move.
    
    表示一个游戏移动。
    
    Attributes:
        row (int): Row index of the move.
                  移动的行索引。
        col (int): Column index of the move.
                  移动的列索引。
        player (int): Player number (1 for black, 2 for white).
                     玩家编号（1为黑棋，2为白棋）。
    """
    row: int
    col: int
    player: int

class Game:
    """
    Main game logic class.
    
    主游戏逻辑类。
    
    This class manages:
    - Game state and board
    - Player moves and turns
    - Game rules enforcement
    - AI opponent (in PvC mode)
    - Game history
    
    此类管理：
    - 游戏状态和棋盘
    - 玩家移动和回合
    - 游戏规则执行
    - AI对手（在PvC模式中）
    - 游戏历史
    """
    
    def __init__(self, board_size: int = 15, game_mode: str = "pvp"):
        """
        Initialize game instance.
        
        初始化游戏实例。
        
        Args:
            board_size (int): Size of the game board (default: 15).
                            游戏棋盘的大小（默认：15）。
            game_mode (str): Game mode (pvp/pvc) (default: pvp).
                           游戏模式（pvp/pvc）（默认：pvp）。
                           pvp: Player vs Player / 玩家对玩家
                           pvc: Player vs Computer / 玩家对电脑
        """
        self.board = Board(board_size)
        self.current_player = 1  # 1 for black, 2 for white / 1为黑棋，2为白棋
        self.moves: List[Move] = []
        self.game_over = False
        self.winner = None
        self.game_mode = game_mode
        self.ai = AI() if game_mode == "pvc" else None
        
        logger.info(f"Game initialized with {board_size}x{board_size} board, mode: {game_mode}")
    
    def make_move(self, row: int, col: int) -> bool:
        """
        Make a move on the board.
        
        在棋盘上进行移动。
        
        Args:
            row (int): Row index of the move.
                      移动的行索引。
            col (int): Column index of the move.
                      移动的列索引。
                      
        Returns:
            bool: True if the move was successful, False otherwise.
                 如果移动成功则为True，否则为False。
        """
        if self.game_over:
            logger.warning("Game is already over / 游戏已经结束")
            return False
            
        if not Rules.is_valid_move(self.board, row, col):
            logger.warning(f"Invalid move at ({row}, {col}) / 在({row}, {col})的移动无效")
            return False
        
        # Make the move / 进行移动
        self.board.place_piece(row, col, self.current_player)
        self.moves.append(Move(row, col, self.current_player))
        
        # Check for win / 检查是否胜利
        if Rules.check_win(self.board, row, col):
            self.game_over = True
            self.winner = self.current_player
            logger.info(f"Player {self.current_player} wins! / 玩家{self.current_player}获胜！")
            return True
            
        # Check for draw / 检查是否平局
        if Rules.is_draw(self.board):
            self.game_over = True
            logger.info("Game is a draw / 游戏平局")
            return True
        
        # Switch players / 切换玩家
        self.current_player = 3 - self.current_player  # Toggle between 1 and 2 / 在1和2之间切换
        
        # Make AI move if in PvC mode / 如果在PvC模式下，进行AI移动
        if self.game_mode == "pvc" and not self.game_over:
            return self._make_ai_move()
        
        return True
    
    def _make_ai_move(self) -> bool:
        """
        Make an AI move.
        
        进行AI移动。
        
        Returns:
            bool: True if the AI move was successful, False otherwise.
                 如果AI移动成功则为True，否则为False。
        """
        if not self.ai:
            logger.error("AI not initialized / AI未初始化")
            return False
        
        try:
            row, col = self.ai.get_move(self.board, self.current_player)
            return self.make_move(row, col)
        except Exception as e:
            logger.error(f"AI move error / AI移动错误: {e}")
            return False
    
    def undo_move(self) -> Optional[Move]:
        """
        Undo the last move.
        
        撤销最后一步移动。
        
        Returns:
            Optional[Move]: The undone move, or None if no moves to undo.
                          被撤销的移动，如果没有可撤销的移动则为None。
        """
        if not self.moves:
            return None
        
        last_move = self.moves.pop()
        self.board.clear_cell(last_move.row, last_move.col)
        
        # Reset game state if game was over / 如果游戏已结束，重置游戏状态
        if self.game_over:
            self.game_over = False
            self.winner = None
        
        # Switch back to previous player / 切换回前一个玩家
        self.current_player = last_move.player
        
        logger.info(f"Move undone at ({last_move.row}, {last_move.col}) / 撤销了在({last_move.row}, {last_move.col})的移动")
        return last_move
    
    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """
        Get all valid moves.
        
        获取所有有效的移动。
        
        Returns:
            List[Tuple[int, int]]: List of valid move coordinates.
                                  有效移动坐标列表。
        """
        return Rules.get_valid_moves(self.board)
    
    def reset(self):
        """
        Reset the game to initial state.
        
        重置游戏到初始状态。
        """
        self.board.clear()
        self.moves.clear()
        self.current_player = 1
        self.game_over = False
        self.winner = None
        logger.info("Game reset / 游戏已重置")
    
    def set_game_mode(self, mode: str):
        """
        Set the game mode.
        
        设置游戏模式。
        
        Args:
            mode (str): Game mode ('pvp' or 'pvc').
                       游戏模式（'pvp'或'pvc'）。
        """
        if mode not in ["pvp", "pvc"]:
            raise ValueError("Invalid game mode / 无效的游戏模式")
            
        self.game_mode = mode
        self.ai = AI() if mode == "pvc" else None
        self.reset()
        logger.info(f"Game mode set to {mode} / 游戏模式设置为{mode}")
    
    def set_ai_difficulty(self, difficulty: str):
        """
        Set AI difficulty level.
        
        设置AI难度级别。
        
        Args:
            difficulty (str): Difficulty level ('easy', 'medium', or 'hard').
                            难度级别（'easy'、'medium'或'hard'）。
        """
        if not self.ai:
            raise RuntimeError("AI not initialized / AI未初始化")
            
        self.ai.set_difficulty(difficulty)
        logger.info(f"AI difficulty set to {difficulty} / AI难度设置为{difficulty}") 
