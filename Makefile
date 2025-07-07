.PHONY: venv install run test lint format docker-build docker-run clean

venv:
	python3 -m venv venv

install:
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt

run:
	venv/bin/python -m monitor_service.metric_collector

test:
	venv/bin/python -m pytest tests/

lint:
	venv/bin/flake8 monitor_service/

format:
	venv/bin/black monitor_service/

docker-build:
	docker build -t linux-resources-monitoring-service .

docker-run:
	docker run --rm linux-resources-monitoring-service

clean:
	rm -rf venv .pytest_cache __pycache__ monitor_service/__pycache__ tests/__pycache__ *.pyc *.pyo *.coverage htmlcov
