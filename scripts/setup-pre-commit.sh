#!/bin/bash

# Setup script for pre-commit hooks
# This script installs and configures pre-commit hooks for the project

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the project root
if [[ ! -f "requirements.txt" ]] || [[ ! -f "pyproject.toml" ]]; then
    log_error "This script must be run from the project root directory"
    exit 1
fi

log_info "Setting up pre-commit hooks for Linux Resources Monitoring Service"

# Check if we're in a virtual environment
if [[ "${VIRTUAL_ENV:-}" == "" ]]; then
    log_warn "Not in a virtual environment. Consider activating one first:"
    echo "  python -m venv venv && source venv/bin/activate"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Setup cancelled"
        exit 0
    fi
fi

# Check if Python is available
if ! command -v python &> /dev/null; then
    log_error "Python is not installed or not in PATH"
    exit 1
fi

# Check if pip is available
if ! command -v pip &> /dev/null; then
    log_error "pip is not installed or not in PATH"
    exit 1
fi

# Install development dependencies
log_info "Installing development dependencies..."
if ! pip install -r requirements.txt; then
    log_error "Failed to install dependencies"
    exit 1
fi

# Check if pre-commit is available
if ! command -v pre-commit &> /dev/null; then
    log_error "pre-commit is not installed. Please install it first:"
    echo "  pip install pre-commit"
    exit 1
fi

# Install pre-commit hooks
log_info "Installing pre-commit hooks..."
if ! pre-commit install; then
    log_error "Failed to install pre-commit hooks"
    exit 1
fi

if ! pre-commit install --hook-type commit-msg; then
    log_error "Failed to install commit-msg hook"
    exit 1
fi

# Run pre-commit on all files to ensure everything is formatted
log_info "Running pre-commit on all files..."
if ! pre-commit run --all-files; then
    log_warn "Pre-commit found issues. Please fix them and run again:"
    echo "  pre-commit run --all-files"
fi

log_info "Pre-commit setup complete!"
echo
echo "Available commands:"
echo "  pre-commit run                    # Run hooks on staged files"
echo "  pre-commit run --all-files        # Run hooks on all files"
echo "  pre-commit run black --all-files  # Run only black formatter"
echo "  pre-commit run flake8 --all-files # Run only flake8 linter"
echo
echo "Git workflow:"
echo "  1. Make your changes"
echo "  2. git add ."
echo "  3. git commit -m 'feat: your commit message'  # Hooks run automatically"
echo "  4. git push  # Tests run automatically"
