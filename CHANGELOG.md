# Changelog

All notable changes to GomokuWorld will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.5] - 2024-03-22

> 详细的版本说明请查看：
> - [用户版本说明](docs/release_notes/v1.4.5.user.md)
> - [初级开发版本说明](docs/release_notes/v1.4.5.dev.beginner.md)
> - [专业开发版本说明](docs/release_notes/v1.4.5.dev.professional.md)

> For detailed release notes, please see:
> - [User Release Notes](docs/release_notes/v1.4.5.user.md)
> - [Beginner Developer Release Notes](docs/release_notes/v1.4.5.dev.beginner.md)
> - [Professional Developer Release Notes](docs/release_notes/v1.4.5.dev.professional.md)

### 主要更新 / Major Updates
- 优化项目目录结构 / Optimized project directory structure
- 统一国际化资源管理 / Unified internationalization resource management
- 清理冗余文件和目录 / Cleaned up redundant files and directories

### 改进 / Improvements
- 统一虚拟环境管理 / Unified virtual environment management
- 优化源代码组织结构 / Improved source code organization
- 规范化项目文件布局 / Standardized project file layout

### 清理 / Cleanup
- 移除重复的配置文件 / Removed duplicate configuration files
- 整理临时文件和脚本 / Organized temporary files and scripts
- 规范化资源目录结构 / Standardized resource directory structure

## [1.4.4] - 2024-03-21

> 详细的版本说明请查看：
> - [用户版本说明](docs/release_notes/v1.4.4.user.md)
> - [初级开发版本说明](docs/release_notes/v1.4.4.dev.beginner.md)
> - [专业开发版本说明](docs/release_notes/v1.4.4.dev.professional.md)

> For detailed release notes, please see:
> - [User Release Notes](docs/release_notes/v1.4.4.user.md)
> - [Beginner Developer Release Notes](docs/release_notes/v1.4.4.dev.beginner.md)
> - [Professional Developer Release Notes](docs/release_notes/v1.4.4.dev.professional.md)

### 主要更新 / Major Updates
- 全新的用户指南系统 / New user guide system
- 优化的双语支持 / Enhanced bilingual support
- 改进的界面交互 / Improved interface interaction

### 改进 / Improvements
- 更清晰的文档结构 / Clearer documentation structure
- 更好的用户体验 / Better user experience
- 更完善的帮助系统 / Enhanced help system

### 修复 / Fixes
- 界面和显示问题 / Interface and display issues
- 文档和翻译问题 / Documentation and translation issues

### 文档更新 / Documentation Updates
- 全新的用户指南 / New User Guide
  - 新手入门教程，从零开始学习五子棋 / Beginner's tutorial for learning Gomoku from scratch
  - 详细的游戏规则说明，包含图解示例 / Detailed game rules with illustrated examples
  - 界面操作指南，帮助快速上手 / Interface operation guide for quick start
  - 常见问题解答，解决使用疑惑 / FAQ section to address common concerns

- 双语支持优化 / Bilingual Support Enhancement
  - 所有文档支持中英文对照 / All documentation available in both Chinese and English
  - 界面语言无缝切换 / Seamless interface language switching
  - 更准确的翻译内容 / More accurate translations
  - 本地化支持更完善 / Enhanced localization support

- 功能说明完善 / Feature Documentation
  - AI对战模式详细说明 / Detailed explanation of AI battle modes
  - 联机对战功能指南 / Online multiplayer feature guide
  - 录像回放使用说明 / Game replay feature instructions
  - 自定义设置详解 / Custom settings explanation

### 使用体验改进 / User Experience Improvements
- 更清晰的菜单结构 / Clearer menu structure
- 更直观的设置选项 / More intuitive setting options
- 更友好的错误提示 / Friendlier error messages

### 问题修复 / Bug Fixes
- 修复了一些界面显示问题 / Fixed some interface display issues
- 改进了语言切换的稳定性 / Improved language switching stability
- 优化了文档阅读体验 / Enhanced documentation reading experience
- 解决了部分翻译不准确的问题 / Resolved some translation inaccuracies

## [1.4.3] - 2024-02-22

### Added / 新增
- Network-aware internationalization / 网络感知的国际化系统
  - Online/offline mode detection / 在线/离线模式检测
  - Multi-layer translation loading strategy / 多层翻译加载策略
    - Local cache / 本地缓存
    - Remote translation service / 远程翻译服务
    - Bundled translations / 内置翻译
  - Thread-safe translation management / 线程安全的翻译管理
  - Network status monitoring / 网络状态监控
  - Automatic fallback mechanism / 自动回退机制

### Changed / 变更
- Enhanced translation loading / 增强的翻译加载
  - Improved caching mechanism / 改进的缓存机制
  - Better error handling / 更好的错误处理
  - Optimized network requests / 优化的网络请求
  - Smarter language detection / 更智能的语言检测

### Fixed / 修复
- Network-related issues / 网络相关问题
  - Connection timeout handling / 连接超时处理
  - Service unavailability handling / 服务不可用处理
  - Cache corruption recovery / 缓存损坏恢复
  - Network state transitions / 网络状态转换

