.PHONY: venv install run test test-health test-health-endpoints lint format docker-build docker-run clean docker-compose-up docker-compose-down grafana-import fastapi-server help dev stop

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


# Run the FastAPI ingestion server
fastapi-server:
	venv/bin/uvicorn monitor_service.cloud_ingestion:app --host 0.0.0.0 --port 8080

# Clean up build/test artifacts
clean:
	rm -rf venv .pytest_cache __pycache__ monitor_service/__pycache__ tests/__pycache__ *.pyc *.pyo *.coverage htmlcov

# Run all services for local development
dev:
	@echo "Starting local development environment..."
	@make docker-compose-up
	@make fastapi-server &
	@make run

# Stop all app services (Docker Compose and local)
stop:
	@echo "Stopping all app services..."
	-docker-compose down
	-pkill -f monitor_service.cloud_ingestion || true
	-pkill -f monitor_service.metric_collector || true
