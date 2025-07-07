# Linux Resources Monitoring Service

A production-ready Python service for monitoring Linux system resources with cloud ingestion, alerting, and visualization capabilities.

## Assignment Overview

**Site Reliability Engineer Take-Home Assignment**

This project demonstrates SRE/DevOps best practices by building a lightweight Linux monitoring service that:

- ✅ **Metric Collection**: Gathers CPU, memory, and disk metrics using psutil
- ✅ **Code Quality**: Pre-commit hooks with Black, flake8, mypy, bandit, and more
- ✅ **Testing Framework**: pytest setup with coverage reporting
- ✅ **Documentation**: Comprehensive README and setup guides
- 🔄 **Cloud Ingestion**: HTTP client with retry logic (in progress)
- 🔄 **Alerting**: Threshold-based alerts with cooldown prevention (in progress)
- 🔄 **Production Ready**: systemd service with structured logging (in progress)
- 🔄 **Observability**: Health checks, metrics, and comprehensive logging (in progress)

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Linux System  │    │  Monitor Service│    │  Cloud Endpoint │
│                 │    │                 │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │   psutil    │ │◄───┤ │  Collector  │ │───►│ │   FastAPI   │ │
│ │  (CPU/Mem/  │ │    │ │             │ │    │ │  Endpoint   │ │
│ │   Disk)     │ │    │ └─────────────┘ │    │ └─────────────┘ │
│ └─────────────┘ │    │ ┌─────────────┐ │    └─────────────────┘
│                 │    │ │   Sender    │ │
│                 │    │ │ (HTTP/Retry)│ │    ┌─────────────────┐
│                 │    │ └─────────────┘ │    │   Dashboard     │
│                 │    │ ┌─────────────┐ │    │  (Plotly Dash)  │
│                 │    │ │  Alerting   │ │    │                 │
│                 │    │ │(Thresholds) │ │    └─────────────────┘
│                 │    │ └─────────────┘ │
│                 │    └─────────────────┘
└─────────────────┘
```

## Project Structure

A well-organized folder structure is crucial for code quality, readability, maintainability, testability, and reproducible deployment. Python organizes code primarily through modules and packages:

- **Modules**: Single Python files (e.g., `my_module.py`) containing variables, classes, or functions. Modules promote reusability and separation of concerns.
- **Packages**: Folders containing modules, made recognizable to Python by the presence of an `__init__.py` file. Packages allow for hierarchical organization and better abstraction as projects grow.

**Example Structure for SRE Assignment:**

```
linux-resources-monitoring-service/
├── .gitignore             # To ignore 'venv/', '__pycache__/', etc.
├── .dockerignore          # Docker build context exclusions
├── Dockerfile             # Docker image for local dev/testing
├── README.md              # Setup, usage, assumptions
├── requirements.txt       # Project dependencies
├── config.yaml            # Service configuration (metrics, endpoints, thresholds)
├── setup.py               # For packaging and distribution
├── monitor_service/
│   ├── __init__.py        # Makes it a Python package
│   ├── metric_collector.py # Gathers system metrics (CPU, Memory, Disk)
│   ├── cloud_ingestion.py  # Flask/FastAPI endpoint to receive metrics
│   ├── alerts.py          # Alerting logic with cooldown
│   └── utils.py           # Helper functions (e.g., for structured logging)
├── tests/
│   ├── __init__.py
│   └── test_metrics.py    # Unit tests for metric collection (add as needed)
├── deploy/                # Optional: For systemd service file, Dockerfile etc.
│   └── sre_monitor.service # Systemd service file
├── docs/                  # Documentation (e.g., pre-commit setup)
│   └── PRE_COMMIT_SETUP.md
├── scripts/               # Setup and utility scripts
│   └── setup-pre-commit.sh
└── venv/                  # Virtual environment (ignored by Git)
```

*Note: Some files may be placeholders for future implementation.*

**Key Points:**
- The `monitor_service/` directory is a Python package (contains `__init__.py`) and holds all core logic.
- Configuration, deployment, and documentation are separated for clarity and maintainability.
- Tests are isolated in their own directory for easy discovery and execution.
- The use of a virtual environment (`venv/`) is recommended for dependency isolation and reproducibility.

**Why this structure?**
This layout ensures clear separation of concerns, making your project easier to develop, debug, and deploy. It aligns with expert SRE and Python best practices, supporting code quality, maintainability, and reproducible deployment.

## Quick Start

### Prerequisites

- **Python**: 3.8 or higher
- **OS**: Linux (for system metrics)
- **Dependencies**: psutil, pytest, pytest-cov, pre-commit tools

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd linux-resources-monitoring-service

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup pre-commit hooks (recommended)
./scripts/setup-pre-commit.sh
```

## 🛠️ Development

### Code Quality & Pre-commit Hooks

We use pre-commit hooks to ensure code quality and consistency. See [docs/PRE_COMMIT_SETUP.md](docs/PRE_COMMIT_SETUP.md) for detailed information.

