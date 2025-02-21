"""
Sound management module
澹伴煶绠＄悊妯″潡
"""

import os
from pathlib import Path
from typing import Dict, Optional
import pygame

from ..config import RESOURCES_DIR
from .logger import get_logger

logger = get_logger(__name__)

class SoundManager:
    """
    Manages game sounds and music
    绠＄悊娓告垙闊虫晥鍜岄煶涔?
    """
    
    def __init__(self):
        """Initialize sound manager"""
        # Initialize pygame mixer
        pygame.mixer.init()
        
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.enabled = True
        self.volume = 0.5
        
        # Load default sounds
        self._init_sounds()
        
        logger.info("Sound manager initialized")
    
    def _init_sounds(self):
        """Initialize default sounds"""
        sound_dir = RESOURCES_DIR / "sounds"
        
        # Create default sounds if they don't exist
        self._create_default_sounds()
        
        # Load all sound files
        for sound_file in sound_dir.glob("*.wav"):
            try:
                sound_name = sound_file.stem
                self.sounds[sound_name] = pygame.mixer.Sound(str(sound_file))
                logger.debug(f"Loaded sound: {sound_name}")
            except Exception as e:
                logger.error(f"Error loading sound {sound_file}: {e}")
    
    def _create_default_sounds(self):
        """Create default sound files"""
        # This is a placeholder. In a real implementation,
        # you would include actual sound files in your resources.
        pass
    
    def play(self, sound_name: str):
        """
        Play a sound effect
        鎾斁闊虫晥
        
        Args:
            sound_name: Name of the sound to play
        """
        if not self.enabled:
            return
            
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].set_volume(self.volume)
                self.sounds[sound_name].play()
                logger.debug(f"Playing sound: {sound_name}")
            except Exception as e:
                logger.error(f"Error playing sound {sound_name}: {e}")
        else:
            logger.warning(f"Sound not found: {sound_name}")
    
    def set_enabled(self, enabled: bool):
        """
        Enable or disable sounds
        鍚敤鎴栫鐢ㄥ０闊?
        
        Args:
            enabled: Whether sounds should be enabled
        """
        self.enabled = enabled
        logger.info(f"Sounds {'enabled' if enabled else 'disabled'}")
    
    def set_volume(self, volume: float):
        """
        Set sound volume
        璁剧疆闊抽噺
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.volume = max(0.0, min(1.0, volume))
        logger.info(f"Volume set to: {self.volume}")
    
    def cleanup(self):
        """Clean up resources"""
        pygame.mixer.quit()
        logger.info("Sound manager cleaned up")

# Create global instance
sound_manager = SoundManager() 
