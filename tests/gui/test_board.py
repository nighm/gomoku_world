"""
Unit tests for the Board component
棋盘组件单元测试
"""

import unittest
import pygame
from src.gui.board import Board
from src.game import Game
from src.theme import theme
from tests.gui.test_base import GUITestCase

class TestBoard(GUITestCase):
    def setUp(self):
        """Set up test environment"""
        super().setUp()
        self.window_size = 800
        self.game = Game(size=15)
        self.board = Board(self.window_size, self.game)
    
    def test_board_initialization(self):
        """Test board initialization"""
        self.assertEqual(self.board.window_size, self.window_size)
        self.assertEqual(self.board.game, self.game)
        self.assertEqual(self.board.grid_size, self.window_size // (self.game.size + 1))
        self.assertIsNone(self.board.last_move)
    
    def test_handle_click_valid(self):
        """Test handling valid click positions"""
        # Test various valid positions
        test_positions = [
            ((1, 1), (0, 0)),    # Top-left corner
            ((13, 13), (12, 12)),  # Bottom-right corner
            ((8, 8), (7, 7)),    # Center
            ((1, 13), (0, 12)),  # Top-right corner
            ((13, 1), (12, 0))   # Bottom-left corner
        ]
        
        for click_pos, expected_move in test_positions:
            grid_size = self.board.grid_size
            pos = (grid_size * click_pos[0], grid_size * click_pos[1])
            move = self.board.handle_click(pos)
            self.assertEqual(move, expected_move)
    
    def test_handle_click_invalid(self):
        """Test handling invalid click positions"""
        invalid_positions = [
            (self.window_size + 10, self.window_size + 10),  # Outside board
            (-10, -10),  # Negative coordinates
            (0, 0),      # Too close to edge
            (self.window_size // 2, -10),  # Valid x, invalid y
            (-10, self.window_size // 2)   # Invalid x, valid y
        ]
        
        for pos in invalid_positions:
            move = self.board.handle_click(pos)
            self.assertIsNone(move)
    
    def test_set_last_move(self):
        """Test setting last move"""
        test_moves = [
            (7, 7),   # Center
            (0, 0),   # Corner
            (14, 14), # Edge
            (5, 9),   # Random position
        ]
        
        for move in test_moves:
            self.board.set_last_move(move)
            self.assertEqual(self.board.last_move, move)
    
    def test_draw_board(self):
        """Test board drawing"""
        # Test empty board
        self.board.draw(self.screen)
        # Check background color between grid lines
        check_pos = (self.board.grid_size * 1.5, self.board.grid_size * 1.5)
        bg_color = self.get_surface_color_at(self.screen, check_pos)
        expected_bg_color = theme.get_color('background')
        self.assertColorEqual(bg_color, expected_bg_color)
        
        # Test board with pieces
        test_moves = [
            (7, 7),   # Black piece
            (8, 8),   # White piece
            (7, 8),   # Black piece
            (8, 7)    # White piece
        ]
        
        for i, move in enumerate(test_moves):
            self.game.make_move(move[0], move[1])
            self.board.set_last_move(move)
            self.board.draw(self.screen)
            
            # Check piece color
            pos = (self.board.grid_size * (move[1] + 1), self.board.grid_size * (move[0] + 1))
            color = self.get_surface_color_at(self.screen, pos)
            expected_color = theme.get_color('black_piece' if i % 2 == 0 else 'white_piece')
            self.assertColorEqual(color, expected_color)
    
    def test_grid_size_calculation(self):
        """Test grid size calculation"""
        # Test different board sizes
        test_sizes = [9, 13, 15, 19]
        for size in test_sizes:
            game = Game(size=size)
            board = Board(self.window_size, game)
            expected_size = self.window_size // (size + 1)
            self.assertEqual(board.grid_size, expected_size)
    
    def test_star_points(self):
        """Test star points drawing"""
        # Test 15x15 board
        self.board.draw(self.screen)
        star_points_15 = [
            (3, 3), (3, 7), (3, 11),
            (7, 3), (7, 7), (7, 11),
            (11, 3), (11, 7), (11, 11)
        ]
        
        for row, col in star_points_15:
            pos = (self.board.grid_size * (row + 1), self.board.grid_size * (col + 1))
            # 检查星位点周围的多个点
            offsets = [(0, 0), (2, 0), (-2, 0), (0, 2), (0, -2)]
            found_star = False
            for dx, dy in offsets:
                check_pos = (pos[0] + dx, pos[1] + dy)
                color = self.get_surface_color_at(self.screen, check_pos)
                if color == theme.get_color('grid'):
                    found_star = True
                    break
            self.assertTrue(found_star, f"Star point not found at {pos}")
        
        # Test 19x19 board
        game = Game(size=19)
        board = Board(self.window_size, game)
        board.draw(self.screen)
        star_points_19 = [
            (3, 3), (3, 9), (3, 15),
            (9, 3), (9, 9), (9, 15),
            (15, 3), (15, 9), (15, 15)
        ]
        
        for row, col in star_points_19:
            pos = (board.grid_size * (row + 1), board.grid_size * (col + 1))
            # 检查星位点周围的多个点
            offsets = [(0, 0), (2, 0), (-2, 0), (0, 2), (0, -2)]
            found_star = False
            for dx, dy in offsets:
                check_pos = (pos[0] + dx, pos[1] + dy)
                color = self.get_surface_color_at(self.screen, check_pos)
                if color == theme.get_color('grid'):
                    found_star = True
                    break
            self.assertTrue(found_star, f"Star point not found at {pos}")
    
    def test_last_move_highlight(self):
        """Test last move highlight"""
        # Make a move
        move = (7, 7)
        self.game.make_move(move[0], move[1])
        self.board.set_last_move(move)
        self.board.draw(self.screen)
        
        # Check highlight
        pos = (self.board.grid_size * (move[1] + 1), self.board.grid_size * (move[0] + 1))
        color = self.get_surface_color_at(self.screen, pos)
        self.assertNotEqual(color, theme.get_color('background'))
    
    def test_board_boundaries(self):
        """Test board boundaries"""
        # Test clicks near board boundaries
        boundary_positions = [
            (self.board.grid_size, self.board.grid_size),  # Top-left valid
            (self.board.grid_size * 15, self.board.grid_size * 15),  # Bottom-right valid
            (self.board.grid_size * 0.5, self.board.grid_size * 0.5),  # Just outside top-left
            (self.board.grid_size * 15.5, self.board.grid_size * 15.5)  # Just outside bottom-right
        ]
        
        for pos in boundary_positions:
            move = self.board.handle_click(pos)
            if 1 <= pos[0] / self.board.grid_size <= 15 and 1 <= pos[1] / self.board.grid_size <= 15:
                self.assertIsNotNone(move)
            else:
                self.assertIsNone(move)

if __name__ == '__main__':
    unittest.main() 