# Sequential Detection

## Scope

This document describes sequential change detection algorithms in ununseptium.

### Non-Goals

- Batch change point detection
- Offline retrospective analysis
- Time series forecasting

## Definitions

| Term | Definition |
|------|------------|
| Change Point | Time when statistical properties change |
| CUSUM | Cumulative Sum algorithm |
| SPRT | Sequential Probability Ratio Test |
| ADWIN | Adaptive Windowing |

See [Glossary](../glossary.md) for additional terminology.

## Algorithms Overview

| Algorithm | Use Case | Complexity |
|-----------|----------|------------|
| CUSUM | Mean shift detection | O(1) per update |
| SPRT | Hypothesis testing | O(1) per update |
| ADWIN | Distribution change | O(log n) per update |

## CUSUM

### Algorithm

Cumulative Sum for detecting mean shifts:

$$S_n^+ = \max(0, S_{n-1}^+ + (x_n - \mu_0 - k))$$
$$S_n^- = \max(0, S_{n-1}^- - (x_n - \mu_0 + k))$$

Alarm when $S_n^+ > h$ or $S_n^- > h$.

### Usage

```python
from ununseptium.mathstats import CUSUM

detector = CUSUM(
    mu=0.0,        # Expected mean
    k=0.5,         # Slack parameter
    threshold=5.0, # Detection threshold
)

for observation in stream:
    alert = detector.update(observation)
    if alert:
        print(f"Change detected at time {detector.change_time}")
        detector.reset()

```text
### Parameters

| Parameter | Description | Typical Values |
|-----------|-------------|----------------|
| `mu` | Expected mean | Data-dependent |
| `k` | Sensitivity | 0.25-1.0 |
| `threshold` | False alarm control | 3-10 |

### Tuning

Average run length (ARL) before false alarm:

$$\text{ARL}_0 \approx \exp(2h(h+1.166)/\sigma^2)$$

| Threshold h | ARL (approx) |
|-------------|--------------|
| 3 | 500 |
| 4 | 3,000 |
| 5 | 20,000 |

## SPRT

### Algorithm

Sequential Probability Ratio Test:

$$\Lambda_n = \sum_{i=1}^{n} \log \frac{f_1(x_i)}{f_0(x_i)}$$

Decision rules:
- $\Lambda_n \geq B$: Accept $H_1$ (change)
- $\Lambda_n \leq A$: Accept $H_0$ (no change)
- Otherwise: Continue

### Usage

```python
from ununseptium.mathstats import SPRT

detector = SPRT(
    mu0=0.0,     # Null hypothesis mean
    mu1=1.0,     # Alternative mean
    sigma=1.0,   # Known std
    alpha=0.05,  # Type I error
    beta=0.10,   # Type II error
)

for observation in stream:
    result = detector.update(observation)
    if result == "H1":
        print("Change detected!")
    elif result == "H0":
        print("No change, resetting")
        detector.reset()

```text
### Thresholds

$$A = \log \frac{\beta}{1-\alpha}$$
$$B = \log \frac{1-\beta}{\alpha}$$

| $\alpha$ | $\beta$ | A | B |
|----------|---------|---|---|
| 0.05 | 0.10 | -2.25 | 2.89 |
| 0.01 | 0.05 | -2.94 | 4.55 |
| 0.01 | 0.01 | -4.60 | 4.60 |

## ADWIN

### Algorithm

Adaptive Windowing for arbitrary distribution changes:

```mermaid
graph LR
    W[Window] --> SPLIT[Try Splits]
    SPLIT --> TEST{Means Differ?}
    TEST -->|Yes| DROP[Drop Old Data]
    TEST -->|No| KEEP[Keep Window]
    DROP --> W
    KEEP --> W

```text
### Usage

```python
from ununseptium.mathstats import ADWIN

detector = ADWIN(delta=0.01)

for observation in stream:
    if detector.update(observation):
        print(f"Change detected!")
        print(f"New mean estimate: {detector.mean}")

```text
### Parameters

| Parameter | Description | Effect |
|-----------|-------------|--------|
| `delta` | Confidence | Lower = fewer false alarms |

## Combined Detection

### Multi-Algorithm Voting

```python
from ununseptium.mathstats import CUSUM, SPRT, ADWIN, EnsembleDetector

ensemble = EnsembleDetector(
    detectors=[
        CUSUM(threshold=4),
        SPRT(mu0=0, mu1=0.5),
        ADWIN(delta=0.01),
    ],
    voting="majority",  # or "any", "all"
)

for observation in stream:
    if ensemble.update(observation):
        print("Ensemble detected change!")

```text
## Application: Transaction Monitoring

```python
from ununseptium.aml import TransactionMonitor
from ununseptium.mathstats import CUSUM

# Monitor account velocity
detector = CUSUM(mu=10, k=2, threshold=5)

for tx in transaction_stream:
    velocity = monitor.compute_velocity(tx.account)

    if detector.update(velocity):
        alert = Alert(
            type="velocity_change",
            account=tx.account,
            details={"old_mean": 10, "new_value": velocity}
        )
        monitor.raise_alert(alert)
        detector.reset()

```text
## Performance

| Algorithm | Update | Memory |
|-----------|--------|--------|
| CUSUM | O(1) | O(1) |
| SPRT | O(1) | O(1) |
| ADWIN | O(log n) | O(log n) |

## Related Documentation

- [MathStats Overview](mathstats-overview.md)
- [Hawkes Processes](hawkes.md)
- [AML Overview](../aml/aml-overview.md)

## References

- Page, E. S. (1954). Continuous Inspection Schemes. Biometrika.
- Wald, A. (1947). Sequential Analysis.
- Bifet, A., & Gavalda, R. (2007). Learning from Time-Changing Data with Adaptive Windowing.
- [Glossary](../glossary.md)
