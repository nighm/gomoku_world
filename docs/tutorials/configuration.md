# 配置系统指南 / Configuration System Guide

## 概述 / Overview

配置系统提供了一个统一的方式来管理游戏的各种设置。本指南将介绍如何使用配置系统的各项功能。

The configuration system provides a unified way to manage various game settings. This guide will introduce how to use the features of the configuration system.

## 主要功能 / Main Features

1. **统一配置接口 / Unified Configuration Interface**
   - 使用点号访问嵌套配置 / Access nested configurations using dot notation
   - 自动合并默认配置 / Automatic merging with default configurations
   - 配置验证和类型检查 / Configuration validation and type checking

2. **配置文件格式 / Configuration File Format**
   - 基于YAML的配置文件 / YAML-based configuration files
   - 支持多语言注释 / Support for multilingual comments
   - 结构化的配置组织 / Structured configuration organization

3. **配置验证 / Configuration Validation**
   - 类型验证 / Type validation
   - 范围检查 / Range checking
   - 枚举值验证 / Enum validation
   - 自定义验证规则 / Custom validation rules

## 使用方法 / Usage

### 基本用法 / Basic Usage

```python
from gomoku_world.config import game_config

# 获取配置值 / Get configuration value
board_size = game_config.get("board.size")  # 返回棋盘大小 / Returns board size

# 设置配置值 / Set configuration value
game_config.set("display.theme", "dark")  # 设置主题为暗色 / Set theme to dark

# 更新多个配置 / Update multiple configurations
game_config.update({
    "sound.enabled": True,
    "sound.volume": 80
})

# 重置配置 / Reset configuration
game_config.reset()
```

### 配置验证 / Configuration Validation

### 基本验证 / Basic Validation
```python
from gomoku_world.config import ConfigValidator

validator = ConfigValidator()

# 验证配置 / Validate configuration
result = validator.validate_config({
    "board": {
        "size": 15,
        "win_count": 5
    }
})

if result.is_valid:
    print("配置有效 / Configuration is valid")
else:
    print("错误：", result.errors)
```

### 高级验证功能 / Advanced Validation Features

1. **类型验证 / Type Validation**
```python
# 定义类型验证规则
schema = {
    "board.size": {"type": "integer", "min": 9, "max": 19},
    "display.theme": {"type": "string", "enum": ["light", "dark"]},
    "sound.volume": {"type": "integer", "min": 0, "max": 100}
}

# 应用验证规则
validator.set_schema(schema)
result = validator.validate_value("board.size", 15)
```

2. **自定义验证规则 / Custom Validation Rules**
```python
from typing import Any
from gomoku_world.config.validation import ValidationRule

class EvenNumberRule(ValidationRule):
    def validate(self, value: Any) -> bool:
        return isinstance(value, int) and value % 2 == 0

# 注册自定义规则
validator.register_rule("even_number", EvenNumberRule())

# 使用自定义规则
schema = {
    "board.size": {"type": "integer", "rules": ["even_number"]}
}
```

3. **条件验证 / Conditional Validation**
```python
# 定义条件验证规则
schema = {
    "network.enabled": {"type": "boolean"},
    "network.port": {
        "type": "integer",
        "min": 1024,
        "max": 65535,
        "required_if": {"network.enabled": True}
    }
}
```

4. **批量验证 / Batch Validation**
```python
# 批量验证多个配置
results = validator.validate_many({
    "board.size": 15,
    "display.theme": "dark",
    "sound.volume": 80
})

for key, result in results.items():
    if not result.is_valid:
        print(f"{key}: {result.errors}")
```

### 验证结果处理 / Validation Result Handling

```python
from gomoku_world.config.validation import ValidationResult

def handle_validation(result: ValidationResult):
    if result.is_valid:
        print("验证通过 / Validation passed")
    else:
        if result.errors:
            print("错误 / Errors:", result.errors)
        if result.warnings:
            print("警告 / Warnings:", result.warnings)
```

### 错误处理 / Error Handling

```