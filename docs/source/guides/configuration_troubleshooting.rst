配置故障排除指南
==============

本指南帮助您解决在使用五子棋世界时可能遇到的配置问题。

常见问题
-------

配置文件无法加载
~~~~~~~~~~~~~

症状：
  * 程序启动时报错 "无法加载配置文件"
  * 配置更改没有生效

解决方案：

1. 检查文件权限::

    # Windows
    icacls config.yaml
    
    # Linux/macOS
    ls -l config.yaml

2. 验证文件格式::

    from gomoku_world.config.instances import config_manager
    
    try:
        config_manager.validate_config("config.yaml")
    except Exception as e:
        print(f"配置文件格式错误: {e}")

3. 确认文件位置::

    from gomoku_world.config import ROOT_DIR
    
    expected_path = ROOT_DIR / "config.yaml"
    print(f"配置文件应位于: {expected_path}")

环境变量问题
~~~~~~~~~~

症状：
  * 环境变量设置未生效
  * 出现环境变量相关的警告

解决方案：

1. 检查环境变量设置::

    import os
    
    # 打印所有环境变量
    for key, value in os.environ.items():
        if key.startswith("GOMOKU_"):
            print(f"{key}: {value}")

2. 验证.env文件::

    from dotenv import load_dotenv
    
    # 加载并验证.env文件
    load_dotenv(verbose=True)

3. 环境变量优先级::

    # 系统环境变量 > .env文件 > 默认值
    from gomoku_world.config.instances import config_manager
    
    value = config_manager.get_value("DEBUG", source="env")
    print(f"当前值: {value}")
    print(f"来源: {config_manager.get_value_source('DEBUG')}")

配置值类型错误
~~~~~~~~~~~

症状：
  * 配置值类型转换错误
  * 数值范围错误

解决方案：

1. 检查配置值类型::

    from gomoku_world.config.instances import config_manager
    
    # 获取配置架构
    schema = config_manager.get_schema()
    
    # 验证特定配置值
    value = config_manager.get_value("AI_THINKING_TIME")
    expected_type = schema["AI_THINKING_TIME"]["type"]
    print(f"期望类型: {expected_type}, 实际类型: {type(value)}")

2. 数值范围验证::

    # 验证数值范围
    def validate_value_range(key, value):
        schema = config_manager.get_schema()
        if key in schema:
            min_val = schema[key].get("min")
            max_val = schema[key].get("max")
            if min_val is not None and value < min_val:
                return False, f"值小于最小值 {min_val}"
            if max_val is not None and value > max_val:
                return False, f"值大于最大值 {max_val}"
        return True, "值在有效范围内"

配置冲突
~~~~~~~

症状：
  * 多个配置源之间的值冲突
  * 配置覆盖问题

解决方案：

1. 检查配置来源::

    from gomoku_world.config.instances import config_manager
    
    # 获取所有配置源
    sources = config_manager.get_config_sources()
    
    # 检查特定配置的所有来源
    value_sources = config_manager.get_value_sources("DEBUG")
    print(f"配置来源: {value_sources}")

2. 解决配置冲突::

    # 手动设置配置优先级
    config_manager.set_source_priority([
        "env",
        "file",
        "default"
    ])

3. 合并配置::

    # 合并多个配置文件
    config_manager.merge_configs([
        "config.base.yaml",
        "config.local.yaml"
    ])

性能问题
~~~~~~~

症状：
  * 配置加载速度慢
  * 频繁的配置访问导致性能下降

解决方案：

1. 启用配置缓存::

    from gomoku_world.config.instances import config_manager
    
    # 启用缓存
    config_manager.enable_cache()
    
    # 设置缓存大小
    config_manager.set_cache_size(1000)

2. 使用配置预加载::

    # 预加载常用配置
    config_manager.preload_keys([
        "AI_DIFFICULTY",
        "NETWORK_HOST",
        "NETWORK_PORT"
    ])

3. 监控配置访问::

    # 启用配置访问监控
    config_manager.enable_monitoring()
    
    # 获取访问统计
    stats = config_manager.get_access_stats()
    print(f"配置访问统计: {stats}")

调试技巧
-------

1. 启用调试模式::

    from gomoku_world.config.instances import config_manager
    
    # 启用配置调试
    config_manager.enable_debug()
    
    # 获取详细日志
    config_manager.set_log_level("DEBUG")

2. 配置转储::

    # 导出当前配置
    config_manager.dump_config("debug_config.yaml")
    
    # 打印配置差异
    config_manager.print_config_diff("config1.yaml", "config2.yaml")

3. 配置验证::

    # 运行完整性检查
    config_manager.run_integrity_check()
    
    # 验证配置依赖
    config_manager.validate_dependencies()

最佳实践
-------

1. 使用配置验证工具
2. 保持配置文件的版本控制
3. 定期备份配置
4. 使用环境特定的配置文件
5. 记录配置更改

配置恢复
-------

如果配置出现问题，可以：

1. 还原到默认配置::

    config_manager.reset_to_defaults()

2. 从备份恢复::

    config_manager.restore_from_backup("backup_2024_01_01.yaml")

3. 重新生成配置::

    config_manager.regenerate_config()

安全注意事项
----------

1. 不要在配置文件中存储敏感信息
2. 使用环境变量存储密钥
3. 限制配置文件的访问权限
4. 定期审查配置安全性

获取帮助
-------

如果您仍然遇到问题：

1. 查看详细日志
2. 使用配置诊断工具
3. 查阅文档
4. 寻求社区支持 