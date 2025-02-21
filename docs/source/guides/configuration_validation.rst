配置验证工具指南
============

本指南介绍了五子棋世界提供的配置验证工具及其使用方法。

配置验证器
--------

基本用法
~~~~~~~

使用配置验证器::

    from gomoku_world.config.validation import ConfigValidator
    
    # 创建验证器
    validator = ConfigValidator()
    
    # 验证配置文件
    result = validator.validate_file("config.yaml")
    
    if result.is_valid:
        print("配置有效")
    else:
        print(f"配置错误: {result.errors}")

验证特定配置项::

    # 验证单个配置值
    is_valid = validator.validate_value(
        key="AI_DIFFICULTY",
        value="medium",
        schema={
            "type": "string",
            "enum": ["easy", "medium", "hard"]
        }
    )

架构验证
~~~~~~~

定义验证架构::

    schema = {
        "app": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "version": {"type": "string"},
                "debug": {"type": "boolean"}
            },
            "required": ["name", "version"]
        },
        "ai": {
            "type": "object",
            "properties": {
                "difficulty": {
                    "type": "string",
                    "enum": ["easy", "medium", "hard"]
                },
                "thinking_time": {
                    "type": "number",
                    "minimum": 0.1,
                    "maximum": 10.0
                }
            }
        }
    }
    
    # 使用自定义架构验证
    validator.set_schema(schema)
    result = validator.validate_file("config.yaml")

类型检查
~~~~~~~

内置类型检查::

    from gomoku_world.config.validation import TypeChecker
    
    # 创建类型检查器
    checker = TypeChecker()
    
    # 检查类型
    is_valid = checker.check_type("AI_THINKING_TIME", 2.0, float)
    
    # 检查范围
    is_valid = checker.check_range("AI_THINKING_TIME", 2.0, 0.1, 10.0)
    
    # 检查枚举值
    is_valid = checker.check_enum("AI_DIFFICULTY", "medium",
                                ["easy", "medium", "hard"])

自定义验证规则
~~~~~~~~~~~

创建自定义验证器::

    from gomoku_world.config.validation import BaseValidator
    
    class CustomValidator(BaseValidator):
        def validate_port(self, value):
            """验证端口号"""
            if not isinstance(value, int):
                return False, "端口必须是整数"
            if not 1 <= value <= 65535:
                return False, "端口必须在1-65535之间"
            return True, None
    
    # 使用自定义验证器
    validator = CustomValidator()
    is_valid, error = validator.validate_port(8080)

验证命令行工具
-----------

使用命令行工具验证配置::

    # 验证配置文件
    python -m gomoku_world.config.validation config.yaml
    
    # 显示详细信息
    python -m gomoku_world.config.validation config.yaml --verbose
    
    # 生成验证报告
    python -m gomoku_world.config.validation config.yaml --report

配置检查器
--------

使用配置检查器::

    from gomoku_world.config.checker import ConfigChecker
    
    # 创建检查器
    checker = ConfigChecker()
    
    # 运行所有检查
    results = checker.run_all_checks()
    
    # 运行特定检查
    results = checker.run_checks([
        "check_types",
        "check_dependencies",
        "check_paths"
    ])

内置检查项：

1. 类型检查::

    checker.check_types()

2. 依赖检查::

    checker.check_dependencies()

3. 路径检查::

    checker.check_paths()

4. 权限检查::

    checker.check_permissions()

5. 环境变量检查::

    checker.check_environment()

配置监控
-------

使用配置监控器::

    from gomoku_world.config.monitor import ConfigMonitor
    
    # 创建监控器
    monitor = ConfigMonitor()
    
    # 启动监控
    monitor.start()
    
    # 获取监控数据
    stats = monitor.get_stats()
    
    # 导出报告
    monitor.export_report("monitor_report.json")

监控指标：

1. 访问频率
2. 配置变更
3. 验证失败
4. 性能指标

配置测试
-------

编写配置测试::

    import pytest
    from gomoku_world.config.testing import ConfigTester
    
    def test_config_validation():
        tester = ConfigTester()
        
        # 测试基本配置
        assert tester.test_basic_config()
        
        # 测试AI配置
        assert tester.test_ai_config()
        
        # 测试网络配置
        assert tester.test_network_config()

运行配置测试::

    # 运行所有配置测试
    pytest tests/config/
    
    # 运行特定测试
    pytest tests/config/test_validation.py

最佳实践
-------

1. 在CI/CD流程中包含配置验证
2. 为每个环境维护单独的验证规则
3. 定期运行完整性检查
4. 记录验证结果
5. 自动化验证过程

故障排除
-------

常见验证错误：

1. 类型不匹配::

    # 检查类型错误
    validator.check_type_mismatch(value, expected_type)

2. 范围错误::

    # 检查范围错误
    validator.check_range_error(value, min_val, max_val)

3. 缺少必需项::

    # 检查必需项
    validator.check_required_fields(config_dict)

4. 格式错误::

    # 检查格式
    validator.check_format(value, format_pattern)

获取帮助
-------

如果遇到问题：

1. 查看验证日志
2. 使用调试模式
3. 检查验证规则
4. 参考示例配置 