# 配置系统故障排除指南 / Configuration System Troubleshooting Guide

## 概述 / Overview

本文档提供了配置系统常见问题的解决方案和调试技巧。

This document provides solutions for common configuration system issues and debugging tips.

## 常见问题 / Common Issues

### 1. 配置加载失败 / Configuration Loading Failed

#### 症状 / Symptoms
- 配置文件无法读取 / Configuration file cannot be read
- 配置值为默认值 / Configuration values are defaults
- 出现文件相关错误 / File-related errors occur

#### 解决方案 / Solutions
1. 检查文件权限 / Check file permissions
```bash
# Windows
icacls config.yaml

# Linux/macOS
ls -l config.yaml
```

2. 验证文件路径 / Verify file path
```python
import os
config_path = "path/to/config.yaml"
print(f"File exists: {os.path.exists(config_path)}")
```

3. 检查文件格式 / Check file format
```python
import yaml
try:
    with open("config.yaml", "r", encoding="utf-8") as f:
        yaml.safe_load(f)
except yaml.YAMLError as e:
    print(f"YAML格式错误 / YAML format error: {e}")
```

### 2. 配置验证错误 / Configuration Validation Errors

#### 症状 / Symptoms
- 配置值被拒绝 / Configuration values are rejected
- 出现类型错误 / Type errors occur
- 验证异常 / Validation exceptions

#### 解决方案 / Solutions
1. 检查值类型 / Check value types
```python
from gomoku_world.config import ConfigValidator

validator = ConfigValidator()
result = validator.validate_value("board.size", 15)
print(f"验证结果 / Validation result: {result}")
```

2. 验证值范围 / Verify value ranges
```python
# 检查数值范围 / Check numeric ranges
if not (9 <= board_size <= 19):
    print("棋盘大小无效 / Invalid board size")
```

3. 查看完整的验证结果 / View complete validation results
```python
result = validator.validate_config(config_dict)
if not result.is_valid:
    for error in result.errors:
        print(f"错误 / Error: {error}")
```

### 3. 配置保存失败 / Configuration Save Failed

#### 症状 / Symptoms
- 配置更改未保存 / Configuration changes not saved
- 出现写入错误 / Write errors occur
- 文件锁定问题 / File locking issues

#### 解决方案 / Solutions
1. 检查目录权限 / Check directory permissions
```python
import os
config_dir = "path/to/config"
if not os.access(config_dir, os.W_OK):
    print("目录不可写 / Directory not writable")
```

2. 使用安全的保存方式 / Use safe saving method
```python
def safe_save_config(config, path):
    temp_path = path + ".tmp"
    try:
        config.save(temp_path)
        os.replace(temp_path, path)
    except Exception as e:
        print(f"保存失败 / Save failed: {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)
```

3. 处理文件锁定 / Handle file locking
```python
import fcntl  # Linux/macOS only

def with_file_lock(func):
    def wrapper(*args, **kwargs):
        with open("config.lock", "w") as lock_file:
            fcntl.flock(lock_file, fcntl.LOCK_EX)
            try:
                return func(*args, **kwargs)
            finally:
                fcntl.flock(lock_file, fcntl.LOCK_UN)
    return wrapper
```

### 4. 配置同步问题 / Configuration Synchronization Issues

#### 症状 / Symptoms
- 配置不一致 / Configuration inconsistency
- 多处配置冲突 / Multiple configuration conflicts
- 更新未生效 / Updates not effective

#### 解决方案 / Solutions
1. 使用版本控制 / Use version control
```python
class VersionedConfig:
    def __init__(self):
        self.version = 0
        self.config = {}
    
    def update(self, changes):
        self.version += 1
        self.config.update(changes)
        self._notify_changes()
```

2. 实现配置监听 / Implement configuration watching
```python
class ConfigWatcher:
    def __init__(self):
        self._callbacks = []
    
    def add_callback(self, callback):
        self._callbacks.append(callback)
    
    def notify_change(self, key, value):
        for callback in self._callbacks:
            callback(key, value)
```

## 调试技巧 / Debugging Tips

