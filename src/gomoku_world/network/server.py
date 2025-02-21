"""
Game server implementation
娓告垙鏈嶅姟鍣ㄥ疄鐜?
"""

import asyncio
import json
from typing import Dict, Set, Optional
from dataclasses import dataclass, asdict

from ..utils.logger import get_logger
from ..config import (
    DEFAULT_HOST, DEFAULT_PORT,
    MAX_SPECTATORS_PER_GAME,
    SPECTATOR_UPDATE_INTERVAL
)
from .spectator import SpectatorManager

logger = get_logger(__name__)

@dataclass
class Player:
    """Player information"""
    id: str
    name: str
    rating: int = 1500
    is_ready: bool = False
    game_id: Optional[str] = None

@dataclass
class Game:
    """Game session information"""
    id: str
    black_player: str
    white_player: str
    moves: list
    status: str = "waiting"  # waiting/playing/finished
    spectator_count: int = 0

class GameServer:
    """
    Game server that handles multiple game sessions
    澶勭悊澶氫釜娓告垙浼氳瘽鐨勬父鎴忔湇鍔″櫒
    """
    
    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
        """Initialize game server"""
        self.host = host
        self.port = port
        self.players: Dict[str, Player] = {}
        self.games: Dict[str, Game] = {}
        self.waiting_players: Set[str] = set()
        
        # Initialize spectator manager
        self.spectator_manager = SpectatorManager()
        
        logger.info(f"Game server initialized on {host}:{port}")
    
    async def start(self):
        """Start the server"""
        server = await asyncio.start_server(
            self._handle_client,
            self.host,
            self.port
        )
        
        logger.info(f"Server running on {self.host}:{self.port}")
        
        async with server:
            await server.serve_forever()
    
    async def _handle_client(self, reader: asyncio.StreamReader, 
                           writer: asyncio.StreamWriter):
        """Handle client connection"""
        addr = writer.get_extra_info('peername')
        logger.info(f"New connection from {addr}")
        
        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                
                message = json.loads(data.decode())
                response = await self._process_message(message)
                
                writer.write(json.dumps(response).encode())
                await writer.drain()
                
        except Exception as e:
            logger.error(f"Error handling client {addr}: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
            logger.info(f"Connection closed for {addr}")
    
    async def _process_message(self, message: dict) -> dict:
        """Process client message"""
        cmd = message.get('cmd')
        data = message.get('data', {})
        
        handlers = {
            'login': self._handle_login,
            'logout': self._handle_logout,
            'find_game': self._handle_find_game,
            'make_move': self._handle_make_move,
            'cancel_match': self._handle_cancel_match,
            'get_status': self._handle_get_status,
            # Add spectator handlers
            'list_games': self._handle_list_games,
            'spectate_game': self._handle_spectate_game,
            'leave_spectate': self._handle_leave_spectate,
            'spectator_chat': self._handle_spectator_chat
        }
        
        handler = handlers.get(cmd)
        if handler:
            try:
                return await handler(data)
            except Exception as e:
                logger.error(f"Error processing {cmd}: {e}")
                return {'status': 'error', 'message': str(e)}
        else:
            return {'status': 'error', 'message': 'Unknown command'}
    
    async def _handle_login(self, data: dict) -> dict:
        """Handle player login"""
        player_id = data.get('id')
        name = data.get('name')
        
        if not player_id or not name:
            return {'status': 'error', 'message': 'Invalid login data'}
        
        if player_id in self.players:
            return {'status': 'error', 'message': 'Player already logged in'}
        
        player = Player(id=player_id, name=name)
        self.players[player_id] = player
        
        logger.info(f"Player {name} ({player_id}) logged in")
        return {
            'status': 'ok',
            'data': asdict(player)
        }
    
    async def _handle_logout(self, data: dict) -> dict:
        """Handle player logout"""
        player_id = data.get('id')
        
        if player_id in self.players:
            player = self.players[player_id]
            if player.game_id:
                await self._end_game(player.game_id)
            
            self.waiting_players.discard(player_id)
            del self.players[player_id]
            
            logger.info(f"Player {player.name} logged out")
            return {'status': 'ok'}
        
        return {'status': 'error', 'message': 'Player not found'}
    
    async def _handle_find_game(self, data: dict) -> dict:
        """Handle game matchmaking"""
        player_id = data.get('id')
        
        if player_id not in self.players:
            return {'status': 'error', 'message': 'Player not found'}
        
        player = self.players[player_id]
        
        # If player is already in a game
        if player.game_id:
            return {'status': 'error', 'message': 'Player already in game'}
        
        # Add to waiting list
        self.waiting_players.add(player_id)
        
        # Try to match with another player
        if len(self.waiting_players) >= 2:
            players = list(self.waiting_players)[:2]
            game_id = f"game_{len(self.games)}"
            
            game = Game(
                id=game_id,
                black_player=players[0],
                white_player=players[1],
                moves=[]
            )
            
            self.games[game_id] = game
            self.players[players[0]].game_id = game_id
            self.players[players[1]].game_id = game_id
            
            self.waiting_players.remove(players[0])
            self.waiting_players.remove(players[1])
            
            logger.info(f"Game {game_id} started between {players[0]} and {players[1]}")
            
            return {
                'status': 'ok',
                'data': {
                    'game_id': game_id,
                    'black_player': self.players[players[0]].name,
                    'white_player': self.players[players[1]].name
                }
            }
        
        return {
            'status': 'ok',
            'message': 'Waiting for opponent'
        }
    
    async def _handle_make_move(self, data: dict) -> dict:
        """Handle game move"""
        player_id = data.get('id')
        game_id = data.get('game_id')
        move = data.get('move')
        
        if not all([player_id, game_id, move]):
            return {'status': 'error', 'message': 'Invalid move data'}
        
        if game_id not in self.games:
            return {'status': 'error', 'message': 'Game not found'}
        
        game = self.games[game_id]
        if game.status != "playing":
            return {'status': 'error', 'message': 'Game not in progress'}
        
        # Validate move
        # TODO: Implement move validation
        
        game.moves.append(move)
        
        logger.info(f"Move made in game {game_id}: {move}")
        return {
            'status': 'ok',
            'data': {'move': move}
        }
    
    async def _handle_cancel_match(self, data: dict) -> dict:
        """Handle match cancellation"""
        player_id = data.get('id')
        
        if player_id in self.waiting_players:
            self.waiting_players.remove(player_id)
            logger.info(f"Player {player_id} cancelled matchmaking")
            return {'status': 'ok'}
        
        return {'status': 'error', 'message': 'Player not in matchmaking'}
    
    async def _handle_get_status(self, data: dict) -> dict:
        """Handle status request"""
        return {
            'status': 'ok',
            'data': {
                'players_online': len(self.players),
                'games_active': len(self.games),
                'players_waiting': len(self.waiting_players)
            }
        }
    
    async def _handle_list_games(self, data: dict) -> dict:
        """Handle game list request"""
        active_games = [
            {
                'id': game_id,
                'black_player': game.black_player,
                'white_player': game.white_player,
                'status': game.status,
                'spectator_count': self.spectator_manager.get_spectator_count(game_id)
            }
            for game_id, game in self.games.items()
            if game.status == "playing"
        ]
        
        return {
            'status': 'ok',
            'data': {
                'games': active_games
            }
        }
    
    async def _handle_spectate_game(self, data: dict) -> dict:
        """Handle spectate game request"""
        player_id = data.get('id')
        game_id = data.get('game_id')
        
        if not game_id or game_id not in self.games:
            return {'status': 'error', 'message': 'Game not found'}
        
        game = self.games[game_id]
        if game.status != "playing":
            return {'status': 'error', 'message': 'Game is not in progress'}
        
        # Check spectator limit
        current_count = self.spectator_manager.get_spectator_count(game_id)
        if current_count >= MAX_SPECTATORS_PER_GAME:
            return {'status': 'error', 'message': 'Game has reached spectator limit'}
        
        # Add spectator
        player = self.players.get(player_id)
        if not player:
            return {'status': 'error', 'message': 'Player not found'}
            
        if self.spectator_manager.add_spectator(player_id, player.name, game_id):
            # Update game state
            game.spectator_count = current_count + 1
            
            # Return initial game state
            return {
                'status': 'ok',
                'data': {
                    'game_id': game_id,
                    'black_player': game.black_player,
                    'white_player': game.white_player,
                    'moves': game.moves,
                    'status': game.status,
                    'spectator_count': game.spectator_count
                }
            }
        else:
            return {'status': 'error', 'message': 'Failed to add spectator'}
    
    async def _handle_leave_spectate(self, data: dict) -> dict:
        """Handle leave spectate request"""
        player_id = data.get('id')
        
        spectator = self.spectator_manager.get_spectator_info(player_id)
        if not spectator:
            return {'status': 'error', 'message': 'Not spectating any game'}
        
        game_id = spectator.game_id
        if self.spectator_manager.remove_spectator(player_id):
            # Update game state
            if game_id in self.games:
                game = self.games[game_id]
                game.spectator_count -= 1
            
            return {'status': 'ok'}
        else:
            return {'status': 'error', 'message': 'Failed to remove spectator'}
    
    async def _handle_spectator_chat(self, data: dict) -> dict:
        """Handle spectator chat message"""
        player_id = data.get('id')
        message = data.get('message')
        
        spectator = self.spectator_manager.get_spectator_info(player_id)
        if not spectator:
            return {'status': 'error', 'message': 'Not spectating any game'}
        
        # Broadcast chat message to all spectators
        chat_data = {
            'event': 'chat',
            'data': {
                'sender': spectator.name,
                'message': message
            }
        }
        
        self.spectator_manager.broadcast_to_spectators(
            spectator.game_id,
            chat_data,
            self._send_message_to_client
        )
        
        return {'status': 'ok'}
    
    async def _send_message_to_client(self, client_id: str, message: dict):
        """Send message to specific client"""
        # TODO: Implement actual message sending
        pass
    
    async def _broadcast_game_state(self, game_id: str):
        """Broadcast game state to spectators"""
        if game_id not in self.games:
            return
            
        game = self.games[game_id]
        state = {
            'event': 'game_state',
            'data': {
                'game_id': game_id,
                'black_player': game.black_player,
                'white_player': game.white_player,
                'moves': game.moves,
                'status': game.status,
                'spectator_count': game.spectator_count
            }
        }
        
        self.spectator_manager.broadcast_to_spectators(
            game_id,
            state,
            self._send_message_to_client
        )
    
    async def _end_game(self, game_id: str):
        """End a game session"""
        if game_id in self.games:
            game = self.games[game_id]
            game.status = "finished"
            
            # Clear player game references
            if game.black_player in self.players:
                self.players[game.black_player].game_id = None
            if game.white_player in self.players:
                self.players[game.white_player].game_id = None
            
            # Clean up spectators
            self.spectator_manager.cleanup_game(game_id)
            
            logger.info(f"Game {game_id} ended")
            del self.games[game_id] 
