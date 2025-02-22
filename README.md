# GomokuWorld

A modern Gomoku (Five in a Row) game with advanced AI and multiplayer support.

现代五子棋游戏，具有高级AI和多人游戏支持。

## Features / 特性

- Advanced AI with multiple difficulty levels / 具有多个难度级别的高级AI
- Online multiplayer support / 在线多人游戏支持
- Beautiful modern UI / 精美的现代界面
- Cross-platform compatibility / 跨平台兼容性
- Internationalization support / 国际化支持
- Comprehensive metrics and monitoring / 全面的指标和监控
- Cloud save and sync / 云存储和同步
- Tournament system / 比赛系统

## Installation / 安装

### From PyPI / 从PyPI安装

```bash
pip install gomoku-world
```

### From Source / 从源代码安装

```bash
git clone https://github.com/gomokuworld/gomoku-world.git
cd gomoku-world
pip install -e ".[dev]"
```

## Quick Start / 快速开始

```python
from gomoku_world import GomokuGUI

# Start the game / 启动游戏
GomokuGUI().run()
```

### Examples / 示例

The `examples` directory contains several demo programs showing how to use different features:

- `network_i18n_demo.py`: Demonstrates the network-aware internationalization system
  ```python
  # Run the network i18n demo / 运行网络国际化示例
  python examples/network_i18n_demo.py
  ```

- `ai_game_demo.py`: Shows how to play against the AI
- `multiplayer_demo.py`: Demonstrates online multiplayer functionality
- `tournament_demo.py`: Shows how to set up and run a tournament

See the comments in each example file for detailed usage instructions.

## Development / 开发

### Setup / 环境设置

```bash
# Create virtual environment / 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies / 安装依赖
pip install -e ".[dev]"

# Install pre-commit hooks / 安装pre-commit钩子
pre-commit install
```

### Testing / 测试

```bash
# Run all tests / 运行所有测试
pytest

# Run with coverage / 运行覆盖率测试
pytest --cov=gomoku_world

# Run performance tests / 运行性能测试
pytest tests/performance/
```

### Building / 构建

```bash
# Build for all platforms / 为所有平台构建
python build.py all

# Build for specific platform / 为特定平台构建
python build.py windows
python build.py linux
python build.py android
```

## Deployment / 部署

### Docker / Docker部署

```bash
# Build image / 构建镜像
docker build -t gomoku-world .

# Run container / 运行容器
docker run -p 8080:8080 gomoku-world
```

### Kubernetes / Kubernetes部署

```bash
# Deploy to Kubernetes / 部署到Kubernetes
kubectl apply -f deployment/kubernetes/
```

## Documentation / 文档

- [User Guide / 用户指南](https://docs.gomokuworld.com/user/)
- [Developer Guide / 开发者指南](https://docs.gomokuworld.com/dev/)
- [API Reference / API参考](https://docs.gomokuworld.com/api/)

## Contributing / 贡献

Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting a Pull Request.

在提交Pull Request之前，请阅读我们的[贡献指南](CONTRIBUTING.md)。

## License / 许可证

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

本项目采用MIT许可证 - 详见[LICENSE](LICENSE)文件。

## Contact / 联系方式

- Website / 网站: [https://gomokuworld.com](https://gomokuworld.com)
- Email / 邮箱: team@gomokuworld.com
- Discord: [Join our server](https://discord.gg/gomokuworld)
- WeChat Group / 微信群: GomokuWorld 