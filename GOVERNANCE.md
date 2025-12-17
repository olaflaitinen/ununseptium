# Governance

## Scope

This document describes the governance model for the ununseptium project, including decision-making processes, roles, and release procedures.

### Non-Goals

- This document does not define technical architecture (see [docs/architecture/overview.md](docs/architecture/overview.md))
- This document does not replace the [Code of Conduct](CODE_OF_CONDUCT.md) for behavioral standards

## Definitions

| Term | Definition |
|------|------------|
| Maintainer | Individual with commit access and project oversight responsibility |
| Contributor | Anyone who submits code, documentation, or other improvements |
| RFC | Request for Comments - formal proposal for significant changes |
| SemVer | Semantic Versioning (MAJOR.MINOR.PATCH) |

## Project Structure

```mermaid
graph TB
    subgraph "Decision Making"
        LEAD[Project Lead]
        MAINT[Maintainers]
        CONTRIB[Contributors]
    end

    subgraph "Technical Areas"
        CORE[Core Module]
        KYC[KYC/AML Modules]
        SEC[Security Module]
        AI[AI/ML Modules]
        MATH[MathStats Module]
    end

    LEAD --> MAINT
    MAINT --> CONTRIB
    MAINT --> CORE
    MAINT --> KYC
    MAINT --> SEC
    MAINT --> AI
    MAINT --> MATH

```text
## Maintainers

### Current Maintainers

| Name | Role | GitHub | Focus Areas |
|------|------|--------|-------------|
| Olaf Laitinen | Project Lead | [@olaflaitinen](https://github.com/olaflaitinen) | All modules |

### Maintainer Responsibilities

1. **Code Review**: Review and merge pull requests
2. **Issue Triage**: Label and prioritize issues
3. **Release Management**: Prepare and publish releases
4. **Community Support**: Respond to discussions and questions
5. **Technical Direction**: Guide architectural decisions

### Becoming a Maintainer

Maintainer status is by invitation. Candidates typically:

- Have a history of quality contributions
- Demonstrate understanding of project goals
- Show consistent engagement over 6+ months
- Exhibit alignment with code of conduct

## Decision Process

### Types of Decisions

| Type | Process | Timeline |
|------|---------|----------|
| Bug fixes | Direct PR, maintainer approval | 1-3 days |
| Minor features | Issue discussion, PR review | 1-2 weeks |
| Major features | RFC process | 2-4 weeks |
| Breaking changes | RFC + extended review | 4-8 weeks |
| Governance changes | RFC + maintainer consensus | 4-8 weeks |

### RFC Process

For significant changes, follow this process:

1. **Proposal**: Open an issue titled "RFC: [Title]"
2. **Discussion**: Community feedback period (minimum 2 weeks)
3. **Revision**: Update proposal based on feedback
4. **Decision**: Maintainers approve, request changes, or reject
5. **Implementation**: If approved, proceed with implementation

### Voting

When consensus cannot be reached:

- Each maintainer has one vote
- Decisions require simple majority
- Project lead has tie-breaking vote
- Voting period is 7 days

## Release Process

### Versioning

Ununseptium follows [Semantic Versioning 2.0.0](https://semver.org/):

$$\text{Version} = \text{MAJOR}.\text{MINOR}.\text{PATCH}$$

| Component | Increment When |
|-----------|----------------|
| MAJOR | Incompatible API changes |
| MINOR | Backwards-compatible functionality |
| PATCH | Backwards-compatible bug fixes |

### Release Checklist

1. **Pre-release**
   - [ ] All tests pass
   - [ ] CHANGELOG.md updated
   - [ ] Version bumped in pyproject.toml
   - [ ] Documentation updated

2. **Release**
   - [ ] Create git tag (v1.x.x)
   - [ ] Push tag to trigger release workflow
   - [ ] Verify PyPI publication
   - [ ] Create GitHub release with notes

3. **Post-release**
   - [ ] Announce in discussions
   - [ ] Monitor for issues

### Release Schedule

| Release Type | Frequency | Notes |
|--------------|-----------|-------|
| Patch | As needed | Security and bug fixes |
| Minor | Monthly | New features |
| Major | Annually | Breaking changes |

## Security Governance

Security issues follow a separate process. See [SECURITY.md](SECURITY.md) for:

- Vulnerability reporting
- Disclosure timeline
- Security fix prioritization

## Amendments

This governance document may be amended through the RFC process with maintainer consensus.

## References

- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [CNCF Governance](https://www.cncf.io/governance/)
