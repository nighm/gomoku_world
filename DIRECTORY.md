# Gomoku World 项目目录结构 / Project Directory Structure

## 0. 文档说明 / Document Information

### 0.1 文档元信息 / Document Metadata
- 文档版本：1.4.6
- 更新日期：2025-03-01
- 文档状态：活跃维护
- 文档作者：Gomoku World Team
- 文档审核：Technical Committee
- 文档分类：项目结构说明
- 保密级别：公开

### 0.2 版本历史 / Version History
| 版本 | 日期 | 作者 | 更新说明 |
|------|------|------|----------|
| 1.4.6 | 2025-03-01 | Dev Team | 更新配置系统相关内容 |
| 1.4.5 | 2025-02-22 | Dev Team | 更新国际化系统相关内容 |
| 1.4.4 | 2025-02-15 | Dev Team | 初始版本 |

### 0.3 相关文档 / Related Documents
- [项目开发计划](docs/project_plan.md)
- [技术架构文档](docs/architecture.md)
- [API文档](docs/api/README.md)
- [发布说明](docs/release_notes/README.md)

## 1. 项目概览 / Project Overview

### 1.1 项目简介 / Project Introduction
Gomoku World 是一个现代化的五子棋游戏实现，采用 Python 语言开发。项目采用模块化设计，支持多语言，具备AI对战、网络对战等功能。

### 1.2 技术栈 / Technology Stack
- 开发语言：Python 3.8+
- GUI框架：PyQt6
- AI框架：PyTorch
- 构建工具：Poetry
- 测试框架：Pytest
- 文档工具：MkDocs

### 1.3 项目规模 / Project Scale
#### 1.3.1 目录统计 / Directory Statistics
- 一级目录：4个
- 二级目录：15个
- 三级目录：25个
- 总目录数：44个

#### 1.3.2 文件统计 / File Statistics
- Python源文件：42个
- 文档文件：35个
- 配置文件：12个
- 资源文件：68个
- 测试文件：28个
- 工具脚本：15个
- 总文件数：200个

#### 1.3.3 代码统计 / Code Statistics
- 源代码行数：15,000+
- 测试代码行数：5,000+
- 文档行数：8,000+
- 注释行数：3,000+

## 2. 目录结构详解 / Directory Structure Details

### 2.1 根目录结构 / Root Directory Structure
```
gomoku_world/              # 项目根目录
├── src/                  # 源代码目录
├── tests/               # 测试目录
├── docs/                # 文档目录
├── resources/           # 资源目录
├── scripts/             # 脚本工具目录
├── tools/               # 开发工具目录
├── deployment/          # 部署配置目录
├── build/               # 构建输出目录
├── bin/                 # 可执行文件目录
├── examples/            # 示例代码目录
├── logs/                # 日志目录
├── replays/             # 游戏回放目录
├── saves/               # 游戏存档目录
├── .github/             # GitHub配置目录
├── .cursor/             # 编辑器配置目录
└── venv/                # 虚拟环境目录
```

### 2.2 源代码目录 (src/) / Source Code Directory

#### 2.2.1 核心模块 / Core Modules
```
src/gomoku_world/
├── __init__.py           # 包初始化文件：定义公共接口和版本信息
├── _version.py          # 版本信息文件：定义版本号(1.4.6)
├── __main__.py          # 主入口文件：程序启动入口
├── constants.py         # 常量定义文件：全局常量
├── exceptions.py        # 异常定义文件：自定义异常
└── typing.py            # 类型定义文件：类型提示
```

#### 2.2.2 游戏核心 (core/) / Game Core
```
core/
├── __init__.py          # 核心模块初始化
├── board.py            # 棋盘实现：状态管理、基本操作
├── rules.py            # 规则实现：规则检查、胜负判定
├── game.py             # 游戏实现：流程控制、状态管理
├── player.py           # 玩家实现：玩家管理、权限控制
├── move.py             # 移动实现：走子记录、历史管理
├── timer.py            # 计时器实现：游戏计时功能
└── events.py           # 事件系统：游戏事件处理
```

