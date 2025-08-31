# Contributing to Week1 Chatbot

Thank you for your interest in contributing to the Week1 Chatbot project! This document provides guidelines and information for contributors.

## 🚀 Quick Start

1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone https://github.com/yourusername/week1-chatbot.git
   cd week1-chatbot
   ```

3. **Set up development environment:**
   ```bash
   # Install uv (recommended) or use pip
   pip install -e ".[dev]"
   pre-commit install
   ```

4. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🛠️ Development Setup

### Using uv (Recommended)

```bash
# Install uv
pip install uv

# Create virtual environment and install dependencies
uv sync --dev

# Run tests
uv run pytest

# Format code
uv run black .
uv run isort .
```

### Using pip

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
pre-commit install
```

## 📋 Development Workflow

1. **Make your changes**
2. **Run tests:**
   ```bash
   pytest
   ```

3. **Check code quality:**
   ```bash
   make check  # or: make format-check && make lint && make test
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

5. **Push and create a pull request**

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=chatbot --cov=tools --cov=utils

# Run specific test file
pytest tests/test_config.py

# Run with verbose output
pytest -v
```

### Writing Tests

- Place tests in the `tests/` directory
- Use descriptive test names
- Follow the pattern `test_*.py`
- Use pytest fixtures when appropriate
- Mock external dependencies

Example test:
```python
def test_my_feature():
    """Test description."""
    result = my_function()
    assert result == expected_value
```

## 🎨 Code Style

We use several tools to maintain code quality:

- **Black** - Code formatting
- **isort** - Import sorting
- **flake8** - Linting
- **mypy** - Type checking
- **bandit** - Security checking

### Formatting

```bash
# Format code
make format

# Check formatting
make format-check
```

### Linting

```bash
# Run all linting checks
make lint
```

## 📝 Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Test changes
- `chore:` - Maintenance tasks

Examples:
```
feat: add new weather tool
fix: resolve import error in config
docs: update README with new features
```

## 🔧 Adding New Tools

To add a new tool:

1. Create a new file in `tools/available/`
2. Inherit from `BaseTool`
3. Implement required methods
4. Add tests in `tests/`
5. Update documentation

Example tool:
```python
from tools.base import BaseTool, ToolParameter
from typing import List

class MyTool(BaseTool):
    @property
    def name(self) -> str:
        return "my_tool"
    
    @property
    def description(self) -> str:
        return "Description of my tool"
    
    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="param1",
                type="string",
                description="Parameter description",
                required=True
            )
        ]
    
    def execute(self, param1: str) -> str:
        # Tool logic here
        return f"Result: {param1}"
```

## 🐛 Bug Reports

When reporting bugs, please include:

- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs

## 💡 Feature Requests

For feature requests:

- Describe the feature clearly
- Explain the use case
- Consider implementation complexity
- Check if it aligns with project goals

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🤝 Questions?

If you have questions about contributing, please:

1. Check existing issues and discussions
2. Open a new issue for questions
3. Join our community discussions

Thank you for contributing! 🎉
