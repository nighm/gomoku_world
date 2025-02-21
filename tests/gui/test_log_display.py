"""
Unit tests for the LogDisplay component
鏃ュ織鏄剧ず缁勪欢鍗曞厓娴嬭瘯
"""

import unittest
import pygame
from gomoku_world.gui.log_display import LogDisplay
from gomoku_world.theme import theme
from tests.gui.test_base import GUITestCase

class TestLogDisplay(GUITestCase):
    def setUp(self):
        """Set up test environment"""
        super().setUp()
        self.rect = pygame.Rect(600, 400, 180, 140)
        self.log_display = LogDisplay(self.rect, max_lines=5)
    
    def test_log_display_initialization(self):
        """Test log display initialization"""
        self.assertRectEqual(self.log_display.rect, self.rect)
        self.assertEqual(self.log_display.max_lines, 5)
        self.assertEqual(len(self.log_display.lines), 0)
        self.assertIsNotNone(self.log_display.font)
    
    def test_add_line(self):
        """Test adding lines to log display"""
        # Test single line
        self.log_display.add_line("Test message")
        self.assertEqual(len(self.log_display.lines), 1)
        self.assertEqual(self.log_display.lines[0], "Test message")
        
        # Test multiple lines
        messages = ["Message " + str(i) for i in range(4)]
        for msg in messages:
            self.log_display.add_line(msg)
        self.assertEqual(len(self.log_display.lines), 5)
        
        # Test overflow
        self.log_display.add_line("New message")
        self.assertEqual(len(self.log_display.lines), 5)
        self.assertEqual(self.log_display.lines[0], "Message 0")
        self.assertEqual(self.log_display.lines[-1], "New message")
    
    def test_clear(self):
        """Test clearing log display"""
        # Add some lines
        for i in range(3):
            self.log_display.add_line(f"Message {i}")
        self.assertEqual(len(self.log_display.lines), 3)
        
        # Clear lines
        self.log_display.clear()
        self.assertEqual(len(self.log_display.lines), 0)
        
        # Add more lines after clearing
        self.log_display.add_line("New message")
        self.assertEqual(len(self.log_display.lines), 1)
    
    def test_draw(self):
        """Test drawing log display"""
        # Test empty log
        self.log_display.draw(self.screen)
        bg_color = self.get_surface_color_at(self.screen, (self.rect.centerx, self.rect.centery))
        self.assertColorEqual(bg_color, (240, 240, 240))  # Background color
        
        # Test with lines
        messages = [f"Message {i}" for i in range(3)]
        for msg in messages:
            self.log_display.add_line(msg)
        
        self.log_display.draw(self.screen)
        border_color = self.get_surface_color_at(self.screen, (self.rect.left, self.rect.top))
        self.assertColorEqual(border_color, theme.get_color('text'))
    
    def test_max_lines_limit(self):
        """Test maximum lines limit"""
        # Add more lines than max_lines
        for i in range(10):
            self.log_display.add_line(f"Message {i}")
        
        # Check that only max_lines are kept
        self.assertEqual(len(self.log_display.lines), 5)
        self.assertEqual(self.log_display.lines[0], "Message 5")
        self.assertEqual(self.log_display.lines[-1], "Message 9")
        
        # Add one more line
        self.log_display.add_line("Final message")
        self.assertEqual(len(self.log_display.lines), 5)
        self.assertEqual(self.log_display.lines[-1], "Final message")
    
    def test_unicode_text(self):
        """Test handling of Unicode text"""
        unicode_messages = [
            "浣犲ソ锛屼笘鐣?,  # Chinese
            "銇撱倱銇仭銇?,  # Japanese
            "鞎堧厱頃橃劯鞖?,  # Korean
            "袩褉懈胁械褌",    # Russian
            "馃幃馃幉馃幆"     # Emojis
        ]
        
        for msg in unicode_messages:
            self.log_display.add_line(msg)
            self.log_display.draw(self.screen)
            # Just verify no exceptions are raised
            self.assertTrue(True)
    
    def test_long_text(self):
        """Test handling of long text"""
        long_messages = [
            "A" * 100,  # Very long single line
            "This is a very long message that should be handled properly by the log display",
            "Another long message " * 5
        ]
        
        for msg in long_messages:
            self.log_display.add_line(msg)
            self.log_display.draw(self.screen)
            # Just verify no exceptions are raised
            self.assertTrue(True)
    
    def test_special_characters(self):
        """Test handling of special characters"""
        special_messages = [
            "Line\nbreak",  # Newline
            "Tab\there",    # Tab
            "Special: !@#$%^&*()",  # Special characters
            "",  # Empty string
            " "  # Space only
        ]
        
        for msg in special_messages:
            self.log_display.add_line(msg)
            self.log_display.draw(self.screen)
            # Just verify no exceptions are raised
            self.assertTrue(True)
    
    def test_rapid_updates(self):
        """Test rapid log updates"""
        # Add and clear rapidly
        for i in range(100):
            self.log_display.add_line(f"Message {i}")
            if i % 10 == 0:
                self.log_display.clear()
            self.log_display.draw(self.screen)
        
        # Should still respect max_lines
        self.assertLessEqual(len(self.log_display.lines), self.log_display.max_lines)
    
    def test_different_sizes(self):
        """Test different log display sizes"""
        test_sizes = [
            pygame.Rect(0, 0, 100, 50),    # Small
            pygame.Rect(0, 0, 500, 300),   # Large
            pygame.Rect(0, 0, 1000, 50),   # Wide
            pygame.Rect(0, 0, 50, 1000),   # Tall
            pygame.Rect(0, 0, 10, 10)      # Tiny
        ]
        
        for rect in test_sizes:
            log = LogDisplay(rect, max_lines=5)
            log.add_line("Test message")
            log.draw(self.screen)
            # Just verify no exceptions are raised
            self.assertTrue(True)

if __name__ == '__main__':
    unittest.main() 
