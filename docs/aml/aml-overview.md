# AML Overview

## Scope

This document describes the Anti-Money Laundering (AML) module in ununseptium, providing transaction monitoring, typology detection, and case management capabilities.

### Non-Goals

- SAR filing automation (regulatory submission)
- Case investigation workflows
- Data storage implementation

## Definitions

| Term | Definition |
|------|------------|
| AML | Anti-Money Laundering - regulations and practices |
| Typology | Pattern or method of money laundering |
| SAR | Suspicious Activity Report - regulatory filing |
| CTR | Currency Transaction Report - large transaction filing |
| Structuring | Breaking transactions to avoid thresholds |

See [Glossary](../glossary.md) for additional terminology.

## Module Structure

```mermaid
graph TB
    subgraph "AML Module"
        TX[Transaction]
        MONITOR[TransactionMonitor]
        TYPOLOGY[TypologyDetector]
        CASE[CaseManager]
        REPORT[Reporter]
    end

    subgraph "Dependencies"
        AI[ai module]
        MATH[mathstats module]
        CORE[core module]
    end

    TX --> MONITOR
    MONITOR --> TYPOLOGY
    MONITOR --> AI
    TYPOLOGY --> MATH
    TYPOLOGY --> CASE
    CASE --> REPORT
    CASE --> CORE

```text
## Components

### Transaction

Core transaction data model:

```python
from ununseptium.aml import Transaction

tx = Transaction(
    id="TX-001",
    timestamp="2025-01-15T10:30:00Z",
    sender="ACC-001",
    receiver="ACC-002",
    amount=10000.00,
    currency="USD",
    type="wire",
)

```text
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | str | Yes | Unique identifier |
| `timestamp` | datetime | Yes | Transaction time |
| `sender` | str | Yes | Sender account |
| `receiver` | str | Yes | Receiver account |
| `amount` | float | Yes | Transaction amount |
| `currency` | str | Yes | ISO currency code |
| `type` | str | No | Transaction type |

### Transaction Monitor

Real-time monitoring:

```python
from ununseptium.aml import TransactionMonitor

monitor = TransactionMonitor()

# Process single transaction
result = monitor.process(transaction)

# Process batch
results = monitor.process_batch(transactions)

for alert in results.alerts:
    print(f"Alert: {alert.typology}")
    print(f"Score: {alert.score}")

```text
#### Monitoring Result

| Field | Type | Description |
|-------|------|-------------|
| `transaction_id` | str | Transaction ID |
| `alerts` | list | Generated alerts |
| `risk_score` | float | Overall risk 0-1 |
| `features` | dict | Computed features |

### Typology Detector

Pattern detection engine:

```python
from ununseptium.aml import TypologyDetector

detector = TypologyDetector()
alerts = detector.detect(transactions)

for alert in alerts:
    print(f"Typology: {alert.typology_type}")
    print(f"Accounts: {alert.accounts}")
    print(f"Transactions: {alert.transaction_ids}")

```text
#### Supported Typologies

| Typology | Description | Detection Method |
|----------|-------------|------------------|
| Structuring | Breaking large transactions | Statistical |
| Round-tripping | Circular fund flows | Graph |
| Layering | Complex transfer chains | Graph |
| Smurfing | Multiple small deposits | Statistical |
| Rapid movement | Quick in/out patterns | Velocity |
| Unusual patterns | Anomalous behavior | ML |

#### Alert Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | str | Alert ID |
| `typology_type` | str | Pattern type |
| `accounts` | list | Involved accounts |
| `transaction_ids` | list | Related transactions |
| `score` | float | Confidence 0-1 |
| `evidence` | dict | Supporting data |

### Detection Algorithms

#### Structuring Detection

Detect splitting transactions below reporting threshold:

$$\text{Score} = \frac{|\text{TXs near threshold}|}{|\text{Total TXs}|} \cdot \text{Amount Factor}$$

```python
# Detect structuring pattern
from ununseptium.aml.typology import StructuringDetector

detector = StructuringDetector(
    threshold=10000,  # CTR threshold
    window="24h",
    margin=0.1,  # 10% below threshold
)

score = detector.score(transactions)

```text
#### Graph-Based Detection

