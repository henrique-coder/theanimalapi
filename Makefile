PYTHON ?= python3
VENV := .venv

.PHONY: lint format help
.DEFAULT_GOAL := help

lint:
	ruff check

format:
	ruff format

help:
	@echo "Available commands:"
	@echo "  lint        - Check code with ruff"
	@echo "  format      - Format code with ruff"
	@echo "  help        - Show this help message"
