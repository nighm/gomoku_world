"""
Unit tests for the Button component
按钮组件单元测试
"""

import unittest
import pygame
from src.gui.button import Button
from src.theme import theme
from tests.gui.test_base import GUITestCase

class TestButton(GUITestCase):
    def setUp(self):
        """Set up test environment"""
        super().setUp()
        self.rect = pygame.Rect(100, 100, 200, 50)
        self.clicked = False
        self.click_count = 0
        
        def on_click():
            self.clicked = True
            self.click_count += 1
            
        self.button = Button("Test Button", self.rect, on_click)
    
    def test_button_initialization(self):
        """Test button initialization"""
        self.assertEqual(self.button.text, "Test Button")
        self.assertRectEqual(self.button.rect, self.rect)
        self.assertFalse(self.button.hovered)
        self.assertIsNone(self.button.icon)
        self.assertIsNone(self.button.icon_surface)
    
    def test_button_hover(self):
        """Test button hover state"""
        # Test mouse outside button
        event = pygame.event.Event(pygame.MOUSEMOTION, {'pos': (0, 0)})
        self.button.handle_event(event)
        self.assertFalse(self.button.hovered)
        
        # Test mouse over button
        event = pygame.event.Event(pygame.MOUSEMOTION, {'pos': (150, 125)})
        self.button.handle_event(event)
        self.assertTrue(self.button.hovered)
    
    def test_button_click(self):
        """Test button click handling"""
        # Move mouse over button
        event = pygame.event.Event(pygame.MOUSEMOTION, {'pos': (150, 125)})
        self.button.handle_event(event)
        
        # Click button
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (150, 125)})
        self.button.handle_event(event)
        self.assertTrue(self.clicked)
        self.assertEqual(self.click_count, 1)
        
        # Click again
        self.button.handle_event(event)
        self.assertEqual(self.click_count, 2)
    
    def test_button_click_outside(self):
        """Test clicking outside button"""
        # Click outside button
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (0, 0)})
        self.button.handle_event(event)
        self.assertFalse(self.clicked)
        self.assertEqual(self.click_count, 0)
    
    def test_button_draw(self):
        """Test button drawing"""
        font = pygame.font.SysFont(None, 24)
        
        # Draw button in normal state
        self.button.draw(self.screen, font)
        normal_color = self.get_surface_color_at(self.screen, (150, 125))
        self.assertColorEqual(normal_color, theme.get_color('button'))
        
        # Draw button in hover state
        self.button.hovered = True
        self.button.draw(self.screen, font)
        hover_color = self.get_surface_color_at(self.screen, (150, 125))
        self.assertColorEqual(hover_color, theme.get_color('button_hover'))
    
    def test_button_with_icon(self):
        """Test button with icon"""
        button = Button("Icon Button", self.rect, lambda: None, icon="test")
        self.assertEqual(button.icon, "test")
        self.assertIsNone(button.icon_surface)  # Icon should be None as file doesn't exist
    
    def test_button_text_overflow(self):
        """Test button with long text"""
        long_text = "This is a very long button text that should be handled properly"
        button = Button(long_text, self.rect, lambda: None)
        font = pygame.font.SysFont(None, 24)
        
        # Draw button with long text
        button.draw(self.screen, font)
        # Just verify no exceptions are raised
        self.assertTrue(True)
    
    def test_button_edge_cases(self):
        """Test button edge cases"""
        # Empty text
        button = Button("", self.rect, lambda: None)
        font = pygame.font.SysFont(None, 24)
        button.draw(self.screen, font)
        
        # Zero size rect
        zero_rect = pygame.Rect(0, 0, 0, 0)
        button = Button("Test", zero_rect, lambda: None)
        button.draw(self.screen, font)
        
        # Negative size rect
        neg_rect = pygame.Rect(0, 0, -10, -10)
        button = Button("Test", neg_rect, lambda: None)
        button.draw(self.screen, font)
    
    def test_button_rapid_clicks(self):
        """Test rapid button clicks"""
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (150, 125)})
        for _ in range(10):
            self.button.handle_event(event)
        self.assertEqual(self.click_count, 10)
    
    def test_button_hover_edge(self):
        """Test button hover at edges"""
        # Test hover at button edges
        edges = [
            (self.rect.left, self.rect.centery),   # Left edge
            (self.rect.right, self.rect.centery),  # Right edge
            (self.rect.centerx, self.rect.top),    # Top edge
            (self.rect.centerx, self.rect.bottom)  # Bottom edge
        ]
        
        for pos in edges:
            event = pygame.event.Event(pygame.MOUSEMOTION, {'pos': pos})
            self.button.handle_event(event)
            self.assertTrue(self.button.hovered)

if __name__ == '__main__':
    unittest.main() 