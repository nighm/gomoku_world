"""
Base test class for GUI components
GUI组件测试基类
"""

import unittest
import pygame
import os
import sys
from typing import Tuple

class GUITestCase(unittest.TestCase):
    """Base test class for GUI components"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment once for all tests"""
        # Initialize pygame
        os.environ['SDL_VIDEODRIVER'] = 'dummy'  # Use dummy video driver
        pygame.init()
        pygame.font.init()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        pygame.quit()
    
    def setUp(self):
        """Set up test environment for each test"""
        self.screen = pygame.Surface((800, 600))
    
    def assertColorEqual(self, color1: Tuple[int, int, int], color2: Tuple[int, int, int]):
        """Assert that two colors are equal"""
        self.assertEqual(len(color1), len(color2))
        for c1, c2 in zip(color1, color2):
            self.assertEqual(c1, c2)
    
    def assertRectEqual(self, rect1: pygame.Rect, rect2: pygame.Rect):
        """Assert that two rectangles are equal"""
        self.assertEqual(rect1.x, rect2.x)
        self.assertEqual(rect1.y, rect2.y)
        self.assertEqual(rect1.width, rect2.width)
        self.assertEqual(rect1.height, rect2.height)
    
    def simulate_click(self, pos: Tuple[int, int]) -> bool:
        """Simulate mouse click at given position"""
        # Create motion event
        motion_event = pygame.event.Event(pygame.MOUSEMOTION, {'pos': pos})
        
        # Create click event
        click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {
            'button': 1,
            'pos': pos
        })
        
        # Process events
        handled = False
        if hasattr(self, 'button'):
            # Handle motion first
            if self.button.handle_event(motion_event):
                handled = True
            # Then handle click
            if self.button.handle_event(click_event):
                handled = True
        return handled
    
    def simulate_key_press(self, key: int) -> bool:
        """Simulate keyboard key press"""
        event = pygame.event.Event(pygame.KEYDOWN, {'key': key})
        
        # Process event
        handled = False
        if hasattr(self, 'handle_event'):
            handled = self.handle_event(event)
        return handled
    
    def get_surface_color_at(self, surface: pygame.Surface, pos: Tuple[int, int]) -> Tuple[int, int, int]:
        """Get color at specific position on surface"""
        try:
            return surface.get_at((int(pos[0]), int(pos[1])))[:3]  # Ignore alpha channel
        except IndexError:
            return (0, 0, 0)  # Return black for out of bounds 