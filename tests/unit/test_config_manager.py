"""
Configuration manager unit tests
閰嶇疆绠＄悊鍣ㄥ崟鍏冩祴璇?
"""

import pytest
from gomoku_world.config.instances import config_manager

def test_config_manager_singleton():
    """Test config manager singleton pattern"""
    from gomoku_world.config.manager import ConfigManager
    
    # Get another instance
    another_manager = ConfigManager()
    
    # Should be the same instance
    assert config_manager is another_manager

def test_config_manager_initialization():
    """Test config manager initialization"""
    # Default values should be set
    assert config_manager.get_value('BOARD_SIZE') == 15
    assert config_manager.get_value('WIN_LENGTH') == 5
    assert config_manager.get_value('DEFAULT_THEME') == 'light'
    assert config_manager.get_value('DEFAULT_LANGUAGE') == 'en'

def test_config_manager_set_get():
    """Test setting and getting config values"""
    # Set a test value
    config_manager.set_value('TEST_KEY', 'test_value')
    
    # Get the value back
    assert config_manager.get_value('TEST_KEY') == 'test_value'
    
    # Get non-existent value should return None or default
    assert config_manager.get_value('NON_EXISTENT') is None
    assert config_manager.get_value('NON_EXISTENT', 'default') == 'default'

def test_config_manager_load_save():
    """Test loading and saving configuration"""
    # Set some test values
    test_config = {
        'TEST_KEY1': 'value1',
        'TEST_KEY2': 'value2'
    }
    
    # Save configuration
    config_manager.save_config(test_config)
    
    # Load configuration
    loaded_config = config_manager.load_config()
    
    # Check values
    assert loaded_config['TEST_KEY1'] == 'value1'
    assert loaded_config['TEST_KEY2'] == 'value2'

def test_config_manager_reset():
    """Test resetting configuration"""
    # Set a test value
    config_manager.set_value('TEST_KEY', 'test_value')
    
    # Reset configuration
    config_manager.reset()
    
    # Value should be gone
    assert config_manager.get_value('TEST_KEY') is None 