## [1.4.2] - 2024-02-22

### Added / 新增
- Enhanced internationalization system / 增强的国际化系统
  - Standard language codes (ISO 639-1) / 标准语言代码（ISO 639-1）
  - Region codes (ISO 3166-1) / 地区代码（ISO 3166-1）
  - Language fallback mechanism / 语言回退机制
  - Resource categorization / 资源分类
  - Date and time localization / 日期和时间本地化
  - Number formatting / 数字格式化
  - Font family selection / 字体系列选择
- Structured translation resources / 结构化翻译资源
  - Common translations / 通用翻译
  - Game-specific translations / 游戏特定翻译
  - Multiple language support / 多语言支持
  - Region-specific variations / 地区特定变体

### Changed / 变更
- Improved i18n architecture / 改进的国际化架构
  - Centralized i18n management / 集中的国际化管理
  - Dynamic resource loading / 动态资源加载
  - Flexible text formatting / 灵活的文本格式化
  - Enhanced error handling / 增强的错误处理

## [1.4.1] - 2024-02-22

### Changed / 变更
- Enhanced version management system / 增强的版本管理系统
  - Migrated to setuptools_scm for automatic version management / 迁移到setuptools_scm实现自动版本管理
  - Centralized version handling through git tags / 通过git标签集中管理版本
  - Removed manual version update process / 移除手动版本更新流程
  - Improved version consistency across package / 改进整个包的版本一致性

## [1.4.0] - 2024-02-22

### Added / 新增
- Tutorial video generation system / 教程视频生成系统
  - Start game animation / 开始游戏动画
  - Making moves animation / 落子动画
  - Win conditions animation / 胜利条件动画
  - AI game animation / AI对战动画
  - Theme switch animation / 主题切换动画
- Video encoding improvements / 视频编码改进
  - MP4V codec support / MP4V编码器支持
  - Frame format optimization / 帧格式优化
  - Color space conversion / 色彩空间转换
- Animation utilities / 动画工具
  - Board animation helpers / 棋盘动画辅助函数
  - Menu animation effects / 菜单动画效果
  - Transition effects / 过渡效果

### Changed / 变更
- Enhanced video generation / 增强的视频生成
  - Improved frame handling / 改进的帧处理
  - Better color management / 更好的颜色管理
  - Optimized animation timing / 优化的动画时间
- Updated documentation / 更新的文档
  - Added tutorial video section / 添加教程视频部分
  - Enhanced animation documentation / 增强的动画文档
  - New video generation guide / 新的视频生成指南

### Fixed / 修复
- Video encoding issues / 视频编码问题
  - Frame format conversion / 帧格式转换
  - Color space handling / 色彩空间处理
  - Video writer configuration / 视频写入器配置
- Animation timing issues / 动画时间问题
  - Frame rate consistency / 帧率一致性
  - Animation duration control / 动画时长控制
  - Transition smoothness / 过渡平滑度

## [1.3.0] - 2024-02-21

### Added / 新增
- Platform-specific implementations / 平台特定实现
  - Windows platform support with native font detection / Windows平台支持，包含本地字体检测
  - Linux platform support with XDG base directory / Linux平台支持，遵循XDG基础目录规范
  - macOS platform support with native font handling / macOS平台支持，包含本地字体处理
  - Web platform support with resource bundling / Web平台支持，包含资源打包
  - Cross-platform configuration management / 跨平台配置管理
  - Platform-specific file path handling / 平台特定的文件路径处理
- Resource management system / 资源管理系统
  - Theme management with JSON configuration / 基于JSON配置的主题管理
  - Text resources with internationalization / 支持国际化的文本资源
  - Font management with fallback support / 带有备选方案的字体管理
  - Dynamic resource loading and hot reload / 动态资源加载和热重载
  - Resource caching and optimization / 资源缓存和优化
  - Resource validation and error handling / 资源验证和错误处理
- AI improvements / AI改进
  - MinMax strategy with alpha-beta pruning / 具有alpha-beta剪枝的MinMax策略
    - Dynamic search depth adjustment / 动态搜索深度调整
    - Move ordering optimization / 移动顺序优化
    - Position caching / 位置缓存
  - Monte Carlo Tree Search strategy / 蒙特卡洛树搜索策略
    - UCT-based node selection / 基于UCT的节点选择
    - Parallel simulation support / 并行模拟支持
    - Dynamic time management / 动态时间管理
  - Position evaluation system / 位置评估系统
    - Pattern-based evaluation / 基于模式的评估
    - Threat detection / 威胁检测
    - Dynamic score adjustment / 动态分数调整

### Changed / 变更
- Improved code organization / 改进的代码组织
  - Modular architecture design / 模块化架构设计
  - Clear dependency management / 清晰的依赖管理
  - Enhanced code reusability / 增强的代码重用性
- Enhanced resource loading / 增强的资源加载
  - Asynchronous resource loading / 异步资源加载
  - Progressive resource loading / 渐进式资源加载
  - Resource dependency management / 资源依赖管理
