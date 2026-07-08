# Specifications: PyAudit CLI

## Functional Requirements

### FR-1: Unified CLI Entry Point
- The tool MUST be invocable as `pyaudit <path>` where `<path>` is a file or directory
- It MUST support `--only` flag to run a subset of tools: `--only flake8`, `--only pylint`, `--only bandit`
- It MUST support `--format` flag: `terminal` (default), `json`
- It MUST return exit code `0` if no issues found, `1` if issues found, `2` on tool error

### FR-2: Flake8 Integration
- Run Flake8 against the target path
- Capture and parse output: file, line, column, error code, message
- Categorize as style violations

### FR-3: Pylint Integration
- Run Pylint against the target path
- Capture score and individual messages: file, line, message-id, symbol, message
- Categorize as code quality issues

### FR-4: Bandit Integration
- Run Bandit against the target path
- Parse JSON output: file, line, severity (LOW/MEDIUM/HIGH), confidence, issue text, CWE
- Categorize as security vulnerabilities

### FR-5: Aggregated Report
- Terminal output MUST group results by tool with clear section headers
- Terminal output MUST show a summary (counts per tool, overall pass/fail)
- JSON output MUST follow a defined schema (see design.md)

### FR-6: GitHub Actions Integration
- Provide a `.github/workflows/pyaudit.yml` that runs on push and pull_request
- Workflow MUST post results as GitHub Check annotations on PRs via GitHub API

## Non-Functional Requirements

### NFR-1: Performance
- Must complete analysis of a 1000-file project in under 60 seconds

### NFR-2: Python Version Support
- Must support Python 3.9+

### NFR-3: Dependencies
- Runtime: `flake8`, `pylint`, `bandit`, `requests`
- No other mandatory runtime dependencies

## Scenarios

### Scenario 1: Clean codebase
```
Given a Python file with no issues
When I run `pyaudit src/`
Then exit code is 0
And terminal output shows "No issues found"
```

### Scenario 2: Style violations found
```
Given a Python file with PEP8 violations
When I run `pyaudit src/`
Then exit code is 1
And terminal output lists each violation with file:line:col and error code
```

### Scenario 3: Security vulnerability found
```
Given a Python file using `subprocess.call(shell=True)`
When I run `pyaudit src/`
Then exit code is 1
And output includes a HIGH severity Bandit finding with CWE reference
```

### Scenario 4: JSON output
```
Given any Python project
When I run `pyaudit src/ --format json`
Then stdout is valid JSON matching the output schema
```

### Scenario 5: Selective tool run
```
Given any Python project
When I run `pyaudit src/ --only bandit`
Then only Bandit results are shown
And Flake8 and Pylint are not executed
```
