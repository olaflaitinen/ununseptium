# Auditability

## Scope

This document describes the audit trail design and verification mechanisms in ununseptium.

### Non-Goals

- Long-term audit storage solutions
- Regulatory audit requirements by jurisdiction
- Audit report generation for regulators

## Definitions

| Term | Definition |
|------|------------|
| Audit Trail | Chronological record of activities |
| Hash Chain | Sequential hashes linking entries |
| Tamper-Evident | Design that reveals modifications |

See [Glossary](../glossary.md) for additional terminology.

## Design Principles

| Principle | Implementation |
|-----------|----------------|
| Immutability | Append-only log structure |
| Integrity | Cryptographic hash chain |
| Attributability | Actor recorded for each entry |
| Chronology | Monotonic timestamps |
| Completeness | All decisions logged |

## Hash Chain Structure

```mermaid
graph LR
    subgraph "Entry 1"
        H1[Hash: H1]
        D1[Data: E1]
        P1[Prev: Genesis]
    end

    subgraph "Entry 2"
        H2[Hash: H2]
        D2[Data: E2]
        P2[Prev: H1]
    end

    subgraph "Entry 3"
        H3[Hash: H3]
        D3[Data: E3]
        P3[Prev: H2]
    end

    H1 --> P2
    H2 --> P3

```text
### Hash Computation

Each entry hash incorporates:

$$H_n = \text{SHA256}(H_{n-1} \| \text{canonical}(\text{entry}_n))$$

Where `canonical()` provides deterministic JSON serialization.

### Genesis Entry

The first entry uses a predefined genesis hash:

$$H_0 = \text{SHA256}(\text{"ununseptium-audit-genesis-v1"})$$

## Audit Entry Schema

```python
@dataclass
class AuditEntry:
    id: str              # Unique identifier
    timestamp: datetime  # ISO-8601 UTC
    action: str          # Action performed
    actor: str | None    # Who performed (optional)
    resource: str | None # Affected resource
    details: dict        # Additional context
    prev_hash: str       # Previous entry hash
    entry_hash: str      # This entry hash

```text
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | str | Yes | UUID v4 |
| `timestamp` | datetime | Yes | UTC timestamp |
| `action` | str | Yes | Action type |
| `actor` | str | No | User/system ID |
| `resource` | str | No | Resource ID |
| `details` | dict | No | Context data |
| `prev_hash` | str | Yes | Chain link |
| `entry_hash` | str | Yes | Integrity check |

## Verification

### Single Entry Verification

```python
def verify_entry(entry: AuditEntry, prev_hash: str) -> bool:
    expected = compute_hash(prev_hash, entry)
    return entry.entry_hash == expected

```text
### Full Chain Verification

```python
from ununseptium.security import AuditLog

log = AuditLog.load("audit.log")
result = log.verify()

if not result.is_valid:
    print(f"Tamper detected at entry {result.failed_index}")
    print(f"Expected: {result.expected_hash}")
    print(f"Found: {result.actual_hash}")

```text
### Verification Result

| Field | Type | Description |
|-------|------|-------------|
| `is_valid` | bool | Overall validity |
| `failed_index` | int | First failed entry (-1 if valid) |
| `expected_hash` | str | Expected hash at failure |
| `actual_hash` | str | Actual hash at failure |
| `entries_checked` | int | Total entries verified |

## Usage Patterns

### Creating Audit Entries

```python
from ununseptium.security import AuditLog

log = AuditLog()

# Simple action
log.append({"action": "user_login", "actor": "user123"})

# Detailed entry
log.append({
    "action": "identity_verified",
    "actor": "system",
    "resource": "identity:ID-001",
    "details": {
        "result": "approved",
        "score": 0.95,
        "checks_passed": ["document", "screening"],
    }
})

log.save("audit.log")

```text
### Querying Audit Logs

```python
# Load and query
log = AuditLog.load("audit.log")

# Filter by action
verifications = log.filter(action="identity_verified")

# Filter by time range
recent = log.filter(
    start=datetime(2025, 1, 1),
    end=datetime(2025, 1, 31),
)

# Filter by actor
user_actions = log.filter(actor="user123")

```text
### Exporting Audit Logs

```python
# Export to JSON
log.export_json("audit_export.json")

# Export to CSV
log.export_csv("audit_export.csv")

# Export with date range
log.export_json(
    "audit_jan.json",
    start=datetime(2025, 1, 1),
    end=datetime(2025, 1, 31),
)

```text
## Audit Actions

### Standard Action Types

| Action | Description | Details |
|--------|-------------|---------|
| `identity_verified` | KYC verification | Result, score |
| `screening_completed` | Watchlist check | Matches found |
| `alert_generated` | AML alert | Typology, score |
| `case_created` | Case opened | Alert IDs |
| `decision_made` | Human decision | Decision, reason |
| `config_changed` | Configuration update | Old/new values |
| `model_loaded` | ML model loaded | Model ID, checksum |

### Custom Actions

Define your own action types:

```python
log.append({
    "action": "custom:my_action",
    "details": {"custom_field": "value"}
})

```text
## Storage Considerations

### File Format

Default format is newline-delimited JSON (NDJSON):

```json
{"id":"...", "timestamp":"...", "action":"...", ...}
{"id":"...", "timestamp":"...", "action":"...", ...}

```text
### Rotation

```python
from ununseptium.security import AuditLog

# Rotate when size exceeds threshold
log = AuditLog(max_size_mb=100, rotate=True)

# Rotation creates: audit.log, audit.1.log, audit.2.log, ...

```text
### Retention

| Consideration | Recommendation |
|---------------|----------------|
| Regulatory minimum | Per jurisdiction |
| Storage cost | Compress archived logs |
| Query performance | Index by date |

## Security Considerations

| Threat | Mitigation |
|--------|------------|
| Log deletion | Store multiple copies |
| Log modification | Hash chain detection |
| Unauthorized access | File permissions, RBAC |
| PII in logs | Mask sensitive data |

## CLI Commands

```bash
# Verify audit log
ununseptium audit verify audit.log

# Show recent entries
ununseptium audit show audit.log --limit 20

# Filter by action
ununseptium audit show audit.log --action identity_verified

# Export to JSON
ununseptium audit export audit.log --format json --output export.json

```text
## Related Documentation

- [Security Overview](security-overview.md)
- [Threat Model](threat-model.md)
- [Compliance](../../COMPLIANCE.md)

## References

- [NIST SP 800-92 Log Management](https://csrc.nist.gov/publications/detail/sp/800-92/final)
- [Glossary](../glossary.md)