#### 2.2.3 AI模块 (ai/) / AI Module
```
ai/
├── __init__.py          # AI模块初始化
├── engine.py           # AI引擎：决策控制
├── evaluation.py       # 评估系统：局势评估
├── search.py           # 搜索系统：路径搜索
├── mcts.py             # 蒙特卡洛树搜索实现
├── neural_net.py       # 神经网络实现
├── training/           # 训练相关实现
│   ├── __init__.py     # 训练模块初始化
│   ├── dataset.py     # 数据集处理
│   └── trainer.py     # 训练器实现
└── models/             # 模型定义目录
    ├── __init__.py     # 模型模块初始化
    ├── base.py        # 基础模型定义
    └── advanced.py    # 高级模型定义
```

#### 2.2.4 图形界面 (gui/) / GUI
```
gui/
├── __init__.py          # GUI模块初始化
├── main_window.py      # 主窗口实现
├── game_widget.py      # 游戏界面实现
├── menu_bar.py         # 菜单栏实现
├── toolbar.py          # 工具栏实现
├── dialogs/            # 对话框目录
│   ├── __init__.py     # 对话框初始化
│   ├── settings.py    # 设置对话框
│   ├── about.py       # 关于对话框
│   └── help.py        # 帮助对话框
├── widgets/            # 自定义控件目录
│   ├── __init__.py     # 控件初始化
│   ├── board.py       # 棋盘控件
│   ├── piece.py       # 棋子控件
│   ├── timer.py       # 计时器控件
│   └── status.py      # 状态栏控件
└── styles/             # 样式目录
    ├── __init__.py     # 样式初始化
    ├── default.py     # 默认样式
    └── dark.py        # 暗色样式
```

#### 2.2.5 配置系统 (config/) / Configuration System
```
config/
├── __init__.py          # 配置模块初始化
├── manager.py          # 配置管理器实现
├── base.py             # 基础配置类实现
├── validation.py       # 配置验证实现
├── migration.py        # 配置迁移工具
├── exceptions.py       # 配置异常定义
└── schemas/            # 配置模式目录
    ├── __init__.py     # 模式初始化
    ├── game.py        # 游戏配置模式
    ├── ai.py          # AI配置模式
    └── network.py     # 网络配置模式
```

#### 2.2.6 国际化 (i18n/) / Internationalization
```
i18n/
├── __init__.py          # 国际化模块初始化
├── manager.py          # 国际化管理器
├── translator.py       # 翻译器实现
├── cache.py            # 翻译缓存实现
├── loaders/            # 加载器目录
│   ├── __init__.py     # 加载器初始化
│   ├── base.py        # 基础加载器
│   ├── json.py        # JSON加载器
│   ├── yaml.py        # YAML加载器
│   └── ini.py         # INI加载器
├── formatters/         # 格式化器目录
│   ├── __init__.py     # 格式化器初始化
│   ├── base.py        # 基础格式化器
│   └── string.py      # 字符串格式化器
└── validators/         # 验证器目录
    ├── __init__.py     # 验证器初始化
    └── translation.py  # 翻译验证器
```

#### 2.2.7 网络模块 (network/) / Network Module
```
network/
├── __init__.py          # 网络模块初始化
├── client.py           # 客户端实现
├── server.py           # 服务器实现
├── protocol.py         # 协议定义
├── connection.py       # 连接管理
├── auth.py             # 认证实现
├── handlers/           # 处理器目录
│   ├── __init__.py     # 处理器初始化
│   ├── game.py        # 游戏处理器
│   └── chat.py        # 聊天处理器
└── security/           # 安全相关目录
    ├── __init__.py     # 安全模块初始化
    ├── encryption.py   # 加密实现
    └── validation.py   # 安全验证
```

