# Figures

## Scope

This directory contains figures and visualizations for ununseptium documentation.

## Definitions

| Term | Definition |
|------|------------|
| SVG | Scalable Vector Graphics |
| Deterministic | Same output for same seed |

## Generation

Figures are generated deterministically using `scripts/generate_figures.py`:

```bash
python scripts/generate_figures.py --output-dir docs/figures --format svg

```text
All figures use a fixed random seed (42) for reproducibility.

## Figure Catalog

| Figure | Description |
|--------|-------------|
| [calibration_curve.svg](calibration_curve.svg) | Model calibration comparison |
| [roc_pr_curves.svg](roc_pr_curves.svg) | ROC and Precision-Recall curves |
| [drift_over_time.svg](drift_over_time.svg) | Data and model drift visualization |
| [evt_tail_plot.svg](evt_tail_plot.svg) | EVT tail probability and QQ plot |
| [latency_histogram.svg](latency_histogram.svg) | Latency distribution comparison |
| [motif_frequency.svg](motif_frequency.svg) | Graph motif frequency analysis |
| [throughput_benchmark.svg](throughput_benchmark.svg) | Throughput vs latency trade-off |
| [audit_chain.svg](audit_chain.svg) | Audit log hash chain illustration |

## Figure Details

### calibration_curve.svg

Compares calibration of two models:
- Well-calibrated model (close to diagonal)
- Overconfident model (below diagonal)

Use case: Evaluating probability calibration.

### roc_pr_curves.svg

Side-by-side ROC and Precision-Recall curves:
- Model A: High performance
- Model B: Baseline

Use case: Model comparison for classification tasks.

### drift_over_time.svg

Three-panel visualization:
- Feature distribution drift (PSI)
- Performance degradation over time
- Prediction distribution shift (KL divergence)

Use case: Monitoring model health over time.

### evt_tail_plot.svg

Extreme Value Theory diagnostics:
- Tail probability plot (log scale)
- QQ plot for GPD fit

Use case: Validating EVT model fit.

### latency_histogram.svg

Latency distribution analysis:
- Histogram comparison (baseline vs optimized)
- Percentile bar chart

Use case: Performance benchmarking.

### motif_frequency.svg

Graph motif comparison:
- Normal vs suspicious accounts
- Multiple motif types

Use case: AML network analysis.

### throughput_benchmark.svg

Dual-axis plot:
- Throughput vs batch size
- P95 latency vs batch size

Use case: Batch size optimization.

### audit_chain.svg

Conceptual illustration:
- Hash chain structure
- Tamper-evident design

Use case: Audit documentation.

## Regenerating Figures

To regenerate all figures:

```bash
cd /path/to/ununseptium
python scripts/generate_figures.py

```text
Requirements:
- matplotlib
- numpy
- scipy

## Style Guide

Figures follow consistent styling:

| Element | Style |
|---------|-------|
| Primary color | #2E86AB |
| Secondary color | #E94F37 |
| Font | Sans-serif, 10pt |
| DPI | 150 |
| Format | SVG (vector) |

## References

- [Performance](../performance/performance.md)
- [MathStats Overview](../mathstats/mathstats-overview.md)
