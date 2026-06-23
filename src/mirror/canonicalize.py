"""Deterministic text canonicalization used for exact duplication checks."""

from __future__ import annotations


def _require_text(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"expected str, got {type(value).__name__}")
    return value


def norm_exact(text: str) -> str:
    """Normalize only leading, trailing, and repeated whitespace."""

    text = _require_text(text)
    return " ".join(text.strip().split())


def norm_alnum(text: str) -> str:
    """Lowercase and retain only alphanumeric characters."""

    text = _require_text(text)
    return "".join(ch.lower() for ch in text if ch.isalnum())


def canonical_pair(text: str) -> tuple[str, str]:
    """Return both canonical signatures used by the deterministic gate."""

    return norm_exact(text), norm_alnum(text)
