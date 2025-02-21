"""
Button component for the Gomoku game GUI
浜斿瓙妫嬫父鎴廏UI鎸夐挳缁勪欢
"""

import os
import pygame
import logging
from ..theme import theme
from ..config.manager import config_manager
from typing import Tuple

logger = logging.getLogger(__name__)

class Button:
    """
    Button with hover effect and text
    甯︽湁鎮仠鏁堟灉鍜屾枃鏈殑鎸夐挳
    """
    
    def __init__(self, rect: pygame.Rect, text: str, font_size: int = 20):
        """
        Initialize button
        鍒濆鍖栨寜閽?
        
        Args:
            rect: Button rectangle (鎸夐挳鐭╁舰)
            text: Button text (鎸夐挳鏂囨湰)
            font_size: Font size (瀛椾綋澶у皬)
        """
        self.rect = rect
        self.text = text
        self.font_size = font_size
        self.is_hovered = False
        
        # Get font from configuration manager
        # 浠庨厤缃鐞嗗櫒鑾峰彇瀛椾綋
        font_path = config_manager.get_font_path()
        try:
            self.font = pygame.font.Font(font_path, font_size)
        except Exception as e:
            logger.warning(f"Failed to load font {font_path}: {e}")
            self.font = pygame.font.Font(None, font_size)
            
        if config_manager.is_debug_mode():
            logger.debug(f"Button initialized with font: {font_path}")

    def draw(self, screen: pygame.Surface, mouse_pos: Tuple[int, int]):
        """
        Draw the button
        缁樺埗鎸夐挳
        
        Args:
            screen: Surface to draw on (缁樺埗琛ㄩ潰)
            mouse_pos: Current mouse position (褰撳墠榧犳爣浣嶇疆)
        """
        # Update hover state
        # 鏇存柊鎮仠鐘舵€?
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Draw button background
        # 缁樺埗鎸夐挳鑳屾櫙
        color = theme.get_color('button_hover' if self.is_hovered else 'button')
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, theme.get_color('border'), self.rect, 1)
        
        # Draw text
        # 缁樺埗鏂囨湰
        text_surface = self.font.render(self.text, True, theme.get_color('text'))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def handle_click(self, mouse_pos: Tuple[int, int]) -> bool:
        """
        Handle click event
        澶勭悊鐐瑰嚮浜嬩欢
        
        Args:
            mouse_pos: Mouse position (榧犳爣浣嶇疆)
        
        Returns:
            bool: True if button was clicked (濡傛灉鎸夐挳琚偣鍑诲垯杩斿洖True)
        """
        return self.rect.collidepoint(mouse_pos)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle mouse events
        澶勭悊榧犳爣浜嬩欢
        
        Args:
            event: Pygame event (pygame浜嬩欢)
        
        Returns:
            bool: True if button was clicked
        """
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False 
