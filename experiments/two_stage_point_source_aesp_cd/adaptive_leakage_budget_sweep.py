#!/usr/bin/env python3
"""Sweep semantic budget splits for the adaptive two-heap leakage lane."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict
from pathlib import Path

from adaptive_leakage_screen_benchmark import run_case
from portfolio_benchmark import (
    binary_tree,
    broom_graph,
    cycle_graph,
    grid_graph,
    path_graph,
    star_graph,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--fractions",
        nargs="+",
        type=float,
        default=(0.5, 0.75, 0.9, 0.99),
    )
    parser.add_argument("--epsilons", nargs="+", type=float, default=(0.005, 0.01, 0.02))
    parser.add_argument("--alphas", nargs="+", type=float, default=(0.01, 0.04, 0.16))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    graphs = [
        ("path-96", path_graph(96)),
        ("cycle-96", cycle_graph(96)),
        ("star-96", star_graph(95)),
        ("binary-depth-7", binary_tree(7)),
        ("broom-48-47", broom_graph(48, 47)),
        ("grid-12x12", grid_graph(12, 12)),
    ]
    rows = [
        run_case(
            family,
            adjacency,
            alpha,
            epsilon,
            leakage_fraction=fraction,
        )
        for family, adjacency in graphs
        for alpha in args.alphas
        for epsilon in args.epsilons
        for fraction in args.fractions
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(asdict(rows[0])))
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    print(f"wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
