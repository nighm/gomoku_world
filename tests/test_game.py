"""
Unit tests for the game logic module.
"""

import unittest
from src.game import Game, InvalidMoveError, Position

class TestGame(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.game = Game(size=15)
    
    def test_initial_state(self):
        """Test the initial game state"""
        self.assertEqual(self.game.size, 15)
        self.assertEqual(self.game.current_player, 1)
        self.assertEqual(len(self.game.move_history), 0)
        
        # Check if board is empty
        for i in range(self.game.size):
            for j in range(self.game.size):
                self.assertEqual(self.game.board[i][j], 0)
    
    def test_invalid_board_size(self):
        """Test that invalid board sizes are rejected"""
        with self.assertRaises(ValueError):
            Game(size=4)
    
    def test_make_move(self):
        """Test making valid and invalid moves"""
        # Test valid move
        self.assertTrue(self.game.make_move(7, 7))
        self.assertEqual(self.game.board[7][7], 1)
        self.assertEqual(self.game.current_player, 2)
        
        # Test move outside board
        with self.assertRaises(InvalidMoveError):
            self.game.make_move(15, 15)
        
        # Test move on occupied position
        with self.assertRaises(InvalidMoveError):
            self.game.make_move(7, 7)
    
    def test_win_horizontal(self):
        """Test winning condition in horizontal direction"""
        # Place 5 black pieces in a row
        for col in range(5):
            self.game.make_move(7, col)  # Black's moves
            if col < 4:
                self.game.make_move(8, col)  # White's moves
        
        self.assertTrue(self.game.check_winner(7, 4))
    
    def test_win_vertical(self):
        """Test winning condition in vertical direction"""
        # Place 5 black pieces in a column
        for row in range(5):
            self.game.make_move(row, 7)  # Black's moves
            if row < 4:
                self.game.make_move(row, 8)  # White's moves
        
        self.assertTrue(self.game.check_winner(4, 7))
    
    def test_win_diagonal(self):
        """Test winning condition in diagonal direction"""
        # Place 5 black pieces in a diagonal
        for i in range(5):
            self.game.make_move(i, i)  # Black's moves
            if i < 4:
                self.game.make_move(i, i+1)  # White's moves
        
        self.assertTrue(self.game.check_winner(4, 4))
    
    def test_reset(self):
        """Test game reset functionality"""
        # Make some moves
        self.game.make_move(7, 7)
        self.game.make_move(7, 8)
        
        # Reset the game
        self.game.reset()
        
        # Check if the game state is reset
        self.assertEqual(self.game.current_player, 1)
        self.assertEqual(len(self.game.move_history), 0)
        for i in range(self.game.size):
            for j in range(self.game.size):
                self.assertEqual(self.game.board[i][j], 0)
    
    def test_valid_moves(self):
        """Test getting valid moves"""
        # Initial board should have all positions as valid moves
        valid_moves = self.game.get_valid_moves()
        self.assertEqual(len(valid_moves), self.game.size * self.game.size)
        
        # Make a move and check if valid moves decreased
        self.game.make_move(7, 7)
        valid_moves = self.game.get_valid_moves()
        self.assertEqual(len(valid_moves), self.game.size * self.game.size - 1)
    
    def test_board_full(self):
        """Test board full condition"""
        self.assertFalse(self.game.is_board_full())
        
        # Fill the board
        for i in range(self.game.size):
            for j in range(self.game.size):
                if (i + j) % 2 == 0:
                    self.game.make_move(i, j)
        
        self.assertTrue(self.game.is_board_full())

if __name__ == '__main__':
    unittest.main() 