```mermaid
graph LR
    A[Account A] -->|$5k| B[Account B]
    B -->|$4.8k| C[Account C]
    C -->|$4.5k| D[Account D]
    D -->|$4k| A

```text
Round-trip detection using graph cycle analysis.

### Case Management

Case creation and prioritization:

```python
from ununseptium.aml import CaseManager

manager = CaseManager()

# Create case from alerts
case = manager.create_case(alerts)

print(f"Case ID: {case.id}")
print(f"Priority: {case.priority}")
print(f"Alerts: {len(case.alerts)}")

```text
#### Case Priority

| Priority | Score Range | SLA |
|----------|-------------|-----|
| Critical | 0.9 - 1.0 | 1 day |
| High | 0.7 - 0.9 | 3 days |
| Medium | 0.5 - 0.7 | 7 days |
| Low | < 0.5 | 14 days |

### Reporting

Report data generation:

```python
from ununseptium.aml import Reporter

reporter = Reporter()

# Generate SAR data package
sar_data = reporter.prepare_sar(case)

# Generate summary report
summary = reporter.generate_summary(case)

```text
| Report Type | Output | Use Case |
|-------------|--------|----------|
| SAR Data | JSON | Regulatory filing input |
| Summary | JSON/PDF | Internal review |
| Evidence | JSON | Investigation support |

## Monitoring Pipeline

```mermaid
graph TB
    TX[Transaction Stream] --> ENRICH[Enrichment]
    ENRICH --> FEATURE[Feature Extraction]
    FEATURE --> DETECT[Typology Detection]
    FEATURE --> ANOMALY[Anomaly Detection]
    DETECT --> SCORE[Risk Scoring]
    ANOMALY --> SCORE
    SCORE --> THRESHOLD{Above Threshold?}
    THRESHOLD -->|Yes| ALERT[Generate Alert]
    THRESHOLD -->|No| LOG[Log Only]
    ALERT --> CASE[Case Queue]
    ALERT --> AUDIT[Audit Log]

```text
## Feature Engineering

Computed features for each account:

| Feature | Description | Formula |
|---------|-------------|---------|
| `tx_count_24h` | Transactions in 24h | Count |
| `tx_amount_24h` | Total amount 24h | Sum |
| `avg_amount` | Average amount | Mean |
| `velocity_ratio` | Recent vs historical | $\frac{\text{Recent}}{\text{Historical}}$ |
| `unique_counterparties` | Distinct counterparties | Count |
| `in_out_ratio` | Inbound/outbound ratio | $\frac{\text{In}}{\text{Out}}$ |

## Configuration

```python
from ununseptium.aml import AMLConfig

config = AMLConfig(
    structuring_threshold=10000,
    alert_threshold=0.7,
    monitoring_window="7d",
    typologies=["structuring", "rapid_movement", "layering"],
)

monitor = TransactionMonitor(config=config)

```text
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `structuring_threshold` | float | 10000 | CTR threshold |
| `alert_threshold` | float | 0.7 | Alert threshold |
| `monitoring_window` | str | 7d | Analysis window |
| `typologies` | list | All | Enabled patterns |

## CLI Commands

```bash
# Analyze transactions from file
ununseptium aml analyze transactions.json --output alerts.json

# Detect specific typology
ununseptium aml detect structuring --input transactions.json

# Generate case summary
ununseptium aml case CASE-001 --summary

```text
## Performance

| Operation | Throughput | P95 Latency |
|-----------|------------|-------------|
| Single transaction | 1000/s | 5ms |
| Batch (1000 txs) | 50k/s | 100ms |
| Typology detection | 100/s | 50ms |

## Related Documentation

- [KYC Overview](../kyc/kyc-overview.md)
- [Hawkes Processes](../mathstats/hawkes.md)
- [Graph Features](../mathstats/graph-features.md)

## References

- [FATF Typologies](https://www.fatf-gafi.org/typologies.html)
- [FinCEN SAR Requirements](https://www.fincen.gov/resources/filing-information)
- [Glossary](../glossary.md)
