dev:
	uv sync --all-groups
	pre-commit install

test:
	uv run pytest --cov=src

.PHONY: dev test
