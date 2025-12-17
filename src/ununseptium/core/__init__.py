"""Core module providing configuration, errors, logging, and schema management."""

from ununseptium.core.canonical import canonical_json, deterministic_hash
from ununseptium.core.config import Settings, load_config
from ununseptium.core.errors import (
    ConfigurationError,
    IntegrityError,
    ModelError,
    SecurityError,
    UnunseptiumError,
    ValidationError,
)
from ununseptium.core.logging import get_logger, setup_logging
from ununseptium.core.schemas import SchemaRegistry, export_schema, validate_data

__all__ = [
    # Errors
    "ConfigurationError",
    "IntegrityError",
    "ModelError",
    # Schemas
    "SchemaRegistry",
    "SecurityError",
    # Configuration
    "Settings",
    "UnunseptiumError",
    "ValidationError",
    # Canonical
    "canonical_json",
    "deterministic_hash",
    "export_schema",
    # Logging
    "get_logger",
    "load_config",
    "setup_logging",
    "validate_data",
]
