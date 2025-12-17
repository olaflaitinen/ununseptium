# Compliance

## Scope

This document describes how ununseptium supports compliance activities. It covers audit outputs, evidence generation, and regulatory alignment.

### Non-Goals

- Providing compliance certification
- Replacing compliance professionals
- Covering all jurisdictions

## Definitions

| Term | Definition |
|------|------------|
| CDD | Customer Due Diligence - verifying customer identity and risk |
| EDD | Enhanced Due Diligence - additional measures for high-risk customers |
| SAR | Suspicious Activity Report - mandatory regulatory filing |
| RBA | Risk-Based Approach - allocating resources based on risk level |
| AML | Anti-Money Laundering - preventing money laundering activities |
| CFT | Combating Financing of Terrorism - preventing terrorist financing |

## Important Notice

> **Not Legal Advice**: This document describes technical capabilities that may support compliance activities. It does not constitute legal advice, compliance certification, or guarantee of regulatory acceptance. Users must conduct their own compliance assessments with qualified professionals.

## Regulatory Framework Alignment

Ununseptium is designed with awareness of major regulatory frameworks. The library does NOT claim compliance certification but provides tooling aligned with these standards.

### FATF Recommendations

| FATF Principle | Library Support |
|----------------|-----------------|
| Risk-Based Approach | Configurable risk scoring, threshold adjustment |
| Customer Due Diligence | Identity verification, document processing |
| Enhanced Due Diligence | PEP screening, high-risk indicators |
| Record Keeping | Tamper-evident audit logs |
| Suspicious Transaction Reporting | Alert generation, case prioritization |

Reference: [FATF Recommendations](https://www.fatf-gafi.org/recommendations.html)

### Supported CDD/KYC Processes

```mermaid
graph TB
    subgraph "Customer Onboarding"
        ID[Identity Collection]
        VER[Verification]
        SCREEN[Screening]
        RISK[Risk Assessment]
    end

    subgraph "Ununseptium Support"
        ID_MOD[kyc.Identity]
        VER_MOD[kyc.IdentityVerifier]
        SCREEN_MOD[kyc.Screener]
        RISK_MOD[ai.RiskModel]
    end

    ID --> ID_MOD
    VER --> VER_MOD
    SCREEN --> SCREEN_MOD
    RISK --> RISK_MOD

```text
## Audit Evidence

### Audit Log Structure

The `security.audit` module generates tamper-evident logs:

$$H_n = \text{SHA256}(H_{n-1} \| \text{entry}_n)$$

Each audit entry contains:

| Field | Description | Evidence Value |
|-------|-------------|----------------|
| `timestamp` | ISO-8601 time | Establishes timeline |
| `action` | Operation performed | Documents decisions |
| `actor` | Who performed action | Attribution |
| `resource` | Affected entity | Scope of action |
| `details` | Action parameters | Context |
| `prev_hash` | Previous entry hash | Integrity chain |
| `entry_hash` | This entry hash | Tamper detection |

### Evidence Export

```python
from ununseptium.security import AuditLog

log = AuditLog.load("audit.log")

# Verify integrity before export
assert log.verify(), "Audit log integrity failed"

# Export for auditors
log.export_json("audit_evidence.json")
log.export_csv("audit_evidence.csv")

```text
## Compliance Mapping

### Module to Compliance Domain

| Module | Compliance Domain | Use Case |
|--------|-------------------|----------|
| `kyc` | CDD/EDD | Identity verification, document checks |
| `kyc.screening` | Sanctions, PEP | Watchlist screening |
| `aml` | AML/CFT | Transaction monitoring |
| `aml.typology` | AML | Pattern detection |
| `security.audit` | Record keeping | Audit trails |
| `ai.explainability` | Model governance | Decision explanation |

### Regulatory Report Support

Ununseptium provides data structures aligned with common reports:

| Report Type | Module | Output |
|-------------|--------|--------|
| SAR data | `aml.reporting` | Structured alert data |
| CTR data | `aml.reporting` | Transaction summaries |
| Risk assessment | `ai.models` | Risk scores with factors |

**Note**: Report generation and filing remain user responsibility.

## Audit Readiness

### Self-Assessment Checklist

Use this checklist to assess audit readiness:

| Category | Check | Library Support |
|----------|-------|-----------------|
| Configuration | Documented config | `core.config` exports |
| Logging | Complete audit trail | `security.audit` |
| Integrity | Tamper-evident logs | Hash chains |
| Decisions | Explainable outputs | `ai.explainability` |
| Testing | Validation evidence | pytest integration |

### Evidence Generation Commands

```bash
# Export configuration
ununseptium config export --output config_evidence.json

# Verify audit log integrity
ununseptium audit verify audit.log --output verification_report.json

# Generate risk model documentation
ununseptium model validate model_card.json

```text
## Jurisdiction Considerations

### Framework Agnostic Design

Ununseptium is designed jurisdiction-agnostic:

| Approach | Benefit |
|----------|---------|
| Configurable thresholds | Adapt to local requirements |
| Extensible schemas | Add jurisdiction-specific fields |
| No hardcoded rules | Customize business logic |
| Audit flexibility | Meet various retention requirements |

### Common Jurisdictions

The library has been designed with awareness of:

| Jurisdiction | Framework | Notes |
|--------------|-----------|-------|
| EU | AMLD 6 | CDD, EDD, beneficial ownership |
| US | BSA/AML | CTR, SAR, 314(b) |
| UK | MLR 2017 | Risk assessment, PEP |
| International | FATF | Risk-based approach |

**Disclaimer**: Awareness does not imply certification or complete coverage.

## Model Governance

For AI/ML model compliance, see:

- [docs/ai/governance.md](docs/ai/governance.md)
- Model card schema in `model_zoo`

### Model Documentation

| Requirement | Implementation |
|-------------|----------------|
| Model purpose | Model card `intended_use` |
| Training data | Model card `training_data` |
| Performance | Model card `metrics` |
| Limitations | Model card `limitations` |
| Bias assessment | Model card `ethical_considerations` |

## Continuous Compliance

### Recommended Practices

| Practice | Implementation |
|----------|----------------|
| Regular audits | Run `ununseptium audit verify` |
| Version control | Track configuration changes |
| Testing | Automated compliance test suite |
| Documentation | Keep model cards current |
| Review | Periodic threshold review |

## Limitations

### What This Does NOT Provide

| Not Provided | Required Action |
|--------------|-----------------|
| Legal interpretation | Consult legal counsel |
| Regulatory filing | Implement filing systems |
| Complete coverage | Assess gaps |
| Certification | Obtain from authorities |

## References

- [FATF Recommendations](https://www.fatf-gafi.org/recommendations.html)
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- [EU AMLD 6](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32018L1673)
- [US BSA/AML](https://www.fincen.gov/resources/statutes-and-regulations/bank-secrecy-act)
- [ISO 37301](https://www.iso.org/standard/75080.html) - Compliance Management Systems

---

**Disclaimer**: This document describes technical capabilities and design considerations. It does not constitute compliance certification, legal advice, or regulatory approval. Users must conduct independent compliance assessments with qualified professionals.
