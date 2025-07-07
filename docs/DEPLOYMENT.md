# Deployment: Systemd, Docker & Kubernetes

## Systemd Service (Production)

1. Copy `deployment/monitor.service` to `/etc/systemd/system/monitor.service`:
   ```bash
   sudo cp deployment/monitor.service /etc/systemd/system/monitor.service
   ```
2. Edit the `User`, `WorkingDirectory`, and `ExecStart` fields in the service file to match your environment.
3. Reload systemd and start the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable monitor
   sudo systemctl start monitor
   sudo systemctl status monitor
   ```

### Health Monitoring with Systemd
Systemd can monitor the service health using the built-in health check:

```bash
# Check service health
sudo systemctl is-active monitor
sudo systemctl is-failed monitor

# View recent logs
sudo journalctl -u monitor -f

# Restart on failure (add to service file)
Restart=always
RestartSec=10
```

## Docker (Local Development & Testing)

### Metric Collector
1. Build the Docker image:
   ```bash
   docker build -t monitor-app .
   ```
2. Run the container:
   ```bash
   docker run --rm monitor-app
   ```

### API Server with Health Checks
1. Build the image (if not already done):
   ```bash
   docker build -t monitor-app .
   ```
2. Run the API server with health check:
   ```bash
   docker run --rm -p 8000:8000 \
     --health-cmd="curl -f http://localhost:8000/health || exit 1" \
     --health-interval=30s \
     --health-timeout=10s \
     --health-retries=3 \
     monitor-app python -m monitor_service.cloud_ingestion
   ```

### Docker Compose with Health Checks
Create a `docker-compose.api.yml` for the API server:

```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    command: python -m monitor_service.cloud_ingestion
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    environment:
      - PYTHONUNBUFFERED=1
```

## Kubernetes Deployment

### API Server Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: monitoring-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: monitoring-api
  template:
    metadata:
      labels:
        app: monitoring-api
    spec:
      containers:
      - name: api
        image: monitor-app:latest
        ports:
        - containerPort: 8000
        command: ["python", "-m", "monitor_service.cloud_ingestion"]
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
```

### Service Configuration
```yaml
apiVersion: v1
kind: Service
metadata:
  name: monitoring-api-service
spec:
  selector:
    app: monitoring-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

### Ingress Configuration (Optional)
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: monitoring-api-ingress
  annotations:
    nginx.ingress.kubernetes.io/health-check-path: /health
spec:
  rules:
  - host: monitoring-api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: monitoring-api-service
            port:
              number: 80
```

## Cloud Ingestion Endpoint (Docker)

To run the FastAPI ingestion server in Docker:

1. Build the image (if not already done):
   ```bash
   docker build -t monitor-app .
   ```
2. Run the ingestion server:
   ```bash
   docker run --rm -p 8000:8000 monitor-app python -m monitor_service.cloud_ingestion
   ```
3. In another terminal, run the collector:
   ```bash
   docker run --rm monitor-app
   ```
4. The ingestion server will log received metrics from the collector.

### Testing Health Endpoints
```bash
# Test health endpoints
curl http://localhost:8000/health
curl http://localhost:8000/health/ready
curl http://localhost:8000/health/live
curl http://localhost:8000/health/detailed

# Or use the Makefile
make test-health-endpoints
```

## InfluxDB + Grafana (Production-Grade Dashboard)

### 1. Start InfluxDB and Grafana

```bash
docker-compose up -d
```
- InfluxDB: http://localhost:8086 (user: admin, pass: admin123, org: demo-org, bucket: metrics, token: demo-token)
- Grafana: http://localhost:3000 (user: admin, pass: admin)

### 2. Configure the Collector
- Set the `influxdb` section in `config.yaml` to match the docker-compose values.
- Run the collector as usual. Metrics will be written to InfluxDB.

### 3. Configure Grafana
- Add InfluxDB as a data source (URL: `http://influxdb:8086`, token: `demo-token`, org: `demo-org`).
- Import the dashboard from `docs/grafana_dashboard.json`.

### 4. Monitor API Health in Grafana
Create additional dashboard panels to monitor API health:

```sql
-- API uptime
from(bucket: "metrics")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "api_health")
  |> filter(fn: (r) => r._field == "uptime")

-- API response time
from(bucket: "metrics")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "api_health")
  |> filter(fn: (r) => r._field == "response_time")
```

## Load Balancer Configuration

### Nginx Configuration
```nginx
upstream monitoring_api {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name monitoring-api.example.com;

    location / {
        proxy_pass http://monitoring_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /health {
        proxy_pass http://monitoring_api/health;
        access_log off;
    }
}
```

### HAProxy Configuration
```haproxy
frontend monitoring_api
    bind *:80
    default_backend monitoring_api_backend

backend monitoring_api_backend
    balance roundrobin
    option httpchk GET /health
    http-check expect status 200
    server api1 127.0.0.1:8000 check
    server api2 127.0.0.1:8001 check
```

## Monitoring Integration

### Prometheus Configuration
```yaml
scrape_configs:
  - job_name: 'monitoring-api'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: /health/detailed
    scrape_interval: 30s
```

### Alerting Rules
```yaml
groups:
  - name: monitoring-api
    rules:
      - alert: APIDown
        expr: up{job="monitoring-api"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Monitoring API is down"
          description: "The monitoring API has been down for more than 1 minute"

      - alert: APIHighResponseTime
        expr: http_request_duration_seconds{job="monitoring-api"} > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High API response time"
          description: "API response time is above 2 seconds"
```

## Troubleshooting

### Health Check Issues
```bash
# Check if API is responding
curl -v http://localhost:8000/health

# Check detailed health
curl http://localhost:8000/health/detailed | jq .

# Check logs
docker logs <container-id>
sudo journalctl -u monitor -f
```

### Common Issues
- **Health check failing**: Ensure the API server is running and accessible
- **Port conflicts**: Check if port 8000 is already in use
- **Permission issues**: Ensure proper file permissions for config files
- **Network issues**: Verify network connectivity for external dependencies

### Debug Mode
Run the API server in debug mode for more verbose logging:

```bash
uvicorn monitor_service.cloud_ingestion:app --host 0.0.0.0 --port 8000 --log-level debug
```

For more detailed troubleshooting, see [docs/RELIABILITY.md](RELIABILITY.md).
