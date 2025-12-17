# Security Policy

## Scope

This security policy covers the ununseptium Python library and its official distribution channels.

### In Scope

- Core library code (`src/ununseptium/`)
- Official PyPI distribution
- GitHub repository and releases
- Documentation that affects security understanding

### Out of Scope

- Third-party integrations
- User implementations built on ununseptium
- Infrastructure where ununseptium is deployed

## Supported Versions

| Version | Supported | Notes |
|---------|-----------|-------|
| 1.0.x   | Yes       | Current stable release |
| < 1.0   | No        | Pre-release versions |

Security updates are provided for the latest minor version only. Users should upgrade to receive security fixes.

## Reporting a Vulnerability

### Disclosure Process

We follow coordinated disclosure. Please do NOT open public issues for security vulnerabilities.

**Report via:** <security@ununseptium.dev> (or create a private security advisory on GitHub)

### Required Information

Please include:

1. **Description**: Clear explanation of the vulnerability
2. **Impact**: What an attacker could achieve
3. **Reproduction**: Steps to reproduce (minimal example preferred)
4. **Environment**: Python version, OS, ununseptium version
5. **Suggested Fix**: If you have one (optional)

### Response Timeline

| Stage | Timeline |
|-------|----------|
| Acknowledgment | 48 hours |
| Initial Assessment | 7 days |
| Fix Development | 30 days (critical: 7 days) |
| Public Disclosure | After fix is released |

### Severity Classification

| Severity | Criteria | Response |
|----------|----------|----------|
| Critical | Remote code execution, authentication bypass | 7-day fix |
| High | Data exposure, privilege escalation | 14-day fix |
| Medium | Information disclosure, DoS | 30-day fix |
| Low | Minor issues, hardening | Next release |

## Security Considerations

### Threat Model

Ununseptium operates under these assumptions:

| Trust Boundary | Assumption |
|----------------|------------|
| Input Data | Untrusted; validate all inputs |
| Configuration | Trusted; protect config files |
| Dependencies | Semi-trusted; pin versions |
| Model Files | Verify checksums before loading |

### Known Limitations

1. **Encryption**: The fallback XOR encryption (when cryptography is unavailable) is NOT cryptographically secure. Install the `cryptography` package for production use.

2. **PII Detection**: Pattern-based detection may have false negatives. Do not rely solely on automated detection for compliance.

3. **Audit Logs**: While tamper-evident, audit logs require secure storage. The hash chain detects tampering but does not prevent it.

### Security Best Practices

```python
# Always verify audit log integrity
from ununseptium.security import AuditLog

log = AuditLog.load("audit.log")
if not log.verify():
    raise SecurityError("Audit log tampering detected")

# Use proper encryption
from ununseptium.security import Encryptor

encryptor = Encryptor()
encryptor.generate_key()  # Requires cryptography package
encrypted = encryptor.encrypt(sensitive_data)

```

## Security Updates

Security advisories are published via:

- GitHub Security Advisories
- Release notes in CHANGELOG.md
- PyPI release metadata

## Acknowledgments

We appreciate responsible disclosure. Reporters of valid vulnerabilities will be acknowledged (unless anonymity is requested) in:

- Security advisory
- CHANGELOG.md
- Project documentation

---

**Disclaimer**: This security policy describes our current practices. It does not constitute a warranty or guarantee. Users are responsible for their own security assessments.
