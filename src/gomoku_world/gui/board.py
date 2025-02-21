"""
Game board component for the Gomoku game GUI
五子棋游戏GUI棋盘组件
"""

import pygame
import logging
from ..theme import theme
from ..game import Game

logger = logging.getLogger(__name__)

class Board:
    """Game board class for drawing and handling board-related operations"""
    
    def __init__(self, window_size: int, game: Game):
        """
        Initialize the game board
        初始化游戏棋盘
        
        Args:
            window_size: Window size in pixels (窗口大小)
            game: Game instance (游戏实例)
        """
        self.window_size = window_size
        self.game = game
        self.grid_size = window_size // (game.size + 1)
        self.last_move = None
        
        # Calculate board boundaries
        margin = self.grid_size
        self.board_rect = pygame.Rect(
            margin - self.grid_size // 2,
            margin - self.grid_size // 2,
            self.grid_size * (game.size + 1),
            self.grid_size * (game.size + 1)
        )
    
    def draw(self, screen: pygame.Surface):
        """
        Draw the game board
        绘制游戏棋盘
        
        Args:
            screen: Surface to draw on (绘制表面)
        """
        # Draw board background
        screen.fill(theme.get_color('background'))
        
        # Draw grid lines
        for i in range(self.game.size):
            # Draw thicker border lines
            line_width = 2 if i == 0 or i == self.game.size - 1 else 1
            
            # Vertical lines
            pygame.draw.line(screen, theme.get_color('grid'),
                           (self.grid_size * (i + 1), self.grid_size),
                           (self.grid_size * (i + 1), self.window_size - self.grid_size),
                           line_width)
            # Horizontal lines
            pygame.draw.line(screen, theme.get_color('grid'),
                           (self.grid_size, self.grid_size * (i + 1)),
                           (self.window_size - self.grid_size, self.grid_size * (i + 1)),
                           line_width)
        
        # Draw star points (天元和星)
        self._draw_star_points(screen)
        
        # Draw pieces
        self._draw_pieces(screen)
        
        # Draw last move highlight
        if self.last_move:
            self._draw_last_move_highlight(screen)
    
    def _draw_star_points(self, screen: pygame.Surface):
        """Draw star points on the board"""
        star_points = []
        if self.game.size == 15:  # 15路棋盘的星位
            star_points = [(3, 3), (3, 7), (3, 11),
                         (7, 3), (7, 7), (7, 11),
                         (11, 3), (11, 7), (11, 11)]
        elif self.game.size == 19:  # 19路棋盘的星位
            star_points = [(3, 3), (3, 9), (3, 15),
                         (9, 3), (9, 9), (9, 15),
                         (15, 3), (15, 9), (15, 15)]
        
        for row, col in star_points:
            # 计算屏幕坐标时保持row和col的顺序一致
            pos = (self.grid_size * (col + 1), self.grid_size * (row + 1))
            # 使用更大的实心圆绘制星位点
            pygame.draw.circle(screen, theme.get_color('grid'), pos, 4, 0)
    
    def _draw_pieces(self, screen: pygame.Surface):
        """Draw game pieces on the board"""
        piece_size = int(self.grid_size * theme.get_size('piece_scale'))
        for i in range(self.game.size):
            for j in range(self.game.size):
                piece = self.game.board[i][j]
                if piece != 0:
                    pos = (self.grid_size * (j + 1), self.grid_size * (i + 1))
                    if piece == 1:  # Black piece
                        pygame.draw.circle(screen, theme.get_color('black_piece'), pos, piece_size)
                    else:  # White piece
                        pygame.draw.circle(screen, theme.get_color('white_piece'), pos, piece_size)
                        pygame.draw.circle(screen, theme.get_color('grid'), pos, piece_size, 1)
    
    def _draw_last_move_highlight(self, screen: pygame.Surface):
        """Draw highlight for the last move"""
        row, col = self.last_move
        pos = (self.grid_size * (col + 1), self.grid_size * (row + 1))
        piece_size = int(self.grid_size * theme.get_size('piece_scale'))
        pygame.draw.circle(screen, theme.get_color('highlight'), pos,
                         int(piece_size * 0.3), 1)
    
    def handle_click(self, pos: tuple) -> tuple:
        """
        Handle mouse click on the board
        处理棋盘上的鼠标点击
        
        Args:
            pos: Mouse position (鼠标位置)
        
        Returns:
            tuple: Board coordinates (row, col) or None
        """
        x, y = pos
        
        # Convert screen coordinates to board coordinates
        # 计算相对于棋盘左上角的偏移
        board_x = x - self.grid_size
        board_y = y - self.grid_size
        
        # 计算最近的交叉点
        col = round(board_x / self.grid_size)
        row = round(board_y / self.grid_size)
        
        # 检查是否在有效范围内
        if 0 <= row < self.game.size and 0 <= col < self.game.size:
            # 检查是否足够接近交叉点
            actual_x = self.grid_size * (col + 1)
            actual_y = self.grid_size * (row + 1)
            
            # 允许一定的误差范围（棋盘格的30%）
            tolerance = self.grid_size * 0.3
            if (abs(x - actual_x) <= tolerance and 
                abs(y - actual_y) <= tolerance):
                return (row, col)
        
        return None
    
    def set_last_move(self, move: tuple):
        """Set the last move for highlighting"""
        self.last_move = move 