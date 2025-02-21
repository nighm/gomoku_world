"""
AI strategy implementations
AI绛栫暐瀹炵幇
"""

import math
import random
import time
from typing import Tuple, List, Optional, Dict
from ..board import Board
from .evaluation import PositionEvaluator
from ...utils.logger import get_logger
import numpy as np

logger = get_logger(__name__)

class MinMaxStrategy:
    """
    MinMax strategy with alpha-beta pruning
    鍏锋湁alpha-beta鍓灊鐨凪inMax绛栫暐
    """
    
    def __init__(self):
        """Initialize MinMax strategy"""
        self.evaluator = PositionEvaluator()
        logger.info("MinMax strategy initialized")
    
    def get_move(self, board: Board, player: int, depth: int) -> Tuple[int, int]:
        """
        Get best move using MinMax algorithm
        浣跨敤MinMax绠楁硶鑾峰彇鏈浣崇Щ鍔?
        
        Args:
            board: Current game board
            player: Current player
            depth: Search depth
            
        Returns:
            Tuple[int, int]: Best move coordinates
        """
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        
        # Get all valid moves
        valid_moves = board.get_empty_cells()
        
        # Randomize move order for variety
        random.shuffle(valid_moves)
        
        for move in valid_moves:
            # Try move
            board.place_piece(move[0], move[1], player)
            
            # Get score from MinMax
            score = self._min_value(
                board,
                depth - 1,
                alpha,
                beta,
                player
            )
            
            # Undo move
            board.clear_cell(move[0], move[1])
            
            # Update best
            if score > best_score:
                best_score = score
                best_move = move
            
            # Update alpha
            alpha = max(alpha, best_score)
            
            # Alpha-beta pruning
            if beta <= alpha:
                break
        
        logger.debug(f"MinMax selected move {best_move} with score {best_score}")
        return best_move if best_move else valid_moves[0]
    
    def _min_value(self, board: Board, depth: int, 
                   alpha: float, beta: float, player: int) -> float:
        """
        Get minimum value for MinMax
        
        Args:
            board: Current game board
            depth: Remaining depth
            alpha: Alpha value
            beta: Beta value
            player: Original player
            
        Returns:
            float: Minimum value
        """
        if depth == 0:
            return self.evaluator.evaluate(board.board, player)
            
        value = float('inf')
        opponent = 3 - player  # Switch player
        
        for move in board.get_empty_cells():
            # Try move
            board.place_piece(move[0], move[1], opponent)
            
            # Get score from MaxValue
            value = min(
                value,
                self._max_value(board, depth - 1, alpha, beta, player)
            )
            
            # Undo move
            board.clear_cell(move[0], move[1])
            
            # Update beta
            beta = min(beta, value)
            
            # Alpha-beta pruning
            if beta <= alpha:
                break
                
        return value
    
    def _max_value(self, board: Board, depth: int,
                   alpha: float, beta: float, player: int) -> float:
        """
        Get maximum value for MinMax
        
        Args:
            board: Current game board
            depth: Remaining depth
            alpha: Alpha value
            beta: Beta value
            player: Original player
            
        Returns:
            float: Maximum value
        """
        if depth == 0:
            return self.evaluator.evaluate(board.board, player)
            
        value = float('-inf')
        
        for move in board.get_empty_cells():
            # Try move
            board.place_piece(move[0], move[1], player)
            
            # Get score from MinValue
            value = max(
                value,
                self._min_value(board, depth - 1, alpha, beta, player)
            )
            
            # Undo move
            board.clear_cell(move[0], move[1])
            
            # Update alpha
            alpha = max(alpha, value)
            
            # Alpha-beta pruning
            if beta <= alpha:
                break
                
        return value


