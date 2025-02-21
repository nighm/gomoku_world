"""
AI implementation for Gomoku
五子棋AI实现
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
    AI player implementation using MinMax algorithm with alpha-beta pruning
    使用带有alpha-beta剪枝的MinMax算法的AI玩家实现
    """
    
    def __init__(self, difficulty: str = "medium"):
        """
        Initialize AI player
        初始化AI玩家
        
        Args:
            difficulty: AI difficulty level (easy/medium/hard)
        """
        self.difficulty = difficulty
        self.max_depth = self._get_depth_for_difficulty()
        self.time_limit = AI_THINKING_TIME
        logger.info(f"AI initialized with {difficulty} difficulty")
    
    def _get_depth_for_difficulty(self) -> int:
        """Get search depth based on difficulty"""
        return {
            "easy": 2,
            "medium": 3,
            "hard": 4
        }.get(self.difficulty, 3)
    
    def get_move(self, board: Board, player: int) -> Tuple[int, int]:
        """
        Get the best move for the current position
        获取当前位置的最佳移动
        
        Args:
            board: Current board state
            player: Current player (1 or 2)
            
        Returns:
            Tuple[int, int]: Best move coordinates
        """
        start_time = time.time()
        logger.info("AI is thinking...")
        
        # For easy difficulty, occasionally make random moves
        if self.difficulty == "easy" and random.random() < 0.3:
            move = self._get_random_move(board)
            logger.info(f"AI chose random move: {move}")
            return move
        
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        
        # Get all valid moves, prioritize center area
        valid_moves = self._get_prioritized_moves(board)
        
        for move in valid_moves:
            if time.time() - start_time > self.time_limit:
                logger.warning("AI thinking time exceeded")
                break
                
            # Try move
            board.place_piece(move[0], move[1], player)
            score = self._minmax(board, self.max_depth, False, player, alpha, beta)
            board.clear_cell(move[0], move[1])
            
            if score > best_score:
                best_score = score
                best_move = move
            
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        
        if best_move is None:
            best_move = self._get_random_move(board)
            logger.warning("No best move found, using random move")
        
        logger.info(f"AI chose move {best_move} with score {best_score}")
        return best_move
    
    def _minmax(self, board: Board, depth: int, is_maximizing: bool, 
                player: int, alpha: float, beta: float) -> float:
        """MinMax algorithm with alpha-beta pruning"""
        if depth == 0 or self._is_terminal(board):
            return self._evaluate_position(board, player)
        
        valid_moves = self._get_prioritized_moves(board)
        
        if is_maximizing:
            max_eval = float('-inf')
            for move in valid_moves:
                board.place_piece(move[0], move[1], player)
                eval = self._minmax(board, depth - 1, False, player, alpha, beta)
                board.clear_cell(move[0], move[1])
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            opponent = 3 - player
            for move in valid_moves:
                board.place_piece(move[0], move[1], opponent)
                eval = self._minmax(board, depth - 1, True, player, alpha, beta)
                board.clear_cell(move[0], move[1])
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
    
    def _evaluate_position(self, board: Board, player: int) -> float:
        """Evaluate board position for the given player"""
        score = 0
        opponent = 3 - player
        
        # Check all directions
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board.get_piece(i, j) == 0:
                    continue
                    
                for dx, dy in directions:
                    # Count consecutive pieces
                    count_player = self._count_consecutive(board, i, j, dx, dy, player)
                    count_opponent = self._count_consecutive(board, i, j, dx, dy, opponent)
                    
                    # Score based on consecutive pieces
                    score += self._score_sequence(count_player, player)
                    score -= self._score_sequence(count_opponent, opponent)
        
        return score
    
    def _count_consecutive(self, board: Board, row: int, col: int, 
                         dx: int, dy: int, player: int) -> int:
        """Count consecutive pieces in a direction"""
        count = 0
        x, y = row, col
        
        while (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and 
               board.get_piece(x, y) == player):
            count += 1
            x += dx
            y += dy
        
        return count
    
    def _score_sequence(self, count: int, player: int) -> float:
        """Score a sequence of pieces"""
        if count >= 5:
            return 1000000  # Win
        elif count == 4:
            return 10000    # One move to win
        elif count == 3:
            return 1000     # Two moves to win
        elif count == 2:
            return 100      # Three moves to win
        elif count == 1:
            return 10       # Four moves to win
        return 0
    
    def _is_terminal(self, board: Board) -> bool:
        """Check if position is terminal (win/draw)"""
        # Check for win
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board.get_piece(i, j) != 0:
                    if self._check_win(board, i, j):
                        return True
        
        # Check for draw
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
        """Get valid moves, prioritizing center and areas near existing pieces"""
        empty_cells = board.get_empty_cells()
        if not empty_cells:
            return []
        
        # If board is empty, prioritize center area
        if len(empty_cells) == BOARD_SIZE * BOARD_SIZE:
            center = BOARD_SIZE // 2
            return [(center, center)]
        
        # Score each empty cell based on proximity to existing pieces
        scored_moves = []
        for row, col in empty_cells:
            score = self._score_move_position(board, row, col)
            scored_moves.append((score, (row, col)))
        
        # Sort by score in descending order
        scored_moves.sort(reverse=True)
        return [move for _, move in scored_moves]
    
    def _score_move_position(self, board: Board, row: int, col: int) -> float:
        """Score a potential move position based on surrounding pieces"""
        score = 0
        for i in range(max(0, row - 2), min(BOARD_SIZE, row + 3)):
            for j in range(max(0, col - 2), min(BOARD_SIZE, col + 3)):
                if board.get_piece(i, j) != 0:
                    distance = abs(row - i) + abs(col - j)
                    score += 1.0 / (distance + 1)
        return score
    
    def _get_random_move(self, board: Board) -> Tuple[int, int]:
        """Get a random valid move"""
        empty_cells = board.get_empty_cells()
        return random.choice(empty_cells) if empty_cells else (BOARD_SIZE // 2, BOARD_SIZE // 2) 