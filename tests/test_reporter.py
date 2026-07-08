import json
import pytest
from pyaudit.reporter import json_report, terminal_report
from pyaudit.parsers.flake8 import Flake8Issue
from pyaudit.parsers.pylint import PylintIssue
from pyaudit.parsers.bandit import BanditIssue


SAMPLE_RESULTS = {
    "flake8": [Flake8Issue("a.py", 1, 1, "E302", "expected 2 blank lines")],
    "pylint": [PylintIssue("a.py", 5, "C0114", "Missing docstring", "missing-module-docstring")],
    "bandit": [BanditIssue("a.py", 10, "HIGH", "HIGH", "shell=True", "CWE-78")],
}

EMPTY_RESULTS = {"flake8": [], "pylint": [], "bandit": []}


class TestJsonReport:
    def test_schema_structure(self):
        output = json.loads(json_report(SAMPLE_RESULTS))
        assert "summary" in output
        assert "results" in output
        assert output["summary"]["total_issues"] == 3
        assert output["summary"]["passed"] is False

    def test_empty_results_pass(self):
        output = json.loads(json_report(EMPTY_RESULTS))
        assert output["summary"]["passed"] is True
        assert output["summary"]["total_issues"] == 0

    def test_flake8_fields(self):
        output = json.loads(json_report(SAMPLE_RESULTS))
        item = output["results"]["flake8"][0]
        assert {"file", "line", "col", "code", "message"} == set(item.keys())

    def test_pylint_fields(self):
        output = json.loads(json_report(SAMPLE_RESULTS))
        item = output["results"]["pylint"][0]
        assert {"file", "line", "message_id", "symbol", "message"} == set(item.keys())

    def test_bandit_fields(self):
        output = json.loads(json_report(SAMPLE_RESULTS))
        item = output["results"]["bandit"][0]
        assert {"file", "line", "severity", "confidence", "issue", "cwe"} == set(item.keys())


class TestTerminalReport:
    def test_runs_without_error(self, capsys):
        terminal_report(SAMPLE_RESULTS)
        captured = capsys.readouterr()
        assert "FLAKE8" in captured.out
        assert "PYLINT" in captured.out
        assert "BANDIT" in captured.out

    def test_empty_shows_no_issues(self, capsys):
        terminal_report(EMPTY_RESULTS)
        captured = capsys.readouterr()
        assert "No issues found" in captured.out
