"""
Game list window implementation
娓告垙鍒楄〃绐楀彛瀹炵幇
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, List, Optional

from ..config import WINDOW_SIZE
from ..utils.logger import get_logger

logger = get_logger(__name__)

class GameListWindow(tk.Toplevel):
    """
    Window for displaying available games to spectate
    鏄剧ず鍙鎴樻父鎴忕殑绐楀彛
    """
    
    def __init__(self, parent: tk.Tk,
                 on_spectate: Optional[Callable[[str], None]] = None):
        """
        Initialize game list window
        鍒濆鍖栨父鎴忓垪琛ㄧ獥鍙?
        
        Args:
            parent: Parent window
            on_spectate: Callback when spectate button is clicked
        """
        super().__init__(parent)
        
        self.on_spectate = on_spectate
        
        # Window setup
        self.title("Available Games")
        self.geometry(WINDOW_SIZE)
        
        # Create UI components
        self._create_widgets()
        self._setup_layout()
        
        logger.info("Game list window created")
    
    def _create_widgets(self):
        """Create window widgets"""
        # Control buttons
        self.control_frame = ttk.Frame(self)
        self.refresh_btn = ttk.Button(
            self.control_frame,
            text="Refresh",
            command=self._on_refresh
        )
        
        # Game list
        self.list_frame = ttk.Frame(self)
        
        # Create treeview
        self.tree = ttk.Treeview(
            self.list_frame,
            columns=("black", "white", "status", "spectators"),
            show="headings"
        )
        
        # Configure columns
        self.tree.heading("black", text="Black Player")
        self.tree.heading("white", text="White Player")
        self.tree.heading("status", text="Status")
        self.tree.heading("spectators", text="Spectators")
        
        self.tree.column("black", width=150)
        self.tree.column("white", width=150)
        self.tree.column("status", width=100)
        self.tree.column("spectators", width=100)
        
        # Add scrollbar
        self.scrollbar = ttk.Scrollbar(
            self.list_frame,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        # Spectate button
        self.spectate_btn = ttk.Button(
            self,
            text="Spectate",
            command=self._on_spectate,
            state=tk.DISABLED
        )
        
        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
    
    def _setup_layout(self):
        """Setup window layout"""
        # Control frame
        self.control_frame.pack(fill=tk.X, padx=5, pady=5)
        self.refresh_btn.pack(side=tk.RIGHT)
        
        # Game list
        self.list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Spectate button
        self.spectate_btn.pack(fill=tk.X, padx=5, pady=5)
    
    def update_game_list(self, games: List[Dict]):
        """
        Update the game list
        鏇存柊娓告垙鍒楄〃
        
        Args:
            games: List of game information
        """
        try:
            # Clear current items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Add new items
            for game in games:
                self.tree.insert(
                    "",
                    tk.END,
                    values=(
                        game.get("black_player", "-"),
                        game.get("white_player", "-"),
                        game.get("status", "-"),
                        game.get("spectator_count", 0)
                    ),
                    tags=(game.get("id", ""))
                )
            
            logger.debug(f"Updated game list with {len(games)} games")
            
        except Exception as e:
            logger.error(f"Error updating game list: {e}")
    
    def _on_select(self, event):
        """Handle game selection"""
        selected = self.tree.selection()
        self.spectate_btn.configure(
            state=tk.NORMAL if selected else tk.DISABLED
        )
    
    def _on_spectate(self):
        """Handle spectate button click"""
        selected = self.tree.selection()
        if selected and self.on_spectate:
            # Get game ID from item tags
            game_id = self.tree.item(selected[0])["tags"][0]
            self.on_spectate(game_id)
            logger.info(f"Spectate requested for game {game_id}")
    
    def _on_refresh(self):
        """Handle refresh button click"""
        if hasattr(self, "on_refresh"):
            self.on_refresh()
            logger.debug("Game list refresh requested") 
