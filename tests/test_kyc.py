"""Tests for KYC module."""

from __future__ import annotations


class TestIdentity:
    """Test Identity class."""

    def test_identity_creation(self):
        """Test basic identity creation."""
        from ununseptium.kyc import Identity

        identity = Identity(
            name="John Doe",
        )
        assert identity.name == "John Doe"
        assert identity.id.startswith("ID-")


class TestIdentityVerifier:
    """Test IdentityVerifier class."""

    def test_verifier_creation(self):
        """Test verifier can be instantiated."""
        from ununseptium.kyc import IdentityVerifier

        verifier = IdentityVerifier()
        assert verifier is not None


class TestScreeningEngine:
    """Test ScreeningEngine class."""

    def test_screening_engine_creation(self):
        """Test screening engine can be instantiated."""
        from ununseptium.kyc import ScreeningEngine

        engine = ScreeningEngine()
        assert engine is not None


class TestEntityResolver:
    """Test EntityResolver class."""

    def test_resolver_creation(self):
        """Test resolver can be instantiated."""
        from ununseptium.kyc import EntityResolver

        resolver = EntityResolver()
        assert resolver is not None
