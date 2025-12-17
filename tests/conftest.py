"""Pytest configuration and fixtures."""

from __future__ import annotations

import pytest


@pytest.fixture
def sample_identity_data() -> dict:
    """Sample identity data for testing."""
    return {
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1990-01-15",
        "nationality": "US",
        "document_type": "passport",
        "document_number": "123456789",
    }


@pytest.fixture
def sample_transaction_data() -> dict:
    """Sample transaction data for testing."""
    return {
        "amount": 1000.00,
        "currency": "USD",
        "sender_id": "SENDER001",
        "receiver_id": "RECEIVER001",
        "transaction_type": "transfer",
    }
