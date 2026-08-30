#!/usr/bin/env python3
"""Measure the smallest rooted ball that captures enough principal PPR mass."""

from __future__ import annotations

import argparse
import csv
from collections import deque
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy.sparse.linalg import spsolve

from portfolio_benchmark import (
    binary_tree,
    broom_graph,
    cycle_graph,
    grid_graph,
    normalized_matrix,
    path_graph,
    star_graph,
)


@dataclass(frozen=True)
class CaptureRow:
    family: str
    vertices: int
    alpha: float
    certificate: str
    target_deficit: float
    radius: int
    envelope_vertices: int
    envelope_volume: int
    full_volume: int
    volume_fraction: float
    principal_mass: float
    mass_deficit: float


def distances(adjacency: list[list[int]], seed: int) -> np.ndarray:
    result = np.full(len(adjacency), -1, dtype=int)
    result[seed] = 0
    queue = deque([seed])
    while queue:
        vertex = queue.popleft()
        for neighbor in adjacency[vertex]:
            if result[neighbor] >= 0:
                continue
            result[neighbor] = result[vertex] + 1
            queue.append(neighbor)
    if np.any(result < 0):
        raise ValueError("diagnostic expects a connected graph")
    return result


def capture_row(
    family: str,
    adjacency: list[list[int]],
    alpha: float,
    certificate: str,
    target_deficit: float,
    seed: int = 0,
) -> CaptureRow:
    degree, matrix = normalized_matrix(adjacency, alpha)
    root_degree = np.sqrt(degree)
    source = np.zeros(len(adjacency))
    source[seed] = alpha / root_degree[seed]
    distance = distances(adjacency, seed)
    full_volume = int(np.sum(degree))
    chosen = None
    for radius in range(int(np.max(distance)) + 1):
        envelope = distance <= radius
        indices = np.flatnonzero(envelope)
        principal = matrix[indices][:, indices]
        restricted_source = source[indices]
        solution = np.asarray(spsolve(principal, restricted_source))
        mass = float(np.dot(root_degree[indices], solution))
        deficit = max(0.0, 1.0 - mass)
        if deficit <= target_deficit * (1.0 + 1e-11):
            chosen = (radius, indices, mass, deficit)
            break
    if chosen is None:
        raise AssertionError("the full graph must capture unit PPR mass")
    radius, indices, mass, deficit = chosen
    volume = int(np.sum(degree[indices]))
    return CaptureRow(
        family,
        len(adjacency),
        alpha,
        certificate,
        target_deficit,
        radius,
        len(indices),
        volume,
        full_volume,
        volume / full_volume,
        mass,
        deficit,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
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
    rows = []
    for family, adjacency in graphs:
        for alpha in (0.01, 0.04, 0.16):
            # The exact checkpoint itself can start cleanup at deficit
            # sqrt(alpha).  The half-slack condition leaves the other half for
            # finite signed scratch plus safe publication.
            for certificate, deficit in (
                ("exact-mass-ready", np.sqrt(alpha)),
                ("aesp-half-slack", np.sqrt(alpha) / 2.0),
            ):
                rows.append(
                    capture_row(
                        family,
                        adjacency,
                        alpha,
                        certificate,
                        float(deficit),
                    )
                )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(asdict(rows[0])))
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    print(f"wrote {len(rows)} rows to {args.output}")
    for row in rows:
        print(
            row.family,
            f"a={row.alpha:g}",
            row.certificate,
            f"R={row.radius}",
            f"V={row.envelope_volume}/{row.full_volume}",
            f"def={row.mass_deficit:.3e}",
        )


if __name__ == "__main__":
    main()
