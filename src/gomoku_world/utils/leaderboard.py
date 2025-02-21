"""
Leaderboard implementation
鎺掕姒滃疄鐜?
"""

import json
import time
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

from ..config import RESOURCES_DIR
from .logger import get_logger

logger = get_logger(__name__)

@dataclass
class PlayerStats:
    """Player statistics"""
    id: str
    name: str
    rating: int = 1500
    wins: int = 0
    losses: int = 0
    draws: int = 0
    total_games: int = 0
    win_streak: int = 0
    best_win_streak: int = 0
    last_game: Optional[float] = None
    rank: Optional[int] = None

class LeaderboardManager:
    """
    Manages player rankings and statistics
    绠＄悊鐜╁鎺掑悕鍜岀粺璁?
    """
    
    def __init__(self):
        """Initialize leaderboard manager"""
        self.stats_file = RESOURCES_DIR / "leaderboard" / "stats.json"
        self.stats_file.parent.mkdir(parents=True, exist_ok=True)
        self.players: Dict[str, PlayerStats] = {}
        self._load_stats()
        logger.info("Leaderboard manager initialized")
    
    def _load_stats(self):
        """Load player statistics from file"""
        try:
            if self.stats_file.exists():
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    stats_dict = json.load(f)
                    for player_id, stats in stats_dict.items():
                        self.players[player_id] = PlayerStats(**stats)
                logger.info(f"Loaded stats for {len(self.players)} players")
        except Exception as e:
            logger.error(f"Error loading player stats: {e}")
    
    def _save_stats(self):
        """Save player statistics to file"""
        try:
            stats_dict = {
                player_id: asdict(stats)
                for player_id, stats in self.players.items()
            }
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats_dict, f, indent=2, ensure_ascii=False)
            logger.debug("Player stats saved")
        except Exception as e:
            logger.error(f"Error saving player stats: {e}")
    
    def get_player_stats(self, player_id: str) -> Optional[PlayerStats]:
        """
        Get player statistics
        鑾峰彇鐜╁缁熻淇℃伅
        
        Args:
            player_id: Player ID
            
        Returns:
            Optional[PlayerStats]: Player statistics or None if not found
        """
        return self.players.get(player_id)
    
    def update_player_stats(self, player_id: str, name: str, game_result: str):
        """
        Update player statistics after a game
        鏇存柊鐜╁娓告垙鍚庣殑缁熻淇℃伅
        
        Args:
            player_id: Player ID
            name: Player name
            game_result: Game result (win/loss/draw)
        """
        if player_id not in self.players:
            self.players[player_id] = PlayerStats(id=player_id, name=name)
        
        stats = self.players[player_id]
        stats.total_games += 1
        stats.last_game = time.time()
        
        if game_result == "win":
            stats.wins += 1
            stats.win_streak += 1
            stats.rating += 25
            stats.best_win_streak = max(stats.win_streak, stats.best_win_streak)
        elif game_result == "loss":
            stats.losses += 1
            stats.win_streak = 0
            stats.rating = max(1, stats.rating - 20)
        else:  # draw
            stats.draws += 1
            stats.win_streak = 0
            stats.rating += 5
        
        self._update_rankings()
        self._save_stats()
        logger.info(f"Updated stats for player {name}")
    
    def _update_rankings(self):
        """Update player rankings based on rating"""
        # Sort players by rating
        sorted_players = sorted(
            self.players.values(),
            key=lambda p: (-p.rating, -p.wins, p.total_games)
        )
        
        # Update ranks
        for i, player in enumerate(sorted_players, 1):
            player.rank = i
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """
        Get current leaderboard
        鑾峰彇褰撳墠鎺掕姒?
        
        Args:
            limit: Maximum number of players to return
            
        Returns:
            List[Dict]: List of player rankings
        """
        sorted_players = sorted(
            self.players.values(),
            key=lambda p: (-p.rating, -p.wins, p.total_games)
        )[:limit]
        
        return [
            {
                'rank': i + 1,
                'name': player.name,
                'rating': player.rating,
                'wins': player.wins,
                'losses': player.losses,
                'win_rate': round(player.wins / player.total_games * 100, 1) if player.total_games > 0 else 0,
                'games': player.total_games
            }
            for i, player in enumerate(sorted_players)
        ]
    
    def get_top_players(self, category: str = "rating", limit: int = 10) -> List[Dict]:
        """
        Get top players by category
        鎸夌被鍒幏鍙栭《灏栫帺瀹?
        
        Args:
            category: Ranking category (rating/wins/streak)
            limit: Maximum number of players to return
            
        Returns:
            List[Dict]: List of top players
        """
        if category == "rating":
            key = lambda p: p.rating
        elif category == "wins":
            key = lambda p: p.wins
        elif category == "streak":
            key = lambda p: p.best_win_streak
        else:
            return []
        
        sorted_players = sorted(
            self.players.values(),
            key=key,
            reverse=True
        )[:limit]
        
        return [
            {
                'name': player.name,
                'value': key(player),
                'games': player.total_games
            }
            for player in sorted_players
        ]
    
    def get_active_players(self, days: int = 7) -> List[Dict]:
        """
        Get recently active players
        鑾峰彇鏈€杩戞椿璺冪殑鐜╁
        
        Args:
            days: Number of days to look back
            
        Returns:
            List[Dict]: List of active players
        """
        cutoff = time.time() - (days * 24 * 60 * 60)
        active_players = [
            player for player in self.players.values()
            if player.last_game and player.last_game > cutoff
        ]
        
        return [
            {
                'name': player.name,
                'games': player.total_games,
                'rating': player.rating,
                'last_game': datetime.fromtimestamp(player.last_game).strftime('%Y-%m-%d %H:%M')
            }
            for player in sorted(active_players, key=lambda p: p.last_game, reverse=True)
        ]
    
    def calculate_rating_change(self, player_rating: int, opponent_rating: int,
                              result: str) -> int:
        """
        Calculate rating change after a game
        璁＄畻娓告垙鍚庣殑绛夌骇鍙樺寲
        
        Args:
            player_rating: Player's current rating
            opponent_rating: Opponent's current rating
            result: Game result (win/loss/draw)
            
        Returns:
            int: Rating change
        """
        # Calculate expected score using ELO formula
        expected = 1 / (1 + 10 ** ((opponent_rating - player_rating) / 400))
        
        # Actual score based on result
        actual = 1.0 if result == "win" else 0.0 if result == "loss" else 0.5
        
        # Calculate rating change
        k_factor = 32  # K-factor for rating adjustment
        change = round(k_factor * (actual - expected))
        
        return change 
