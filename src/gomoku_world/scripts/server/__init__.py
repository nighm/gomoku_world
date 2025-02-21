"""
Server launcher module
鏈嶅姟鍣ㄥ惎鍔ㄦā鍧?
"""

import asyncio
import sys

from ...network.server import GameServer
from ...utils.logger import setup_logging

async def _run_server():
    """Run the server"""
    # Setup logging
    setup_logging()
    
    # Create and start server
    server = GameServer()
    await server.start()

def main():
    """Main entry point"""
    try:
        asyncio.run(_run_server())
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 
