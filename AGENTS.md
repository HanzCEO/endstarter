# AGENTS.md

## Project Overview
- **Project**: endstarter
- **Type**: Python E2E testing framework in YAML, self-hosted, and headless
- **Purpose**: For app developers iterating fast

---

## Build/Lint/Test Commands

### Setup
```bash
# Install dependencies (when pyproject.toml exists)
pip install -e .
pip install -e ".[dev]"

# or with poetry
poetry install
poetry install --with dev
```

### Running Tests
```bash
# Run all tests
pytest

# Run a single test file
pytest tests/test_example.py

# Run a single test function
pytest tests/test_example.py::test_function_name

# Run tests with specific markers
pytest -m "not slow"

# Run with coverage
pytest --cov=src --cov-report=html
```

### Linting & Formatting
```bash
# Format code (when configured)
ruff format .
ruff check --fix .

# Type checking
mypy src/

# All checks before commit
ruff format . && ruff check . && mypy src/ && pytest
```

---

## Code Style Guidelines

### General
- **Line length**: 88 characters (ruff default)
- **Indentation**: 4 spaces
- **End of file**: newline
- **Encoding**: UTF-8

### Imports
```python
# Standard library first, then third-party, then local
import os
import sys
from typing import Any

import pytest
from pydantic import BaseModel

from endstarter import something
```

- Use `import x` for standard library and third-party
- Use `from x import y` when importing specific names
- Avoid wildcard imports (`from x import *`)
- Sort imports alphabetically within groups
- Separate import groups with a single blank line

### Naming Conventions
| Type | Convention | Example |
|------|------------|---------|
| Modules | lowercase, snake_case | `yaml_parser.py` |
| Classes | PascalCase | `TestRunner` |
| Functions | snake_case | `parse_yaml_file` |
| Variables | snake_case | `test_config` |
| Constants | UPPER_SNAKE | `MAX_RETRIES` |
| Type Variables | PascalCase | `T = TypeVar("T")` |

### Types
- Use type hints for all function signatures
- Use `Optional[X]` over `X | None`
- Use `list[X]`, `dict[K, V]` over `List[X]`, `Dict[K, V]`
- Use `Any` sparingly; prefer typed alternatives
- Use `@overload` for functions with multiple signatures

```python
# Good
def process(data: dict[str, Any], timeout: Optional[float] = None) -> list[str]:
    ...

# Avoid
def process(data: Dict, timeout: float = None) -> List[str]:
    ...
```

### Error Handling
- Use specific exception types
- Never use bare `except:`
- Include context in exception messages
- Prefer raising exceptions over returning `None` for error cases

```python
# Good
if not config.exists():
    raise ConfigError(f"Config file not found: {config.path}")

# Avoid
try:
    ...
except:
    pass
```

### Docstrings
- Use Google-style docstrings
- Document public APIs, not internal implementation details

```python
def parse_yaml(path: Path) -> dict[str, Any]:
    """Parse a YAML file into a dictionary.

    Args:
        path: Path to the YAML file.

    Returns:
        Parsed YAML content as a dictionary.

    Raises:
        YAMLError: If the file is not valid YAML.
    """
```

### Testing
- Test file naming: `test_<module>.py`
- Test class naming: `Test<ClassName>`
- Test function naming: `test_<description>`
- Use fixtures for shared setup
- One assertion per test when practical

---

## Project Structure
```
endstarter/
├── src/endstarter/     # Source code
├── tests/              # Test files
├── docs/               # Documentation
├── pyproject.toml      # Project config
└── AGENTS.md           # This file
```

---

## Tool Configuration

### Ruff (Linting & Formatting)
- Line length: 88
- Target: Python 3.11+
- Plugins: F (pyflakes), E (pycodestyle), W (pycodestyle), I (isort)

### MyPy
- Strict mode enabled
- Check untyped defs: error
- Check untyped calls: error

### Pytest
- Default test paths: `tests/`
- Add `tests/` to `PYTHONPATH`
