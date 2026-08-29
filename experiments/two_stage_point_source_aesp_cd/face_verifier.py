#!/usr/bin/env python3
"""Residual-interval verifier for a structural point-source RPPR face."""

from __future__ import annotations

import numpy as np

try:
    from .structural_solvers import (
        principal_residual,
        tree_or_unicyclic_principal_solve,
    )
except ImportError:  # Direct script execution.
    from structural_solvers import (
        principal_residual,
        tree_or_unicyclic_principal_solve,
    )


def exact_face_verifier(
    adjacency: list[list[int]],
    alpha: float,
    rho: float,
    seed: int,
    candidate: np.ndarray,
) -> tuple[bool, int, int, float, float]:
    """Solve a structural candidate face and check global obstacle KKT."""
    degree = np.asarray([len(row) for row in adjacency], dtype=float)
    volume = int(degree[candidate].sum())
    source = -alpha * rho * np.sqrt(degree)
    source[seed] += alpha / np.sqrt(degree[seed])
    if not candidate.any():
        rounding = 2e-12 * max(1.0, float(np.max(np.abs(source))))
        maximum_key = float(np.max(source)) + rounding
        return maximum_key <= 0.0, 0, 0, float("inf"), maximum_key
    try:
        point, arithmetic, _kind = tree_or_unicyclic_principal_solve(
            adjacency, candidate, degree, alpha, source, seed
        )
    except ValueError:
        return False, volume, 0, float("-inf"), float("inf")
    active = np.flatnonzero(candidate)
    retained_residual = principal_residual(
        adjacency,
        candidate,
        degree,
        alpha,
        source,
        point,
    )
    # Strong convexity gives ||point - exact_face||_2 <= ||residual||_2 / alpha.
    # Propagate this one scalar interval through positivity and every exterior
    # row instead of treating floating signs as exact comparisons.
    error_bar = float(np.linalg.norm(retained_residual[active]) / alpha)
    rounding = 2e-12 * max(
        1.0,
        float(np.max(np.abs(source))),
        float(np.max(np.abs(point[active]))),
    )
    minimum_active = float(np.min((point[active] - error_bar - rounding) / np.sqrt(degree[active])))
    coupling = (1.0 - alpha) / 2.0
    boundary = {
        neighbor
        for vertex in active
        for neighbor in adjacency[int(vertex)]
        if not candidate[neighbor]
    }
    maximum_boundary = float("-inf")
    for vertex in boundary:
        key = source[vertex]
        for neighbor in adjacency[vertex]:
            if candidate[neighbor]:
                key += coupling * point[neighbor] / np.sqrt(degree[vertex] * degree[neighbor])
        row_norm = coupling * np.sqrt(
            sum(
                1.0 / (degree[vertex] * degree[neighbor])
                for neighbor in adjacency[vertex]
                if candidate[neighbor]
            )
        )
        upper_key = float(key) + row_norm * error_bar + rounding
        maximum_boundary = max(maximum_boundary, upper_key)
    certified = minimum_active > 0.0 and maximum_boundary <= 0.0
    return certified, volume + arithmetic, volume, minimum_active, maximum_boundary