### 1. 启用调试日志 / Enable Debug Logging
```python
import logging

# 设置日志级别 / Set log level
logging.getLogger("gomoku_world.config").setLevel(logging.DEBUG)

# 添加文件处理器 / Add file handler
handler = logging.FileHandler("config_debug.log")
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))
logging.getLogger("gomoku_world.config").addHandler(handler)
```

### 2. 配置导出 / Configuration Export
```python
def export_debug_info():
    """导出调试信息 / Export debug information"""
    debug_info = {
        "config": config.to_dict(),
        "validation": validator.validate_config(config.to_dict()).to_dict(),
        "system_info": {
            "platform": sys.platform,
            "python_version": sys.version,
            "working_directory": os.getcwd()
        }
    }
    with open("config_debug.json", "w") as f:
        json.dump(debug_info, f, indent=2)
```

### 3. 配置比较 / Configuration Comparison
```python
def compare_configs(config1, config2):
    """比较两个配置 / Compare two configurations"""
    differences = []
    for key in set(config1.keys()) | set(config2.keys()):
        if key not in config1:
            differences.append(f"键仅在config2中存在 / Key only in config2: {key}")
        elif key not in config2:
            differences.append(f"键仅在config1中存在 / Key only in config1: {key}")
        elif config1[key] != config2[key]:
            differences.append(
                f"值不同 / Different values for {key}: "
                f"config1={config1[key]}, config2={config2[key]}"
            )
    return differences
```

## 性能优化 / Performance Optimization

### 1. 配置缓存 / Configuration Caching
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_computed_config(key):
    """获取计算的配置值 / Get computed configuration value"""
    return expensive_computation(key)
```

### 2. 批量操作 / Batch Operations
```python
def batch_update(updates):
    """批量更新配置 / Batch update configurations"""
    with config.batch_context():
        for key, value in updates.items():
            config.set(key, value)
```

## 恢复和备份 / Recovery and Backup

### 1. 自动备份 / Automatic Backup
```python
def backup_config():
    """备份配置文件 / Backup configuration file"""
    import shutil
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"config_backup_{timestamp}.yaml"
    shutil.copy2("config.yaml", backup_path)
    return backup_path
```

### 2. 配置重置 / Configuration Reset
```python
def reset_to_default():
    """重置为默认配置 / Reset to default configuration"""
    config.reset()
    print("配置已重置 / Configuration has been reset")
```

## 工具和命令 / Tools and Commands

### 1. 配置检查工具 / Configuration Check Tool
```python
def check_config():
    """检查配置完整性 / Check configuration integrity"""
    issues = []
    
    # 检查必需的键 / Check required keys
    required_keys = ["board.size", "display.theme", "sound.volume"]
    for key in required_keys:
        if not config.has_key(key):
            issues.append(f"缺少必需的键 / Missing required key: {key}")
    
    # 检查值类型 / Check value types
    type_checks = {
        "board.size": int,
        "display.theme": str,
        "sound.volume": (int, float)
    }
    for key, expected_type in type_checks.items():
        value = config.get(key)
        if not isinstance(value, expected_type):
            issues.append(
                f"类型错误 / Type error for {key}: "
                f"expected {expected_type}, got {type(value)}"
            )
    
    return issues
```

### 2. 配置迁移工具 / Configuration Migration Tool
```python
def migrate_config(old_config, new_version):
    """迁移配置到新版本 / Migrate configuration to new version"""
    migrations = {
        "1.4.5": migrate_to_1_4_5,
        "1.4.6": migrate_to_1_4_6
    }
    
    current_version = old_config.get("version", "1.4.0")
    while current_version != new_version:
        next_version = get_next_version(current_version)
        if next_version not in migrations:
            raise ValueError(f"无法迁移到版本 / Cannot migrate to version: {next_version}")
        old_config = migrations[next_version](old_config)
        current_version = next_version
    
    return old_config
```

## 更多资源 / More Resources

- [配置系统API文档 / Configuration System API Documentation](../api/config.md)
- [配置示例 / Configuration Examples](../examples/config/)
- [常见问题解答 / FAQ](../faq/config.md)
- [配置最佳实践 / Configuration Best Practices](config_best_practices.md) 