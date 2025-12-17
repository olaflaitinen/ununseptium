# AI Pipeline

## Scope

This document describes the AI/ML processing pipeline in ununseptium.

### Non-Goals

- Model training procedures (use your MLOps)
- Infrastructure for model serving
- Specific model implementations

## Definitions

| Term | Definition |
|------|------------|
| Pipeline | Sequence of data transformations |
| Feature | Input variable for model |
| Inference | Model prediction generation |
| Explainability | Understanding model decisions |

See [Glossary](../glossary.md) for additional terminology.

## Pipeline Overview

```mermaid
graph TB
    subgraph "Data Ingestion"
        RAW[Raw Data]
        VALIDATE[Validation]
    end

    subgraph "Feature Engineering"
        EXTRACT[Feature Extraction]
        TRANSFORM[Transformation]
        SELECT[Selection]
    end

    subgraph "Model Inference"
        PREPROCESS[Preprocessing]
        MODEL[Model]
        POSTPROCESS[Postprocessing]
    end

    subgraph "Explainability"
        SHAP[SHAP Values]
        LIME[Local Interpretation]
    end

    subgraph "Governance"
        CARD[Model Card]
        AUDIT[Audit Log]
        MONITOR[Monitoring]
    end

    RAW --> VALIDATE
    VALIDATE --> EXTRACT
    EXTRACT --> TRANSFORM
    TRANSFORM --> SELECT
    SELECT --> PREPROCESS
    PREPROCESS --> MODEL
    MODEL --> POSTPROCESS
    POSTPROCESS --> SHAP
    POSTPROCESS --> AUDIT
    MODEL --> CARD
    MODEL --> MONITOR

```text
## Feature Engineering

### Feature Types

| Category | Features | Use Case |
|----------|----------|----------|
| Aggregate | Sum, mean, count | Transaction patterns |
| Velocity | Rate of change | Behavior changes |
| Graph | Degree, centrality | Network analysis |
| Temporal | Recency, frequency | Time patterns |
| Derived | Ratios, deltas | Comparative analysis |

### Feature Pipeline

```python
from ununseptium.ai import FeaturePipeline, feature

class TransactionFeatures(FeaturePipeline):

    @feature
    def transaction_count_24h(self, account: str) -> int:
        """Number of transactions in last 24 hours."""
        return self.store.count(account, hours=24)

    @feature
    def avg_transaction_amount(self, account: str) -> float:
        """Average transaction amount."""
        return self.store.mean_amount(account)

    @feature
    def velocity_ratio(self, account: str) -> float:
        """Ratio of recent to historical velocity."""
        recent = self.transaction_count_24h(account)
        historical = self.store.avg_daily_count(account)
        return recent / max(historical, 1)

```text
### Feature Store Integration

| Operation | Method |
|-----------|--------|
| Compute | `pipeline.compute(entity_id)` |
| Batch | `pipeline.compute_batch(entity_ids)` |
| Cache | Automatic with TTL |

## Model Framework

### Model Interface

```python
from abc import ABC, abstractmethod
from typing import Any
import numpy as np

class Model(ABC):
    """Base model interface."""

    @abstractmethod
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Generate predictions."""
        ...

    @abstractmethod
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Generate probability estimates."""
        ...

```text
### Model Types

| Type | Implementation | Use Case |
|------|----------------|----------|
| Ensemble | `EnsembleModel` | Production risk scoring |
| Neural | `NeuralModel` | Complex patterns |
| Statistical | `StatModel` | Interpretable baseline |
| Hybrid | `HybridModel` | Combined approaches |

### Ensemble Architecture

```mermaid
graph LR
    INPUT[Features] --> M1[Model 1]
    INPUT --> M2[Model 2]
    INPUT --> M3[Model 3]

    M1 --> AGG[Aggregator]
    M2 --> AGG
    M3 --> AGG

    AGG --> CALIBRATE[Calibration]
    CALIBRATE --> OUTPUT[Final Score]

```text
Ensemble combination:

