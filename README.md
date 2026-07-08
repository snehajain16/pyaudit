# pyaudit

A unified Python CLI tool that combines code linting and static security analysis — Flake8, Pylint, and Bandit — into a single command with actionable, structured output and GitHub Actions integration.

## Features

- Style checks via **Flake8** (PEP8)
- Code quality analysis via **Pylint**
- Security vulnerability detection via **Bandit**
- Terminal output (colored, grouped by tool) and JSON output
- GitHub Check Run annotations on pull requests
- Selective tool execution with `--only`

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Audit a directory
pyaudit src/

# Audit a single file
pyaudit mymodule.py

# Run only security checks
pyaudit src/ --only bandit

# Output as JSON
pyaudit src/ --format json

# Use a custom tool config
pyaudit src/ --config .flake8

# Check version
pyaudit --version
```

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | No issues found |
| `1` | Issues found |
| `2` | Tool error (missing tool, timeout, etc.) |

## JSON Output Schema

```json
{
  "summary": {
    "total_issues": 3,
    "by_tool": { "flake8": 1, "pylint": 1, "bandit": 1 },
    "passed": false
  },
  "results": {
    "flake8": [{ "file": "...", "line": 10, "col": 4, "code": "E302", "message": "..." }],
    "pylint": [{ "file": "...", "line": 22, "message_id": "C0114", "symbol": "...", "message": "..." }],
    "bandit": [{ "file": "...", "line": 45, "severity": "HIGH", "confidence": "HIGH", "issue": "...", "cwe": "CWE-78" }]
  }
}
```

## GitHub Actions

Add to your repo by referencing the included workflow:

```yaml
# .github/workflows/pyaudit.yml is already included
# It runs on every push and pull_request, posting results as Check Run annotations.
```

Requires `GITHUB_TOKEN` (automatically provided by GitHub Actions) and `checks: write` permission.

## Running Tests

```bash
pip install -e ".[dev]"

# Unit tests
pytest tests/ -m "not integration"

# All tests including integration
pytest tests/
```

## Tech Stack

Python · Flake8 · Pylint · Bandit · GitHub API
