"""
Board evaluation implementation
灞闈㈣瘎浼板疄鐜?
""" 

from typing import List, Tuple, Dict
import numpy as np
from ...utils.logger import get_logger

logger = get_logger(__name__)

class PositionEvaluator:
    """
    Position evaluator for AI
    """
    
    def __init__(self):
        """Initialize evaluator"""
        # Pattern scores
        self.pattern_scores = {
            "five": 100000,    # Five in a row
            "four": 10000,     # Four in a row
            "three": 1000,     # Three in a row
            "two": 100,        # Two in a row
            "one": 10          # Single piece
        }
        logger.info("Position evaluator initialized")
    
    def evaluate(self, board: np.ndarray, player: int) -> float:
        """
        Evaluate board position for player
        
        Args:
            board: Game board
            player: Player to evaluate for (1 or 2)
            
        Returns:
            float: Position score
        """
        score = 0.0
        
        # Check horizontal patterns
        for row in range(board.shape[0]):
            score += self._evaluate_line(board[row, :], player)
            
        # Check vertical patterns
        for col in range(board.shape[1]):
            score += self._evaluate_line(board[:, col], player)
            
        # Check main diagonal patterns
        for diag in range(-board.shape[0]+1, board.shape[1]):
            score += self._evaluate_line(np.diagonal(board, diag), player)
            
        # Check anti-diagonal patterns
        flipped_board = np.fliplr(board)
        for diag in range(-board.shape[0]+1, board.shape[1]):
            score += self._evaluate_line(np.diagonal(flipped_board, diag), player)
            
        return score
    
    def _evaluate_line(self, line: np.ndarray, player: int) -> float:
        """
        Evaluate a line of pieces
        
        Args:
            line: Line to evaluate
            player: Player to evaluate for
            
        Returns:
            float: Line score
        """
        score = 0.0
        length = len(line)
        
        # Count consecutive pieces
        count = 0
        for i in range(length):
            if line[i] == player:
                count += 1
            else:
                if count > 0:
                    score += self._get_pattern_score(count)
                count = 0
                
        # Handle end of line
        if count > 0:
            score += self._get_pattern_score(count)
            
        return score
    
    def _get_pattern_score(self, count: int) -> float:
        """
        Get score for a pattern
        
        Args:
            count: Number of consecutive pieces
            
        Returns:
            float: Pattern score
        """
        if count >= 5:
            return self.pattern_scores["five"]
        elif count == 4:
            return self.pattern_scores["four"]
        elif count == 3:
            return self.pattern_scores["three"]
        elif count == 2:
            return self.pattern_scores["two"]
        elif count == 1:
            return self.pattern_scores["one"]
        else:
            return 0.0 