"""
Log display component for the Gomoku game GUI
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
            if event.button == 4:  # 滚轮向上
                self.scroll_position = max(0, self.scroll_position - 1)
                return True
            elif event.button == 5:  # 滚轮向下
                max_scroll = max(0, len(self.lines) - self.get_visible_lines())
                self.scroll_position = min(max_scroll, self.scroll_position + 1)
                return True
            elif event.button == 1:  # 左键点击
                scrollbar_rect = self.get_scrollbar_rect()
                if scrollbar_rect.collidepoint(event.pos):
                    self.dragging = True
                    self.drag_start_y = event.pos[1]
                    self.drag_start_scroll = self.scroll_position
                    return True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
                return True
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                # 计算拖动距离对应的滚动行数
                drag_distance = event.pos[1] - self.drag_start_y
                visible_area_height = self.rect.height - 35
                scroll_range = max(0, len(self.lines) - self.get_visible_lines())
                self.scroll_position = max(0, min(scroll_range,
                    self.drag_start_scroll + int(drag_distance * scroll_range / visible_area_height)))
                return True
        return False
    
    def draw(self, screen: pygame.Surface):
        """
        Draw the log display
        绘制日志显示
        
        Args:
            screen: Surface to draw on (绘制表面)
        """
        # 绘制背景
        background_rect = pygame.Surface((self.rect.width, self.rect.height))
        for y in range(self.rect.height):
            alpha = int(255 * (1 - y / self.rect.height * 0.2))  # 创建渐变效果
            pygame.draw.line(background_rect, (240, 240, 240, alpha), 
                           (0, y), (self.rect.width, y))
        screen.blit(background_rect, self.rect)
        
        # 绘制边框
        pygame.draw.rect(screen, (180, 180, 180), self.rect, 1)
        
        # 绘制标题
        title = self.font.render("游戏日志", True, (100, 100, 100))
        title_rect = title.get_rect(midtop=(self.rect.centerx, self.rect.top + 5))
        screen.blit(title, title_rect)
        
        # 绘制分隔线
        pygame.draw.line(screen, (180, 180, 180),
                        (self.rect.left + 5, self.rect.top + 25),
                        (self.rect.right - 5, self.rect.top + 25))
        
        # 设置裁剪区域
        clip_rect = pygame.Rect(self.rect.left, self.rect.top + 30,
                              self.rect.width - 12, self.rect.height - 35)
        screen.set_clip(clip_rect)
        
        # 绘制日志行
        visible_lines = self.get_visible_lines()
        start_index = max(0, min(self.scroll_position, len(self.lines) - visible_lines))
        y = self.rect.top + 30
        
        for time_str, text, color in self.lines[start_index:start_index + visible_lines]:
            # 绘制时间戳
            time_surface = self.time_font.render(time_str, True, self.colors['time'])
            screen.blit(time_surface, (self.rect.left + 5, y))
            
            # 绘制消息
            text_surface = self.font.render(text, True, color)
            screen.blit(text_surface, (self.rect.left + 70, y))
            y += 20
        
        # 重置裁剪区域
        screen.set_clip(None)
        
        # 绘制滚动条
        if len(self.lines) > visible_lines:
            scrollbar_rect = self.get_scrollbar_rect()
            pygame.draw.rect(screen, (200, 200, 200), scrollbar_rect)
            pygame.draw.rect(screen, (180, 180, 180), scrollbar_rect, 1)
    
    def clear(self):
        """Clear all log lines"""
        self.lines.clear()
        self.scroll_position = 0 