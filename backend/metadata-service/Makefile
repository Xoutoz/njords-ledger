-include .devcontainer/.env

APP=$(APP_NAME)
CONFIG_PATH=pyproject.toml
POETRY=poetry

setup:
	$(POETRY) install

run_app:
	$(POETRY) run metadata_service

unit_test:
	$(POETRY) run pytest tests/