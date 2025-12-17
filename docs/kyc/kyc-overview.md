# KYC Overview

## Scope

This document describes the Know Your Customer (KYC) module in ununseptium, providing identity verification, document processing, and screening capabilities.

### Non-Goals

- Regulatory compliance certification
- Legal identity verification requirements
- Document OCR implementation (integrate your own)

## Definitions

| Term | Definition |
|------|------------|
| CDD | Customer Due Diligence - identity verification and risk assessment |
| EDD | Enhanced Due Diligence - additional checks for high-risk customers |
| PEP | Politically Exposed Person - individual in prominent public position |
| Watchlist | List of sanctioned entities or persons |

See [Glossary](../glossary.md) for additional terminology.

## Module Structure

```mermaid
graph TB
    subgraph "KYC Module"
        IDENTITY[Identity]
        VERIFIER[IdentityVerifier]
        DOCUMENTS[Documents]
        SCREENER[Screener]
        ENTITY[EntityResolver]
    end

    subgraph "Dependencies"
        AI[ai module]
        CORE[core module]
    end

    IDENTITY --> VERIFIER
    VERIFIER --> AI
    VERIFIER --> CORE
    DOCUMENTS --> VERIFIER
    SCREENER --> CORE
    ENTITY --> AI

```text
## Components

### Identity

Core identity data model:

```python
from ununseptium.kyc import Identity

identity = Identity(
    full_name="John Doe",
    date_of_birth="1985-03-15",
    nationality="US",
    document_type="passport",
    document_number="AB123456",
    document_expiry="2030-01-01",
)

```text
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `full_name` | str | Yes | Full legal name |
| `date_of_birth` | date | Yes | Date of birth |
| `nationality` | str | Yes | ISO country code |
| `document_type` | str | No | Document type |
| `document_number` | str | No | Document ID |
| `document_expiry` | date | No | Expiry date |

### Identity Verifier

Verification engine:

```python
from ununseptium.kyc import Identity, IdentityVerifier

verifier = IdentityVerifier()
result = verifier.verify(identity)

print(f"Status: {result.status}")
print(f"Risk Level: {result.risk_level}")
print(f"Reason Codes: {result.reason_codes}")

```text
#### Verification Result

| Field | Type | Description |
|-------|------|-------------|
| `status` | str | approved, pending, rejected |
| `passed` | bool | Overall pass/fail |
| `risk_level` | str | low, medium, high |
| `reason_codes` | list | Flags raised |
| `score` | float | Risk score 0-1 |

#### Verification Checks

| Check | Description | Outcome |
|-------|-------------|---------|
| Schema validation | Required fields present | Pass/Fail |
| Format validation | Field formats correct | Pass/Fail |
| Age verification | Minimum age check | Pass/Fail |
| Document expiry | Not expired | Pass/Fail |
| Screening | Watchlist check | Pass/Fail/Review |

### Document Processing

Document handling utilities:

```python
from ununseptium.kyc import Document, DocumentProcessor

doc = Document(
    type="passport",
    country="US",
    data=extracted_fields,  # From your OCR
)

processor = DocumentProcessor()
result = processor.validate(doc)

```text
| Document Type | Supported Checks |
|---------------|------------------|
| Passport | MRZ validation, expiry |
| ID Card | Format, expiry |
| Driver License | Format, expiry |
| Utility Bill | Recency |

### Screening

Watchlist and PEP screening:

```python
from ununseptium.kyc import Screener

screener = Screener()

# Name screening
result = screener.screen_name("John Doe", threshold=0.8)

for match in result.matches:
    print(f"Match: {match.name}")
    print(f"Score: {match.score}")
    print(f"Source: {match.source}")

```text
#### Screening Sources

| Source | Type | Description |
|--------|------|-------------|
| Sanctions | Watchlist | OFAC, EU, UN lists |
| PEP | Watchlist | Politically exposed persons |
| Adverse Media | Intelligence | Negative news |
| Custom | User-defined | Your lists |

#### Match Scoring

Fuzzy matching score calculation:

$$\text{Score} = \frac{\text{Levenshtein Similarity} + \text{Phonetic Similarity}}{2}$$

| Score Range | Interpretation |
|-------------|----------------|
| 0.95 - 1.0 | Exact match |
| 0.85 - 0.95 | Strong match |
| 0.70 - 0.85 | Potential match |
| < 0.70 | Weak match |

### Entity Resolution

Entity matching for deduplication:

```python
from ununseptium.kyc import EntityResolver

resolver = EntityResolver()

# Find matching entities
matches = resolver.resolve(identity, candidates)

for match in matches:
    print(f"Candidate: {match.entity_id}")
    print(f"Confidence: {match.confidence}")

```text
| Algorithm | Use Case |
|-----------|----------|
| Exact | Known identifiers |
| Fuzzy Name | Name variations |
| Address | Location matching |
| ML-based | Complex matching |

## Verification Pipeline

```mermaid
graph TB
    INPUT[Identity Input] --> VALIDATE[Schema Validation]
    VALIDATE --> FORMAT[Format Validation]
    FORMAT --> DOC[Document Checks]
    DOC --> SCREEN[Screening]
    SCREEN --> RISK[Risk Assessment]
    RISK --> DECISION{Decision}
    DECISION -->|Pass| APPROVED[Approved]
    DECISION -->|Review| PENDING[Pending Review]
    DECISION -->|Fail| REJECTED[Rejected]

    SCREEN --> AUDIT[Audit Log]
    DECISION --> AUDIT

```text
## Configuration

```python
from ununseptium.kyc import KYCConfig

config = KYCConfig(
    verification_threshold=0.7,
    screening_threshold=0.8,
    minimum_age=18,
    require_document=True,
    screening_sources=["sanctions", "pep"],
)

verifier = IdentityVerifier(config=config)

```text
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `verification_threshold` | float | 0.7 | Pass threshold |
| `screening_threshold` | float | 0.8 | Match threshold |
| `minimum_age` | int | 18 | Age requirement |
| `require_document` | bool | True | Document required |
| `screening_sources` | list | All | Sources to check |

## Risk Scoring

Risk score formula:

$$\text{Risk} = \sum_{i} w_i \cdot r_i$$

Where:
- $w_i$ are configurable weights
- $r_i$ are individual risk factors

| Factor | Weight | Description |
|--------|--------|-------------|
| Screening matches | 0.4 | Watchlist hits |
| Document issues | 0.2 | Document problems |
| High-risk country | 0.2 | Country risk |
| Velocity | 0.1 | Rapid activity |
| Other flags | 0.1 | Misc flags |

## CLI Commands

```bash
# Verify identity from JSON file
ununseptium verify identity data.json --output result.json

# Screen a name
ununseptium screen name "John Doe" --threshold 0.8

# Screen with specific sources
ununseptium screen name "John Doe" --sources sanctions,pep

```text
## Related Documentation

- [AML Overview](../aml/aml-overview.md)
- [Security Overview](../security/security-overview.md)
- [AI Overview](../ai/ai-overview.md)

## References

- [FATF Recommendations](https://www.fatf-gafi.org/recommendations.html)
- [NIST SP 800-63](https://pages.nist.gov/800-63-3/)
- [Glossary](../glossary.md)
