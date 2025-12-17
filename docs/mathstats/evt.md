# Extreme Value Theory

## Scope

This document describes Extreme Value Theory (EVT) for tail risk estimation in ununseptium.

### Non-Goals

- Full EVT textbook coverage
- Block maxima methods (focus on POT)
- Multivariate EVT

## Definitions

| Term | Definition |
|------|------------|
| EVT | Extreme Value Theory - statistics of rare events |
| POT | Peaks Over Threshold method |
| GPD | Generalized Pareto Distribution |
| VaR | Value at Risk |
| ES | Expected Shortfall |

See [Glossary](../glossary.md) for additional terminology.

## Peaks Over Threshold

### Concept

For sufficiently high threshold $u$, exceedances follow GPD:

```mermaid
graph LR
    DATA[Data] --> THRESHOLD[Threshold u]
    THRESHOLD --> EXCEED[Exceedances]
    EXCEED --> GPD[Fit GPD]
    GPD --> TAIL[Tail Estimates]

```text
### GPD Distribution

$$F(x) = 1 - \left(1 + \xi \frac{x}{\sigma}\right)^{-1/\xi}$$

| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| $\xi$ (shape) | Tail heaviness | -0.5 to 0.5 |
| $\sigma$ (scale) | Spread | > 0 |

### Shape Interpretation

| $\xi$ Value | Tail Type | Examples |
|-------------|-----------|----------|
| $\xi > 0$ | Heavy (Pareto) | Financial losses |
| $\xi = 0$ | Exponential | Light tails |
| $\xi < 0$ | Bounded | Physical limits |

## Usage

### Basic Fitting

```python
from ununseptium.mathstats import EVTAnalyzer

analyzer = EVTAnalyzer()

# Fit with automatic threshold selection
analyzer.fit(losses, threshold="auto")

# Or specify threshold
analyzer.fit(losses, threshold=100)

# Get parameters
print(f"Shape (xi): {analyzer.xi:.3f}")
print(f"Scale (sigma): {analyzer.sigma:.3f}")

```text
### Risk Measures

```python
# Value at Risk (quantile)
var_99 = analyzer.value_at_risk(0.99)
var_999 = analyzer.value_at_risk(0.999)

# Expected Shortfall (CVaR)
es_99 = analyzer.expected_shortfall(0.99)

# Tail probability
prob = analyzer.tail_probability(extreme_value)

print(f"VaR 99%: {var_99:.2f}")
print(f"ES 99%: {es_99:.2f}")
print(f"P(X > {extreme_value}): {prob:.6f}")

```text
## VaR and ES Formulas

### Value at Risk

$$\text{VaR}_p = u + \frac{\sigma}{\xi}\left[\left(\frac{n}{n_u}(1-p)\right)^{-\xi} - 1\right]$$

Where:
- $u$ is threshold
- $n$ is total observations
- $n_u$ is exceedances

### Expected Shortfall

$$\text{ES}_p = \frac{\text{VaR}_p}{1-\xi} + \frac{\sigma - \xi u}{1-\xi}$$

For $\xi < 1$.

## Threshold Selection

### Automatic Methods

```python
# Mean residual life plot
analyzer.plot_mean_residual()

# Parameter stability plot
analyzer.plot_parameter_stability()

# Automatic selection
threshold = analyzer.select_threshold(method="eyeball")

```text
| Method | Description |
|--------|-------------|
| `eyeball` | Parameter stability |
| `square_root` | $\sqrt{n}$ rule |
| `percentile` | Fixed quantile (e.g., 95th) |

### Trade-off

| Threshold | Exceedances | Bias | Variance |
|-----------|-------------|------|----------|
| Low | Many | High | Low |
| High | Few | Low | High |

## Confidence Intervals

```python
# Bootstrap confidence intervals
ci = analyzer.confidence_interval(
    metric="VaR",
    level=0.99,
    confidence=0.95,
    method="bootstrap",
    n_bootstrap=1000,
)

print(f"VaR 99% CI: [{ci.lower:.2f}, {ci.upper:.2f}]")

```text
## Application: Transaction Risk

```python
from ununseptium.aml import TransactionMonitor
from ununseptium.mathstats import EVTAnalyzer

# Historical transaction amounts
amounts = monitor.get_historical_amounts(account)

# Fit EVT
evt = EVTAnalyzer()
evt.fit(amounts, threshold="auto")

# Assess if new transaction is extreme
new_amount = 50000
prob = evt.tail_probability(new_amount)

if prob < 0.001:  # Less than 1 in 1000
    alert = Alert(
        type="extreme_transaction",
        details={"amount": new_amount, "probability": prob}
    )

```text
## Diagnostics

### QQ Plot

```python
# Generate QQ plot data
qq_data = analyzer.qq_plot_data()

# Check if GPD fit is good
# Points should follow diagonal

```text
### Return Level Plot

```python
# Return levels for different periods
return_levels = analyzer.return_levels(
    periods=[10, 50, 100, 500]
)

for period, level in return_levels.items():
    print(f"{period}-observation return level: {level:.2f}")

```text
## Multivariate Extension

For correlated extremes:

```python
from ununseptium.mathstats import EVTAnalyzer

# Analyze tail dependence
chi = analyzer.tail_dependence_coefficient(losses1, losses2)
print(f"Tail dependence: {chi:.3f}")

```text
## Performance

| Operation | Complexity |
|-----------|------------|
| Fit | O(n) |
| VaR | O(1) |
| ES | O(1) |
| Bootstrap CI | O(B * n) |

## Related Documentation

- [MathStats Overview](mathstats-overview.md)
- [Uncertainty](uncertainty.md)

## References

- Coles, S. (2001). An Introduction to Statistical Modeling of Extreme Values.
- Embrechts, P., Kluppelberg, C., & Mikosch, T. (1997). Modelling Extremal Events.
- McNeil, A. J., Frey, R., & Embrechts, P. (2015). Quantitative Risk Management.
- [Glossary](../glossary.md)