#### 2.2.8 工具模块 (utils/) / Utility Module
```
utils/
├── __init__.py          # 工具模块初始化
├── logger.py           # 日志工具实现
├── resources.py        # 资源管理实现
├── network.py          # 网络工具实现
├── debug.py            # 调试工具实现
├── profiler.py         # 性能分析工具
├── decorators.py       # 装饰器工具
├── helpers/            # 辅助工具目录
│   ├── __init__.py     # 辅助工具初始化
│   ├── time.py        # 时间处理工具
│   └── format.py      # 格式化工具
└── testing/            # 测试工具目录
    ├── __init__.py     # 测试工具初始化
    ├── fixtures.py    # 测试夹具
    └── mocks.py       # 模拟对象
```

### 2.3 测试目录 (tests/) / Test Directory

#### 2.3.1 单元测试 / Unit Tests
```
tests/unit/
├── __init__.py          # 单元测试初始化
├── test_core/          # 核心模块测试
│   ├── __init__.py     # 测试初始化
│   ├── test_board.py  # 棋盘测试
│   ├── test_rules.py  # 规则测试
│   └── test_game.py   # 游戏测试
├── test_ai/            # AI模块测试
│   ├── __init__.py     # 测试初始化
│   ├── test_engine.py # 引擎测试
│   └── test_eval.py   # 评估测试
├── test_gui/           # GUI模块测试
├── test_config/        # 配置模块测试
├── test_i18n/          # 国际化模块测试
└── test_network/       # 网络模块测试
```

#### 2.3.2 集成测试 / Integration Tests
```
tests/integration/
├── __init__.py          # 集成测试初始化
├── test_gameplay.py    # 游戏流程测试
├── test_networking.py  # 网络功能测试
└── test_ai_game.py     # AI对战测试
```

#### 2.3.3 性能测试 / Performance Tests
```
tests/performance/
├── __init__.py          # 性能测试初始化
├── test_ai_speed.py    # AI性能测试
└── test_network_load.py # 网络负载测试
```

#### 2.3.4 测试资源 / Test Resources
```
tests/resources/
├── config/             # 测试配置文件
├── data/               # 测试数据文件
└── mocks/              # 模拟数据文件
```

### 2.4 文档目录 (docs/) / Documentation Directory

#### 2.4.1 用户文档 / User Documentation
```
docs/user/
├── getting_started/     # 入门指南
│   ├── installation.md # 安装说明
│   ├── quick_start.md  # 快速入门
│   └── tutorial.md     # 使用教程
├── features/           # 功能说明
│   ├── game_modes.md  # 游戏模式
│   ├── ai_levels.md   # AI难度
│   └── multiplayer.md # 多人游戏
└── faq/                # 常见问题
    ├── general.md     # 一般问题
    └── technical.md   # 技术问题
```

#### 2.4.2 开发者文档 / Developer Documentation
```
docs/dev/
├── setup/              # 环境搭建
│   ├── environment.md # 环境配置
│   └── tools.md       # 工具安装
├── architecture/       # 架构文档
│   ├── overview.md    # 架构概览
│   ├── core.md        # 核心架构
│   └── modules.md     # 模块说明
├── guides/            # 开发指南
│   ├── style.md      # 代码风格
│   ├── testing.md    # 测试指南
│   └── deployment.md # 部署指南
└── api/               # API文档
    ├── core.md       # 核心API
    ├── ai.md         # AI API
    └── network.md    # 网络API
```

#### 2.4.3 API文档 / API Documentation
```
docs/api/
├── reference/          # API参考
│   ├── core.md        # 核心API
│   ├── ai.md          # AI API
│   └── network.md     # 网络API
├── examples/          # API示例
│   ├── basic.md      # 基础示例
│   └── advanced.md   # 高级示例
└── changelog/         # API变更
    └── v1.x.md       # 1.x版本变更
```

#### 2.4.4 发布文档 / Release Documentation
```
docs/release/
├── notes/              # 发布说明
│   ├── v1.4.6.md     # 1.4.6版本说明
│   └── archive/      # 历史版本说明
├── migration/         # 迁移指南
│   └── v1.4.x.md     # 1.4.x迁移指南
└── roadmap/           # 开发计划
    └── 2025.md       # 2025年计划
```

### 2.5 资源目录 (resources/) / Resource Directory

