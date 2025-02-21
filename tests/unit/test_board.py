"""
Board class unit tests
棋盘类单元测试
"""

import pytest
from gomoku_world.core import Board

def test_board_initialization(board_15x15):
    """Test board initialization"""
    assert board_15x15.size == 15
    assert len(board_15x15.board) == 15
    assert len(board_15x15.board[0]) == 15
    assert board_15x15.get_piece(7, 7) == 0  # Center should be empty

def test_place_piece(board_15x15):
    """Test piece placement"""
    # Place a black piece
    assert board_15x15.place_piece(7, 7, 1) == True
    assert board_15x15.get_piece(7, 7) == 1
    
    # Place a white piece
    assert board_15x15.place_piece(8, 8, 2) == True
    assert board_15x15.get_piece(8, 8) == 2
    
    # Try to place a piece on an occupied position
    assert board_15x15.place_piece(7, 7, 2) == False
    assert board_15x15.get_piece(7, 7) == 1  # Should remain black

def test_invalid_coordinates(board_15x15):
    """Test handling of invalid coordinates"""
    # Test negative coordinates
    with pytest.raises(ValueError):
        board_15x15.place_piece(-1, 0, 1)
    
    # Test out of bounds coordinates
    with pytest.raises(ValueError):
        board_15x15.place_piece(15, 0, 1)
    with pytest.raises(ValueError):
        board_15x15.place_piece(0, 15, 1)

def test_clear_board(board_with_pieces):
    """Test board clearing"""
    board_with_pieces.clear()
    for i in range(15):
        for j in range(15):
            assert board_with_pieces.get_piece(i, j) == 0

def test_board_full(board_15x15):
    """Test board full detection"""
    # Fill the board
    for i in range(15):
        for j in range(15):
            board_15x15.place_piece(i, j, 1 if (i + j) % 2 == 0 else 2)
    
    # Try to place a piece when board is full
    assert board_15x15.place_piece(7, 7, 1) == False 