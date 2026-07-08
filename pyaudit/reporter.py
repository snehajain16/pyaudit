import json
import sys

# ANSI colours
_BOLD = "\033[1m"
_RED = "\033[31m"
_YELLOW = "\033[33m"
_CYAN = "\033[36m"
_GREEN = "\033[32m"
_RESET = "\033[0m"

_SEV_COLOR = {"HIGH": _RED, "MEDIUM": _YELLOW, "LOW": _CYAN}


def _color(text: str, code: str) -> str:
    if sys.stdout.isatty():
        return f"{code}{text}{_RESET}"
    return text


def terminal_report(results: dict) -> None:
    total = sum(len(v) for v in results.values())

    for tool, issues in results.items():
        print(f"\n{_color(f'── {tool.upper()} ──', _BOLD)} ({len(issues)} issue(s))")
        if not issues:
            print(f"  {_color('No issues found', _GREEN)}")
            continue

        for issue in issues:
            if tool == "flake8":
                print(f"  {issue.file}:{issue.line}:{issue.col}  {_color(issue.code, _YELLOW)}  {issue.message}")
            elif tool == "pylint":
                print(f"  {issue.file}:{issue.line}  {_color(issue.message_id, _YELLOW)}  {issue.message}  ({issue.symbol})")
            elif tool == "bandit":
                sev_color = _SEV_COLOR.get(issue.severity, "")
                cwe = f"  {issue.cwe}" if issue.cwe else ""
                print(f"  {issue.file}:{issue.line}  [{_color(issue.severity, sev_color)}/{issue.confidence}]{cwe}  {issue.issue}")

    print()
    if total == 0:
        print(_color("✓ No issues found", _GREEN))
    else:
        print(_color(f"✗ {total} issue(s) found", _RED))
        by_tool = "  " + "  ".join(f"{t}: {len(v)}" for t, v in results.items())
        print(by_tool)


def json_report(results: dict) -> str:
    total = sum(len(v) for v in results.values())
    out: dict = {
        "summary": {
            "total_issues": total,
            "by_tool": {t: len(v) for t, v in results.items()},
            "passed": total == 0,
        },
        "results": {},
    }

    for tool, issues in results.items():
        if tool == "flake8":
            out["results"][tool] = [
                {"file": i.file, "line": i.line, "col": i.col, "code": i.code, "message": i.message}
                for i in issues
            ]
        elif tool == "pylint":
            out["results"][tool] = [
                {"file": i.file, "line": i.line, "message_id": i.message_id, "symbol": i.symbol, "message": i.message}
                for i in issues
            ]
        elif tool == "bandit":
            out["results"][tool] = [
                {"file": i.file, "line": i.line, "severity": i.severity, "confidence": i.confidence, "issue": i.issue, "cwe": i.cwe}
                for i in issues
            ]

    return json.dumps(out, indent=2)