#### 2.5.0 根目录配置 / Root Configuration
```
resources/
├── theme.json          # 全局主题配置
└── texts.json          # 全局文本配置
```

#### 2.5.1 配置目录 (config/) / Configuration Directory
```
resources/config/
├── __init__.py         # 配置包初始化
├── settings.py         # 设置定义
├── logging_config.py   # 日志配置
├── config.json         # 主配置文件
├── config.backup.json  # 配置备份
├── classic.json        # 经典主题配置
└── theme.json          # 主题配置
```

#### 2.5.2 国际化资源 (i18n/) / I18n Resources
```
resources/i18n/
├── en/                 # 英文资源
│   ├── common.json    # 通用文本
│   ├── game.json      # 游戏文本
│   ├── ui.json        # 界面文本
│   ├── error.json     # 错误文本
│   └── help.json      # 帮助文本
├── zh/                 # 中文资源
│   ├── common.json    # 通用文本
│   ├── game.json      # 游戏文本
│   ├── ui.json        # 界面文本
│   ├── error.json     # 错误文本
│   └── help.json      # 帮助文本
└── ja/                 # 日文资源
    └── ...            # 同上结构
```

#### 2.5.3 图像资源 (images/) / Image Resources
```
resources/images/
├── board/             # 棋盘图像
│   ├── default.png   # 默认棋盘
│   └── wood.png      # 木纹棋盘
├── pieces/            # 棋子图像
│   ├── black.png     # 黑子
│   └── white.png     # 白子
├── backgrounds/       # 背景图像
├── icons/            # 图标资源
└── animations/       # 动画资源
```

#### 2.5.4 音频资源 (sounds/) / Audio Resources
```
resources/sounds/
├── effects/           # 音效文件
│   ├── move.wav      # 落子音效
│   ├── win.wav       # 胜利音效
│   └── error.wav     # 错误音效
└── music/            # 背景音乐
    ├── menu.mp3      # 菜单音乐
    └── game.mp3      # 游戏音乐
```

#### 2.5.5 主题资源 (themes/) / Theme Resources
```
resources/themes/
├── default/           # 默认主题
│   ├── theme.json    # 主题配置
│   ├── colors.json   # 颜色定义
│   └── styles.css    # 样式表
├── dark/             # 暗色主题
│   └── ...          # 同上结构
└── custom/           # 自定义主题
    └── ...          # 同上结构
```

#### 2.5.6 通用资源 (assets/) / General Assets
```
resources/assets/
├── backgrounds/        # 背景资源
├── icons/             # 图标资源
└── animations/        # 动画资源
```

#### 2.5.7 字体资源 (fonts/) / Font Resources
```
resources/fonts/
├── default/           # 默认字体
│   ├── regular.ttf   # 常规字体
│   ├── bold.ttf      # 粗体字体
│   └── italic.ttf    # 斜体字体
└── special/          # 特殊字体
    └── game.ttf      # 游戏专用字体
```

### 2.6 脚本目录 (scripts/) / Script Directory
```
scripts/
├── client/             # 客户端脚本目录
│   ├── install.sh     # 客户端安装脚本
│   └── update.sh      # 客户端更新脚本
├── server/            # 服务器脚本目录
│   ├── deploy.sh      # 服务器部署脚本
│   └── monitor.sh     # 服务器监控脚本
├── dev/               # 开发脚本目录
│   ├── setup.sh       # 开发环境设置
│   └── test.sh        # 测试运行脚本
├── release/           # 发布脚本目录
│   ├── build.sh       # 构建脚本
│   └── publish.sh     # 发布脚本
├── utils/             # 工具脚本目录
│   ├── cleanup.sh     # 清理脚本
│   └── backup.sh      # 备份脚本
├── monitor/           # 监控脚本目录
│   ├── perf.sh        # 性能监控
│   └── health.sh      # 健康检查
├── backup/            # 备份脚本目录
│   ├── daily.sh       # 每日备份
│   └── weekly.sh      # 每周备份
├── check_bilingual_docs.py  # 双语文档检查
├── validate_translations.py  # 翻译验证
├── verify_i18n_integration.py # 国际化集成验证
└── generate_tutorials.py     # 教程生成
```

