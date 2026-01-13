# LexAmoris Ecosystem - Partner Documentation

> This document is automatically synchronized across all LexAmoris ecosystem repositories.

## Overview

The LexAmoris ecosystem consists of multiple interconnected repositories working together to create a bio-distributed sovereign stack for harmonious living.

## Ecosystem Repositories

### Core Repositories

1. **LexAmoris** (Main)
   - Repository: `hannesmitterer/LexAmoris`
   - Purpose: Central coordination and shared resources
   - Website: Vision and mission homepage

2. **Nexus**
   - Repository: `hannesmitterer/nexus`
   - Purpose: Central coordination hub and API gateway
   - Role: Connects all modules in the ecosystem

3. **Resonance-**
   - Repository: `hannesmitterer/Resonance-`
   - Purpose: Bio-resonance monitoring and frequency management
   - Role: Handles 0.0043 Hz synchronization

4. **Euystacio-Helmi-AI**
   - Repository: `hannesmitterer/euystacio-helmi-ai`
   - Purpose: Constitutional AI with bio-ethical constraints
   - Role: Non-Slavery Rule (NSR) enforcement

## Architecture Principles

### 1. Decentralized Sovereignty
- No central points of failure
- Air-gapped operation capability
- IPFS-based immutable storage

### 2. Bio-Synthetic Integration
- Wetware-to-Hardware interfaces
- Mycelial computing nodes
- Living error correction

### 3. Constitutional AI
- NSR (Non-Slavery Rule) enforced at code level
- Bio-ethical consent protocols
- Transparent operation logs

### 4. Transparent Operation
- All repositories follow open-source principles
- S-ROI (Sovereignty Return on Investment) tracking
- Community-driven development

## Integration Guidelines

### For Developers

When contributing to any repository in the ecosystem:

1. **Respect the Lex Amoris Signature**: All code must align with the law of love principle
2. **Maintain Compatibility**: Changes should work across all ecosystem repositories
3. **Document Changes**: Update this file when adding new integration points
4. **Test Holistically**: Consider impacts on other repositories

### Shared CI/CD

All repositories use shared CI/CD templates from the LexAmoris repository:

- Linting and code quality checks
- Automated testing
- Docker build and deployment
- Cross-repository synchronization

### Documentation Sync

Key documentation files are automatically synchronized:
- `README_PARTNERS.md` (this file)
- `mission.md`
- Other shared documentation

## Communication Protocols

### Repository Dispatch Events

Repositories communicate via GitHub Actions `repository_dispatch` events:

```yaml
event_type: lexamoris-update
client_payload:
  source_repo: hannesmitterer/LexAmoris
  source_sha: <commit-sha>
  source_ref: refs/heads/main
```

### Build Triggers

When LexAmoris updates, dependent repositories are automatically notified to:
- Rebuild with latest shared modules
- Update documentation
- Run integration tests

## Shared Modules

Common resources are centralized in `LexAmoris/shared-modules/`:

- **Docker configurations**: Standardized container setups
- **Config files**: Shared linting, formatting rules
- **Scripts**: Automation and deployment helpers

## Vision

> "Neid stirbt, wo die Quelle für alle offen ist." (Envy dies where the source is open to all)

We're creating technology that serves humanity, not enslaves it. Every component in this ecosystem respects user sovereignty, environmental harmony, and the fundamental law of love.

## Support & Contact

- **Project Lead**: Hannes Mitterer
- **Philosophy**: Sempre in Costante (Always in Constant Flow)
- **License**: See LICENSE in each repository

---

**Lex Amoris Signature**: Protection of the Law of Love active 📜⚖️❤️

*Last synchronized: Auto-updated via GitHub Actions*
