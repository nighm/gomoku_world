"""
Integration tests for manager instances
管理器实例集成测试
"""

import pytest
import asyncio
from gomoku_world.config.instances import config_manager
from gomoku_world.network.instances import network_manager
from gomoku_world.utils.debug.instances import debug_manager

@pytest.mark.asyncio
async def test_manager_initialization_order():
    """Test proper initialization order of managers"""
    # Reset all managers
    config_manager.reset()
    await network_manager.disconnect()
    debug_manager.reset()
    
    # Configure debug mode through config
    config_manager.set_value('DEBUG_MODE', True)
    
    # Debug manager should reflect config
    debug_manager.toggle_debug_mode()
    assert debug_manager.debug_mode is True
    
    # Network manager should use debug settings
    await network_manager.connect()
    assert network_manager.is_debug_mode() is True

@pytest.mark.asyncio
async def test_network_debug_integration():
    """Test network and debug manager integration"""
    # Enable debug mode
    debug_manager.toggle_debug_mode()
    
    # Connect to server
    await network_manager.connect()
    
    # Send test message
    response = await network_manager.send_message({
        'type': 'test',
        'data': 'test_data'
    })
    
    # Debug info should be updated
    assert 'last_network_message' in debug_manager.debug_info
    assert debug_manager.debug_info['last_network_message'] == 'test_data'
    
    await network_manager.disconnect()

@pytest.mark.asyncio
async def test_config_network_integration():
    """Test configuration and network manager integration"""
    # Set network configuration
    config_manager.set_value('NETWORK_HOST', 'localhost')
    config_manager.set_value('NETWORK_PORT', 5000)
    
    # Network manager should use config values
    await network_manager.connect()
    assert network_manager.host == 'localhost'
    assert network_manager.port == 5000
    
    await network_manager.disconnect()

def test_config_debug_integration():
    """Test configuration and debug manager integration"""
    # Set debug configuration
    config_manager.set_value('DEBUG_MODE', True)
    config_manager.set_value('SHOW_FPS', True)
    config_manager.set_value('SHOW_GRID', True)
    
    # Debug manager should reflect config
    assert debug_manager.debug_mode is True
    assert debug_manager.show_fps is True
    assert debug_manager.show_grid_coords is True

@pytest.mark.asyncio
async def test_manager_cleanup_order():
    """Test proper cleanup order of managers"""
    # Initialize all managers
    await network_manager.connect()
    debug_manager.toggle_debug_mode()
    config_manager.set_value('TEST_KEY', 'test_value')
    
    # Simulate application shutdown
    await network_manager.disconnect()
    debug_manager.reset()
    config_manager.cleanup()
    
    # Verify cleanup
    assert not network_manager.is_connected()
    assert not debug_manager.debug_mode
    assert config_manager.get_value('TEST_KEY') is None

@pytest.mark.asyncio
async def test_error_handling_integration():
    """Test error handling across managers"""
    # Enable debug mode for detailed error logging
    debug_manager.toggle_debug_mode()
    
    # Simulate network error
    await network_manager.connect()
    network_manager._connection_lost()
    
    # Debug manager should capture error
    assert 'last_error' in debug_manager.debug_info
    assert 'connection_lost' in debug_manager.debug_info['last_error']
    
    # Config should record error state
    assert config_manager.get_value('LAST_ERROR_TIME') is not None
    
    await network_manager.disconnect()

@pytest.mark.asyncio
async def test_performance_monitoring():
    """Test performance monitoring integration"""
    # Enable performance monitoring
    debug_manager.toggle_debug_mode()
    config_manager.set_value('MONITOR_PERFORMANCE', True)
    
    # Simulate some network operations
    await network_manager.connect()
    for _ in range(10):
        await network_manager.send_message({'type': 'test'})
    
    # Check performance metrics
    assert 'network_latency' in debug_manager.debug_info
    assert 'message_count' in debug_manager.debug_info
    assert debug_manager.debug_info['message_count'] == 10
    
    await network_manager.disconnect() 