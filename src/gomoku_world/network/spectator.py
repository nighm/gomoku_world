"""
Spectator management module
瑙傛垬绠＄悊妯″潡
"""

from typing import Dict, Set, Optional
from dataclasses import dataclass

from ..utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class SpectatorInfo:
    """
    Spectator information
    瑙傛垬鑰呬俊鎭?
    """
    id: str
    name: str
    game_id: str

class SpectatorManager:
    """
    Manages game spectators
    绠＄悊娓告垙瑙傛垬鑰?
    """
    
    def __init__(self):
        """Initialize spectator manager"""
        # Map of game_id to set of spectator IDs
        self.game_spectators: Dict[str, Set[str]] = {}
        # Map of spectator_id to SpectatorInfo
        self.spectators: Dict[str, SpectatorInfo] = {}
        logger.info("Spectator manager initialized")
    
    def add_spectator(self, spectator_id: str, name: str, game_id: str) -> bool:
        """
        Add a spectator to a game
        娣诲姞瑙傛垬鑰呭埌娓告垙
        
        Args:
            spectator_id: Spectator ID
            name: Spectator name
            game_id: Game ID
            
        Returns:
            bool: True if successfully added
        """
        try:
            # Create spectator info
            spectator = SpectatorInfo(
                id=spectator_id,
                name=name,
                game_id=game_id
            )
            
            # Add to spectators map
            self.spectators[spectator_id] = spectator
            
            # Add to game spectators set
            if game_id not in self.game_spectators:
                self.game_spectators[game_id] = set()
            self.game_spectators[game_id].add(spectator_id)
            
            logger.info(f"Added spectator {name} to game {game_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding spectator: {e}")
            return False
    
    def remove_spectator(self, spectator_id: str) -> bool:
        """
        Remove a spectator
        绉婚櫎瑙傛垬鑰?
        
        Args:
            spectator_id: Spectator ID
            
        Returns:
            bool: True if successfully removed
        """
        try:
            if spectator_id not in self.spectators:
                return False
                
            spectator = self.spectators[spectator_id]
            game_id = spectator.game_id
            
            # Remove from spectators map
            del self.spectators[spectator_id]
            
            # Remove from game spectators set
            if game_id in self.game_spectators:
                self.game_spectators[game_id].discard(spectator_id)
                if not self.game_spectators[game_id]:
                    del self.game_spectators[game_id]
            
            logger.info(f"Removed spectator {spectator.name} from game {game_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error removing spectator: {e}")
            return False
    
    def get_game_spectators(self, game_id: str) -> Set[str]:
        """
        Get all spectators for a game
        鑾峰彇娓告垙鐨勬墍鏈夎鎴樿€?
        
        Args:
            game_id: Game ID
            
        Returns:
            Set[str]: Set of spectator IDs
        """
        return self.game_spectators.get(game_id, set())
    
    def get_spectator_info(self, spectator_id: str) -> Optional[SpectatorInfo]:
        """
        Get spectator information
        鑾峰彇瑙傛垬鑰呬俊鎭?
        
        Args:
            spectator_id: Spectator ID
            
        Returns:
            Optional[SpectatorInfo]: Spectator information or None if not found
        """
        return self.spectators.get(spectator_id)
    
    def get_spectator_count(self, game_id: str) -> int:
        """
        Get number of spectators for a game
        鑾峰彇娓告垙鐨勮鎴樿€呮暟閲?
        
        Args:
            game_id: Game ID
            
        Returns:
            int: Number of spectators
        """
        return len(self.game_spectators.get(game_id, set()))
    
    def broadcast_to_spectators(self, game_id: str, message: dict,
                              callback) -> None:
        """
        Broadcast message to all spectators of a game
        鍚戞父鎴忕殑鎵€鏈夎鎴樿€呭箍鎾秷鎭?
        
        Args:
            game_id: Game ID
            message: Message to broadcast
            callback: Callback function to send message
        """
        try:
            spectators = self.get_game_spectators(game_id)
            for spectator_id in spectators:
                spectator = self.get_spectator_info(spectator_id)
                if spectator:
                    callback(spectator_id, message)
            
            logger.debug(f"Broadcasted message to {len(spectators)} spectators")
            
        except Exception as e:
            logger.error(f"Error broadcasting to spectators: {e}")
    
    def cleanup_game(self, game_id: str) -> None:
        """
        Clean up spectators when a game ends
        娓告垙缁撴潫鏃舵竻鐞嗚鎴樿€?
        
        Args:
            game_id: Game ID
        """
        try:
            if game_id in self.game_spectators:
                spectators = list(self.game_spectators[game_id])
                for spectator_id in spectators:
                    self.remove_spectator(spectator_id)
                logger.info(f"Cleaned up spectators for game {game_id}")
                
        except Exception as e:
            logger.error(f"Error cleaning up spectators: {e}") 
