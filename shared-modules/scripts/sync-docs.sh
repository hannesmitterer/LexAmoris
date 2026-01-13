#!/bin/bash
# LexAmoris Ecosystem - Manual Documentation Sync Script
# Use this script to manually synchronize documentation across repositories

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
SOURCE_REPO="hannesmitterer/LexAmoris"
DEFAULT_REPOS="hannesmitterer/nexus,hannesmitterer/Resonance-,hannesmitterer/euystacio-helmi-ai"
DEFAULT_FILES="README_PARTNERS.md,mission.md"

# Parse arguments
TARGET_REPOS="${1:-$DEFAULT_REPOS}"
SYNC_FILES="${2:-$DEFAULT_FILES}"

echo -e "${GREEN}LexAmoris Documentation Sync${NC}"
echo "=============================="
echo "Source: $SOURCE_REPO"
echo "Targets: $TARGET_REPOS"
echo "Files: $SYNC_FILES"
echo ""

# Check if we're in the LexAmoris repository
if [ ! -f "README_PARTNERS.md" ] && [ ! -f "mission.md" ]; then
    echo -e "${RED}Error: This script must be run from the LexAmoris repository root${NC}"
    exit 1
fi

# Create temporary directory for clones
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

echo -e "${YELLOW}Using temporary directory: $TEMP_DIR${NC}"
echo ""

# Split repos and files into arrays
IFS=',' read -ra REPOS <<< "$TARGET_REPOS"
IFS=',' read -ra FILES <<< "$SYNC_FILES"

# Process each repository
for repo in "${REPOS[@]}"; do
    echo -e "${GREEN}Processing: $repo${NC}"
    
    repo_name=$(echo "$repo" | cut -d'/' -f2)
    clone_dir="$TEMP_DIR/$repo_name"
    
    # Clone repository
    if ! git clone "https://github.com/${repo}.git" "$clone_dir" 2>/dev/null; then
        echo -e "${RED}Failed to clone $repo. Skipping...${NC}"
        echo ""
        continue
    fi
    
    cd "$clone_dir"
    
    # Create sync branch
    branch_name="sync/docs-from-lexamoris-$(date +%Y%m%d-%H%M%S)"
    git checkout -b "$branch_name"
    
    # Copy files
    files_updated=false
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd ../.. && pwd)"
    for file in "${FILES[@]}"; do
        source_file="$SCRIPT_DIR/$file"
        if [ -f "$source_file" ]; then
            echo "  Copying $file..."
            mkdir -p "$(dirname "$file")"
            cp "$source_file" "$file"
            git add "$file"
            files_updated=true
        else
            echo -e "  ${YELLOW}Warning: $file not found in source${NC}"
        fi
    done
    
    # Commit changes
    if [ "$files_updated" = true ] && ! git diff --cached --quiet; then
        git commit -m "docs: sync documentation from LexAmoris

Auto-synced files: $SYNC_FILES

This update is part of the LexAmoris ecosystem synchronization."
        
        echo -e "  ${GREEN}✓ Changes committed to branch $branch_name${NC}"
        echo "  To push: cd $clone_dir && git push origin $branch_name"
    else
        echo "  No changes detected"
    fi
    
    cd - > /dev/null
    echo ""
done

echo -e "${GREEN}Sync complete!${NC}"
echo ""
echo "Review the changes in $TEMP_DIR"
echo "Push branches and create PRs manually if needed."
