# Frequently Asked Questions

## Scope

Common questions about ununseptium installation, usage, and capabilities.

### Non-Goals

- Regulatory interpretations
- Legal advice
- Infrastructure-specific troubleshooting

## Definitions

See [Glossary](glossary.md) for terminology.

## General

### What is ununseptium?

Ununseptium is a Python library providing computational tools for:

| Domain | Capabilities |
|--------|--------------|
| KYC | Identity verification, document processing, screening |
| AML | Transaction monitoring, typology detection |
| Security | PII protection, encryption, audit logs |
| AI/ML | Feature engineering, model governance |
| MathStats | Conformal prediction, EVT, Hawkes processes |

### Is ununseptium a compliance solution?

No. Ununseptium provides computational primitives that can be used to build compliance systems. It does not:

- Provide legal advice
- Guarantee regulatory compliance
- Replace human judgment
- Offer turnkey compliance

### What Python versions are supported?

| Python Version | Support Status |
|----------------|----------------|
| 3.11 | Supported |
| 3.12 | Supported |
| 3.13 | Supported |
| < 3.11 | Not supported |

## Installation

### How do I install ununseptium?

```bash
# From PyPI
pip install ununseptium

# From source
git clone <https://github.com/olaflaitinen/ununseptium.git>
cd ununseptium
pip install -e ".[dev]"

```text
### What are the optional dependencies?

| Extra | Contents | Command |
|-------|----------|---------|
| `crypto` | Cryptography package | `pip install ununseptium[crypto]` |
| `ai-torch` | PyTorch | `pip install ununseptium[ai-torch]` |
| `ai-jax` | JAX | `pip install ununseptium[ai-jax]` |
| `graph` | NetworkX | `pip install ununseptium[graph]` |
| `perf` | Numba | `pip install ununseptium[perf]` |
| `dev` | Development tools | `pip install ununseptium[dev]` |
| `all` | Everything | `pip install ununseptium[all]` |

### How do I verify my installation?

```bash
ununseptium doctor

```text
This checks Python version, dependencies, and configuration.

## Usage

### How do I verify an identity?

```python
from ununseptium.kyc import Identity, IdentityVerifier

identity = Identity(
    full_name="John Doe",
    date_of_birth="1985-03-15",
    nationality="US",
)

verifier = IdentityVerifier()
result = verifier.verify(identity)
print(f"Status: {result.status}")

```text
### How do I screen against watchlists?

```python
from ununseptium.kyc import Screener

screener = Screener()
result = screener.screen_name("John Doe", threshold=0.8)
print(f"Matches: {result.matches}")

```text
### How do I create an audit log?

```python
from ununseptium.security import AuditLog

log = AuditLog()
log.append({"action": "identity_verified", "id": "123"})
log.save("audit.log")

# Later: verify integrity
assert log.verify(), "Tampering detected"

```text
### How do I detect PII?

```python
from ununseptium.security import PIIScanner

scanner = PIIScanner()
findings = scanner.scan("My SSN is 123-45-6789")
print(f"Found: {findings}")

```text
## Security

### Is the encryption secure?

The `security.encryption` module supports:

| Backend | Algorithm | Security Level |
|---------|-----------|----------------|
| cryptography | Fernet (AES-128-CBC) | Production-ready |
| fallback (XOR) | XOR | NOT secure, demo only |

Always install the `cryptography` package for production use.

### Are audit logs tamper-proof?

Audit logs are tamper-evident, not tamper-proof:

$$H_n = \text{SHA256}(H_{n-1} \| \text{entry}_n)$$

The hash chain detects modifications but does not prevent them. Secure storage is your responsibility.

### How do I report a security vulnerability?

See [SECURITY.md](../SECURITY.md) for the disclosure process.

## Performance

### How fast is identity verification?

Performance depends on configuration. Typical benchmarks:

| Operation | Throughput | P95 Latency |
|-----------|------------|-------------|
| Identity verification | ~1000/sec | 5ms |
| Name screening | ~500/sec | 10ms |
| Transaction analysis | ~2000/sec | 3ms |

See [performance.md](performance/performance.md) for detailed benchmarks.

### Can I use GPU acceleration?

Yes, when using the `ai-torch` or `ai-jax` extras:

```python
import torch
from ununseptium.ai import RiskModel

model = RiskModel()
model.to("cuda")  # GPU acceleration

```text
## Model Zoo

### What pretrained models are available?

| Model ID | Domain | Use Case |
|----------|--------|----------|
| `aml-transaction-risk-v1` | AML | Transaction risk scoring |
| `anomaly-detector-v1` | General | Anomaly detection |
| `entity-resolution-v1` | KYC | Entity matching |

See [model-zoo.md](model-zoo/model-zoo.md) for the complete catalog.

### How do I load a pretrained model?

```python
from ununseptium.model_zoo import PretrainedModel

model = PretrainedModel.load("aml-transaction-risk-v1")
result = model.predict(features)

```text
## Troubleshooting

### Why do I get ModuleNotFoundError?

Ensure you installed optional dependencies:

```bash
pip install ununseptium[all]

```text
### Why is my audit log failing verification?

Common causes:

| Issue | Check |
|-------|-------|
| File corruption | Check file system |
| Manual editing | Audit logs should not be edited |
| Encoding issues | Ensure UTF-8 encoding |

### How do I debug configuration issues?

```bash
# Export current configuration
ununseptium config export --output config.json

# Validate configuration
ununseptium config validate

```text
## Contributing

### How do I contribute?

See [CONTRIBUTING.md](../CONTRIBUTING.md) for:

- Development setup
- Code style guidelines
- Pull request process

### Where do I report bugs?

Open an issue at: <https://github.com/olaflaitinen/ununseptium/issues>

## References

- [README](../README.md)
- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [SUPPORT.md](../SUPPORT.md)
