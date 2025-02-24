# Gomoku World / 五子棋世界

![License](https://img.shields.io/github/license/gomokuworld/gomoku-world)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Build Status](https://img.shields.io/github/workflow/status/gomokuworld/gomoku-world/CI)
![Code Coverage](https://img.shields.io/codecov/c/github/gomokuworld/gomoku-world)

[English](./README.md) | [简体中文](./README.zh-CN.md)

A modern Gomoku (Five in a Row) game platform with advanced AI opponents, online multiplayer, and tournament features.

## Latest Release / 最新版本

Version 2.1.2 is now available! Check out our detailed release notes:
- [User Release Notes](docs/release_notes/v2.1.2.user.md)
- [Developer Notes](docs/release_notes/v2.1.2.dev.md)

## Features / 功能特点

- 🎮 **Rich Game Modes**
  - Player vs AI (Multiple Levels)
  - Local Multiplayer
  - Online Multiplayer
  - Tournament System

- 🤖 **Advanced AI**
  - Multi-level Search
  - Neural Network Evaluation
  - Adaptive Difficulty
  - Open AI Interface

- 🌐 **Complete Network Features**
  - Real-time Battles
  - Ranking System
  - Game Replay
  - Spectator System

- 🎨 **Modern Interface**
  - Responsive Design
  - Theme Customization
  - Animation Effects
  - Multi-language Support

## Quick Start / 快速开始

### Installation / 安装

```bash
# Install from PyPI
pip install gomoku-world

# Or install from source
git clone https://github.com/gomokuworld/gomoku-world.git
cd gomoku-world
pip install -e ".[dev]"
```

### Running / 运行

```python
from gomoku_world import GomokuGUI

# Start the game
GomokuGUI().run()
```

## Project Structure / 项目结构

```
gomoku-world/
├── src/                    # Source code
│   └── gomoku_world/       # Main package
│       ├── core/          # Core game logic
│       ├── ai/            # AI implementation
│       ├── gui/           # Graphical interface
│       ├── network/       # Network features
│       └── utils/         # Utility functions
├── tests/                 # Test code
├── docs/                  # Documentation
├── examples/              # Example code
└── scripts/              # Utility scripts
```

## Documentation / 文档

- [Tutorial Guide](docs/index.md)
- [Development Documentation](docs/README.md)
- [API Reference](https://docs.gomokuworld.com/api)
- [Example Code](examples/)

## Development / 开发指南

### Setup / 环境设置

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Testing / 测试

```bash
# Run all tests
pytest

# Run coverage tests
pytest --cov=gomoku_world

# Run performance tests
pytest tests/performance/
```

### Building / 构建

```bash
# Build package
python -m build

# Build documentation
sphinx-build docs/ docs/_build/html
```

## Contributing / 贡献指南

We welcome all forms of contributions, including but not limited to:

- Submitting issues and suggestions
- Improving documentation
- Submitting code changes
- Sharing usage experiences

See [Contributing Guide](CONTRIBUTING.md) for details.

## Community / 社区

- [Discord](https://discord.gg/gomokuworld)
- [Forum](https://forum.gomokuworld.com)
- [WeChat Group](https://gomokuworld.com/wechat)

## Changelog / 版本历史

See [CHANGELOG.md](CHANGELOG.md)

## License / 许可证

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Authors / 作者

- Development Team - [Contributors](https://github.com/gomokuworld/gomoku-world/graphs/contributors)

## Acknowledgments / 致谢

Thanks to all developers and users who have contributed to this project.

## Citation / 引用

If you use this project in your research, please cite:

```bibtex
@software{gomoku_world,
  title = {Gomoku World},
  author = {Gomoku World Team},
  year = {2024},
  version = {2.1.2},
  url = {https://github.com/gomokuworld/gomoku-world}
}
``` 