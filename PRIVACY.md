# Privacy Policy

## Scope

This document describes the data handling principles of the ununseptium library. It applies to the library's computational operations, not to any specific deployment or infrastructure.

### Non-Goals

- This document does not cover infrastructure-level privacy (your responsibility)
- This document does not provide legal compliance certification
- This document does not replace professional legal counsel

## Definitions

| Term | Definition |
|------|------------|
| PII | Personally Identifiable Information - data that can identify an individual |
| Data Subject | The individual to whom personal data relates |
| Processing | Any operation performed on personal data |
| Controller | Entity that determines purposes of processing |
| Processor | Entity that processes data on behalf of controller |

## Important Notice

> **Not Legal Advice**: This document describes the technical data handling characteristics of the ununseptium library. It does not constitute legal advice and should not be relied upon for compliance determinations. Users must conduct their own legal analysis and consult qualified privacy professionals regarding applicable data protection laws (GDPR, CCPA, etc.).

## Data Handling Principles

### Library Design Philosophy

Ununseptium is designed with privacy-by-design principles:

| Principle | Implementation |
|-----------|----------------|
| Data Minimization | Library does not persist data; processing is in-memory |
| Purpose Limitation | Each module has defined, limited data access scope |
| Transparency | All data flows are documented and auditable |
| Security | Encryption and access controls available |

### Data Flow Model

```mermaid
graph LR
    subgraph "Your Infrastructure"
        INPUT[Input Data]
        OUTPUT[Output Data]
        STORAGE[(Your Storage)]
    end

    subgraph "Ununseptium Library"
        PROC[Processing]
        AUDIT[Audit Log]
    end

    INPUT --> PROC
    PROC --> OUTPUT
    PROC --> AUDIT
    OUTPUT --> STORAGE
    AUDIT --> STORAGE

```text
### What the Library Does NOT Do

| Action | Status |
|--------|--------|
| Store data persistently | No - processing is in-memory |
| Transmit data externally | No - no network calls by default |
| Collect telemetry | No - no usage data collection |
| Access external services | No - unless explicitly configured |

### What the Library CAN Do (If You Configure It)

| Capability | Module | Purpose |
|------------|--------|---------|
| PII Detection | `security.pii` | Identify personal data in text |
| PII Masking | `security.masking` | Remove or tokenize PII |
| Encryption | `security.encryption` | Encrypt sensitive data |
| Audit Logging | `security.audit` | Create tamper-evident logs |

## PII Detection

The `security.pii` module can detect the following data types:

| Category | Examples |
|----------|----------|
| Identifiers | SSN, passport numbers, driver's license |
| Contact | Email, phone, address |
| Financial | Credit card, bank account |
| Biometric | Fingerprint hashes (patterns only) |
| Location | IP addresses, GPS coordinates |

### Detection Limitations

- Pattern-based detection may have false negatives
- Custom PII patterns may require configuration
- Detection does not guarantee compliance

## Threat Boundaries

### Library Responsibility

The ununseptium library is responsible for:

| Responsibility | Implementation |
|----------------|----------------|
| Secure algorithms | Reviewed cryptographic implementations |
| Input validation | Schema validation via Pydantic |
| Audit capability | Hash-chain audit logs |
| Documentation | Clear data handling documentation |

### User Responsibility

Users are responsible for:

| Responsibility | Examples |
|----------------|----------|
| Infrastructure security | Network, storage, access controls |
| Data governance | Retention policies, access policies |
| Legal compliance | GDPR, CCPA, sector-specific laws |
| Risk assessment | DPIA, vendor due diligence |

### Out of Scope

The library does NOT address:

- Physical security
- Personnel security
- Third-party integrations
- Incident response procedures

## International Data Transfers

The ununseptium library does not transfer data internationally. Any cross-border data flows are determined by:

1. Your infrastructure deployment
2. Your configuration choices
3. Your integration with external services

Users must ensure appropriate safeguards for international transfers.

## Data Subject Rights

Ununseptium provides utilities that can assist with data subject rights:

| Right | Library Support |
|-------|-----------------|
| Access | Audit logs document processing |
| Rectification | Data is not stored; rectify at source |
| Erasure | No persistence; erase from your storage |
| Portability | Standard schemas enable export |

Implementation of these rights is the user's responsibility.

## Retention

The library does not retain data. Retention policies apply to:

- Your storage systems
- Audit logs you generate
- Any caches you implement

## Security Measures

See [SECURITY.md](SECURITY.md) and [docs/security/security-overview.md](docs/security/security-overview.md) for security measures.

## Updates to This Document

This document may be updated to reflect:

- New library features
- Clarified data handling practices
- Community feedback

Check the [CHANGELOG.md](CHANGELOG.md) for updates.

## References

- [GDPR](https://gdpr.eu/) - General Data Protection Regulation
- [CCPA](https://oag.ca.gov/privacy/ccpa) - California Consumer Privacy Act
- [NIST Privacy Framework](https://www.nist.gov/privacy-framework)
- [ISO/IEC 27701](https://www.iso.org/standard/71670.html) - Privacy Information Management

---

**Disclaimer**: This document describes technical capabilities and design principles. It does not constitute legal advice. Users must ensure their implementations comply with applicable privacy laws. Consult qualified legal professionals for guidance.
