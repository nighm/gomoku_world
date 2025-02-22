"""
Configuration system tests.

配置系统测试。
"""

import pytest
from pathlib import Path
import yaml

from gomoku_world.config import ConfigManager
from gomoku_world.config.exceptions import (
    ConfigError,
    ConfigKeyError,
    ConfigValueError,
    ConfigTypeError,
    ConfigRangeError,
    ConfigEnumError
)

# Test data / 测试数据
TEST_CONFIG = {
    "test": {
        "string": "value",
        "integer": 42,
        "float": 3.14,
        "boolean": True,
        "nested": {
            "key": "value"
        }
    }
}

@pytest.fixture
def config_manager():
    """Create test configuration manager / 创建测试配置管理器"""
    return ConfigManager("test", TEST_CONFIG)

def test_config_load_save(tmp_path, config_manager):
    """
    Test configuration loading and saving.
    测试配置加载和保存。
    """
    # Save configuration / 保存配置
    config_file = tmp_path / "test.yaml"
    with open(config_file, 'w', encoding='utf-8') as f:
        yaml.safe_dump(TEST_CONFIG, f)
    
    # Load configuration / 加载配置
    config = ConfigManager("test", {})
    assert config.get("test.string") == "value"
    assert config.get("test.integer") == 42
    assert config.get("test.float") == 3.14
    assert config.get("test.boolean") is True
    assert config.get("test.nested.key") == "value"

def test_config_get(config_manager):
    """
    Test configuration value retrieval.
    测试配置值获取。
    """
    # Test existing keys / 测试存在的键
    assert config_manager.get("test.string") == "value"
    assert config_manager.get("test.integer") == 42
    assert config_manager.get("test.nested.key") == "value"
    
    # Test default values / 测试默认值
    assert config_manager.get("nonexistent", "default") == "default"
    
    # Test missing keys / 测试缺失的键
    with pytest.raises(ConfigKeyError):
        config_manager.get("nonexistent")

def test_config_set(config_manager):
    """
    Test configuration value setting.
    测试配置值设置。
    """
    # Set new values / 设置新值
    config_manager.set("test.new_key", "new_value")
    assert config_manager.get("test.new_key") == "new_value"
    
    # Update existing values / 更新现有值
    config_manager.set("test.string", "updated")
    assert config_manager.get("test.string") == "updated"
    
    # Set nested values / 设置嵌套值
    config_manager.set("test.nested.new_key", "nested_value")
    assert config_manager.get("test.nested.new_key") == "nested_value"

def test_config_update(config_manager):
    """
    Test multiple configuration updates.
    测试多个配置更新。
    """
    updates = {
        "test.string": "updated",
        "test.integer": 100,
        "test.new_key": "new_value"
    }
    
    config_manager.update(updates)
    
    assert config_manager.get("test.string") == "updated"
    assert config_manager.get("test.integer") == 100
    assert config_manager.get("test.new_key") == "new_value"

def test_config_reset(config_manager):
    """
    Test configuration reset.
    测试配置重置。
    """
    # Modify configuration / 修改配置
    config_manager.set("test.string", "modified")
    config_manager.set("test.new_key", "new_value")
    
    # Reset configuration / 重置配置
    config_manager.reset()
    
    # Verify reset / 验证重置
    assert config_manager.get("test.string") == "value"
    with pytest.raises(ConfigKeyError):
        config_manager.get("test.new_key")

def test_config_validation(config_manager):
    """
    Test configuration validation.
    测试配置验证。
    """
    # Test type validation / 测试类型验证
    with pytest.raises(ConfigValueError):
        config_manager.set("test.integer", "not_an_integer")
    
    # Test range validation / 测试范围验证
    with pytest.raises(ConfigValueError):
        config_manager.set("test.integer", -1)
    
    # Test enum validation / 测试枚举验证
    with pytest.raises(ConfigValueError):
        config_manager.set("test.string", "invalid_enum_value")

def test_config_export(tmp_path, config_manager):
    """
    Test configuration export.
    测试配置导出。
    """
    # Export configuration / 导出配置
    export_file = tmp_path / "export.yaml"
    config_manager.export(export_file)
    
    # Verify exported file / 验证导出文件
    with open(export_file, 'r', encoding='utf-8') as f:
        exported = yaml.safe_load(f)
    
    assert exported == config_manager._config

def test_config_merge(config_manager):
    """
    Test configuration merging.
    测试配置合并。
    """
    user_config = {
        "test": {
            "string": "user_value",
            "nested": {
                "new_key": "new_value"
            }
        }
    }
    
    config_manager._merge_config(user_config)
    
    assert config_manager.get("test.string") == "user_value"
    assert config_manager.get("test.integer") == 42  # Preserved from default
    assert config_manager.get("test.nested.key") == "value"  # Preserved from default
    assert config_manager.get("test.nested.new_key") == "new_value"  # Added from user config 