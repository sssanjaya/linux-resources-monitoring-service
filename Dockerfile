FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# By default, run the metric collector. To run the ingestion server, override CMD.
CMD ["python", "-m", "monitor_service.metric_collector"]
# To run the ingestion server:
# docker run --rm -p 8000:8000 linux-resources-monitoring-service python -m monitor_service.cloud_ingestion
