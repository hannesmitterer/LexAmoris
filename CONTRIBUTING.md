# Contributing to LexAmoris Ecosystem

Thank you for your interest in contributing to the LexAmoris ecosystem! This document provides guidelines for contributing to this repository and the broader ecosystem.

## Philosophy

All contributions should align with the LexAmoris principle: **Protection of the Law of Love**.

This means:
- Respecting user sovereignty and privacy
- Promoting transparency and openness
- Avoiding harmful or exploitative patterns
- Supporting harmony between technology and nature

## How to Contribute

### 1. Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the issue tracker
2. Create a new issue with a clear title and description
3. Include relevant details: steps to reproduce, expected behavior, actual behavior
4. Tag the issue appropriately

### 2. Proposing Changes

For new features or significant changes:

1. Open an issue first to discuss the proposal
2. Wait for feedback from maintainers
3. Once approved, proceed with implementation

### 3. Submitting Pull Requests

#### Prerequisites

- Fork the repository
- Create a feature branch from `main`
- Make your changes following our coding standards

#### Code Standards

**For JavaScript/Node.js:**
```bash
# Use shared ESLint and Prettier configurations
cp shared-modules/config/.eslintrc.json .
cp shared-modules/config/.prettierrc.json .

# Run linting
npm run lint

# Format code
npm run format
```

**For Python:**
```bash
# Use shared configuration
cp shared-modules/config/pyproject.toml .

# Format code
black .
isort .

# Run linting
flake8 .
```

#### Commit Messages

Use conventional commit format:

```
type(scope): subject

body

footer
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(ci): add Python support to CI template

Add Python linting and testing to the reusable CI/CD template.
Includes support for pytest, black, and flake8.

Closes #123
```

```
docs(shared): update shared modules README

Clarify usage instructions for Docker templates.
```

#### Pull Request Process

1. **Create the PR**:
   - Provide a clear title and description
   - Reference any related issues
   - Explain what changes were made and why

2. **Ensure CI passes**:
   - All automated checks must pass
   - Fix any linting or test failures

3. **Wait for review**:
   - Maintainers will review your PR
   - Address any feedback or requested changes

4. **Merge**:
   - Once approved, maintainers will merge your PR
   - Your changes will be automatically synced to dependent repositories if applicable

### 4. Working with Shared Modules

When updating shared configurations or templates:

1. **Test thoroughly**:
   - Test changes in at least one dependent repository
   - Ensure backward compatibility when possible

2. **Document changes**:
   - Update relevant README files
   - Include migration instructions if needed

3. **Consider impact**:
   - Changes to shared modules affect all ecosystem repositories
   - Coordinate with maintainers before making breaking changes

### 5. Contributing to CI/CD Workflows

When modifying GitHub Actions workflows:

1. **Test locally** (if possible):
   - Use `act` or similar tools to test workflows locally
   - Validate YAML syntax

2. **Use workflow_dispatch**:
   - Add `workflow_dispatch` trigger for manual testing
   - Test in a fork before proposing changes

3. **Document inputs and outputs**:
   - Clearly document all workflow inputs
   - Explain expected behavior

## Development Setup

### Prerequisites

- Git
- Node.js 18+ (for JavaScript projects)
- Python 3.11+ (for Python projects)
- Docker (for Docker-related work)

### Initial Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hannesmitterer/LexAmoris.git
   cd LexAmoris
   ```

2. **Install development tools**:
   ```bash
   # For JavaScript
   npm install -g eslint prettier

   # For Python
   pip install black isort flake8 pytest
   ```

3. **Review existing code**:
   - Familiarize yourself with the codebase
   - Read README_PARTNERS.md for ecosystem overview
   - Check existing issues and PRs

## Testing

### Workflow Testing

To test workflow changes:

1. Fork the repository
2. Enable GitHub Actions in your fork
3. Push changes to trigger workflows
4. Verify workflows execute as expected

### Manual Testing

For documentation sync and build triggers:

1. Test with manual workflow dispatch
2. Verify outputs in dependent repositories
3. Check for any errors or warnings

## Code of Conduct

### Expected Behavior

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the best outcome for the ecosystem
- Respect differing viewpoints

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or inflammatory comments
- Publishing others' private information
- Any conduct that violates the Law of Love principle

## Getting Help

If you need assistance:

1. Check existing documentation (README files)
2. Search closed issues for similar questions
3. Open a new issue with the `question` label
4. Contact maintainers if needed

## Recognition

All contributors will be recognized in the project. Significant contributions may be highlighted in release notes.

## Ecosystem-Wide Contributions

Contributing to LexAmoris often means contributing to the entire ecosystem:

- Changes to shared modules affect all repositories
- Documentation syncs across multiple repositories
- CI/CD improvements benefit all projects

Your contributions have a multiplied impact!

## License

By contributing to LexAmoris, you agree that your contributions will be licensed under the same license as the project.

---

**Thank you for contributing to LexAmoris!**

*Lex Amoris Signature: Protection of the Law of Love active 📜⚖️❤️*
