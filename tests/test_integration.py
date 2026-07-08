import subprocess
import sys
import json
import os
import pytest

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")


def _run(args):
    return subprocess.run(
        [sys.executable, "-m", "pyaudit.cli"] + args,
        capture_output=True,
        text=True,
    )


@pytest.mark.integration
def test_clean_file_exits_zero():
    result = _run([os.path.join(FIXTURES, "clean.py")])
    assert result.returncode == 0


@pytest.mark.integration
def test_security_vulns_exits_one():
    result = _run([os.path.join(FIXTURES, "security_vulns.py")])
    assert result.returncode == 1


@pytest.mark.integration
def test_json_output_is_valid():
    result = _run([FIXTURES, "--format", "json"])
    assert result.returncode in (0, 1)
    data = json.loads(result.stdout)
    assert "summary" in data
    assert "results" in data


@pytest.mark.integration
def test_only_bandit():
    result = _run([os.path.join(FIXTURES, "security_vulns.py"), "--only", "bandit", "--format", "json"])
    data = json.loads(result.stdout)
    assert "bandit" in data["results"]
    assert "flake8" not in data["results"]
    assert "pylint" not in data["results"]
