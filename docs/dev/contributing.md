# Contributing to Gomoku

Thank you for your interest in contributing to Gomoku! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/yourusername/gomoku.git
   cd gomoku
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Unix or MacOS:
   source venv/bin/activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Development Workflow

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and ensure they follow our coding standards:
   - Use Black for code formatting
   - Use isort for import sorting
   - Follow PEP 8 guidelines
   - Add type hints to new code
   - Write docstrings for new functions and classes
   - Add tests for new functionality

3. Run the test suite:
   ```bash
   pytest
   ```

4. Commit your changes:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```
   Follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.

5. Push to your fork and create a Pull Request

## Project Structure

```
gomoku/
├── src/gomoku/          # Main package
│   ├── core/           # Core game logic
│   ├── gui/            # GUI components
│   ├── network/        # Networking code
│   ├── utils/          # Utilities
│   └── resources/      # Game resources
├── tests/              # Test suite
├── docs/               # Documentation
└── build.py           # Build script
```

## Building the Game

- For Windows: `python build.py windows`
- For Linux: `python build.py linux`
- For Android: `python build.py android`

## Documentation

- Update documentation for any new features
- Use docstrings for Python code
- Update README.md if necessary
- Add migration notes for breaking changes

## Code Review Process

1. All code must be reviewed before merging
2. Address review comments promptly
3. Keep pull requests focused and small
4. Ensure CI passes before requesting review

## Questions?

Feel free to open an issue or contact the maintainers if you have any questions. 