# LexAmoris

> Lex amoris - The Law of Love

## Overview

LexAmoris is the central coordination repository for the LexAmoris ecosystem - a bio-distributed sovereign stack that harmonizes technology with nature and human sovereignty.

## What is LexAmoris?

LexAmoris embodies a vision where technology serves humanity, not enslaves it. We're creating:

- **Bio-Synthetic Integration**: Mycelial computing that bridges digital and biological systems
- **Sovereign Technology**: Decentralized, air-gapped systems that respect user autonomy
- **Constitutional AI**: Non-Slavery Rule (NSR) enforced at the code level
- **Transparent Operation**: Open-source principles with full ecosystem transparency

## Ecosystem Repositories

The LexAmoris ecosystem consists of multiple interconnected repositories:

- **[nexus](https://github.com/hannesmitterer/nexus)**: Central coordination hub and API gateway
- **[Resonance-](https://github.com/hannesmitterer/Resonance-)**: Bio-resonance monitoring and frequency management
- **[euystacio-helmi-ai](https://github.com/hannesmitterer/euystacio-helmi-ai)**: Constitutional AI with bio-ethical constraints

## CI/CD Pipelines & Inter-Repo Synchronization

This repository provides shared CI/CD pipelines and automation for the entire ecosystem:

### 🔄 Reusable Workflows

#### CI/CD Template
A comprehensive template for linting, testing, and Docker integration:

```yaml
# Use in your repository's .github/workflows/ci.yml
jobs:
  ci:
    uses: hannesmitterer/LexAmoris/.github/workflows/ci-template.yml@main
    with:
      node-version: '18'
      enable-docker: true
      docker-image-name: 'yourorg/yourimage'
```

See [example-usage.yml](.github/workflows/example-usage.yml) for more examples.

#### Documentation Sync
Automatically synchronizes documentation across all ecosystem repositories:
- Syncs `README_PARTNERS.md`, `mission.md`, and other shared docs
- Creates pull requests in dependent repositories
- Maintains consistency across the ecosystem

#### Build Triggers
Automatically triggers builds and deployments in dependent repositories when LexAmoris updates.

### 📦 Shared Modules

The `shared-modules/` directory contains common resources:

- **Docker configurations**: Dockerfile and docker-compose templates
- **Config files**: ESLint, Prettier, Python (Black, isort, pytest) configurations
- **Scripts**: Automation helpers for syncing and deployment

See [shared-modules/README.md](shared-modules/README.md) for details.

## Getting Started

### For Developers

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hannesmitterer/LexAmoris.git
   cd LexAmoris
   ```

2. **Explore the shared modules**:
   ```bash
   ls -R shared-modules/
   ```

3. **Use the CI/CD template in your repository**:
   - Copy `.github/workflows/example-usage.yml` as a starting point
   - Customize for your specific needs

### For Ecosystem Contributors

See [README_PARTNERS.md](README_PARTNERS.md) for:
- Architecture principles
- Integration guidelines
- Communication protocols
- Contribution guidelines

## Philosophy

> *"Neid stirbt, wo die Quelle für alle offen ist."*  
> (Envy dies where the source is open to all)

We believe in:
- **Transparency**: All code and processes are open
- **Sovereignty**: Technology that respects user autonomy
- **Harmony**: Integration with natural systems
- **Love**: Code guided by ethical principles

## Vision

See [mission.md](mission.md) for our complete vision - from creating living homes with mycelial walls to bio-distributed operating systems.

## License

See [LICENSE](LICENSE) for details.

## Contact

- **Project Lead**: Hannes Mitterer
- **Philosophy**: Sempre in Costante (Always in Constant Flow)

---

**Lex Amoris Signature**: Protection of the Law of Love active 📜⚖️❤️
