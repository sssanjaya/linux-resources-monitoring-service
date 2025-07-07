git # Pre-commit Setup

Simple pre-commit hooks for code quality and git best practices.

## 🚀 Quick Setup

```bash
# Install and configure pre-commit hooks
./scripts/setup-pre-commit.sh
```

## 📋 What's Included

| Tool | Purpose |
|------|---------|
| **Black** | Code formatting (88 character line length) |
| **isort** | Import sorting (Black-compatible) |
| **flake8** | Linting (88 character line length) |
| **trailing-whitespace** | Remove trailing whitespace |
| **end-of-file-fixer** | Ensure files end with newline |
| **commitizen** | Conventional commit messages |

## 🔧 Installation

```bash
# Ensure you're in a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup pre-commit hooks
./scripts/setup-pre-commit.sh
```

## 📝 Git Workflow

### 1. Make Changes
```bash
# Create feature branch
git checkout -b feature/add-new-metric

# Make your changes
# ... edit files ...

# Stage changes
git add .
```

### 2. Commit with Conventional Message
```bash
# Use conventional commit format
git commit -m "feat: add CPU temperature monitoring"
git commit -m "fix: resolve memory leak in metric collection"
git commit -m "docs: update README with setup instructions"
```

### 3. Pre-commit Hooks Run Automatically
- **Code Formatting**: Black and isort format your code
- **Linting**: flake8 checks for issues
- **Git Hygiene**: Remove trailing whitespace, fix end of files
- **Commit Message**: commitizen validates format

## 🛠️ Manual Commands

```bash
# Run all hooks on staged files
pre-commit run

# Run on all files
pre-commit run --all-files

# Run specific hooks
pre-commit run black --all-files
pre-commit run flake8 --all-files
pre-commit run isort --all-files
```

## 📝 Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <description>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples
```bash
git commit -m "feat: add CPU temperature monitoring"
git commit -m "fix: resolve memory leak in metric collection"
git commit -m "docs: update README with setup instructions"
git commit -m "test: add unit tests for alerting module"
git commit -m "refactor: extract HTTP client to separate class"
git commit -m "chore: update dependencies"
```

## 🔍 Troubleshooting

### Hook Fails on Commit
```bash
# Check what failed
pre-commit run --all-files

# Fix formatting issues
pre-commit run black --all-files
pre-commit run isort --all-files

# Fix linting issues
pre-commit run flake8 --all-files
```

### Common Issues
- **Unused imports**: Remove imports that aren't used
- **Unused variables**: Remove or use variables that are assigned but never used
- **Bare except**: Use `except Exception:` instead of just `except:`
- **Trailing whitespace**: Will be automatically fixed
- **Missing newline**: Will be automatically fixed

### Skip Hooks (Emergency Only)
```bash
# Skip all hooks (not recommended)
git commit -m "feat: add feature" --no-verify
```

## 📚 Resources

- [Pre-commit Documentation](https://pre-commit.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Black Code Style](https://black.readthedocs.io/)
