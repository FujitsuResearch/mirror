#!/usr/bin/env python3
"""Basic release hygiene checks."""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "README.md",
    "LICENSE",
    "pyproject.toml",
    "CITATION.cff",
    "configs/paper_config.json",
    "docs/REPRODUCIBILITY.md",
    "docs/RESPONSIBLE_USE.md",
    "artifacts/paper_results/EXPERIMENT_RESULTS_FULL_CANONICAL.tex",
    "src/mirror/novelty.py",
    "src/mirror/metrics.py",
    "scripts/verify_paper_tables.py",
]

DENY_FILENAMES = {
    ".env",
    ".env.local",
    "id_rsa",
    "id_ed25519",
}

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"AZURE_OPENAI_API_KEY\s*="),
    re.compile(r"OPENAI_API_KEY\s*="),
]


def main() -> int:
    problems: list[str] = []
    for rel in REQUIRED_PATHS:
        if not (ROOT / rel).exists():
            problems.append(f"missing required path: {rel}")

    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.name in DENY_FILENAMES:
            problems.append(f"forbidden file name: {path.relative_to(ROOT)}")
        if path.is_file() and path.stat().st_size <= 2_000_000:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    problems.append(f"possible secret pattern in {path.relative_to(ROOT)}")

    if problems:
        print("release check failed")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print("release check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
