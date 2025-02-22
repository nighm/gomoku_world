"""
Button widget implementation
按钮组件实现
"""

import pygame
from typing import Optional, Callable, Tuple

from ...i18n import i18n_manager
from ...theme import theme
from ...utils.logger import get_logger

logger = get_logger(__name__)

class Button:
    """Button widget with internationalization support"""
    
    def __init__(
        self,
        text_key: str,
        x: int,
        y: int,
        width: int,
        height: int,
        callback: Optional[Callable] = None,
        category: str = "common"
    ):
        """
        Initialize button
        
        Args:
            text_key: Translation key for button text
            x: X position
            y: Y position
            width: Button width
            height: Button height
            callback: Click callback function
            category: Translation category
        """
        self.text_key = text_key
        self.category = category
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback
        self.is_hovered = False
        self.is_pressed = False
        
        # Update text
        self.update_text()
        
        logger.debug(f"Button created: {text_key}")
        
    def update_text(self):
        """Update button text when language changes"""
        self.text = i18n_manager.get_text(self.text_key, self.category)
        
        # Create text surface
        font = pygame.font.SysFont(i18n_manager.get_font_family(), 24)
        self.text_surface = font.render(self.text, True, pygame.Color(theme.get_color("button.foreground")))
        
        # Center text
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        
    def draw(self, surface: pygame.Surface):
        """Draw button on surface"""
        # Get colors
        if self.is_pressed:
            color = pygame.Color(theme.get_color("button.active_background"))
        elif self.is_hovered:
            color = pygame.Color(theme.get_color("button.hover_background"))
        else:
            color = pygame.Color(theme.get_color("button.background"))
            
        # Draw button
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, pygame.Color(theme.get_color("button.foreground")), self.rect, 1)
        
        # Draw text
        surface.blit(self.text_surface, self.text_rect)
        
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle mouse event
        
        Returns:
            bool: True if event was handled
        """
        if event.type == pygame.MOUSEMOTION:
            # Update hover state
            self.is_hovered = self.rect.collidepoint(event.pos)
            return self.is_hovered
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                self.is_pressed = True
                return True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.is_pressed:
                self.is_pressed = False
                if self.is_hovered and self.callback:
                    self.callback()
                return True
                
        return False 