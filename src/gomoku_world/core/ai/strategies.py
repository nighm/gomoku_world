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
        浣跨敤MinMax绠楁硶鑾峰彇鏈€浣崇Щ鍔?
        
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
            score = self._min_max(
                board,
                depth - 1,
                alpha,
                beta,
                False,
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
        return best_move
    
    def _min_max(self, board: Board, depth: int, alpha: float, beta: float,
                 maximizing: bool, player: int) -> float:
        """
        MinMax algorithm with alpha-beta pruning
        鍏锋湁alpha-beta鍓灊鐨凪inMax绠楁硶
        
        Args:
            board: Current game board
            depth: Remaining depth
            alpha: Alpha value
            beta: Beta value
            maximizing: Whether maximizing or minimizing
            player: Original player
            
        Returns:
            float: Position score
        """
        # Terminal conditions
        if depth == 0 or board.is_game_over():
            return self.evaluator.evaluate(board, player)
        
        current_player = player if maximizing else 3 - player
        
        if maximizing:
            max_eval = float('-inf')
            for move in board.get_empty_cells():
                board.place_piece(move[0], move[1], current_player)
                eval = self._min_max(board, depth - 1, alpha, beta, False, player)
                board.clear_cell(move[0], move[1])
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.get_empty_cells():
                board.place_piece(move[0], move[1], current_player)
                eval = self._min_max(board, depth - 1, alpha, beta, True, player)
                board.clear_cell(move[0], move[1])
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval


class MCTSNode:
    """
    Monte Carlo Tree Search node
    钂欑壒鍗℃礇鏍戞悳绱㈣妭鐐?
    """
    
    def __init__(self, board: Board, parent: Optional['MCTSNode'] = None,
                 move: Optional[Tuple[int, int]] = None, player: int = 1):
        """
        Initialize MCTS node
        鍒濆鍖朚CTS鑺傜偣
        
        Args:
            board: Game board
            parent: Parent node
            move: Move that led to this node
            player: Player who made the move
        """
        self.board = board
        self.parent = parent
        self.move = move
        self.player = player
        self.children: List[MCTSNode] = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = board.get_empty_cells()
        
    def uct_value(self, c: float = 1.41) -> float:
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
        return (self.wins / self.visits + 
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
            parent=self,
            move=move,
            player=3 - self.player
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
        self.wins += result


class MCTSStrategy:
    """
    Monte Carlo Tree Search strategy
    钂欑壒鍗℃礇鏍戞悳绱㈢瓥鐣?
    """
    
    def __init__(self, simulation_time: float = 1.0):
        """
        Initialize MCTS strategy
        鍒濆鍖朚CTS绛栫暐
        
        Args:
            simulation_time: Time limit for simulations in seconds
        """
        self.simulation_time = simulation_time
        logger.info("MCTS strategy initialized")
    
    def get_move(self, board: Board, player: int) -> Tuple[int, int]:
        """
        Get best move using MCTS
        浣跨敤MCTS鑾峰彇鏈€浣崇Щ鍔?
        
        Args:
            board: Current game board
            player: Current player
            
        Returns:
            Tuple[int, int]: Best move coordinates
        """
        root = MCTSNode(board=board, player=player)
        
        # Run simulations
        end_time = time.time() + self.simulation_time
        while time.time() < end_time:
            node = self._select(root)
            if not node.board.is_game_over() and node.untried_moves:
                node = self._expand(node)
            result = self._simulate(node)
            self._backpropagate(node, result)
        
        # Select best child
        best_child = max(root.children, key=lambda c: c.visits)
        logger.debug(f"MCTS selected move {best_child.move}")
        return best_child.move
    
    def _select(self, node: MCTSNode) -> MCTSNode:
        """
        Select promising node to explore
        閫夋嫨鏈夊笇鏈涚殑鑺傜偣杩涜鎺㈢储
        
        Args:
            node: Starting node
            
        Returns:
            MCTSNode: Selected node
        """
        while node.children and not node.untried_moves:
            node = max(node.children, key=lambda n: n.uct_value())
        return node
    
    def _expand(self, node: MCTSNode) -> MCTSNode:
        """
        Expand node by adding a child
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
    
    def _simulate(self, node: MCTSNode) -> float:
        """
        Run simulation from node
        浠庤妭鐐硅繍琛屾ā鎷?
        
        Args:
            node: Starting node
            
        Returns:
            float: Simulation result
        """
        board = node.board.copy()
        current_player = node.player
        
        while not board.is_game_over():
            valid_moves = board.get_empty_cells()
            if not valid_moves:
                break
            move = random.choice(valid_moves)
            board.place_piece(move[0], move[1], current_player)
            current_player = 3 - current_player
        
        if board.is_winner(node.player):
            return 1.0
        elif board.is_winner(3 - node.player):
            return 0.0
        else:
            return 0.5
    
    def _backpropagate(self, node: MCTSNode, result: float):
        """
        Backpropagate simulation result
        鍙嶅悜浼犳挱妯℃嫙缁撴灉
        
        Args:
            node: Starting node
            result: Simulation result
        """
        while node:
            node.update(result)
            node = node.parent
            if node:
                result = 1 - result 
