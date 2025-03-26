dev:
	uv sync --all-groups
	pre-commit install

lint:
	uv run ruff check .

test:
	uv run pytest --cov=fixtures.main

.PHONY: dev test
