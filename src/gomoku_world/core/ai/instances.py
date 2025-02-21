"""
Global instances for AI
AI全局实例
"""

from .engine import AI
from .strategies import MinMaxStrategy, MCTSStrategy
from .evaluation import PositionEvaluator

# Create global instances
ai_engine = AI()
minmax_strategy = MinMaxStrategy()
mcts_strategy = MCTSStrategy()
evaluator = PositionEvaluator()

__all__ = [
    'ai_engine',
    'minmax_strategy',
    'mcts_strategy',
    'evaluator'
] 