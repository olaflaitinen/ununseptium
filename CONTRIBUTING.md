# Contributing to Ununseptium

Thank you for your interest in contributing to ununseptium. This document provides guidelines for contributions.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Testing Requirements](#testing-requirements)
- [Documentation Standards](#documentation-standards)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

All contributors must adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## Getting Started

### Types of Contributions

| Type | Description | Requirements |
|------|-------------|--------------|
| Bug Fix | Fix existing issues | Issue reference, tests |
| Feature | New functionality | Discussion first, full tests |
| Documentation | Improve docs | Style compliance |
| Test | Add test coverage | Follows existing patterns |

### Before Contributing

1. Check existing [issues](https://github.com/olaflaitinen/ununseptium/issues) for duplicates
2. For features, open a discussion first
3. For security issues, see [SECURITY.md](SECURITY.md)

## Development Setup

### Prerequisites

- Python 3.11+
- Git
- Virtual environment tool (venv, conda, etc.)

### Setup Steps

```bash
# Clone repository
git clone https://github.com/olaflaitinen/ununseptium.git
cd ununseptium

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Verify installation
ununseptium doctor

```

### Development Dependencies

The `[dev]` extra includes:

| Tool | Purpose |
|------|---------|
| pytest | Testing framework |
| pytest-cov | Coverage reporting |
| ruff | Linting and formatting |
| pyright | Static type checking |
| pre-commit | Git hooks |

## Code Style

### Formatting

We use ruff for formatting and linting:

```bash
# Format code
ruff format src/ tests/

# Lint code
ruff check src/ tests/ --fix

```

### Type Hints

All code must be fully typed and pass pyright:

```bash
pyright src/

```

### Style Rules

| Rule | Standard |
|------|----------|
| Line length | 88 characters |
| Imports | isort-compatible (ruff handles this) |
| Docstrings | Google style |
| Naming | snake_case for functions, PascalCase for classes |
| F-strings | Preferred over .format() |

### Docstring Example

```python
def verify_identity(
    identity: Identity,
    config: VerificationConfig | None = None,
) -> VerificationResult:
    """Verify an identity against configured rules.

    Args:
        identity: Identity object to verify.
        config: Optional verification configuration.

    Returns:
        VerificationResult with status and reason codes.

    Raises:
        ValidationError: If identity data is invalid.

    Example:
        ```python
        result = verify_identity(identity)
        if result.passed:
            print("Verification successful")
        ```

    """

```

## Testing Requirements

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ununseptium --cov-report=html

# Run specific module
pytest tests/test_kyc.py

# Run with verbose output
pytest -v

```

### Test Structure

```text
tests/
  conftest.py          # Shared fixtures
  test_core/           # Core module tests
  test_kyc/            # KYC module tests
  test_aml/            # AML module tests
  test_security/       # Security module tests
  test_mathstats/      # MathStats module tests
  test_ai/             # AI module tests
  test_integration/    # Integration tests

```

### Test Requirements

| Requirement | Description |
|-------------|-------------|
| Coverage | Minimum 80% for new code |
| Determinism | Tests must be reproducible (use seeds) |
| Isolation | No tests should depend on external services |
| Speed | Individual tests should complete in < 1 second |

### Writing Tests

```python
import pytest
from ununseptium.kyc import IdentityVerifier

class TestIdentityVerifier:
    """Tests for IdentityVerifier."""

    def test_verify_valid_identity(self, valid_identity):
        """Verify returns passed for valid identity."""
        verifier = IdentityVerifier()
        result = verifier.verify(valid_identity)

        assert result.passed is True
        assert result.status == "approved"

    def test_verify_invalid_identity_raises(self):
        """Verify raises ValidationError for invalid input."""
        verifier = IdentityVerifier()

        with pytest.raises(ValidationError):
            verifier.verify({})  # Invalid input

```

## Documentation Standards

### Markdown Requirements

All documentation must:

1. **No emojis** - Use text descriptions instead
2. **Include scope** - What the doc covers and does not cover
3. **Include definitions** - Link to glossary or define terms
4. **Include tables** - For structured information
5. **Include diagrams** - Mermaid for flows/architecture
6. **Include references** - Link to authoritative sources

### Documentation Structure

```markdown
# Title

## Scope

What this document covers.

### Non-Goals

What this document does not cover.

## Definitions

| Term | Definition |
|------|------------|
| ... | ... |

## Content

Main documentation content.

## References

- [Reference 1](url)
- [Reference 2](url)

```

### Running Documentation Checks

```bash
python scripts/docs_lint.py

```

## Pull Request Process

### Before Submitting

1. All tests pass: `pytest`
2. Code is formatted: `ruff format src/ tests/`
3. Linting passes: `ruff check src/ tests/`
4. Types check: `pyright src/`
5. Documentation is updated if needed
6. CHANGELOG.md is updated

### PR Checklist

- [ ] Tests added for new functionality
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] All CI checks pass
- [ ] PR description explains changes
- [ ] Linked to relevant issue(s)

### Review Process

1. Maintainers will review within 5 business days
2. Address feedback in new commits (don't force-push)
3. Once approved, maintainers will merge
4. Squash merging is used for clean history

### Commit Messages

Follow conventional commits:

```text
type(scope): description

[optional body]

[optional footer]

```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:

```text
feat(kyc): add document expiry validation
fix(aml): correct structuring detection threshold
docs(readme): add model zoo section

```

## Questions

- Open a [Discussion](https://github.com/olaflaitinen/ununseptium/discussions) for questions
- Check [FAQ](docs/faq.md) for common questions
- See [SUPPORT.md](SUPPORT.md) for support options

---

Thank you for contributing to ununseptium.
