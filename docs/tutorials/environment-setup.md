# 开发环境配置 / Environment Setup

## 前置要求 / Prerequisites

在开始之前，请确保你的系统满足以下要求：

- Python 3.8 或更高版本
- Git 版本控制工具
- 文本编辑器或 IDE（推荐 VS Code、PyCharm）
- 命令行工具

## 步骤 1：安装 Python / Step 1: Install Python

### Windows
1. 访问 [Python 官网](https://www.python.org/downloads/)
2. 下载最新版本的 Python 安装包
3. 运行安装程序，确保勾选"Add Python to PATH"
4. 验证安装：
   ```bash
   python --version
   pip --version
   ```

### macOS
```bash
# 使用 Homebrew 安装
brew install python

# 验证安装
python3 --version
pip3 --version
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip
python3 --version
pip3 --version
```

## 步骤 2：安装 Git / Step 2: Install Git

### Windows
1. 访问 [Git 官网](https://git-scm.com/download/win)
2. 下载并安装 Git
3. 验证安装：
   ```bash
   git --version
   ```

### macOS
```bash
brew install git
git --version
```

### Linux
```bash
sudo apt install git
git --version
```

## 步骤 3：获取项目代码 / Step 3: Get the Code

```bash
# 克隆项目仓库
git clone https://github.com/gomokuworld/gomoku-world.git
cd gomoku-world

# 创建并激活虚拟环境
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

## 步骤 4：安装依赖 / Step 4: Install Dependencies

```bash
# 安装项目依赖
pip install -e ".[dev]"

# 安装开发工具
pre-commit install
```

## 步骤 5：IDE 配置 / Step 5: IDE Setup

### VS Code
1. 安装 Python 扩展
2. 安装 Git 扩展
3. 推荐的扩展：
   - Python Test Explorer
   - Python Docstring Generator
   - Python Type Hint
   - GitLens

### PyCharm
1. 打开项目目录
2. 配置 Python 解释器（选择虚拟环境）
3. 启用 Git 集成
4. 配置代码风格（PEP 8）

## 步骤 6：验证安装 / Step 6: Verify Installation

```bash
# 运行测试
pytest

# 启动游戏
python -m gomoku_world
```

## 常见问题 / Common Issues

### 1. Python 路径问题
确保 Python 已添加到系统环境变量中：
- Windows: 检查系统环境变量 PATH
- macOS/Linux: 检查 ~/.bashrc 或 ~/.zshrc

### 2. 依赖安装失败
```bash
# 更新 pip
python -m pip install --upgrade pip

# 清除 pip 缓存
pip cache purge

# 重试安装
pip install -e ".[dev]"
```

### 3. 虚拟环境问题
```bash
# 删除现有虚拟环境
rm -rf venv

# 重新创建虚拟环境
python -m venv venv
```

## 下一步 / Next Steps

完成环境配置后，你可以：
1. 阅读项目文档
2. 运行示例程序
3. 开始第一个练习项目

## 配置检查清单 / Setup Checklist

- [ ] Python 安装成功
- [ ] Git 安装成功
- [ ] 项目代码已克隆
- [ ] 虚拟环境已创建并激活
- [ ] 依赖安装完成
- [ ] IDE 配置完成
- [ ] 测试运行成功
- [ ] 游戏可以启动

## 获取帮助 / Getting Help

如果遇到问题：
1. 查看项目 [FAQ](../faq.md)
2. 在 GitHub Issues 中搜索
3. 在 Discord 社区提问
4. 发送邮件到支持团队 