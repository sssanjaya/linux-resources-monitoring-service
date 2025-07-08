# Linux Resources Monitoring Service

A production-ready Python service for monitoring Linux system resources (CPU, memory, disk) with comprehensive health checks, structured logging, and easy deployment options.

## Features
- **System Metrics Collection**: CPU, memory, and disk usage monitoring
- **Health Check Endpoints**: Comprehensive API health monitoring for production deployment
- **Configurable Collection**: Adjustable intervals and alert thresholds
- **Structured JSON Logging**: Easy troubleshooting and log aggregation
- **Robust Error Handling**: Retries and graceful failure handling
- **Production Ready**: Systemd and Docker deployment support
- **InfluxDB Integration**: Time-series data storage for metrics
- **Grafana Dashboard**: Ready-to-use visualization templates

## Quick Start

### Prerequisites
- Python 3.8+
- Linux OS (for system metrics)
- Docker & Docker Compose (for InfluxDB/Grafana)

**Note**: The project uses a minimal set of dependencies for better maintainability and security.

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd linux-resources-monitoring-service

# Create and activate a virtual environment
make venv
source venv/bin/activate

# Install dependencies
make install
```

### Configuration
Edit `config.yaml` to set:
- Metrics collection interval (seconds)
- Cloud endpoint & API key
- Alert thresholds for CPU, memory, and disk
- InfluxDB connection details

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
influxdb:
  url: "http://localhost:8086"
  token: "your-influxdb-token"
  org: "your-org"
  bucket: "metrics"
```

### Running the Service

#### Using Makefile (Recommended)
```bash
# Start InfluxDB and Grafana
make docker-compose-up

# Run the metric collector
make run

# Start the API server
make fastapi-server
```

#### Manual Commands
```bash
# Print metrics once
python -m monitor_service.metric_collector

# Run periodic monitoring
python -m monitor_service.metric_collector

# Start the API server
python -m monitor_service.cloud_ingestion
```

## API Endpoints

### Health Checks
The API provides comprehensive health check endpoints for production monitoring:

- **`GET /health`** - Basic health status
- **`GET /health/ready`** - Readiness check (for container orchestration)
- **`GET /health/live`** - Liveness check (for load balancers)
- **`GET /health/detailed`** - Comprehensive system health with metrics

### Metrics Ingestion
- **`POST /api/metrics`** - Receive system metrics from collectors

### API Information
- **`GET /`** - API overview and available endpoints
- **`GET /docs`** - Interactive API documentation (Swagger UI)

### Example Health Check Response
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "uptime": 3600.5
}
```

## Testing

### Run All Tests
```bash
make test
```

### Test Health Endpoints
```bash
# Run health check tests
make test-health

# Test health endpoints manually (requires server running)
make test-health-endpoints
```

### Test API Endpoints
```bash
# Start the server
make fastapi-server

# In another terminal, test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/health/detailed
```

## Visualization with InfluxDB & Grafana

### Start the Stack
```bash
# Start InfluxDB and Grafana
make docker-compose-up

# Access Grafana at http://localhost:3000
# Username: admin, Password: admin
```

### Import Dashboard
1. Go to Grafana → Dashboards → Import
2. Upload `docs/grafana_dashboard.json`
3. Select InfluxDB as data source
4. View your metrics!

## Development

### Code Quality
```bash
# Format code
make format

# Lint code
make lint

# Run tests
make test
```

### Docker Development
```bash
# Build image
make docker-build

# Run container
make docker-run
```

## Available Makefile Targets

```bash
make help                    # Show all available targets
make venv                    # Create virtual environment
make install                 # Install dependencies
make run                     # Run metric collector
make fastapi-server          # Start API server
make test                    # Run all tests
make test-health             # Run health check tests
make test-health-endpoints   # Test health endpoints manually
make docker-compose-up       # Start InfluxDB/Grafana
make docker-compose-down     # Stop InfluxDB/Grafana
make docker-build            # Build Docker image
make docker-run              # Run Docker container
make clean                   # Clean build artifacts
```

## More Documentation
- [Systemd & Docker Deployment](docs/DEPLOYMENT.md)
- [Configuration Details](docs/CONFIG.md)
- [Development & Testing](docs/DEVELOPMENT.md)
- [Reliability & Observability](docs/RELIABILITY.md)
- [API Documentation](docs/API.md)

---

For advanced usage, troubleshooting, and contribution guidelines, see the [docs/](docs/) folder.
