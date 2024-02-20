-include .devcontainer/.env

APP=$(SERVICE_NAME)
CONFIG_PATH=pyproject.toml
POETRY=poetry

setup:
	$(POETRY) install --without dev

dev_setup:
	$(POETRY) install

run_app:
	$(POETRY) run metadata_service

black:
	-$(POETRY) run black .

ruff:
	-$(POETRY) run ruff .

ruff_fix:
	-$(POETRY) run ruff --fix .

vulture:
	-$(POETRY) run vulture

lint: black ruff vulture

test:
	$(POETRY) run pytest tests/ --cov

coverage:
	$(POETRY) run coverage report -m