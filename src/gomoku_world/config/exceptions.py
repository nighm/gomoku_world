"""
Configuration system exceptions.

配置系统异常。

This module defines all exceptions that can be raised by the configuration system.
本模块定义了配置系统可能抛出的所有异常。
"""

class ConfigError(Exception):
    """
    Base exception for all configuration related errors.
    所有配置相关错误的基类。
    """
    pass

class ConfigFileError(ConfigError):
    """
    Raised when there is an error with configuration files.
    当配置文件出现错误时抛出。
    """
    def __init__(self, file_path: str, error: str):
        self.file_path = file_path
        self.error = error
        super().__init__(f"Error in configuration file '{file_path}': {error} / "
                        f"配置文件'{file_path}'出错：{error}")

class ValidationError(ConfigError):
    """
    Raised when configuration validation fails.
    当配置验证失败时抛出。
    """
    def __init__(self, message: str, details: dict = None):
        self.details = details or {}
        super().__init__(f"{message} Details: {details} / "
                        f"{message} 详细信息：{details}")

class SchemaError(ConfigError):
    """
    Raised when there is an error with the validation schema.
    当验证架构出现错误时抛出。
    """
    def __init__(self, message: str, schema: dict = None):
        self.schema = schema
        super().__init__(f"{message} Schema: {schema} / "
                        f"{message} 架构：{schema}")

class ConfigValueError(ConfigError):
    """
    Raised when there is an error with a configuration value.
    当配置值出现错误时抛出。
    """
    def __init__(self, key: str, value: any, message: str):
        self.key = key
        self.value = value
        super().__init__(f"Invalid value for '{key}': {value}. {message} / "
                        f"'{key}'的值无效：{value}。{message}")

class ConfigKeyError(ConfigError):
    """
    Raised when a configuration key is not found.
    当找不到配置键时抛出。
    """
    def __init__(self, key: str):
        self.key = key
        super().__init__(f"Configuration key not found: {key} / "
                        f"未找到配置键：{key}")

class ConfigTypeError(ConfigError):
    """
    Raised when a configuration value has an invalid type.
    当配置值类型无效时抛出。
    """
    def __init__(self, key: str, expected_type: str, actual_type: str):
        self.key = key
        self.expected_type = expected_type
        self.actual_type = actual_type
        super().__init__(f"Invalid type for '{key}': expected {expected_type}, got {actual_type} / "
                        f"'{key}'的类型无效：期望 {expected_type}，实际为 {actual_type}")

class ConfigRangeError(ConfigError):
    """
    Raised when a configuration value is out of range.
    当配置值超出范围时抛出。
    """
    def __init__(self, key: str, value: any, minimum: any = None, maximum: any = None):
        self.key = key
        self.value = value
        self.minimum = minimum
        self.maximum = maximum
        
        range_str = ""
        if minimum is not None and maximum is not None:
            range_str = f"between {minimum} and {maximum}"
        elif minimum is not None:
            range_str = f"greater than or equal to {minimum}"
        elif maximum is not None:
            range_str = f"less than or equal to {maximum}"
            
        range_str_zh = ""
        if minimum is not None and maximum is not None:
            range_str_zh = f"在 {minimum} 和 {maximum} 之间"
        elif minimum is not None:
            range_str_zh = f"大于或等于 {minimum}"
        elif maximum is not None:
            range_str_zh = f"小于或等于 {maximum}"
        
        super().__init__(f"Value {value} for '{key}' must be {range_str} / "
                        f"'{key}'的值 {value} 必须{range_str_zh}")

class ConfigEnumError(ConfigError):
    """
    Raised when a configuration value is not in the allowed set.
    当配置值不在允许的集合中时抛出。
    """
    def __init__(self, key: str, value: any, allowed_values: list):
        self.key = key
        self.value = value
        self.allowed_values = allowed_values
        super().__init__(f"Value {value} for '{key}' must be one of {allowed_values} / "
                        f"'{key}'的值 {value} 必须是 {allowed_values} 之一") 