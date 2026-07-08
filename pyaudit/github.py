import os
import requests


_API = "https://api.github.com"


def post_check_annotations(results: dict, sha: str) -> None:
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo:
        raise RuntimeError("GITHUB_TOKEN and GITHUB_REPOSITORY must be set")

    annotations = _build_annotations(results)
    conclusion = "success" if all(len(v) == 0 for v in results.values()) else "failure"
    total = sum(len(v) for v in results.values())

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    # Create check run
    resp = requests.post(
        f"{_API}/repos/{repo}/check-runs",
        headers=headers,
        json={
            "name": "pyaudit",
            "head_sha": sha,
            "status": "completed",
            "conclusion": conclusion,
            "output": {
                "title": f"PyAudit: {total} issue(s) found",
                "summary": _summary(results),
                "annotations": annotations[:50],  # GitHub API limit per request
            },
        },
        timeout=30,
    )
    resp.raise_for_status()


def _summary(results: dict) -> str:
    lines = []
    for tool, issues in results.items():
        lines.append(f"**{tool}**: {len(issues)} issue(s)")
    return "\n".join(lines)


def _build_annotations(results: dict) -> list[dict]:
    annotations = []

    for tool, issues in results.items():
        for issue in issues:
            if tool == "flake8":
                msg = f"[{issue.code}] {issue.message}"
                level = "warning"
            elif tool == "pylint":
                msg = f"[{issue.message_id}] {issue.message} ({issue.symbol})"
                level = "warning"
            elif tool == "bandit":
                msg = f"[{issue.severity}/{issue.confidence}] {issue.issue}"
                if issue.cwe:
                    msg += f" ({issue.cwe})"
                level = "failure" if issue.severity == "HIGH" else "warning"
            else:
                continue

            annotations.append({
                "path": issue.file,
                "start_line": issue.line,
                "end_line": issue.line,
                "annotation_level": level,
                "message": msg,
                "title": f"pyaudit/{tool}",
            })

    return annotations
