dev:
	uv sync --all-groups
	pre-commit install

test:
	uv run pytest --cov=fixtures.main

.PHONY: dev test
