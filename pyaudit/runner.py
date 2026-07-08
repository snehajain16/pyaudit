import subprocess
from dataclasses import dataclass


@dataclass
class RunResult:
    stdout: str
    stderr: str
    returncode: int


def run_tool(cmd: list[str], timeout: int = 120) -> RunResult:
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return RunResult(proc.stdout, proc.stderr, proc.returncode)
    except FileNotFoundError as e:
        raise RuntimeError(f"Tool not found: {cmd[0]}. Is it installed?") from e
    except subprocess.TimeoutExpired as e:
        raise RuntimeError(f"Tool timed out after {timeout}s: {cmd[0]}") from e
