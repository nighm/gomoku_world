"""
Animation generator for tutorials
教程动画生成器
"""

import os
import pygame
import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional
from ...core.board import Board, Game
from ...theme import theme

class AnimationGenerator:
    """Animation generator for creating tutorial videos"""
    
    def __init__(self, width: int = 1280, height: int = 720, fps: int = 30):
        """
        Initialize animation generator
        
        Args:
            width: Video width
            height: Video height
            fps: Frames per second
        """
        pygame.init()
        self.width = width
        self.height = height
        self.fps = fps
        self.screen = pygame.Surface((width, height))
        self.clock = pygame.time.Clock()
        self.board_size = min(width, height) * 0.8
        self.cell_size = self.board_size / 15
        
    def generate_start_game(self, output_path: str):
        """Generate start game animation"""
        frames = []
        game = Game()
        
        # Menu animation
        for i in range(30):  # 1 second
            surface = pygame.Surface((self.width, self.height))
            surface.fill(pygame.Color(theme.get_color("window.background")))
            
            # Draw menu
            self._draw_menu(surface, i/30)
            frames.append(pygame.surfarray.array3d(surface))
            
        # Game setup animation
        for i in range(30):  # 1 second
            surface = pygame.Surface((self.width, self.height))
            surface.fill(pygame.Color(theme.get_color("window.background")))
            
            # Draw board setup
            self._draw_board_setup(surface, game, i/30)
            frames.append(pygame.surfarray.array3d(surface))
            
        self._save_animation(frames, output_path)
        
    def generate_making_moves(self, output_path: str):
        """Generate making moves animation"""
        frames = []
        game = Game()
        moves = [(7,7), (8,8), (7,8), (6,7)]  # Example moves
        
        # Initial board
        for i in range(15):  # 0.5 seconds
            surface = pygame.Surface((self.width, self.height))
            surface.fill(pygame.Color(theme.get_color("window.background")))
            self._draw_board(surface, game)
            frames.append(pygame.surfarray.array3d(surface))
            
        # Make moves
        for move in moves:
            # Move animation
            for i in range(20):  # ~0.7 seconds per move
                surface = pygame.Surface((self.width, self.height))
                surface.fill(pygame.Color(theme.get_color("window.background")))
                self._draw_board(surface, game)
                self._draw_move_animation(surface, move, i/20)
                frames.append(pygame.surfarray.array3d(surface))
                
            game.make_move(move[0], move[1])
            
            # Show result
            for i in range(10):  # 0.3 seconds pause
                surface = pygame.Surface((self.width, self.height))
                surface.fill(pygame.Color(theme.get_color("window.background")))
                self._draw_board(surface, game)
                frames.append(pygame.surfarray.array3d(surface))
                
        self._save_animation(frames, output_path)
        
    def generate_win_conditions(self, output_path: str):
        """Generate win conditions animation"""
        frames = []
        patterns = [
            [(7,7), (7,8), (7,9), (7,10), (7,11)],  # Horizontal
            [(7,7), (8,7), (9,7), (10,7), (11,7)],  # Vertical
            [(7,7), (8,8), (9,9), (10,10), (11,11)]  # Diagonal
        ]
        
        for pattern in patterns:
            game = Game()
            
            # Show pattern gradually
            for i in range(len(pattern)):
                move = pattern[i]
                game.make_move(move[0], move[1])
                
                # Move animation
                for j in range(20):
                    surface = pygame.Surface((self.width, self.height))
                    surface.fill(pygame.Color(theme.get_color("window.background")))
                    self._draw_board(surface, game)
                    self._draw_win_pattern(surface, pattern[:i+1], j/20)
                    frames.append(pygame.surfarray.array3d(surface))
                    
            # Pause on complete pattern
            for i in range(30):
                surface = pygame.Surface((self.width, self.height))
                surface.fill(pygame.Color(theme.get_color("window.background")))
                self._draw_board(surface, game)
                self._draw_win_pattern(surface, pattern, 1)
                frames.append(pygame.surfarray.array3d(surface))
                
        self._save_animation(frames, output_path)
        
    def generate_ai_game(self, output_path: str):
        """Generate AI game animation"""
        frames = []
        game = Game()
        
        # Show AI difficulty selection
        for i in range(30):  # 1 second
            surface = pygame.Surface((self.width, self.height))
            surface.fill(pygame.Color(theme.get_color("window.background")))
            self._draw_difficulty_selection(surface, i/30)
            frames.append(pygame.surfarray.array3d(surface))
            
        # Show AI thinking and moves
        moves = [(7,7), (8,8), (7,8), (6,7)]  # Example moves
        for move in moves:
            # AI thinking animation
            for i in range(15):  # 0.5 seconds
                surface = pygame.Surface((self.width, self.height))
                surface.fill(pygame.Color(theme.get_color("window.background")))
                self._draw_board(surface, game)
                self._draw_thinking_animation(surface, i/15)
                frames.append(pygame.surfarray.array3d(surface))
                
            # Make move
            game.make_move(move[0], move[1])
            
            # Show move result
            for i in range(15):  # 0.5 seconds
                surface = pygame.Surface((self.width, self.height))
                surface.fill(pygame.Color(theme.get_color("window.background")))
                self._draw_board(surface, game)
                frames.append(pygame.surfarray.array3d(surface))
                
        self._save_animation(frames, output_path)
        
    def generate_theme_switch(self, output_path: str):
        """Generate theme switching animation"""
        frames = []
        game = Game()
        game.make_move(7, 7)  # Add some pieces for demonstration
        game.make_move(8, 8)
        
        themes = [
            {"background": "#FFFFFF", "grid": "#000000", "black": "#000000", "white": "#FFFFFF"},
            {"background": "#DEB887", "grid": "#8B4513", "black": "#000000", "white": "#F0F0F0"},
            {"background": "#4A4A4A", "grid": "#FFFFFF", "black": "#000000", "white": "#FFFFFF"}
        ]
        
        # Show theme transitions
        for theme_data in themes:
            # Fade transition
            for i in range(30):  # 1 second
                surface = pygame.Surface((self.width, self.height))
                surface.fill(pygame.Color(theme_data["background"]))
                self._draw_board_with_theme(surface, game, theme_data, i/30)
                frames.append(pygame.surfarray.array3d(surface))
                
            # Show theme for a while
            for i in range(30):  # 1 second
                surface = pygame.Surface((self.width, self.height))
                surface.fill(pygame.Color(theme_data["background"]))
                self._draw_board_with_theme(surface, game, theme_data, 1)
                frames.append(pygame.surfarray.array3d(surface))
                
        self._save_animation(frames, output_path)
        
    def _draw_menu(self, surface: pygame.Surface, progress: float):
        """Draw menu animation"""
        menu_rect = pygame.Rect(
            self.width * 0.3,
            self.height * 0.3,
            self.width * 0.4,
            self.height * 0.4
        )
        pygame.draw.rect(surface, pygame.Color(theme.get_color("button.background")), menu_rect)
        
    def _draw_board_setup(self, surface: pygame.Surface, game: Game, progress: float):
        """Draw board setup animation"""
        board_rect = self._get_board_rect()
        pygame.draw.rect(surface, pygame.Color(theme.get_color("board.background")), board_rect)
        self._draw_grid(surface, progress)
        
    def _draw_board(self, surface: pygame.Surface, game: Game):
        """Draw game board"""
        board_rect = self._get_board_rect()
        pygame.draw.rect(surface, pygame.Color(theme.get_color("board.background")), board_rect)
        self._draw_grid(surface, 1)
        self._draw_pieces(surface, game)
        
    def _draw_grid(self, surface: pygame.Surface, progress: float):
        """Draw board grid"""
        board_rect = self._get_board_rect()
        lines = int(14 * progress) + 1
        
        for i in range(lines):
            # Vertical lines
            start_pos = (
                board_rect.left + i * self.cell_size,
                board_rect.top
            )
            end_pos = (
                board_rect.left + i * self.cell_size,
                board_rect.bottom
            )
            pygame.draw.line(
                surface,
                pygame.Color(theme.get_color("board.grid_color")),
                start_pos,
                end_pos
            )
            
            # Horizontal lines
            start_pos = (
                board_rect.left,
                board_rect.top + i * self.cell_size
            )
            end_pos = (
                board_rect.right,
                board_rect.top + i * self.cell_size
            )
            pygame.draw.line(
                surface,
                pygame.Color(theme.get_color("board.grid_color")),
                start_pos,
                end_pos
            )
            
    def _draw_pieces(self, surface: pygame.Surface, game: Game):
        """Draw game pieces"""
        board_rect = self._get_board_rect()
        
        for row in range(15):
            for col in range(15):
                if game.board[row, col] != 0:
                    center = (
                        board_rect.left + col * self.cell_size,
                        board_rect.top + row * self.cell_size
                    )
                    color = theme.get_color("board.black_piece") if game.board[row, col] == 1 else theme.get_color("board.white_piece")
                    pygame.draw.circle(
                        surface,
                        pygame.Color(color),
                        center,
                        self.cell_size * 0.4
                    )
                    
    def _draw_move_animation(self, surface: pygame.Surface, move: Tuple[int, int], progress: float):
        """Draw move animation"""
        board_rect = self._get_board_rect()
        center = (
            board_rect.left + move[1] * self.cell_size,
            board_rect.top + move[0] * self.cell_size
        )
        radius = self.cell_size * 0.4 * progress
        pygame.draw.circle(
            surface,
            pygame.Color(theme.get_color("board.black_piece")),
            center,
            radius
        )
        
    def _draw_win_pattern(self, surface: pygame.Surface, pattern: List[Tuple[int, int]], progress: float):
        """Draw win pattern animation"""
        board_rect = self._get_board_rect()
        if len(pattern) > 1:
            points = []
            for move in pattern:
                points.append((
                    board_rect.left + move[1] * self.cell_size,
                    board_rect.top + move[0] * self.cell_size
                ))
            pygame.draw.lines(
                surface,
                pygame.Color(theme.get_color("board.highlight")),
                False,
                points,
                int(self.cell_size * 0.1)
            )
            
    def _draw_difficulty_selection(self, surface: pygame.Surface, progress: float):
        """Draw AI difficulty selection animation"""
        difficulties = ["Easy", "Medium", "Hard"]
        for i, diff in enumerate(difficulties):
            rect = pygame.Rect(
                self.width * 0.3,
                self.height * (0.3 + i * 0.15),
                self.width * 0.4,
                self.height * 0.1
            )
            color = pygame.Color(theme.get_color("button.background"))
            if i == int(progress * 3):
                color = pygame.Color(theme.get_color("button.hover_background"))
            pygame.draw.rect(surface, color, rect)
            
    def _draw_thinking_animation(self, surface: pygame.Surface, progress: float):
        """Draw AI thinking animation"""
        dots = "." * (int(progress * 3) + 1)
        text = f"AI Thinking{dots}"
        # Draw thinking text (placeholder for now)
        
    def _draw_board_with_theme(self, surface: pygame.Surface, game: Game, theme_data: dict, progress: float):
        """Draw board with specific theme"""
        board_rect = self._get_board_rect()
        pygame.draw.rect(surface, pygame.Color(theme_data["background"]), board_rect)
        
        # Draw grid
        for i in range(15):
            # Vertical lines
            start_pos = (board_rect.left + i * self.cell_size, board_rect.top)
            end_pos = (board_rect.left + i * self.cell_size, board_rect.bottom)
            pygame.draw.line(surface, pygame.Color(theme_data["grid"]), start_pos, end_pos)
            
            # Horizontal lines
            start_pos = (board_rect.left, board_rect.top + i * self.cell_size)
            end_pos = (board_rect.right, board_rect.top + i * self.cell_size)
            pygame.draw.line(surface, pygame.Color(theme_data["grid"]), start_pos, end_pos)
            
        # Draw pieces
        for row in range(15):
            for col in range(15):
                if game.board[row, col] != 0:
                    center = (
                        board_rect.left + col * self.cell_size,
                        board_rect.top + row * self.cell_size
                    )
                    color = theme_data["black"] if game.board[row, col] == 1 else theme_data["white"]
                    pygame.draw.circle(
                        surface,
                        pygame.Color(color),
                        center,
                        self.cell_size * 0.4
                    )
        
    def _get_board_rect(self) -> pygame.Rect:
        """Get board rectangle"""
        return pygame.Rect(
            (self.width - self.board_size) / 2,
            (self.height - self.board_size) / 2,
            self.board_size,
            self.board_size
        )
        
    def _save_animation(self, frames: List[np.ndarray], output_path: str):
        """Save animation frames to video file"""
        import cv2
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Convert frames to correct format
        frames = [frame.transpose(1, 0, 2) for frame in frames]  # Swap width and height
        frames = [cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) for frame in frames]  # Convert RGB to BGR
        frames = [frame.astype(np.uint8) for frame in frames]  # Ensure uint8 type
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))
        
        # Write frames
        for frame in frames:
            out.write(frame)
            
        # Release resources
        out.release() 