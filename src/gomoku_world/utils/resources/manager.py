"""
Resource manager implementation
璧勬簮绠＄悊鍣ㄥ疄鐜?
""" 

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

from ..logger import get_logger

logger = get_logger(__name__)

class ResourceManager:
    """
    Resource manager class for handling game resources
    """
    
    def __init__(self):
        """Initialize resource manager"""
        self._resources: Dict[str, Any] = {}
        self._theme = {
            "window": {
                "background": "#FFFFFF",
                "foreground": "#000000"
            }
        }
        self._texts = {
            "game.title": "Gomoku World",
            "game.new_game": "New game started",
            "game.black_wins": "Black wins!",
            "game.white_wins": "White wins!",
            "game.draw": "Game is a draw!",
            "game.black_turn": "Black's turn",
            "game.white_turn": "White's turn",
            "game.undo": "Move undone"
        }
        logger.info("Resource manager initialized")
    
    def get_theme(self) -> Dict[str, Any]:
        """
        Get current theme
        
        Returns:
            Dict[str, Any]: Theme settings
        """
        return self._theme
    
    def get_text(self, key: str) -> str:
        """
        Get text by key
        
        Args:
            key: Text key
            
        Returns:
            str: Text value
        """
        return self._texts.get(key, key)
    
    def load_resources(self, resource_dir: Optional[Path] = None):
        """
        Load resources from directory
        
        Args:
            resource_dir: Resource directory path
        """
        if resource_dir is None:
            resource_dir = Path(__file__).parent.parent.parent.parent / "resources"
            
        if not resource_dir.exists():
            logger.warning(f"Resource directory {resource_dir} does not exist")
            return
            
        # Load theme
        theme_file = resource_dir / "theme.json"
        if theme_file.exists():
            try:
                with open(theme_file, "r", encoding="utf-8") as f:
                    self._theme.update(json.load(f))
                logger.info("Theme loaded")
            except Exception as e:
                logger.error(f"Failed to load theme: {e}")
                
        # Load texts
        texts_file = resource_dir / "texts.json"
        if texts_file.exists():
            try:
                with open(texts_file, "r", encoding="utf-8") as f:
                    self._texts.update(json.load(f))
                logger.info("Texts loaded")
            except Exception as e:
                logger.error(f"Failed to load texts: {e}")
                
        logger.info("Resources loaded") 