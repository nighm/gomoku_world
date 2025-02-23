"""
Configuration validator.
配置验证器。
"""

from typing import Any, Callable, Dict, List, Optional, Union
from .exceptions import ConfigValidationError

class ConfigValidator:
    """
    Configuration validator class.
    配置验证器类。
    """
    
    def __init__(self):
        """
        Initialize configuration validator.
        初始化配置验证器。
        """
        self.rules: Dict[str, List[Callable]] = {}
        self.errors: Dict[str, str] = {}
    
    def add_rule(self, key: str, rule: Callable[[Any], bool], message: str) -> None:
        """
        Add validation rule.
        添加验证规则。
        
        Args:
            key: Configuration key to validate
                 要验证的配置键
            rule: Validation function that returns True if valid
                  返回True表示有效的验证函数
            message: Error message if validation fails
                    验证失败时的错误消息
        """
        if key not in self.rules:
            self.rules[key] = []
        self.rules[key].append(lambda value: (rule(value), message))
    
    def add_type_rule(self, key: str, expected_type: Union[type, tuple]) -> None:
        """
        Add type validation rule.
        添加类型验证规则。
        
        Args:
            key: Configuration key to validate
                 要验证的配置键
            expected_type: Expected type or tuple of types
                         预期类型或类型元组
        """
        type_name = expected_type.__name__ if isinstance(expected_type, type) else \
                   " or ".join(t.__name__ for t in expected_type)
        self.add_rule(
            key,
            lambda value: isinstance(value, expected_type),
            f"Must be of type {type_name}"
        )
    
    def add_range_rule(self, key: str, min_value: Optional[float] = None,
                      max_value: Optional[float] = None) -> None:
        """
        Add range validation rule.
        添加范围验证规则。
        
        Args:
            key: Configuration key to validate
                 要验证的配置键
            min_value: Minimum allowed value
                      最小允许值
            max_value: Maximum allowed value
                      最大允许值
        """
        if min_value is not None and max_value is not None:
            self.add_rule(
                key,
                lambda value: min_value <= value <= max_value,
                f"Must be between {min_value} and {max_value}"
            )
        elif min_value is not None:
            self.add_rule(
                key,
                lambda value: value >= min_value,
                f"Must be greater than or equal to {min_value}"
            )
        elif max_value is not None:
            self.add_rule(
                key,
                lambda value: value <= max_value,
                f"Must be less than or equal to {max_value}"
            )
    
    def add_enum_rule(self, key: str, allowed_values: List[Any]) -> None:
        """
        Add enumeration validation rule.
        添加枚举验证规则。
        
        Args:
            key: Configuration key to validate
                 要验证的配置键
            allowed_values: List of allowed values
                          允许值列表
        """
        self.add_rule(
            key,
            lambda value: value in allowed_values,
            f"Must be one of {allowed_values}"
        )
    
    def add_custom_rule(self, key: str, validator: Callable[[Any], bool],
                       message: str) -> None:
        """
        Add custom validation rule.
        添加自定义验证规则。
        
        Args:
            key: Configuration key to validate
                 要验证的配置键
            validator: Custom validation function
                      自定义验证函数
            message: Error message if validation fails
                    验证失败时的错误消息
        """
        self.add_rule(key, validator, message)
    
    def validate(self, config: Dict[str, Any]) -> None:
        """
        Validate configuration.
        验证配置。
        
        Args:
            config: Configuration to validate
                   要验证的配置
                   
        Raises:
            ConfigValidationError: If validation fails
                                 如果验证失败
        """
        self.errors.clear()
        
        def validate_dict(prefix: str, data: Dict[str, Any]) -> None:
            for key, value in data.items():
                full_key = f"{prefix}.{key}" if prefix else key
                
                if isinstance(value, dict):
                    validate_dict(full_key, value)
                elif full_key in self.rules:
                    for rule in self.rules[full_key]:
                        is_valid, message = rule(value)
                        if not is_valid:
                            self.errors[full_key] = message
                            break
        
        validate_dict("", config)
        
        if self.errors:
            raise ConfigValidationError(self.errors)

__all__ = ["ConfigValidator"] 