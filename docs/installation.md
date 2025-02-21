# Installation Guide

This document provides detailed instructions for installing the Gomoku game on different platforms.

## Prerequisites

Before installing the game, ensure you have the following prerequisites:

- Python 3.6 or higher
- pip (Python package installer)
- Git (for installation from source)

## Installation Methods

### 1. Installation from PyPI

The simplest way to install the game is using pip:

```bash
pip install gomoku
```

### 2. Installation from Source

For developers or users who want the latest version:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/gomoku.git
   cd gomoku
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/MacOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install in development mode:
   ```bash
   pip install -e .
   ```

## Platform-Specific Instructions

### Windows

1. Install Python from the [official website](https://www.python.org/downloads/)
2. Ensure Python is added to PATH during installation
3. Open Command Prompt and run:
   ```bash
   pip install gomoku
   ```

### Linux

1. Install Python and pip:
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip

   # Fedora
   sudo dnf install python3 python3-pip
   ```

2. Install the game:
   ```bash
   pip3 install gomoku
   ```

### macOS

1. Install Python using Homebrew:
   ```bash
   brew install python
   ```

2. Install the game:
   ```bash
   pip3 install gomoku
   ```

## Troubleshooting

### Common Issues

1. **Pygame Installation Fails**
   - Windows: Ensure Microsoft Visual C++ Build Tools are installed
   - Linux: Install SDL dependencies:
     ```bash
     sudo apt install python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
     ```

2. **Permission Errors**
   - Use `--user` flag with pip:
     ```bash
     pip install --user gomoku
     ```

3. **Python Version Conflicts**
   - Use a virtual environment
   - Ensure correct Python version is in PATH

### Getting Help

If you encounter any issues:

1. Check the [GitHub Issues](https://github.com/yourusername/gomoku/issues)
2. Create a new issue with:
   - Your operating system
   - Python version (`python --version`)
   - Error message
   - Steps to reproduce 