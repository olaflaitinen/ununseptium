# Ununseptium

**State-of-the-Art RegTech and Cybersecurity Python Library**

[![CI](https://github.com/olaflaitinen/ununseptium/actions/workflows/ci.yml/badge.svg)](https://github.com/olaflaitinen/ununseptium/actions/workflows/ci.yml)
[![Docs Quality](https://github.com/olaflaitinen/ununseptium/actions/workflows/docs-quality.yml/badge.svg)](https://github.com/olaflaitinen/ununseptium/actions/workflows/docs-quality.yml)
[![Security](https://github.com/olaflaitinen/ununseptium/actions/workflows/security.yml/badge.svg)](https://github.com/olaflaitinen/ununseptium/actions/workflows/security.yml)
[![Build](https://github.com/olaflaitinen/ununseptium/actions/workflows/build.yml/badge.svg)](https://github.com/olaflaitinen/ununseptium/actions/workflows/build.yml)
[![Release](https://github.com/olaflaitinen/ununseptium/actions/workflows/release.yml/badge.svg)](https://github.com/olaflaitinen/ununseptium/actions/workflows/release.yml)
[![Publish](https://github.com/olaflaitinen/ununseptium/actions/workflows/publish.yml/badge.svg)](https://github.com/olaflaitinen/ununseptium/actions/workflows/publish.yml)
[![CodeQL](https://github.com/olaflaitinen/ununseptium/actions/workflows/codeql.yml/badge.svg)](https://github.com/olaflaitinen/ununseptium/actions/workflows/codeql.yml)
[![Scorecard](https://github.com/olaflaitinen/ununseptium/actions/workflows/scorecard.yml/badge.svg)](https://github.com/olaflaitinen/ununseptium/actions/workflows/scorecard.yml)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/olaflaitinen/ununseptium/blob/main/LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/ununseptium)](https://pypi.org/project/ununseptium/)
[![Python versions](https://img.shields.io/pypi/pyversions/ununseptium)](https://pypi.org/project/ununseptium/)
[![Coverage](https://img.shields.io/codecov/c/github/olaflaitinen/ununseptium)](https://codecov.io/gh/olaflaitinen/ununseptium)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Checked with pyright](https://img.shields.io/badge/pyright-checked-blue)](https://github.com/microsoft/pyright)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/olaflaitinen/ununseptium/pulls)
[![Issues](https://img.shields.io/github/issues/olaflaitinen/ununseptium)](https://github.com/olaflaitinen/ununseptium/issues)
[![Last Commit](https://img.shields.io/github/last-commit/olaflaitinen/ununseptium)](https://github.com/olaflaitinen/ununseptium/commits/main)
[![Commit Activity](https://img.shields.io/github/commit-activity/m/olaflaitinen/ununseptium)](https://github.com/olaflaitinen/ununseptium/pulse)
[![Downloads](https://img.shields.io/pypi/dm/ununseptium)](https://pypi.org/project/ununseptium/)
[![SLSA 3](https://slsa.dev/images/gh-badge-level3.svg)](https://slsa.dev)

---

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Security Posture](#security-posture)
- [Auditability](#auditability)
- [Mathematical Foundations](#mathematical-foundations)
- [Model Zoo](#model-zoo)
- [CLI Reference](#cli-reference)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Overview

Ununseptium is an enterprise-grade Python library providing comprehensive tooling for:

| Domain | Capabilities |
|--------|--------------|
| **KYC Automation** | Identity verification, document processing, sanctions screening, entity resolution |
| **AML Monitoring** | Transaction analysis, typology detection, case management, regulatory reporting |
| **Data Security** | PII detection/masking, encryption, access control, tamper-evident audit logs |
| **AI Risk Engine** | Feature engineering, ensemble models, explainability, model governance |
| **Scientific ML** | Physics-Informed Neural Networks, Neural ODEs, Neural Operators |
| **Math/Stats** | Conformal prediction, EVT, Hawkes processes, copulas, graph statistics |

### Scope

Ununseptium provides computational primitives and frameworks for building compliance systems. It is designed for:

- Financial institutions implementing AML/KYC programs
- RegTech vendors building compliance platforms
- Research teams developing risk quantification methods
- Auditors requiring tamper-evident data trails

### Non-Goals

- Ununseptium is NOT a turnkey compliance solution
- It does NOT provide legal advice or regulatory interpretation
- It does NOT replace human judgment in compliance decisions
- It is NOT a database or case management system (integrate with your own)

---

## Installation

### Requirements

- Python 3.11 or higher
- NumPy, SciPy, Pydantic v2

### From PyPI

```bash
pip install ununseptium

```text
### From Source

```bash
git clone <https://github.com/olaflaitinen/ununseptium.git>
cd ununseptium
pip install -e ".[dev]"

```text
### Optional Dependencies

```bash
# Cryptography extras
pip install ununseptium[crypto]

# Full ML stack
pip install ununseptium[ml]

# All optional dependencies
pip install ununseptium[all]

```text
---

## Quick Start

### Identity Verification

```python
from ununseptium.kyc import Identity, IdentityVerifier

identity = Identity(
    full_name="John Doe",
    date_of_birth="1985-03-15",
    nationality="US",
    document_number="AB123456",
)

verifier = IdentityVerifier()
result = verifier.verify(identity)

print(f"Status: {result.status}")
print(f"Risk Level: {result.risk_level}")
print(f"Reason Codes: {result.reason_codes}")

```text
### Transaction Monitoring

```python
from ununseptium.aml import Transaction, TypologyDetector

transactions = [
    Transaction(sender="ACC001", receiver="ACC002", amount=9500),
    Transaction(sender="ACC001", receiver="ACC003", amount=9600),
    Transaction(sender="ACC001", receiver="ACC004", amount=9400),
]

detector = TypologyDetector()
alerts = detector.detect(transactions)

for alert in alerts:
    print(f"Typology: {alert.typology_type}, Score: {alert.score}")

```text
### Tamper-Evident Audit

```python
from ununseptium.security import AuditLog

log = AuditLog()

log.append({"action": "identity_verified", "identity_id": "ID-001"})
log.append({"action": "risk_assessed", "score": 0.72})

# Verify integrity
assert log.verify() is True

# Save with hash chain
log.save("audit.log")

```text
---

## Architecture

```mermaid
graph TB
    subgraph "Public API"
        CLI[CLI Interface]
        SDK[Python SDK]
    end

    subgraph "Domain Modules"
        KYC[KYC Module]
        AML[AML Module]
        SEC[Security Module]
    end

    subgraph "Intelligence Layer"
        AI[AI Module]
        MATH[MathStats Module]
        ZOO[Model Zoo]
    end

    subgraph "Infrastructure"
        CORE[Core Module]
        PLUG[Plugin System]
    end

    CLI --> KYC
    CLI --> AML
    SDK --> KYC
    SDK --> AML
    SDK --> SEC

    KYC --> AI
    AML --> AI
    AML --> MATH

    AI --> ZOO
    AI --> CORE
    MATH --> CORE

    SEC --> CORE
    PLUG --> CORE

```text
### Module Summary

| Module | Purpose | Key Components |
|--------|---------|----------------|
| `core` | Foundation | Configuration, errors, logging, schemas |
| `kyc` | Identity | Verification, documents, screening, entity resolution |
| `aml` | Transactions | Monitoring, typologies, cases, reporting |
| `security` | Protection | PII, crypto, access control, audit logs |
| `mathstats` | Statistics | Conformal, EVT, Hawkes, copulas, graphs |
| `ai` | Intelligence | Features, models, explainability, governance |
| `model_zoo` | Pretrained | Catalog, download, verification |
| `cli` | Interface | Commands for all operations |
| `plugins` | Extensibility | Plugin discovery and loading |

See [docs/architecture/overview.md](docs/architecture/overview.md) for detailed architecture documentation.

---

## Security Posture

Ununseptium implements defense-in-depth security:

### Data Protection

| Layer | Mechanism | Implementation |
|-------|-----------|----------------|
| Detection | PII Scanner | Regex patterns with configurable rules |
| Masking | Tokenization | Replace PII with reversible tokens |
| Encryption | Fernet/AES | Symmetric encryption with key rotation |
| Access | RBAC | Role-based permission enforcement |

### Integrity Assurance

The audit subsystem uses cryptographic hash chains:

$$H_n = \text{SHA256}(H_{n-1} \| \text{entry}_n)$$

Where each entry is linked to its predecessor, making tampering detectable.

### Threat Model

| Threat | Mitigation |
|--------|------------|
| PII Exposure | Detection + masking pipeline |
| Unauthorized Access | RBAC with audit logging |
| Data Tampering | Hash-chain verification |
| Model Manipulation | Checksums + provenance tracking |

See [docs/security/security-overview.md](docs/security/security-overview.md) for the complete threat model.

---

## Auditability

Every operation in ununseptium can be traced through the audit subsystem:

```python
from ununseptium.security import AuditLog, AuditVerifier

# Create verifiable audit trail
log = AuditLog()
log.append({"action": "screening_completed", "matches": 0})

# Later: verify integrity
verifier = AuditVerifier()
result = verifier.verify_file("audit.log")

if not result.is_valid:
    raise SecurityError(f"Tamper detected at entry {result.failed_index}")

```text
### Audit Entry Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique entry identifier |
| `timestamp` | ISO-8601 | Entry creation time |
| `action` | string | Action performed |
| `actor` | string | Who performed the action |
| `resource` | string | Affected resource |
| `prev_hash` | string | Hash of previous entry |
| `entry_hash` | string | Hash of this entry |

---

## Mathematical Foundations

Ununseptium provides statistically rigorous methods:

### Conformal Prediction

Coverage-guaranteed prediction sets:

$$P(Y \in C(X)) \geq 1 - \alpha$$

```python
from ununseptium.mathstats import ConformalPredictor

predictor = ConformalPredictor(alpha=0.1)
predictor.calibrate(y_cal, y_pred_cal)

pred_set = predictor.predict(y_new)
print(f"Interval: [{pred_set.lower}, {pred_set.upper}]")

```text
### Extreme Value Theory

Tail risk via Generalized Pareto Distribution:

$$F(x) = 1 - \left(1 + \xi \frac{x}{\sigma}\right)^{-1/\xi}$$

### Sequential Detection

Real-time change detection with CUSUM, SPRT, and ADWIN algorithms.

See [docs/mathstats/mathstats-overview.md](docs/mathstats/mathstats-overview.md) for complete mathematical documentation.

---

## Model Zoo

Pretrained models for common AML/KYC tasks:

| Model ID | Domain | Architecture | AUC-ROC |
|----------|--------|--------------|---------|
| `aml-transaction-risk-v1` | AML | Gradient Boosting | 0.92 |
| `anomaly-detector-v1` | Anomaly | Ensemble | 0.88 |
| `entity-resolution-v1` | KYC | Neural Network | 0.91 |
| `sar-priority-v1` | AML | Transformer | 0.87 |
| `graph-risk-v1` | AML | GNN | 0.90 |

```python
from ununseptium.model_zoo import PretrainedModel

model = PretrainedModel.load("aml-transaction-risk-v1")
result = model.predict(features)

```text
See [docs/model-zoo/model-zoo.md](docs/model-zoo/model-zoo.md) for the complete model catalog.

---

## CLI Reference

```bash
# Display library information
ununseptium info

# Run diagnostics
ununseptium doctor

# Verify identity from JSON
ununseptium verify identity data.json --output result.json

# Screen a name
ununseptium screen name "John Doe" --threshold 0.8

# Verify audit log integrity
ununseptium audit verify audit.log

# Show audit entries
ununseptium audit show audit.log --limit 20

# Validate model card
ununseptium model validate model_card.json

```text
---

## Documentation

Comprehensive documentation is available in the [docs/](docs/) directory:

- [Architecture Overview](docs/architecture/overview.md)
- [KYC Module](docs/kyc/kyc-overview.md)
- [AML Module](docs/aml/aml-overview.md)
- [Security Guide](docs/security/security-overview.md)
- [Mathematical Methods](docs/mathstats/mathstats-overview.md)
- [AI and ML](docs/ai/ai-overview.md)
- [Model Zoo](docs/model-zoo/model-zoo.md)
- [FAQ](docs/faq.md)
- [Glossary](docs/glossary.md)

---

## Contributing

We welcome contributions. Please read [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Development setup
- Code style guidelines
- Testing requirements
- Pull request process

---

## License

Ununseptium is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.

---

## Citation

If you use ununseptium in academic work, please cite:

```bibtex
@software{ununseptium2025,
  author = {Laitinen, Olaf},
  title = {Ununseptium: RegTech and Cybersecurity Library},
  year = {2025},
  url = {<https://github.com/olaflaitinen/ununseptium>},
  version = {1.0.0}
}

```text
See [CITATION.md](CITATION.md) for additional citation formats.

---

## Support

- [GitHub Issues](https://github.com/olaflaitinen/ununseptium/issues) for bug reports
- [GitHub Discussions](https://github.com/olaflaitinen/ununseptium/discussions) for questions
- See [SUPPORT.md](SUPPORT.md) for additional resources

---

**Disclaimer**: Ununseptium provides computational tools only. It does not constitute legal, compliance, or regulatory advice. Users are responsible for ensuring their implementations meet applicable regulatory requirements. Consult qualified legal and compliance professionals for guidance.
