## Project type
Python package.

## Repository layout
- `src/` or the package folder: library code
- `tests/`: pytest tests, one file per module

## Setup and commands
- Install (editable, with test extras): `pip install -e ".[test]"`
- Test: `pytest -q`
- Single test: `pytest -q tests/test_x.py -k name`
- Lint/format: `ruff check . && ruff format --check .`

## Code rules
- Support the minimum Python version in `pyproject.toml`; do not use newer syntax.
- Public functions get type hints and a one-line docstring.
- Keep I/O at the edges; core functions take and return plain data.
