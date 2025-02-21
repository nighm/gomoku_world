"""
Save manager implementation
瀛樻。绠＄悊鍣ㄥ疄鐜?
"""

import json
import time
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

from ..config import SAVE_DIR
from ..utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class GameSave:
    """Game save data"""
    id: str
    timestamp: float
    black_player: str
    white_player: str
    moves: List[Dict]
    board_size: int
    game_mode: str
    winner: Optional[int] = None
    metadata: Dict = None

class SaveManager:
    """
    Manages game saves and replays
    绠＄悊娓告垙瀛樻。鍜屽洖鏀?
    """
    
    def __init__(self):
        """Initialize save manager"""
        self.save_dir = SAVE_DIR
        self.save_dir.mkdir(parents=True, exist_ok=True)
        logger.info("Save manager initialized")
    
    def save_game(self, game_data: GameSave) -> bool:
        """
        Save a game
        淇濆瓨娓告垙
        
        Args:
            game_data: Game data to save
            
        Returns:
            bool: True if save successful
        """
        try:
            # Create save file path
            save_path = self.save_dir / f"{game_data.id}_{int(game_data.timestamp)}.json"
            
            # Convert game data to dictionary
            save_dict = asdict(game_data)
            
            # Write to file
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(save_dict, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Game saved to {save_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving game: {e}")
            return False
    
    def load_game(self, save_id: str) -> Optional[GameSave]:
        """
        Load a saved game
        鍔犺浇宸蹭繚瀛樼殑娓告垙
        
        Args:
            save_id: Save file ID
            
        Returns:
            Optional[GameSave]: Loaded game data or None if not found
        """
        try:
            # Find save file
            save_files = list(self.save_dir.glob(f"{save_id}_*.json"))
            if not save_files:
                logger.warning(f"Save file not found: {save_id}")
                return None
            
            save_path = save_files[0]
            
            # Read save file
            with open(save_path, 'r', encoding='utf-8') as f:
                save_dict = json.load(f)
            
            # Convert to GameSave object
            game_save = GameSave(**save_dict)
            
            logger.info(f"Game loaded from {save_path}")
            return game_save
            
        except Exception as e:
            logger.error(f"Error loading game: {e}")
            return None
    
    def list_saves(self) -> List[Dict]:
        """
        List all saved games
        鍒楀嚭鎵€鏈夊凡淇濆瓨鐨勬父鎴?
        
        Returns:
            List[Dict]: List of save info
        """
        try:
            saves = []
            for save_path in self.save_dir.glob("*.json"):
                try:
                    with open(save_path, 'r', encoding='utf-8') as f:
                        save_dict = json.load(f)
                        saves.append({
                            'id': save_dict['id'],
                            'timestamp': save_dict['timestamp'],
                            'black_player': save_dict['black_player'],
                            'white_player': save_dict['white_player'],
                            'winner': save_dict.get('winner'),
                            'moves_count': len(save_dict['moves'])
                        })
                except Exception as e:
                    logger.warning(f"Error reading save file {save_path}: {e}")
            
            # Sort by timestamp descending
            saves.sort(key=lambda x: x['timestamp'], reverse=True)
            return saves
            
        except Exception as e:
            logger.error(f"Error listing saves: {e}")
            return []
    
    def delete_save(self, save_id: str) -> bool:
        """
        Delete a saved game
        鍒犻櫎宸蹭繚瀛樼殑娓告垙
        
        Args:
            save_id: Save file ID
            
        Returns:
            bool: True if deletion successful
        """
        try:
            save_files = list(self.save_dir.glob(f"{save_id}_*.json"))
            if not save_files:
                logger.warning(f"Save file not found: {save_id}")
                return False
            
            save_path = save_files[0]
            save_path.unlink()
            
            logger.info(f"Save file deleted: {save_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting save file: {e}")
            return False
    
    def create_save_data(self, game_id: str, black_player: str, white_player: str,
                        moves: List[Dict], board_size: int, game_mode: str,
                        winner: Optional[int] = None, metadata: Dict = None) -> GameSave:
        """
        Create a new game save data object
        鍒涘缓鏂扮殑娓告垙瀛樻。鏁版嵁瀵硅薄
        
        Args:
            game_id: Game ID
            black_player: Black player name
            white_player: White player name
            moves: List of game moves
            board_size: Board size
            game_mode: Game mode
            winner: Winner player number
            metadata: Additional metadata
            
        Returns:
            GameSave: Created game save data
        """
        return GameSave(
            id=game_id,
            timestamp=time.time(),
            black_player=black_player,
            white_player=white_player,
            moves=moves,
            board_size=board_size,
            game_mode=game_mode,
            winner=winner,
            metadata=metadata or {}
        )
    
    def auto_save(self, game_data: GameSave) -> bool:
        """
        Auto save current game state
        鑷姩淇濆瓨褰撳墠娓告垙鐘舵€?
        
        Args:
            game_data: Current game data
            
        Returns:
            bool: True if auto-save successful
        """
        try:
            # Create auto-save file path
            auto_save_path = self.save_dir / f"autosave_{game_data.id}.json"
            
            # Convert game data to dictionary
            save_dict = asdict(game_data)
            
            # Write to file
            with open(auto_save_path, 'w', encoding='utf-8') as f:
                json.dump(save_dict, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"Game auto-saved to {auto_save_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error auto-saving game: {e}")
            return False
    
    def load_auto_save(self, game_id: str) -> Optional[GameSave]:
        """
        Load auto-saved game
        鍔犺浇鑷姩淇濆瓨鐨勬父鎴?
        
        Args:
            game_id: Game ID
            
        Returns:
            Optional[GameSave]: Loaded game data or None if not found
        """
        try:
            auto_save_path = self.save_dir / f"autosave_{game_id}.json"
            if not auto_save_path.exists():
                return None
            
            # Read auto-save file
            with open(auto_save_path, 'r', encoding='utf-8') as f:
                save_dict = json.load(f)
            
            # Convert to GameSave object
            game_save = GameSave(**save_dict)
            
            logger.info(f"Auto-save loaded from {auto_save_path}")
            return game_save
            
        except Exception as e:
            logger.error(f"Error loading auto-save: {e}")
            return None 
