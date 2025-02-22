"""
Network module for online Gomoku gameplay.
浜斿瓙妫嬬綉缁滃鎴樻ā鍧?
"""

import socket
import json
import threading
import logging
import time
from typing import Dict, Optional, Tuple, Callable
from queue import Queue
from ..i18n import i18n_manager as i18n
from .config import config

logger = logging.getLogger(__name__)

class NetworkManager:
    """
    Network manager for handling online gameplay
    缃戠粶瀵规垬绠＄悊鍣?
    """
    
    def __init__(self):
        """Initialize network manager"""
        self.server_address = config.get('network', 'server', 'localhost')
        self.server_port = config.get('network', 'port', 5000)
        self.username = config.get('network', 'username', '')
        
        self.socket: Optional[socket.socket] = None
        self.connected = False
        self.room_id: Optional[str] = None
        self.player_id: Optional[int] = None
        
        # Message queues
        self.send_queue = Queue()
        self.receive_queue = Queue()
        
        # Callback functions
        self.callbacks: Dict[str, Callable] = {}
        
        logger.info(i18n.get('network_initialized'))
    
    def connect(self) -> bool:
        """
        Connect to game server
        杩炴帴鍒版父鎴忔湇鍔″櫒
        
        Returns:
            bool: True if connected successfully
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_address, self.server_port))
            self.connected = True
            
            # Start network threads
            threading.Thread(target=self._receive_loop, daemon=True).start()
            threading.Thread(target=self._send_loop, daemon=True).start()
            
            # Send login message
            self.send_message({
                'type': 'login',
                'username': self.username
            })
            
            logger.info(i18n.get('network_connected'))
            return True
        except Exception as e:
            logger.error(f"Connection error: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """
        Disconnect from game server
        鏂紑涓庢父鎴忔湇鍔″櫒鐨勮繛鎺?
        """
        if self.connected:
            try:
                self.send_message({'type': 'logout'})
                self.socket.close()
            except Exception as e:
                logger.error(f"Disconnect error: {e}")
            finally:
                self.connected = False
                self.socket = None
                logger.info(i18n.get('network_disconnected'))
    
    def create_room(self) -> Optional[str]:
        """
        Create a new game room
        鍒涘缓鏂扮殑娓告垙鎴块棿
        
        Returns:
            str: Room ID if created successfully
        """
        if not self.connected:
            return None
        
        self.send_message({'type': 'create_room'})
        
        # Wait for response
        start_time = time.time()
        while time.time() - start_time < 5:  # 5 second timeout
            if not self.receive_queue.empty():
                msg = self.receive_queue.get()
                if msg.get('type') == 'room_created':
                    self.room_id = msg.get('room_id')
                    self.player_id = 1  # Creator is player 1
                    logger.info(i18n.get('room_created', self.room_id))
                    return self.room_id
        
        logger.error(i18n.get('room_creation_failed'))
        return None
    
    def join_room(self, room_id: str) -> bool:
        """
        Join an existing game room
        鍔犲叆鐜版湁鐨勬父鎴忔埧闂?
        
        Args:
            room_id: Room ID to join (鎴块棿ID)
        
        Returns:
            bool: True if joined successfully
        """
        if not self.connected:
            return False
        
        self.send_message({
            'type': 'join_room',
            'room_id': room_id
        })
        
        # Wait for response
        start_time = time.time()
        while time.time() - start_time < 5:  # 5 second timeout
            if not self.receive_queue.empty():
                msg = self.receive_queue.get()
                if msg.get('type') == 'room_joined':
                    self.room_id = room_id
                    self.player_id = 2  # Joiner is player 2
                    logger.info(i18n.get('room_joined', room_id))
                    return True
                elif msg.get('type') == 'room_join_failed':
                    logger.error(i18n.get('room_join_failed', msg.get('reason', '')))
                    return False
        
        logger.error(i18n.get('room_join_timeout'))
        return False
    
    def leave_room(self):
        """
        Leave current game room
        绂诲紑褰撳墠娓告垙鎴块棿
        """
        if self.room_id:
            self.send_message({'type': 'leave_room'})
            self.room_id = None
            self.player_id = None
            logger.info(i18n.get('room_left'))
    
    def make_move(self, row: int, col: int) -> bool:
        """
        Send a move to the server
        鍚戞湇鍔″櫒鍙戦佽惤瀛愪俊鎭?
        
        Args:
            row: Row number (琛屽彿)
            col: Column number (鍒楀彿)
        
        Returns:
            bool: True if move was sent successfully
        """
        if not (self.connected and self.room_id):
            return False
        
        self.send_message({
            'type': 'move',
            'row': row,
            'col': col
        })
        logger.debug(i18n.get('move_sent', row, col))
        return True
    
    def register_callback(self, event_type: str, callback: Callable):
        """
        Register a callback function for network events
        娉ㄥ唽缃戠粶浜嬩欢鐨勫洖璋冨嚱鏁?
        
        Args:
            event_type: Event type (浜嬩欢绫诲瀷)
            callback: Callback function (鍥炶皟鍑芥暟)
        """
        self.callbacks[event_type] = callback
        logger.debug(i18n.get('callback_registered', event_type))
    
    def send_message(self, message: Dict):
        """
        Send a message to the server
        鍚戞湇鍔″櫒鍙戦佹秷鎭?
        
        Args:
            message: Message to send (瑕佸彂閫佺殑娑堟伅)
        """
        if self.connected:
            self.send_queue.put(message)
    
    def _receive_loop(self):
        """
        Background thread for receiving messages
        鎺ユ敹娑堟伅鐨勫悗鍙扮嚎绋?
        """
        while self.connected:
            try:
                data = self.socket.recv(4096)
                if not data:
                    break
                
                message = json.loads(data.decode())
                msg_type = message.get('type')
                
                # Handle system messages
                if msg_type in ['ping', 'pong']:
                    continue
                
                logger.debug(f"Received: {message}")
                
                # Put message in queue
                self.receive_queue.put(message)
                
                # Call registered callback
                if msg_type in self.callbacks:
                    self.callbacks[msg_type](message)
            except Exception as e:
                logger.error(f"Receive error: {e}")
                break
        
        self.connected = False
        logger.info(i18n.get('network_disconnected'))
    
    def _send_loop(self):
        """
        Background thread for sending messages
        鍙戦佹秷鎭殑鍚庡彴绾跨▼
        """
        while self.connected:
            try:
                message = self.send_queue.get()
                if message:
                    data = json.dumps(message).encode()
                    self.socket.send(data)
                    logger.debug(f"Sent: {message}")
            except Exception as e:
                logger.error(f"Send error: {e}")
                break
        
        self.connected = False

# Create global instance
network = NetworkManager() 
