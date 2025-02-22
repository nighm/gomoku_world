"""
Main window implementation for the Gomoku World game
浜斿瓙妫嬩笘鐣屾父鎴忕殑涓荤獥鍙ｅ疄鐜?
"""

import sys
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Tuple, List
import asyncio
import pygame

# 浣跨敤鐩稿瀵煎叆
from ..core.game import Game
from ..utils.logger import get_logger
from ..utils.resources import resource_manager
from ..utils.sound import sound_manager
from .board_canvas import BoardCanvas
from .control_panel import ControlPanel
from .status_bar import StatusBar
from .menu_bar import MenuBar
from .game_list_window import GameListWindow
from .spectator_window import SpectatorWindow
from .widgets.button import Button
from ..i18n import i18n_manager
from ..theme import theme

logger = get_logger(__name__)

class GomokuGUI:
    """
    Main window class for the Gomoku World game
    浜斿瓙妫嬩笘鐣屾父鎴忕殑涓荤獥鍙ｇ被
    """
    
    def __init__(self):
        """
        Initialize the main window
        鍒濆鍖栦富绐楀彛
        """
        self.root = tk.Tk()
        self.root.title(resource_manager.get_text("game.title"))
        self.root.geometry("800x600")
        
        # Initialize game
        self.game = Game()
        
        # Apply theme
        self._apply_theme()
        
        # Create GUI components
        self._create_widgets()
        self._setup_layout()
        
        # Play startup sound
        sound_manager.play("start")
        
        logger.info("Main window initialized")
        
        # Set window title from translations
        self._update_window_title()
        
        # Create UI elements
        self.buttons: List[Button] = [
            Button("button.new_game", 300, 200, callback=self.start_new_game),
            Button("button.settings", 300, 260, callback=self.open_settings),
            Button("button.quit", 300, 320, callback=self.quit_game)
        ]
        
        # Register for language/theme changes
        i18n_manager.add_change_listener(self._on_language_change)
        theme.add_change_listener(self._on_theme_change)
    
    def _apply_theme(self):
        """
        Apply current theme
        搴旂敤褰撳墠涓婚
        """
        theme = resource_manager.get_theme()
        style = ttk.Style()
        
        # Configure ttk styles
        style.configure(".", 
                       background=theme["window"]["background"],
                       foreground=theme["window"]["foreground"])
        
        # Configure root window
        self.root.configure(bg=theme["window"]["background"])
    
    def _create_widgets(self):
        """
        Create all GUI widgets
        鍒涘缓鎵鏈塆UI缁勪欢
        """
        # Create menu bar
        self.menu_bar = MenuBar(self.root, self)
        self.root.config(menu=self.menu_bar)
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        
        # Create board canvas
        self.board_canvas = BoardCanvas(self.main_frame, self.game)
        
        # Create control panel
        self.control_panel = ControlPanel(self.main_frame, self)
        
        # Create status bar
        self.status_bar = StatusBar(self.root)
        
        # Create spectate button
        self.spectate_btn = ttk.Button(
            self.control_panel,
            text="Watch Games",
            command=self._show_game_list
        )
        
        # Initialize game list window
        self.game_list_window = None
        # Initialize spectator windows
        self.spectator_windows = {}
        
        logger.debug("All widgets created")
    
    def _setup_layout(self):
        """
        Setup the layout of all widgets
        璁剧疆鎵鏈夌粍浠剁殑甯冨眬
        """
        # Setup main frame
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        # Setup board canvas
        self.board_canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        # Setup control panel
        self.control_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        
        # Setup spectate button
        self.spectate_btn.pack(fill=tk.X, padx=5, pady=5)
        
        # Setup status bar
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        logger.debug("Layout setup completed")
    
    def new_game(self):
        """
        Start a new game
        寮濮嬫柊娓告垙
        """
        self.game.reset()
        self.board_canvas.redraw()
        self.status_bar.set_message(resource_manager.get_text("game.new_game"))
        sound_manager.play("start")
        logger.info("New game started")
    
    def undo_move(self):
        """
        Undo the last move
        鎾ら攢鏈鍚庝竴姝?
        """
        if self.game.undo_move():
            self.board_canvas.redraw()
            self.status_bar.set_message(resource_manager.get_text("game.undo"))
            sound_manager.play("undo")
            logger.info("Move undone")
        else:
            self.status_bar.set_message("No moves to undo")
            sound_manager.play("invalid")
            logger.warning("Attempted to undo with no moves available")
    
    def handle_click(self, row: int, col: int):
        """
        Handle mouse click on the board
        澶勭悊妫嬬洏涓婄殑榧犳爣鐐瑰嚮
        
        Args:
            row: Row number
            col: Column number
        """
        if self.game.make_move(row, col):
            self.board_canvas.redraw()
            sound_manager.play("place")
            
            if self.game.winner is not None:
                win_text = resource_manager.get_text(
                    "game.black_wins" if self.game.winner == 1 else "game.white_wins"
                )
                self.status_bar.set_message(win_text)
                messagebox.showinfo("Game Over", win_text)
                sound_manager.play("win")
                logger.info(f"Player {self.game.winner} won the game")
            elif self.game.is_draw():
                draw_text = resource_manager.get_text("game.draw")
                self.status_bar.set_message(draw_text)
                messagebox.showinfo("Game Over", draw_text)
                logger.info("Game ended in a draw")
            else:
                turn_text = resource_manager.get_text(
                    "game.black_turn" if self.game.current_player == 1 else "game.white_turn"
                )
                self.status_bar.set_message(turn_text)
        else:
            self.status_bar.set_message("Invalid move!")
            sound_manager.play("invalid")
            logger.warning(f"Invalid move attempted at ({row}, {col})")
    
    def _show_game_list(self):
        """Show game list window"""
        if not self.game_list_window:
            self.game_list_window = GameListWindow(
                self.root,
                on_spectate=self._start_spectating
            )
            self.game_list_window.on_refresh = self._refresh_game_list
            
            # Initial game list update
            asyncio.create_task(self._refresh_game_list())
    
    async def _refresh_game_list(self):
        """Refresh game list"""
        if not self.game_list_window:
            return
            
        try:
            games = await self.client.list_games()
            self.game_list_window.update_game_list(games)
        except Exception as e:
            logger.error(f"Error refreshing game list: {e}")
            messagebox.showerror(
                "Error",
                "Failed to refresh game list"
            )
    
    def _start_spectating(self, game_id: str):
        """Start spectating a game"""
        if game_id in self.spectator_windows:
            self.spectator_windows[game_id].lift()
            return
            
        try:
            # Create spectator window
            window = SpectatorWindow(
                self.root,
                game_id,
                on_close=lambda: self._stop_spectating(game_id)
            )
            
            # Store window reference
            self.spectator_windows[game_id] = window
            
            # Start spectating
            asyncio.create_task(self._connect_spectator(game_id, window))
            
        except Exception as e:
            logger.error(f"Error creating spectator window: {e}")
            messagebox.showerror(
                "Error",
                "Failed to start spectating"
            )
    
    async def _connect_spectator(self, game_id: str, window: SpectatorWindow):
        """Connect spectator to game"""
        try:
            # Start spectating
            if await self.client.spectate_game(game_id):
                # Register event handlers
                self.client.on('game_state', window.update_game_state)
                self.client.on('chat', lambda data: window.add_chat_message(
                    data['sender'],
                    data['message']
                ))
                
                # Register chat callback
                window.on_chat_message = lambda msg: asyncio.create_task(
                    self.client.send_spectator_chat(msg)
                )
                
                logger.info(f"Started spectating game {game_id}")
            else:
                messagebox.showerror(
                    "Error",
                    "Failed to connect to game"
                )
                window.destroy()
                del self.spectator_windows[game_id]
                
        except Exception as e:
            logger.error(f"Error connecting spectator: {e}")
            messagebox.showerror(
                "Error",
                "Failed to connect to game"
            )
            window.destroy()
            del self.spectator_windows[game_id]
    
    def _stop_spectating(self, game_id: str):
        """Stop spectating a game"""
        if game_id in self.spectator_windows:
            # Remove window reference
            del self.spectator_windows[game_id]
            
            # Stop spectating
            asyncio.create_task(self.client.leave_spectate())
            
            logger.info(f"Stopped spectating game {game_id}")
    
    def _update_window_title(self):
        """Update window title when language changes"""
        title = i18n_manager.get_text("app.name")
        self.root.title(title)
        
    def _on_language_change(self):
        """Handle language change"""
        self._update_window_title()
        # Update all button texts
        for button in self.buttons:
            button.update_text()
            
    def _on_theme_change(self):
        """Handle theme change"""
        # Update all button styles
        for button in self.buttons:
            button.update_style()
            
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            # Pass event to all buttons
            for button in self.buttons:
                if button.handle_event(event):
                    break
                    
        return True
        
    def draw(self):
        """Draw window contents"""
        # Clear screen with theme background color
        self.root.configure(bg=theme.get_color("window.background"))
        
        # Draw all buttons
        for button in self.buttons:
            button.draw(self.root)
            
        # Update display
        self.root.update()
        
    def start_new_game(self):
        """Start new game callback"""
        print(i18n_manager.get_text("game.new"))
        
    def open_settings(self):
        """Open settings callback"""
        print(i18n_manager.get_text("menu.settings"))
        
    def quit_game(self):
        """Quit game callback"""
        print(i18n_manager.get_text("game.quit"))
        pygame.quit()
        
    def run(self):
        """
        Start the main event loop
        鍚姩涓讳簨浠跺惊鐜?
        """
        logger.info("Starting main event loop")
        self.root.mainloop()
        
        # Clean up
        sound_manager.cleanup()

    def update_language(self):
        """Update all UI texts when language changes"""
        # Update window title
        self._update_window_title()
        
        # Update menu bar
        self.menu_bar.update_language()
        
        # Update control panel
        self.control_panel.update_language()
        
        # Update status bar
        self.status_bar.update_language()
        
        # Update game list window if open
        if self.game_list_window:
            self.game_list_window.update_language()
            
        # Update spectator windows
        for window in self.spectator_windows.values():
            window.update_language()
            
        # Update current game status
        if self.game.winner is not None:
            win_text = i18n_manager.get_text(
                "game.black_wins" if self.game.winner == 1 else "game.white_wins"
            )
            self.status_bar.set_message(win_text)
        elif self.game.is_draw():
            self.status_bar.set_message(i18n_manager.get_text("game.draw"))
        else:
            turn_text = i18n_manager.get_text(
                "game.black_turn" if self.game.current_player == 1 else "game.white_turn"
            )
            self.status_bar.set_message(turn_text)
            
        logger.info("UI language updated") 
