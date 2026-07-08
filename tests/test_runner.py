import pytest
from unittest.mock import patch, MagicMock
import subprocess
from pyaudit.runner import run_tool, RunResult


def test_run_tool_success():
    result = run_tool(["echo", "hello"])
    assert result.returncode == 0
    assert "hello" in result.stdout


def test_run_tool_captures_stderr():
    result = run_tool(["python3", "-c", "import sys; sys.stderr.write('err')"])
    assert "err" in result.stderr


def test_run_tool_nonzero_exit():
    result = run_tool(["python3", "-c", "import sys; sys.exit(1)"])
    assert result.returncode == 1


def test_run_tool_missing_command():
    with pytest.raises(RuntimeError, match="Tool not found"):
        run_tool(["no_such_tool_xyz"])


def test_run_tool_timeout():
    with pytest.raises(RuntimeError, match="timed out"):
        run_tool(["sleep", "10"], timeout=1)
