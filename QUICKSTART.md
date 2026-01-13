# Quick Start Guide - LexAmoris CI/CD & Synchronization

This guide helps you quickly integrate LexAmoris CI/CD pipelines and synchronization into your repository.

## For Ecosystem Repositories

If you're working on a repository that's part of the LexAmoris ecosystem (nexus, Resonance-, euystacio-helmi-ai, etc.), follow these steps:

### Step 1: Add CI/CD Workflow

Create `.github/workflows/ci.yml` in your repository:

```yaml
name: CI

on:
  push:
    branches: [main, master, develop]
  pull_request:
  workflow_dispatch:

jobs:
  ci:
    uses: hannesmitterer/LexAmoris/.github/workflows/ci-template.yml@main
    with:
      node-version: '18'              # Adjust as needed
      python-version: '3.11'          # Adjust as needed
      run-linting: true
      run-tests: true
      enable-docker: false            # Set to true if you use Docker
      docker-image-name: ''           # Set if enable-docker is true
    secrets:
      DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
      DOCKER_PASSWORD: ${{ secrets.DOCKER_PASSWORD }}
```

### Step 2: Handle LexAmoris Updates

Create `.github/workflows/lexamoris-update.yml`:

```yaml
name: Handle LexAmoris Updates

on:
  repository_dispatch:
    types: [lexamoris-update]

jobs:
  rebuild:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Log update
        run: |
          echo "LexAmoris updated!"
          echo "Source: ${{ github.event.client_payload.source_repo }}"
          echo "SHA: ${{ github.event.client_payload.source_sha }}"
      
      - name: Trigger CI
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.actions.createWorkflowDispatch({
              owner: context.repo.owner,
              repo: context.repo.repo,
              workflow_id: 'ci.yml',
              ref: 'main'
            })
```

### Step 3: Copy Shared Configurations

```bash
# From your repository root
mkdir -p .github/workflows

# Copy configuration files
curl -o .eslintrc.json https://raw.githubusercontent.com/hannesmitterer/LexAmoris/main/shared-modules/config/.eslintrc.json
curl -o .prettierrc.json https://raw.githubusercontent.com/hannesmitterer/LexAmoris/main/shared-modules/config/.prettierrc.json
curl -o pyproject.toml https://raw.githubusercontent.com/hannesmitterer/LexAmoris/main/shared-modules/config/pyproject.toml

# Copy Docker templates (if using Docker)
curl -o Dockerfile https://raw.githubusercontent.com/hannesmitterer/LexAmoris/main/shared-modules/docker/Dockerfile.template
curl -o docker-compose.yml https://raw.githubusercontent.com/hannesmitterer/LexAmoris/main/shared-modules/docker/docker-compose.template.yml
```

### Step 4: Customize for Your Project

Edit the copied files to match your project's needs:

- Update `Dockerfile` with your specific dependencies
- Adjust `docker-compose.yml` for your services
- Modify linting rules if needed (but try to stay consistent)

### Step 5: Enable GitHub Actions

1. Go to your repository settings
2. Navigate to Actions > General
3. Ensure "Allow all actions and reusable workflows" is selected
4. Enable "Read and write permissions" for the GITHUB_TOKEN

### Step 6: Test the Setup

```bash
# Commit and push
git add .
git commit -m "chore: integrate LexAmoris CI/CD pipelines"
git push

# Check the Actions tab in GitHub to see workflows running
```

## For New Projects

If you're starting a new project in the ecosystem:

### 1. Initialize Your Project

```bash
# Create repository on GitHub first, then:
git clone https://github.com/yourorg/yourrepo.git
cd yourrepo
```

### 2. Set Up Basic Structure

```bash
# For Node.js project
npm init -y

# For Python project
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

### 3. Follow Steps 1-6 Above

Add CI/CD workflows and shared configurations as described.

### 4. Add to Synchronization

To receive documentation updates from LexAmoris:

1. Fork the LexAmoris repository
2. Update `.github/workflows/sync-docs.yml` to include your repository
3. Submit a PR to the LexAmoris repository

## Common Tasks

### Run Linting Locally

```bash
# JavaScript/Node.js
npm run lint

# Python
black --check .
flake8 .
isort --check-only .
```

### Build Docker Image

```bash
docker build -t yourimage:latest .
docker-compose up
```

### Manual Documentation Sync

```bash
# Clone LexAmoris
git clone https://github.com/hannesmitterer/LexAmoris.git
cd LexAmoris

# Run sync script
./shared-modules/scripts/sync-docs.sh "yourorg/yourrepo" "README_PARTNERS.md,mission.md"
```

### Trigger Build in Another Repository

Use the GitHub API or workflow dispatch:

```bash
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.github.com/repos/yourorg/yourrepo/dispatches \
  -d '{"event_type":"lexamoris-update"}'
```

## Troubleshooting

### Workflows Not Running

- Check Actions are enabled in repository settings
- Verify workflow YAML syntax
- Check branch protection rules

### Docker Build Fails

- Ensure Dockerfile is customized for your project
- Check dependencies are available
- Verify Docker secrets are set correctly

### Linting Errors

- Run linters locally first
- Fix errors before pushing
- Consider using pre-commit hooks

## Next Steps

1. Read [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
2. Review [README_PARTNERS.md](README_PARTNERS.md) for ecosystem overview
3. Join discussions in the LexAmoris community

## Support

- Open an issue in the LexAmoris repository
- Tag with `question` or `help wanted`
- Provide context and error messages

---

**Lex Amoris Signature**: Protection of the Law of Love active 📜⚖️❤️
