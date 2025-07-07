# API Documentation

The Linux Resources Monitoring Service provides a RESTful API for ingesting system metrics and monitoring service health.

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, the API uses a simple API key authentication via the `x-api-key` header for the metrics endpoint.

## Endpoints

### Health Checks

#### GET /health
Basic health check endpoint that returns service status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "uptime": 3600.5
}
```

**Use Cases:**
- Load balancer health checks
- Basic service monitoring
- Simple uptime verification

#### GET /health/ready
Readiness check endpoint for Kubernetes and container orchestration.

**Response:**
```json
{
  "status": "ready",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "uptime": 3600.5
}
```

**Use Cases:**
- Kubernetes readiness probes
- Service mesh health checks
- Container orchestration platforms

#### GET /health/live
Liveness check endpoint for service monitoring.

**Response:**
```json
{
  "status": "alive",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "uptime": 3600.5
}
```

**Use Cases:**
- Kubernetes liveness probes
- Service monitoring systems
- Process health verification

#### GET /health/detailed
Comprehensive health check with system metrics and information.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "uptime": 3600.5,
  "system_info": {
    "hostname": "server-01",
    "platform": "Linux",
    "release": "5.15.0-generic",
    "version": "#1 SMP Ubuntu 5.15.0-56-generic",
    "machine": "x86_64",
    "cpu_count": 8,
    "cpu_percent": 25.5
  },
  "memory_usage": {
    "total_gb": 16.0,
    "available_gb": 8.5,
    "used_gb": 7.5,
    "percent": 46.9
  },
  "disk_usage": {
    "total_gb": 500.0,
    "used_gb": 200.0,
    "free_gb": 300.0,
    "percent": 40.0
  }
}
```

**Use Cases:**
- Comprehensive system monitoring
- Detailed health diagnostics
- Performance analysis

### Metrics Ingestion

#### POST /api/metrics
Receive system metrics from collectors.

**Headers:**
```
Content-Type: application/json
x-api-key: your-api-key
```

**Request Body:**
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "hostname": "server-01",
  "metrics": {
    "cpu": {
      "cpu_usage": 25.5,
      "cpu_count": 8,
      "per_core_usage": [20.1, 30.2, 25.3, 22.4, 28.5, 26.6, 24.7, 27.8]
    },
    "memory": {
      "total_gb": 16.0,
      "used_gb": 7.5,
      "free_gb": 8.5,
      "percent": 46.9
    },
    "disk": {
      "/": {
        "total_gb": 500.0,
        "used_gb": 200.0,
        "free_gb": 300.0,
        "percent": 40.0
      },
      "/home": {
        "total_gb": 100.0,
        "used_gb": 50.0,
        "free_gb": 50.0,
        "percent": 50.0
      }
    }
  }
}
```

**Response:**
```json
{
  "status": "ok",
  "received_at": "2024-01-15T10:30:01Z",
  "hostname": "server-01"
}
```

**Error Responses:**
- `400 Bad Request` - Invalid payload format
- `401 Unauthorized` - Missing or invalid API key
- `500 Internal Server Error` - Server processing error

### API Information

#### GET /
Root endpoint providing API overview and available endpoints.

**Response:**
```json
{
  "message": "Linux Resources Monitoring API",
  "version": "1.0.0",
  "endpoints": {
    "health": "/health",
    "readiness": "/health/ready",
    "liveness": "/health/live",
    "detailed_health": "/health/detailed",
    "metrics": "/api/metrics",
    "docs": "/docs"
  }
}
```

#### GET /docs
Interactive API documentation using Swagger UI.

## Testing the API

### Using curl

#### Health Checks
```bash
# Basic health check
curl http://localhost:8000/health

# Readiness check
curl http://localhost:8000/health/ready

# Liveness check
curl http://localhost:8000/health/live

# Detailed health check
curl http://localhost:8000/health/detailed
```

#### Metrics Ingestion
```bash
# Send metrics
curl -X POST http://localhost:8000/api/metrics \
  -H "Content-Type: application/json" \
  -H "x-api-key: your-api-key" \
  -d '{
    "timestamp": "2024-01-15T10:30:00Z",
    "hostname": "test-server",
    "metrics": {
      "cpu": {"cpu_usage": 25.5, "cpu_count": 4, "per_core_usage": [20, 30, 25, 22]},
      "memory": {"total_gb": 8.0, "used_gb": 4.0, "free_gb": 4.0, "percent": 50.0},
      "disk": {"/": {"total_gb": 100.0, "used_gb": 50.0, "free_gb": 50.0, "percent": 50.0}}
    }
  }'
```

### Using Makefile
```bash
# Test health endpoints
make test-health-endpoints

# Run health check tests
make test-health
```

## Error Handling

The API uses standard HTTP status codes:

- `200 OK` - Successful request
- `400 Bad Request` - Invalid request format
- `401 Unauthorized` - Authentication required
- `404 Not Found` - Endpoint not found
- `500 Internal Server Error` - Server error

All error responses include a JSON body with error details:

```json
{
  "detail": "Error description"
}
```

## Rate Limiting

Currently, no rate limiting is implemented. For production deployments, consider implementing rate limiting based on your requirements.

## Logging

The API uses structured JSON logging with the following fields:
- `timestamp` - UTC ISO timestamp
- `level` - Log level (INFO, WARNING, ERROR)
- `message` - Log message
- `event` - Event type for structured logging
- Additional context fields as needed

## Production Considerations

### Health Check Configuration

For Kubernetes deployment, configure health checks:

```yaml
livenessProbe:
  httpGet:
    path: /health/live
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /health/ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
```

### Load Balancer Configuration

Configure load balancer health checks to use `/health` endpoint:

```yaml
healthCheck:
  path: /health
  port: 8000
  interval: 30s
  timeout: 5s
  healthyThreshold: 2
  unhealthyThreshold: 3
```

### Monitoring Integration

The health endpoints can be integrated with monitoring systems like:
- Prometheus (via custom metrics)
- Nagios/Icinga
- Datadog
- New Relic
- Custom monitoring solutions
