import json
import pytest
from pyaudit.parsers import flake8 as f8, pylint as pl, bandit as bd


class TestFlake8Parser:
    def test_parses_single_issue(self):
        output = "src/foo.py:10:4: E302 expected 2 blank lines, found 1\n"
        issues = f8.parse(output)
        assert len(issues) == 1
        i = issues[0]
        assert i.file == "src/foo.py"
        assert i.line == 10
        assert i.col == 4
        assert i.code == "E302"
        assert "blank lines" in i.message

    def test_parses_multiple_issues(self):
        output = (
            "a.py:1:1: E401 multiple imports on one line\n"
            "a.py:3:5: W291 trailing whitespace\n"
        )
        assert len(f8.parse(output)) == 2

    def test_empty_output(self):
        assert f8.parse("") == []

    def test_ignores_non_matching_lines(self):
        assert f8.parse("Some random text\n") == []


class TestPylintParser:
    def test_parses_single_issue(self):
        output = "src/foo.py:22:0: C0114: Missing module docstring (missing-module-docstring)\n"
        issues = pl.parse(output)
        assert len(issues) == 1
        i = issues[0]
        assert i.file == "src/foo.py"
        assert i.line == 22
        assert i.message_id == "C0114"
        assert i.symbol == "missing-module-docstring"

    def test_empty_output(self):
        assert pl.parse("") == []


class TestBanditParser:
    def _make_output(self, results):
        return json.dumps({"results": results})

    def test_parses_issue_with_cwe(self):
        data = [{
            "filename": "src/foo.py",
            "line_number": 45,
            "issue_severity": "HIGH",
            "issue_confidence": "HIGH",
            "issue_text": "Use of subprocess with shell=True",
            "issue_cwe": {"id": 78, "link": ""},
        }]
        issues = bd.parse(self._make_output(data))
        assert len(issues) == 1
        i = issues[0]
        assert i.severity == "HIGH"
        assert i.cwe == "CWE-78"

    def test_parses_issue_without_cwe(self):
        data = [{
            "filename": "f.py", "line_number": 1,
            "issue_severity": "LOW", "issue_confidence": "MEDIUM",
            "issue_text": "some issue", "issue_cwe": {},
        }]
        issues = bd.parse(self._make_output(data))
        assert issues[0].cwe == ""

    def test_invalid_json(self):
        assert bd.parse("not json") == []

    def test_empty_results(self):
        assert bd.parse(json.dumps({"results": []})) == []
