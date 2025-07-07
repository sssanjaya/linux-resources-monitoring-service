# Linux Resources Monitoring Service

A simple, reliable Python service for monitoring Linux system resources (CPU, memory, disk) with easy configuration, robust logging, and production-ready deployment options.

## Features
- Collects CPU, memory, and disk metrics
- Configurable collection interval and alert thresholds
- Structured JSON logging for easy troubleshooting
- Robust error handling and retries
- Ready for systemd and Docker deployment
- Simple to install, run, and extend

## Quick Start

### Prerequisites
- Python 3.8+
- Linux OS (for system metrics)

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd linux-resources-monitoring-service

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration
Edit `config.yaml` to set:
- Metrics collection interval (seconds)
- Cloud endpoint & API key (for future use)
- Alert thresholds for CPU, memory, and disk

Example:
```yaml
metrics:
  interval: 10
cloud:
  endpoint: "http://localhost:8000/api/metrics"
  api_key: "dev-local-key"
alerting:
  cpu_threshold: 90
  memory_threshold: 80
  disk_threshold: 80
```

### Running the Service
```bash
# Print metrics once
python -m monitor_service.metric_collector

# Run periodic monitoring (edit the script to enable)
# or use systemd/docker for background operation
```

### More
- [Systemd & Docker Deployment](docs/DEPLOYMENT.md)
- [Configuration Details](docs/CONFIG.md)
- [Development & Testing](docs/DEVELOPMENT.md)
- [Reliability & Observability](docs/RELIABILITY.md)

---

For advanced usage, troubleshooting, and contribution guidelines, see the [docs/](docs/) folder.
