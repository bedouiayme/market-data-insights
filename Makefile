.PHONY: install run test lint docker-up docker-down

install:
	python -m pip install --upgrade pip
	python -m pip install ".[dev]"

run:
	uvicorn market_data_insights_api.main:app --reload

test:
	pytest

lint:
	ruff check .

docker-up:
	docker compose up --build

docker-down:
	docker compose down
