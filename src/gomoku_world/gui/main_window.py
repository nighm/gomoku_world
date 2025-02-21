"""
Main window implementation for the Gomoku World game
五子棋世界游戏的主窗口实现
"""

import sys
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Tuple, List
import asyncio

# 使用相对导入
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

logger = get_logger(__name__)

class GomokuGUI:
    """
    Main window class for the Gomoku World game
    五子棋世界游戏的主窗口类
    """
    
    def __init__(self):
        """
        Initialize the main window
        初始化主窗口
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
    
    def _apply_theme(self):
        """
        Apply current theme
        应用当前主题
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
        创建所有GUI组件
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
        设置所有组件的布局
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
        开始新游戏
        """
        self.game.reset()
        self.board_canvas.redraw()
        self.status_bar.set_message(resource_manager.get_text("game.new_game"))
        sound_manager.play("start")
        logger.info("New game started")
    
    def undo_move(self):
        """
        Undo the last move
        撤销最后一步
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
        处理棋盘上的鼠标点击
        
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
    
    def run(self):
        """
        Start the main event loop
        启动主事件循环
        """
        logger.info("Starting main event loop")
        self.root.mainloop()
        
        # Clean up
        sound_manager.cleanup() 