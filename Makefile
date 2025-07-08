.PHONY: venv install run test test-health test-health-endpoints lint format docker-build docker-run clean docker-compose-up docker-compose-down grafana-import fastapi-server help dev

# Create Python virtual environment
venv:
	python3 -m venv venv

# Install Python dependencies
install:
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt

# Run the metric collector
run:
	venv/bin/python -m monitor_service.metric_collector

# Run all tests
test:
	venv/bin/python -m pytest tests/

# Run health check tests specifically
test-health:
	venv/bin/python -m pytest tests/cloud_ingestion_test.py::test_health_check tests/cloud_ingestion_test.py::test_readiness_check tests/cloud_ingestion_test.py::test_liveness_check tests/cloud_ingestion_test.py::test_detailed_health_check -v

# Lint code
lint:
	venv/bin/flake8 monitor_service/

# Format code
format:
	venv/bin/black monitor_service/

# Build Docker image for the collector
docker-build:
	docker build -t monitor-app .

# Run the collector Docker image
# (Assumes InfluxDB/Grafana are running via docker-compose)
docker-run:
	docker run --rm monitor-app

# Start InfluxDB and Grafana via docker-compose
docker-compose-up:
	docker-compose up -d

# Stop InfluxDB and Grafana
docker-compose-down:
	docker-compose down

# Import Grafana dashboard (requires Grafana running and API key)
# Usage: make grafana-import GRAFANA_URL=... API_KEY=...
grafana-import:
	@echo "Importing Grafana dashboard..."
	@curl -X POST \
	  -H "Content-Type: application/json" \
	  -H "Authorization: Bearer $(API_KEY)" \
	  -d @docs/grafana_dashboard.json \
	  $(GRAFANA_URL)/api/dashboards/db || echo "See docs/DEPLOYMENT.md for manual import instructions."

# Run the FastAPI ingestion server
fastapi-server:
	venv/bin/uvicorn monitor_service.cloud_ingestion:app --host 0.0.0.0 --port 8080

# Test health endpoints (requires server running)
test-health-endpoints:
	@echo "Testing health endpoints..."
	@curl -s http://localhost:8000/health | jq . || echo "Health endpoint test failed"
	@curl -s http://localhost:8000/health/ready | jq . || echo "Readiness endpoint test failed"
	@curl -s http://localhost:8000/health/live | jq . || echo "Liveness endpoint test failed"
	@curl -s http://localhost:8000/health/detailed | jq . || echo "Detailed health endpoint test failed"

# Clean up build/test artifacts
clean:
	rm -rf venv .pytest_cache __pycache__ monitor_service/__pycache__ tests/__pycache__ *.pyc *.pyo *.coverage htmlcov

# Show help for all targets
help:
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:' Makefile | cut -d: -f1 | sort | uniq | xargs -n1 echo '  -'

# Run all services for local development
dev:
	@echo "Starting local development environment..."
	@make docker-compose-up
	@make fastapi-server &
	@make run
