# LexAmoris Ecosystem Architecture

## Overview

The LexAmoris ecosystem uses a hub-and-spoke model with the LexAmoris repository at the center, providing shared resources and automation to all connected repositories.

## Repository Structure

```
LexAmoris (Central Hub)
├── Shared CI/CD Workflows
├── Shared Modules
├── Documentation Templates
└── Automation Scripts
    |
    ├─── Triggers ───> nexus
    ├─── Syncs ─────> Resonance-
    └─── Updates ───> euystacio-helmi-ai
```

## Components

### 1. Central Repository: LexAmoris

**Purpose**: Central coordination, shared resources, documentation

**Responsibilities**:
- Host reusable CI/CD workflow templates
- Store shared configuration files
- Maintain ecosystem-wide documentation
- Trigger builds in dependent repositories
- Synchronize documentation across repos

**Key Files**:
- `.github/workflows/ci-template.yml` - Reusable CI/CD template
- `.github/workflows/sync-docs.yml` - Documentation sync automation
- `.github/workflows/trigger-builds.yml` - Build trigger automation
- `shared-modules/` - Common resources and configurations
- `README_PARTNERS.md` - Ecosystem documentation

### 2. Dependent Repositories

**Examples**: nexus, Resonance-, euystacio-helmi-ai

**How They Integrate**:

1. **Use CI/CD Template**:
   ```yaml
   jobs:
     ci:
       uses: hannesmitterer/LexAmoris/.github/workflows/ci-template.yml@main
   ```

2. **Receive Documentation Updates**:
   - Automatic PR creation when LexAmoris docs change
   - Files synced: `README_PARTNERS.md`, `mission.md`

3. **Handle Build Triggers**:
   - Listen for `repository_dispatch` events
   - Rebuild when LexAmoris updates

## Workflow Diagrams

### CI/CD Template Flow

```
Developer Pushes Code
         |
         v
GitHub Actions Triggered
         |
         v
   LexAmoris CI Template
         |
    ┌────┴────┐
    v         v
  Lint      Test
    |         |
    └────┬────┘
         v
    Docker Build (optional)
         |
         v
    Push to Registry (optional)
```

### Documentation Sync Flow

```
LexAmoris README_PARTNERS.md Updated
         |
         v
sync-docs.yml Triggered
         |
         v
Clone Target Repos
    (nexus, Resonance-, euystacio-helmi-ai)
         |
         v
Copy Updated Documentation
         |
         v
Create Sync Branch
         |
         v
Push & Create PR
         |
         v
Target Repos Receive PRs
```

### Build Trigger Flow

```
LexAmoris Push/Release
         |
         v
trigger-builds.yml Runs
         |
         v
Send repository_dispatch Events
         |
    ┌────┼────┐
    v    v    v
  nexus  Res  eustacio
    |    |    |
    v    v    v
 Rebuild/Redeploy
```

## Communication Protocols

### 1. Reusable Workflows

**Protocol**: `workflow_call`

**Flow**:
1. Dependent repo declares workflow usage
2. GitHub Actions calls LexAmoris template
3. Template executes with provided inputs
4. Results returned to calling repo

**Example**:
```yaml
jobs:
  ci:
    uses: hannesmitterer/LexAmoris/.github/workflows/ci-template.yml@main
    with:
      node-version: '18'
```

### 2. Repository Dispatch

**Protocol**: GitHub API `repository_dispatch`

**Payload**:
```json
{
  "event_type": "lexamoris-update",
  "client_payload": {
    "source_repo": "hannesmitterer/LexAmoris",
    "source_sha": "abc123...",
    "source_ref": "refs/heads/main",
    "commit_message": "...",
    "triggered_at": "2026-01-13T..."
  }
}
```

**Flow**:
1. LexAmoris sends dispatch event
2. Target repo receives event
3. Target repo triggers rebuild/redeploy

### 3. Git-based Sync

**Protocol**: Direct Git operations

**Flow**:
1. Clone target repository
2. Create sync branch
3. Copy files
4. Commit changes
5. Push and create PR

## Shared Resources

### Docker Templates

**Location**: `shared-modules/docker/`

**Files**:
- `Dockerfile.template` - Multi-stage build template
- `docker-compose.template.yml` - Local development setup

**Usage**: Copy and customize for each project

### Configuration Files

**Location**: `shared-modules/config/`

**Files**:
- `.eslintrc.json` - JavaScript linting
- `.prettierrc.json` - Code formatting
- `pyproject.toml` - Python tools config

**Usage**: Copy to project root, customize as needed

### Scripts

**Location**: `shared-modules/scripts/`

**Files**:
- `sync-docs.sh` - Manual documentation sync

**Usage**: Execute from LexAmoris root

## Security Considerations

### 1. GitHub Token Permissions

Workflows use `GITHUB_TOKEN` with limited permissions:
- Read: All repositories
- Write: Only within workflow execution

### 2. Secrets Management

Sensitive data (Docker credentials) stored as GitHub Secrets:
- Never committed to code
- Accessed only in workflow context

### 3. Repository Access

Sync operations require:
- Write access to target repositories
- Proper GitHub token scopes

## Scalability

### Adding New Repositories

1. **Update sync-docs.yml**:
   ```yaml
   default: 'existing-repos,new-repo'
   ```

2. **Update trigger-builds.yml**:
   ```yaml
   default: 'existing-repos,new-repo'
   ```

3. **Configure new repo**:
   - Add CI workflow using template
   - Add repository_dispatch handler
   - Test sync and triggers

### Removing Repositories

1. Remove from sync/trigger lists
2. No other changes needed
3. Existing repos continue working

## Best Practices

### For Central Repository Maintainers

1. **Test workflow changes** in fork before merging
2. **Version workflows** with tags for stability
3. **Document breaking changes** in release notes
4. **Maintain backward compatibility** when possible

### For Dependent Repository Maintainers

1. **Pin workflow versions** for stability:
   ```yaml
   uses: hannesmitterer/LexAmoris/.github/workflows/ci-template.yml@v1.0.0
   ```

2. **Review sync PRs** before merging
3. **Handle dispatch events** gracefully
4. **Report issues** to LexAmoris repo

## Monitoring & Observability

### Workflow Runs

Monitor via GitHub Actions tab:
- Check success/failure rates
- Review execution logs
- Identify bottlenecks

### Sync Status

Track documentation sync:
- Check PR creation
- Verify file updates
- Monitor merge status

### Build Triggers

Verify trigger delivery:
- Check dispatch event logs
- Confirm rebuilds occur
- Monitor deployment status

## Future Enhancements

Potential improvements:

1. **Automated version bumping** across ecosystem
2. **Dependency update automation** (Dependabot style)
3. **Integrated testing** across multiple repos
4. **Automated changelog generation**
5. **Cross-repo issue tracking**
6. **Unified monitoring dashboard**

## Support & Resources

- **Main Documentation**: [README.md](README.md)
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **Partner Info**: [README_PARTNERS.md](README_PARTNERS.md)

---

**Lex Amoris Signature**: Protection of the Law of Love active 📜⚖️❤️
