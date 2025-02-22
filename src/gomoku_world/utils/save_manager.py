"""
Save management module for the Gomoku World game.

五子棋世界游戏的存档管理模块。

This module provides game save management functionality:
- Game state saving and loading
- Auto-save functionality
- Save file management
- Save metadata handling
- Save data validation

本模块提供游戏存档管理功能：
- 游戏状态保存和加载
- 自动保存功能
- 存档文件管理
- 存档元数据处理
- 存档数据验证
"""

import json
import time
from pathlib import Path
from typing import List, Dict, Optional, Union
from dataclasses import dataclass, asdict
import shutil

from ..config import SAVE_DIR, AUTO_SAVE_DIR
from .logger import get_logger

logger = get_logger(__name__)

@dataclass
class GameSave:
    """
    Game save data structure.
    
    游戏存档数据结构。
    
    Attributes:
        id (str): Unique save identifier.
                 唯一存档标识符。
        timestamp (float): Save creation time.
                         存档创建时间。
        black_player (str): Black player's name.
                          黑方玩家名称。
        white_player (str): White player's name.
                          白方玩家名称。
        moves (List[Dict]): List of game moves.
                          游戏移动列表。
        board_size (int): Size of the game board.
                        游戏棋盘大小。
        game_mode (str): Game mode (pvp/pvc).
                       游戏模式（pvp/pvc）。
        winner (Optional[int]): Winner of the game (None if not finished).
                              游戏胜者（如果未完成则为None）。
        metadata (Dict): Additional game information.
                       额外的游戏信息。
    """
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
    Save manager for handling game saves and replays.
    
    游戏存档和回放的管理器。
    
    This class manages:
    - Game state persistence
    - Save file operations
    - Auto-save functionality
    - Save data validation
    - Save metadata handling
    
    此类管理：
    - 游戏状态持久化
    - 存档文件操作
    - 自动保存功能
    - 存档数据验证
    - 存档元数据处理
    """
    
    def __init__(self):
        """
        Initialize the save manager.
        
        初始化存档管理器。
        
        Creates required directories:
        - Main save directory
        - Auto-save directory
        - Backup directory
        
        创建所需目录：
        - 主存档目录
        - 自动保存目录
        - 备份目录
        """
        # Create save directories / 创建存档目录
        self.save_dir = SAVE_DIR
        self.auto_save_dir = AUTO_SAVE_DIR
        self.backup_dir = SAVE_DIR / "backups"
        
        for directory in [self.save_dir, self.auto_save_dir, self.backup_dir]:
            directory.mkdir(parents=True, exist_ok=True)
            
        logger.info("Save manager initialized / 存档管理器已初始化")
    
    def save_game(self, game_data: GameSave) -> bool:
        """
        Save a game state.
        
        保存游戏状态。
        
        Args:
            game_data (GameSave): Game data to save.
                                要保存的游戏数据。
                                
        Returns:
            bool: True if save successful, False otherwise.
                 如果保存成功则为True，否则为False。
        """
        try:
            # Create backup of existing save / 创建现有存档的备份
            save_path = self.save_dir / f"{game_data.id}.json"
            if save_path.exists():
                backup_path = self.backup_dir / f"{game_data.id}_{int(time.time())}.json"
                shutil.copy2(save_path, backup_path)
            
            # Save new data / 保存新数据
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(asdict(game_data), f, indent=4, ensure_ascii=False)
                
            logger.info(f"Game saved successfully: {game_data.id} / "
                       f"游戏保存成功：{game_data.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save game {game_data.id}: {e} / "
                        f"保存游戏{game_data.id}失败：{e}")
            return False
    
    def load_game(self, save_id: str) -> Optional[GameSave]:
        """
        Load a saved game.
        
        加载已保存的游戏。
        
        Args:
            save_id (str): ID of the save to load.
                         要加载的存档ID。
                         
        Returns:
            Optional[GameSave]: Loaded game data or None if load fails.
                              加载的游戏数据，如果加载失败则为None。
        """
        try:
            save_path = self.save_dir / f"{save_id}.json"
            if not save_path.exists():
                logger.warning(f"Save file not found: {save_id} / "
                             f"未找到存档文件：{save_id}")
                return None
            
            with open(save_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                game_save = GameSave(**data)
                logger.info(f"Game loaded successfully: {save_id} / "
                           f"游戏加载成功：{save_id}")
                return game_save
                
        except Exception as e:
            logger.error(f"Failed to load game {save_id}: {e} / "
                        f"加载游戏{save_id}失败：{e}")
            return None
    
    def list_saves(self) -> List[Dict]:
        """
        List all available saves.
        
        列出所有可用存档。
        
        Returns:
            List[Dict]: List of save metadata:
                       存档元数据列表：
                       - id: Save identifier / 存档标识符
                       - timestamp: Creation time / 创建时间
                       - black_player: Black player / 黑方玩家
                       - white_player: White player / 白方玩家
                       - game_mode: Game mode / 游戏模式
        """
        saves = []
        try:
            for save_file in self.save_dir.glob("*.json"):
                try:
                    with open(save_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        saves.append({
                            "id": data["id"],
                            "timestamp": data["timestamp"],
                            "black_player": data["black_player"],
                            "white_player": data["white_player"],
                            "game_mode": data["game_mode"]
                        })
                except Exception as e:
                    logger.error(f"Error reading save {save_file}: {e} / "
                               f"读取存档{save_file}出错：{e}")
                    continue
                    
            return sorted(saves, key=lambda x: x["timestamp"], reverse=True)
            
        except Exception as e:
            logger.error(f"Failed to list saves: {e} / 列出存档失败：{e}")
            return []
    
    def delete_save(self, save_id: str) -> bool:
        """
        Delete a save file.
        
        删除存档文件。
        
        Args:
            save_id (str): ID of the save to delete.
                         要删除的存档ID。
                         
        Returns:
            bool: True if deletion successful, False otherwise.
                 如果删除成功则为True，否则为False。
        """
        try:
            save_path = self.save_dir / f"{save_id}.json"
            if not save_path.exists():
                logger.warning(f"Save file not found: {save_id} / "
                             f"未找到存档文件：{save_id}")
                return False
            
            # Move to backup before deletion / 删除前移动到备份
            backup_path = self.backup_dir / f"{save_id}_{int(time.time())}.json"
            shutil.move(save_path, backup_path)
            
            logger.info(f"Save deleted successfully: {save_id} / "
                       f"存档删除成功：{save_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete save {save_id}: {e} / "
                        f"删除存档{save_id}失败：{e}")
            return False
    
    def create_save_data(self, game_id: str, black_player: str, white_player: str,
                        moves: List[Dict], board_size: int, game_mode: str,
                        winner: Optional[int] = None, metadata: Dict = None) -> GameSave:
        """
        Create a new save data object.
        
        创建新的存档数据对象。
        
        Args:
            game_id (str): Unique game identifier.
                         唯一游戏标识符。
            black_player (str): Black player's name.
                             黑方玩家名称。
            white_player (str): White player's name.
                             白方玩家名称。
            moves (List[Dict]): List of game moves.
                             游戏移动列表。
            board_size (int): Size of the game board.
                           游戏棋盘大小。
            game_mode (str): Game mode (pvp/pvc).
                          游戏模式（pvp/pvc）。
            winner (Optional[int]): Winner of the game.
                                 游戏胜者。
            metadata (Dict): Additional game information.
                          额外的游戏信息。
                          
        Returns:
            GameSave: Created save data object.
                     创建的存档数据对象。
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
        Automatically save game state.
        
        自动保存游戏状态。
        
        Args:
            game_data (GameSave): Game data to save.
                                要保存的游戏数据。
                                
        Returns:
            bool: True if auto-save successful, False otherwise.
                 如果自动保存成功则为True，否则为False。
        """
        try:
            auto_save_path = self.auto_save_dir / f"{game_data.id}_auto.json"
            
            # Create backup of existing auto-save / 创建现有自动存档的备份
            if auto_save_path.exists():
                backup_path = self.backup_dir / f"{game_data.id}_auto_{int(time.time())}.json"
                shutil.copy2(auto_save_path, backup_path)
            
            # Save new auto-save / 保存新的自动存档
            with open(auto_save_path, "w", encoding="utf-8") as f:
                json.dump(asdict(game_data), f, indent=4, ensure_ascii=False)
                
            logger.info(f"Auto-save successful: {game_data.id} / "
                       f"自动保存成功：{game_data.id}")
            return True
            
        except Exception as e:
            logger.error(f"Auto-save failed for game {game_data.id}: {e} / "
                        f"游戏{game_data.id}的自动保存失败：{e}")
            return False
    
    def load_auto_save(self, game_id: str) -> Optional[GameSave]:
        """
        Load an auto-saved game.
        
        加载自动保存的游戏。
        
        Args:
            game_id (str): ID of the game to load.
                         要加载的游戏ID。
                         
        Returns:
            Optional[GameSave]: Loaded game data or None if load fails.
                              加载的游戏数据，如果加载失败则为None。
        """
        try:
            auto_save_path = self.auto_save_dir / f"{game_id}_auto.json"
            if not auto_save_path.exists():
                logger.warning(f"Auto-save not found: {game_id} / "
                             f"未找到自动存档：{game_id}")
                return None
            
            with open(auto_save_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                game_save = GameSave(**data)
                logger.info(f"Auto-save loaded successfully: {game_id} / "
                           f"自动存档加载成功：{game_id}")
                return game_save
                
        except Exception as e:
            logger.error(f"Failed to load auto-save {game_id}: {e} / "
                        f"加载自动存档{game_id}失败：{e}")
            return None

# Create global save manager instance / 创建全局存档管理器实例
save_manager = SaveManager()

__all__ = ['save_manager', 'SaveManager', 'GameSave'] 
