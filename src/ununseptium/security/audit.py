"""Tamper-evident audit logging.

Provides hash-chain based audit logs with cryptographic
verification for tamper detection.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from ununseptium.core.canonical import canonical_json, deterministic_hash


class AuditEntry(BaseModel):
    """An entry in the audit log.

    Attributes:
        id: Entry identifier.
        timestamp: Entry timestamp.
        action: Action performed.
        actor: Who performed the action.
        resource: Affected resource.
        resource_id: Resource identifier.
        details: Action details.
        prev_hash: Hash of previous entry.
        entry_hash: Hash of this entry.
        metadata: Additional data.
    """

    id: str = Field(default_factory=lambda: f"AUD-{uuid4().hex[:12].upper()}")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    action: str
    actor: str | None = None
    resource: str | None = None
    resource_id: str | None = None
    details: dict[str, Any] = Field(default_factory=dict)
    prev_hash: str = ""
    entry_hash: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)

    def compute_hash(self) -> str:
        """Compute the hash for this entry.

        Returns:
            Hash string.
        """
        data = {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "action": self.action,
            "actor": self.actor,
            "resource": self.resource,
            "resource_id": self.resource_id,
            "details": self.details,
            "prev_hash": self.prev_hash,
        }
        return deterministic_hash(data, algorithm="sha256")


class HashChain:
    """Cryptographic hash chain for integrity.

    Links entries with cryptographic hashes to detect tampering.

    Example:
        ```python
        from ununseptium.security import HashChain

        chain = HashChain()

        chain.append({"action": "login", "user": "admin"})
        chain.append({"action": "update", "resource": "config"})

        # Verify integrity
        is_valid, index = chain.verify()
        assert is_valid
        ```
    """

    def __init__(self, algorithm: str = "sha256") -> None:
        """Initialize the hash chain.

        Args:
            algorithm: Hash algorithm to use.
        """
        self.algorithm = algorithm
        self._entries: list[dict[str, Any]] = []
        self._hashes: list[str] = []

    def append(self, data: dict[str, Any]) -> str:
        """Append data to the chain.

        Args:
            data: Data to append.

        Returns:
            Hash of the new entry.
        """
        prev_hash = self._hashes[-1] if self._hashes else ""

        chain_data = {
            "index": len(self._entries),
            "prev_hash": prev_hash,
            "data": data,
            "timestamp": datetime.now(UTC).isoformat(),
        }

        entry_hash = deterministic_hash(chain_data, algorithm=self.algorithm)

        self._entries.append(chain_data)
        self._hashes.append(entry_hash)

        return entry_hash

    def verify(self) -> tuple[bool, int | None]:
        """Verify the integrity of the chain.

        Returns:
            Tuple of (is_valid, first_invalid_index).
        """
        if not self._entries:
            return True, None

        prev_hash = ""

        for i, entry in enumerate(self._entries):
            # Verify prev_hash linkage
            if entry["prev_hash"] != prev_hash:
                return False, i

            # Verify entry hash
            computed = deterministic_hash(entry, algorithm=self.algorithm)

            # Extract just the hash part (remove algorithm prefix)
            computed_digest = computed.split(":", 1)[1] if ":" in computed else computed
            stored_digest = (
                self._hashes[i].split(":", 1)[1] if ":" in self._hashes[i] else self._hashes[i]
            )

            if computed_digest != stored_digest:
                return False, i

            prev_hash = self._hashes[i]

        return True, None

    def __len__(self) -> int:
        """Return number of entries."""
        return len(self._entries)

    def get_entries(self) -> list[dict[str, Any]]:
        """Get all entries.

        Returns:
            List of chain entries.
        """
        return list(self._entries)


class AuditLog:
    """Tamper-evident audit log.

    Provides comprehensive audit logging with hash-chain
    integrity verification.

    Example:
        ```python
        from ununseptium.security import AuditLog

        log = AuditLog()

        log.append({
            "action": "identity_verified",
            "identity_id": "ID-001",
            "result": "approved"
        })

        log.save("audit.log")

        # Later: verify integrity
        loaded = AuditLog.load("audit.log")
        is_valid = loaded.verify()
        ```
    """

    def __init__(self) -> None:
        """Initialize the audit log."""
        self._chain = HashChain()
        self._entries: list[AuditEntry] = []

    def append(
        self,
        data: dict[str, Any],
        *,
        action: str | None = None,
        actor: str | None = None,
        resource: str | None = None,
        resource_id: str | None = None,
    ) -> AuditEntry:
        """Append an entry to the log.

        Args:
            data: Entry data.
            action: Action performed.
            actor: Who performed the action.
            resource: Affected resource.
            resource_id: Resource identifier.

        Returns:
            Created AuditEntry.
        """
        prev_hash = self._chain._hashes[-1] if self._chain._hashes else ""

        entry = AuditEntry(
            action=action or data.get("action", "unknown"),
            actor=actor or data.get("actor"),
            resource=resource or data.get("resource"),
            resource_id=resource_id or data.get("resource_id"),
            details=data,
            prev_hash=prev_hash,
        )

        entry.entry_hash = entry.compute_hash()
        self._entries.append(entry)
        self._chain.append(entry.model_dump(mode="json"))

        return entry

    def verify(self) -> bool:
        """Verify log integrity.

        Returns:
            True if log is valid.
        """
        is_valid, _ = self._chain.verify()
        return is_valid

    def verify_detailed(self) -> tuple[bool, int | None, str]:
        """Verify log with detailed result.

        Returns:
            Tuple of (is_valid, index, message).
        """
        is_valid, index = self._chain.verify()

        if is_valid:
            return True, None, "Audit log integrity verified"

        return False, index, f"Integrity check failed at entry {index}"

    def save(self, path: Path | str) -> None:
        """Save audit log to file.

        Args:
            path: File path.
        """
        path = Path(path)
        data = {
            "version": "1.0",
            "algorithm": self._chain.algorithm,
            "entries": [e.model_dump(mode="json") for e in self._entries],
            "hashes": self._chain._hashes,
        }

        with path.open("w") as f:
            f.write(canonical_json(data, indent=2))

    @classmethod
    def load(cls, path: Path | str) -> AuditLog:
        """Load audit log from file.

        Args:
            path: File path.

        Returns:
            Loaded AuditLog.
        """
        path = Path(path)

        with path.open() as f:
            data = json.load(f)

        log = cls()
        log._chain.algorithm = data.get("algorithm", "sha256")

        for entry_data in data.get("entries", []):
            entry = AuditEntry.model_validate(entry_data)
            log._entries.append(entry)

        log._chain._entries = [
            {
                "index": i,
                "prev_hash": e.prev_hash,
                "data": e.model_dump(mode="json"),
                "timestamp": e.timestamp.isoformat(),
            }
            for i, e in enumerate(log._entries)
        ]
        log._chain._hashes = data.get("hashes", [])

        return log

    def __len__(self) -> int:
        """Return number of entries."""
        return len(self._entries)

    def get_entries(
        self,
        *,
        action: str | None = None,
        actor: str | None = None,
        resource: str | None = None,
    ) -> list[AuditEntry]:
        """Get entries with optional filtering.

        Args:
            action: Filter by action.
            actor: Filter by actor.
            resource: Filter by resource.

        Returns:
            Matching entries.
        """
        entries = self._entries

        if action:
            entries = [e for e in entries if e.action == action]
        if actor:
            entries = [e for e in entries if e.actor == actor]
        if resource:
            entries = [e for e in entries if e.resource == resource]

        return entries


class AuditVerifier:
    """Verify audit log integrity.

    Provides verification utilities for audit logs.

    Example:
        ```python
        from ununseptium.security import AuditVerifier

        verifier = AuditVerifier()

        result = verifier.verify_file("audit.log")
        if result.is_valid:
            print("Audit log is intact")
        else:
            print(f"Tampering detected at entry {result.failed_index}")
        ```
    """

    def verify_file(self, path: Path | str) -> VerificationResult:
        """Verify an audit log file.

        Args:
            path: Path to audit log.

        Returns:
            VerificationResult.
        """
        try:
            log = AuditLog.load(path)
            is_valid, index, message = log.verify_detailed()

            return VerificationResult(
                is_valid=is_valid,
                entry_count=len(log),
                failed_index=index,
                message=message,
                verified_at=datetime.now(UTC),
            )
        except Exception as e:
            return VerificationResult(
                is_valid=False,
                entry_count=0,
                message=f"Verification failed: {e}",
                verified_at=datetime.now(UTC),
            )

    def verify_log(self, log: AuditLog) -> VerificationResult:
        """Verify an audit log instance.

        Args:
            log: AuditLog to verify.

        Returns:
            VerificationResult.
        """
        is_valid, index, message = log.verify_detailed()

        return VerificationResult(
            is_valid=is_valid,
            entry_count=len(log),
            failed_index=index,
            message=message,
            verified_at=datetime.now(UTC),
        )


class VerificationResult(BaseModel):
    """Result of audit verification.

    Attributes:
        is_valid: Whether log is valid.
        entry_count: Number of entries verified.
        failed_index: Index of first failed entry.
        message: Verification message.
        verified_at: Verification timestamp.
    """

    is_valid: bool
    entry_count: int
    failed_index: int | None = None
    message: str
    verified_at: datetime
