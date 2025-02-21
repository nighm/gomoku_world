"""
Log display component for the Gomoku game GUI
浜斿瓙妫嬫父鎴廏UI鏃ュ織鏄剧ず缁勪欢
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
        鍒濆鍖栨棩蹇楁樉绀?
        
        Args:
            rect: Display area rectangle (鏄剧ず鍖哄煙鐭╁舰)
        """
        self.rect = rect
        self.lines = []
        self.max_lines = 20  # 澧炲姞鏈澶ф樉绀鸿鏁?
        self.scroll_position = 0  # 婊氬姩浣嶇疆
        self.dragging = False  # 鏄惁姝ｅ湪鎷栧姩婊氬姩鏉?
        self.drag_start_y = 0  # 鎷栧姩寮濮嬬殑y鍧愭爣
        self.drag_start_scroll = 0  # 鎷栧姩寮濮嬫椂鐨勬粴鍔ㄤ綅缃?
        
        self.colors = {
            'default': (0, 0, 0),
            'player': (0, 0, 255),    # 钃濊壊琛ㄧず鐜╁鎿嶄綔
            'ai': (255, 0, 0),        # 绾㈣壊琛ㄧずAI鎿嶄綔
            'system': (0, 128, 0),    # 缁胯壊琛ㄧず绯荤粺娑堟伅
            'warning': (255, 165, 0),  # 姗欒壊琛ㄧず璀﹀憡
            'win': (128, 0, 128),     # 绱壊琛ㄧず鑳滃埄娑堟伅
            'time': (128, 128, 128)   # 鐏拌壊琛ㄧず鏃堕棿鏍囩
        }
        
        try:
            font_path = "C:\\Windows\\Fonts\\simhei.ttf"
            self.font = pygame.font.Font(font_path, 14)
            self.time_font = pygame.font.Font(font_path, 12)  # 鏃堕棿鏍囩浣跨敤灏忎竴鍙峰瓧浣?
        except:
            try:
                font_path = "C:\\Windows\\Fonts\\simsun.ttc"
                self.font = pygame.font.Font(font_path, 14)
                self.time_font = pygame.font.Font(font_path, 12)
            except:
                self.font = pygame.font.Font(None, 14)
                self.time_font = pygame.font.Font(None, 12)
                logger.warning("鏃犳硶鍔犺浇涓枃瀛椾綋锛屼娇鐢ㄧ郴缁熼粯璁ゅ瓧浣?)
    
    def add_line(self, text: str, color_type: str = 'default'):
        """
        Add a new line to the log
        娣诲姞鏂扮殑鏃ュ織琛?
        
        Args:
            text: Log text (鏃ュ織鏂囨湰)
            color_type: Color type for the text (鏂囨湰棰滆壊绫诲瀷)
        """
        time_str = datetime.now().strftime("%H:%M:%S")
        color = self.colors.get(color_type, self.colors['default'])
        self.lines.append((time_str, text, color))
        if len(self.lines) > 1000:  # 闄愬埗鏈澶у瓨鍌ㄨ鏁?
            self.lines.pop(0)
        # 濡傛灉婊氬姩浣嶇疆鍦ㄥ簳閮紝鍒欒窡闅忔柊娑堟伅
        if self.scroll_position >= len(self.lines) - self.get_visible_lines():
            self.scroll_position = max(0, len(self.lines) - self.get_visible_lines())
    
    def get_visible_lines(self) -> int:
        """鑾峰彇鍙琛屾暟"""
        return (self.rect.height - 35) // 20  # 20鏄楂?
    
    def get_scrollbar_rect(self) -> pygame.Rect:
        """鑾峰彇婊氬姩鏉＄煩褰㈠尯鍩?""
        visible_lines = self.get_visible_lines()
        if len(self.lines) <= visible_lines:
            return pygame.Rect(0, 0, 0, 0)
        
        # 璁＄畻婊氬姩鏉￠珮搴﹀拰浣嶇疆
        scrollbar_height = max(30, (visible_lines / len(self.lines)) * (self.rect.height - 35))
        scrollbar_pos = 35 + (self.scroll_position / len(self.lines)) * (self.rect.height - 35 - scrollbar_height)
        return pygame.Rect(self.rect.right - 10, scrollbar_pos, 8, scrollbar_height)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle mouse events for scrolling
        澶勭悊榧犳爣婊氬姩浜嬩欢
        
        Args:
            event: Pygame event
            
        Returns:
            bool: True if event was handled
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # 婊氳疆鍚戜笂
                self.scroll_position = max(0, self.scroll_position - 1)
                return True
            elif event.button == 5:  # 婊氳疆鍚戜笅
                max_scroll = max(0, len(self.lines) - self.get_visible_lines())
                self.scroll_position = min(max_scroll, self.scroll_position + 1)
                return True
            elif event.button == 1:  # 宸﹂敭鐐瑰嚮
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
                # 璁＄畻鎷栧姩璺濈瀵瑰簲鐨勬粴鍔ㄨ鏁?
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
        缁樺埗鏃ュ織鏄剧ず
        
        Args:
            screen: Surface to draw on (缁樺埗琛ㄩ潰)
        """
        # 缁樺埗鑳屾櫙
        background_rect = pygame.Surface((self.rect.width, self.rect.height))
        for y in range(self.rect.height):
            alpha = int(255 * (1 - y / self.rect.height * 0.2))  # 鍒涘缓娓愬彉鏁堟灉
            pygame.draw.line(background_rect, (240, 240, 240, alpha), 
                           (0, y), (self.rect.width, y))
        screen.blit(background_rect, self.rect)
        
        # 缁樺埗杈规
        pygame.draw.rect(screen, (180, 180, 180), self.rect, 1)
        
        # 缁樺埗鏍囬
        title = self.font.render("娓告垙鏃ュ織", True, (100, 100, 100))
        title_rect = title.get_rect(midtop=(self.rect.centerx, self.rect.top + 5))
        screen.blit(title, title_rect)
        
        # 缁樺埗鍒嗛殧绾?
        pygame.draw.line(screen, (180, 180, 180),
                        (self.rect.left + 5, self.rect.top + 25),
                        (self.rect.right - 5, self.rect.top + 25))
        
        # 璁剧疆瑁佸壀鍖哄煙
        clip_rect = pygame.Rect(self.rect.left, self.rect.top + 30,
                              self.rect.width - 12, self.rect.height - 35)
        screen.set_clip(clip_rect)
        
        # 缁樺埗鏃ュ織琛?
        visible_lines = self.get_visible_lines()
        start_index = max(0, min(self.scroll_position, len(self.lines) - visible_lines))
        y = self.rect.top + 30
        
        for time_str, text, color in self.lines[start_index:start_index + visible_lines]:
            # 缁樺埗鏃堕棿鎴?
            time_surface = self.time_font.render(time_str, True, self.colors['time'])
            screen.blit(time_surface, (self.rect.left + 5, y))
            
            # 缁樺埗娑堟伅
            text_surface = self.font.render(text, True, color)
            screen.blit(text_surface, (self.rect.left + 70, y))
            y += 20
        
        # 閲嶇疆瑁佸壀鍖哄煙
        screen.set_clip(None)
        
        # 缁樺埗婊氬姩鏉?
        if len(self.lines) > visible_lines:
            scrollbar_rect = self.get_scrollbar_rect()
            pygame.draw.rect(screen, (200, 200, 200), scrollbar_rect)
            pygame.draw.rect(screen, (180, 180, 180), scrollbar_rect, 1)
    
    def clear(self):
        """Clear all log lines"""
        self.lines.clear()
        self.scroll_position = 0 
