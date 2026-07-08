import json
from dataclasses import dataclass


@dataclass
class BanditIssue:
    file: str
    line: int
    severity: str
    confidence: str
    issue: str
    cwe: str


def parse(output: str) -> list[BanditIssue]:
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return []

    issues = []
    for r in data.get("results", []):
        cwe = r.get("issue_cwe", {})
        cwe_str = f"CWE-{cwe.get('id', '')}" if cwe.get("id") else ""
        issues.append(BanditIssue(
            file=r.get("filename", ""),
            line=r.get("line_number", 0),
            severity=r.get("issue_severity", ""),
            confidence=r.get("issue_confidence", ""),
            issue=r.get("issue_text", ""),
            cwe=cwe_str,
        ))
    return issues
