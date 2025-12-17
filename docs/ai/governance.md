# Model Governance

## Scope

This document describes model governance practices supported by ununseptium.

### Non-Goals

- Full MLOps platform
- Model registry implementation
- Regulatory compliance certification

## Definitions

| Term | Definition |
|------|------------|
| Model Card | Structured model documentation |
| Model Validation | Verification of model quality |
| Drift | Change in data or model behavior |
| Governance | Policies for model lifecycle |

See [Glossary](../glossary.md) for additional terminology.

## Model Card Schema

```python
from ununseptium.ai import ModelCard

card = ModelCard(
    model_id="aml-transaction-risk-v1",
    version="1.0.0",
    name="Transaction Risk Model",

    # Purpose
    intended_use="Score transaction risk for AML monitoring",
    out_of_scope_use=[
        "Credit decisioning",
        "Automated sanctions decisions",
    ],

    # Data
    training_data="Historical transactions 2020-2024",
    training_data_size=10_000_000,
    preprocessing="Standard scaling, one-hot encoding",

    # Architecture
    model_type="Gradient Boosting Ensemble",
    hyperparameters={
        "n_estimators": 200,
        "max_depth": 6,
        "learning_rate": 0.1,
    },

    # Performance
    metrics={
        "auc_roc": 0.92,
        "auc_pr": 0.78,
        "precision_at_90_recall": 0.65,
    },

    # Limitations
    limitations=[
        "Trained on US market data only",
        "May underperform on new typologies",
        "Requires minimum 30-day transaction history",
    ],

    # Ethics
    ethical_considerations=[
        "Reviewed for demographic bias",
        "Regular fairness audits required",
        "Human review required for adverse decisions",
    ],
)

```text
## Model Card Fields

| Section | Fields | Purpose |
|---------|--------|---------|
| Identity | id, version, name | Identification |
| Purpose | intended_use, out_of_scope | Usage boundaries |
| Data | training_data, size | Data provenance |
| Architecture | type, hyperparameters | Technical details |
| Performance | metrics | Quality evidence |
| Limitations | limitations | Known issues |
| Ethics | ethical_considerations | Fairness |

## Validation

### Model Card Validation

```python
from ununseptium.ai import ModelCardValidator

validator = ModelCardValidator()
result = validator.validate(card)

if not result.is_valid:
    for error in result.errors:
        print(f"Error: {error}")

```text
### Required Fields

| Field | Required | Validation |
|-------|----------|------------|
| model_id | Yes | Non-empty string |
| version | Yes | Semantic version |
| intended_use | Yes | Non-empty |
| metrics | Yes | At least one metric |
| limitations | Yes | At least one |

## Model Registry

### Registration

```python
from ununseptium.ai import ModelRegistry

registry = ModelRegistry()

# Register model with card
registry.register(model, card)

# List registered models
for model_id in registry.list():
    print(model_id)

```text
### Versioning

```mermaid
graph LR
    V1[v1.0.0] --> V11[v1.1.0]
    V11 --> V12[v1.2.0]
    V12 --> V2[v2.0.0]

    V1 --> PROD1[Production]
    V12 --> PROD2[Production]

```text
## Model Validation

### Validation Checks

| Check | Description |
|-------|-------------|
| Performance | Meets threshold metrics |
| Stability | Predictions are stable |
| Fairness | No demographic bias |
| Robustness | Handles edge cases |

```python
from ununseptium.ai import ModelValidator

validator = ModelValidator()
report = validator.validate(model, X_test, y_test)

print(f"Performance: {report.performance}")
print(f"Fairness: {report.fairness}")
print(f"Approved: {report.approved}")

```text
### Approval Workflow

```mermaid
graph TB
    DEV[Development] --> VALIDATE[Validation]
    VALIDATE --> REVIEW{Review}
    REVIEW -->|Approved| STAGE[Staging]
    REVIEW -->|Rejected| DEV
    STAGE --> MONITOR[Monitoring]
    MONITOR -->|Drift| RETRAIN[Retrain]
    RETRAIN --> VALIDATE

```text
## Drift Detection

### Data Drift

Distribution shift in input features:

$$\text{PSI} = \sum_{i} (p_i - q_i) \ln\frac{p_i}{q_i}$$

```python
from ununseptium.ai import DriftDetector

detector = DriftDetector()

# Compare reference and current distributions
drift = detector.detect(X_reference, X_current)

if drift.psi > 0.2:
    print("Significant drift detected!")

```text
### Performance Drift

```python
# Monitor performance over time
monitor = detector.monitor_performance(y_true, y_pred)

if monitor.auc_drop > 0.05:
    print("Performance degradation detected!")

```text
### Drift Thresholds

| PSI Value | Interpretation | Action |
|-----------|----------------|--------|
| < 0.1 | No shift | Continue |
| 0.1 - 0.2 | Moderate | Monitor |
| > 0.2 | Significant | Investigate |

## Audit Trail

### Logged Events

| Event | Fields |
|-------|--------|
| Model registered | id, version, timestamp |
| Model deployed | id, environment |
| Prediction made | id, input_hash, output |
| Drift detected | id, metric, value |

```python
from ununseptium.ai import GovernanceLog

log = GovernanceLog()

# Log model event
log.append({
    "event": "model_deployed",
    "model_id": "aml-transaction-risk-v1",
    "version": "1.0.0",
    "environment": "production",
})

```text
## CLI Commands

```bash
# Validate model card
ununseptium model validate model_card.json

# Check model drift
ununseptium model drift --model-id aml-v1 --data current.csv

# Show model info
ununseptium model info aml-transaction-risk-v1

```text
## Related Documentation

- [AI Overview](ai-overview.md)
- [Model Zoo](../model-zoo/model-zoo.md)
- [Compliance](../../COMPLIANCE.md)

## References

- [Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993)
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- [Glossary](../glossary.md)