- Optimized AI performance / 优化的AI性能
  - Improved search efficiency / 改进的搜索效率
  - Better position evaluation / 更好的位置评估
  - Memory usage optimization / 内存使用优化
- Better platform compatibility / 更好的平台兼容性
  - Cross-platform file handling / 跨平台文件处理
  - Platform-specific optimizations / 平台特定优化
  - Unified platform interface / 统一的平台接口

### Fixed / 修复
- File encoding issues / 文件编码问题
  - UTF-8 encoding enforcement / 强制使用UTF-8编码
  - BOM handling / BOM处理
  - Line ending normalization / 行尾规范化
- Platform-specific path handling / 平台特定的路径处理
  - Path separator issues / 路径分隔符问题
  - Absolute path resolution / 绝对路径解析
  - Special path characters / 特殊路径字符
- Resource loading errors / 资源加载错误
  - Missing resource handling / 缺失资源处理
  - Invalid resource format / 无效资源格式
  - Resource fallback mechanism / 资源回退机制
- GUI initialization issues / GUI初始化问题
  - Window creation errors / 窗口创建错误
  - Widget initialization / 组件初始化
  - Event handling problems / 事件处理问题

## [1.2.0] - 2024-02-21

### Added / 新增
- Encoding fix utility scripts series (v1-v4) / 编码修复工具脚本系列（v1-v4）
  - Advanced encoding detection with retry mechanism / 具有重试机制的高级编码检测
  - Parallel processing support / 并行处理支持
  - Progress bar and detailed logging / 进度条和详细日志
  - Multiple encoding support / 多种编码支持
- New documentation sections / 新的文档部分
  - API reference documentation / API参考文档
  - Development guides / 开发指南
  - Configuration guides / 配置指南
  - Deployment documentation / 部署文档
  - Getting started tutorials / 入门教程
  - Advanced tutorials / 进阶教程

### Changed / 变更
- Enhanced project structure / 增强的项目结构
- Improved configuration management / 改进的配置管理
- Updated dependency management / 更新的依赖管理
- Enhanced multi-platform support / 增强的多平台支持
- Improved internationalization system / 改进的国际化系统
- Enhanced monitoring and profiling capabilities / 增强的监控和性能分析功能

### Fixed / 修复
- File encoding issues across the project / 项目中的文件编码问题
- Documentation formatting and structure / 文档格式和结构
- Platform-specific line ending issues / 平台特定的行尾问题

## [1.1.0] - 2024-02-22

### Added / 新增
- Comprehensive API documentation for all modules / 完整的模块API文档
- Configuration validation tool with schema support / 带有模式支持的配置验证工具
- Configuration migration guide / 配置迁移指南
- Configuration troubleshooting guide / 配置故障排除指南
- Performance optimization guide / 性能优化指南
- Security guide with best practices / 安全最佳实践指南
- Configuration best practices guide / 配置最佳实践指南

### Changed / 变更
- Enhanced documentation structure and organization / 增强的文档结构和组织
- Improved configuration file validation / 改进的配置文件验证
- Optimized performance monitoring system / 优化的性能监控系统
- Enhanced security measures / 增强的安全措施

### Fixed / 修复
- Configuration validation error handling / 配置验证错误处理
- Documentation formatting issues / 文档格式问题
- Performance monitoring accuracy / 性能监控准确性

## [1.0.0] - 2024-02-21

### Added / 新增
- Initial release of GomokuWorld / GomokuWorld初始版本发布
- Advanced AI system with multiple difficulty levels / 具有多个难度级别的高级AI系统
- Online multiplayer support / 在线多人游戏支持
- Modern UI with theme support / 支持主题的现代界面
- Internationalization (English/Chinese) / 国际化（英文/中文）
- Comprehensive metrics and monitoring / 全面的指标和监控
- Cloud save and sync functionality / 云存储和同步功能
- Tournament system / 比赛系统
- Kubernetes deployment support / Kubernetes部署支持
- Performance optimization tools / 性能优化工具

### Changed / 变更
- Complete project restructure / 完整的项目重构
- Enhanced build system / 增强的构建系统
- Improved documentation / 改进的文档

### Fixed / 修复
- Initial bug fixes and optimizations / 初始bug修复和优化

## [0.2.0] - 2024-03-21

### 新增 / Added
- 完整的项目文档结构
  - 新增中英文 README
  - 新增中英文目录结构说明
  - 新增完整的教程文档框架
- 详细的教程文档
  - 基础教程（游戏规则、环境配置等）
  - 进阶教程（AI开发、网络功能等）
  - 高级特性（性能优化、国际化等）
- 标准的项目结构
  - 优化源代码组织
  - 完善测试目录结构
  - 规范化资源管理

### 改进 / Improved
- 文档组织更加清晰
- 双语支持更加完善
- 目录结构更加规范
- 开发指南更加详细

### 修复 / Fixed
- 文档结构不清晰的问题
- 中英文内容不同步的问题
- 目录说明不完整的问题

## [0.1.0] - 2024-03-20

### 新增 / Added
- 项目基础框架
- 基本游戏功能
- 初始文档结构 