class MCTSNode:
    """
    Monte Carlo Tree Search node
    钂欑壒鍗℃礇鏍戞悳绱㈣妭鐐?
    """
    
    def __init__(self, board: Board, player: int,
                 parent: Optional['MCTSNode'] = None,
                 move: Optional[Tuple[int, int]] = None):
        """
        Initialize MCTS node
        鍒濆鍖朚CTS鑺傜偣
        
        Args:
            board: Game board
            player: Player who made the move
            parent: Parent node
            move: Move that led to this node
        """
        self.board = board
        self.player = player
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.value = 0.0
        self.untried_moves = board.get_empty_cells()
        
    def is_terminal(self) -> bool:
        """
        Check if node is terminal
        
        Returns:
            bool: True if terminal
        """
        return self.board.is_full()
    
    def uct_value(self, c: float = math.sqrt(2)) -> float:
        """
        Calculate UCT value for node selection
        璁＄畻鑺傜偣閫夋嫨鐨刄CT鍊?
        
        Args:
            c: Exploration parameter
            
        Returns:
            float: UCT value
        """
        if self.visits == 0:
            return float('inf')
        return (self.value / self.visits + 
                c * math.sqrt(math.log(self.parent.visits) / self.visits))
    
    def add_child(self, move: Tuple[int, int], board: Board) -> 'MCTSNode':
        """
        Add child node
        娣诲姞瀛愯妭鐐?
        
        Args:
            move: Move to create child from
            board: Board state for child
            
        Returns:
            MCTSNode: New child node
        """
        child = MCTSNode(
            board=board,
            player=3 - self.player,
            parent=self,
            move=move
        )
        self.untried_moves.remove(move)
        self.children.append(child)
        return child
    
    def update(self, result: float):
        """
        Update node statistics
        鏇存柊鑺傜偣缁熻淇℃伅
        
        Args:
            result: Game result (1 for win, 0 for loss)
        """
        self.visits += 1
        self.value += result


class MCTSStrategy:
    """
    Monte Carlo Tree Search strategy
    钂欑壒鍗℃礇鏍戞悳绱㈢瓥鐣?
    """
    
    def __init__(self, simulation_limit: int = 1000):
        """
        Initialize MCTS strategy
        鍒濆鍖朚CTS绛栫暐
        
        Args:
            simulation_limit: Maximum number of simulations
        """
        self.simulation_limit = simulation_limit
        self.evaluator = PositionEvaluator()
        logger.info("MCTS strategy initialized")
    
    def get_move(self, board: Board, player: int) -> Tuple[int, int]:
        """
        Get best move using MCTS
        浣跨敤MCTS鑾峰彇鏈浣崇Щ鍔?
        
        Args:
            board: Current game board
            player: Current player
            
        Returns:
            Tuple[int, int]: Best move coordinates
        """
        root = MCTSNode(board=board, player=player)
        
        # Run simulations
        for _ in range(self.simulation_limit):
            # Selection
            node = self._select(root)
            
            # Expansion
            if not node.is_terminal() and node.untried_moves:
                node = self._expand(node)
            
            # Simulation
            result = self._simulate(node)
            
            # Backpropagation
            self._backpropagate(node, result)
        
        # Get best move
        best_child = max(
            root.children,
            key=lambda c: c.visits
        )
        
        logger.debug(f"MCTS selected move {best_child.move}")
        return best_child.move
    
    def _select(self, node: 'MCTSNode') -> 'MCTSNode':
        """
        Select a node for expansion
        閫夋嫨鏈夊笇鏈涚殑鑺傜偣杩涜鎺㈢储
        
        Args:
            node: Current node
            
        Returns:
            MCTSNode: Selected node
        """
        while node.children and not node.untried_moves:
            node = max(
                node.children,
                key=lambda c: c.uct_value()
            )
        return node
    
    def _expand(self, node: 'MCTSNode') -> 'MCTSNode':
        """
        Expand a node
        閫氳繃娣诲姞瀛愯妭鐐规潵鎵╁睍鑺傜偣
        
        Args:
            node: Node to expand
            
        Returns:
            MCTSNode: New child node
        """
        move = random.choice(node.untried_moves)
        new_board = node.board.copy()
        new_board.place_piece(move[0], move[1], node.player)
        return node.add_child(move, new_board)
    
    def _simulate(self, node: 'MCTSNode') -> float:
        """
        Run a simulation from a node
        浠庤妭鐐硅繍琛屾ā鎷?
        
        Args:
            node: Starting node
            
        Returns:
            float: Simulation result
        """
        board = node.board.copy()
        current_player = node.player
        
        while not board.is_full():
            valid_moves = board.get_empty_cells()
            if not valid_moves:
                break
            move = random.choice(valid_moves)
            board.place_piece(move[0], move[1], current_player)
            current_player = 3 - current_player
        
        return self.evaluator.evaluate(board.board, node.player)
    
    def _backpropagate(self, node: 'MCTSNode', result: float):
        """
        Backpropagate simulation result
        鍙嶅悜浼犳挱妯℃嫙缁撴灉
        
        Args:
            node: Starting node
            result: Simulation result
        """
        while node:
            node.visits += 1
            node.value += result
            node = node.parent
            if node:
                result = 1 - result 
