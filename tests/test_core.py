"""Tests for core module."""

from __future__ import annotations

import json

import pytest


class TestSettings:
    """Test Settings class."""

    def test_settings_default(self):
        """Test default settings creation."""
        from ununseptium.core import Settings

        settings = Settings()
        assert settings is not None
        assert settings.log_level in ["DEBUG", "INFO", "WARNING", "ERROR"]


class TestCanonicalJson:
    """Test canonical JSON functions."""

    def test_canonical_json_deterministic(self):
        """Test canonical JSON produces deterministic output."""
        from ununseptium.core.canonical import canonical_json

        data = {"b": 2, "a": 1, "c": 3}
        result1 = canonical_json(data)
        result2 = canonical_json(data)

        assert result1 == result2

    def test_canonical_json_sorted_keys(self):
        """Test canonical JSON sorts keys."""
        from ununseptium.core.canonical import canonical_json

        data = {"z": 1, "a": 2, "m": 3}
        result = canonical_json(data)
        parsed = json.loads(result)
        keys = list(parsed.keys())

        assert keys == sorted(keys)


class TestDeterministicHash:
    """Test deterministic hashing."""

    def test_hash_consistency(self):
        """Test hash produces consistent output."""
        from ununseptium.core.canonical import deterministic_hash

        data = {"key": "value", "number": 42}
        hash1 = deterministic_hash(data)
        hash2 = deterministic_hash(data)

        assert hash1 == hash2
        assert isinstance(hash1, str)

    def test_hash_different_data(self):
        """Test different data produces different hashes."""
        from ununseptium.core.canonical import deterministic_hash

        hash1 = deterministic_hash({"a": 1})
        hash2 = deterministic_hash({"a": 2})

        assert hash1 != hash2
