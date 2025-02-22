# 项目目录结构说明 / Project Directory Structure

## 1. 项目概览 / Project Overview

Gomoku World 项目采用标准的 Python 包结构，遵循模块化和关注点分离原则进行组织。主要分为源代码、测试、文档、资源等几个主要部分。

## 2. 目录结构 / Directory Structure

```
gomoku-world/                  # 项目根目录 / Project root
├── src/                      # 源代码目录 / Source code
├── tests/                    # 测试代码 / Tests
├── docs/                     # 文档 / Documentation
├── examples/                 # 示例代码 / Example code
├── scripts/                  # 脚本工具 / Scripts
├── resources/                # 资源文件 / Resources
├── locales/                  # 本地化文件 / Localization
├── deployment/               # 部署配置 / Deployment
└── tools/                    # 开发工具 / Development tools
```

## 3. 详细说明 / Detailed Description

### 3.1 源代码目录 (src/) / Source Code

```
src/gomoku_world/            # 主包 / Main package
├── core/                    # 核心游戏逻辑 / Core game logic
│   ├── __init__.py         # 包初始化
│   ├── board.py            # 棋盘类：棋盘状态管理、落子规则
│   ├── game.py             # 游戏类：游戏流程控制、胜负判定
│   └── player.py           # 玩家类：玩家信息、权限管理
│
├── ai/                     # AI 模块 / AI module
│   ├── __init__.py         # 包初始化
│   ├── engine.py           # AI引擎：整体控制和协调
│   ├── evaluate.py         # 评估函数：局势评估、棋型识别
│   └── search.py           # 搜索算法：极大极小、Alpha-Beta剪枝
│
├── gui/                    # 图形界面 / GUI
│   ├── __init__.py         # 包初始化
│   ├── window.py           # 主窗口：窗口管理、布局控制
│   ├── board.py            # 棋盘界面：棋盘绘制、交互处理
│   └── widgets/            # 自定义组件
│       ├── __init__.py
│       ├── timer.py        # 计时器组件
│       └── status.py       # 状态栏组件
│
├── network/                # 网络模块 / Network module
│   ├── __init__.py         # 包初始化
│   ├── client.py           # 客户端：连接管理、数据收发
│   ├── server.py           # 服务器：会话管理、请求处理
│   └── protocol.py         # 通信协议：消息格式、序列化
│
└── utils/                  # 工具函数 / Utilities
    ├── __init__.py         # 包初始化
    ├── logger.py           # 日志工具：日志配置、记录
    └── config.py           # 配置工具：配置加载、验证
```

### 3.2 测试目录 (tests/) / Tests

```
tests/
├── unit/                   # 单元测试 / Unit tests
│   ├── test_board.py       # 棋盘测试
│   ├── test_game.py        # 游戏逻辑测试
│   └── test_ai.py          # AI 功能测试
│
├── integration/            # 集成测试 / Integration tests
│   ├── test_gameplay.py    # 游戏流程测试
│   └── test_network.py     # 网络功能测试
│
└── performance/            # 性能测试 / Performance tests
    ├── test_ai_speed.py    # AI 性能测试
    └── test_network_load.py # 网络负载测试
```

### 3.3 文档目录 (docs/) / Documentation

```
docs/
├── index.md               # 文档首页：总体介绍
├── tutorials/             # 教程文档
│   ├── learning-path.md   # 学习路径
│   ├── environment-setup.md # 环境配置
│   ├── game-rules.md      # 游戏规则
│   └── ...
├── api/                   # API 文档
├── examples/              # 示例文档
└── faq/                   # 常见问题
```

### 3.4 示例目录 (examples/) / Examples

```
examples/
├── basic/                 # 基础示例
│   ├── simple_game.py     # 简单游戏示例
│   └── basic_ai.py        # 基础 AI 示例
├── advanced/              # 进阶示例
│   ├── custom_ai.py       # 自定义 AI 示例
│   └── network_game.py    # 网络对战示例
└── plugins/               # 插件示例
    └── custom_theme.py    # 自定义主题示例
```

### 3.5 资源目录 (resources/) / Resources

```
resources/
├── images/                # 图片资源
│   ├── board/            # 棋盘图片
│   └── pieces/           # 棋子图片
├── sounds/                # 音效资源
│   ├── move.wav          # 落子音效
│   └── win.wav           # 胜利音效
└── themes/                # 主题资源
    ├── default/          # 默认主题
    └── dark/             # 暗色主题
```

### 3.6 本地化目录 (locales/) / Localization

```
locales/
├── en/                    # 英文
│   └── LC_MESSAGES/
├── zh/                    # 中文
│   └── LC_MESSAGES/
└── ja/                    # 日文
    └── LC_MESSAGES/
```

### 3.7 部署目录 (deployment/) / Deployment

```
deployment/
├── docker/                # Docker 配置
│   ├── Dockerfile        # Docker 构建文件
│   └── docker-compose.yml # 容器编排配置
└── kubernetes/            # Kubernetes 配置
    └── deployment.yaml   # 部署配置文件
```

## 4. 特殊文件说明 / Special Files

### 4.1 配置文件 / Configuration Files
- `pyproject.toml`: 项目元数据、构建配置
- `setup.cfg`: 包配置、工具配置
- `requirements.txt`: 项目依赖
- `requirements-dev.txt`: 开发依赖

### 4.2 文档文件 / Documentation Files
- `README.md`: 项目说明（英文）
- `README.zh-CN.md`: 项目说明（中文）
- `CHANGELOG.md`: 版本历史
- `CONTRIBUTING.md`: 贡献指南
- `LICENSE`: 许可证

### 4.3 工具配置 / Tool Configuration
- `.gitignore`: Git 忽略规则
- `.pre-commit-config.yaml`: 预提交钩子
- `.editorconfig`: 编辑器配置
- `tox.ini`: 测试工具配置

## 5. 开发规范 / Development Guidelines

### 5.1 代码组织 / Code Organization
- 相关功能放在同一目录
- 保持目录结构清晰
- 遵循模块化原则

### 5.2 文件命名 / File Naming
- 使用小写字母
- 用下划线分隔单词
- 保持名称描述性

### 5.3 导入规范 / Import Guidelines
- 遵循相对导入原则
- 避免循环导入
- 保持导入路径清晰

### 5.4 资源管理 / Resource Management
- 资源文件放在 resources 目录
- 遵循资源分类原则
- 保持资源文件命名规范

## 6. 维护说明 / Maintenance Notes

### 6.1 目录更新 / Directory Updates
- 新功能应在适当位置创建目录
- 保持目录结构的一致性
- 及时更新目录文档

### 6.2 文档同步 / Documentation Sync
- 代码改动及时更新文档
- 保持中英文文档同步
- 维护示例代码的有效性

### 6.3 版本控制 / Version Control
- 遵循语义化版本规范
- 保持更新日志同步
- 维护分支管理策略 