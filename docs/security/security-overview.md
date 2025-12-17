# Security Overview

## Scope

This document describes the security module in ununseptium, providing data protection, cryptography, access control, and audit capabilities.

### Non-Goals

- Infrastructure security (user responsibility)
- Network security configurations
- Physical security requirements

## Definitions

| Term | Definition |
|------|------------|
| PII | Personally Identifiable Information |
| RBAC | Role-Based Access Control |
| Hash Chain | Linked sequence of cryptographic hashes |
| Fernet | Symmetric encryption scheme using AES-128-CBC |

See [Glossary](../glossary.md) for additional terminology.

## Module Structure

```mermaid
graph TB
    subgraph "Security Module"
        PII[PII Scanner]
        MASK[Data Masking]
        CRYPTO[Encryption]
        ACCESS[Access Control]
        AUDIT[Audit Log]
    end

    subgraph "Dependencies"
        CORE[core module]
        CRYPTOLIB[cryptography lib]
    end

    PII --> MASK
    MASK --> CRYPTO
    CRYPTO --> CRYPTOLIB
    ACCESS --> CORE
    AUDIT --> CORE

```text
## Components

### PII Detection

Pattern-based PII scanner:

```python
from ununseptium.security import PIIScanner

scanner = PIIScanner()
findings = scanner.scan("My SSN is 123-45-6789")

for finding in findings:
    print(f"Type: {finding.pii_type}")
    print(f"Value: {finding.value}")
    print(f"Position: {finding.start}-{finding.end}")

```text
#### Supported PII Types

| Type | Pattern | Examples |
|------|---------|----------|
| SSN | `\d{3}-\d{2}-\d{4}` | 123-45-6789 |
| Email | RFC 5322 | john@example.com |
| Phone | E.164 variants | +1-555-123-4567 |
| Credit Card | Luhn-validated | 4111111111111111 |
| IBAN | ISO 13616 | DE89370400440532013000 |
| IP Address | IPv4/IPv6 | 192.168.1.1 |

#### Custom Patterns

```python
from ununseptium.security import PIIScanner, PIIPattern

custom = PIIPattern(
    name="custom_id",
    pattern=r"CUST-\d{6}",
    description="Customer ID",
)

scanner = PIIScanner(patterns=[custom])

```text
### Data Masking

Tokenization and redaction:

```python
from ununseptium.security import Masker

masker = Masker()

# Mask with tokens (reversible)
masked, tokens = masker.mask(text, reversible=True)

# Later: unmask
original = masker.unmask(masked, tokens)

# Redact (non-reversible)
redacted = masker.redact(text)

```text
#### Masking Strategies

| Strategy | Reversible | Output |
|----------|------------|--------|
| Tokenization | Yes | `[TOKEN:abc123]` |
| Partial | No | `***-**-6789` |
| Redaction | No | `[REDACTED]` |
| Hash | No | `sha256:a1b2c3...` |

### Encryption

Symmetric encryption:

```python
from ununseptium.security import Encryptor

encryptor = Encryptor()
encryptor.generate_key()

# Encrypt
ciphertext = encryptor.encrypt(b"sensitive data")

# Decrypt
plaintext = encryptor.decrypt(ciphertext)

```text
#### Encryption Backends

| Backend | Algorithm | Security Level |
|---------|-----------|----------------|
| cryptography | Fernet (AES-128-CBC + HMAC) | Production |
| fallback (XOR) | XOR | NOT secure, demo only |

> **Warning**: Always install the `cryptography` package for production use. The XOR fallback is for demonstration only.

#### Key Management

```python
# Save key securely
key = encryptor.export_key()

# Load key
encryptor.load_key(key)

# Rotate key
encryptor.rotate_key()

```text
### Access Control

Role-based access control:

```python
from ununseptium.security import RBACManager, Role, Permission

manager = RBACManager()

# Define roles
analyst = Role(
    name="analyst",
    permissions=[
        Permission.READ_CASES,
        Permission.CREATE_ALERTS,
    ]
)

manager.add_role(analyst)

# Check access
if manager.check(user, Permission.READ_CASES):
    # Allow access
    pass

```text
#### Permission Model

```mermaid
graph TB
    USER[User] --> ROLE[Role]
    ROLE --> PERM1[Permission 1]
    ROLE --> PERM2[Permission 2]
    ROLE --> PERM3[Permission 3]

```text
| Permission Level | Access |
|------------------|--------|
| READ | View data |
| WRITE | Modify data |
| DELETE | Remove data |
| ADMIN | Full control |

### Audit Logging

Tamper-evident audit trail:

```python
from ununseptium.security import AuditLog

log = AuditLog()

# Append entry
log.append({
    "action": "identity_verified",
    "identity_id": "ID-001",
    "result": "approved",
})

# Save
log.save("audit.log")

# Verify integrity
assert log.verify(), "Tampering detected"

```text
#### Hash Chain

Each entry is linked to its predecessor:

$$H_n = \text{SHA256}(H_{n-1} \| \text{JSON}(\text{entry}_n))$$

This creates a tamper-evident chain where modifying any entry invalidates all subsequent hashes.

```mermaid
graph LR
    E1[Entry 1<br>H1] --> E2[Entry 2<br>H2=SHA256 H1+E2]
    E2 --> E3[Entry 3<br>H3=SHA256 H2+E3]
    E3 --> E4[Entry 4<br>H4=SHA256 H3+E4]

```text
#### Audit Entry Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | str | Unique ID |
| `timestamp` | ISO-8601 | Entry time |
| `action` | str | Action performed |
| `actor` | str | Who performed |
| `resource` | str | Affected resource |
| `details` | dict | Additional data |
| `prev_hash` | str | Previous hash |
| `entry_hash` | str | This entry hash |

## Security Pipeline

```mermaid
graph TB
    INPUT[Input Data] --> SCAN[PII Scan]
    SCAN --> DETECT{PII Found?}
    DETECT -->|Yes| MASK[Mask PII]
    DETECT -->|No| PROCESS[Process]
    MASK --> PROCESS
    PROCESS --> ENCRYPT{Sensitive?}
    ENCRYPT -->|Yes| ENC[Encrypt]
    ENCRYPT -->|No| OUTPUT[Output]
    ENC --> OUTPUT
    OUTPUT --> AUDIT[Audit Log]

```text
## Configuration

```python
from ununseptium.security import SecurityConfig

config = SecurityConfig(
    encryption_enabled=True,
    audit_enabled=True,
    pii_detection_enabled=True,
    masking_strategy="tokenization",
)

```text
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `encryption_enabled` | bool | True | Enable encryption |
| `audit_enabled` | bool | True | Enable audit logs |
| `pii_detection_enabled` | bool | True | Enable PII scan |
| `masking_strategy` | str | tokenization | Masking method |

## CLI Commands

```bash
# Verify audit log integrity
ununseptium audit verify audit.log

# Show audit entries
ununseptium audit show audit.log --limit 20

# Export audit log
ununseptium audit export audit.log --format json --output export.json

```text
## Related Documentation

- [Threat Model](threat-model.md)
- [Auditability](auditability.md)
- [Crypto and Key Management](crypto-and-key-management.md)

## References

- [NIST Cryptographic Standards](https://csrc.nist.gov/publications/sp)
- [OWASP Data Protection](https://owasp.org/www-project-data-protection/)
- [Glossary](../glossary.md)
