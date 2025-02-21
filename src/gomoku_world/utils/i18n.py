"""
Internationalization module for the Gomoku game.
多语言支持模块
"""

import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class I18n:
    """
    Internationalization class for handling multiple languages
    多语言支持类
    """
    
    def __init__(self, default_lang: str = 'en'):
        """
        Initialize the I18n system
        初始化多语言系统
        
        Args:
            default_lang (str): Default language code (默认语言代码)
        """
        self.current_lang = default_lang
        self.translations: Dict[str, Dict[str, str]] = {
            'en': {
                # Game title and modes
                'game_title': 'Gomoku',
                'pvp_mode': 'Player vs Player',
                'ai_mode_easy': 'Player vs AI (Easy)',
                'ai_mode_medium': 'Player vs AI (Medium)',
                'ai_mode_hard': 'Player vs AI (Hard)',
                'network_mode': 'Online Play',
                'load_game': 'Load Game',
                'settings': 'Settings',
                'quit': 'Quit',
                
                # Game messages
                'black_wins': 'Black wins!',
                'white_wins': 'White wins!',
                'game_draw': 'Game draw!',
                'invalid_move': 'Invalid move!',
                'game_reset': 'Game reset',
                'current_player': 'Current player: {}',
                'your_turn': 'Your turn',
                'ai_thinking': 'AI is thinking...',
                'waiting_opponent': 'Waiting for opponent...',
                
                # Menu items
                'volume': 'Volume: {}%',
                'board_size': 'Board Size: {}x{}',
                'show_coordinates': 'Show Coordinates',
                'highlight_last_move': 'Highlight Last Move',
                'save': 'Save',
                'cancel': 'Cancel',
                'back_to_menu': 'Back to Menu',
                'new_game': 'New Game',
                
                # Network messages
                'connecting': 'Connecting to server...',
                'connection_failed': 'Connection failed',
                'connection_lost': 'Connection lost',
                'room_created': 'Room created: {}',
                'room_joined': 'Joined room: {}',
                'room_full': 'Room is full',
                'player_left': 'Opponent left the game',
                
                # Save/Load messages
                'save_success': 'Game saved',
                'save_failed': 'Failed to save game',
                'load_success': 'Game loaded',
                'load_failed': 'Failed to load game',
                'replay_start': 'Starting replay',
                'replay_end': 'Replay ended',
                
                # Debug messages
                'debug_mode_enabled': 'Debug mode enabled',
                'debug_mode_disabled': 'Debug mode disabled',
                'fps_counter': 'FPS: {}',
                'memory_usage': 'Memory: {:.1f} MB',
                'frame_time': 'Frame Time: {:.1f} ms',
                'mouse_position': 'Mouse: {}',
                'board_position': 'Board: {}',
                'last_move': 'Last Move: {}',
                
                # System messages
                'log_initialized': 'Logging system initialized',
                'session_started': 'New session started',
                'session_ended': 'Session ended',
                'settings_saved': 'Settings saved',
                'sound_volume_changed': 'Sound volume changed to {}%',
                'theme_loaded': 'Theme loaded: {}',
                'theme_not_found': 'Theme not found: {}',
                'font_not_found': 'Font not found: {}',
            },
            'zh': {
                # 游戏标题和模式
                'game_title': '五子棋',
                'pvp_mode': '双人对战',
                'ai_mode_easy': '人机对战（简单）',
                'ai_mode_medium': '人机对战（中等）',
                'ai_mode_hard': '人机对战（困难）',
                'network_mode': '在线对战',
                'load_game': '加载游戏',
                'settings': '设置',
                'quit': '退出',
                
                # 游戏消息
                'black_wins': '黑方获胜！',
                'white_wins': '白方获胜！',
                'game_draw': '游戏平局！',
                'invalid_move': '无效的落子！',
                'game_reset': '游戏重置',
                'current_player': '当前玩家：{}',
                'your_turn': '轮到你了',
                'ai_thinking': 'AI思考中...',
                'waiting_opponent': '等待对手...',
                
                # 菜单项
                'volume': '音量：{}%',
                'board_size': '棋盘大小：{}x{}',
                'show_coordinates': '显示坐标',
                'highlight_last_move': '高亮最后一手',
                'save': '保存',
                'cancel': '取消',
                'back_to_menu': '返回菜单',
                'new_game': '新游戏',
                
                # 网络消息
                'connecting': '正在连接服务器...',
                'connection_failed': '连接失败',
                'connection_lost': '连接断开',
                'room_created': '房间已创建：{}',
                'room_joined': '已加入房间：{}',
                'room_full': '房间已满',
                'player_left': '对手已离开游戏',
                
                # 存档消息
                'save_success': '游戏已保存',
                'save_failed': '保存游戏失败',
                'load_success': '游戏已加载',
                'load_failed': '加载游戏失败',
                'replay_start': '开始回放',
                'replay_end': '回放结束',
                
                # 调试信息
                'debug_mode_enabled': '调试模式已启用',
                'debug_mode_disabled': '调试模式已禁用',
                'fps_counter': '帧率：{}',
                'memory_usage': '内存使用：{:.1f} MB',
                'frame_time': '帧时间：{:.1f} ms',
                'mouse_position': '鼠标位置：{}',
                'board_position': '棋盘位置：{}',
                'last_move': '最后落子：{}',
                
                # 系统消息
                'log_initialized': '日志系统已初始化',
                'session_started': '新会话已开始',
                'session_ended': '会话已结束',
                'settings_saved': '设置已保存',
                'sound_volume_changed': '音量已调整为{}%',
                'theme_loaded': '主题已加载：{}',
                'theme_not_found': '未找到主题：{}',
                'font_not_found': '未找到字体：{}',
            }
        }
        
        logger.info(f"Internationalization system initialized with default language: {default_lang}")
    
    def set_language(self, lang: str):
        """
        Set the current language
        设置当前语言
        
        Args:
            lang (str): Language code (语言代码)
        """
        if lang in self.translations:
            self.current_lang = lang
            logger.info(f"Language changed to: {lang}")
        else:
            logger.warning(f"Language {lang} not supported, using default")
    
    def get(self, key: str, *args) -> str:
        """
        Get a translated string
        获取翻译后的字符串
        
        Args:
            key (str): Translation key (翻译键值)
            *args: Format arguments (格式化参数)
        
        Returns:
            str: Translated string (翻译后的字符串)
        """
        try:
            translation = self.translations[self.current_lang].get(
                key,
                self.translations['en'].get(key, key)
            )
            return translation.format(*args) if args else translation
        except Exception as e:
            logger.error(f"Translation error for key '{key}': {e}")
            return key
    
    def get_all_languages(self) -> list:
        """
        Get list of all supported languages
        获取所有支持的语言列表
        
        Returns:
            list: List of language codes (语言代码列表)
        """
        return list(self.translations.keys())

# Create a global instance
i18n = I18n(default_lang='zh') 