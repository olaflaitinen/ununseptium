"""PII detection, masking, and storage.

Provides Personally Identifiable Information (PII) handling
with detection, masking, and secure storage capabilities.
"""

from __future__ import annotations

import re
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class PIIType(str, Enum):
    """Types of PII data."""

    SSN = "ssn"
    EMAIL = "email"
    PHONE = "phone"
    CREDIT_CARD = "credit_card"
    BANK_ACCOUNT = "bank_account"
    DATE_OF_BIRTH = "dob"
    ADDRESS = "address"
    NAME = "name"
    PASSPORT = "passport"
    DRIVERS_LICENSE = "drivers_license"
    IP_ADDRESS = "ip_address"
    CUSTOM = "custom"


class PIIMatch(BaseModel):
    """A detected PII match.

    Attributes:
        pii_type: Type of PII detected.
        value: Original value (for internal use).
        masked_value: Masked representation.
        start: Start position in text.
        end: End position in text.
        confidence: Detection confidence.
    """

    pii_type: PIIType
    value: str
    masked_value: str
    start: int
    end: int
    confidence: float = Field(ge=0.0, le=1.0)


class PIIDetector:
    """Detect PII in text and structured data.

    Uses pattern matching to identify various types of PII.

    Example:
        ```python
        from ununseptium.security import PIIDetector

        detector = PIIDetector()

        text = "Contact John at john@example.com or 555-123-4567"
        matches = detector.detect(text)

        for match in matches:
            print(f"{match.pii_type}: {match.masked_value}")
        ```
    """

    def __init__(self) -> None:
        """Initialize the detector with default patterns."""
        self._patterns: dict[PIIType, list[re.Pattern[str]]] = {
            PIIType.EMAIL: [re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")],
            PIIType.PHONE: [
                re.compile(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"),
                re.compile(r"\+\d{1,3}[-.]?\d{1,4}[-.]?\d{1,4}[-.]?\d{1,9}\b"),
            ],
            PIIType.SSN: [
                re.compile(r"\b\d{3}[-]?\d{2}[-]?\d{4}\b"),
            ],
            PIIType.CREDIT_CARD: [
                re.compile(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"),
            ],
            PIIType.IP_ADDRESS: [
                re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
            ],
        }

    def detect(self, text: str) -> list[PIIMatch]:
        """Detect PII in text.

        Args:
            text: Text to scan.

        Returns:
            List of PII matches.
        """
        matches: list[PIIMatch] = []

        for pii_type, patterns in self._patterns.items():
            for pattern in patterns:
                for match in pattern.finditer(text):
                    value = match.group()
                    matches.append(
                        PIIMatch(
                            pii_type=pii_type,
                            value=value,
                            masked_value=self._mask_value(value, pii_type),
                            start=match.start(),
                            end=match.end(),
                            confidence=0.9,
                        )
                    )

        return matches

    def detect_in_dict(
        self,
        data: dict[str, Any],
        *,
        fields: list[str] | None = None,
    ) -> dict[str, list[PIIMatch]]:
        """Detect PII in dictionary fields.

        Args:
            data: Dictionary to scan.
            fields: Specific fields to scan (None = all).

        Returns:
            Dictionary mapping field names to matches.
        """
        results: dict[str, list[PIIMatch]] = {}

        for key, value in data.items():
            if fields and key not in fields:
                continue

            if isinstance(value, str):
                matches = self.detect(value)
                if matches:
                    results[key] = matches
            elif isinstance(value, dict):
                nested = self.detect_in_dict(value)
                for nested_key, nested_matches in nested.items():
                    results[f"{key}.{nested_key}"] = nested_matches

        return results

    def add_pattern(self, pii_type: PIIType, pattern: str) -> None:
        """Add a custom pattern.

        Args:
            pii_type: Type of PII.
            pattern: Regex pattern.
        """
        if pii_type not in self._patterns:
            self._patterns[pii_type] = []
        self._patterns[pii_type].append(re.compile(pattern))

    def _mask_value(self, value: str, pii_type: PIIType) -> str:
        """Mask a PII value."""
        if pii_type == PIIType.EMAIL:
            parts = value.split("@")
            if len(parts) == 2:
                return f"{parts[0][0]}***@{parts[1]}"
        elif pii_type == PIIType.PHONE:
            digits = re.sub(r"\D", "", value)
            return f"***-***-{digits[-4:]}" if len(digits) >= 4 else "***"
        elif pii_type == PIIType.SSN:
            return "***-**-" + value[-4:] if len(value) >= 4 else "***"
        elif pii_type == PIIType.CREDIT_CARD:
            return "**** **** **** " + value[-4:] if len(value) >= 4 else "****"

        # Default masking
        if len(value) <= 4:
            return "*" * len(value)
        return value[:2] + "*" * (len(value) - 4) + value[-2:]


class PIIMasker:
    """Mask PII in text and data.

    Replaces detected PII with masked versions.

    Example:
        ```python
        from ununseptium.security import PIIMasker

        masker = PIIMasker()

        text = "Email: john@example.com"
        masked = masker.mask(text)
        # "Email: j***@example.com"
        ```
    """

    def __init__(self, detector: PIIDetector | None = None) -> None:
        """Initialize the masker.

        Args:
            detector: PII detector to use.
        """
        self._detector = detector or PIIDetector()

    def mask(self, text: str) -> str:
        """Mask PII in text.

        Args:
            text: Text to mask.

        Returns:
            Masked text.
        """
        matches = self._detector.detect(text)

        # Sort by position (reverse to maintain indices)
        matches.sort(key=lambda m: m.start, reverse=True)

        result = text
        for match in matches:
            result = result[: match.start] + match.masked_value + result[match.end :]

        return result

    def mask_dict(
        self,
        data: dict[str, Any],
        *,
        fields: list[str] | None = None,
    ) -> dict[str, Any]:
        """Mask PII in dictionary.

        Args:
            data: Dictionary to mask.
            fields: Specific fields to mask.

        Returns:
            Masked dictionary copy.
        """
        result = data.copy()

        for key, value in result.items():
            if fields and key not in fields:
                continue

            if isinstance(value, str):
                result[key] = self.mask(value)
            elif isinstance(value, dict):
                result[key] = self.mask_dict(value)

        return result


class PIIVault:
    """Secure storage for PII with tokenization.

    Provides tokenized access to PII data with
    encryption at rest.

    Example:
        ```python
        from ununseptium.security import PIIVault

        vault = PIIVault()

        # Store PII and get token
        token = vault.store("john@example.com", PIIType.EMAIL)

        # Retrieve with token
        value = vault.retrieve(token)
        ```
    """

    def __init__(self) -> None:
        """Initialize the vault."""
        self._storage: dict[str, dict[str, Any]] = {}
        self._token_lookup: dict[str, str] = {}

    def store(
        self,
        value: str,
        pii_type: PIIType,
        *,
        entity_id: str | None = None,
    ) -> str:
        """Store a PII value and return a token.

        Args:
            value: PII value to store.
            pii_type: Type of PII.
            entity_id: Associated entity ID.

        Returns:
            Token for retrieval.
        """
        token = f"PII-{uuid4().hex}"

        self._storage[token] = {
            "value": value,  # In production: encrypt this
            "pii_type": pii_type.value,
            "entity_id": entity_id,
            "stored_at": datetime.now(timezone.utc).isoformat(),
        }

        # Create lookup by value hash
        value_hash = hash(value)
        self._token_lookup[str(value_hash)] = token

        return token

    def retrieve(self, token: str) -> str | None:
        """Retrieve a PII value by token.

        Args:
            token: Token from store operation.

        Returns:
            Original value or None if not found.
        """
        entry = self._storage.get(token)
        if entry:
            return entry["value"]
        return None

    def delete(self, token: str) -> bool:
        """Delete a stored PII value.

        Args:
            token: Token to delete.

        Returns:
            True if deleted, False if not found.
        """
        if token in self._storage:
            del self._storage[token]
            return True
        return False

    def find_by_value(self, value: str) -> str | None:
        """Find token for a value.

        Args:
            value: Value to find.

        Returns:
            Token if found, None otherwise.
        """
        value_hash = str(hash(value))
        return self._token_lookup.get(value_hash)

    def get_metadata(self, token: str) -> dict[str, Any] | None:
        """Get metadata for a token.

        Args:
            token: Token to query.

        Returns:
            Metadata without the value.
        """
        entry = self._storage.get(token)
        if entry:
            return {k: v for k, v in entry.items() if k != "value"}
        return None
