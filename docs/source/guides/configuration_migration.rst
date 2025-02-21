配置迁移指南
============

本指南将帮助您在不同版本之间迁移配置。

版本迁移路径
----------

1.0.x 到 1.1.x
~~~~~~~~~~~~~

主要变更：

* 配置文件格式从INI改为YAML
* 新增AI配置选项
* 修改了部分配置键名

迁移步骤::

    from gomoku_world.config.instances import config_manager
    from gomoku_world.utils.migration import ConfigMigrator
    
    # 创建迁移器
    migrator = ConfigMigrator()
    
    # 执行迁移
    migrator.migrate_from_1_0_to_1_1("old_config.ini", "new_config.yaml")

自动迁移工具会处理以下转换：

* 将 ``AI_LEVEL`` 转换为 ``AI_DIFFICULTY``
* 将 ``SAVE_DIR`` 更新为新的默认位置
* 添加新的必需配置项

手动迁移步骤：

1. 备份原有配置::

    cp config.ini config.ini.bak

2. 转换配置格式::

    # 旧格式
    [AI]
    level = medium
    
    # 新格式
    ai:
      difficulty: medium

3. 更新配置键名::

    # 旧键名 -> 新键名
    AI_LEVEL -> AI_DIFFICULTY
    SAVE_PATH -> SAVE_DIR
    LOG_PATH -> LOG_DIR

4. 添加新的必需配置项::

    ai:
      difficulty: medium
      thinking_time: 2.0
      cache_size: 1000

5. 验证新配置::

    from gomoku_world.config.instances import config_manager
    
    # 验证新配置
    is_valid = config_manager.validate_config("new_config.yaml")
    print(f"配置验证结果: {is_valid}")

0.9.x 到 1.0.x
~~~~~~~~~~~~~

主要变更：

* 添加了环境变量支持
* 重构了配置结构
* 新增了网络配置选项

迁移步骤::

    from gomoku_world.config.instances import config_manager
    from gomoku_world.utils.migration import ConfigMigrator
    
    # 创建迁移器
    migrator = ConfigMigrator()
    
    # 执行迁移
    migrator.migrate_from_0_9_to_1_0("old_config.json", "new_config.yaml")

自动化迁移
---------

使用迁移助手::

    from gomoku_world.utils.migration import MigrationAssistant
    
    # 创建迁移助手
    assistant = MigrationAssistant()
    
    # 检测当前配置版本
    current_version = assistant.detect_version("config.yaml")
    
    # 获取迁移建议
    suggestions = assistant.get_migration_suggestions(current_version)
    
    # 执行自动迁移
    success = assistant.auto_migrate("config.yaml")

配置备份
-------

迁移前自动备份::

    from gomoku_world.utils.backup import ConfigBackup
    
    # 创建备份
    backup = ConfigBackup()
    
    # 备份当前配置
    backup_path = backup.create("config.yaml")
    
    # 如果需要，还原配置
    backup.restore(backup_path)

故障排除
-------

如果迁移过程中遇到问题：

1. 检查日志文件获取详细错误信息
2. 使用 ``--debug`` 参数运行迁移工具获取更多信息
3. 确保所有必需的配置项都已正确设置
4. 验证配置文件格式是否正确

最佳实践
-------

1. 始终在迁移前备份配置
2. 使用版本控制管理配置文件
3. 在测试环境中先进行迁移测试
4. 保持配置文件的结构清晰
5. 记录所有的配置更改

配置模板
-------

为了帮助迁移，这里提供了各版本的配置模板：

1.1.x 模板::

    # 基本设置
    app:
      name: "Gomoku World"
      version: "1.1.0"
      debug: false
    
    # AI设置
    ai:
      difficulty: "medium"
      thinking_time: 2.0
      cache_size: 1000
    
    # 存储设置
    storage:
      save_dir: "saves"
      log_dir: "logs"
    
    # 网络设置
    network:
      host: "localhost"
      port: 5000
      max_connections: 1000

1.0.x 模板::

    [APP]
    name = Gomoku World
    version = 1.0.0
    debug = false
    
    [AI]
    level = medium
    
    [STORAGE]
    save_path = saves
    log_path = logs
    
    [NETWORK]
    host = localhost
    port = 5000 