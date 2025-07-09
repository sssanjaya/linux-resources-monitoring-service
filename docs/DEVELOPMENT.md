# Development & Testing

## Setup
- Create a virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate
  ```
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Local Development

To simplify local development, a `dev` command is provided in the `Makefile`. This command will start all the necessary services in the correct order.

```bash
# Start the entire local development environment
make dev
```

## Code Quality
- Run all pre-commit hooks:
  ```bash
  ./scripts/setup-pre-commit.sh
  pre-commit run --all-files
  ```
- Lint, format, and type-check:
  ```bash
  make lint
  make format
  make test
  ```

## Running Tests
- Run all tests:
  ```bash
  make test
  ```
- Tests cover metric collection and error handling/retries.

## Adding Features
- Extend `MetricCollector` for new metrics.
- Add tests in `tests/`.
- Update `config.yaml` and docs as needed.
