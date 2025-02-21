"""
Spectator window implementation
瑙傛垬绐楀彛瀹炵幇
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, List, Optional
from datetime import datetime

from ..config import (
    WINDOW_SIZE, CELL_SIZE, PIECE_RADIUS,
    SPECTATOR_CHAT_ENABLED, SPECTATOR_CHAT_HISTORY,
    SPECTATOR_FEATURES
)
from ..utils.logger import get_logger
from .board_canvas import BoardCanvas

logger = get_logger(__name__)

class SpectatorWindow(tk.Toplevel):
    """
    Spectator window for watching games
    瑙傛垬绐楀彛鐢ㄤ簬瑙傜湅娓告垙
    """
    
    def __init__(self, parent: tk.Tk, game_id: str,
                 on_close: Optional[Callable] = None):
        """
        Initialize spectator window
        
        Args:
            parent: Parent window
            game_id: Game ID
            on_close: Callback when window is closed
        """
        super().__init__(parent)
        
        self.game_id = game_id
        self.on_close = on_close
        
        # Window setup
        self.title(f"Watching Game - {game_id}")
        self.geometry(WINDOW_SIZE)
        
        # Create UI components
        self._create_widgets()
        self._setup_layout()
        
        # Bind events
        self.protocol("WM_DELETE_WINDOW", self._on_window_close)
        
        logger.info(f"Spectator window created for game {game_id}")
    
    def _create_widgets(self):
        """Create window widgets"""
        # Game board
        self.board_frame = ttk.Frame(self)
        self.board_canvas = BoardCanvas(
            self.board_frame,
            cell_size=CELL_SIZE,
            piece_radius=PIECE_RADIUS
        )
        
        # Game info panel
        self.info_frame = ttk.LabelFrame(self, text="Game Information")
        self.black_label = ttk.Label(self.info_frame, text="Black: -")
        self.white_label = ttk.Label(self.info_frame, text="White: -")
        self.turn_label = ttk.Label(self.info_frame, text="Turn: -")
        self.spectator_count = ttk.Label(self.info_frame, text="Spectators: 0")
        
        # Player stats
        if SPECTATOR_FEATURES["player_stats"]:
            self.stats_frame = ttk.LabelFrame(self, text="Player Statistics")
            self.black_stats = ttk.Label(self.stats_frame, text="")
            self.white_stats = ttk.Label(self.stats_frame, text="")
        
        # Move history
        if SPECTATOR_FEATURES["move_history"]:
            self.history_frame = ttk.LabelFrame(self, text="Move History")
            self.history_text = tk.Text(
                self.history_frame,
                width=30,
                height=10,
                wrap=tk.WORD,
                state=tk.DISABLED
            )
            self.history_scroll = ttk.Scrollbar(
                self.history_frame,
                orient=tk.VERTICAL,
                command=self.history_text.yview
            )
            self.history_text.configure(yscrollcommand=self.history_scroll.set)
        
        # Chat
        if SPECTATOR_FEATURES["chat"] and SPECTATOR_CHAT_ENABLED:
            self.chat_frame = ttk.LabelFrame(self, text="Chat")
            self.chat_text = tk.Text(
                self.chat_frame,
                width=30,
                height=15,
                wrap=tk.WORD,
                state=tk.DISABLED
            )
            self.chat_scroll = ttk.Scrollbar(
                self.chat_frame,
                orient=tk.VERTICAL,
                command=self.chat_text.yview
            )
            self.chat_text.configure(yscrollcommand=self.chat_scroll.set)
            
            self.chat_input_frame = ttk.Frame(self.chat_frame)
            self.chat_entry = ttk.Entry(self.chat_input_frame)
            self.chat_send = ttk.Button(
                self.chat_input_frame,
                text="Send",
                command=self._on_chat_send
            )
    
    def _setup_layout(self):
        """Setup window layout"""
        # Main layout
        self.board_frame.grid(row=0, column=0, rowspan=3, padx=5, pady=5)
        self.board_canvas.pack(expand=True, fill=tk.BOTH)
        
        # Game info
        self.info_frame.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.black_label.pack(anchor="w", padx=5, pady=2)
        self.white_label.pack(anchor="w", padx=5, pady=2)
        self.turn_label.pack(anchor="w", padx=5, pady=2)
        self.spectator_count.pack(anchor="w", padx=5, pady=2)
        
        # Player stats
        if SPECTATOR_FEATURES["player_stats"]:
            self.stats_frame.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
            self.black_stats.pack(anchor="w", padx=5, pady=2)
            self.white_stats.pack(anchor="w", padx=5, pady=2)
        
        # Move history
        if SPECTATOR_FEATURES["move_history"]:
            self.history_frame.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
            self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.history_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Chat
        if SPECTATOR_FEATURES["chat"] and SPECTATOR_CHAT_ENABLED:
            self.chat_frame.grid(
                row=3, column=0, columnspan=2,
                padx=5, pady=5, sticky="ew"
            )
            self.chat_text.pack(fill=tk.BOTH, expand=True)
            self.chat_scroll.pack(side=tk.RIGHT, fill=tk.Y)
            
            self.chat_input_frame.pack(fill=tk.X, padx=5, pady=5)
            self.chat_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.chat_send.pack(side=tk.RIGHT, padx=5)
    
    def update_game_state(self, game_state: Dict):
        """
        Update game state display
        鏇存柊娓告垙鐘舵佹樉绀?
        
        Args:
            game_state: Current game state
        """
        try:
            # Update board
            self.board_canvas.clear_board()
            for move in game_state.get("moves", []):
                self.board_canvas.place_piece(
                    move["x"],
                    move["y"],
                    move["color"]
                )
            
            # Update info
            self.black_label.config(text=f"Black: {game_state.get('black_player', '-')}")
            self.white_label.config(text=f"White: {game_state.get('white_player', '-')}")
            self.turn_label.config(text=f"Turn: {game_state.get('current_turn', '-')}")
            
            # Update spectator count
            count = game_state.get("spectator_count", 0)
            self.spectator_count.config(text=f"Spectators: {count}")
            
            logger.debug("Game state updated in spectator window")
            
        except Exception as e:
            logger.error(f"Error updating game state: {e}")
    
    def update_player_stats(self, black_stats: Dict, white_stats: Dict):
        """
        Update player statistics display
        鏇存柊鐜╁缁熻淇℃伅鏄剧ず
        
        Args:
            black_stats: Black player statistics
            white_stats: White player statistics
        """
        if not SPECTATOR_FEATURES["player_stats"]:
            return
            
        try:
            # Update black player stats
            black_text = (
                f"Rating: {black_stats.get('rating', '-')}\n"
                f"Wins: {black_stats.get('wins', 0)}\n"
                f"Win Rate: {black_stats.get('win_rate', '0')}%"
            )
            self.black_stats.config(text=black_text)
            
            # Update white player stats
            white_text = (
                f"Rating: {white_stats.get('rating', '-')}\n"
                f"Wins: {white_stats.get('wins', 0)}\n"
                f"Win Rate: {white_stats.get('win_rate', '0')}%"
            )
            self.white_stats.config(text=white_text)
            
            logger.debug("Player stats updated in spectator window")
            
        except Exception as e:
            logger.error(f"Error updating player stats: {e}")
    
    def add_move_to_history(self, move: Dict):
        """
        Add move to history display
        娣诲姞绉诲姩鍒板巻鍙茶褰曟樉绀?
        
        Args:
            move: Move information
        """
        if not SPECTATOR_FEATURES["move_history"]:
            return
            
        try:
            # Format move text
            move_text = (
                f"{move.get('player', '-')} placed at "
                f"({move.get('x', '?')}, {move.get('y', '?')})\n"
            )
            
            # Add to history
            self.history_text.configure(state=tk.NORMAL)
            self.history_text.insert(tk.END, move_text)
            self.history_text.see(tk.END)
            self.history_text.configure(state=tk.DISABLED)
            
            logger.debug("Move added to history")
            
        except Exception as e:
            logger.error(f"Error adding move to history: {e}")
    
    def add_chat_message(self, sender: str, message: str):
        """
        Add message to chat display
        娣诲姞娑堟伅鍒拌亰澶╂樉绀?
        
        Args:
            sender: Message sender
            message: Chat message
        """
        if not (SPECTATOR_FEATURES["chat"] and SPECTATOR_CHAT_ENABLED):
            return
            
        try:
            # Format message
            timestamp = datetime.now().strftime("%H:%M")
            chat_text = f"[{timestamp}] {sender}: {message}\n"
            
            # Add to chat
            self.chat_text.configure(state=tk.NORMAL)
            self.chat_text.insert(tk.END, chat_text)
            
            # Limit chat history
            if self.chat_text.index(tk.END) > str(SPECTATOR_CHAT_HISTORY):
                self.chat_text.delete("1.0", "2.0")
            
            self.chat_text.see(tk.END)
            self.chat_text.configure(state=tk.DISABLED)
            
            logger.debug("Chat message added")
            
        except Exception as e:
            logger.error(f"Error adding chat message: {e}")
    
    def _on_chat_send(self):
        """Handle chat send button click"""
        if not (SPECTATOR_FEATURES["chat"] and SPECTATOR_CHAT_ENABLED):
            return
            
        message = self.chat_entry.get().strip()
        if message:
            # Clear input
            self.chat_entry.delete(0, tk.END)
            
            # Emit chat message event
            if hasattr(self, "on_chat_message"):
                self.on_chat_message(message)
    
    def _on_window_close(self):
        """Handle window close event"""
        if self.on_close:
            self.on_close()
        self.destroy()
        logger.info("Spectator window closed") 
