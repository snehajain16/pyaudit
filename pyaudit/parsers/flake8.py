import re
from dataclasses import dataclass

_PATTERN = re.compile(r"^(.+):(\d+):(\d+):\s+(\S+)\s+(.+)$")


@dataclass
class Flake8Issue:
    file: str
    line: int
    col: int
    code: str
    message: str


def parse(output: str) -> list[Flake8Issue]:
    issues = []
    for line in output.splitlines():
        m = _PATTERN.match(line.strip())
        if m:
            issues.append(Flake8Issue(
                file=m.group(1),
                line=int(m.group(2)),
                col=int(m.group(3)),
                code=m.group(4),
                message=m.group(5),
            ))
    return issues
