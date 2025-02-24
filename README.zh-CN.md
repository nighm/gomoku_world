# 五子棋世界 / Gomoku World

![许可证](https://img.shields.io/github/license/nighm/gomoku_world)
![Python版本](https://img.shields.io/badge/python-3.8%2B-blue)
![构建状态](https://img.shields.io/github/workflow/status/nighm/gomoku_world/CI)
![代码覆盖率](https://img.shields.io/codecov/c/github/nighm/gomoku_world)

[English](./README.md) | [简体中文](./README.zh-CN.md)

一个现代化的五子棋游戏平台，具有高级AI对手、在线多人对战和比赛功能。

## 最新版本 / Latest Release

版本2.1.3现已发布！查看详细发布说明：
- [用户发布说明](docs/release_notes/v2.1.3.user.zh-CN.md)
- [开发者说明](docs/release_notes/v2.1.3.dev.zh-CN.md)

## 功能特点 / Features

- 🎮 **丰富的游戏模式**
  - 人机对战（多级AI）
  - 本地双人对战
  - 在线多人对战
  - 比赛系统

- 🤖 **先进的AI**
  - 多层深度搜索
  - 神经网络评估
  - 自适应难度
  - 开放AI接口

- 🌐 **完整的网络功能**
  - 实时对战
  - 排名系统
  - 录像回放
  - 观战系统

- 🎨 **现代化界面**
  - 响应式设计
  - 主题定制
  - 动画效果
  - 多语言支持

## 快速开始 / Quick Start

### 安装 / Installation

```bash
# 从PyPI安装
pip install gomoku-world

# 或从源码安装
git clone https://github.com/nighm/gomoku_world.git
cd gomoku_world
pip install -e ".[dev]"
```

### 运行 / Running

```python
from gomoku_world import GomokuGUI

# 启动游戏
GomokuGUI().run()
```

## 项目结构 / Project Structure

```
gomoku-world/
├── src/                    # 源代码
│   └── gomoku_world/       # 主包
│       ├── core/          # 核心游戏逻辑
│       ├── ai/            # AI实现
│       ├── gui/           # 图形界面
│       ├── network/       # 网络功能
│       └── utils/         # 工具函数
├── tests/                 # 测试代码
├── docs/                  # 文档
├── examples/              # 示例代码
└── scripts/              # 工具脚本
```

## 文档 / Documentation

- [教程总纲](docs/index.md)
- [开发文档](docs/README.md)
- [API参考](https://docs.gomokuworld.com/api)
- [示例代码](examples/)

## 开发指南 / Development

### 环境设置 / Setup

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# 安装依赖
pip install -e ".[dev]"

# 安装pre-commit hooks
pre-commit install
```

### 测试 / Testing

```bash
# 运行所有测试
pytest

# 运行覆盖率测试
pytest --cov=gomoku_world

# 运行性能测试
pytest tests/performance/
```

### 构建 / Building

```bash
# 构建包
python -m build

# 构建文档
sphinx-build docs/ docs/_build/html
```

## 贡献指南 / Contributing

我们欢迎各种形式的贡献，包括但不限于：

- 提交问题和建议
- 改进文档
- 提交代码修改
- 分享使用经验

详见[贡献指南](CONTRIBUTING.md)。

## 社区 / Community

- [Discord](https://discord.gg/gomokuworld)
- [论坛](https://forum.gomokuworld.com)
- [微信群](https://gomokuworld.com/wechat)

## 版本历史 / Changelog

详见[CHANGELOG.md](CHANGELOG.md)

## 许可证 / License

本项目采用MIT许可证 - 详见[LICENSE](LICENSE)文件

## 作者 / Authors

- 开发团队 - [贡献者列表](https://github.com/nighm/gomoku_world/graphs/contributors)

## 致谢 / Acknowledgments

感谢所有为本项目做出贡献的开发者和用户。

## 引用 / Citation

如果您在研究中使用了本项目，请引用：

```bibtex
@software{gomoku_world,
  title = {Gomoku World},
  author = {Gomoku World Team},
  year = {2024},
  version = {2.1.3},
  url = {https://github.com/nighm/gomoku_world}
}
```