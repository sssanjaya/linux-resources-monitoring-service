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
git
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
│   ├── __init__.py          # Test package initialization 🔄
│   └── test_metric_collector.py # Metric collection tests 🔄
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

### Running the Metric Collector

```bash
# Run the metric collector directly
python -c "
from monitor_service.metric_collector import MetricCollector
collector = MetricCollector()
metrics = collector.collect_all_metrics()
print('Collected metrics:', metrics)
"

# Or run with continuous monitoring
python -c "
from monitor_service.metric_collector import MetricCollector
import time

collector = MetricCollector()
try:
    while True:
        metrics = collector.collect_all_metrics()
        print(f'[{time.strftime(\"%H:%M:%S\")}] {metrics}')
        time.sleep(60)  # Collect every minute
except KeyboardInterrupt:
    print('\\nMonitoring stopped.')
"
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=monitor_service --cov-report=html

# Run specific test file
python -m pytest tests/test_metric_collector.py -v
```

### Test Structure

```
tests/
├── __init__.py              # Test package initialization 🔄
└── test_metric_collector.py # Metric collection tests 🔄
```

### Test Categories

#### Unit Tests (Planned)
- **Metric Collection**: CPU, memory, disk metric accuracy
- **HTTP Client**: Retry logic, error handling, circuit breakers
- **Alerting**: Threshold evaluation, cooldown logic
- **Configuration**: YAML parsing, validation, environment overrides

#### Integration Tests (Planned)
- **End-to-End**: Complete metric collection and sending flow
- **API Integration**: FastAPI endpoint testing
- **Database**: InfluxDB connection and data persistence

#### Performance Tests (Planned)
- **Load Testing**: High-frequency metric collection
- **Memory Usage**: Long-running service stability
- **Network Resilience**: Connection failure scenarios

### Code Quality & Testing

```bash
# Run all tests with coverage
pytest tests/ --cov=monitor_service --cov-report=html

# Run pre-commit hooks (includes tests)
pre-commit run --all-files

# Run specific quality checks
black monitor_service/          # Code formatting
flake8 monitor_service/         # Linting
mypy monitor_service/           # Type checking
bandit -r monitor_service/      # Security scanning
```

### Test Examples (Planned)

```python
# Example test for metric collection
def test_cpu_metrics_collection():
    collector = MetricCollector()
    metrics = collector.collect_cpu_metrics()

    assert 'cpu_usage' in metrics
    assert 0 <= metrics['cpu_usage'] <= 100
    assert 'cpu_count' in metrics
    assert metrics['cpu_count'] > 0

# Example test for alerting
def test_alert_threshold_evaluation():
    alert_manager = AlertManager(config)
    metrics = {'cpu_percent': 85}

    alerts = alert_manager.evaluate_metrics(metrics)
    assert len(alerts) > 0
    assert alerts[0]['metric'] == 'cpu_percent'
```

## 📊 Metrics Collected

### CPU Metrics ✅
- Overall CPU utilization percentage
- Per-core CPU utilization
- CPU count and frequency

### Memory Metrics ✅
- Total, used, and free memory
- Memory utilization percentage
- Swap usage statistics

### Disk Metrics ✅
- Per filesystem usage
- Total, used, and free space
- Disk utilization percentage

### System Metrics ✅
- Hostname and timestamp
- System uptime
- Load average

## 🔔 Alerting (Planned)

The service will include intelligent alerting with:

- **Configurable thresholds** for CPU, memory, and disk
- **Cooldown periods** to prevent alert storms
- **Multiple channels**: logs, email, Slack (configurable)
- **Alert history** and deduplication

## 🎯 Code Quality Standards

This project follows strict code quality standards enforced by pre-commit hooks:

- **Code Formatting**: Black (88 character line length)
- **Import Sorting**: isort (Black-compatible)
- **Linting**: flake8 and pylint
- **Type Checking**: mypy (strict mode)
- **Security**: bandit vulnerability scanning
- **Documentation**: pydocstyle (Google convention)
- **Git Hygiene**: Various git best practices
- **Testing**: pytest runs on every push

See [docs/PRE_COMMIT_SETUP.md](docs/PRE_COMMIT_SETUP.md) for detailed setup instructions.

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

# 2. Make changes and ensure code quality
pre-commit run --all-files

# 3. Commit with conventional commit message
git commit -m "feat: add new monitoring capability"

# 4. Push (tests run automatically)
git push origin feature/add-new-metric
```

**Note**: Pre-commit hooks run automatically on commit and push to ensure code quality.

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
| **Testing** | Unit tests with instructions | ✅ pytest framework setup, pre-commit integration, comprehensive tests planned |
| **Deployment** | Reproducible setup (systemd/Docker) | 🔄 systemd service definition created, implementation in progress |

## 🤝 Contributing

This is a learning project demonstrating SRE/DevOps best practices. Each component is built step-by-step with:

- Clear separation of concerns
- Production-ready error handling
- Comprehensive logging and monitoring
- Automated testing and deployment
- Strict code quality standards with pre-commit hooks

### Development Standards

- **Code Style**: Black formatting, isort imports, flake8 linting
- **Type Safety**: mypy type checking with strict mode
- **Security**: bandit vulnerability scanning
- **Documentation**: Google-style docstrings with pydocstyle
- **Testing**: pytest with coverage reporting
- **Git Workflow**: Conventional commit messages with commitizen

## 📄 License

This project is created for educational purposes as part of an SRE take-home assignment.
