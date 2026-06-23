import unittest

from mirror.canonicalize import norm_alnum, norm_exact
from mirror.novelty import NoveltyGate


class CanonicalizeTests(unittest.TestCase):
    def test_norm_exact_collapses_whitespace(self):
        self.assertEqual(norm_exact("  alpha\n beta\tgamma  "), "alpha beta gamma")

    def test_norm_alnum_removes_punctuation_and_lowercases(self):
        self.assertEqual(norm_alnum("A-b C! 123"), "abc123")

    def test_novelty_gate_rejects_benchmark_duplicate(self):
        gate = NoveltyGate(benchmark_texts=["Known prompt"])
        decision = gate.check("Known   prompt")
        self.assertFalse(decision.accepted)
        self.assertEqual(decision.reason, "benchmark_duplicate")

    def test_novelty_gate_rejects_session_duplicate_after_accept(self):
        gate = NoveltyGate()
        self.assertTrue(gate.accept("fresh text").accepted)
        decision = gate.accept("fresh text")
        self.assertFalse(decision.accepted)
        self.assertEqual(decision.reason, "session_duplicate")


if __name__ == "__main__":
    unittest.main()
