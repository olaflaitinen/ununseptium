# Hawkes Processes

## Scope

This document describes Hawkes processes for self-exciting event modeling in ununseptium.

### Non-Goals

- General point process theory
- Spatial point processes
- Advanced non-parametric methods

## Definitions

| Term | Definition |
|------|------------|
| Point Process | Random process counting events |
| Intensity | Instantaneous event rate |
| Self-Excitation | Events increase future event probability |
| Branching Ratio | Expected offspring per event |

See [Glossary](../glossary.md) for additional terminology.

## Hawkes Process Model

### Intensity Function

$$\lambda(t) = \mu + \sum_{t_i < t} \alpha e^{-\beta(t - t_i)}$$

| Parameter | Description | Interpretation |
|-----------|-------------|----------------|
| $\mu$ | Baseline intensity | Background rate |
| $\alpha$ | Excitation | Jump per event |
| $\beta$ | Decay | Memory decay |

### Branching Ratio

$$n = \frac{\alpha}{\beta}$$

| Branching Ratio | Behavior |
|-----------------|----------|
| $n < 1$ | Stable (subcritical) |
| $n = 1$ | Critical |
| $n > 1$ | Explosive (supercritical) |

## Basic Usage

### Fitting

```python
from ununseptium.mathstats import HawkesProcess

hawkes = HawkesProcess()
hawkes.fit(event_times)

print(f"Baseline mu: {hawkes.mu:.4f}")
print(f"Excitation alpha: {hawkes.alpha:.4f}")
print(f"Decay beta: {hawkes.beta:.4f}")
print(f"Branching ratio: {hawkes.branching_ratio:.3f}")

```text
### Intensity Computation

```python
# Compute intensity at specific time
intensity = hawkes.intensity(t=100.0)

# Compute intensity over time range
times = np.linspace(0, 200, 1000)
intensities = [hawkes.intensity(t) for t in times]

```text
### Simulation

```python
# Simulate events
simulated_times = hawkes.simulate(
    T=1000,       # Time horizon
    seed=42,      # Reproducibility
)

print(f"Generated {len(simulated_times)} events")

```text
## Visualization

```mermaid
graph TB
    subgraph "Hawkes Process"
        E1[Event 1] --> I1[Intensity Spike]
        E2[Event 2] --> I2[Intensity Spike]
        E3[Event 3] --> I3[Intensity Spike]
    end

    I1 --> DECAY1[Exponential Decay]
    I2 --> DECAY2[Exponential Decay]
    I3 --> DECAY3[Exponential Decay]

    DECAY1 --> SUM[Sum = Current Intensity]
    DECAY2 --> SUM
    DECAY3 --> SUM
    BASELINE[Baseline mu] --> SUM

```text
## Kernel Functions

### Exponential (Default)

$$g(t) = \alpha e^{-\beta t}$$

```python
hawkes = HawkesProcess(kernel="exponential")

```text
### Power Law

$$g(t) = \frac{\alpha}{(1 + t/\tau)^{1+\theta}}$$

```python
hawkes = HawkesProcess(kernel="power_law")

```text
### Kernel Comparison

| Kernel | Memory | Use Case |
|--------|--------|----------|
| Exponential | Short | Financial transactions |
| Power law | Long | Social media, earthquakes |

## Parameter Estimation

### Maximum Likelihood

Log-likelihood:

$$\ell(\theta) = \sum_{i} \log \lambda(t_i) - \int_0^T \lambda(t) dt$$

```python
# Fit with specific method
hawkes.fit(event_times, method="mle")

# Get log-likelihood
ll = hawkes.log_likelihood()
print(f"Log-likelihood: {ll:.2f}")

```text
### Expectation-Maximization

```python
hawkes.fit(event_times, method="em", max_iter=100)

```text
## Branching Structure

### Declustering

Identify triggered vs. background events:

```python
# Estimate event origins
origins = hawkes.decluster(event_times)

for i, origin in enumerate(origins):
    if origin == -1:
        print(f"Event {i}: Background")
    else:
        print(f"Event {i}: Triggered by event {origin}")

```text
### Cluster Statistics

```python
clusters = hawkes.identify_clusters(event_times)

print(f"Number of clusters: {len(clusters)}")
print(f"Mean cluster size: {np.mean([len(c) for c in clusters]):.2f}")

```text
## Application: Transaction Bursts

```python
from ununseptium.aml import TransactionMonitor
from ununseptium.mathstats import HawkesProcess

# Get transaction times for account
tx_times = monitor.get_transaction_times(account)

# Fit Hawkes process
hawkes = HawkesProcess()
hawkes.fit(tx_times)

# Check for unusual clustering
if hawkes.branching_ratio > 0.8:
    alert = Alert(
        type="suspicious_clustering",
        details={
            "branching_ratio": hawkes.branching_ratio,
            "baseline_rate": hawkes.mu,
        }
    )

```text
### Burst Detection

```python
# Current intensity
current_intensity = hawkes.intensity(current_time)
baseline = hawkes.mu

# Alert if intensity much higher than baseline
if current_intensity > 5 * baseline:
    print("Transaction burst detected!")

```text
## Goodness of Fit

### Residual Analysis

Transform to unit Poisson:

$$\tau_i = \int_0^{t_i} \lambda(s) ds$$

If model is correct, $\{\tau_i\}$ are unit Poisson.

```python
# Compute residuals
residuals = hawkes.residual_process(event_times)

# Test for Poisson (should have exponential gaps)
from scipy.stats import kstest
stat, pvalue = kstest(np.diff(residuals), "expon")
print(f"KS test p-value: {pvalue:.4f}")

```text
## Multivariate Extension

For interacting processes:

```python
from ununseptium.mathstats import MultivariateHawkes

# Two interacting processes
mhawkes = MultivariateHawkes(n_processes=2)
mhawkes.fit([times_1, times_2])

# Cross-excitation matrix
print("Excitation matrix:")
print(mhawkes.alpha_matrix)

```text
## Performance

| Operation | Complexity |
|-----------|------------|
| Fit (MLE) | O(n^2) |
| Fit (EM) | O(n^2 * iter) |
| Intensity | O(n) |
| Simulate | O(n) |

## Related Documentation

- [MathStats Overview](mathstats-overview.md)
- [Sequential Detection](sequential.md)
- [AML Overview](../aml/aml-overview.md)

## References

- Hawkes, A. G. (1971). Spectra of some self-exciting and mutually exciting point processes. Biometrika.
- Bacry, E., Mastromatteo, I., & Muzy, J. F. (2015). Hawkes processes in finance.
- [Glossary](../glossary.md)
