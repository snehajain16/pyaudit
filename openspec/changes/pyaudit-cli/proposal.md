# Proposal: PyAudit CLI Tool

## Summary

A unified Python CLI tool that combines code linting and static security analysis to improve code quality and reliability. It integrates Flake8, Pylint, and Bandit into a single command with structured, actionable output and GitHub Actions support for continuous auditing.

## Problem

Python developers currently need to run multiple separate tools (Flake8 for style, Pylint for code quality, Bandit for security) with no unified view of results, making it hard to get a holistic picture of code health in one pass.

## Proposed Solution

Build a `pyaudit` CLI that:
- Runs Flake8 (PEP8 style), Pylint (code quality), and Bandit (security vulnerabilities) in a single command
- Aggregates and formats results into a clear, categorized report
- Supports multiple output formats (terminal, JSON, GitHub annotations)
- Integrates with GitHub Actions for CI/CD auditing via the GitHub API

## Scope

### In Scope
- CLI entry point (`pyaudit` command)
- Flake8 integration for style checks
- Pylint integration for code quality checks
- Bandit integration for security vulnerability detection
- Aggregated report output (terminal + JSON)
- GitHub Actions workflow for continuous auditing
- GitHub API integration to post check results as PR annotations

### Out of Scope
- Auto-fix capabilities (v2)
- Support for languages other than Python (v2)
- Custom rule authoring (v2)

## Rationale

Combining these tools reduces friction, enforces consistent usage across teams, and enables automation that would otherwise require complex shell scripts or separate CI jobs.
