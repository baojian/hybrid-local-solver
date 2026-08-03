"""Reference implementation of classical lazy APPR.

The update and stopping rule follow Andersen, Chung, and Lang (2007),
Definition 3.3 and Algorithm 1. The implementation exposes several legal
active-vertex orderings so ordering-independent claims can be tested under one
common degree-weighted adjacency-work counter.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Literal

import numpy as np

from src.graphs import GraphData

APPROrdering = Literal["fifo", "lifo", "max-ratio", "random"]
APPR_ORDERINGS: tuple[APPROrdering, ...] = ("fifo", "lifo", "max-ratio", "random")


@dataclass(frozen=True, slots=True)
class APPRResult:
    """Terminal APPR state and exact work statistics."""

    estimate: np.ndarray
    residual: np.ndarray
    pushes: int
    work: float
    push_counts: np.ndarray
    ordering: APPROrdering
    random_seed: int | None
    initial_mass: float
    push_trace: tuple[int, ...]


def approximate_pagerank(
    graph: GraphData,
    seed: int | np.ndarray,
    *,
    alpha: float,
    eps_appr: float,
    ordering: APPROrdering = "fifo",
    random_seed: int = 0,
    max_pushes: int | None = None,
    record_trace: bool = False,
) -> APPRResult:
    """Run classical lazy APPR on an unweighted undirected graph.

    A vertex ``u`` is active exactly when
    ``residual[u] >= eps_appr * degree[u]``. A push at ``u`` charges
    ``degree[u]`` adjacency-list work. The four ordering policies differ only
    in which currently active vertex they select.
    """

    if not 0.0 < alpha <= 1.0:
        raise ValueError(f"alpha must lie in (0, 1], got {alpha}")
    if eps_appr <= 0.0:
        raise ValueError(f"eps_appr must be positive, got {eps_appr}")
    if ordering not in APPR_ORDERINGS:
        choices = ", ".join(APPR_ORDERINGS)
        raise ValueError(f"unknown ordering {ordering!r}; expected one of: {choices}")
    if max_pushes is not None and max_pushes < 1:
        raise ValueError(f"max_pushes must be positive, got {max_pushes}")

    degree = np.asarray(graph.degree, dtype=np.float64)
    row_sizes = np.diff(graph.indptr)
    if np.any(degree <= 0.0):
        raise ValueError("classical APPR requires a graph without isolated vertices")
    if not np.array_equal(degree, row_sizes.astype(np.float64)):
        raise ValueError("classical APPR baseline requires an unweighted CSR graph")

    residual = _seed_vector(graph.n, seed)
    initial_mass = float(residual.sum())
    estimate = np.zeros(graph.n, dtype=np.float64)
    push_counts = np.zeros(graph.n, dtype=np.int64)
    threshold = eps_appr * degree
    lazy_factor = 0.5 * (1.0 - alpha)

    initially_active = [int(u) for u in np.flatnonzero(residual >= threshold)]
    active = set(initially_active)
    frontier = deque(initially_active)
    generator = np.random.default_rng(random_seed)
    trace: list[int] = []
    work = 0.0
    pushes = 0

    def activate(u: int) -> None:
        if residual[u] >= threshold[u] and u not in active:
            active.add(u)
            if ordering in ("fifo", "lifo"):
                frontier.append(u)

    def select_active() -> int:
        if ordering in ("fifo", "lifo"):
            while frontier:
                u = frontier.popleft() if ordering == "fifo" else frontier.pop()
                if u in active:
                    active.remove(u)
                    return u
            raise RuntimeError("active frontier became inconsistent")
        if ordering == "max-ratio":
            u = max(active, key=lambda node: (residual[node] / degree[node], -node))
        else:
            candidates = sorted(active)
            u = candidates[int(generator.integers(len(candidates)))]
        active.remove(u)
        return u

    while active:
        if max_pushes is not None and pushes >= max_pushes:
            raise RuntimeError(f"APPR exceeded max_pushes={max_pushes}")

        u = select_active()
        pushed_residual = residual[u]
        retained = lazy_factor * pushed_residual
        estimate[u] += alpha * pushed_residual
        residual[u] = retained

        start, stop = graph.indptr[u], graph.indptr[u + 1]
        neighbors = graph.indices[start:stop]
        increment = retained / degree[u]
        residual[neighbors] += increment

        pushes += 1
        work += degree[u]
        push_counts[u] += 1
        if record_trace:
            trace.append(u)

        activate(u)
        for neighbor in neighbors:
            activate(int(neighbor))

    return APPRResult(
        estimate=estimate,
        residual=residual,
        pushes=pushes,
        work=float(work),
        push_counts=push_counts,
        ordering=ordering,
        random_seed=random_seed if ordering == "random" else None,
        initial_mass=initial_mass,
        push_trace=tuple(trace),
    )


def _seed_vector(n: int, seed: int | np.ndarray) -> np.ndarray:
    if isinstance(seed, (int, np.integer)):
        vertex = int(seed)
        if not 0 <= vertex < n:
            raise ValueError(f"seed vertex must lie in [0, {n}), got {vertex}")
        vector = np.zeros(n, dtype=np.float64)
        vector[vertex] = 1.0
        return vector

    vector = np.array(seed, dtype=np.float64, copy=True)
    if vector.shape != (n,):
        raise ValueError(f"seed vector must have shape {(n,)}, got {vector.shape}")
    if not np.all(np.isfinite(vector)) or np.any(vector < 0.0):
        raise ValueError("seed vector must be finite and nonnegative")
    mass = float(vector.sum())
    if not 0.0 < mass <= 1.0 + 1e-12:
        raise ValueError(f"seed vector must have l1 mass in (0, 1], got {mass}")
    return vector
