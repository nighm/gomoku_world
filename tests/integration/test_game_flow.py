"""
Game flow integration tests
娓告垙娴佺▼闆嗘垚娴嬭瘯
"""

import pytest
from gomoku_world.core import Board, Rules, AI

def test_game_win_flow():
    """Test complete game flow ending in a win"""
    # Initialize game components
    board = Board(size=15)
    ai = AI()
    
    # Simulate a game where black wins with a horizontal line
    moves = [(7, i) for i in range(5)]  # Winning moves for black
    ai_moves = [(8, i) for i in range(4)]  # AI (white) moves
    
    # Play alternating moves
    for i in range(4):
        # Black's move
        row, col = moves[i]
        assert board.place_piece(row, col, 1) == True
        assert Rules.check_win(board, row, col) == False
        
        # White's move
        row, col = ai_moves[i]
        assert board.place_piece(row, col, 2) == True
        assert Rules.check_win(board, row, col) == False
    
    # Final winning move for black
    row, col = moves[4]
    assert board.place_piece(row, col, 1) == True
    assert Rules.check_win(board, row, col) == True

def test_game_draw_flow():
    """Test complete game flow ending in a draw"""
    board = Board(size=15)
    
    # Fill the board in a way that prevents any wins
    for i in range(15):
        for j in range(15):
            player = 1 if (i + j) % 2 == 0 else 2
            assert board.place_piece(i, j, player) == True
    
    assert Rules.is_draw(board) == True
    
    # Verify no winning condition exists
    for i in range(15):
        for j in range(15):
            assert Rules.check_win(board, i, j) == False

def test_ai_defense():
    """Test AI defensive moves"""
    board = Board(size=15)
    ai = AI()
    
    # Create a threat (4 in a row)
    for i in range(4):
        board.place_piece(7, i, 1)  # Black pieces
    
    # AI should block the winning move
    ai_move = ai.get_move(board, 2)  # AI plays as white
    assert ai_move == (7, 4)  # Should block at (7, 4)
    
    # Make the blocking move
    board.place_piece(7, 4, 2)
    assert Rules.check_win(board, 7, 0) == False 
