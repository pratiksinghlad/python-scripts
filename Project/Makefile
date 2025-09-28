# Background Job Scheduler Makefile
# Provides common development and deployment tasks

.PHONY: help install install-dev test lint format type-check clean run migrate docker-build docker-run

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install production dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo "  test         - Run tests"
	@echo "  lint         - Run linting"
	@echo "  format       - Format code"
	@echo "  type-check   - Run type checking"
	@echo "  clean        - Clean build artifacts"
	@echo "  run          - Run the scheduler"
	@echo "  migrate      - Run database migrations"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run with Docker Compose"

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pip install -r requirements.txt

# Testing
test:
	pytest tests/ -v

test-coverage:
	pytest tests/ --cov=src/background_job_scheduler --cov-report=html --cov-report=term

# Code quality
lint:
	ruff check src/ tests/
	black --check src/ tests/
	isort --check-only src/ tests/

format:
	black src/ tests/
	isort src/ tests/
	ruff format src/ tests/

type-check:
	mypy src/

# Cleanup
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/

# Application
run:
	python run_scheduler.py

migrate:
	python -m background_job_scheduler.cli migrate

cli-help:
	python -m background_job_scheduler.cli --help

# Docker
docker-build:
	docker build -t background-job-scheduler .

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

docker-logs:
	docker-compose logs -f

# Development database (requires Docker)
dev-db-start:
	docker run -d \
		--name job-scheduler-mysql \
		-e MYSQL_ROOT_PASSWORD=password \
		-e MYSQL_DATABASE=job_scheduler \
		-p 3306:3306 \
		mysql:8.0

dev-db-stop:
	docker stop job-scheduler-mysql || true
	docker rm job-scheduler-mysql || true

# Quick setup for development
dev-setup: dev-db-start install-dev migrate
	@echo "Development environment ready!"
	@echo "Database: mysql://root:password@localhost:3306/job_scheduler"
	@echo "Run 'make run' to start the scheduler"