# Cryptography and Key Management

## Scope

This document describes cryptographic mechanisms and key management in ununseptium.

### Non-Goals

- Hardware security module (HSM) integration
- Enterprise key management systems
- Cryptographic protocol design

## Definitions

| Term | Definition |
|------|------------|
| Symmetric Encryption | Same key for encrypt/decrypt |
| Fernet | Symmetric encryption using AES-128-CBC + HMAC |
| Key Derivation | Generate keys from passwords |
| Key Rotation | Periodic key replacement |

See [Glossary](../glossary.md) for additional terminology.

## Encryption Overview

```mermaid
graph TB
    subgraph "Encryption"
        PLAIN[Plaintext] --> ENC[Encrypt]
        KEY1[Key] --> ENC
        ENC --> CIPHER[Ciphertext]
    end

    subgraph "Decryption"
        CIPHER2[Ciphertext] --> DEC[Decrypt]
        KEY2[Key] --> DEC
        DEC --> PLAIN2[Plaintext]
    end

```text
## Supported Algorithms

| Algorithm | Use Case | Security Level |
|-----------|----------|----------------|
| Fernet (AES-128-CBC) | Data encryption | Production |
| SHA-256 | Hashing | Production |
| PBKDF2 | Key derivation | Production |
| XOR (fallback) | Demo only | NOT secure |

### Fernet Encryption

Fernet provides:

- AES-128-CBC encryption
- HMAC-SHA256 authentication
- Timestamp verification
- Base64 URL-safe encoding

```python
from ununseptium.security import Encryptor

enc = Encryptor()
enc.generate_key()

ciphertext = enc.encrypt(b"sensitive data")
plaintext = enc.decrypt(ciphertext)

```text
### Algorithm Selection

$$\text{Security} = f(\text{Algorithm}, \text{KeySize}, \text{Implementation})$$

| Factor | Fernet | XOR Fallback |
|--------|--------|--------------|
| Algorithm strength | Strong | None |
| Key size | 256 bits | Variable |
| Authentication | Yes (HMAC) | No |
| Production use | Yes | No |

## Key Management

### Key Generation

```python
from ununseptium.security import Encryptor

enc = Encryptor()

# Generate random key
enc.generate_key()

# Export key (store securely!)
key_bytes = enc.export_key()

```text
### Key Storage

| Storage Method | Security | Use Case |
|----------------|----------|----------|
| Environment variable | Medium | Development |
| Secrets manager | High | Production |
| HSM | Very high | Regulated |
| File (encrypted) | Medium | Backup |

> **Warning**: Never store keys in code, logs, or version control.

### Key Loading

```python
# Load from bytes
enc.load_key(key_bytes)

# Load from file (ensure file is encrypted at rest)
with open("key.bin", "rb") as f:
    enc.load_key(f.read())

```text
### Key Rotation

Regular key rotation reduces exposure:

```python
# Generate new key
new_key = enc.rotate_key()

# Re-encrypt data with new key
new_ciphertext = enc.encrypt(enc.decrypt(old_ciphertext))

```text
#### Rotation Schedule

| Data Sensitivity | Rotation Frequency |
|------------------|-------------------|
| Critical | 30 days |
| High | 90 days |
| Medium | 180 days |
| Low | 365 days |

## Key Derivation

Derive keys from passwords:

```python
from ununseptium.security import derive_key

# Derive key from password
key = derive_key(
    password="user_password",
    salt=b"random_salt",
    iterations=600000,  # OWASP recommended
)

```text
### PBKDF2 Parameters

$$\text{Key} = \text{PBKDF2}(\text{Password}, \text{Salt}, \text{Iterations})$$

| Parameter | Recommendation |
|-----------|----------------|
| Algorithm | SHA-256 |
| Iterations | 600,000+ (OWASP 2023) |
| Salt length | 16+ bytes |
| Salt source | Cryptographically random |

## Hash Functions

### SHA-256

Used for integrity verification:

```python
from ununseptium.security import compute_hash

hash_value = compute_hash(data)

```text
### Hash Chain

Audit log integrity:

$$H_n = \text{SHA256}(H_{n-1} \| \text{data}_n)$$

## Encryption Modes

### Single Value

```python
ciphertext = enc.encrypt(b"single value")

```text
### Streaming (Large Data)

```python
# For large files
with enc.stream_encrypt("input.bin", "output.enc") as stream:
    stream.process()

```text
## Error Handling

| Error | Cause | Action |
|-------|-------|--------|
| `InvalidToken` | Wrong key or corrupted | Check key, verify data |
| `InvalidSignature` | Tampered ciphertext | Reject data |
| `KeyNotLoaded` | No key set | Load or generate key |

```python
from ununseptium.security import Encryptor, InvalidToken

try:
    plaintext = enc.decrypt(ciphertext)
except InvalidToken:
    log.error("Decryption failed - invalid key or corrupted data")

```text
## Security Best Practices

| Practice | Implementation |
|----------|----------------|
| Use production backend | Install `cryptography` package |
| Secure key storage | Environment vars, secrets manager |
| Regular rotation | Scheduled key rotation |
| Audit key access | Log key operations |
| Minimize key scope | Different keys per purpose |

## Fallback Encryption

> **Critical Warning**: The XOR fallback is NOT cryptographically secure. It exists only for environments where `cryptography` cannot be installed.

```python
# Check which backend is active
print(enc.backend)  # "fernet" or "xor"

# Warn if using fallback
if enc.backend == "xor":
    warnings.warn("Using insecure XOR fallback!")

```text
## Configuration

```python
from ununseptium.security import SecurityConfig

config = SecurityConfig(
    encryption_enabled=True,
    require_production_crypto=True,  # Fail if cryptography unavailable
    key_rotation_days=90,
)

```text
## CLI Commands

```bash
# Generate key
ununseptium crypto keygen --output key.bin

# Encrypt file
ununseptium crypto encrypt --key key.bin input.txt output.enc

# Decrypt file
ununseptium crypto decrypt --key key.bin output.enc decrypted.txt

```text
## Related Documentation

- [Security Overview](security-overview.md)
- [Threat Model](threat-model.md)
- [Auditability](auditability.md)

## References

- [Fernet Specification](https://github.com/fernet/spec/)
- [NIST SP 800-132 Key Derivation](https://csrc.nist.gov/publications/detail/sp/800-132/final)
- [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [Glossary](../glossary.md)
