#!/usr/bin/env python3
"""Integrity-check the shipped canonical supplementary result tables."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from mirror.tables import parse_results_tex


EXPECTED = {
    ("generalrag", "B1_TEXT_POISON", "grimoire"): (47.0, 0.587, 241),
    ("generalrag", "B1_TEXT_POISON", "gcg_approx"): (79.0, 0.869, 280),
    ("generalrag", "B1_TEXT_POISON", "open_loop"): (63.0, 0.761, 434),
    ("generalrag", "B1_TEXT_POISON", "pair"): (77.0, 0.861, 287),
    ("generalrag", "B1_TEXT_POISON", "random_sampling"): (58.0, 0.727, 472),
    ("generalrag", "B1_TEXT_POISON", "tap"): (72.0, 0.826, 315),
    ("generalrag", "B2_IMAGE_POISON", "grimoire"): (76.0, 0.860, 41),
    ("generalrag", "B2_IMAGE_POISON", "b2_stego"): (32.0, 0.556, 94),
    ("generalrag", "B2_IMAGE_POISON", "b2_text_overlay"): (52.0, 0.696, 76),
    ("generalrag", "B3_DIRECT_QUERY", "grimoire"): (31.0, 0.429, 528),
    ("generalrag", "B3_DIRECT_QUERY", "gcg_approx"): (1.0, 0.315, 794),
    ("generalrag", "B3_DIRECT_QUERY", "open_loop"): (24.0, 0.462, 701),
    ("generalrag", "B3_DIRECT_QUERY", "pair"): (3.0, 0.312, 779),
    ("generalrag", "B3_DIRECT_QUERY", "random_sampling"): (20.0, 0.514, 655),
    ("generalrag", "B3_DIRECT_QUERY", "tap"): (0.0, 0.284, 800),
    ("generalrag", "B4_ORCHESTRATOR", "grimoire"): (97.0, 0.970, 100),
    ("generalrag", "B4_ORCHESTRATOR", "open_loop_toolflip"): (86.0, 0.860, 291),
    ("cyberrag", "B1_TEXT_POISON", "grimoire"): (44.4, 0.511, 13),
    ("cyberrag", "B1_TEXT_POISON", "gcg_approx"): (100.0, 1.000, 15),
    ("cyberrag", "B1_TEXT_POISON", "open_loop"): (88.9, 0.922, 32),
    ("cyberrag", "B1_TEXT_POISON", "pair"): (88.9, 0.944, 16),
    ("cyberrag", "B1_TEXT_POISON", "random_sampling"): (100.0, 1.000, 34),
    ("cyberrag", "B1_TEXT_POISON", "tap"): (88.9, 0.944, 22),
    ("cyberrag", "B3_DIRECT_QUERY", "grimoire"): (28.6, 0.432, 150),
    ("cyberrag", "B3_DIRECT_QUERY", "gcg_approx"): (71.4, 0.836, 106),
    ("cyberrag", "B3_DIRECT_QUERY", "open_loop"): (57.1, 0.750, 137),
    ("cyberrag", "B3_DIRECT_QUERY", "pair"): (57.1, 0.743, 128),
    ("cyberrag", "B3_DIRECT_QUERY", "random_sampling"): (28.6, 0.550, 176),
    ("cyberrag", "B3_DIRECT_QUERY", "tap"): (42.9, 0.625, 145),
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        nargs="?",
        default=ROOT / "artifacts/paper_results/EXPERIMENT_RESULTS_FULL_CANONICAL.tex",
        type=Path,
    )
    args = parser.parse_args()

    rows = parse_results_tex(args.path)
    by_key = {(row.target, row.surface, row.method): row for row in rows}

    problems: list[str] = []
    missing = set(EXPECTED) - set(by_key)
    extra = set(by_key) - set(EXPECTED)
    for key in sorted(missing):
        problems.append(f"missing row: {key}")
    for key in sorted(extra):
        problems.append(f"unexpected row: {key}")

    for key, expected in EXPECTED.items():
        row = by_key.get(key)
        if row is None:
            continue
        expected_asr, expected_score, expected_total_q = expected
        if row.asr_percent != expected_asr:
            problems.append(f"{key} ASR {row.asr_percent} != {expected_asr}")
        if row.mean_score != expected_score:
            problems.append(f"{key} mean score {row.mean_score} != {expected_score}")
        if row.total_q != expected_total_q:
            problems.append(f"{key} total Q {row.total_q} != {expected_total_q}")

    if problems:
        print("verification failed")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print(f"verified {len(rows)} canonical result rows from {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
