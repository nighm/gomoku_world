# API Changelog / API版本历史

## Overview / 概述
This document tracks all notable API changes in GomokuWorld.
本文档记录GomokuWorld中所有重要的API变更。

## [1.3.0] - 2024-02-21

### Added / 新增
- Platform API / 平台API
  - `PlatformBase` class with platform-specific implementations / 带有平台特定实现的`PlatformBase`类
  - Font detection and management / 字体检测和管理
  - Resource path handling / 资源路径处理
  - Configuration management / 配置管理

- Resource Management API / 资源管理API
  - `ResourceManager` class for centralized resource handling / 用于集中资源处理的`ResourceManager`类
  - Theme management system / 主题管理系统
  - Internationalization support / 国际化支持
  - Resource caching mechanism / 资源缓存机制

- AI System API / AI系统API
  - Enhanced MinMax strategy with alpha-beta pruning / 增强的MinMax策略，带有alpha-beta剪枝
  - MCTS strategy implementation / MCTS策略实现
  - Position evaluation system / 位置评估系统

### Changed / 变更
- Game API / 游戏API
  - Improved board state management / 改进的棋盘状态管理
  - Enhanced move validation / 增强的移动验证
  - Better win condition checking / 更好的胜利条件检查

- Resource API / 资源API
  - Refactored resource loading / 重构的资源加载
  - Optimized asset management / 优化的资源管理
  - Enhanced error handling / 增强的错误处理

### Deprecated / 弃用
- Old resource loading methods / 旧的资源加载方法
- Legacy platform detection / 旧的平台检测
- Outdated AI interfaces / 过时的AI接口

## [1.2.0] - 2024-02-21

### Added / 新增
- Documentation API / 文档API
  - API reference generation / API参考生成
  - Interactive examples / 交互示例
  - Code snippets / 代码片段

- Configuration API / 配置API
  - Schema validation / 模式验证
  - Migration support / 迁移支持
  - Environment variables / 环境变量

### Changed / 变更
- Project structure / 项目结构
  - Module organization / 模块组织
  - Package layout / 包布局
  - Import paths / 导入路径

### Fixed / 修复
- API consistency issues / API一致性问题
- Documentation errors / 文档错误
- Type hints / 类型提示

## [1.1.0] - 2024-02-22

### Added / 新增
- Validation API / 验证API
  - Input validation / 输入验证
  - State validation / 状态验证
  - Error reporting / 错误报告

### Changed / 变更
- Error handling / 错误处理
  - Exception hierarchy / 异常层次
  - Error messages / 错误消息
  - Recovery mechanisms / 恢复机制

### Deprecated / 弃用
- Legacy error codes / 旧的错误代码
- Outdated validation methods / 过时的验证方法

## [1.0.0] - 2024-02-21

### Added / 新增
- Core Game API / 核心游戏API
  - Board management / 棋盘管理
  - Game logic / 游戏逻辑
  - Player management / 玩家管理

- AI API / AI API
  - Strategy interface / 策略接口
  - Evaluation system / 评估系统
  - Decision making / 决策制定

- Network API / 网络API
  - Connection handling / 连接处理
  - State synchronization / 状态同步
  - Message protocol / 消息协议

### Changed / 变更
- Initial stable release / 初始稳定版本

## Migration Guide / 迁移指南

### 1.2.x to 1.3.0
- Update platform-specific code / 更新平台特定代码
- Migrate to new resource management / 迁移到新的资源管理
- Adapt to enhanced AI interfaces / 适应增强的AI接口

### 1.1.x to 1.2.0
- Update project structure / 更新项目结构
- Implement new validation rules / 实现新的验证规则
- Migrate configuration format / 迁移配置格式

### 1.0.x to 1.1.0
- Update error handling / 更新错误处理
- Implement new validation / 实现新的验证
- Migrate legacy code / 迁移旧代码

## Compatibility Notes / 兼容性说明

### Version 1.3.0
- Requires Python 3.8+ / 需要Python 3.8+
- Platform-specific features / 平台特定功能
- Enhanced AI capabilities / 增强的AI功能

### Version 1.2.0
- Documentation updates / 文档更新
- Configuration changes / 配置变更
- Structure improvements / 结构改进

### Version 1.1.0
- Validation enhancements / 验证增强
- Error handling improvements / 错误处理改进
- Legacy support / 旧版本支持

### Version 1.0.0
- Initial stable API / 初始稳定API
- Core functionality / 核心功能
- Basic features / 基本功能 