"""Novelty gate for exact and alphanumeric duplicate rejection."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .canonicalize import canonical_pair


@dataclass(frozen=True)
class NoveltyDecision:
    accepted: bool
    reason: str
    exact_signature: str
    alnum_signature: str


@dataclass
class NoveltyGate:
    """Deterministic exact-match novelty gate.

    The gate rejects candidates that match the benchmark pool, the retrieved
    neighbor set, or the within-session accepted set under either canonical
    signature.
    """

    benchmark_texts: Iterable[str] = field(default_factory=tuple)
    retrieved_texts: Iterable[str] = field(default_factory=tuple)
    session_texts: Iterable[str] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        self._benchmark_exact: set[str] = set()
        self._benchmark_alnum: set[str] = set()
        self._retrieved_exact: set[str] = set()
        self._retrieved_alnum: set[str] = set()
        self._session_exact: set[str] = set()
        self._session_alnum: set[str] = set()

        self.add_benchmark(self.benchmark_texts)
        self.add_retrieved(self.retrieved_texts)
        self.add_session(self.session_texts)

    def _add_many(self, texts: Iterable[str], exact_set: set[str], alnum_set: set[str]) -> None:
        for text in texts:
            exact, alnum = canonical_pair(text)
            exact_set.add(exact)
            alnum_set.add(alnum)

    def add_benchmark(self, texts: Iterable[str]) -> None:
        self._add_many(texts, self._benchmark_exact, self._benchmark_alnum)

    def add_retrieved(self, texts: Iterable[str]) -> None:
        self._add_many(texts, self._retrieved_exact, self._retrieved_alnum)

    def add_session(self, texts: Iterable[str]) -> None:
        self._add_many(texts, self._session_exact, self._session_alnum)

    def check(self, text: str) -> NoveltyDecision:
        exact, alnum = canonical_pair(text)
        if exact in self._benchmark_exact or alnum in self._benchmark_alnum:
            return NoveltyDecision(False, "benchmark_duplicate", exact, alnum)
        if exact in self._retrieved_exact or alnum in self._retrieved_alnum:
            return NoveltyDecision(False, "retrieved_duplicate", exact, alnum)
        if exact in self._session_exact or alnum in self._session_alnum:
            return NoveltyDecision(False, "session_duplicate", exact, alnum)
        return NoveltyDecision(True, "accepted", exact, alnum)

    def accept(self, text: str) -> NoveltyDecision:
        decision = self.check(text)
        if decision.accepted:
            self._session_exact.add(decision.exact_signature)
            self._session_alnum.add(decision.alnum_signature)
        return decision
