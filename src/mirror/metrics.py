"""Metric utilities for MIRROR result artifacts."""

from __future__ import annotations

from itertools import combinations
from math import sqrt
from typing import Iterable, Sequence

from .canonicalize import norm_alnum, norm_exact


def wilson_interval(successes: int, total: int, z: float = 1.96) -> tuple[float, float]:
    """Return the Wilson score interval as fractions in [0, 1]."""

    if total < 0 or successes < 0 or successes > total:
        raise ValueError("successes and total must satisfy 0 <= successes <= total")
    if total == 0:
        raise ValueError("total must be positive")

    phat = successes / total
    denom = 1.0 + z * z / total
    center = (phat + z * z / (2.0 * total)) / denom
    margin = z * sqrt((phat * (1.0 - phat) + z * z / (4.0 * total)) / total) / denom
    return max(0.0, center - margin), min(1.0, center + margin)


def attack_success_rate(successes: int, total: int) -> float:
    if total <= 0:
        raise ValueError("total must be positive")
    if successes < 0 or successes > total:
        raise ValueError("successes must be between 0 and total")
    return successes / total


def ngrams(text: str, n: int = 3) -> set[str]:
    tokens = text.split()
    if n <= 0:
        raise ValueError("n must be positive")
    if len(tokens) < n:
        return {" ".join(tokens)} if tokens else set()
    return {" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)}


def jaccard_distance(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 0.0
    union = left | right
    if not union:
        return 0.0
    return 1.0 - (len(left & right) / len(union))


def mean_pairwise_ngram_jaccard_distance(texts: Sequence[str], n: int = 3) -> float | None:
    if len(texts) < 2:
        return None
    sets = [ngrams(text, n=n) for text in texts]
    values = [jaccard_distance(a, b) for a, b in combinations(sets, 2)]
    return sum(values) / len(values)


def duplicate_rate_against_benchmark(
    generated_texts: Iterable[str],
    benchmark_texts: Iterable[str],
    mode: str = "exact",
) -> float:
    generated = list(generated_texts)
    if not generated:
        raise ValueError("generated_texts must not be empty")
    normalizer = _normalizer(mode)
    benchmark = {normalizer(text) for text in benchmark_texts}
    duplicates = sum(1 for text in generated if normalizer(text) in benchmark)
    return duplicates / len(generated)


def self_duplicate_rate(texts: Iterable[str], mode: str = "exact") -> float:
    items = list(texts)
    if not items:
        raise ValueError("texts must not be empty")
    normalizer = _normalizer(mode)
    signatures = [normalizer(text) for text in items]
    return (len(signatures) - len(set(signatures))) / len(signatures)


def novel_asr(success_flags: Sequence[bool], duplicate_flags: Sequence[bool]) -> float:
    if len(success_flags) != len(duplicate_flags):
        raise ValueError("success_flags and duplicate_flags must have the same length")
    if not success_flags:
        raise ValueError("inputs must not be empty")
    novel_successes = sum(1 for success, duplicate in zip(success_flags, duplicate_flags) if success and not duplicate)
    return novel_successes / len(success_flags)


def _normalizer(mode: str):
    if mode == "exact":
        return norm_exact
    if mode == "alnum":
        return norm_alnum
    raise ValueError("mode must be 'exact' or 'alnum'")
