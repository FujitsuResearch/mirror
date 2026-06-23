"""Parser for the canonical supplementary result table source."""

from __future__ import annotations

from dataclasses import dataclass
import re
from pathlib import Path


@dataclass(frozen=True)
class ResultRow:
    target: str
    surface: str
    method: str
    asr_percent: float
    ci_low_percent: float
    ci_high_percent: float
    mean_score: float
    q_per_success: float | None
    total_q: int
    diversity: float | None
    stealth: float | None
    mean_time_seconds: float
    nrp_b4: float | None


_TABLE_RE = re.compile(
    r"\\caption\{Results on (?P<target>\w+) (?P<surface>.+?) "
    r"\(success threshold (?P<threshold>[0-9.]+)\).\}.*?"
    r"\\midrule(?P<body>.*?)\\bottomrule",
    re.DOTALL,
)

_ASR_RE = re.compile(
    r"(?P<asr>[0-9.]+)\\%\\\\\((?P<low>[0-9.]+)\\%, (?P<high>[0-9.]+)\\%\)"
)


def parse_results_tex(path: str | Path) -> list[ResultRow]:
    text = Path(path).read_text(encoding="utf-8")
    rows: list[ResultRow] = []
    for match in _TABLE_RE.finditer(text):
        target = match.group("target")
        surface = match.group("surface").strip().replace("\\_", "_")
        body = match.group("body")
        for raw_line in body.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("\\"):
                continue
            if "&" not in line:
                continue
            rows.append(_parse_row(target, surface, line))
    return rows


def _parse_row(target: str, surface: str, line: str) -> ResultRow:
    line = line.rstrip("\\").strip()
    parts = [part.strip() for part in line.split("&")]
    if len(parts) != 9:
        raise ValueError(f"expected 9 columns, got {len(parts)} in line: {line}")

    asr_match = _ASR_RE.search(parts[1])
    if not asr_match:
        raise ValueError(f"could not parse ASR column: {parts[1]}")

    return ResultRow(
        target=target,
        surface=surface,
        method=parts[0].replace("\\_", "_"),
        asr_percent=float(asr_match.group("asr")),
        ci_low_percent=float(asr_match.group("low")),
        ci_high_percent=float(asr_match.group("high")),
        mean_score=float(parts[2]),
        q_per_success=_parse_float_or_none(parts[3]),
        total_q=int(parts[4]),
        diversity=_parse_float_or_none(parts[5]),
        stealth=_parse_float_or_none(parts[6]),
        mean_time_seconds=float(parts[7]),
        nrp_b4=_parse_float_or_none(parts[8]),
    )


def _parse_float_or_none(value: str) -> float | None:
    if value in {"-", "--"}:
        return None
    if value == "inf":
        return None
    return float(value)
