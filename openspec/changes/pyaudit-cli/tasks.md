# Tasks: PyAudit CLI

## Phase 1: Project Setup
- [ ] Initialize Python package structure (`pyaudit/`, `tests/`, `pyproject.toml`)
- [ ] Add dependencies: `flake8`, `pylint`, `bandit`, `requests`
- [ ] Configure entry point in `pyproject.toml` (`pyaudit = "pyaudit.cli:main"`)
- [ ] Set up `.gitignore`, `README.md`

## Phase 2: Core Runners & Parsers
- [ ] Implement `runner.py` — subprocess execution with timeout and error handling
- [ ] Implement `parsers/flake8.py` — parse flake8 line output via regex
- [ ] Implement `parsers/pylint.py` — parse pylint text output
- [ ] Implement `parsers/bandit.py` — parse bandit `-f json` output

## Phase 3: CLI & Reporter
- [ ] Implement `cli.py` — argparse setup, orchestration, exit codes
- [ ] Implement `reporter.py` — terminal formatter (colored, grouped by tool)
- [ ] Implement `reporter.py` — JSON formatter matching output schema

## Phase 4: GitHub Integration
- [ ] Implement `github.py` — post results as GitHub Check Run annotations
- [ ] Create `.github/workflows/pyaudit.yml`

## Phase 5: Tests
- [ ] Write fixture Python files (clean, style errors, quality issues, security vulns)
- [ ] Write `test_parsers.py` for each parser
- [ ] Write `test_runner.py` for subprocess runner
- [ ] Write `test_reporter.py` for both output formats
- [ ] Write integration test: full `pyaudit` run on fixture directory

## Phase 6: Polish
- [ ] Add `--version` flag
- [ ] Add `--config` flag for custom tool config paths
- [ ] Write full `README.md` with usage examples
- [ ] Publish to PyPI (optional)
