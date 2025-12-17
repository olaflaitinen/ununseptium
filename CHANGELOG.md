# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Scope

This changelog documents user-facing changes to the ununseptium library.

### Document Conventions

| Prefix | Meaning |
|--------|---------|
| Added | New features |
| Changed | Changes in existing functionality |
| Deprecated | Soon-to-be removed features |
| Removed | Removed features |
| Fixed | Bug fixes |
| Security | Vulnerability fixes |

## [Unreleased]

No unreleased changes.

## [1.0.0] - 2025-12-17

### Added

- **Core Module**
  - Configuration management with Pydantic v2 settings
  - Structured logging with structlog integration
  - Type-safe error hierarchy
  - Core data schemas and types

- **KYC Module**
  - Identity verification framework
  - Document processing utilities
  - Sanctions screening interface
  - Entity resolution primitives
  - Politically Exposed Persons (PEP) screening

- **AML Module**
  - Transaction monitoring framework
  - Typology detection engine
  - Case management primitives
  - Regulatory reporting schemas
  - Alert prioritization

- **Security Module**
  - PII detection with configurable patterns
  - Data masking and tokenization
  - Encryption utilities (Fernet/AES with fallback)
  - Role-based access control (RBAC)
  - Tamper-evident audit logging with hash chains

- **MathStats Module**
  - Conformal prediction for uncertainty quantification
  - Extreme Value Theory (EVT) with GPD fitting
  - Hawkes process models for event clustering
  - Copula implementations for dependency modeling
  - Sequential detection algorithms (CUSUM, SPRT, ADWIN)
  - Graph feature extraction utilities

- **AI Module**
  - Feature engineering pipelines
  - Model ensemble framework
  - Explainability utilities (SHAP interface)
  - Model governance schemas (model cards)
  - Scientific ML primitives (PINN, Neural ODE interfaces)

- **Model Zoo**
  - Pretrained model catalog
  - Download with checksum verification
  - Model card validation

- **CLI**
  - `ununseptium info` - Display library information
  - `ununseptium doctor` - Run diagnostics
  - `ununseptium verify` - Identity verification
  - `ununseptium screen` - Sanctions screening
  - `ununseptium audit` - Audit log management

- **Plugin System**
  - Entry point based plugin discovery
  - Plugin lifecycle management

- **Documentation**
  - Comprehensive README with architecture diagrams
  - Complete API documentation
  - Security policy and threat model
  - Mathematical foundations with formulas
  - Contribution guidelines

### Security

- Implemented hash-chain audit logs for tamper detection
- Added PII detection and masking pipeline
- Implemented model checksum verification
- Added role-based access control framework

## References

- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)

---

[Unreleased]: <https://github.com/olaflaitinen/ununseptium/compare/v1.0.0...HEAD>
[1.0.0]: <https://github.com/olaflaitinen/ununseptium/releases/tag/v1.0.0>
