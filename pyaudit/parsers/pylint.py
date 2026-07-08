import re
from dataclasses import dataclass

# e.g. "src/foo.py:10:0: C0114: Missing module docstring (missing-module-docstring)"
_PATTERN = re.compile(r"^(.+):(\d+):\d+:\s+(\w+):\s+(.+?)\s+\((\S+)\)\s*$")


@dataclass
class PylintIssue:
    file: str
    line: int
    message_id: str
    message: str
    symbol: str


def parse(output: str) -> list[PylintIssue]:
    issues = []
    for line in output.splitlines():
        m = _PATTERN.match(line.strip())
        if m:
            issues.append(PylintIssue(
                file=m.group(1),
                line=int(m.group(2)),
                message_id=m.group(3),
                message=m.group(4),
                symbol=m.group(5),
            ))
    return issues
