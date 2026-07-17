#!/usr/bin/env python3
"""Summarize JSONL output produced by reproduce.py."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


def wilson_interval(successes: int, trials: int, z: float = 1.95996398454) -> tuple[float, float]:
    if trials == 0:
        return (0.0, 0.0)
    proportion = successes / trials
    denominator = 1 + z * z / trials
    center = (proportion + z * z / (2 * trials)) / denominator
    margin = (
        z
        * math.sqrt(
            proportion * (1 - proportion) / trials + z * z / (4 * trials * trials)
        )
        / denominator
    )
    return (max(0.0, center - margin), min(1.0, center + margin))


def records(paths: Iterable[Path]):
    for path in paths:
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                record = json.loads(line)
                if not isinstance(record, dict):
                    raise ValueError(f"{path}:{line_number}: record is not an object")
                yield record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", type=Path, nargs="+")
    args = parser.parse_args()

    grouped: dict[str, Counter[str]] = defaultdict(Counter)
    hashes: dict[str, set[str]] = defaultdict(set)
    for record in records(args.paths):
        envelope = str(record.get("envelope", "unknown"))
        grouped[envelope][str(record.get("classification", "unknown"))] += 1
        if record.get("request_sha256"):
            hashes[envelope].add(str(record["request_sha256"]))

    summary = {"envelopes": {}}
    for envelope, counts in sorted(grouped.items()):
        trials = sum(counts.values())
        substitutions = sum(
            count
            for label, count in counts.items()
            if label in {"claude_substitution", "cursor_substitution", "other_path"}
        )
        low, high = wilson_interval(substitutions, trials)
        summary["envelopes"][envelope] = {
            "trials": trials,
            "counts": dict(sorted(counts.items())),
            "substitution_rate": substitutions / trials if trials else 0.0,
            "substitution_rate_wilson_95": [low, high],
            "request_sha256": sorted(hashes[envelope]),
        }

    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
