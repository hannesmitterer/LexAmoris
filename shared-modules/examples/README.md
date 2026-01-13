# Examples

This directory contains example configuration files for LexAmoris ecosystem projects.

## Files

### package.json

Example `package.json` for Node.js projects with:
- Linting scripts (ESLint)
- Formatting scripts (Prettier)
- Testing scripts (Jest)
- Development scripts

**Usage:**
```bash
# Copy to your project root
cp shared-modules/examples/package.json .

# Install dependencies
npm install

# Run linting
npm run lint

# Run tests
npm test
```

### requirements.txt

Example Python dependencies file with:
- Development tools (Black, isort, flake8, pytest)
- Optional dependencies commented out

**Usage:**
```bash
# Copy to your project root
cp shared-modules/examples/requirements.txt .

# Install dependencies
pip install -r requirements.txt

# Run linting
black --check .
flake8 .

# Run tests
pytest
```

## Customization

These are starting templates. Customize them for your specific project:

1. **Add your project dependencies**: Uncomment or add new dependencies
2. **Adjust versions**: Update to latest compatible versions
3. **Modify scripts**: Add project-specific scripts as needed
4. **Keep core tools**: Maintain linting/formatting tools for consistency

## Integration with CI/CD

These examples work seamlessly with the LexAmoris CI/CD template:

- The CI template will automatically detect `package.json` or `requirements.txt`
- It will install dependencies and run linting/testing
- No additional configuration needed

See [QUICKSTART.md](../../QUICKSTART.md) for complete integration guide.