$$\hat{y} = \sum_{i=1}^{n} w_i \cdot f_i(x)$$

Where $w_i$ are learned weights and $f_i$ are base models.

## Inference Pipeline

### Preprocessing

| Step | Transformation |
|------|----------------|
| Missing values | Imputation |
| Categorical | Encoding (one-hot, target) |
| Numerical | Scaling (standard, robust) |
| Outliers | Clipping |

### Postprocessing

| Step | Transformation |
|------|----------------|
| Calibration | Platt scaling, isotonic |
| Thresholding | Convert to decisions |
| Explanation | Generate SHAP values |

### Calibration

Probability calibration using Platt scaling:

$$P(y=1|f) = \frac{1}{1 + \exp(Af + B)}$$

Where $A$ and $B$ are learned parameters.

## Explainability

### SHAP Integration

```python
from ununseptium.ai import Explainer

explainer = Explainer(model)
explanation = explainer.explain(features)

print(f"Top factors: {explanation.top_features(n=5)}")

```text
### Explanation Output

| Field | Type | Description |
|-------|------|-------------|
| `shap_values` | array | Feature contributions |
| `base_value` | float | Expected value |
| `feature_names` | list | Feature labels |

### Interpretation Guidelines

| SHAP Value | Interpretation |
|------------|----------------|
| Positive | Increases prediction |
| Negative | Decreases prediction |
| Zero | No contribution |
| Large magnitude | Strong influence |

## Model Governance

### Model Card Schema

```python
from ununseptium.ai import ModelCard

card = ModelCard(
    model_id="aml-transaction-risk-v1",
    version="1.0.0",
    intended_use="Transaction risk scoring",
    training_data="Historical transactions 2020-2024",
    metrics={
        "auc_roc": 0.92,
        "precision_at_90_recall": 0.78,
    },
    limitations=[
        "Trained on US market data",
        "May underperform on new typologies",
    ],
    ethical_considerations=[
        "Reviewed for demographic bias",
        "Regular fairness audits required",
    ],
)

```text
### Governance Workflow

```mermaid
graph TB
    DEV[Development] --> VALIDATE[Validation]
    VALIDATE --> REVIEW[Review]
    REVIEW --> APPROVE{Approved?}
    APPROVE -->|Yes| DEPLOY[Deployment]
    APPROVE -->|No| DEV
    DEPLOY --> MONITOR[Monitoring]
    MONITOR -->|Drift| RETRAIN[Retrain]
    RETRAIN --> VALIDATE

```text
## Scientific ML

### Physics-Informed Neural Networks

Interface for PINNs:

```python
from ununseptium.ai.sciml import PINN

class RiskDynamics(PINN):
    def physics_loss(self, x: Tensor, y: Tensor) -> Tensor:
        """Enforce domain constraints."""
        # Risk must be non-negative
        return torch.relu(-y).mean()

```text
### Neural ODEs

For continuous-time dynamics:

$$\frac{dy}{dt} = f_\theta(y, t)$$

```python
from ununseptium.ai.sciml import NeuralODE

model = NeuralODE(
    hidden_dim=64,
    method="dopri5",
)

```text
## Performance Optimization

### Batch Processing

| Batch Size | Throughput | Latency |
|------------|------------|---------|
| 1 | 100/s | 10ms |
| 32 | 2000/s | 16ms |
| 128 | 5000/s | 25ms |

### Caching

| Level | TTL | Use Case |
|-------|-----|----------|
| Feature | 1h | Computed features |
| Model | Infinite | Loaded models |
| Prediction | 5m | Recent predictions |

## Related Documentation

- [Architecture Overview](overview.md)
- [Data Flow](data-flow.md)
- [AI Overview](../ai/ai-overview.md)
- [Model Zoo](../model-zoo/model-zoo.md)

## References

- [SHAP Paper](https://arxiv.org/abs/1705.07874)
- [Model Cards](https://arxiv.org/abs/1810.03993)
- [Neural ODE Paper](https://arxiv.org/abs/1806.07366)
- [Glossary](../glossary.md)
