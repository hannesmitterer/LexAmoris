# CI/CD Pipeline Documentation

## Overview

This repository includes a comprehensive CI/CD pipeline for the LexAmoris project, automating code quality checks, testing, containerization, and deployment.

## Workflows

### 1. CI Pipeline (`.github/workflows/ci.yml`)

Runs on every push and pull request to the `main` branch.

**Jobs:**
- **Python Linting**: Uses flake8 to check Python code style and quality
- **JavaScript Linting**: Uses eslint to check JavaScript code style
- **Python Unit Tests**: Runs pytest test suites
- **JavaScript Unit Tests**: Runs npm test scripts
- **Docker Build**: Builds and tests Docker containers for reproducibility

### 2. GitHub Pages Deployment (`.github/workflows/deploy-pages.yml`)

Automatically deploys documentation to GitHub Pages when changes are pushed to `main`.

## Configuration Files

### Python
- `requirements.txt`: Python dependencies
- `.flake8`: Flake8 linting configuration

### JavaScript
- `package.json`: Node.js project configuration and scripts
- `.eslintrc.json`: ESLint configuration

### Docker
- `Dockerfile`: Container definition for the web service
- `docker-compose.yml`: Multi-container orchestration (includes provisions for future IPFS integration)

### Git
- `.gitignore`: Excludes build artifacts, dependencies, and temporary files

## Local Development

### Running Linters

**Python:**
```bash
pip install -r requirements.txt
flake8 .
```

**JavaScript:**
```bash
npm install
npm run lint
```

### Running Tests

**Python:**
```bash
pytest
```

**JavaScript:**
```bash
npm test
```

### Docker

**Build and run with Docker Compose:**
```bash
docker-compose up --build
```

**Or use npm scripts:**
```bash
npm run docker:build
npm run docker:run
```

**Access the site:**
```
http://localhost:8080
```

## Future Extensions

The CI/CD pipeline is designed with extensibility in mind for:

1. **IPFS Integration**: Docker Compose includes commented configuration for IPFS nodes
2. **Mycelium Bio-Synthetic Components**: Placeholder for air-gapped and distributed deployments
3. **Advanced Testing**: Integration tests for bio-distributed systems
4. **Security Scanning**: Automated vulnerability scanning
5. **Performance Monitoring**: Metrics collection for sovereign stack components

## Lex Amoris Principles

All CI/CD processes follow the core principles:
- **Transparency**: All build and deployment processes are open and auditable
- **Sovereignty**: No external dependencies that compromise control
- **Distributed**: Designed for resilience and decentralization
- **Bio-Compatible**: Ready for integration with organic computing substrates

---

*Sempre in Costante | Lex Amoris*
