# Tasks: PyAudit CLI

## Phase 1: Project Setup
- [x] Initialize Python package structure (`pyaudit/`, `tests/`, `pyproject.toml`)
- [x] Add dependencies: `flake8`, `pylint`, `bandit`, `requests`
- [x] Configure entry point in `pyproject.toml` (`pyaudit = "pyaudit.cli:main"`)
- [x] Set up `.gitignore`, `README.md`

## Phase 2: Core Runners & Parsers
- [x] Implement `runner.py` — subprocess execution with timeout and error handling
- [x] Implement `parsers/flake8.py` — parse flake8 line output via regex
- [x] Implement `parsers/pylint.py` — parse pylint text output
- [x] Implement `parsers/bandit.py` — parse bandit `-f json` output

## Phase 3: CLI & Reporter
- [x] Implement `cli.py` — argparse setup, orchestration, exit codes
- [x] Implement `reporter.py` — terminal formatter (colored, grouped by tool)
- [x] Implement `reporter.py` — JSON formatter matching output schema

## Phase 4: GitHub Integration
- [x] Implement `github.py` — post results as GitHub Check Run annotations
- [x] Create `.github/workflows/pyaudit.yml`

## Phase 5: Tests
- [x] Write fixture Python files (clean, style errors, quality issues, security vulns)
- [x] Write `test_parsers.py` for each parser
- [x] Write `test_runner.py` for subprocess runner
- [x] Write `test_reporter.py` for both output formats
- [x] Write integration test: full `pyaudit` run on fixture directory

## Phase 6: Polish
- [x] Add `--version` flag
- [x] Add `--config` flag for custom tool config paths
- [x] Write full `README.md` with usage examples
- [ ] Publish to PyPI (optional)
