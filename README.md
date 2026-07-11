# Market Data Insights API

Market Data Insights API is a Python portfolio project focused on finance, data engineering, FastAPI, Docker, CI/CD, and cloud readiness.

Sprint 1 delivers the foundation:

- FastAPI application skeleton
- `/health` endpoint
- central configuration with environment variables
- professional `src/` package layout
- PostgreSQL service with Docker Compose
- automated tests with pytest
- lint configuration with Ruff
- CI workflow with GitHub Actions

## Why This Architecture

This project uses a `src/` layout so the application code is separated from project configuration, tests, Docker files, and documentation.

The importable Python package is named `market_data_insights_api`, which is more explicit than a generic package name like `app`.

The code is split into layers:

- `api`: HTTP routes exposed by FastAPI
- `core`: application configuration and shared runtime settings
- `db`: database connection and persistence setup
- `models`: SQLAlchemy database models
- `schemas`: Pydantic request and response schemas
- `services`: business logic
- `ingestion`: market data ingestion workflows
- `utils`: small shared helpers

FastAPI is used because it is a modern Python web framework with strong typing, automatic OpenAPI documentation, and excellent test ergonomics.

PostgreSQL is used because financial data is structured, relational, and often queried by asset, timestamp, and metric. It is also a realistic production database for fintech and data engineering systems.

Docker Compose is used for local development because it lets the API and database run together in a reproducible environment.

Pytest is used because it is the standard testing tool in modern Python projects and scales well from unit tests to integration tests.

GitHub Actions is included from the beginning to show a production-minded CI/CD workflow: every change can be linted and tested automatically.

## Project Structure

```text
market-data-insights-api/
|-- src/
|   `-- market_data_insights_api/
|       |-- __init__.py
|       |-- main.py
|       |-- api/
|       |   `-- routes/
|       |       `-- health.py
|       |-- core/
|       |   `-- config.py
|       |-- db/
|       |-- ingestion/
|       |-- models/
|       |-- schemas/
|       |-- services/
|       `-- utils/
|-- tests/
|   |-- test_config.py
|   `-- test_health.py
|-- .github/
|   `-- workflows/
|       `-- ci.yml
|-- Dockerfile
|-- docker-compose.yml
|-- pyproject.toml
|-- Makefile
`-- README.md
```

## Requirements

- Python 3.12+
- Docker and Docker Compose

## Local Setup

Create and activate a virtual environment, then install the project:

```bash
python -m venv .venv
python -m pip install --upgrade pip
python -m pip install ".[dev]"
```

Run the API locally:

```bash
uvicorn market_data_insights_api.main:app --reload
```

Open:

- API: <http://localhost:8000>
- Health check: <http://localhost:8000/health>
- OpenAPI docs: <http://localhost:8000/docs>

## Run With Docker

Start the API and PostgreSQL:

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

PostgreSQL will be available locally on port `5432`.

Default local database settings:

```text
POSTGRES_USER=market_user
POSTGRES_PASSWORD=market_password
POSTGRES_DB=market_data
```

## Configuration

Configuration is managed through environment variables.

Copy `.env.example` to `.env` for local overrides:

```bash
cp .env.example .env
```

Supported variables:

| Variable | Purpose |
| --- | --- |
| `ENVIRONMENT` | Runtime environment name, for example `local`, `test`, or `prod` |
| `DATABASE_URL` | PostgreSQL connection string used by the application |

## Tests

Run tests:

```bash
pytest
```

Run linting:

```bash
ruff check .
```

## Current API

### `GET /health`

Returns the current service status.

Example response:

```json
{
  "status": "ok",
  "service": "Market Data Insights API",
  "version": "0.1.0",
  "environment": "local"
}
```

## Next Sprints

Sprint 2 should add:

- database models for assets and prices
- Alembic migrations
- external market data ingestion
- first read endpoints for assets and prices

Sprint 3 should add:

- financial indicators such as returns, moving averages, volatility, and drawdown
- integration tests with PostgreSQL
- richer API documentation

Sprint 4 should add:

- Docker image publication
- AWS deployment path using ECR, ECS Fargate, RDS, and CloudWatch
- scheduled ingestion jobs with EventBridge