```bash
# Quick setup
./scripts/setup-pre-commit.sh

# Manual code quality checks
pre-commit run --all-files

# Run specific tools
black monitor_service/          # Code formatting
isort monitor_service/          # Import sorting
flake8 monitor_service/         # Linting
mypy monitor_service/           # Type checking
bandit -r monitor_service/      # Security scanning
pylint monitor_service/         # Advanced linting
pydocstyle monitor_service/     # Docstring formatting
```

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/add-new-metric

# Make changes and commit with conventional commit message
git add .
git commit -m "feat: add new monitoring capability"

# Push (tests run automatically)
git push origin feature/add-new-metric
```

### Adding New Metrics

1. Extend `MetricCollector` class in `monitor_service/metric_collector.py`
2. Add corresponding tests in `tests/test_metric_collector.py`
3. Update configuration schema in `monitor_service/config.py`

### Adding New Alert Rules

1. Define rules in `config/config.yaml`
2. Implement evaluation logic in `monitor_service/alerting.py`
3. Add tests for new alert conditions

### Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/add-new-metric

# 2. Make changes
# ... edit files ...

# 3. Stage and commit (hooks run automatically)
git add .
git commit -m "feat: add new monitoring capability"

# 4. Push
git push origin feature/add-new-metric
```

## Troubleshooting

### Common Issues

**Service won't start:**
```bash
# Check systemd logs (when service is implemented)
sudo journalctl -u monitor -n 50

# Check configuration (when config validation is implemented)
python -m monitor_service --validate-config
```

**Metrics not being sent:**
```bash
# Test endpoint connectivity (when sender is implemented)
curl -X POST http://localhost:8000/metrics \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'

# Check network connectivity
ping your-endpoint.com
```

**High resource usage:**
```bash
# Check service resource usage
ps aux | grep monitor_service
top -p $(pgrep -f monitor_service)
```

### Log Analysis

```bash
# View real-time logs (when logging is implemented)
sudo journalctl -u monitor -f

# Search for errors (when logging is implemented)
sudo journalctl -u monitor | grep ERROR

# Export logs for analysis (when logging is implemented)
sudo journalctl -u monitor --since "1 hour ago" > monitor.log
```

## Monitoring & Observability (Planned)

### Health Checks

```bash
# Service health (when implemented)
curl http://localhost:8080/health

# Metrics endpoint (when implemented)
curl http://localhost:8080/metrics
```

### Key Metrics (Planned)

- **Collection success rate**: Percentage of successful metric collections
- **Send success rate**: Percentage of successful metric transmissions
- **Alert frequency**: Number of alerts triggered per time period
- **Service uptime**: Service availability percentage

## Evaluation Criteria Alignment

| **Category** | **What We're Looking For** | **Implementation Status** |
|--------------|----------------------------|---------------------------|
| **Correctness** | Accurate metrics, successful ingestion, working dashboard and alerts | ✅ Metric collection implemented, 🔄 ingestion/dashboard/alerts in progress |
| **Code Quality** | Modular, readable, adheres to best practices | ✅ Clean architecture, type hints, comprehensive error handling, separation of concerns |
| **Reliability** | Error handling, retries, alert storm prevention | ✅ Error handling in collector, 🔄 retries/alerting in progress |
| **Documentation** | Clear README, comments, config explanations | ✅ Comprehensive README, inline documentation, configuration examples, troubleshooting guide |
| **Observability** | Structured logs, appropriate log levels | 🔄 Logging framework in progress, health checks planned |
| **Testing** | Unit tests with instructions | 🔄 Test framework setup, comprehensive tests planned |
| **Deployment** | Reproducible setup (systemd/Docker) | 🔄 systemd service definition created, implementation in progress |

## 🚀 Deployment & Local Development

### Running as a systemd Service (Production)

1. Copy `deploy/sre_monitor.service` to `/etc/systemd/system/sre_monitor.service`.
2. Edit the `User`, `WorkingDirectory`, and `ExecStart` fields as needed.
3. Reload systemd and start the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable sre_monitor
   sudo systemctl start sre_monitor
   sudo systemctl status sre_monitor
   ```

### Running with Docker (Local Development & Testing)

1. Build the Docker image:
   ```bash
   docker build -t linux-resources-monitoring-service .
   ```
2. Run the container:
   ```bash
   docker run --rm linux-resources-monitoring-service
   ```

*The Dockerfile uses Python 3.10 and runs the monitor service as the default command.*

## 🛠️ Makefile Commands

For easier development and testing, use the provided Makefile:

- `make venv`           – Create a Python virtual environment
- `make install`        – Install dependencies into the venv
- `make run`            – Run the monitor service locally
- `make test`           – Run all tests
- `make lint`           – Run flake8 linter
- `make format`         – Format code with Black
- `make docker-build`   – Build the Docker image
- `make docker-run`     – Run the Docker container
- `make clean`          – Remove venv, caches, and build artifacts

Example usage:
```bash
make venv
make install
make run
```
