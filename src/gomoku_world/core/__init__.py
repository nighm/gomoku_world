"""Core module for Gomoku.

五子棋核心模块。
"""

from .board import Game, InvalidMoveError, Position, Board
from .rules import Rules
from .ai.strategy import AIStrategy as AI

__all__ = [
    'Game',
    'InvalidMoveError',
    'Position',
    'Board',
    'Rules',
    'AI'
]
