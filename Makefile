.PHONY: install test lint format clean docs build publish

install:
	pip install -e ".[dev,docs]"
	pre-commit install

test:
	pytest tests/ -v --cov=gomoku_world --cov-report=term-missing

lint:
	flake8 src/gomoku_world tests
	pylint src/gomoku_world tests
	mypy src/gomoku_world tests

format:
	black src/gomoku_world tests
	isort src/gomoku_world tests

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf htmlcov/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docs:
	cd docs && make html

build:
	python -m build

publish:
	python -m twine upload dist/*

run-server:
	python src/run_server.py

run-client:
	python src/run_game.py

dev-setup: install
	pre-commit install
	pip install -r requirements-dev.txt 