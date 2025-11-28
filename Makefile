.PHONY: help install test clean lint format run-cli run-ui benchmark docs

help:
	@echo "Rubik's Cube Solver - Available Commands"
	@echo "========================================"
	@echo ""
	@echo "Setup:"
	@echo "  make install          Install dependencies"
	@echo "  make install-kociemba Install with Kociemba solver"
	@echo ""
	@echo "Running:"
	@echo "  make run-cli          Run CLI solver"
	@echo "  make run-ui           Run Flask web UI"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test             Run unit tests"
	@echo "  make test-cov         Run tests with coverage"
	@echo "  make lint             Run linting"
	@echo "  make format           Format code with black"
	@echo ""
	@echo "Tools:"
	@echo "  make benchmark        Run solver benchmark"
	@echo "  make scan             Run cube color scanner"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean            Remove build artifacts"
	@echo "  make clean-all        Remove all generated files"

install:
	pip install -r requirements.txt

install-kociemba:
	pip install -r requirements.txt -r requirements-kociemba.txt

test:
	python -m pytest tests/ -v

test-cov:
	python -m pytest tests/ -v --cov=cube --cov=solvers --cov-report=html

lint:
	python -m flake8 cube solvers cli tools python tests --max-line-length=100
	python -m mypy cube solvers cli tools --ignore-missing-imports

format:
	python -m black cube solvers cli tools python tests ui

run-cli:
	python cli/cli.py -h

run-ui:
	python ui/app.py

benchmark:
	python tools/benchmark.py --solvers ida --trials 3 --depths 5 8 10

scan:
	python python/scan.py examples/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ *.egg-info/
	rm -f .coverage htmlcov

clean-all: clean
	rm -f solution.json scan_result.json benchmark_results.json

.DEFAULT_GOAL := help
