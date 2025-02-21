"""
Game client implementation
娓告垙瀹㈡埛绔疄鐜?
"""

import asyncio
import json
import uuid
from typing import Optional, Callable, Dict, List
from dataclasses import dataclass

from ..utils.logger import get_logger
from ..config import DEFAULT_HOST, DEFAULT_PORT, SPECTATOR_UPDATE_INTERVAL

logger = get_logger(__name__)

@dataclass
class GameClient:
    """
    Game client that handles server communication
    澶勭悊鏈嶅姟鍣ㄩ氫俊鐨勬父鎴忓鎴风
    """
    
    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
        """Initialize game client"""
        self.host = host
        self.port = port
        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None
        self.connected = False
        self.player_id = str(uuid.uuid4())
        self.game_id: Optional[str] = None
        self.spectating_game_id: Optional[str] = None
        self.callbacks: Dict[str, Callable] = {}
        self.update_task: Optional[asyncio.Task] = None
        
        logger.info(f"Game client initialized for {host}:{port}")
    
    async def connect(self) -> bool:
        """
        Connect to the game server
        杩炴帴鍒版父鎴忔湇鍔″櫒
        
        Returns:
            bool: True if connection successful
        """
        try:
            self.reader, self.writer = await asyncio.open_connection(
                self.host, 
                self.port
            )
            self.connected = True
            logger.info("Connected to server")
            
            # Start listening for server messages
            asyncio.create_task(self._listen_for_messages())
            
            return True
            
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from the server"""
        if self.connected:
            # Stop spectating if active
            if self.spectating_game_id:
                await self.leave_spectate()
            
            # Cancel update task if running
            if self.update_task:
                self.update_task.cancel()
                
            if self.writer:
                self.writer.close()
                await self.writer.wait_closed()
            self.connected = False
            logger.info("Disconnected from server")
    
    async def list_games(self) -> List[Dict]:
        """
        Get list of available games to spectate
        鑾峰彇鍙鎴樼殑娓告垙鍒楄〃
        
        Returns:
            List[Dict]: List of game information
        """
        response = await self._send_message('list_games', {})
        if response.get('status') == 'ok':
            return response.get('data', {}).get('games', [])
        return []
    
    async def spectate_game(self, game_id: str) -> bool:
        """
        Start spectating a game
        寮濮嬭鎴樻父鎴?
        
        Args:
            game_id: Game ID to spectate
            
        Returns:
            bool: True if successfully started spectating
        """
        if self.spectating_game_id:
            await self.leave_spectate()
            
        response = await self._send_message('spectate_game', {
            'id': self.player_id,
            'game_id': game_id
        })
        
        if response.get('status') == 'ok':
            self.spectating_game_id = game_id
            
            # Start update task
            self.update_task = asyncio.create_task(
                self._spectator_update_loop()
            )
            
            # Emit initial game state
            if 'game_state' in self.callbacks:
                self.callbacks['game_state'](response.get('data', {}))
            
            logger.info(f"Started spectating game {game_id}")
            return True
            
        return False
    
    async def leave_spectate(self) -> bool:
        """
        Stop spectating current game
        鍋滄瑙傛垬褰撳墠娓告垙
        
        Returns:
            bool: True if successfully stopped spectating
        """
        if not self.spectating_game_id:
            return True
            
        response = await self._send_message('leave_spectate', {
            'id': self.player_id
        })
        
        if response.get('status') == 'ok':
            # Cancel update task
            if self.update_task:
                self.update_task.cancel()
                self.update_task = None
            
            self.spectating_game_id = None
            logger.info("Stopped spectating")
            return True
            
        return False
    
    async def send_spectator_chat(self, message: str) -> bool:
        """
        Send chat message while spectating
        鍙戦佽鎴樿亰澶╂秷鎭?
        
        Args:
            message: Chat message
            
        Returns:
            bool: True if message sent successfully
        """
        if not self.spectating_game_id:
            return False
            
        response = await self._send_message('spectator_chat', {
            'id': self.player_id,
            'message': message
        })
        
        return response.get('status') == 'ok'
    
    def on(self, event: str, callback: Callable):
        """
        Register event callback
        娉ㄥ唽浜嬩欢鍥炶皟
        
        Args:
            event: Event name
            callback: Callback function
        """
        self.callbacks[event] = callback
    
    async def _spectator_update_loop(self):
        """Update loop for spectator mode"""
        try:
            while self.spectating_game_id:
                response = await self._send_message('get_game_state', {
                    'game_id': self.spectating_game_id
                })
                
                if response.get('status') == 'ok':
                    if 'game_state' in self.callbacks:
                        self.callbacks['game_state'](response.get('data', {}))
                
                await asyncio.sleep(SPECTATOR_UPDATE_INTERVAL)
                
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Error in spectator update loop: {e}")
    
    async def _send_message(self, cmd: str, data: dict) -> dict:
        """Send message to server"""
        if not self.connected:
            return {'status': 'error', 'message': 'Not connected'}
        
        message = {
            'cmd': cmd,
            'data': data
        }
        
        try:
            self.writer.write(json.dumps(message).encode())
            await self.writer.drain()
            
            response_data = await self.reader.read(1024)
            response = json.loads(response_data.decode())
            
            return response
            
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def _listen_for_messages(self):
        """Listen for server messages"""
        try:
            while self.connected:
                data = await self.reader.read(1024)
                if not data:
                    break
                
                message = json.loads(data.decode())
                event = message.get('event')
                
                if event and event in self.callbacks:
                    self.callbacks[event](message.get('data', {}))
                
        except Exception as e:
            logger.error(f"Error listening for messages: {e}")
        finally:
            await self.disconnect() 
