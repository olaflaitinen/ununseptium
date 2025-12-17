"""Ununseptium: State-of-the-art RegTech and Cybersecurity Python Library.

Provides comprehensive tools for:
- KYC/AML automation
- Data security and PII management
- AI-driven risk analysis
- Scientific ML (PINN, Neural ODEs)
"""

from ununseptium import ai, aml, cli, core, kyc, mathstats, model_zoo, plugins, security
from ununseptium.core.config import Settings, load_config
from ununseptium.core.errors import (
    IntegrityError,
    ModelError,
    SecurityError,
    UnunseptiumError,
    ValidationError,
)

__version__ = "1.0.0"
__author__ = "Olaf Laitinen"
__email__ = "olaf.laitinen@protonmail.com"

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

