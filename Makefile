SCRIPT       = a_maze_ing.py
DEFAULT_CONF = config_standard.txt

.PHONY: all install run debug clean lint lint-strict

all: run

install:
	poetry install

run:
	poetry run python $(SCRIPT) $(DEFAULT_CONF)

debug:
	poetry run python -m pdb $(SCRIPT) $(DEFAULT_CONF)

test:
	poetry run python -m pytest tests/ -v
clean:
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf mazegen/__pycache__
	rm -rf .mypy_cache
	rm -rf .pytest_cache

lint:
	poetry run flake8 .
	poetry run mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	poetry run flake8 .
	poetry run mypy --strict .

