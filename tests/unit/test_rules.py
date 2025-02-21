"""
Rules class unit tests
规则类单元测试
"""

import pytest
from gomoku_world.core import Rules

def test_horizontal_win(board_15x15):
    """Test horizontal winning condition"""
    # Create a horizontal line
    for i in range(5):
        board_15x15.place_piece(7, i, 1)
    
    assert Rules.check_win(board_15x15, 7, 4) == True
    assert Rules.check_win(board_15x15, 7, 0) == True

def test_vertical_win(board_15x15):
    """Test vertical winning condition"""
    # Create a vertical line
    for i in range(5):
        board_15x15.place_piece(i, 7, 1)
    
    assert Rules.check_win(board_15x15, 4, 7) == True
    assert Rules.check_win(board_15x15, 0, 7) == True

def test_diagonal_win(board_15x15):
    """Test diagonal winning condition"""
    # Create a diagonal line
    for i in range(5):
        board_15x15.place_piece(i, i, 1)
    
    assert Rules.check_win(board_15x15, 4, 4) == True
    assert Rules.check_win(board_15x15, 0, 0) == True

def test_no_win(board_with_pieces):
    """Test non-winning positions"""
    # Test with 4 pieces in a row
    assert Rules.check_win(board_with_pieces, 7, 0) == False
    assert Rules.check_win(board_with_pieces, 7, 3) == False

def test_valid_moves(board_with_pieces):
    """Test valid moves detection"""
    moves = Rules.get_valid_moves(board_with_pieces)
    # Should be total positions minus placed pieces
    assert len(moves) == 15 * 15 - 5  # 5 pieces are placed in board_with_pieces

def test_draw_detection(board_15x15):
    """Test draw condition detection"""
    # Fill the board
    for i in range(15):
        for j in range(15):
            board_15x15.place_piece(i, j, 1 if (i + j) % 2 == 0 else 2)
    
    assert Rules.is_draw(board_15x15) == True

def test_not_draw(board_with_pieces):
    """Test non-draw condition"""
    assert Rules.is_draw(board_with_pieces) == False 