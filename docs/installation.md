# Installation Guide

This document provides detailed instructions for installing the Gomoku game on different platforms.

## Prerequisites

Before installing the game, ensure you have the following prerequisites:

- Python 3.8 or higher
- pip (Python package installer)
- Git (for installation from source)
- SDL2 (for GUI support)
- Microsoft Visual C++ Build Tools (Windows only)

## Dependencies

The game requires the following Python packages:

- pygame>=2.5.2: Game graphics and UI
- psutil>=5.9.0: System monitoring
- requests>=2.31.0: Network communication
- urllib3>=2.1.0: HTTP client
- certifi>=2023.11.17: SSL certificates
- chardet>=5.2.0: Character encoding detection
- pillow>=10.1.0: Image processing
- numpy>=1.26.0: Numerical computations

## Installation Methods

### 1. Installation from PyPI

The simplest way to install the game is using pip:

```bash
pip install gomoku-world
```

### 2. Installation from Source

For developers or users who want the latest version:

1. Clone the repository:
   ```bash
   git clone https://github.com/nighm/gomoku_world.git
   cd gomoku_world
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   # Windows
   python -m venv .venv
   .\.venv\Scripts\activate

   # Linux/MacOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install in development mode:
   ```bash
   pip install -e .
   ```

## Platform-Specific Instructions

### Windows

1. Install Python from the [official website](https://www.python.org/downloads/)
2. Ensure Python is added to PATH during installation
3. Install Microsoft Visual C++ Build Tools:
   - Download from [Microsoft](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   - Select "Desktop development with C++"
4. Open Command Prompt and run:
   ```bash
   pip install gomoku-world
   ```

### Linux

1. Install Python and system dependencies:
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip python3-dev
   sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
   sudo apt install libffi-dev libjpeg-dev zlib1g-dev

   # Fedora
   sudo dnf install python3 python3-pip python3-devel
   sudo dnf install SDL2-devel SDL2_image-devel SDL2_mixer-devel SDL2_ttf-devel
   sudo dnf install libffi-devel libjpeg-devel zlib-devel
   ```

2. Install the game:
   ```bash
   pip3 install gomoku-world
   ```

### macOS

1. Install Python and dependencies using Homebrew:
   ```bash
   brew install python
   brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf
   ```

2. Install the game:
   ```bash
   pip3 install gomoku-world
   ```

## Configuration

### Network Settings

The game supports proxy configuration for network access:

```python
from gomoku_world.config import config_manager

# Configure proxy
config_manager.set("network", "proxy", {
    "enabled": True,
    "host": "proxy.example.com",
    "port": 8080,
    "auth": {
        "username": "user",
        "password": "pass"
    }
})
```

### Language Settings

The game supports multiple languages:

```python
from gomoku_world.i18n import i18n_manager

# Set language
i18n_manager.set_language("zh")  # Chinese
i18n_manager.set_language("en")  # English
i18n_manager.set_language("ja")  # Japanese
i18n_manager.set_language("ko")  # Korean
```

## Troubleshooting

### Common Issues

1. **Pygame Installation Fails**
   - Windows: Ensure Microsoft Visual C++ Build Tools are installed
   - Linux: Install SDL dependencies as shown above
   - macOS: Install SDL2 via Homebrew

2. **Network Connection Issues**
   - Check proxy settings if behind a firewall
   - Verify network permissions
   - Check SSL certificate settings

3. **Font Issues**
   - Windows: Install language-specific fonts
   - Linux: Install fonts-cjk package
   - macOS: Install required fonts via Homebrew

4. **Permission Errors**
   - Use `--user` flag with pip:
     ```bash
     pip install --user gomoku-world
     ```
   - Use virtual environment (recommended)

5. **Python Version Conflicts**
   - Use Python 3.8 or higher
   - Use virtual environment
   - Ensure correct Python version is in PATH

### Getting Help

If you encounter any issues:

1. Check the [GitHub Issues](https://github.com/nighm/gomoku_world/issues)
2. Create a new issue with:
   - Your operating system and version
   - Python version (`python --version`)
   - Error message and traceback
   - Steps to reproduce
   - Network configuration (if relevant)
   - Language settings (if relevant) 