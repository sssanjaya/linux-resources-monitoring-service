# Configuration Guide

The service is configured via `config.yaml` in the project root.

## Example config.yaml
```yaml
metrics:
  interval: 10  # seconds
cloud:
  endpoint: "http://localhost:8000/api/metrics"
  api_key: "dev-local-key"
alerting:
  cpu_threshold: 90      # percent
  memory_threshold: 80   # percent
  disk_threshold: 80     # percent
```

## Options
- **metrics.interval**: How often to collect metrics (in seconds)
- **cloud.endpoint**: URL to send metrics to (future feature)
- **cloud.api_key**: API key or credentials for the cloud endpoint
- **alerting.cpu_threshold**: CPU usage percent to trigger alert
- **alerting.memory_threshold**: Memory usage percent to trigger alert
- **alerting.disk_threshold**: Disk usage percent to trigger alert

Edit these values to match your environment and requirements.
