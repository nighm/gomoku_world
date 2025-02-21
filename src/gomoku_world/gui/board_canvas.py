"""
Board canvas implementation
妫嬬洏鐢诲竷瀹炵幇
"""

import tkinter as tk
from typing import Optional, Tuple

# 浣跨敤鐩稿瀵煎叆
from ..core.game import Game
from ..utils.logger import get_logger

logger = get_logger(__name__)

class BoardCanvas(tk.Canvas):
    """
    Canvas for drawing the game board
    鐢ㄤ簬缁樺埗娓告垙妫嬬洏鐨勭敾甯?
    """
    
    def __init__(self, parent, game: Game):
        """
        Initialize the board canvas
        鍒濆鍖栨鐩樼敾甯?
        
        Args:
            parent: Parent widget
            game: Game instance
        """
        super().__init__(parent, bg='#EEEEEE')
        
        self.game = game
        self.cell_size = 30
        self.margin = 20
        self.piece_radius = 12
        
        # Bind events
        self.bind('<Configure>', self._on_resize)
        self.bind('<Button-1>', self._on_click)
        
        # Initialize board size
        self._resize_board()
        
        logger.info("Board canvas initialized")
    
    def _resize_board(self):
        """
        Resize the board based on canvas size
        鏍规嵁鐢诲竷澶у皬璋冩暣妫嬬洏
        """
        width = self.winfo_width()
        height = self.winfo_height()
        
        # Calculate cell size
        self.cell_size = min(
            (width - 2 * self.margin) // (self.game.board.size - 1),
            (height - 2 * self.margin) // (self.game.board.size - 1)
        )
        
        # Update piece radius
        self.piece_radius = max(4, min(12, self.cell_size // 2 - 2))
        
        self.redraw()
    
    def _on_resize(self, event):
        """
        Handle resize event
        澶勭悊璋冩暣澶у皬浜嬩欢
        
        Args:
            event: Resize event
        """
        self._resize_board()
    
    def _on_click(self, event):
        """
        Handle mouse click event
        澶勭悊榧犳爣鐐瑰嚮浜嬩欢
        
        Args:
            event: Mouse event
        """
        # Convert click coordinates to board position
        x = event.x - self.margin
        y = event.y - self.margin
        
        # Calculate row and column
        row = round(y / self.cell_size)
        col = round(x / self.cell_size)
        
        # Check if click is within valid range
        if 0 <= row < self.game.board.size and 0 <= col < self.game.board.size:
            # Notify parent
            self.event_generate('<<BoardClick>>', 
                              data=str({'row': row, 'col': col}))
    
    def _draw_grid(self):
        """
        Draw the board grid
        缁樺埗妫嬬洏缃戞牸
        """
        # Clear canvas
        self.delete('all')
        
        # Draw background
        width = (self.game.board.size - 1) * self.cell_size + 2 * self.margin
        height = width
        self.configure(width=width, height=height)
        
        # Draw grid lines
        for i in range(self.game.board.size):
            # Vertical lines
            x = i * self.cell_size + self.margin
            self.create_line(
                x, self.margin,
                x, height - self.margin,
                fill='black'
            )
            
            # Horizontal lines
            y = i * self.cell_size + self.margin
            self.create_line(
                self.margin, y,
                width - self.margin, y,
                fill='black'
            )
        
        # Draw star points
        if self.game.board.size >= 13:
            star_points = [
                (3, 3), (3, self.game.board.size-4),
                (self.game.board.size-4, 3),
                (self.game.board.size-4, self.game.board.size-4),
                ((self.game.board.size-1)//2, (self.game.board.size-1)//2)
            ]
            
            for row, col in star_points:
                x = col * self.cell_size + self.margin
                y = row * self.cell_size + self.margin
                self.create_oval(
                    x - 3, y - 3,
                    x + 3, y + 3,
                    fill='black'
                )
    
    def _draw_pieces(self):
        """
        Draw all pieces on the board
        缁樺埗妫嬬洏涓婄殑鎵€鏈夋瀛?
        """
        for row in range(self.game.board.size):
            for col in range(self.game.board.size):
                piece = self.game.board.get_piece(row, col)
                if piece > 0:
                    x = col * self.cell_size + self.margin
                    y = row * self.cell_size + self.margin
                    color = 'black' if piece == 1 else 'white'
                    outline = 'white' if piece == 1 else 'black'
                    
                    self.create_oval(
                        x - self.piece_radius,
                        y - self.piece_radius,
                        x + self.piece_radius,
                        y + self.piece_radius,
                        fill=color,
                        outline=outline
                    )
    
    def redraw(self):
        """
        Redraw the entire board
        閲嶆柊缁樺埗鏁翠釜妫嬬洏
        """
        self._draw_grid()
        self._draw_pieces()
        logger.debug("Board redrawn") 
