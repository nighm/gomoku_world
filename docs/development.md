# Development Guide / 开发指南

## Overview / 概述

This document provides detailed information for developers who want to contribute to the Gomoku game project.
本文档为想要参与五子棋游戏项目开发的开发者提供详细信息。

## Development Environment / 开发环境

### Requirements / 要求

- Python 3.8+ / Python 3.8或更高版本
- Pygame 2.5.2 / Pygame 2.5.2
- psutil 5.9.0+ / psutil 5.9.0或更高版本
- A code editor (VS Code recommended) / 代码编辑器（推荐使用VS Code）

### Setup / 环境搭建

1. Clone the repository / 克隆仓库
```bash
git clone https://github.com/yourusername/gomoku.git
cd gomoku
```

2. Create a virtual environment / 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies / 安装依赖
```bash
pip install -r requirements.txt
```

## Project Structure / 项目结构

### Core Components / 核心组件

1. Game Logic (`game.py`) / 游戏逻辑
   - Board management / 棋盘管理
   - Move validation / 落子验证
   - Win condition checking / 胜利条件检查

2. GUI (`gui.py`) / 图形界面
   - Window management / 窗口管理
   - Event handling / 事件处理
   - Drawing routines / 绘图程序

3. Settings Menu (`settings_menu.py`) / 设置菜单
   - Game configuration / 游戏配置
   - User preferences / 用户偏好

4. Debug System (`debug.py`) / 调试系统
   - Performance monitoring / 性能监控
   - Debug information display / 调试信息显示
   - Debug snapshot creation / 调试快照创建

5. Logging System (`logger.py`) / 日志系统
   - Log file management / 日志文件管理
   - Session logging / 会话日志
   - Log rotation / 日志轮转

6. Internationalization (`i18n.py`) / 国际化
   - Language management / 语言管理
   - Translation system / 翻译系统

7. Sound System (`sound.py`) / 音效系统
   - Sound effect management / 音效管理
   - Volume control / 音量控制

## Coding Standards / 编码标准

### Python Style Guide / Python风格指南

- Follow PEP 8 / 遵循PEP 8规范
- Use type hints / 使用类型提示
- Document all functions and classes / 为所有函数和类编写文档
- Keep functions focused and small / 保持函数专注且简短
- Use meaningful variable names / 使用有意义的变量名

### Documentation / 文档

- Use docstrings for all public APIs / 为所有公共API使用文档字符串
- Include both English and Chinese comments / 包含中英文注释
- Keep documentation up to date / 保持文档更新

### Logging / 日志记录

- Use appropriate log levels / 使用适当的日志级别
  - DEBUG: Detailed information / 详细信息
  - INFO: General information / 一般信息
  - WARNING: Warning messages / 警告信息
  - ERROR: Error messages / 错误信息
  - CRITICAL: Critical issues / 严重问题

- Include context in log messages / 在日志消息中包含上下文
- Log all significant events / 记录所有重要事件

## Testing / 测试

### Unit Tests / 单元测试

- Write tests for all new features / 为所有新功能编写测试
- Maintain test coverage / 维护测试覆盖率
- Run tests before committing / 提交前运行测试

### Debug Mode / 调试模式

- Use F3-F6 keys for debugging / 使用F3-F6键进行调试
- Check performance metrics / 检查性能指标
- Create debug snapshots when needed / 在需要时创建调试快照

## Contributing / 贡献

1. Create a new branch / 创建新分支
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes / 进行修改
   - Follow coding standards / 遵循编码标准
   - Add tests / 添加测试
   - Update documentation / 更新文档

3. Commit your changes / 提交修改
```bash
git commit -m "Add: detailed description of your changes"
```

4. Push to your branch / 推送到分支
```bash
git push origin feature/your-feature-name
```

5. Create a Pull Request / 创建Pull Request

## Release Process / 发布流程

1. Version Bump / 版本更新
   - Update version number / 更新版本号
   - Update changelog / 更新更新日志

2. Testing / 测试
   - Run all tests / 运行所有测试
   - Perform manual testing / 执行手动测试

3. Documentation / 文档
   - Update documentation / 更新文档
   - Review changes / 审查更改

4. Release / 发布
   - Create release tag / 创建发布标签
   - Update release notes / 更新发布说明 