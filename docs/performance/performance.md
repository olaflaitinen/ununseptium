# Performance

## Scope

This document describes performance characteristics and benchmarks for ununseptium.

### Non-Goals

- Infrastructure sizing
- Deployment optimization
- Hardware recommendations

## Definitions

| Term | Definition |
|------|------------|
| Throughput | Operations per second |
| Latency | Time for single operation |
| P95 | 95th percentile latency |

See [Glossary](../glossary.md) for additional terminology.

## Benchmark Summary

| Component | Operation | Throughput | P95 Latency |
|-----------|-----------|------------|-------------|
| KYC | Identity verification | 1,000/s | 5ms |
| KYC | Name screening | 500/s | 10ms |
| AML | Transaction scoring | 2,000/s | 3ms |
| AML | Typology detection | 100/s | 50ms |
| Security | PII scan | 5,000/s | 1ms |
| Security | Audit verify | 10,000/s | 0.5ms |

## Benchmark Configuration

Tests run on:

| Parameter | Value |
|-----------|-------|
| CPU | 8-core AMD64 |
| RAM | 16 GB |
| Python | 3.11 |
| OS | Ubuntu 22.04 |

## KYC Benchmarks

### Identity Verification

```text
Operation: IdentityVerifier.verify()
Iterations: 10,000

```text
| Metric | Value |
|--------|-------|
| Mean latency | 4.2ms |
| P50 latency | 3.8ms |
| P95 latency | 5.1ms |
| P99 latency | 7.2ms |
| Throughput | 1,050/s |

### Name Screening

```text
Operation: Screener.screen_name()
Watchlist size: 100,000 entries

```text
| Metric | Value |
|--------|-------|
| Mean latency | 8.5ms |
| P95 latency | 12ms |
| Throughput | 520/s |

## AML Benchmarks

### Transaction Scoring

```text
Operation: TransactionMonitor.process()
Features: 20 dimensions

```text
| Metric | Value |
|--------|-------|
| Mean latency | 2.5ms |
| P95 latency | 3.2ms |
| Throughput | 2,100/s |

### Batch Processing

| Batch Size | Throughput | P95 Latency |
|------------|------------|-------------|
| 1 | 2,100/s | 3ms |
| 32 | 15,000/s | 15ms |
| 128 | 25,000/s | 40ms |
| 512 | 30,000/s | 120ms |

## Model Zoo Benchmarks

### Model Loading

| Model | Load Time (cold) | Load Time (warm) |
|-------|------------------|------------------|
| aml-transaction-risk-v1 | 250ms | 50ms |
| anomaly-detector-v1 | 180ms | 40ms |
| entity-resolution-v1 | 200ms | 45ms |

### Inference

| Model | Throughput | P95 Latency |
|-------|------------|-------------|
| aml-transaction-risk-v1 | 5,000/s | 1.2ms |
| anomaly-detector-v1 | 8,000/s | 0.8ms |
| entity-resolution-v1 | 3,000/s | 2ms |

## Memory Usage

| Operation | Peak Memory |
|-----------|-------------|
| Library import | 50 MB |
| + Model load | +100-200 MB |
| + 1M transactions | +500 MB |

## Scalability

### CPU Scaling

Throughput scales linearly with cores:

| Cores | Relative Throughput |
|-------|---------------------|
| 1 | 1.0x |
| 2 | 1.9x |
| 4 | 3.7x |
| 8 | 7.2x |

### Batch Size Effect

$$\text{Throughput} \approx \frac{\text{Batch Size}}{\text{Fixed Cost} + \text{Per-Item Cost} \times \text{Batch Size}}$$

## Optimization Tips

| Technique | Benefit |
|-----------|---------|
| Batch processing | Higher throughput |
| Feature caching | Reduced redundant computation |
| Model preloading | Avoid cold start |
| Numba JIT | 2-10x for numerical ops |

### Using Numba

```bash
pip install ununseptium[perf]

```text

```python
# Numba-accelerated operations auto-detected
from ununseptium.mathstats import EVTAnalyzer

analyzer = EVTAnalyzer()  # Uses Numba if available

```text
## Profiling

### Timing Decorator

```python
from ununseptium.core import timed

@timed
def my_function():
    ...

# Outputs: my_function took 123.45ms

```text
### Built-in Profiling

```bash
ununseptium profile --operation verify --iterations 1000

```text
## Reproducing Benchmarks

```bash
# Run benchmarks
pytest benchmarks/ --benchmark-only

# Save results
pytest benchmarks/ --benchmark-json=results.json

```text
## Performance Figures

See [figures/](../figures/) for benchmark visualizations:

- [latency_histogram.svg](../figures/latency_histogram.svg)
- [throughput_benchmark.svg](../figures/throughput_benchmark.svg)

## Related Documentation

- [Architecture Overview](../architecture/overview.md)
- [AI Pipeline](../architecture/ai-pipeline.md)

## References

- [Glossary](../glossary.md)

