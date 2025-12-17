# Threat Model

## Scope

This document describes the threat model for ununseptium, identifying trust boundaries, threats, and mitigations.

### Non-Goals

- Infrastructure threat modeling (user responsibility)
- Physical security threats
- Social engineering threats

## Definitions

| Term | Definition |
|------|------------|
| Threat | Potential security violation |
| Trust Boundary | Interface between trusted and untrusted zones |
| Mitigation | Control to reduce threat risk |

See [Glossary](../glossary.md) for additional terminology.

## Trust Boundaries

```mermaid
graph TB
    subgraph "Untrusted"
        INPUT[External Input]
        NETWORK[Network]
    end

    subgraph "Semi-Trusted"
        DEPS[Dependencies]
        MODELS[Model Files]
    end

    subgraph "Trusted"
        CONFIG[Configuration]
        KEYS[Encryption Keys]
        CORE[Core Library]
    end

    INPUT -->|Boundary 1| CORE
    DEPS -->|Boundary 2| CORE
    MODELS -->|Boundary 3| CORE
    CONFIG -->|Protected| CORE
    KEYS -->|Protected| CORE

```text
### Boundary Definitions

| Boundary | Source | Assumption |
|----------|--------|------------|
| External Input | User data | Untrusted, validate all |
| Dependencies | PyPI packages | Semi-trusted, pin versions |
| Model Files | Downloaded models | Verify checksums |
| Configuration | Config files | Trusted, protect access |
| Keys | Encryption keys | Trusted, secure storage |

## Threat Analysis (STRIDE)

### Spoofing

| Threat | Scenario | Mitigation |
|--------|----------|------------|
| T1 | Impersonate legitimate user | RBAC, audit logging |
| T2 | Forge audit entries | Hash chain verification |
| T3 | Submit fake model | Checksum verification |

### Tampering

| Threat | Scenario | Mitigation |
|--------|----------|------------|
| T4 | Modify audit logs | Hash chain detection |
| T5 | Alter model weights | Checksum verification |
| T6 | Inject malicious code | Dependency pinning, scanning |

### Repudiation

| Threat | Scenario | Mitigation |
|--------|----------|------------|
| T7 | Deny performing action | Tamper-evident audit logs |
| T8 | Dispute verification result | Logged decisions with context |

### Information Disclosure

| Threat | Scenario | Mitigation |
|--------|----------|------------|
| T9 | PII exposure in logs | PII detection/masking |
| T10 | Key exposure | Secure key management |
| T11 | Model extraction | Access controls |

### Denial of Service

| Threat | Scenario | Mitigation |
|--------|----------|------------|
| T12 | Large input processing | Input validation, limits |
| T13 | Resource exhaustion | Timeouts, rate limiting |

### Elevation of Privilege

| Threat | Scenario | Mitigation |
|--------|----------|------------|
| T14 | Bypass access controls | RBAC enforcement |
| T15 | Execute arbitrary code | Input sanitization |

## Threat Matrix

| ID | Category | Severity | Likelihood | Risk |
|----|----------|----------|------------|------|
| T1 | Spoofing | High | Medium | High |
| T4 | Tampering | High | Low | Medium |
| T7 | Repudiation | Medium | Medium | Medium |
| T9 | Disclosure | High | Medium | High |
| T12 | DoS | Medium | Medium | Medium |
| T14 | Elevation | High | Low | Medium |

Risk calculation:

$$\text{Risk} = \text{Severity} \times \text{Likelihood}$$

## Attack Surface

### Input Vectors

| Vector | Description | Validation |
|--------|-------------|------------|
| Identity data | User-provided PII | Schema validation |
| Transaction data | Financial records | Type/range checks |
| File uploads | Documents | Type verification |
| CLI arguments | User commands | Sanitization |

### Dependency Surface

| Component | Risk | Mitigation |
|-----------|------|------------|
| PyPI packages | Supply chain | pip-audit, version pinning |
| System libraries | Vulnerabilities | Security advisories |
| Model files | Malicious models | Checksum verification |

## Security Controls

### Prevention

| Control | Threats Addressed |
|---------|-------------------|
| Input validation | T12, T15 |
| Schema enforcement | T12, T15 |
| RBAC | T1, T14 |
| Dependency pinning | T6 |

### Detection

| Control | Threats Addressed |
|---------|-------------------|
| Audit logging | T1, T7, T8 |
| Hash chain verification | T4 |
| Anomaly detection | T1, T14 |

### Response

| Control | Threats Addressed |
|---------|-------------------|
| Alert generation | All |
| Audit export | T7, T8 |

## Out of Scope

The following are explicitly out of scope for this library:

| Area | Reason | Responsibility |
|------|--------|----------------|
| Network security | Infrastructure | User |
| Physical security | Infrastructure | User |
| Personnel security | Organization | User |
| Incident response | Operations | User |
| Key storage | Infrastructure | User |

## Security Testing

| Test Type | Frequency | Tools |
|-----------|-----------|-------|
| SAST | Every PR | Bandit, CodeQL |
| Dependency scan | Daily | pip-audit |
| Secret scanning | Every PR | TruffleHog |

## Related Documentation

- [Security Overview](security-overview.md)
- [Auditability](auditability.md)
- [Crypto and Key Management](crypto-and-key-management.md)

## References

- [STRIDE Model](https://docs.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats)
- [OWASP Threat Modeling](https://owasp.org/www-community/Threat_Modeling)
- [Glossary](../glossary.md)
