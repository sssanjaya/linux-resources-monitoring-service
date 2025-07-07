# Pre-commit Setup and Git Best Practices

This document explains the pre-commit hooks setup and git best practices for the Linux Resources Monitoring Service project.

## 🚀 Quick Setup

```bash
# Install and configure pre-commit hooks
./scripts/setup-pre-commit.sh
```

## 📋 What's Included

### Code Quality Tools

| Tool | Purpose | Configuration |
|------|---------|---------------|
| **Black** | Code formatting | 88 character line length, Python 3.8+ |
| **isort** | Import sorting | Black-compatible profile |
| **flake8** | Linting | 88 character line length, Black-compatible |
| **mypy** | Type checking | Strict mode, psutil types included |
| **pylint** | Advanced linting | Disabled overly strict rules |
| **bandit** | Security scanning | Excludes tests and virtual environments |
| **pydocstyle** | Docstring formatting | Google convention |

### Git Workflow Tools

| Tool | Purpose | Configuration |
|------|---------|---------------|
| **pre-commit** | Hook management | Runs on commit and push |
| **commitizen** | Commit message formatting | Conventional commits |
| **pytest** | Test execution | Runs on push |

## 🔧 Installation

### Prerequisites

```bash
# Ensure you're in a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Setup Pre-commit Hooks

```bash
# Run the automated setup script
./scripts/setup-pre-commit.sh
```

This script will:
1. ✅ Install all development dependencies
2. ✅ Install pre-commit hooks
3. ✅ Configure commit-msg hook for conventional commits
4. ✅ Run initial formatting on all files

## 📝 Git Workflow

### 1. Making Changes

```bash
# Create a feature branch
git checkout -b feature/add-new-metric

# Make your changes
# ... edit files ...

# Stage changes
git add .

# Commit with conventional commit message
git commit -m "feat: add disk I/O monitoring"
```

### 2. Pre-commit Hooks Run Automatically

When you commit, the following hooks run:

1. **Code Formatting**: Black and isort format your code
2. **Linting**: flake8 and pylint check for issues
3. **Type Checking**: mypy validates type annotations
4. **Security**: bandit scans for security issues
5. **Documentation**: pydocstyle checks docstrings
6. **Git Checks**: Various git hygiene checks

### 3. Commit Message Format

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

#### Examples

```bash
git commit -m "feat: add CPU temperature monitoring"
git commit -m "fix: resolve memory leak in metric collection"
git commit -m "docs: update README with setup instructions"
git commit -m "test: add unit tests for alerting module"
git commit -m "refactor: extract HTTP client to separate class"
```

### 4. Push and Test Execution

```bash
# Push your changes
git push origin feature/add-new-metric
```

On push, pytest runs automatically to ensure tests pass.

## 🛠️ Manual Commands

### Run All Hooks

```bash
# Run on staged files only
pre-commit run

# Run on all files
pre-commit run --all-files
```

### Run Specific Hooks

```bash
# Format code only
pre-commit run black --all-files

# Lint only
pre-commit run flake8 --all-files

# Type check only
pre-commit run mypy --all-files

# Security scan only
pre-commit run bandit --all-files
```

### Skip Hooks (Emergency Only)

```bash
# Skip all hooks (not recommended)
git commit -m "feat: add feature" --no-verify

# Skip specific hook
SKIP=flake8 git commit -m "feat: add feature"
```

## 📊 Configuration Files

### `.pre-commit-config.yaml`

Main configuration file defining all hooks and their settings.

### `pyproject.toml`

Tool-specific configurations:
- Black formatting settings
- isort import sorting
- mypy type checking
- pytest test configuration
- commitizen commit message rules

### `requirements.txt`

Development dependencies for all code quality tools.

## 🔍 Troubleshooting

### Common Issues

#### Hook Fails on Commit

```bash
# Check what failed
pre-commit run --all-files

# Fix formatting issues
pre-commit run black --all-files
pre-commit run isort --all-files

# Fix linting issues
pre-commit run flake8 --all-files
```

#### Type Checking Errors

```bash
# Run mypy with more details
mypy monitor_service/ --show-error-codes

# Add type ignores if needed
# type: ignore[import-untyped]
```

#### Security Issues

```bash
# View detailed security report
bandit -r . -f json -o bandit-report.json
cat bandit-report.json | jq '.'
```

### Updating Hooks

```bash
# Update all hooks to latest versions
pre-commit autoupdate

# Update specific hook
pre-commit autoupdate --freeze
```

## 🎯 Best Practices

### 1. Code Quality

- ✅ Write type hints for all functions
- ✅ Add docstrings using Google convention
- ✅ Keep functions small and focused
- ✅ Use meaningful variable names
- ✅ Handle exceptions appropriately

### 2. Git Workflow

- ✅ Use conventional commit messages
- ✅ Make small, focused commits
- ✅ Write descriptive commit messages
- ✅ Test before committing
- ✅ Never commit with `--no-verify`

### 3. Development Process

- ✅ Create feature branches for new work
- ✅ Run tests locally before pushing
- ✅ Review your own code before committing
- ✅ Keep dependencies up to date
- ✅ Document complex logic

## 📚 Additional Resources

- [Pre-commit Documentation](https://pre-commit.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Black Code Style](https://black.readthedocs.io/)
- [mypy Type Checking](https://mypy.readthedocs.io/)
- [Bandit Security](https://bandit.readthedocs.io/)

## 🔄 Continuous Integration

The pre-commit hooks are designed to work with CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run pre-commit
  uses: pre-commit/action@v3.0.0
  with:
    extra_args: --all-files
```

This ensures code quality is maintained across all environments.