### 2.7 部署目录 (deployment/) / Deployment Directory
```
deployment/
├── docker/            # Docker配置
│   ├── Dockerfile    # Docker构建文件
│   └── compose.yml   # 容器编排配置
├── kubernetes/       # K8s配置
│   └── deploy.yml    # 部署配置
└── scripts/          # 部署脚本
    ├── deploy.sh     # 部署脚本
    └── rollback.sh   # 回滚脚本
```

### 2.8 GitHub配置目录 (.github/) / GitHub Configuration Directory
```
.github/
├── workflows/           # GitHub Actions工作流
│   ├── ci.yml          # 持续集成配置
│   ├── release.yml     # 发布工作流
│   └── docs.yml        # 文档部署工作流
├── linters/            # 代码检查配置
│   ├── python.yml      # Python检查配置
│   └── markdown.yml    # Markdown检查配置
├── ISSUE_TEMPLATE/     # Issue模板目录
│   ├── bug_report.md   # 错误报告模板
│   └── feature_request.md # 功能请求模板
├── CODEOWNERS          # 代码所有者配置
├── dependabot.yml      # 依赖更新配置
└── PULL_REQUEST_TEMPLATE.md # PR模板
```

### 2.9 示例目录 (examples/) / Examples Directory
```
examples/
├── i18n_demo.py        # 国际化功能示例
├── network_i18n_demo.py # 网络国际化示例
├── online_game.py      # 在线游戏示例
├── basic_game.py       # 基础游戏示例
└── ai_game.py          # AI游戏示例
```

### 2.10 日志目录 (logs/) / Logs Directory
```
logs/
├── gomoku_world.log    # 主日志文件
├── debug.log          # 调试日志文件
├── gomoku.log         # 游戏日志文件
├── archive/           # 日志归档目录
│   └── ...           # 历史日志文件
└── session_*.log      # 会话日志文件
```

### 2.11 游戏数据目录 / Game Data Directories

#### 2.11.1 回放目录 (replays/) / Replay Directory
```
replays/                # 游戏回放存储目录
├── pvp/               # 玩家对战回放
├── pve/               # AI对战回放
└── online/            # 在线对战回放
```

#### 2.11.2 存档目录 (saves/) / Save Directory
```
saves/                  # 游戏存档目录
├── auto/              # 自动存档
├── manual/            # 手动存档
└── temp/              # 临时存档
```

## 3. 特殊文件说明 / Special Files Description

### 3.1 配置文件 / Configuration Files
| 文件名 | 位置 | 用途 | 说明 |
|--------|------|------|------|
| setup.cfg | / | 项目配置 | 定义包信息和依赖 |
| pyproject.toml | / | 项目构建 | Poetry项目配置 |
| requirements.txt | / | 依赖管理 | 项目依赖列表 |
| requirements-dev.txt | / | 开发依赖 | 开发环境依赖列表 |
| tox.ini | / | 测试配置 | 测试环境配置 |
| .pre-commit-config.yaml | / | 代码检查 | 提交前检查配置 |
| MANIFEST.in | / | 包含文件 | 分发包含文件 |
| Makefile | / | 构建配置 | Make构建配置 |
| docker-compose.yml | / | Docker配置 | Docker编排配置 |
| Dockerfile | / | Docker配置 | Docker构建配置 |
| .env.example | / | 环境配置 | 环境变量示例 |

### 3.2 文档文件 / Documentation Files
| 文件名 | 位置 | 用途 | 说明 |
|--------|------|------|------|
| README.md | / | 项目说明 | 项目主要说明（英文）|
| README.zh-CN.md | / | 项目说明 | 项目主要说明（中文）|
| CHANGELOG.md | / | 更新日志 | 版本更新记录 |
| CONTRIBUTING.md | / | 贡献指南 | 项目贡献说明 |
| CODE_OF_CONDUCT.md | / | 行为准则 | 社区行为规范 |
| SECURITY.md | / | 安全策略 | 安全问题报告指南 |
| CITATION.cff | / | 引用配置 | 项目引用信息 |
| LICENSE | / | 许可证 | 项目许可说明 |
| DIRECTORY.md | / | 目录说明 | 项目结构说明（英文）|
| DIRECTORY.zh-CN.md | / | 目录说明 | 项目结构说明（中文）|

