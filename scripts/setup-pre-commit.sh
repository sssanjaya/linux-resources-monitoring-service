#!/bin/bash

# Setup script for pre-commit hooks
# This script installs and configures pre-commit hooks for the project

set -e

echo "Setting up pre-commit hooks for Linux Resources Monitoring Service"

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo " Warning: Not in a virtual environment. Consider activating one first."
    echo " python -m venv venv && source venv/bin/activate"
fi

# Install development dependencies
echo " Installing development dependencies..."
pip install -r requirements.txt

# Install pre-commit hooks
echo " Installing pre-commit hooks..."
pre-commit install
pre-commit install --hook-type commit-msg

# Run pre-commit on all files to ensure everything is formatted
echo " Running pre-commit on all files..."
pre-commit run --all-files

echo " Pre-commit setup complete!"
echo ""
echo " Available commands:"
echo "  pre-commit run                    # Run hooks on staged files"
echo "  pre-commit run --all-files        # Run hooks on all files"
echo "  pre-commit run black --all-files  # Run only black formatter"
echo "  pre-commit run flake8 --all-files # Run only flake8 linter"
echo ""
echo " Git workflow:"
echo "  1. Make your changes"
echo "  2. git add ."
echo "  3. git commit -m 'feat: your commit message'  # Hooks run automatically"
echo "  4. git push  # Tests run automatically"
