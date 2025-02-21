"""
Settings menu for the Gomoku game
五子棋游戏设置菜单
"""

import pygame
import logging
from typing import Dict, Any, Tuple, Optional
from ..theme import theme
from ..i18n import i18n
from .button import Button

logger = logging.getLogger(__name__)

class SettingsMenu:
    """
    Settings menu interface
    设置菜单界面
    """
    
    def __init__(self, screen: pygame.Surface):
        """
        Initialize settings menu
        初始化设置菜单
        
        Args:
            screen: Pygame surface to draw on (pygame绘制表面)
        """
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 400, 500)
        self.rect.center = (screen.get_width() // 2, screen.get_height() // 2)
        
        # Create buttons
        # 创建按钮
        button_width = 300
        button_height = 40
        button_margin = 20
        
        # Volume slider
        # 音量滑块
        self.volume_rect = pygame.Rect(
            self.rect.left + 50,
            self.rect.top + 100,
            button_width,
            button_height
        )
        
        # Language selection
        # 语言选择
        self.language_buttons = {
            'en': Button(
                pygame.Rect(
                    self.rect.left + 50,
                    self.rect.top + 180,
                    button_width // 2 - 10,
                    button_height
                ),
                "English"
            ),
            'zh': Button(
                pygame.Rect(
                    self.rect.left + 50 + button_width // 2 + 10,
                    self.rect.top + 180,
                    button_width // 2 - 10,
                    button_height
                ),
                "中文"
            )
        }
        
        # Theme selection
        # 主题选择
        self.theme_buttons = {
            'classic': Button(
                pygame.Rect(
                    self.rect.left + 50,
                    self.rect.top + 260,
                    button_width // 3 - 10,
                    button_height
                ),
                i18n.get_bilingual("themes.classic")
            ),
            'modern': Button(
                pygame.Rect(
                    self.rect.left + 50 + button_width // 3 + 10,
                    self.rect.top + 260,
                    button_width // 3 - 10,
                    button_height
                ),
                i18n.get_bilingual("themes.modern")
            ),
            'dark': Button(
                pygame.Rect(
                    self.rect.left + 50 + 2 * (button_width // 3 + 10),
                    self.rect.top + 260,
                    button_width // 3 - 10,
                    button_height
                ),
                i18n.get_bilingual("themes.dark")
            )
        }
        
        # Save and cancel buttons
        # 保存和取消按钮
        self.save_button = Button(
            pygame.Rect(
                self.rect.left + 50,
                self.rect.bottom - 70,
                button_width // 2 - 10,
                button_height
            ),
            i18n.get_bilingual("settings.save")
        )
        
        self.cancel_button = Button(
            pygame.Rect(
                self.rect.left + 50 + button_width // 2 + 10,
                self.rect.bottom - 70,
                button_width // 2 - 10,
                button_height
            ),
            i18n.get_bilingual("settings.cancel")
        )
        
        # Current settings
        # 当前设置
        self.current_settings = {
            'volume': 0.7,
            'language': 'en',
            'theme': 'classic'
        }
    
    def draw(self, mouse_pos: Tuple[int, int]):
        """
        Draw the settings menu
        绘制设置菜单
        
        Args:
            mouse_pos: Current mouse position (当前鼠标位置)
        """
        # Draw background
        # 绘制背景
        pygame.draw.rect(self.screen, theme.get_color('menu_bg'), self.rect)
        pygame.draw.rect(self.screen, theme.get_color('border'), self.rect, 2)
        
        # Draw title
        # 绘制标题
        try:
            title_font = pygame.font.Font("C:\\Windows\\Fonts\\simhei.ttf", 24)
        except:
            title_font = pygame.font.Font(None, 24)
        
        title = title_font.render(i18n.get_bilingual("settings.title"), True, theme.get_color('text'))
        title_rect = title.get_rect(midtop=(self.rect.centerx, self.rect.top + 20))
        self.screen.blit(title, title_rect)
        
        # Draw volume slider
        # 绘制音量滑块
        volume_label = title_font.render(i18n.get_bilingual("settings.volume"), True, theme.get_color('text'))
        self.screen.blit(volume_label, (self.volume_rect.left, self.volume_rect.top - 30))
        pygame.draw.rect(self.screen, theme.get_color('button'), self.volume_rect)
        pygame.draw.rect(self.screen, theme.get_color('slider_fill'),
                        pygame.Rect(self.volume_rect.left,
                                  self.volume_rect.top,
                                  self.volume_rect.width * self.current_settings['volume'],
                                  self.volume_rect.height))
        
        # Draw language label
        # 绘制语言标签
        lang_label = title_font.render(i18n.get_bilingual("settings.language"), True, theme.get_color('text'))
        self.screen.blit(lang_label, (self.language_buttons['en'].rect.left, self.language_buttons['en'].rect.top - 30))
        
        # Draw theme label
        # 绘制主题标签
        theme_label = title_font.render(i18n.get_bilingual("settings.theme"), True, theme.get_color('text'))
        self.screen.blit(theme_label, (self.theme_buttons['classic'].rect.left, self.theme_buttons['classic'].rect.top - 30))
        
        # Draw buttons
        # 绘制按钮
        for button in self.language_buttons.values():
            button.draw(self.screen, mouse_pos)
        
        for button in self.theme_buttons.values():
            button.draw(self.screen, mouse_pos)
        
        self.save_button.draw(self.screen, mouse_pos)
        self.cancel_button.draw(self.screen, mouse_pos)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle settings menu events
        处理设置菜单事件
        
        Args:
            event: Pygame event (pygame事件)
        
        Returns:
            bool: True if settings menu should close (如果设置菜单应该关闭则返回True)
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                
                # Handle volume slider
                # 处理音量滑块
                if self.volume_rect.collidepoint(mouse_pos):
                    self.current_settings['volume'] = (mouse_pos[0] - self.volume_rect.left) / self.volume_rect.width
                    self.current_settings['volume'] = max(0, min(1, self.current_settings['volume']))
                    return False
                
                # Handle language buttons
                # 处理语言按钮
                for lang, button in self.language_buttons.items():
                    if button.rect.collidepoint(mouse_pos):
                        self.current_settings['language'] = lang
                        i18n.set_language(lang)
                        return False
                
                # Handle theme buttons
                # 处理主题按钮
                for theme_name, button in self.theme_buttons.items():
                    if button.rect.collidepoint(mouse_pos):
                        self.current_settings['theme'] = theme_name
                        theme.set_theme(theme_name)
                        return False
                
                # Handle save/cancel
                # 处理保存/取消
                if self.save_button.rect.collidepoint(mouse_pos):
                    self.save_settings()
                    return True
                
                if self.cancel_button.rect.collidepoint(mouse_pos):
                    return True
        
        return False
    
    def save_settings(self):
        """
        Save current settings
        保存当前设置
        """
        # TODO: Implement settings save
        # TODO: 实现设置保存
        pass 