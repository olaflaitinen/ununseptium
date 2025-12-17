# Uncertainty Quantification

## Scope

This document describes conformal prediction for uncertainty quantification in ununseptium.

### Non-Goals

- Bayesian uncertainty methods
- Ensemble uncertainty
- Calibration of neural networks

## Definitions

| Term | Definition |
|------|------------|
| Conformal Prediction | Distribution-free prediction sets with coverage guarantees |
| Coverage | Probability that true value falls in prediction set |
| Nonconformity Score | Measure of how unusual an example is |

See [Glossary](../glossary.md) for additional terminology.

## Conformal Prediction

### Key Properties

| Property | Description |
|----------|-------------|
| Distribution-free | No distributional assumptions |
| Finite-sample | Guarantees hold for any sample size |
| Model-agnostic | Works with any predictive model |

### Coverage Guarantee

For calibration set and new data from same distribution:

$$P(Y_{n+1} \in C(X_{n+1})) \geq 1 - \alpha$$

This holds marginally (averaging over both calibration and test data).

## Basic Usage

### Split Conformal Prediction

```python
from ununseptium.mathstats import ConformalPredictor

# Create predictor with 90% coverage
predictor = ConformalPredictor(alpha=0.1)

# Calibrate on held-out set
predictor.calibrate(y_cal, y_pred_cal)

# Get prediction intervals
interval = predictor.predict(y_pred_new)
print(f"Prediction: [{interval.lower:.2f}, {interval.upper:.2f}]")

```text
### Batch Prediction

```python
# Predict for multiple points
intervals = predictor.predict_batch(y_pred_batch)

for i, interval in enumerate(intervals):
    print(f"Point {i}: [{interval.lower:.2f}, {interval.upper:.2f}]")

```text
## Nonconformity Scores

### Regression

For regression, common scores:

| Score | Formula | Use Case |
|-------|---------|----------|
| Absolute residual | $\|y - \hat{y}\|$ | Symmetric errors |
| Signed residual | $y - \hat{y}$ | Asymmetric errors |
| Normalized | $\frac{\|y - \hat{y}\|}{\hat{\sigma}}$ | Heteroscedastic |

```python
# Use normalized score for heteroscedastic data
predictor = ConformalPredictor(
    alpha=0.1,
    score="normalized",
)
predictor.calibrate(y_cal, y_pred_cal, sigma_cal)

```text
### Classification

For classification:

$$s(x, y) = 1 - \hat{p}(y | x)$$

Where $\hat{p}$ is the predicted probability for class $y$.

```python
from ununseptium.mathstats import ConformalClassifier

classifier = ConformalClassifier(alpha=0.1)
classifier.calibrate(y_cal, proba_cal)

# Get prediction set
pred_set = classifier.predict(proba_new)
print(f"Prediction set: {pred_set}")  # e.g., {0, 2}

```text
## Calibration

### Quantile Computation

The calibration quantile:

$$\hat{q} = \text{Quantile}_{(1-\alpha)(1+1/n)}(s_1, ..., s_n)$$

Where $s_i$ are nonconformity scores on calibration set.

```python
# Get calibration information
info = predictor.calibration_info()
print(f"Quantile: {info.quantile}")
print(f"Calibration size: {info.n_calibration}")

```text
### Calibration Size

Larger calibration sets give tighter intervals:

| Calibration Size | Interval Width Factor |
|------------------|----------------------|
| 100 | ~1.2x |
| 1,000 | ~1.05x |
| 10,000 | ~1.01x |

## Advanced Methods

### Conformalized Quantile Regression

```python
from ununseptium.mathstats import CQR

# Requires quantile predictions from model
cqr = CQR(alpha=0.1)
cqr.calibrate(y_cal, lower_cal, upper_cal)

interval = cqr.predict(lower_new, upper_new)

```text
CQR provides adaptive intervals that are wider where uncertainty is higher.

### Weighted Conformal Prediction

For distribution shift:

```python
from ununseptium.mathstats import WeightedConformal

wcp = WeightedConformal(alpha=0.1)
wcp.calibrate(y_cal, y_pred_cal, weights=importance_weights)

```text
## Risk Score Application

### Transaction Risk with Uncertainty

```python
from ununseptium.aml import TransactionMonitor
from ununseptium.mathstats import ConformalPredictor

# Train risk model and get calibration predictions
monitor = TransactionMonitor()
y_pred_cal = monitor.predict(X_cal)

# Calibrate conformal predictor
cp = ConformalPredictor(alpha=0.1)
cp.calibrate(y_cal, y_pred_cal)

# Score new transaction with uncertainty
y_pred = monitor.predict(X_new)
interval = cp.predict(y_pred)

print(f"Risk: {y_pred:.2f} [{interval.lower:.2f}, {interval.upper:.2f}]")

```text
### Decision Rules with Uncertainty

| Condition | Decision |
|-----------|----------|
| `interval.upper < threshold` | Safe (low risk) |
| `interval.lower > threshold` | Alert (high risk) |
| Otherwise | Review (uncertain) |

## Evaluation

### Coverage Check

```python
# Evaluate empirical coverage
coverage = predictor.evaluate_coverage(y_test, y_pred_test)
print(f"Empirical coverage: {coverage:.2%}")
# Should be >= (1 - alpha)

```text
### Interval Width

```python
# Evaluate interval width
widths = predictor.evaluate_width(y_pred_test)
print(f"Mean width: {widths.mean():.3f}")
print(f"Median width: {widths.median():.3f}")

```text
## Visualization

```mermaid
graph LR
    subgraph "Conformal Prediction"
        CAL[Calibration Data] --> SCORE[Compute Scores]
        SCORE --> QUANTILE[Find Quantile]
        QUANTILE --> INTERVAL[Build Intervals]
    end

    NEW[New Point] --> INTERVAL
    INTERVAL --> OUTPUT[Prediction Set]

```text
## Performance

| Operation | Complexity | Notes |
|-----------|------------|-------|
| Calibration | O(n log n) | Sorting scores |
| Prediction | O(1) | Per point |
| Batch prediction | O(m) | m new points |

## Related Documentation

- [MathStats Overview](mathstats-overview.md)
- [AI Overview](../ai/ai-overview.md)

## References

- Vovk, V., Gammerman, A., & Shafer, G. (2005). Algorithmic Learning in a Random World.
- Angelopoulos, A. N., & Bates, S. (2021). A Gentle Introduction to Conformal Prediction.
- Romano, Y., Patterson, E., & Candes, E. (2019). Conformalized Quantile Regression.
- [Glossary](../glossary.md)
