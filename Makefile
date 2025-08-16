.PHONY: help install install-dev test test-cov lint format clean build publish version-bump version-patch version-minor version-major

help: ## Show this help message
	@echo "Turkish Tokenizer - Development Commands"
	@echo "========================================"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package in development mode
	pip install -e .

install-dev: ## Install the package with development dependencies
	pip install -e ".[dev]"

test: ## Run tests
	python -m pytest tests/ -v

test-cov: ## Run tests with coverage report
	python -m pytest tests/ -v --cov=turkish_tokenizer --cov-report=term-missing --cov-report=html

test-fast: ## Run tests without slow tests
	python -m pytest tests/ -v -m "not slow"

lint: ## Run linting checks
	flake8 turkish_tokenizer/ tests/ scripts/
	mypy turkish_tokenizer/ scripts/

format: ## Format code with black
	black turkish_tokenizer/ tests/ scripts/

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .coverage
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: ## Build the package
	python -m build

publish: ## Build and publish to PyPI
	$(MAKE) clean
	$(MAKE) build
	twine check dist/*
	twine upload dist/*

version-current: ## Show current version
	python scripts/version_manager.py current

version-bump: ## Bump patch version (0.1.9 -> 0.1.10)
	python scripts/version_manager.py bump patch

version-minor: ## Bump minor version (0.1.9 -> 0.2.0)
	python scripts/version_manager.py bump minor

version-major: ## Bump major version (0.1.9 -> 1.0.0)
	python scripts/version_manager.py bump major

version-set: ## Set version to specific value (usage: make version-set VERSION=1.0.0)
	python scripts/version_manager.py set $(VERSION)

check: ## Run all checks (lint, test, format)
	$(MAKE) lint
	$(MAKE) test
	$(MAKE) format

dev-setup: ## Set up development environment
	$(MAKE) install-dev
	$(MAKE) version-current

ci: ## Run CI checks (lint, test, build)
	$(MAKE) lint
	$(MAKE) test-cov
	$(MAKE) build
