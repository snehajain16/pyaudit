import argparse
import sys

from pyaudit import __version__
from pyaudit.runner import run_tool
from pyaudit.parsers import flake8 as flake8_parser
from pyaudit.parsers import pylint as pylint_parser
from pyaudit.parsers import bandit as bandit_parser
from pyaudit.reporter import terminal_report, json_report

TOOLS = ("flake8", "pylint", "bandit")


def _run_flake8(path: str, config: str | None):
    cmd = ["flake8", path]
    if config:
        cmd += ["--config", config]
    result = run_tool(cmd)
    return flake8_parser.parse(result.stdout)


def _run_pylint(path: str, config: str | None):
    cmd = ["pylint", path, "--output-format=text", "--score=no"]
    if config:
        cmd += ["--rcfile", config]
    result = run_tool(cmd)
    return pylint_parser.parse(result.stdout)


def _run_bandit(path: str, config: str | None):
    cmd = ["bandit", "-r", path, "-f", "json", "-q"]
    if config:
        cmd += ["--configfile", config]
    result = run_tool(cmd)
    return bandit_parser.parse(result.stdout)


def main():
    parser = argparse.ArgumentParser(
        prog="pyaudit",
        description="Unified Python linting and static security analysis",
    )
    parser.add_argument("path", help="File or directory to audit")
    parser.add_argument(
        "--only",
        choices=TOOLS,
        help="Run only the specified tool",
    )
    parser.add_argument(
        "--format",
        choices=("terminal", "json"),
        default="terminal",
        dest="fmt",
        help="Output format (default: terminal)",
    )
    parser.add_argument(
        "--config",
        help="Path to tool config file",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"pyaudit {__version__}",
    )

    args = parser.parse_args()
    selected = [args.only] if args.only else list(TOOLS)

    results = {}
    try:
        if "flake8" in selected:
            results["flake8"] = _run_flake8(args.path, args.config)
        if "pylint" in selected:
            results["pylint"] = _run_pylint(args.path, args.config)
        if "bandit" in selected:
            results["bandit"] = _run_bandit(args.path, args.config)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)

    if args.fmt == "json":
        print(json_report(results), flush=True)
    else:
        terminal_report(results)
        sys.stdout.flush()

    total_issues = sum(len(v) for v in results.values())
    sys.exit(1 if total_issues > 0 else 0)


if __name__ == "__main__":
    main()
