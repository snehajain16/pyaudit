# Design: PyAudit CLI

## Architecture

```
pyaudit/
├── pyaudit/
│   ├── __init__.py
│   ├── cli.py          # Entry point — argument parsing, orchestration
│   ├── runner.py       # Runs each tool as subprocess, captures output
│   ├── parsers/
│   │   ├── flake8.py   # Parses flake8 stdout
│   │   ├── pylint.py   # Parses pylint stdout/JSON
│   │   └── bandit.py   # Parses bandit JSON output
│   ├── reporter.py     # Formats aggregated results (terminal + JSON)
│   └── github.py       # GitHub API client for posting check annotations
├── tests/
│   ├── fixtures/       # Sample Python files for testing
│   ├── test_parsers.py
│   ├── test_runner.py
│   └── test_reporter.py
├── .github/
│   └── workflows/
│       └── pyaudit.yml
├── setup.py / pyproject.toml
└── README.md
```

## JSON Output Schema

```json
{
  "summary": {
    "total_issues": 12,
    "by_tool": {
      "flake8": 5,
      "pylint": 4,
      "bandit": 3
    },
    "passed": false
  },
  "results": {
    "flake8": [
      {
        "file": "src/foo.py",
        "line": 10,
        "col": 4,
        "code": "E302",
        "message": "expected 2 blank lines, found 1"
      }
    ],
    "pylint": [
      {
        "file": "src/foo.py",
        "line": 22,
        "message_id": "C0114",
        "symbol": "missing-module-docstring",
        "message": "Missing module docstring"
      }
    ],
    "bandit": [
      {
        "file": "src/foo.py",
        "line": 45,
        "severity": "HIGH",
        "confidence": "HIGH",
        "issue": "Use of subprocess with shell=True",
        "cwe": "CWE-78"
      }
    ]
  }
}
```

## CLI Interface

```
usage: pyaudit [-h] [--only {flake8,pylint,bandit}] [--format {terminal,json}] path

positional arguments:
  path                  File or directory to audit

options:
  --only TOOL           Run only the specified tool
  --format FORMAT       Output format: terminal (default) or json
  -h, --help            Show help
```

## GitHub Actions Integration

The workflow triggers on `push` and `pull_request`. It:
1. Installs `pyaudit` and its dependencies
2. Runs `pyaudit` with `--format json`
3. Uses the GitHub Checks API to post annotations on the PR diff

## Key Design Decisions

- **Subprocess-based runners**: Invoke tools as subprocesses rather than importing their Python APIs. This avoids version coupling and keeps each tool independently upgradable.
- **Bandit JSON mode**: Bandit is always invoked with `-f json` for reliable parsing. Flake8 and Pylint output is parsed via regex.
- **Exit codes**: Mirrors `grep` convention — 0 = clean, 1 = issues found, 2 = tool/config error.
