"""
Button component for the Gomoku game GUI
五子棋游戏GUI按钮组件
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
    带有悬停效果和文本的按钮
    """
    
    def __init__(self, rect: pygame.Rect, text: str, font_size: int = 20):
        """
        Initialize button
        初始化按钮
        
        Args:
            rect: Button rectangle (按钮矩形)
            text: Button text (按钮文本)
            font_size: Font size (字体大小)
        """
        self.rect = rect
        self.text = text
        self.font_size = font_size
        self.is_hovered = False
        
        # Get font from configuration manager
        # 从配置管理器获取字体
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
        绘制按钮
        
        Args:
            screen: Surface to draw on (绘制表面)
            mouse_pos: Current mouse position (当前鼠标位置)
        """
        # Update hover state
        # 更新悬停状态
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Draw button background
        # 绘制按钮背景
        color = theme.get_color('button_hover' if self.is_hovered else 'button')
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, theme.get_color('border'), self.rect, 1)
        
        # Draw text
        # 绘制文本
        text_surface = self.font.render(self.text, True, theme.get_color('text'))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def handle_click(self, mouse_pos: Tuple[int, int]) -> bool:
        """
        Handle click event
        处理点击事件
        
        Args:
            mouse_pos: Mouse position (鼠标位置)
        
        Returns:
            bool: True if button was clicked (如果按钮被点击则返回True)
        """
        return self.rect.collidepoint(mouse_pos)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle mouse events
        处理鼠标事件
        
        Args:
            event: Pygame event (pygame事件)
        
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