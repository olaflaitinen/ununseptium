# Architecture Overview

## Scope

This document describes the overall architecture of the ununseptium library, including module organization, dependencies, and design principles.

### Non-Goals

- Implementation details of individual components (see module-specific docs)
- Deployment architecture (user responsibility)
- Infrastructure design (user responsibility)

## Definitions

| Term | Definition |
|------|------------|
| Module | Python package providing domain functionality |
| Plugin | Dynamically loaded extension |
| Pipeline | Sequence of processing steps |

See [Glossary](../glossary.md) for additional terminology.

## Design Principles

| Principle | Implementation |
|-----------|----------------|
| Modularity | Independent, focused modules |
| Type Safety | Full type hints, strict checking |
| Configurability | Pydantic-based configuration |
| Extensibility | Plugin architecture |
| Auditability | Comprehensive logging and audit trails |
| Testability | Designed for property-based testing |

## Module Hierarchy

```mermaid
graph TB
    subgraph "Public API"
        CLI[cli]
        SDK[Python SDK]
    end

    subgraph "Domain Modules"
        KYC[kyc]
        AML[aml]
        SEC[security]
    end

    subgraph "Intelligence Layer"
        AI[ai]
        MATH[mathstats]
        ZOO[model_zoo]
    end

    subgraph "Foundation"
        CORE[core]
        PLUG[plugins]
    end

    CLI --> KYC
    CLI --> AML
    CLI --> SEC
    SDK --> KYC
    SDK --> AML
    SDK --> SEC

    KYC --> AI
    KYC --> CORE
    AML --> AI
    AML --> MATH
    AML --> CORE
    SEC --> CORE

    AI --> ZOO
    AI --> CORE
    MATH --> CORE

    PLUG --> CORE

```text
## Module Descriptions

| Module | Purpose | Key Components |
|--------|---------|----------------|
| `core` | Foundation services | Config, errors, logging, schemas |
| `kyc` | Identity verification | Verification, documents, screening |
| `aml` | Transaction monitoring | Monitoring, typologies, cases |
| `security` | Data protection | PII, crypto, audit, RBAC |
| `mathstats` | Statistical methods | Conformal, EVT, Hawkes, copulas |
| `ai` | Machine learning | Features, models, explainability |
| `model_zoo` | Pretrained models | Catalog, download, verification |
| `cli` | Command interface | All user-facing commands |
| `plugins` | Extensibility | Discovery, loading, lifecycle |

## Dependency Graph

```mermaid
graph LR
    subgraph External
        PYDANTIC[pydantic]
        NUMPY[numpy]
        SCIPY[scipy]
        HTTPX[httpx]
    end

    subgraph Core
        CORE[core]
    end

    subgraph Optional
        CRYPTO[cryptography]
        TORCH[torch]
        NETWORKX[networkx]
    end

    CORE --> PYDANTIC
    CORE --> NUMPY
    CORE --> SCIPY
    CORE --> HTTPX

    SEC[security] --> CRYPTO
    AI[ai] --> TORCH
    MATH[mathstats] --> NETWORKX

```text
### Dependency Layers

| Layer | Dependencies | Optional |
|-------|--------------|----------|
| Core | pydantic, numpy, scipy | No |
| Security | cryptography | Yes (fallback available) |
| AI | torch, jax | Yes |
| Graph | networkx, torch-geometric | Yes |
| Performance | numba | Yes |

## Package Structure

```text
src/ununseptium/
    __init__.py          # Package root
    py.typed             # PEP 561 marker
    core/                # Foundation
        __init__.py
        config.py        # Configuration
        errors.py        # Error types
        logging.py       # Structured logging
        schemas.py       # Base schemas
    kyc/                 # Identity
        __init__.py
        identity.py      # Identity types
        verification.py  # Verifier
        documents.py     # Documents
        screening.py     # Watchlists
        entity_resolution.py
    aml/                 # Transactions
        __init__.py
        transaction.py   # Transaction types
        monitoring.py    # Monitor
        typology.py      # Detection
        case.py          # Case management
        reporting.py     # Reports
    security/            # Protection
        __init__.py
        pii.py           # PII detection
        masking.py       # Data masking
        encryption.py    # Crypto
        access.py        # RBAC
        audit.py         # Audit logs
    mathstats/           # Statistics
        __init__.py
        conformal.py     # Conformal prediction
        evt.py           # Extreme values
        hawkes.py        # Point processes
        copula.py        # Copulas
        sequential.py    # Change detection
        graph.py         # Graph stats
    ai/                  # Intelligence
        __init__.py
        features.py      # Feature eng
        models.py        # Model framework
        explainability.py # SHAP etc
        governance.py    # Model cards
        sciml/           # Scientific ML
    model_zoo/           # Pretrained
        __init__.py
        catalog.py       # Model index
        download.py      # Downloader
        verify.py        # Checksums
    cli/                 # Commands
        __init__.py
        main.py          # CLI entry
    plugins/             # Extensions
        __init__.py
        discovery.py     # Plugin loading
        base.py          # Plugin base

```text
## Key Abstractions

### Configuration

Configuration uses Pydantic Settings:

```python
from ununseptium.core import Config

config = Config()
config.kyc.verification_threshold = 0.8

```text
### Error Handling

Hierarchical exceptions:

$$\text{UnunseptiumError} \supset \text{DomainError} \supset \text{SpecificError}$$

| Base Error | Domain Errors |
|------------|---------------|
| `UnunseptiumError` | All library errors |
| `ValidationError` | Input validation failures |
| `ConfigurationError` | Configuration issues |
| `SecurityError` | Security violations |

### Schemas

Pydantic models for type safety:

```python
from ununseptium.core.schemas import BaseSchema

class Identity(BaseSchema):
    full_name: str
    date_of_birth: date

```text
## Cross-Cutting Concerns

| Concern | Implementation |
|---------|----------------|
| Logging | structlog integration |
| Metrics | Optional prometheus export |
| Tracing | Optional OpenTelemetry |
| Configuration | Environment + file + code |

## Related Documentation

- [Data Flow](data-flow.md)
- [Plugin Architecture](plugin-architecture.md)
- [AI Pipeline](ai-pipeline.md)

## References

- [README](../../README.md)
- [Glossary](../glossary.md)
- [Python Packaging](https://packaging.python.org/)
