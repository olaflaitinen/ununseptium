# AI Overview

## Scope

This document describes the AI/ML module in ununseptium for risk modeling, feature engineering, and model governance.

### Non-Goals

- Model training infrastructure
- MLOps platform features
- Deep learning frameworks

## Definitions

| Term | Definition |
|------|------------|
| Feature Engineering | Creating input variables for models |
| Ensemble | Combining multiple models |
| Explainability | Understanding model decisions |
| Model Card | Structured model documentation |

See [Glossary](../glossary.md) for additional terminology.

## Module Structure

```mermaid
graph TB
    subgraph "AI Module"
        FEATURES[Feature Engineering]
        MODELS[Model Framework]
        EXPLAIN[Explainability]
        GOVERN[Governance]
        SCIML[Scientific ML]
    end

    subgraph "Dependencies"
        NUMPY[numpy]
        TORCH[torch - optional]
        SHAP[shap - optional]
    end

    FEATURES --> NUMPY
    MODELS --> TORCH
    EXPLAIN --> SHAP
    GOVERN --> NUMPY
    SCIML --> TORCH

```text
## Components

| Component | Purpose | See |
|-----------|---------|-----|
| Feature Engineering | Transform raw data to features | This doc |
| Model Framework | Unified model interface | This doc |
| Explainability | SHAP, feature importance | This doc |
| Model Governance | Model cards, validation | [governance.md](governance.md) |
| Scientific ML | PINNs, Neural ODEs | [sciml.md](sciml.md) |

## Feature Engineering

### Feature Pipeline

```python
from ununseptium.ai import FeaturePipeline, feature

class TransactionFeatures(FeaturePipeline):

    @feature
    def tx_count_24h(self, account: str) -> int:
        return self.store.count(account, hours=24)

    @feature
    def avg_amount(self, account: str) -> float:
        return self.store.mean_amount(account)

    @feature
    def velocity_ratio(self, account: str) -> float:
        recent = self.tx_count_24h(account)
        historical = self.store.avg_daily_count(account)
        return recent / max(historical, 1)

# Compute features
pipeline = TransactionFeatures(store=feature_store)
features = pipeline.compute(account_id)

```text
### Feature Types

| Type | Examples | Use Case |
|------|----------|----------|
| Aggregate | sum, mean, count | Summary statistics |
| Velocity | rate, acceleration | Behavior change |
| Temporal | recency, frequency | Time patterns |
| Graph | degree, centrality | Network structure |
| Derived | ratios, deltas | Comparisons |

## Model Framework

### Base Interface

```python
from ununseptium.ai import Model

class RiskModel(Model):
    def predict(self, X):
        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)

```text
### Ensemble Models

```python
from ununseptium.ai import EnsembleModel

ensemble = EnsembleModel(
    models=[model1, model2, model3],
    weights=[0.4, 0.3, 0.3],
    aggregation="weighted_average",
)

predictions = ensemble.predict(X)

```text
Ensemble score:

$$\hat{y} = \sum_{i=1}^{n} w_i \cdot f_i(x)$$

### Model Types

| Type | Use Case |
|------|----------|
| `EnsembleModel` | Production scoring |
| `CalibratedModel` | Calibrated probabilities |
| `ThresholdModel` | Binary decisions |

## Explainability

### SHAP Integration

```python
from ununseptium.ai import Explainer

explainer = Explainer(model)

# Explain single prediction
explanation = explainer.explain(X_single)

print("Top factors:")
for factor in explanation.top_features(5):
    print(f"  {factor.name}: {factor.contribution:+.3f}")

# Batch explanations
explanations = explainer.explain_batch(X_batch)

```text
### SHAP Values

For prediction $f(x)$:

$$f(x) = \phi_0 + \sum_{i=1}^{M} \phi_i$$

Where $\phi_i$ is the contribution of feature $i$.

| SHAP Value | Interpretation |
|------------|----------------|
| Positive | Increases prediction |
| Negative | Decreases prediction |
| Zero | No effect |

### Feature Importance

```python
# Global importance
importance = explainer.feature_importance(X)

for name, value in importance.items():
    print(f"{name}: {value:.4f}")

```text
## Model Calibration

Ensure probabilities are well-calibrated:

```python
from ununseptium.ai import CalibratedModel

calibrated = CalibratedModel(model, method="isotonic")
calibrated.fit(X_cal, y_cal)

proba = calibrated.predict_proba(X_test)

```text
### Calibration Methods

| Method | Description |
|--------|-------------|
| Platt | Logistic regression |
| Isotonic | Non-parametric |

Platt scaling:

$$P(y=1|f) = \frac{1}{1 + \exp(Af + B)}$$

## Thresholding

Convert probabilities to decisions:

```python
from ununseptium.ai import ThresholdModel

thresholded = ThresholdModel(
    model,
    threshold=0.7,
    labels=["low_risk", "high_risk"],
)

decisions = thresholded.predict(X)

```text
### Threshold Selection

| Strategy | Approach |
|----------|----------|
| Fixed | Domain-determined |
| Cost-based | Minimize expected cost |
| Precision-based | Target precision level |
| Recall-based | Target recall level |

## Inference Pipeline

```mermaid
graph TB
    INPUT[Raw Data] --> PREPROCESS[Preprocessing]
    PREPROCESS --> FEATURES[Feature Engineering]
    FEATURES --> MODEL[Model Inference]
    MODEL --> CALIBRATE[Calibration]
    CALIBRATE --> EXPLAIN[Explainability]
    EXPLAIN --> OUTPUT[Result]

```text
## Performance Optimization

### Batch Processing

```python
# Process in batches for efficiency
results = model.predict_batch(X, batch_size=256)

```text
| Batch Size | Throughput | Latency |
|------------|------------|---------|
| 1 | 100/s | 10ms |
| 64 | 2000/s | 32ms |
| 256 | 5000/s | 50ms |

### Caching

```python
from ununseptium.ai import CachedModel

cached = CachedModel(model, cache_ttl=300)  # 5 minutes

```text
## Integration with AML/KYC

```python
from ununseptium.kyc import IdentityVerifier
from ununseptium.ai import RiskModel, Explainer

# Load risk model
model = RiskModel.load("identity-risk-v1")
explainer = Explainer(model)

# Verify with risk assessment
verifier = IdentityVerifier(risk_model=model)
result = verifier.verify(identity)

# Explain risk score
if result.risk_level == "high":
    explanation = explainer.explain(result.features)
    print(f"Risk factors: {explanation.top_features(3)}")

```text
## Related Documentation

- [SciML](sciml.md)
- [Governance](governance.md)
- [AI Pipeline](../architecture/ai-pipeline.md)
- [Model Zoo](../model-zoo/model-zoo.md)

## References

- [SHAP Paper](https://arxiv.org/abs/1705.07874)
- [Glossary](../glossary.md)
