"""
PyTest configuration file
娴嬭瘯閰嶇疆鏂囦欢
"""

import pytest

@pytest.fixture
def board_15x15():
    """Create a 15x15 empty board"""
    from gomoku_world.core import Board
    return Board(size=15)

@pytest.fixture
def board_with_pieces():
    """Create a board with some pieces"""
    from gomoku_world.core import Board
    board = Board(size=15)
    # Add some pieces in a row
    for i in range(4):
        board.place_piece(7, i, 1)  # Black pieces
    board.place_piece(7, 4, 2)      # White piece
    return board

@pytest.fixture
def winning_board():
    """Create a board with a winning position"""
    from gomoku_world.core import Board
    board = Board(size=15)
    # Create a winning line for black (player 1)
    for i in range(5):
        board.place_piece(7, i, 1)
    return board 
