# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.3] - 2024-03-21

### Changed
- 优化AI缓存系统，提升性能 / Optimized AI caching system for better performance
- 改进日志记录，增加更多调试信息 / Improved logging with more debug information

## [2.1.2] - 2024-03-20

### Changed
- 重构AI模块架构，提升代码可维护性 / Refactored AI module architecture for better maintainability
- 优化AI搜索算法，提高性能 / Optimized AI search algorithm for better performance
- 改进AI策略评估系统 / Improved AI strategy evaluation system
- 更新API文档以反映最新变更 / Updated API documentation to reflect latest changes

### Added
- 新增AI难度动态调整功能 / Added dynamic AI difficulty adjustment
- 增强AI决策树剪枝算法 / Enhanced AI decision tree pruning algorithm

## [1.4.6] - 2024-03-15

### Changed
- 优化AI评估结果缓存机制，提高决策效率 / Optimized AI evaluation result caching mechanism for better decision efficiency
- 改进AI节点计数器，更准确地追踪搜索性能 / Improved AI node counter for more accurate search performance tracking
- 优化缓存清理机制，防止内存占用过高 / Enhanced cache cleaning mechanism to prevent excessive memory usage

## [2.0.0] - 2024-03-15

### Breaking Changes
- 完整重构配置系统，提供更强大的验证和迁移功能 / Complete configuration system refactoring with enhanced validation and migration
- 重新设计国际化系统架构，支持更多语言和动态加载 / Redesigned i18n system architecture with more languages and dynamic loading
- API接口重大更新，提供更好的类型提示和错误处理 / Major API updates with better type hints and error handling
- 文档系统全面更新，提供更完整的开发指南和示例 / Comprehensive documentation update with complete development guides and examples

### Added
- 新增配置验证系统 / New configuration validation system
- 新增配置迁移工具 / New configuration migration tools
- 新增多语言动态加载支持 / Added dynamic multi-language loading support
- 新增完整的开发者文档和教程 / Added complete developer documentation and tutorials
- 新增更多单元测试和集成测试 / Added more unit tests and integration tests

### Changed
- 优化了配置管理器的性能 / Optimized configuration manager performance
- 改进了国际化系统的缓存机制 / Improved i18n system caching mechanism
- 更新了所有文档结构和内容 / Updated all documentation structure and content
- 改进了错误处理机制 / Improved error handling mechanism

### Removed
- 移除了旧版配置系统 / Removed old configuration system
- 移除了过时的国际化接口 / Removed deprecated i18n interfaces
- 移除了不推荐使用的API / Removed deprecated APIs

For detailed release notes, see:
- [User Release Notes](docs/release_notes/v2.0.0.user.md)
- [Developer Notes](docs/release_notes/v2.0.0.dev.md)

[2.0.0]: https://github.com/gomokuworld/gomoku_world/releases/tag/v2.0.0

## [1.4.6] - 2025-03-01

### Added
- Enhanced configuration management system:
  - Unified configuration interface
  - YAML-based configuration files
  - Dot notation for nested values
  - Configuration validation
  - Automatic configuration merging
  - Bilingual documentation
- Comprehensive test suite for configuration system
- Configuration validation tools
- Configuration migration utilities
- Configuration documentation and examples

### Changed
- Reorganized configuration system structure
- Improved error handling and reporting
- Enhanced configuration validation
- Updated documentation with configuration examples
- Optimized configuration loading performance

### Fixed
- Configuration loading issues
- Configuration validation errors
- Configuration merge conflicts
- Documentation inconsistencies

For detailed release notes, see:
- [User Release Notes](docs/release_notes/v1.4.6.user.md)
- [Developer Notes](docs/release_notes/v1.4.6.dev.md)

[1.4.6]: https://github.com/gomokuworld/gomoku_world/releases/tag/v1.4.6

## [1.4.5] - 2025-02-22

### Added
- Comprehensive internationalization (i18n) support:
  - Multiple translation file formats (JSON, YAML, INI)
  - Advanced string formatting with error handling
  - Memory caching with TTL support
  - Translation management tools
  - Bilingual text display
  - Network-aware translation loading
- Translation management command line tool (`gomoku-i18n`)
- New translation categories: common, game, network, error, and UI
- Real-time language switching functionality
- Enhanced network status monitoring
- Detailed release notes for different user types

### Changed
- Reorganized project structure for better maintainability
- Improved resource file organization
- Enhanced error handling and reporting
- Updated documentation and examples
- Optimized translation loading performance

### Fixed
- Translation loading issues in offline mode
- UI refresh problems during language switching
- Network status update delays
- Various localization string formatting issues

For detailed release notes, see:
- [User Release Notes](docs/release_notes/v1.4.5.user.md)
- [Beginner Developer Notes](docs/release_notes/v1.4.5.dev.beginner.md)

[1.4.5]: https://github.com/gomokuworld/gomoku_world/releases/tag/v1.4.5

## [1.4.4] - 2025-02-15

### Added
- Basic internationalization support
- Network status monitoring
- Example programs for features

### Changed
- Updated project dependencies
- Improved error handling
- Enhanced documentation

### Fixed
- Various bug fixes and improvements

[1.4.4]: https://github.com/gomokuworld/gomoku_world/releases/tag/v1.4.4

## [1.4.3] - 2025-02-08

### Added
- Initial release with basic features
- Game core functionality
- Simple UI implementation
- Basic network support

[1.4.3]: https://github.com/gomokuworld/gomoku_world/releases/tag/v1.4.3