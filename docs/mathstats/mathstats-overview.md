# MathStats Overview

## Scope

This document describes the mathematical and statistical methods module in ununseptium.

### Non-Goals

- Comprehensive statistics textbook
- All possible statistical methods
- Deep mathematical proofs

## Definitions

| Term | Definition |
|------|------------|
| Conformal Prediction | Distribution-free prediction sets |
| EVT | Extreme Value Theory for tail risks |
| Hawkes Process | Self-exciting point process |
| Copula | Multivariate dependency structure |

See [Glossary](../glossary.md) for additional terminology.

## Module Structure

```mermaid
graph TB
    subgraph "MathStats Module"
        CONF[Conformal Prediction]
        EVT[EVT]
        HAWKES[Hawkes Processes]
        COPULA[Copulas]
        SEQ[Sequential Detection]
        GRAPH[Graph Statistics]
    end

    subgraph "Dependencies"
        NUMPY[numpy]
        SCIPY[scipy]
        NETWORKX[networkx]
    end

    CONF --> SCIPY
    EVT --> SCIPY
    HAWKES --> NUMPY
    COPULA --> SCIPY
    SEQ --> NUMPY
    GRAPH --> NETWORKX

```text
## Method Overview

| Method | Use Case | Document |
|--------|----------|----------|
| Conformal Prediction | Uncertainty quantification | [uncertainty.md](uncertainty.md) |
| Sequential Detection | Real-time change detection | [sequential.md](sequential.md) |
| EVT | Tail risk estimation | [evt.md](evt.md) |
| Hawkes Processes | Event clustering | [hawkes.md](hawkes.md) |
| Copulas | Dependency modeling | (this doc) |
| Graph Statistics | Network analysis | [graph-features.md](graph-features.md) |

## Quick Start

### Conformal Prediction

Coverage-guaranteed prediction intervals:

```python
from ununseptium.mathstats import ConformalPredictor

predictor = ConformalPredictor(alpha=0.1)  # 90% coverage
predictor.calibrate(y_cal, y_pred_cal)

# Prediction with uncertainty
interval = predictor.predict(y_pred_new)
print(f"[{interval.lower}, {interval.upper}]")

```text
### Extreme Value Theory

Tail risk estimation:

```python
from ununseptium.mathstats import EVTAnalyzer

analyzer = EVTAnalyzer()
analyzer.fit(losses, threshold="auto")

# Estimate rare event probability
prob = analyzer.tail_probability(extreme_value)
var_99 = analyzer.value_at_risk(0.99)

```text
### Hawkes Processes

Event clustering analysis:

```python
from ununseptium.mathstats import HawkesProcess

hawkes = HawkesProcess()
hawkes.fit(event_times)

# Predict future intensity
intensity = hawkes.intensity(future_time)

```text
### Sequential Detection

Real-time change detection:

```python
from ununseptium.mathstats import CUSUM

detector = CUSUM(threshold=5.0)

for observation in stream:
    if detector.update(observation):
        print("Change detected!")

```text
## Mathematical Foundations

### Coverage Guarantee

Conformal prediction provides:

$$P(Y \in C(X)) \geq 1 - \alpha$$

Where $C(X)$ is the prediction set and $\alpha$ is the miscoverage rate.

### Tail Distribution

EVT models extreme values via GPD:

$$F(x) = 1 - \left(1 + \xi \frac{x}{\sigma}\right)^{-1/\xi}$$

Where $\xi$ is the shape and $\sigma$ is the scale parameter.

### Self-Excitation

Hawkes intensity function:

$$\lambda(t) = \mu + \sum_{t_i < t} \alpha e^{-\beta(t - t_i)}$$

Where $\mu$ is baseline, $\alpha$ is excitation, and $\beta$ is decay.

## Copulas

Model multivariate dependencies:

```python
from ununseptium.mathstats import GaussianCopula, TCopula

# Fit Gaussian copula
copula = GaussianCopula()
copula.fit(data)

# Sample from joint distribution
samples = copula.sample(1000)

# Compute dependence metrics
kendall_tau = copula.kendall_tau()

```text
### Supported Copulas

| Copula | Tail Dependence | Use Case |
|--------|-----------------|----------|
| Gaussian | None | General dependence |
| Student-t | Symmetric | Tail dependence |
| Clayton | Lower | Loss dependence |
| Gumbel | Upper | Extreme co-movements |
| Frank | None | Wide range of dependence |

### Tail Dependence Coefficient

$$\lambda_U = \lim_{u \to 1} P(F_2(X_2) > u | F_1(X_1) > u)$$

| Copula | $\lambda_U$ | $\lambda_L$ |
|--------|-------------|-------------|
| Gaussian | 0 | 0 |
| Student-t | $2t_{\nu+1}\left(-\sqrt{\nu+1}\sqrt{\frac{1-\rho}{1+\rho}}\right)$ | Same |
| Clayton | 0 | $2^{-1/\theta}$ |
| Gumbel | $2 - 2^{1/\theta}$ | 0 |

## Performance Characteristics

| Method | Complexity | Memory |
|--------|------------|--------|
| Conformal calibration | O(n log n) | O(n) |
| EVT fitting | O(n) | O(1) |
| Hawkes fitting | O(n^2) | O(n) |
| Copula fitting | O(n d^2) | O(d^2) |
| CUSUM update | O(1) | O(1) |

## Integration with AML/KYC

| Method | Application |
|--------|-------------|
| Conformal | Risk score uncertainty |
| EVT | Tail loss estimation |
| Hawkes | Transaction burst detection |
| Copulas | Joint risk modeling |
| Sequential | Real-time anomaly detection |
| Graph | Network risk features |

## Related Documentation

- [Uncertainty Quantification](uncertainty.md)
- [Sequential Detection](sequential.md)
- [EVT](evt.md)
- [Hawkes Processes](hawkes.md)
- [Graph Features](graph-features.md)

## References

- Vovk, V. et al. (2005). Algorithmic Learning in a Random World.
- Coles, S. (2001). An Introduction to Statistical Modeling of Extreme Values.
- Hawkes, A. G. (1971). Spectra of self-exciting point processes.
- Nelsen, R. B. (2006). An Introduction to Copulas.
- [Glossary](../glossary.md)