### 3.3 工具配置文件 / Tool Configuration Files
| 文件名 | 位置 | 用途 | 说明 |
|--------|------|------|------|
| .gitignore | / | Git配置 | Git忽略规则 |
| .gitmessage | / | Git配置 | 提交消息模板 |
| .editorconfig | / | 编辑器配置 | 编码风格配置 |
| .flake8 | / | 代码检查 | Flake8配置 |
| mypy.ini | / | 类型检查 | MyPy配置 |
| pytest.ini | / | 测试配置 | PyTest配置 |

## 4. 使用指南 / Usage Guide

### 4.1 开发环境设置 / Development Environment Setup
1. 克隆项目
```bash
git clone https://github.com/gomokuworld/gomoku_world.git
cd gomoku_world
```

2. 安装依赖
```bash
poetry install
```

3. 激活环境
```bash
poetry shell
```

### 4.2 项目构建 / Project Building
1. 运行测试
```bash
pytest
```

2. 构建包
```bash
poetry build
```

3. 本地安装
```bash
pip install -e .
```

### 4.3 文档生成 / Documentation Generation
1. 安装文档工具
```bash
poetry install --with docs
```

2. 生成文档
```bash
mkdocs build
```

3. 本地预览
```bash
mkdocs serve
```

## 5. 维护指南 / Maintenance Guide

### 5.1 代码维护 / Code Maintenance
1. 代码风格
   - 遵循PEP 8规范
   - 使用Black格式化
   - 通过MyPy类型检查

2. 测试要求
   - 单元测试覆盖率>80%
   - 集成测试覆盖关键路径
   - 定期运行性能测试

3. 文档要求
   - 及时更新API文档
   - 维护中英文文档同步
   - 示例代码保持最新

### 5.2 版本管理 / Version Management
1. 分支策略
   - main: 主分支
   - develop: 开发分支
   - feature/*: 功能分支
   - release/*: 发布分支
   - hotfix/*: 修复分支

2. 版本号规则
   - 主版本号: 不兼容的API修改
   - 次版本号: 向下兼容的功能性新增
   - 修订号: 向下兼容的问题修正

3. 发布流程
   - 更新版本号
   - 更新更新日志
   - 生成文档
   - 打包发布
   - 标记版本

### 5.3 资源维护 / Resource Maintenance
1. 资源组织
   - 按类型分类存储
   - 遵循命名规范
   - 保持目录结构清晰

2. 资源更新
   - 定期检查过期资源
   - 优化资源大小
   - 维护资源版本

3. 国际化维护
   - 及时更新翻译
   - 验证翻译完整性
   - 检查翻译质量

## 6. 附录 / Appendix

### 6.1 常用命令 / Common Commands
```bash
# 开发相关
poetry install          # 安装依赖
poetry run pytest      # 运行测试
poetry run black .     # 格式化代码
poetry run flake8     # 代码检查

# 文档相关
mkdocs serve          # 本地预览文档
mkdocs build         # 构建文档
mkdocs gh-deploy    # 部署到GitHub Pages

# 构建相关
poetry build         # 构建项目
poetry publish      # 发布到PyPI
```

### 6.2 相关资源 / Related Resources
- 项目主页：https://github.com/gomokuworld/gomoku_world
- 文档站点：https://docs.gomokuworld.org
- PyPI页面：https://pypi.org/project/gomoku-world
- 问题追踪：https://github.com/gomokuworld/gomoku_world/issues

### 6.3 贡献指南 / Contributing Guide
详见 [CONTRIBUTING.md](CONTRIBUTING.md)

### 6.4 许可证 / License
本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。 