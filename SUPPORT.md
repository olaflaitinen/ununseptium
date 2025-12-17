# Support

## Scope

This document describes how to get help with ununseptium, including available support channels and resources.

### Non-Goals

- Security vulnerability reporting (see [SECURITY.md](SECURITY.md))
- Contributing guidelines (see [CONTRIBUTING.md](CONTRIBUTING.md))

## Definitions

| Term | Definition |
|------|------------|
| Issue | Bug report or feature request on GitHub |
| Discussion | Community question or conversation |
| PR | Pull Request with proposed changes |

## Getting Help

### Before Asking

Before opening an issue or discussion:

1. Check the [FAQ](docs/faq.md)
2. Search existing [issues](https://github.com/olaflaitinen/ununseptium/issues)
3. Search [discussions](https://github.com/olaflaitinen/ununseptium/discussions)
4. Review relevant [documentation](docs/index.md)

### Support Channels

| Channel | Use For | Response Time |
|---------|---------|---------------|
| [GitHub Issues](https://github.com/olaflaitinen/ununseptium/issues) | Bug reports, feature requests | 3-5 business days |
| [GitHub Discussions](https://github.com/olaflaitinen/ununseptium/discussions) | Questions, ideas, community help | Best effort |
| [Documentation](docs/index.md) | Self-service reference | Immediate |

### Issue Guidelines

When opening an issue, include:

```markdown
**Environment**
- Python version:
- ununseptium version:
- Operating system:

**Description**
Clear description of the issue.

**Steps to Reproduce**
1. Step one
2. Step two

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Minimal Reproducible Example**

```python
# Code that reproduces the issue

```text

```text
## Documentation Resources

### Quick Links

| Resource | Description |
|----------|-------------|
| [README](README.md) | Project overview and quick start |
| [Installation](README.md#installation) | Installation instructions |
| [Architecture](docs/architecture/overview.md) | System design |
| [Glossary](docs/glossary.md) | Terminology definitions |
| [FAQ](docs/faq.md) | Common questions |

### Module Documentation

| Module | Documentation |
|--------|---------------|
| KYC | [docs/kyc/kyc-overview.md](docs/kyc/kyc-overview.md) |
| AML | [docs/aml/aml-overview.md](docs/aml/aml-overview.md) |
| Security | [docs/security/security-overview.md](docs/security/security-overview.md) |
| MathStats | [docs/mathstats/mathstats-overview.md](docs/mathstats/mathstats-overview.md) |
| AI | [docs/ai/ai-overview.md](docs/ai/ai-overview.md) |
| Model Zoo | [docs/model-zoo/model-zoo.md](docs/model-zoo/model-zoo.md) |

## Self-Diagnosis

Run the built-in doctor command to check your installation:

```bash
ununseptium doctor

```text
This checks:

- Python version compatibility
- Required dependencies
- Optional dependencies
- Configuration validity

## Commercial Support

Ununseptium is open-source software provided as-is. Commercial support options may be available through third-party consultants.

**Disclaimer**: The ununseptium project does not endorse any specific commercial support providers.

## Response Expectations

| Priority | Description | Target Response |
|----------|-------------|-----------------|
| Critical | Security vulnerabilities | 48 hours |
| High | Blocking bugs | 3 business days |
| Medium | Non-blocking bugs, features | 1-2 weeks |
| Low | Enhancements, questions | Best effort |

## Community Guidelines

When seeking support:

1. Be respectful and patient
2. Provide complete information
3. Use appropriate channels
4. Follow the [Code of Conduct](CODE_OF_CONDUCT.md)

## References

- [GitHub Issues Best Practices](https://docs.github.com/en/issues)
- [How to Ask Questions the Smart Way](http://www.catb.org/~esr/faqs/smart-questions.html)

---

**Note**: This is a community-supported open-source project. Response times are best-effort and not guaranteed.
