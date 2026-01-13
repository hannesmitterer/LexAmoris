# LexAmoris Shared Modules

This directory contains common resources, configurations, and templates shared across the LexAmoris ecosystem repositories.

## Directory Structure

```
shared-modules/
├── docker/           # Docker configurations
├── config/           # Linting and formatting configs
├── scripts/          # Automation scripts
└── README.md         # This file
```

## Contents

### Docker (`docker/`)

- **Dockerfile.template**: Base Dockerfile template for ecosystem services
- **docker-compose.template.yml**: Docker Compose configuration template

#### Usage

Copy the templates to your repository and customize as needed:

```bash
cp shared-modules/docker/Dockerfile.template ./Dockerfile
cp shared-modules/docker/docker-compose.template.yml ./docker-compose.yml
```

Customize the files for your specific service while maintaining the common patterns.

### Configuration (`config/`)

Shared linting and code quality configurations:

- **.eslintrc.json**: ESLint configuration for JavaScript/Node.js
- **.prettierrc.json**: Prettier formatting configuration
- **pyproject.toml**: Python project configuration (Black, isort, pytest)

#### Usage

**For JavaScript/Node.js projects:**

```bash
# Copy config files
cp shared-modules/config/.eslintrc.json .
cp shared-modules/config/.prettierrc.json .

# Install dependencies
npm install --save-dev eslint prettier

# Add scripts to package.json
# "lint": "eslint .",
# "format": "prettier --write ."
```

**For Python projects:**

```bash
# Copy config
cp shared-modules/config/pyproject.toml .

# Install tools
pip install black isort flake8 pytest pytest-cov
```

### Scripts (`scripts/`)

Automation and helper scripts:

- **sync-docs.sh**: Manual documentation synchronization script

#### Usage

```bash
# Sync default documentation files
./shared-modules/scripts/sync-docs.sh

# Sync custom repositories and files
./shared-modules/scripts/sync-docs.sh "owner/repo1,owner/repo2" "file1.md,file2.md"
```

## Integration with CI/CD

The LexAmoris repository provides reusable GitHub Actions workflows:

### CI/CD Template

Use the CI/CD template in your repository:

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, master, develop]
  pull_request:

jobs:
  ci:
    uses: hannesmitterer/LexAmoris/.github/workflows/ci-template.yml@main
    with:
      node-version: '18'
      python-version: '3.11'
      enable-docker: true
      docker-image-name: 'yourorg/yourimage'
    secrets:
      DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
      DOCKER_PASSWORD: ${{ secrets.DOCKER_PASSWORD }}
```

### Automatic Documentation Sync

Documentation is automatically synchronized when changes are pushed to the LexAmoris repository. To enable this in your repository:

1. Ensure your repository is listed in the sync targets
2. Add a workflow to handle `repository_dispatch` events:

```yaml
# .github/workflows/handle-lexamoris-update.yml
name: Handle LexAmoris Update

on:
  repository_dispatch:
    types: [lexamoris-update]

jobs:
  rebuild:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Trigger CI
        run: echo "Rebuilding after LexAmoris update from ${{ github.event.client_payload.source_sha }}"
```

### Build Triggers

Your repository will automatically receive build triggers when LexAmoris is updated. Handle these events to rebuild/redeploy as needed.

## Best Practices

### 1. Keep Configurations Synchronized

Periodically update your local copies of shared configurations:

```bash
# From your repository root
git checkout -b update-shared-config
cp ../LexAmoris/shared-modules/config/.eslintrc.json .
cp ../LexAmoris/shared-modules/config/.prettierrc.json .
git add .
git commit -m "chore: update shared configurations from LexAmoris"
```

### 2. Maintain Compatibility

When making changes to your repository:
- Ensure they work with the shared configurations
- Test with the CI/CD template
- Document any deviations from the standard setup

### 3. Contribute Back

If you create useful configurations or scripts:
- Consider contributing them back to LexAmoris/shared-modules
- Submit a PR to help the entire ecosystem

## Philosophy

> "Neid stirbt, wo die Quelle für alle offen ist."

These shared modules embody the LexAmoris principle of open, transparent collaboration. By sharing common resources:

- We reduce duplication
- We maintain consistency
- We enable faster development
- We strengthen the ecosystem

## Support

For questions or issues:
- Open an issue in the LexAmoris repository
- Consult the README_PARTNERS.md documentation
- Contact the project maintainer

---

**Lex Amoris Signature**: Protection of the Law of Love active 📜⚖️❤️
