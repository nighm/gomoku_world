"""
Unit tests for the GomokuGUI main window
五子棋游戏主窗口单元测试
"""

import unittest
import pygame
from gomoku_world.gui.main_window import GomokuGUI

class TestGomokuGUI(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        pygame.init()
        self.gui = GomokuGUI(window_size=800)
    
    def tearDown(self):
        """Clean up after tests"""
        pygame.quit()
    
    def test_gui_initialization(self):
        """Test GUI initialization"""
        self.assertEqual(self.gui.window_size, 800)
        self.assertEqual(self.gui.sidebar_width, 180)
        self.assertTrue(self.gui.running)
        self.assertFalse(self.gui.show_settings)
        self.assertIsNone(self.gui.game_mode)
        self.assertEqual(len(self.gui.ai_players), 0)
        self.assertIsNotNone(self.gui.game)
        self.assertIsNotNone(self.gui.board)
        self.assertIsNotNone(self.gui.sound)
        self.assertIsNotNone(self.gui.debug)
        self.assertIsNotNone(self.gui.settings_menu)
        self.assertIsNotNone(self.gui.log_display)
    
    def test_button_creation(self):
        """Test button creation"""
        self.assertGreater(len(self.gui.buttons), 0)
        # Check if essential buttons exist
        button_texts = [button.text for button in self.gui.buttons]
        self.assertIn('双人对战', button_texts)
        self.assertIn('人机对战（简单）', button_texts)
        self.assertIn('设置', button_texts)
        self.assertIn('退出', button_texts)
    
    def test_game_mode_setting(self):
        """Test setting game modes"""
        # Test PvP mode
        self.gui.set_game_mode('pvp')
        self.assertEqual(self.gui.game_mode, 'pvp')
        self.assertEqual(len(self.gui.ai_players), 0)
        
        # Test AI mode
        self.gui.set_game_mode('ai_easy')
        self.assertEqual(self.gui.game_mode, 'ai_easy')
        self.assertEqual(len(self.gui.ai_players), 1)
        self.assertIn(2, self.gui.ai_players)  # AI should be player 2
    
    def test_settings_menu(self):
        """Test settings menu"""
        self.assertFalse(self.gui.show_settings)
        self.gui.open_settings()
        self.assertTrue(self.gui.show_settings)
    
    def test_quit_game(self):
        """Test quitting game"""
        self.assertTrue(self.gui.running)
        self.gui.quit_game()
        self.assertFalse(self.gui.running)
    
    def test_handle_game_event(self):
        """Test game event handling"""
        # Test invalid move
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {
            'button': 1,
            'pos': (-1, -1)  # Invalid position
        })
        self.gui._handle_game_event(event)
        # Should not make any move
        self.assertEqual(self.gui.game.board[7][7], 0)
        
        # Test valid move
        grid_size = self.gui.board.grid_size
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {
            'button': 1,
            'pos': (grid_size * 8, grid_size * 8)  # Position (7, 7)
        })
        self.gui._handle_game_event(event)
        # Move should be made on the board
        self.assertEqual(self.gui.game.board[7][7], 1)
    
    def test_draw_screen(self):
        """Test screen drawing"""
        # Make some moves
        self.gui.game.make_move(7, 7)
        self.gui.game.make_move(8, 8)
        self.gui.board.set_last_move((8, 8))
        
        # Draw screen
        self.gui._draw_screen()
        # Since drawing is visual, we just verify no exceptions are raised
        self.assertTrue(True)
    
    def test_ai_game_mode(self):
        """Test AI game modes"""
        # Test easy AI
        self.gui.set_game_mode('ai_easy')
        self.assertEqual(self.gui.ai_players[2].difficulty, 'easy')
        
        # Test medium AI
        self.gui.set_game_mode('ai_medium')
        self.assertEqual(self.gui.ai_players[2].difficulty, 'medium')
        
        # Test hard AI
        self.gui.set_game_mode('ai_hard')
        self.assertEqual(self.gui.ai_players[2].difficulty, 'hard')

if __name__ == '__main__':
    unittest.main()
