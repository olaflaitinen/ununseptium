# Data Flow

## Scope

This document describes how data flows through ununseptium processing pipelines.

### Non-Goals

- External system integration (user responsibility)
- Network protocols (out of scope)
- Persistent storage design (user responsibility)

## Definitions

| Term | Definition |
|------|------------|
| Pipeline | Sequence of processing stages |
| Stage | Individual processing step |
| Context | Metadata passed through pipeline |

See [Glossary](../glossary.md) for additional terminology.

## Overview

Data flows through ununseptium in discrete pipelines:

```mermaid
graph LR
    INPUT[Input Data] --> VALIDATE[Validation]
    VALIDATE --> PROCESS[Processing]
    PROCESS --> ENRICH[Enrichment]
    ENRICH --> OUTPUT[Output]

    PROCESS --> AUDIT[Audit Log]

```text
## KYC Data Flow

### Identity Verification Pipeline

```mermaid
graph TB
    subgraph "Input"
        ID_DATA[Identity Data]
        DOC_DATA[Document Data]
    end

    subgraph "Validation"
        SCHEMA[Schema Validation]
        FORMAT[Format Checks]
    end

    subgraph "Processing"
        VERIFY[Identity Verifier]
        DOC_PROC[Document Processor]
        SCREEN[Screener]
    end

    subgraph "Enrichment"
        RISK[Risk Scoring]
        EXPLAIN[Explainability]
    end

    subgraph "Output"
        RESULT[Verification Result]
        AUDIT[Audit Entry]
    end

    ID_DATA --> SCHEMA
    DOC_DATA --> FORMAT
    SCHEMA --> VERIFY
    FORMAT --> DOC_PROC
    VERIFY --> SCREEN
    DOC_PROC --> SCREEN
    SCREEN --> RISK
    RISK --> EXPLAIN
    EXPLAIN --> RESULT
    RESULT --> AUDIT

```text
### Data Transformations

| Stage | Input | Output | Transformation |
|-------|-------|--------|----------------|
| Validation | Raw JSON | Identity | Schema validation |
| Document | Image/PDF | Extracted fields | OCR/parsing |
| Screening | Name | Match list | Fuzzy matching |
| Risk | Features | Score | Model inference |

## AML Data Flow

### Transaction Monitoring Pipeline

```mermaid
graph TB
    subgraph "Ingestion"
        TX_STREAM[Transaction Stream]
        BATCH[Batch Import]
    end

    subgraph "Processing"
        NORMAL[Normalization]
        FEATURE[Feature Extraction]
        DETECT[Typology Detection]
    end

    subgraph "Analysis"
        SCORE[Risk Scoring]
        CLUSTER[Clustering]
        GRAPH[Graph Analysis]
    end

    subgraph "Output"
        ALERT[Alert Generation]
        CASE[Case Creation]
        REPORT[Reporting]
    end

    TX_STREAM --> NORMAL
    BATCH --> NORMAL
    NORMAL --> FEATURE
    FEATURE --> DETECT
    FEATURE --> GRAPH
    DETECT --> SCORE
    GRAPH --> SCORE
    SCORE --> CLUSTER
    CLUSTER --> ALERT
    ALERT --> CASE
    CASE --> REPORT

```text
### Typology Detection Flow

| Stage | Algorithm | Latency |
|-------|-----------|---------|
| Feature extraction | Statistical aggregation | ~5ms |
| Pattern matching | Rule engine | ~2ms |
| Anomaly detection | Ensemble model | ~10ms |
| Graph analysis | Subgraph matching | ~50ms |

## Security Data Flow

### PII Detection Pipeline

```mermaid
graph LR
    TEXT[Input Text] --> SCAN[PII Scanner]
    SCAN --> FINDINGS[PII Findings]
    FINDINGS --> MASK[Masking]
    MASK --> SAFE[Safe Output]
    MASK --> TOKEN_MAP[Token Map]

```text
### Audit Log Flow

Each operation generates an audit entry:

```mermaid
graph TB
    OP[Operation] --> ENTRY[Create Entry]
    ENTRY --> HASH[Compute Hash]

    subgraph "Hash Chain"
        PREV[Previous Hash]
        CURR[Current Hash]
    end

    PREV --> HASH
    HASH --> CURR
    CURR --> STORE[Store Entry]

```text
The hash chain formula:

$$H_n = \text{SHA256}(H_{n-1} \| \text{JSON}(\text{entry}_n))$$

## AI/ML Data Flow

### Model Inference Pipeline

```mermaid
graph TB
    subgraph "Input"
        RAW[Raw Features]
    end

    subgraph "Preprocessing"
        CLEAN[Cleaning]
        ENCODE[Encoding]
        SCALE[Scaling]
    end

    subgraph "Inference"
        MODEL[Model]
        ENSEMBLE[Ensemble]
    end

    subgraph "Postprocessing"
        CALIBRATE[Calibration]
        EXPLAIN[SHAP Values]
    end

    subgraph "Output"
        PRED[Prediction]
        CONF[Confidence]
        EXPL[Explanation]
    end

    RAW --> CLEAN
    CLEAN --> ENCODE
    ENCODE --> SCALE
    SCALE --> MODEL
    MODEL --> ENSEMBLE
    ENSEMBLE --> CALIBRATE
    CALIBRATE --> EXPLAIN
    EXPLAIN --> PRED
    EXPLAIN --> CONF
    EXPLAIN --> EXPL

```text
### Batch vs Streaming

| Mode | Use Case | Latency | Throughput |
|------|----------|---------|------------|
| Batch | Historical analysis | Minutes | High |
| Streaming | Real-time monitoring | <100ms | Medium |
| Micro-batch | Hybrid | 1-10s | High |

## Context Propagation

Metadata flows through pipelines:

```python
@dataclass
class PipelineContext:
    request_id: str
    timestamp: datetime
    user_id: str | None
    trace_id: str | None

```text
| Context Field | Purpose |
|---------------|---------|
| `request_id` | Correlation across stages |
| `timestamp` | Audit timeline |
| `user_id` | Attribution |
| `trace_id` | Distributed tracing |

## Error Handling

```mermaid
graph TB
    STAGE[Stage] --> ERROR{Error?}
    ERROR -->|No| NEXT[Next Stage]
    ERROR -->|Recoverable| RETRY[Retry]
    ERROR -->|Fatal| LOG[Log Error]
    RETRY -->|Success| NEXT
    RETRY -->|Fail| LOG
    LOG --> AUDIT[Audit]

```text
| Error Type | Handling |
|------------|----------|
| Validation | Reject input |
| Transient | Retry with backoff |
| Fatal | Log and terminate |

## Related Documentation

- [Architecture Overview](overview.md)
- [AI Pipeline](ai-pipeline.md)
- [Auditability](../security/auditability.md)

## References

- [Glossary](../glossary.md)
