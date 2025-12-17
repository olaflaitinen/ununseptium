# Model Zoo

## Scope

This document describes pretrained models available in the ununseptium Model Zoo.

### Non-Goals

- Model training procedures
- Custom model development
- Model deployment infrastructure

## Definitions

| Term | Definition |
|------|------------|
| Pretrained Model | Model trained on representative data |
| Model Card | Structured model documentation |
| Checksum | Hash for integrity verification |

See [Glossary](../glossary.md) for additional terminology.

## Available Models

| Model ID | Domain | Type | AUC-ROC |
|----------|--------|------|---------|
| `aml-transaction-risk-v1` | AML | Classification | 0.92 |
| `anomaly-detector-v1` | General | Anomaly | 0.88 |
| `entity-resolution-v1` | KYC | Matching | 0.91 |
| `sar-priority-v1` | AML | Ranking | 0.87 |
| `graph-risk-v1` | AML | GNN | 0.90 |

## Loading Models

```python
from ununseptium.model_zoo import PretrainedModel

# Load model
model = PretrainedModel.load("aml-transaction-risk-v1")

# Make predictions
scores = model.predict(features)

```text
### With Specific Version

```python
model = PretrainedModel.load(
    "aml-transaction-risk-v1",
    version="1.0.0",
)

```text
## Model Details

### aml-transaction-risk-v1

Transaction-level risk scoring for AML.

| Attribute | Value |
|-----------|-------|
| **Input** | Transaction features (20 dims) |
| **Output** | Risk score [0, 1] |
| **Architecture** | Gradient Boosting |
| **Training Data** | Synthetic + benchmark |

**Features Required:**

| Feature | Type | Description |
|---------|------|-------------|
| `amount` | float | Transaction amount |
| `tx_count_24h` | int | Account transactions in 24h |
| `avg_amount_7d` | float | Average amount last 7 days |
| `unique_receivers` | int | Distinct receivers |
| ... | ... | (see model card) |

### anomaly-detector-v1

General-purpose anomaly detection.

| Attribute | Value |
|-----------|-------|
| **Input** | Numeric features (variable) |
| **Output** | Anomaly score [0, 1] |
| **Architecture** | Isolation Forest + Neural |
| **Use Case** | Unsupervised anomaly detection |

### entity-resolution-v1

Entity matching for deduplication.

| Attribute | Value |
|-----------|-------|
| **Input** | Entity pair features |
| **Output** | Match probability [0, 1] |
| **Architecture** | Neural classifier |
| **Use Case** | KYC entity matching |

### sar-priority-v1

SAR prioritization model.

| Attribute | Value |
|-----------|-------|
| **Input** | Alert features |
| **Output** | Priority score [0, 1] |
| **Architecture** | Transformer-based |
| **Use Case** | Alert triage |

### graph-risk-v1

Graph-based risk scoring.

| Attribute | Value |
|-----------|-------|
| **Input** | Node embedding |
| **Output** | Risk score [0, 1] |
| **Architecture** | GNN (requires networkx) |
| **Use Case** | Network-aware risk |

## Package Structure

```text
model_zoo/
    catalog.json        # Model index
    models/
        aml-transaction-risk-v1/
            model.pkl   # Model weights
            card.json   # Model card
            checksum.sha256

```text
## Integrity Verification

All models include checksums:

```python
from ununseptium.model_zoo import verify_model

# Verify before loading
if verify_model("aml-transaction-risk-v1"):
    model = PretrainedModel.load("aml-transaction-risk-v1")
else:
    raise SecurityError("Model checksum mismatch!")

```text
### Checksum Format

SHA-256 hash of model file:

$$\text{checksum} = \text{SHA256}(\text{model\_bytes})$$

## Model Cards

Each model includes a card:

```python
from ununseptium.model_zoo import get_model_card

card = get_model_card("aml-transaction-risk-v1")

print(f"Intended use: {card.intended_use}")
print(f"Limitations: {card.limitations}")
print(f"Metrics: {card.metrics}")

```text
## Custom Model Registration

Register your own models:

```python
from ununseptium.model_zoo import ModelRegistry

registry = ModelRegistry()

# Register custom model
registry.register(
    model_id="my-custom-model",
    model=model,
    card=model_card,
)

# Later: load custom model
custom = registry.load("my-custom-model")

```text
## Downloading Models

Models are downloaded on first use:

```python
# Auto-downloads if not cached
model = PretrainedModel.load("aml-transaction-risk-v1")

```text
### Manual Download

```python
from ununseptium.model_zoo import download_model

# Pre-download
download_model("aml-transaction-risk-v1", cache_dir="~/.ununseptium/models")

```text
### Cache Location

| Platform | Default Location |
|----------|------------------|
| Linux | `~/.cache/ununseptium/models` |
| macOS | `~/Library/Caches/ununseptium/models` |
| Windows | `%LOCALAPPDATA%\ununseptium\models` |

## Usage Examples

### Transaction Scoring

```python
from ununseptium.model_zoo import PretrainedModel
from ununseptium.aml import Transaction

model = PretrainedModel.load("aml-transaction-risk-v1")

transactions = [
    Transaction(amount=9500, ...),
    Transaction(amount=500, ...),
]

for tx in transactions:
    features = extract_features(tx)
    score = model.predict(features)[0]
    print(f"Risk: {score:.3f}")

```text
### Batch Processing

```python
# Efficient batch scoring
scores = model.predict_batch(features_batch)

```text
## CLI Commands

```bash
# List available models
ununseptium model list

# Download model
ununseptium model download aml-transaction-risk-v1

# Show model info
ununseptium model info aml-transaction-risk-v1

# Verify model
ununseptium model verify aml-transaction-risk-v1

```text
## Performance

| Operation | Latency |
|-----------|---------|
| Load (cached) | ~100ms |
| Load (download) | Network-dependent |
| Predict (single) | ~1ms |
| Predict (batch=100) | ~10ms |

## Related Documentation

- [AI Overview](../ai/ai-overview.md)
- [Governance](../ai/governance.md)
- [Security Overview](../security/security-overview.md)

## References

- [Model Cards Paper](https://arxiv.org/abs/1810.03993)
- [Glossary](../glossary.md)
