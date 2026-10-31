# Makefile for A-Maze-ing project

PYTHON = python3
SCRIPT = a_maze_ing.py
CONFIG = config.txt

install:
	pip install flake8 mypy pytest build types-setuptools

run:
	$(PYTHON) $(SCRIPT) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(SCRIPT) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .mypy_cache .pytest_cache dist build *.egg-info

lint:
	flake8 . --exclude=./venv
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 . --exclude=./venv
	mypy . --strict

.PHONY: install run debug clean lint lint-strict