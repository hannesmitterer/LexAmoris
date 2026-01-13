#!/bin/bash

# LexAmoris Deployment Initialization Script
# This script prepares the project for deployment and performs basic validation

set -e  # Exit on error

echo "🚀 LexAmoris Deployment Initialization"
echo "======================================="
echo ""

# Check if index.html exists
if [ ! -f "index.html" ]; then
    echo "❌ Error: index.html not found!"
    exit 1
fi

echo "✅ index.html found"

# Validate HTML structure (basic check)
if grep -q "<!DOCTYPE html>" index.html && grep -q "</html>" index.html; then
    echo "✅ HTML structure appears valid"
else
    echo "⚠️  Warning: HTML structure may be incomplete"
fi

# Check for required files
echo ""
echo "Checking project files..."
files=("LICENSE" "README.md" "mission.md" "render.yaml")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file found"
    else
        echo "⚠️  Warning: $file not found"
    fi
done

# Check render.yaml syntax (basic YAML validation)
echo ""
echo "Validating render.yaml..."
if command -v python3 &> /dev/null; then
    python3 -c "import yaml; yaml.safe_load(open('render.yaml'))" 2>/dev/null && \
        echo "✅ render.yaml syntax is valid" || \
        echo "⚠️  Warning: render.yaml may have syntax issues"
else
    echo "ℹ️  Python3 not available, skipping YAML validation"
fi

# Display deployment information
echo ""
echo "📊 Deployment Information:"
echo "  Project: LexAmoris (Nexus Martinique)"
echo "  Type: Static Website"
echo "  Entry Point: index.html"
echo "  Deployment Platform: Render.com (or any static host)"
echo ""

# Create a deployment timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "⏰ Deployment prepared at: $TIMESTAMP"

echo ""
echo "✨ Deployment initialization complete!"
echo "💚 Ready to deploy - Lex Amoris Signature: Protection of the Law of Love active."
echo ""
