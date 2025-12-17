"""Basic import and smoke tests for ununseptium."""

from __future__ import annotations


def test_import_ununseptium():
    """Test that ununseptium can be imported."""
    import ununseptium

    assert hasattr(ununseptium, "__version__")
    assert isinstance(ununseptium.__version__, str)


def test_import_core():
    """Test core module imports."""
    from ununseptium.core import Settings, load_config

    assert Settings is not None
    assert load_config is not None


def test_import_kyc():
    """Test KYC module imports."""
    from ununseptium.kyc import IdentityVerifier

    assert IdentityVerifier is not None


def test_import_aml():
    """Test AML module imports."""
    from ununseptium.aml import Transaction, TransactionParser

    assert Transaction is not None
    assert TransactionParser is not None


def test_import_security():
    """Test security module imports."""
    from ununseptium.security import PIIDetector, AuditLog

    assert PIIDetector is not None
    assert AuditLog is not None


def test_import_ai():
    """Test AI module imports."""
    from ununseptium.ai import RiskScorer, FeatureEngineer

    assert RiskScorer is not None
    assert FeatureEngineer is not None


def test_import_mathstats():
    """Test mathstats module imports."""
    from ununseptium.mathstats import EVTAnalyzer, HawkesProcess

    assert EVTAnalyzer is not None
    assert HawkesProcess is not None


def test_version_format():
    """Test version follows semver format."""
    import re

    import ununseptium

    version_pattern = r"^\d+\.\d+\.\d+.*$"
    assert re.match(version_pattern, ununseptium.__version__)
