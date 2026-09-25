.PHONY: bootstrap check doctor down format help lint logs run test typecheck up

VENV := .venv
PYTHON := $(VENV)/bin/python
RUFF := $(VENV)/bin/ruff
MYPY := $(VENV)/bin/mypy
PYTEST := $(VENV)/bin/pytest
UVICORN := $(VENV)/bin/uvicorn

help:
	@printf '%s\n' \
		'make bootstrap  Create .venv, install dependencies, and prepare .env' \
		'make doctor     Check required local commands and files' \
		'make run        Start the FastAPI development server' \
		'make check      Run lint, formatting, types, and tests' \
		'make format     Apply Ruff formatting and safe fixes' \
		'make up         Start the Docker Compose stack' \
		'make down       Stop the Docker Compose stack' \
		'make logs       Follow Docker Compose logs'

bootstrap:
	bash scripts/bootstrap.sh

doctor:
	$(PYTHON) scripts/doctor.py

run:
	$(UVICORN) restaurant_agent.main:app --reload

lint:
	$(RUFF) check .
	$(RUFF) format --check .

typecheck:
	$(MYPY) src scripts

test:
	$(PYTEST)

check: lint typecheck test

format:
	$(RUFF) check --fix .
	$(RUFF) format .

up:
	@test -f .env || (printf '%s\n' 'Missing .env. Run make bootstrap first.' && exit 1)
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs --follow
