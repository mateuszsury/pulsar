# Contributing to Pulsar

Thank you for your interest in contributing to Pulsar! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and considerate in all interactions. We're all here to build great software for the ESP32 community.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- Git

### Development Setup

1. **Fork and clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/pulsar.git
cd pulsar
```

2. **Set up Python environment**

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -e ".[dev]"
```

3. **Set up frontend**

```bash
cd frontend
npm install
cd ..
```

4. **Run in development mode**

```bash
# Terminal 1: Start Vite dev server
cd frontend && npm run dev

# Terminal 2: Start Python backend
python -m pulsar --dev
```

## Project Structure

```
pulsar/
├── src/                 # Python backend
│   ├── core/           # Core application logic
│   ├── server/         # HTTP/WebSocket server
│   ├── serial_manager/ # Serial communication
│   ├── tools/          # Development tools
│   └── ui/             # UI layer
├── frontend/           # React frontend
│   └── src/
│       ├── components/ # UI components
│       ├── stores/     # State management
│       └── services/   # API clients
├── stubs/              # MicroPython type stubs
└── tests/              # Test files
```

## Making Changes

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation changes
- `refactor/description` - Code refactoring

### Commit Messages

Follow conventional commit format:

```
type(scope): description

[optional body]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance

Examples:
```
feat(editor): add code folding support
fix(serial): handle connection timeout gracefully
docs(readme): update installation instructions
```

### Code Style

**Python:**
- Follow PEP 8
- Use type hints
- Run `black` for formatting
- Run `ruff` for linting

```bash
black src/
ruff check src/
```

**TypeScript/React:**
- Use functional components
- Follow ESLint rules
- Use TypeScript strict mode

```bash
cd frontend
npm run lint
```

## Testing

### Running Tests

```bash
# Python tests
pytest

# Frontend tests
cd frontend && npm test
```

### Writing Tests

- Place tests in the `tests/` directory
- Use pytest for Python tests
- Mirror the source structure in tests

## Pull Request Process

1. **Create a feature branch**
```bash
git checkout -b feature/your-feature
```

2. **Make your changes**
- Write code
- Add tests
- Update documentation

3. **Run checks**
```bash
# Format code
black src/

# Lint
ruff check src/

# Run tests
pytest
```

4. **Commit and push**
```bash
git add .
git commit -m "feat(scope): description"
git push origin feature/your-feature
```

5. **Open a Pull Request**
- Use a clear title
- Describe what changes were made
- Link any related issues
- Add screenshots for UI changes

### PR Review Checklist

- [ ] Code follows project style
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Commits are clean and descriptive

## Adding MicroPython Stubs

To add type stubs for a new MicroPython module:

1. Create a `.pyi` file in `stubs/micropython/`
2. Follow existing stub format
3. Include docstrings with examples
4. Test autocompletion works

Example stub:

```python
"""Type stubs for mymodule."""

from typing import Optional

def my_function(arg: str, flag: bool = False) -> int:
    """Do something.

    Args:
        arg: Description
        flag: Description

    Returns:
        Description

    Example:
        result = my_function("test")
    """
    ...
```

## Reporting Issues

### Bug Reports

Include:
- Pulsar version
- Operating system
- ESP32 model
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs

### Feature Requests

Include:
- Use case description
- Proposed solution
- Alternatives considered

## Questions?

- Open a GitHub Discussion
- Check existing issues

Thank you for contributing to Pulsar!
