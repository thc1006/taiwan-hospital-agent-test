.PHONY: bootstrap dev test lint demo render

bootstrap:
	python -m venv .venv && source .venv/bin/activate && pip install -U pip && pip install fastapi uvicorn boto3 pydantic pytest graphviz

dev:
	uvicorn services.api.main:app --reload --port 8000

test:
	pytest -q

lint:
	@echo "Add linting commands (e.g. ruff, mypy) here"

demo:
	bash scripts/local_demo.sh

render:
	python scripts/render_arch.py