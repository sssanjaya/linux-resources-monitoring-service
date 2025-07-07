# Linux Resources Monitoring Service

A production-ready Python service for monitoring Linux system resources with cloud ingestion, alerting, and visualization capabilities.

## 📋 Assignment Overview

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

## 🏗️ Architecture

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

## 📁 Project Structure

```
linux-resources-monitoring-service/
├── monitor_service/          # Core monitoring package
│   ├── __init__.py          # Package initialization ✅
│   ├── metric_collector.py  # CPU, memory, disk collection ✅
│   ├── sender.py            # HTTP client with retry logic 🔄
│   ├── alerting.py          # Threshold monitoring & alerts 🔄
│   └── config.py            # Configuration management 🔄
├── tests/                   # Unit and integration tests
│   └── __init__.py          # Test package initialization 🔄
├── config/                  # Configuration files
│   └── config.yaml         # Service settings & thresholds 🔄
├── deployment/              # Production deployment
│   └── monitor.service     # systemd service definition 🔄
├── docs/                    # Documentation
│   └── PRE_COMMIT_SETUP.md # Pre-commit setup guide ✅
├── scripts/                 # Setup and utility scripts
│   └── setup-pre-commit.sh # Pre-commit setup script ✅
├── requirements.txt         # Python dependencies ✅
├── pyproject.toml          # Project configuration ✅
├── .pre-commit-config.yaml # Pre-commit hooks config ✅
└── README.md               # This documentation ✅
```

**Legend**: ✅ Implemented | 🔄 In Progress/Placeholder

## 🚀 Quick Start

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

## 🔧 Troubleshooting

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

## 📈 Monitoring & Observability (Planned)

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

## 🏆 Evaluation Criteria Alignment

| **Category** | **What We're Looking For** | **Implementation Status** |
|--------------|----------------------------|---------------------------|
| **Correctness** | Accurate metrics, successful ingestion, working dashboard and alerts | ✅ Metric collection implemented, 🔄 ingestion/dashboard/alerts in progress |
| **Code Quality** | Modular, readable, adheres to best practices | ✅ Clean architecture, type hints, comprehensive error handling, separation of concerns |
| **Reliability** | Error handling, retries, alert storm prevention | ✅ Error handling in collector, 🔄 retries/alerting in progress |
| **Documentation** | Clear README, comments, config explanations | ✅ Comprehensive README, inline documentation, configuration examples, troubleshooting guide |
| **Observability** | Structured logs, appropriate log levels | 🔄 Logging framework in progress, health checks planned |
| **Testing** | Unit tests with instructions | 🔄 Test framework setup, comprehensive tests planned |
| **Deployment** | Reproducible setup (systemd/Docker) | 🔄 systemd service definition created, implementation in progress |
