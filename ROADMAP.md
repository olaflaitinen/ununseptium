# Roadmap

## Scope

This document outlines the development roadmap for ununseptium, distinguishing between shipped features and planned improvements.

### Non-Goals

- Committing to specific release dates
- Guaranteeing future features

## Definitions

| Term | Definition |
|------|------------|
| Shipped | Features included in released versions |
| Planned | Features under consideration for future releases |
| RFC | Request for Comments - proposal for major features |

## Current Release: v1.0.0

Release Date: December 2025

### Shipped Features

The following features are included in v1.0.0:

#### Core Infrastructure

| Feature | Status | Module |
|---------|--------|--------|
| Pydantic v2 configuration | Shipped | `core` |
| Structured logging | Shipped | `core` |
| Type-safe error hierarchy | Shipped | `core` |
| Plugin system | Shipped | `plugins` |

#### KYC Module

| Feature | Status | Description |
|---------|--------|-------------|
| Identity verification | Shipped | Basic identity validation |
| Document processing | Shipped | Document type detection |
| Sanctions screening | Shipped | Watchlist matching |
| PEP screening | Shipped | Politically exposed persons |
| Entity resolution | Shipped | Name matching algorithms |

#### AML Module

| Feature | Status | Description |
|---------|--------|-------------|
| Transaction monitoring | Shipped | Transaction analysis |
| Typology detection | Shipped | Pattern recognition |
| Case management | Shipped | Alert handling primitives |
| Alert prioritization | Shipped | Risk-based ranking |

#### Security Module

| Feature | Status | Description |
|---------|--------|-------------|
| PII detection | Shipped | Pattern-based detection |
| Data masking | Shipped | Tokenization, redaction |
| Encryption | Shipped | Fernet/AES with fallback |
| RBAC | Shipped | Role-based access control |
| Audit logging | Shipped | Hash-chain logs |

#### MathStats Module

| Feature | Status | Description |
|---------|--------|-------------|
| Conformal prediction | Shipped | Coverage-guaranteed sets |
| EVT (GPD) | Shipped | Tail risk estimation |
| Hawkes processes | Shipped | Event clustering |
| Copulas | Shipped | Dependency modeling |
| Sequential detection | Shipped | CUSUM, SPRT, ADWIN |
| Graph features | Shipped | Network statistics |

#### AI Module

| Feature | Status | Description |
|---------|--------|-------------|
| Feature engineering | Shipped | Pipeline primitives |
| Model ensembles | Shipped | Ensemble framework |
| Explainability | Shipped | SHAP interface |
| Model governance | Shipped | Model card schema |

#### Model Zoo

| Feature | Status | Description |
|---------|--------|-------------|
| Model catalog | Shipped | Pretrained model index |
| Download/verify | Shipped | Checksum verification |
| Model cards | Shipped | Documentation schema |

#### CLI

| Feature | Status | Description |
|---------|--------|-------------|
| `info` command | Shipped | Library information |
| `doctor` command | Shipped | Diagnostics |
| `verify` command | Shipped | Identity verification |
| `screen` command | Shipped | Sanctions screening |
| `audit` command | Shipped | Audit log management |

---

## Future Development

```mermaid
gantt
    title Ununseptium Roadmap
    dateFormat  YYYY-MM
    section v1.1.x
    Enhanced screening    :2026-01, 2026-03
    Batch processing      :2026-02, 2026-04
    Performance tuning    :2026-03, 2026-05
    section v1.2.x
    Graph neural networks :2026-04, 2026-07
    Real-time streaming   :2026-05, 2026-08
    section v2.0.x
    API redesign          :2026-09, 2026-12

```text
### Post-1.0.x Considerations

The following features are under consideration for future releases. Inclusion is not guaranteed.

#### v1.1.x (Minor Enhancements)

| Feature | Priority | Description |
|---------|----------|-------------|
| Enhanced PII patterns | High | Additional detection patterns |
| Batch processing APIs | High | Bulk verification/screening |
| Performance optimizations | High | Numba JIT acceleration |
| Additional typologies | Medium | More AML patterns |
| Extended audit export | Medium | Additional export formats |

#### v1.2.x (Feature Additions)

| Feature | Priority | Description |
|---------|----------|-------------|
| Graph neural networks | Medium | GNN-based risk models |
| Real-time streaming | Medium | Stream processing support |
| Document OCR integration | Medium | Document image processing |
| Multi-language PII | Medium | Non-English PII detection |
| Federated learning | Low | Privacy-preserving training |

#### v2.0.x (Major Release)

| Feature | Priority | Description |
|---------|----------|-------------|
| Async-first APIs | High | Full async/await support |
| Plugin API v2 | Medium | Enhanced plugin capabilities |
| Configuration DSL | Medium | Domain-specific configuration |

### Not Planned

The following are explicitly NOT planned:

| Feature | Reason |
|---------|--------|
| Database integration | Out of scope; use your own |
| REST API server | Out of scope; wrap as needed |
| UI/Dashboard | Out of scope; build your own |
| Hosted service | Not applicable to library |

## Contributing to Roadmap

### Proposing Features

1. Open a [Discussion](https://github.com/olaflaitinen/ununseptium/discussions) with your idea
2. Gather community feedback
3. If warranted, create an RFC issue
4. Follow [GOVERNANCE.md](GOVERNANCE.md) decision process

### Prioritization Factors

| Factor | Weight |
|--------|--------|
| User demand | High |
| Maintainer capacity | High |
| Technical feasibility | Medium |
| Scope alignment | High |
| Community contribution | Medium |

## Version Policy

Ununseptium follows [Semantic Versioning](https://semver.org/):

$$\text{Version} = \text{MAJOR}.\text{MINOR}.\text{PATCH}$$

| Version | Changes | Breaking |
|---------|---------|----------|
| PATCH | Bug fixes | No |
| MINOR | New features | No |
| MAJOR | Any changes | Possibly |

## Disclaimer

> This roadmap represents current thinking and is subject to change. Features listed as "planned" or "under consideration" are not commitments. Development priorities may shift based on community feedback, maintainer capacity, and technical constraints.

## References

- [Semantic Versioning](https://semver.org/)
- [GOVERNANCE.md](GOVERNANCE.md)
- [CHANGELOG.md](CHANGELOG.md)
