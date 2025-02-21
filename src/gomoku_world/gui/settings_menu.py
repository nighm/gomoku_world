"""
Settings menu for the Gomoku game
浜斿瓙妫嬫父鎴忚缃彍鍗?
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
    璁剧疆鑿滃崟鐣岄潰
    """
    
    def __init__(self, screen: pygame.Surface):
        """
        Initialize settings menu
        鍒濆鍖栬缃彍鍗?
        
        Args:
            screen: Pygame surface to draw on (pygame缁樺埗琛ㄩ潰)
        """
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 400, 500)
        self.rect.center = (screen.get_width() // 2, screen.get_height() // 2)
        
        # Create buttons
        # 鍒涘缓鎸夐挳
        button_width = 300
        button_height = 40
        button_margin = 20
        
        # Volume slider
        # 闊抽噺婊戝潡
        self.volume_rect = pygame.Rect(
            self.rect.left + 50,
            self.rect.top + 100,
            button_width,
            button_height
        )
        
        # Language selection
        # 璇█閫夋嫨
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
                "涓枃"
            )
        }
        
        # Theme selection
        # 涓婚閫夋嫨
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
        # 淇濆瓨鍜屽彇娑堟寜閽?
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
        # 褰撳墠璁剧疆
        self.current_settings = {
            'volume': 0.7,
            'language': 'en',
            'theme': 'classic'
        }
    
    def draw(self, mouse_pos: Tuple[int, int]):
        """
        Draw the settings menu
        缁樺埗璁剧疆鑿滃崟
        
        Args:
            mouse_pos: Current mouse position (褰撳墠榧犳爣浣嶇疆)
        """
        # Draw background
        # 缁樺埗鑳屾櫙
        pygame.draw.rect(self.screen, theme.get_color('menu_bg'), self.rect)
        pygame.draw.rect(self.screen, theme.get_color('border'), self.rect, 2)
        
        # Draw title
        # 缁樺埗鏍囬
        try:
            title_font = pygame.font.Font("C:\\Windows\\Fonts\\simhei.ttf", 24)
        except:
            title_font = pygame.font.Font(None, 24)
        
        title = title_font.render(i18n.get_bilingual("settings.title"), True, theme.get_color('text'))
        title_rect = title.get_rect(midtop=(self.rect.centerx, self.rect.top + 20))
        self.screen.blit(title, title_rect)
        
        # Draw volume slider
        # 缁樺埗闊抽噺婊戝潡
        volume_label = title_font.render(i18n.get_bilingual("settings.volume"), True, theme.get_color('text'))
        self.screen.blit(volume_label, (self.volume_rect.left, self.volume_rect.top - 30))
        pygame.draw.rect(self.screen, theme.get_color('button'), self.volume_rect)
        pygame.draw.rect(self.screen, theme.get_color('slider_fill'),
                        pygame.Rect(self.volume_rect.left,
                                  self.volume_rect.top,
                                  self.volume_rect.width * self.current_settings['volume'],
                                  self.volume_rect.height))
        
        # Draw language label
        # 缁樺埗璇█鏍囩
        lang_label = title_font.render(i18n.get_bilingual("settings.language"), True, theme.get_color('text'))
        self.screen.blit(lang_label, (self.language_buttons['en'].rect.left, self.language_buttons['en'].rect.top - 30))
        
        # Draw theme label
        # 缁樺埗涓婚鏍囩
        theme_label = title_font.render(i18n.get_bilingual("settings.theme"), True, theme.get_color('text'))
        self.screen.blit(theme_label, (self.theme_buttons['classic'].rect.left, self.theme_buttons['classic'].rect.top - 30))
        
        # Draw buttons
        # 缁樺埗鎸夐挳
        for button in self.language_buttons.values():
            button.draw(self.screen, mouse_pos)
        
        for button in self.theme_buttons.values():
            button.draw(self.screen, mouse_pos)
        
        self.save_button.draw(self.screen, mouse_pos)
        self.cancel_button.draw(self.screen, mouse_pos)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle settings menu events
        澶勭悊璁剧疆鑿滃崟浜嬩欢
        
        Args:
            event: Pygame event (pygame浜嬩欢)
        
        Returns:
            bool: True if settings menu should close (濡傛灉璁剧疆鑿滃崟搴旇鍏抽棴鍒欒繑鍥濼rue)
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                
                # Handle volume slider
                # 澶勭悊闊抽噺婊戝潡
                if self.volume_rect.collidepoint(mouse_pos):
                    self.current_settings['volume'] = (mouse_pos[0] - self.volume_rect.left) / self.volume_rect.width
                    self.current_settings['volume'] = max(0, min(1, self.current_settings['volume']))
                    return False
                
                # Handle language buttons
                # 澶勭悊璇█鎸夐挳
                for lang, button in self.language_buttons.items():
                    if button.rect.collidepoint(mouse_pos):
                        self.current_settings['language'] = lang
                        i18n.set_language(lang)
                        return False
                
                # Handle theme buttons
                # 澶勭悊涓婚鎸夐挳
                for theme_name, button in self.theme_buttons.items():
                    if button.rect.collidepoint(mouse_pos):
                        self.current_settings['theme'] = theme_name
                        theme.set_theme(theme_name)
                        return False
                
                # Handle save/cancel
                # 澶勭悊淇濆瓨/鍙栨秷
                if self.save_button.rect.collidepoint(mouse_pos):
                    self.save_settings()
                    return True
                
                if self.cancel_button.rect.collidepoint(mouse_pos):
                    return True
        
        return False
    
    def save_settings(self):
        """
        Save current settings
        淇濆瓨褰撳墠璁剧疆
        """
        # TODO: Implement settings save
        # TODO: 瀹炵幇璁剧疆淇濆瓨
        pass 
