#!/usr/bin/env python3
"""Larger-graph scaling check for the one-shot Green--CG lane."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict
from pathlib import Path

import numpy as np

from green_ball_high_accuracy_benchmark import run_case
from portfolio_benchmark import (
    binary_tree,
    broom_graph,
    cycle_graph,
    grid_graph,
    path_graph,
    star_graph,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    graphs = [
        ("path-1024", path_graph(1024)),
        ("cycle-1024", cycle_graph(1024)),
        ("star-1024", star_graph(1023)),
        ("binary-depth-10", binary_tree(10)),
        ("grid-32x32", grid_graph(32, 32)),
        ("broom-512-511", broom_graph(512, 511)),
    ]
    parameters = (
        (0.01, 0.0001),
        (0.01, 0.0005),
        (0.04, 0.0001),
    )
    rows = [
        run_case(family, graph, alpha, epsilon)
        for alpha, epsilon in parameters
        for family, graph in graphs
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=asdict(rows[0]).keys())
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    wins = [row for row in rows if row.succeeded and row.lane_ratio < 1]
    print(
        f"rows={len(rows)} successes={sum(row.succeeded for row in rows)} "
        f"wins={len(wins)} median={np.median([row.lane_ratio for row in rows]):.6f}"
    )
    for row in sorted(wins, key=lambda item: item.lane_ratio):
        print(
            row.family,
            row.alpha,
            row.epsilon,
            f"ratio={row.lane_ratio:.6f}",
            f"volume={row.envelope_volume}",
            f"cg={row.cg_iterations}",
        )


if __name__ == "__main__":
    main()
