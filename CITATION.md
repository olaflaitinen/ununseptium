# Citation

## Scope

This document provides citation formats for academic and professional use of ununseptium.

### Non-Goals

- Licensing information (see [LICENSE](LICENSE))
- Contribution attribution (see [CONTRIBUTING.md](CONTRIBUTING.md))

## Definitions

| Term | Definition |
|------|------------|
| DOI | Digital Object Identifier - persistent identifier for digital content |
| BibTeX | Bibliography format for LaTeX documents |
| APA | American Psychological Association citation style |
| CFF | Citation File Format - machine-readable citation metadata |

## Preferred Citation

If you use ununseptium in academic work, please cite:

```text
Laitinen, O. (2025). Ununseptium: RegTech and Cybersecurity Library (Version 1.0.0) [Computer software]. <https://github.com/olaflaitinen/ununseptium>

```text
## Citation Formats

### BibTeX

```bibtex
@software{ununseptium2025,
  author       = {Laitinen, Olaf},
  title        = {Ununseptium: RegTech and Cybersecurity Library},
  year         = {2025},
  version      = {1.0.0},
  url          = {<https://github.com/olaflaitinen/ununseptium>},
  note         = {Python library for KYC/AML automation, data security, and AI-driven risk analysis}
}

```text
### APA 7th Edition

```text
Laitinen, O. (2025). Ununseptium: RegTech and Cybersecurity Library (Version 1.0.0) [Computer software]. GitHub. <https://github.com/olaflaitinen/ununseptium>

```text
### IEEE

```text
O. Laitinen, "Ununseptium: RegTech and Cybersecurity Library," version 1.0.0, 2025. [Online]. Available: <https://github.com/olaflaitinen/ununseptium>

```text
### Chicago

```text
Laitinen, Olaf. 2025. Ununseptium: RegTech and Cybersecurity Library. Version 1.0.0. <https://github.com/olaflaitinen/ununseptium.>

```text
### Harvard

```text
Laitinen, O., 2025. Ununseptium: RegTech and Cybersecurity Library. Version 1.0.0. Available at: <https://github.com/olaflaitinen/ununseptium> [Accessed: DD Mon YYYY].

```text
### MLA 9th Edition

```text
Laitinen, Olaf. Ununseptium: RegTech and Cybersecurity Library. Version 1.0.0, 2025, github.com/olaflaitinen/ununseptium.

```text
## Module-Specific Citations

When citing specific modules, reference the appropriate section:

| Module | Focus Area |
|--------|------------|
| `ununseptium.mathstats` | Statistical methods (conformal, EVT, Hawkes) |
| `ununseptium.ai` | ML methods (SciML, governance) |
| `ununseptium.security` | Security methods (audit, crypto) |
| `ununseptium.kyc` | Identity verification methods |
| `ununseptium.aml` | Transaction monitoring methods |

### Example for MathStats Module

```bibtex
@software{ununseptium_mathstats2025,
  author       = {Laitinen, Olaf},
  title        = {Ununseptium MathStats: Statistical Methods for Financial Risk},
  year         = {2025},
  version      = {1.0.0},
  url          = {<https://github.com/olaflaitinen/ununseptium>},
  note         = {Conformal prediction, EVT, Hawkes processes, copulas, sequential detection}
}

```text
## Mathematical Methods

When citing specific mathematical methods implemented in ununseptium, also cite the original works:

### Conformal Prediction

```bibtex
@book{vovk2005algorithmic,
  title     = {Algorithmic Learning in a Random World},
  author    = {Vovk, Vladimir and Gammerman, Alex and Shafer, Glenn},
  year      = {2005},
  publisher = {Springer}
}

```text
### Extreme Value Theory

```bibtex
@book{coles2001introduction,
  title     = {An Introduction to Statistical Modeling of Extreme Values},
  author    = {Coles, Stuart},
  year      = {2001},
  publisher = {Springer}
}

```text
### Hawkes Processes

```bibtex
@article{hawkes1971spectra,
  title   = {Spectra of some self-exciting and mutually exciting point processes},
  author  = {Hawkes, Alan G},
  journal = {Biometrika},
  volume  = {58},
  number  = {1},
  pages   = {83--90},
  year    = {1971}
}

```text
## CITATION.cff

A machine-readable citation file is provided at the repository root:

```yaml
cff-version: 1.2.0
message: "If you use this software, please cite it as below."
type: software
title: "Ununseptium: RegTech and Cybersecurity Library"
version: 1.0.0
date-released: 2025-12-17
url: "<https://github.com/olaflaitinen/ununseptium>"
repository-code: "<https://github.com/olaflaitinen/ununseptium>"
license: Apache-2.0
authors:
  - family-names: "Laitinen"
    given-names: "Olaf"
keywords:
  - kyc
  - aml
  - regtech
  - compliance
  - cybersecurity
  - machine-learning

```text
## Acknowledgments

If acknowledging rather than formally citing:

```text
We acknowledge the use of the ununseptium library (https://github.com/olaflaitinen/ununseptium) for [specific functionality].

```text
## Version Specificity

When reproducibility matters, specify the exact version:

```bibtex
@software{ununseptium_v1_0_0,
  author  = {Laitinen, Olaf},
  title   = {Ununseptium},
  version = {1.0.0},
  year    = {2025},
  url     = {<https://github.com/olaflaitinen/ununseptium/releases/tag/v1.0.0>}
}

```text
## References

- [BibTeX](http://www.bibtex.org/)
- [Citation File Format](https://citation-file-format.github.io/)
- [APA Style](https://apastyle.apa.org/)
- [Software Citation Principles](https://doi.org/10.7717/peerj-cs.86)
