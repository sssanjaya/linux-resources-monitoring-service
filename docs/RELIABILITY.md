# Reliability & Observability

## Error Handling & Retries
- Metric collection is retried up to 3 times on error.
- Errors and max retries are logged.
- The service continues running after errors.

## Structured Logging
- All logs are JSON with UTC timestamps, log level, and event type.
- Example log:
  ```json
  {
    "timestamp": "2024-07-07T12:34:56.789012+00:00",
    "level": "INFO",
    "event": "metrics_collected",
    "cpu": {...},
    "memory": {...},
    "disk": {...}
  }
  ```
- Logs are suitable for ingestion by log aggregators (ELK, Datadog, etc).

## Unit Tests
- Tests cover metric collection, error handling, and retry logic.
- To run tests:
  ```bash
  make test
  ```

## Tips
- Check logs for `collection_error` and `metrics_collected` events.
- For more, see the code in `monitor_service/metric_collector.py` and `tests/`.
