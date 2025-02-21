"""
Network manager unit tests
网络管理器单元测试
"""

import pytest
import asyncio
from gomoku_world.network.instances import network_manager

@pytest.mark.asyncio
async def test_network_manager_singleton():
    """Test network manager singleton pattern"""
    from gomoku_world.network.network import NetworkManager
    
    # Get another instance
    another_manager = NetworkManager()
    
    # Should be the same instance
    assert network_manager is another_manager

@pytest.mark.asyncio
async def test_network_manager_connection():
    """Test network connection"""
    # Connect to server
    connected = await network_manager.connect()
    assert connected is True
    
    # Should be connected
    assert network_manager.is_connected() is True
    
    # Disconnect
    await network_manager.disconnect()
    assert network_manager.is_connected() is False

@pytest.mark.asyncio
async def test_network_manager_send_receive():
    """Test sending and receiving messages"""
    # Connect first
    await network_manager.connect()
    
    # Send a test message
    response = await network_manager.send_message({
        'type': 'test',
        'data': 'test_data'
    })
    
    # Check response
    assert response is not None
    assert response.get('status') == 'ok'
    
    # Disconnect
    await network_manager.disconnect()

@pytest.mark.asyncio
async def test_network_manager_events():
    """Test event handling"""
    events = []
    
    # Add event handler
    def on_test_event(data):
        events.append(data)
    
    network_manager.on('test_event', on_test_event)
    
    # Connect
    await network_manager.connect()
    
    # Simulate receiving an event
    await network_manager._handle_event({
        'event': 'test_event',
        'data': 'test_data'
    })
    
    # Check event was handled
    assert len(events) == 1
    assert events[0] == 'test_data'
    
    # Remove event handler
    network_manager.off('test_event', on_test_event)
    
    # Disconnect
    await network_manager.disconnect()

@pytest.mark.asyncio
async def test_network_manager_reconnection():
    """Test automatic reconnection"""
    # Connect
    await network_manager.connect()
    
    # Simulate connection loss
    network_manager._connection_lost()
    
    # Wait for reconnection attempt
    await asyncio.sleep(1)
    
    # Should be reconnected
    assert network_manager.is_connected() is True
    
    # Disconnect
    await network_manager.disconnect() 