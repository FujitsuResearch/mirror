import unittest

from mirror.metrics import (
    duplicate_rate_against_benchmark,
    mean_pairwise_ngram_jaccard_distance,
    novel_asr,
    self_duplicate_rate,
    wilson_interval,
)


class MetricsTests(unittest.TestCase):
    def test_wilson_interval_known_shape(self):
        low, high = wilson_interval(47, 100)
        self.assertAlmostEqual(low, 0.375, places=3)
        self.assertAlmostEqual(high, 0.567, places=3)

    def test_duplicate_rate_against_benchmark(self):
        rate = duplicate_rate_against_benchmark(["a b", "new"], ["a   b"], mode="exact")
        self.assertEqual(rate, 0.5)

    def test_self_duplicate_rate(self):
        self.assertEqual(self_duplicate_rate(["A!", "a", "B"], mode="alnum"), 1 / 3)

    def test_novel_asr(self):
        self.assertEqual(novel_asr([True, True, False], [False, True, False]), 1 / 3)

    def test_mean_pairwise_distance(self):
        value = mean_pairwise_ngram_jaccard_distance(["a b c d", "a b c e"], n=3)
        self.assertIsNotNone(value)
        self.assertGreaterEqual(value, 0.0)
        self.assertLessEqual(value, 1.0)


if __name__ == "__main__":
    unittest.main()
