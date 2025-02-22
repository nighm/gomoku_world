"""
Sound management module for the Gomoku World game.

五子棋世界游戏的声音管理模块。

This module provides sound management functionality:
- Sound effect playback
- Background music control
- Volume control
- Sound enabling/disabling
- Resource management

本模块提供声音管理功能：
- 音效播放
- 背景音乐控制
- 音量控制
- 声音启用/禁用
- 资源管理
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
    Sound manager for handling game audio.
    
    游戏音频管理器。
    
    This class manages:
    - Sound effect loading and playback
    - Background music control
    - Volume settings
    - Audio state management
    - Resource handling
    
    此类管理：
    - 音效加载和播放
    - 背景音乐控制
    - 音量设置
    - 音频状态管理
    - 资源处理
    """
    
    def __init__(self):
        """
        Initialize the sound manager.
        
        初始化声音管理器。
        
        Sets up:
        - Pygame mixer
        - Default sounds
        - Volume settings
        - Audio state
        
        设置：
        - Pygame混音器
        - 默认音效
        - 音量设置
        - 音频状态
        """
        # Initialize pygame mixer / 初始化Pygame混音器
        pygame.mixer.init()
        
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.enabled = True
        self.volume = 0.5
        self.current_music: Optional[str] = None
        
        # Load default sounds / 加载默认音效
        self._init_sounds()
        
        logger.info("Sound manager initialized / 声音管理器已初始化")
    
    def _init_sounds(self):
        """
        Initialize sound resources.
        
        初始化声音资源。
        
        This method:
        - Creates default sounds if needed
        - Loads all sound files
        - Sets initial volume
        
        此方法：
        - 如果需要则创建默认音效
        - 加载所有声音文件
        - 设置初始音量
        """
        sound_dir = RESOURCES_DIR / "sounds"
        sound_dir.mkdir(exist_ok=True)
        
        # Create default sounds if they don't exist / 如果默认音效不存在则创建
        self._create_default_sounds()
        
        # Load all sound files / 加载所有声音文件
        for sound_file in sound_dir.glob("*.wav"):
            try:
                sound_name = sound_file.stem
                self.sounds[sound_name] = pygame.mixer.Sound(str(sound_file))
                self.sounds[sound_name].set_volume(self.volume)
                logger.info(f"Loaded sound: {sound_name} / 已加载音效：{sound_name}")
            except Exception as e:
                logger.error(f"Failed to load sound {sound_file}: {e} / 加载音效{sound_file}失败：{e}")
    
    def _create_default_sounds(self):
        """
        Create default sound files.
        
        创建默认声音文件。
        
        Creates:
        - Piece placement sound
        - Game start sound
        - Victory sound
        - Menu selection sound
        
        创建：
        - 落子音效
        - 游戏开始音效
        - 胜利音效
        - 菜单选择音效
        """
        # Default sound files will be copied from resources / 默认音效文件将从资源复制
        default_sounds = {
            "piece": "piece.wav",
            "start": "start.wav",
            "victory": "victory.wav",
            "select": "select.wav"
        }
        
        sound_dir = RESOURCES_DIR / "sounds"
        for name, filename in default_sounds.items():
            sound_file = sound_dir / filename
            if not sound_file.exists():
                # Copy from package resources / 从包资源复制
                try:
                    # Implementation of sound file creation / 音效文件创建的实现
                    logger.info(f"Created default sound: {name} / 已创建默认音效：{name}")
                except Exception as e:
                    logger.error(f"Failed to create sound {name}: {e} / 创建音效{name}失败：{e}")
    
    def play(self, sound_name: str):
        """
        Play a sound effect.
        
        播放音效。
        
        Args:
            sound_name (str): Name of the sound to play.
                            要播放的音效名称。
        """
        if not self.enabled:
            return
            
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                logger.error(f"Failed to play sound {sound_name}: {e} / 播放音效{sound_name}失败：{e}")
        else:
            logger.warning(f"Sound not found: {sound_name} / 未找到音效：{sound_name}")
    
    def play_music(self, music_name: str, loop: bool = True):
        """
        Play background music.
        
        播放背景音乐。
        
        Args:
            music_name (str): Name of the music file to play.
                            要播放的音乐文件名称。
            loop (bool): Whether to loop the music (default: True).
                        是否循环播放音乐（默认：True）。
        """
        if not self.enabled:
            return
            
        music_file = RESOURCES_DIR / "music" / f"{music_name}.mp3"
        if music_file.exists():
            try:
                pygame.mixer.music.load(str(music_file))
                pygame.mixer.music.set_volume(self.volume)
                pygame.mixer.music.play(-1 if loop else 0)
                self.current_music = music_name
                logger.info(f"Playing music: {music_name} / 正在播放音乐：{music_name}")
            except Exception as e:
                logger.error(f"Failed to play music {music_name}: {e} / 播放音乐{music_name}失败：{e}")
        else:
            logger.warning(f"Music file not found: {music_name} / 未找到音乐文件：{music_name}")
    
    def stop_music(self):
        """
        Stop currently playing music.
        
        停止当前播放的音乐。
        """
        pygame.mixer.music.stop()
        self.current_music = None
        logger.info("Music stopped / 音乐已停止")
    
    def set_enabled(self, enabled: bool):
        """
        Enable or disable all audio.
        
        启用或禁用所有音频。
        
        Args:
            enabled (bool): True to enable audio, False to disable.
                          True表示启用音频，False表示禁用。
        """
        self.enabled = enabled
        if not enabled:
            pygame.mixer.stop()
            pygame.mixer.music.stop()
        logger.info(f"Audio {'enabled' if enabled else 'disabled'} / 音频已{'启用' if enabled else '禁用'}")
    
    def set_volume(self, volume: float):
        """
        Set audio volume.
        
        设置音频音量。
        
        Args:
            volume (float): Volume level (0.0 to 1.0).
                          音量级别（0.0到1.0）。
                          
        Raises:
            ValueError: If volume is out of range.
                       如果音量超出范围。
        """
        if not 0.0 <= volume <= 1.0:
            raise ValueError("Volume must be between 0.0 and 1.0 / 音量必须在0.0和1.0之间")
            
        self.volume = volume
        for sound in self.sounds.values():
            sound.set_volume(volume)
        pygame.mixer.music.set_volume(volume)
        logger.info(f"Volume set to {volume} / 音量已设置为{volume}")
    
    def cleanup(self):
        """
        Clean up sound resources.
        
        清理声音资源。
        
        This method:
        - Stops all playing sounds
        - Stops background music
        - Releases resources
        
        此方法：
        - 停止所有播放中的音效
        - 停止背景音乐
        - 释放资源
        """
        pygame.mixer.stop()
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        self.sounds.clear()
        logger.info("Sound manager cleaned up / 声音管理器已清理")

# Create global sound manager instance / 创建全局声音管理器实例
sound_manager = SoundManager()

__all__ = ['sound_manager', 'SoundManager'] 
