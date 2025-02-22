"""
Configuration validation module.

配置验证模块。

This module provides validation functionality for configuration values:
- Type checking
- Value range validation
- Required field validation
- Schema validation
- Custom validation rules

本模块提供配置值的验证功能：
- 类型检查
- 值范围验证
- 必需字段验证
- 架构验证
- 自定义验证规则
"""

import logging
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from pathlib import Path
import yaml

from .exceptions import ValidationError

logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """
    Validation result data class.
    验证结果数据类。
    """
    is_valid: bool
    errors: List[str]
    warnings: List[str]

class ConfigValidator:
    """
    Configuration validator class.
    配置验证器类。
    """
    
    def __init__(self):
        """
        Initialize validator.
        初始化验证器。
        """
        self._schema: Dict = {}
        self._load_default_schema()
    
    def _load_default_schema(self):
        """
        Load default validation schema.
        加载默认验证架构。
        """
        self._schema = {
            "game": {
                "type": "object",
                "properties": {
                    "board": {
                        "type": "object",
                        "properties": {
                            "size": {"type": "integer", "minimum": 5, "maximum": 19},
                            "win_length": {"type": "integer", "minimum": 3, "maximum": 5}
                        },
                        "required": ["size", "win_length"]
                    },
                    "ai": {
                        "type": "object",
                        "properties": {
                            "enabled": {"type": "boolean"},
                            "difficulty": {
                                "type": "string",
                                "enum": ["easy", "medium", "hard"]
                            },
                            "thinking_time": {"type": "number", "minimum": 0.1}
                        }
                    },
                    "display": {
                        "type": "object",
                        "properties": {
                            "window_size": {"type": "integer", "minimum": 400},
                            "theme": {"type": "string"},
                            "language": {"type": "string"}
                        }
                    },
                    "sound": {
                        "type": "object",
                        "properties": {
                            "enabled": {"type": "boolean"},
                            "volume": {"type": "number", "minimum": 0.0, "maximum": 1.0},
                            "music": {"type": "boolean"}
                        }
                    }
                }
            },
            "i18n": {
                "type": "object",
                "properties": {
                    "general": {
                        "type": "object",
                        "properties": {
                            "default_language": {"type": "string"},
                            "fallback_language": {"type": "string"}
                        },
                        "required": ["default_language"]
                    },
                    "cache": {
                        "type": "object",
                        "properties": {
                            "enabled": {"type": "boolean"},
                            "ttl": {"type": "integer", "minimum": 0},
                            "max_size": {"type": "integer", "minimum": 0}
                        }
                    },
                    "network": {
                        "type": "object",
                        "properties": {
                            "enabled": {"type": "boolean"},
                            "update_interval": {"type": "integer", "minimum": 0},
                            "timeout": {"type": "integer", "minimum": 0}
                        }
                    }
                }
            }
        }
    
    def validate_file(self, filepath: Union[str, Path]) -> ValidationResult:
        """
        Validate configuration file.
        验证配置文件。
        
        Args:
            filepath: Path to configuration file
                     配置文件路径
            
        Returns:
            ValidationResult: Validation result
                            验证结果
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            return self.validate_config(config)
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                errors=[f"Failed to load configuration file: {e}"],
                warnings=[]
            )
    
    def validate_config(self, config: Dict) -> ValidationResult:
        """
        Validate configuration dictionary.
        验证配置字典。
        
        Args:
            config: Configuration dictionary
                   配置字典
            
        Returns:
            ValidationResult: Validation result
                            验证结果
        """
        errors = []
        warnings = []
        
        for section, schema in self._schema.items():
            if section not in config:
                if "required" in schema:
                    errors.append(f"Missing required section: {section}")
                continue
            
            section_result = self._validate_section(config[section], schema, section)
            errors.extend(section_result.errors)
            warnings.extend(section_result.warnings)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def validate_value(self, key: str, value: Any, schema: Dict) -> Tuple[bool, Optional[str]]:
        """
        Validate single configuration value.
        验证单个配置值。
        
        Args:
            key: Configuration key
                 配置键
            value: Configuration value
                   配置值
            schema: Validation schema
                    验证架构
            
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message)
                                      (是否有效，错误消息)
        """
        # Type validation / 类型验证
        if "type" in schema:
            if not self._validate_type(value, schema["type"]):
                return False, f"Invalid type for {key}: expected {schema['type']}, got {type(value).__name__}"
        
        # Range validation / 范围验证
        if schema.get("type") in ["integer", "number"]:
            if "minimum" in schema and value < schema["minimum"]:
                return False, f"Value for {key} is below minimum: {value} < {schema['minimum']}"
            if "maximum" in schema and value > schema["maximum"]:
                return False, f"Value for {key} is above maximum: {value} > {schema['maximum']}"
        
        # Enum validation / 枚举验证
        if "enum" in schema and value not in schema["enum"]:
            return False, f"Invalid value for {key}: {value} not in {schema['enum']}"
        
        return True, None
    
    def _validate_section(self, config: Dict, schema: Dict, path: str = "") -> ValidationResult:
        """
        Validate configuration section.
        验证配置部分。
        
        Args:
            config: Configuration section
                   配置部分
            schema: Section schema
                    部分架构
            path: Configuration path
                  配置路径
            
        Returns:
            ValidationResult: Validation result
                            验证结果
        """
        errors = []
        warnings = []
        
        # Type validation / 类型验证
        if not isinstance(config, dict):
            return ValidationResult(
                is_valid=False,
                errors=[f"Invalid type for section {path}: expected dict, got {type(config).__name__}"],
                warnings=[]
            )
        
        # Required fields / 必需字段
        if "required" in schema:
            for field in schema["required"]:
                if field not in config:
                    errors.append(f"Missing required field: {path}.{field}")
        
        # Properties validation / 属性验证
        if "properties" in schema:
            for key, value in config.items():
                if key not in schema["properties"]:
                    warnings.append(f"Unknown configuration key: {path}.{key}")
                    continue
                
                field_schema = schema["properties"][key]
                field_path = f"{path}.{key}" if path else key
                
                if field_schema.get("type") == "object":
                    result = self._validate_section(value, field_schema, field_path)
                    errors.extend(result.errors)
                    warnings.extend(result.warnings)
                else:
                    is_valid, error = self.validate_value(field_path, value, field_schema)
                    if not is_valid:
                        errors.append(error)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def _validate_type(self, value: Any, expected_type: str) -> bool:
        """
        Validate value type.
        验证值类型。
        
        Args:
            value: Value to validate
                  要验证的值
            expected_type: Expected type name
                         期望的类型名称
            
        Returns:
            bool: Whether the type is valid
                  类型是否有效
        """
        type_map = {
            "string": str,
            "integer": int,
            "number": (int, float),
            "boolean": bool,
            "object": dict,
            "array": list
        }
        
        if expected_type not in type_map:
            logger.warning(f"Unknown type: {expected_type}")
            return True
        
        expected_types = type_map[expected_type]
        if not isinstance(expected_types, tuple):
            expected_types = (expected_types,)
        
        return isinstance(value, expected_types)
    
    def set_schema(self, schema: Dict):
        """
        Set custom validation schema.
        设置自定义验证架构。
        
        Args:
            schema: Validation schema
                   验证架构
        """
        self._schema = schema 