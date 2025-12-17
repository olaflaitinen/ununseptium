"""Ununseptium: State-of-the-art RegTech and Cybersecurity Python Library.

Provides comprehensive tools for:
- KYC/AML automation
- Data security and PII management
- AI-driven risk analysis
- Scientific ML (PINN, Neural ODEs)
"""

# Version must be defined BEFORE any submodule imports to avoid circular imports
__version__ = "1.0.0"
__author__ = "Olaf Laitinen"
__email__ = "olaf.laitinen@protonmail.com"

# Import submodules (cli is imported lazily to avoid circular import)
from ununseptium import ai, aml, core, kyc, mathstats, model_zoo, plugins, security
from ununseptium.core.config import Settings, load_config
from ununseptium.core.errors import (
    IntegrityError,
    ModelError,
    SecurityError,
    UnunseptiumError,
    ValidationError,
)

# Lazy import for cli to avoid circular import
def __getattr__(name: str):
    """Lazy import for cli module."""
    if name == "cli":
        from ununseptium import cli as _cli
        return _cli
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    "IntegrityError",
    "ModelError",
    "SecurityError",
    "Settings",
    "UnunseptiumError",
    "ValidationError",
    "__author__",
    "__email__",
    "__version__",
    "ai",
    "aml",
    "cli",
    "core",
    "kyc",
    "load_config",
    "mathstats",
    "model_zoo",
    "plugins",
    "security",
]

