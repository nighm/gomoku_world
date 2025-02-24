"""Log display component for the Gomoku game GUI
五子棋游戏GUI日志显示组件
"""

import pygame
import logging
from datetime import datetime
from ..theme import theme

logger = logging.getLogger(__name__)

class LogDisplay:
    """Log display component for showing game messages"""
    
    def __init__(self, rect: pygame.Rect):
        """
        Initialize log display
        初始化日志显示
        
        Args:
            rect: Display area rectangle (显示区域矩形)
        """
        self.rect = rect
        self.lines = []
        self.max_lines = 20  # 增加最大显示行数
        self.scroll_position = 0  # 滚动位置
        self.dragging = False  # 是否正在拖动滚动条
        self.drag_start_y = 0  # 拖动开始的y坐标
        self.drag_start_scroll = 0  # 拖动开始时的滚动位置
        
        self.colors = {
            'default': (0, 0, 0),
            'player': (0, 0, 255),    # 蓝色表示玩家操作
            'ai': (255, 0, 0),        # 红色表示AI操作
            'system': (0, 128, 0),    # 绿色表示系统消息
            'warning': (255, 165, 0),  # 橙色表示警告
            'win': (128, 0, 128),     # 紫色表示胜利消息
            'time': (128, 128, 128)   # 灰色表示时间标签
        }
        
        try:
            font_path = "C:\\Windows\\Fonts\\simhei.ttf"
            self.font = pygame.font.Font(font_path, 14)
            self.time_font = pygame.font.Font(font_path, 12)  # 时间标签使用小一号字体
        except:
            try:
                font_path = "C:\\Windows\\Fonts\\simsun.ttc"
                self.font = pygame.font.Font(font_path, 14)
                self.time_font = pygame.font.Font(font_path, 12)
            except:
                self.font = pygame.font.Font(None, 14)
                self.time_font = pygame.font.Font(None, 12)
                logger.warning("无法加载中文字体，使用系统默认字体")
    
    def add_line(self, text: str, color_type: str = 'default'):
        """
        Add a new line to the log
        添加新的日志行
        
        Args:
            text: Log text (日志文本)
            color_type: Color type for the text (文本颜色类型)
        """
        time_str = datetime.now().strftime("%H:%M:%S")
        color = self.colors.get(color_type, self.colors['default'])
        self.lines.append((time_str, text, color))
        if len(self.lines) > 1000:  # 限制最大存储行数
            self.lines.pop(0)
        # 如果滚动位置在底部，则跟随新消息
        if self.scroll_position >= len(self.lines) - self.get_visible_lines():
            self.scroll_position = max(0, len(self.lines) - self.get_visible_lines())
    
    def get_visible_lines(self) -> int:
        """获取可见行数"""
        return (self.rect.height - 35) // 20  # 20是行高
    
    def get_scrollbar_rect(self) -> pygame.Rect:
        """获取滚动条矩形区域"""
        visible_lines = self.get_visible_lines()
        if len(self.lines) <= visible_lines:
            return pygame.Rect(0, 0, 0, 0)
        
        # 计算滚动条高度和位置
        scrollbar_height = max(30, (visible_lines / len(self.lines)) * (self.rect.height - 35))
        scrollbar_pos = 35 + (self.scroll_position / len(self.lines)) * (self.rect.height - 35 - scrollbar_height)
        return pygame.Rect(self.rect.right - 10, scrollbar_pos, 8, scrollbar_height)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle mouse events for scrolling
        处理鼠标滚动事件
        
        Args:
            event: Pygame event
            
        Returns:
            bool: True if event was handled
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Mouse wheel up
                self.scroll_position = max(0, self.scroll_position - 1)
                return True
            elif event.button == 5:  # Mouse wheel down
                self.scroll_position = min(
                    len(self.lines) - self.get_visible_lines(),
                    self.scroll_position + 1
                )
                return True
            
            # Check if clicked on scrollbar
            scrollbar_rect = self.get_scrollbar_rect()
            if scrollbar_rect.collidepoint(event.pos):
                self.dragging = True
                self.drag_start_y = event.pos[1]
                self.drag_start_scroll = self.scroll_position
                return True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                self.dragging = False
                return True
                
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                # Calculate new scroll position
                delta_y = event.pos[1] - self.drag_start_y
                visible_lines = self.get_visible_lines()
                scroll_range = len(self.lines) - visible_lines
                if scroll_range > 0:
                    scroll_unit = (self.rect.height - 35) / scroll_range
                    delta_scroll = delta_y / scroll_unit
                    self.scroll_position = max(0, min(
                        scroll_range,
                        self.drag_start_scroll + delta_scroll
                    ))
                return True
                
        return False
    
    def draw(self, surface: pygame.Surface):
        """
        Draw the log display
        绘制日志显示
        
        Args:
            surface: Surface to draw on (绘制目标表面)
        """
        # Draw background
        pygame.draw.rect(surface, (240, 240, 240), self.rect)
        pygame.draw.rect(surface, theme.get_color('text'), self.rect, 1)
        
        # Draw visible lines
        visible_lines = self.get_visible_lines()
        start_idx = int(self.scroll_position)
        y = self.rect.top + 5
        
        for i in range(start_idx, min(start_idx + visible_lines, len(self.lines))):
            time_str, text, color = self.lines[i]
            
            # Draw time
            time_surface = self.time_font.render(time_str, True, self.colors['time'])
            surface.blit(time_surface, (self.rect.left + 5, y))
            
            # Draw text
            text_surface = self.font.render(text, True, color)
            surface.blit(text_surface, (self.rect.left + 65, y))
            
            y += 20
        
        # Draw scrollbar if needed
        scrollbar_rect = self.get_scrollbar_rect()
        if scrollbar_rect.width > 0:
            pygame.draw.rect(surface, (180, 180, 180), scrollbar_rect)
