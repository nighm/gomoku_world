"""
Core game logic
鏍稿績娓告垙閫昏緫
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
    Represents a game move
    琛ㄧず涓涓父鎴忕Щ鍔?
    """
    row: int
    col: int
    player: int

class Game:
    """
    Main game logic class
    涓绘父鎴忛昏緫绫?
    """
    
    def __init__(self, board_size: int = 15, game_mode: str = "pvp"):
        """
        Initialize game
        鍒濆鍖栨父鎴?
        
        Args:
            board_size: Size of the game board (default: 15)
            game_mode: Game mode (pvp/pvc) (default: pvp)
        """
        self.board = Board(board_size)
        self.current_player = 1  # 1 for black, 2 for white
        self.moves: List[Move] = []
        self.game_over = False
        self.winner = None
        self.game_mode = game_mode
        self.ai = AI() if game_mode == "pvc" else None
        
        logger.info(f"Game initialized with {board_size}x{board_size} board, mode: {game_mode}")
    
    def make_move(self, row: int, col: int) -> bool:
        """
        Make a move on the board
        鍦ㄦ鐩樹笂钀藉瓙
        
        Args:
            row: Row number
            col: Column number
        
        Returns:
            bool: True if move was successful
        """
        if self.game_over:
            logger.warning("Attempted move after game over")
            return False
            
        if not self.board.is_valid_move(row, col):
            logger.warning(f"Invalid move attempted at ({row}, {col})")
            return False
        
        # Make player's move
        self.board.place_piece(row, col, self.current_player)
        move = Move(row, col, self.current_player)
        self.moves.append(move)
        
        # Check game state after player's move
        if Rules.check_win(self.board, row, col):
            self.game_over = True
            self.winner = self.current_player
            logger.info(f"Player {self.current_player} wins")
            return True
        elif Rules.is_draw(self.board):
            self.game_over = True
            logger.info("Game ends in draw")
            return True
        
        # Switch player
        self.current_player = 3 - self.current_player
        
        # If playing against AI and it's AI's turn
        if self.game_mode == "pvc" and self.current_player == 2 and not self.game_over:
            return self._make_ai_move()
        
        return True
    
    def _make_ai_move(self) -> bool:
        """
        Make AI move
        鎵цAI绉诲姩
        
        Returns:
            bool: True if move was successful
        """
        if not self.ai:
            logger.error("AI not initialized")
            return False
        
        # Get AI's move
        ai_row, ai_col = self.ai.get_move(self.board, self.current_player)
        
        # Make AI's move
        self.board.place_piece(ai_row, ai_col, self.current_player)
        move = Move(ai_row, ai_col, self.current_player)
        self.moves.append(move)
        
        # Check game state after AI's move
        if Rules.check_win(self.board, ai_row, ai_col):
            self.game_over = True
            self.winner = self.current_player
            logger.info(f"AI wins")
            return True
        elif Rules.is_draw(self.board):
            self.game_over = True
            logger.info("Game ends in draw")
            return True
        
        # Switch back to player
        self.current_player = 3 - self.current_player
        return True
    
    def undo_move(self) -> Optional[Move]:
        """
        Undo the last move
        鎾ら攢鏈鍚庝竴姝?
        
        Returns:
            Optional[Move]: The move that was undone, or None if no moves to undo
        """
        if not self.moves:
            logger.warning("No moves to undo")
            return None
        
        # If playing against AI, undo both AI's move and player's move
        if self.game_mode == "pvc" and len(self.moves) >= 2:
            # Undo AI's move
            ai_move = self.moves.pop()
            self.board.clear_cell(ai_move.row, ai_move.col)
            # Undo player's move
            player_move = self.moves.pop()
            self.board.clear_cell(player_move.row, player_move.col)
            self.current_player = player_move.player
        else:
            # Just undo the last move
            move = self.moves.pop()
            self.board.clear_cell(move.row, move.col)
            self.current_player = move.player
        
        self.game_over = False
        self.winner = None
        logger.info("Move(s) undone")
        return move
    
    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """
        Get all valid moves
        鑾峰彇鎵鏈夋湁鏁堢殑绉诲姩
        
        Returns:
            List[Tuple[int, int]]: List of valid move coordinates
        """
        return Rules.get_valid_moves(self.board)
    
    def reset(self):
        """
        Reset the game to initial state
        閲嶇疆娓告垙鍒板垵濮嬬姸鎬?
        """
        self.board.clear()
        self.current_player = 1
        self.moves.clear()
        self.game_over = False
        self.winner = None
        logger.info("Game reset")
    
    def set_game_mode(self, mode: str):
        """
        Set game mode
        璁剧疆娓告垙妯″紡
        
        Args:
            mode: Game mode (pvp/pvc)
        """
        if mode in ["pvp", "pvc"]:
            self.game_mode = mode
            self.ai = AI() if mode == "pvc" else None
            logger.info(f"Game mode set to {mode}")
        else:
            logger.warning(f"Invalid game mode: {mode}")
    
    def set_ai_difficulty(self, difficulty: str):
        """
        Set AI difficulty
        璁剧疆AI闅惧害
        
        Args:
            difficulty: AI difficulty level
        """
        if self.ai:
            self.ai = AI(difficulty)
            logger.info(f"AI difficulty set to {difficulty}")
        else:
            logger.warning("Cannot set AI difficulty in PvP mode") 
