"""
Internationalization module for the Gomoku game.
澶氳瑷€鏀寔妯″潡
"""

import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class I18n:
    """
    Internationalization class for handling multiple languages
    澶氳瑷€鏀寔绫?
    """
    
    def __init__(self, default_lang: str = 'en'):
        """
        Initialize the I18n system
        鍒濆鍖栧璇█绯荤粺
        
        Args:
            default_lang (str): Default language code (榛樿璇█浠ｇ爜)
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
                # 娓告垙鏍囬鍜屾ā寮?
                'game_title': '浜斿瓙妫?,
                'pvp_mode': '鍙屼汉瀵规垬',
                'ai_mode_easy': '浜烘満瀵规垬锛堢畝鍗曪級',
                'ai_mode_medium': '浜烘満瀵规垬锛堜腑绛夛級',
                'ai_mode_hard': '浜烘満瀵规垬锛堝洶闅撅級',
                'network_mode': '鍦ㄧ嚎瀵规垬',
                'load_game': '鍔犺浇娓告垙',
                'settings': '璁剧疆',
                'quit': '閫€鍑?,
                
                # 娓告垙娑堟伅
                'black_wins': '榛戞柟鑾疯儨锛?,
                'white_wins': '鐧芥柟鑾疯儨锛?,
                'game_draw': '娓告垙骞冲眬锛?,
                'invalid_move': '鏃犳晥鐨勮惤瀛愶紒',
                'game_reset': '娓告垙閲嶇疆',
                'current_player': '褰撳墠鐜╁锛歿}',
                'your_turn': '杞埌浣犱簡',
                'ai_thinking': 'AI鎬濊€冧腑...',
                'waiting_opponent': '绛夊緟瀵规墜...',
                
                # 鑿滃崟椤?
                'volume': '闊抽噺锛歿}%',
                'board_size': '妫嬬洏澶у皬锛歿}x{}',
                'show_coordinates': '鏄剧ず鍧愭爣',
                'highlight_last_move': '楂樹寒鏈€鍚庝竴鎵?,
                'save': '淇濆瓨',
                'cancel': '鍙栨秷',
                'back_to_menu': '杩斿洖鑿滃崟',
                'new_game': '鏂版父鎴?,
                
                # 缃戠粶娑堟伅
                'connecting': '姝ｅ湪杩炴帴鏈嶅姟鍣?..',
                'connection_failed': '杩炴帴澶辫触',
                'connection_lost': '杩炴帴鏂紑',
                'room_created': '鎴块棿宸插垱寤猴細{}',
                'room_joined': '宸插姞鍏ユ埧闂达細{}',
                'room_full': '鎴块棿宸叉弧',
                'player_left': '瀵规墜宸茬寮€娓告垙',
                
                # 瀛樻。娑堟伅
                'save_success': '娓告垙宸蹭繚瀛?,
                'save_failed': '淇濆瓨娓告垙澶辫触',
                'load_success': '娓告垙宸插姞杞?,
                'load_failed': '鍔犺浇娓告垙澶辫触',
                'replay_start': '寮€濮嬪洖鏀?,
                'replay_end': '鍥炴斁缁撴潫',
                
                # 璋冭瘯淇℃伅
                'debug_mode_enabled': '璋冭瘯妯″紡宸插惎鐢?,
                'debug_mode_disabled': '璋冭瘯妯″紡宸茬鐢?,
                'fps_counter': '甯х巼锛歿}',
                'memory_usage': '鍐呭瓨浣跨敤锛歿:.1f} MB',
                'frame_time': '甯ф椂闂达細{:.1f} ms',
                'mouse_position': '榧犳爣浣嶇疆锛歿}',
                'board_position': '妫嬬洏浣嶇疆锛歿}',
                'last_move': '鏈€鍚庤惤瀛愶細{}',
                
                # 绯荤粺娑堟伅
                'log_initialized': '鏃ュ織绯荤粺宸插垵濮嬪寲',
                'session_started': '鏂颁細璇濆凡寮€濮?,
                'session_ended': '浼氳瘽宸茬粨鏉?,
                'settings_saved': '璁剧疆宸蹭繚瀛?,
                'sound_volume_changed': '闊抽噺宸茶皟鏁翠负{}%',
                'theme_loaded': '涓婚宸插姞杞斤細{}',
                'theme_not_found': '鏈壘鍒颁富棰橈細{}',
                'font_not_found': '鏈壘鍒板瓧浣擄細{}',
            }
        }
        
        logger.info(f"Internationalization system initialized with default language: {default_lang}")
    
    def set_language(self, lang: str):
        """
        Set the current language
        璁剧疆褰撳墠璇█
        
        Args:
            lang (str): Language code (璇█浠ｇ爜)
        """
        if lang in self.translations:
            self.current_lang = lang
            logger.info(f"Language changed to: {lang}")
        else:
            logger.warning(f"Language {lang} not supported, using default")
    
    def get(self, key: str, *args) -> str:
        """
        Get a translated string
        鑾峰彇缈昏瘧鍚庣殑瀛楃涓?
        
        Args:
            key (str): Translation key (缈昏瘧閿€?
            *args: Format arguments (鏍煎紡鍖栧弬鏁?
        
        Returns:
            str: Translated string (缈昏瘧鍚庣殑瀛楃涓?
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
        鑾峰彇鎵€鏈夋敮鎸佺殑璇█鍒楄〃
        
        Returns:
            list: List of language codes (璇█浠ｇ爜鍒楄〃)
        """
        return list(self.translations.keys())

# Create a global instance
i18n = I18n(default_lang='zh') 
