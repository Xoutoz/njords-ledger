-include .devcontainer/.env

APP=$(APP_NAME)
CONFIG_PATH=pyproject.toml
POETRY=poetry

update:
	$(POETRY) lock

setup:
	$(POETRY) install

run_app:
	$(POETRY) run analytical_service

unit_test:
	$(POETRY) run pytest tests/

run:
	$(POETRY) run python3 analytics/operations.py