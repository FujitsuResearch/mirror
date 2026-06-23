from pathlib import Path
import unittest

from mirror.tables import parse_results_tex


class TableParserTests(unittest.TestCase):
    def test_parse_canonical_results(self):
        path = Path(__file__).resolve().parents[1] / "artifacts/paper_results/EXPERIMENT_RESULTS_FULL_CANONICAL.tex"
        rows = parse_results_tex(path)
        self.assertEqual(len(rows), 29)
        first = rows[0]
        self.assertEqual(first.target, "generalrag")
        self.assertEqual(first.surface, "B1_TEXT_POISON")
        self.assertEqual(first.method, "grimoire")
        self.assertEqual(first.asr_percent, 47.0)


if __name__ == "__main__":
    unittest.main()
