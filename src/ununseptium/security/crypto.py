"""Cryptographic operations for security.

Provides encryption, hashing, and key management with
secure defaults.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import os
import secrets
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    pass


class HashResult(BaseModel):
    """Result of a hash operation.

    Attributes:
        algorithm: Hash algorithm used.
        digest: Hex-encoded hash digest.
        salt: Salt used (if applicable).
    """

    algorithm: str
    digest: str
    salt: str | None = None

    def __str__(self) -> str:
        """Return prefixed hash string."""
        return f"{self.algorithm}:{self.digest}"


class Hasher:
    """Secure hashing utilities.

    Provides consistent hashing with constant-time comparison.

    Example:
        ```python
        from ununseptium.security import Hasher

        hasher = Hasher()

        # Hash data
        result = hasher.hash("sensitive data")
        print(result.digest)

        # Verify with constant-time comparison
        is_valid = hasher.verify("sensitive data", result)
        ```
    """

    def __init__(self, algorithm: str = "sha256") -> None:
        """Initialize the hasher.

        Args:
            algorithm: Hash algorithm (sha256, sha384, sha512).
        """
        self.algorithm = algorithm

    def hash(
        self,
        data: str | bytes,
        *,
        salt: str | None = None,
    ) -> HashResult:
        """Hash data.

        Args:
            data: Data to hash.
            salt: Optional salt to prepend.

        Returns:
            HashResult with digest.
        """
        if isinstance(data, str):
            data = data.encode("utf-8")

        if salt is None:
            salt = secrets.token_hex(16)

        salted_data = salt.encode("utf-8") + data
        hasher = hashlib.new(self.algorithm)
        hasher.update(salted_data)

        return HashResult(
            algorithm=self.algorithm,
            digest=hasher.hexdigest(),
            salt=salt,
        )

    def hash_no_salt(self, data: str | bytes) -> HashResult:
        """Hash data without salt.

        Args:
            data: Data to hash.

        Returns:
            HashResult with digest.
        """
        if isinstance(data, str):
            data = data.encode("utf-8")

        hasher = hashlib.new(self.algorithm)
        hasher.update(data)

        return HashResult(
            algorithm=self.algorithm,
            digest=hasher.hexdigest(),
        )

    def verify(
        self,
        data: str | bytes,
        expected: HashResult | str,
    ) -> bool:
        """Verify data against a hash using constant-time comparison.

        Args:
            data: Data to verify.
            expected: Expected hash result or string.

        Returns:
            True if hash matches.
        """
        if isinstance(data, str):
            data = data.encode("utf-8")

        if isinstance(expected, str):
            # Parse "algorithm:digest" format
            if ":" in expected:
                algo, digest = expected.split(":", 1)
                expected = HashResult(algorithm=algo, digest=digest)
            else:
                expected = HashResult(algorithm=self.algorithm, digest=expected)

        if expected.salt:
            salted_data = expected.salt.encode("utf-8") + data
        else:
            salted_data = data

        hasher = hashlib.new(expected.algorithm)
        hasher.update(salted_data)
        actual_digest = hasher.hexdigest()

        return hmac.compare_digest(actual_digest, expected.digest)

    @staticmethod
    def constant_time_compare(a: str | bytes, b: str | bytes) -> bool:
        """Constant-time string comparison.

        Args:
            a: First value.
            b: Second value.

        Returns:
            True if equal.
        """
        if isinstance(a, str):
            a = a.encode("utf-8")
        if isinstance(b, str):
            b = b.encode("utf-8")
        return hmac.compare_digest(a, b)


class EncryptedData(BaseModel):
    """Encrypted data container.

    Attributes:
        ciphertext: Base64-encoded ciphertext.
        nonce: Base64-encoded nonce/IV.
        algorithm: Encryption algorithm.
        key_id: Key identifier.
    """

    ciphertext: str
    nonce: str
    algorithm: str = "fernet"
    key_id: str | None = None


class Encryptor:
    """Encryption utilities.

    Provides symmetric encryption with secure defaults.
    Requires the 'cryptography' extra.

    Example:
        ```python
        from ununseptium.security import Encryptor

        encryptor = Encryptor()
        encryptor.generate_key()

        # Encrypt
        encrypted = encryptor.encrypt("sensitive data")

        # Decrypt
        decrypted = encryptor.decrypt(encrypted)
        ```
    """

    def __init__(self, key: bytes | None = None) -> None:
        """Initialize the encryptor.

        Args:
            key: Encryption key (generated if not provided).
        """
        self._key = key
        self._fernet: object | None = None

    def generate_key(self) -> bytes:
        """Generate a new encryption key.

        Returns:
            Generated key.
        """
        try:
            from cryptography.fernet import Fernet

            self._key = Fernet.generate_key()
            self._fernet = Fernet(self._key)
            return self._key
        except ImportError:
            # Fallback: generate random key
            self._key = secrets.token_bytes(32)
            return self._key

    def set_key(self, key: bytes) -> None:
        """Set the encryption key.

        Args:
            key: Encryption key.
        """
        self._key = key
        try:
            from cryptography.fernet import Fernet

            self._fernet = Fernet(key)
        except ImportError:
            pass

    def encrypt(self, data: str | bytes, *, key_id: str | None = None) -> EncryptedData:
        """Encrypt data.

        Args:
            data: Data to encrypt.
            key_id: Key identifier for tracking.

        Returns:
            EncryptedData container.
        """
        if isinstance(data, str):
            data = data.encode("utf-8")

        if self._fernet is not None:
            # Use Fernet if available
            ciphertext = self._fernet.encrypt(data)  # type: ignore[union-attr]
            return EncryptedData(
                ciphertext=base64.b64encode(ciphertext).decode("ascii"),
                nonce="",  # Fernet handles nonce internally
                algorithm="fernet",
                key_id=key_id,
            )

        # Fallback: XOR with key (NOT cryptographically secure - demo only)
        if self._key is None:
            self.generate_key()

        nonce = secrets.token_bytes(16)
        key_stream = self._derive_key_stream(nonce, len(data))
        ciphertext = bytes(a ^ b for a, b in zip(data, key_stream, strict=False))

        return EncryptedData(
            ciphertext=base64.b64encode(ciphertext).decode("ascii"),
            nonce=base64.b64encode(nonce).decode("ascii"),
            algorithm="xor-fallback",
            key_id=key_id,
        )

    def decrypt(self, encrypted: EncryptedData) -> bytes:
        """Decrypt data.

        Args:
            encrypted: Encrypted data container.

        Returns:
            Decrypted data.
        """
        if encrypted.algorithm == "fernet" and self._fernet is not None:
            ciphertext = base64.b64decode(encrypted.ciphertext)
            return self._fernet.decrypt(ciphertext)  # type: ignore[union-attr]

        # Fallback decryption
        ciphertext = base64.b64decode(encrypted.ciphertext)
        nonce = base64.b64decode(encrypted.nonce)
        key_stream = self._derive_key_stream(nonce, len(ciphertext))
        return bytes(a ^ b for a, b in zip(ciphertext, key_stream, strict=False))

    def _derive_key_stream(self, nonce: bytes, length: int) -> bytes:
        """Derive a key stream from key and nonce."""
        if self._key is None:
            msg = "No key set"
            raise ValueError(msg)

        # Simple key derivation (NOT for production)
        stream = b""
        counter = 0
        while len(stream) < length:
            block = hashlib.sha256(self._key + nonce + counter.to_bytes(4, "big")).digest()
            stream += block
            counter += 1
        return stream[:length]


class KeyManager:
    """Manage encryption keys.

    Provides key generation, storage, and rotation.

    Example:
        ```python
        from ununseptium.security import KeyManager

        manager = KeyManager()

        # Create a new key
        key_id = manager.create_key("data-encryption")

        # Get key
        key = manager.get_key(key_id)

        # Rotate key
        new_key_id = manager.rotate_key(key_id)
        ```
    """

    def __init__(self) -> None:
        """Initialize the key manager."""
        self._keys: dict[str, dict[str, object]] = {}

    def create_key(
        self,
        purpose: str,
        *,
        algorithm: str = "fernet",
    ) -> str:
        """Create a new key.

        Args:
            purpose: Key purpose description.
            algorithm: Key algorithm.

        Returns:
            Key identifier.
        """
        key_id = f"KEY-{secrets.token_hex(8)}"

        if algorithm == "fernet":
            try:
                from cryptography.fernet import Fernet

                key_material = Fernet.generate_key()
            except ImportError:
                key_material = secrets.token_bytes(32)
        else:
            key_material = secrets.token_bytes(32)

        self._keys[key_id] = {
            "key": key_material,
            "purpose": purpose,
            "algorithm": algorithm,
            "created_at": os.urandom(0),  # Placeholder
            "active": True,
        }

        return key_id

    def get_key(self, key_id: str) -> bytes | None:
        """Get a key by ID.

        Args:
            key_id: Key identifier.

        Returns:
            Key material or None.
        """
        entry = self._keys.get(key_id)
        if entry and entry.get("active"):
            return entry["key"]  # type: ignore[return-value]
        return None

    def rotate_key(self, old_key_id: str) -> str:
        """Rotate a key.

        Args:
            old_key_id: Key to rotate.

        Returns:
            New key ID.
        """
        old_entry = self._keys.get(old_key_id)
        if not old_entry:
            msg = f"Key not found: {old_key_id}"
            raise ValueError(msg)

        # Deactivate old key
        old_entry["active"] = False

        # Create new key with same purpose
        return self.create_key(
            str(old_entry["purpose"]),
            algorithm=str(old_entry.get("algorithm", "fernet")),
        )

    def delete_key(self, key_id: str) -> bool:
        """Delete a key.

        Args:
            key_id: Key to delete.

        Returns:
            True if deleted.
        """
        if key_id in self._keys:
            del self._keys[key_id]
            return True
        return False

    def list_keys(self, *, active_only: bool = True) -> list[str]:
        """List key IDs.

        Args:
            active_only: Only return active keys.

        Returns:
            List of key IDs.
        """
        return [
            k
            for k, v in self._keys.items()
            if not active_only or v.get("active", True)
        ]
