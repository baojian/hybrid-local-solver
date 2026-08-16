"""Conjugate-gradient prototypes with graph-local work instrumentation.

The routines in this module deliberately separate two notions of locality:

* ``frontier_sparse_cg`` runs the exact ordinary CG recurrence.  Starting
  from a seed-supported right-hand side, its directions propagate by at most
  one graph hop per iteration, but they are never thresholded.
* ``restarted_evolving_set_cg`` freezes an explored vertex set, runs CG on
  the corresponding principal system, inspects the true boundary residual,
  expands the set, and restarts CG.

Both solvers use the shared manuscript system

    Q = alpha I + (1 - alpha) / 2 * (I - D^{-1/2} A D^{-1/2}),
    b = alpha D^{-1/2} e_source.

The stopping rule is note-scoped rather than repository-wide: a result is
certified when ``max_i |r_i| / sqrt(d_i) <= alpha * eps_ppr`` for the
verifier-owned residual ``r = b - Qx``.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import scipy.sparse as sp

from src.graphs import GraphData


@dataclass(frozen=True, slots=True)
class CGTrace:
    """Per-iteration diagnostics for ordinary frontier-sparse CG."""

    residual_scaled_inf: tuple[float, ...]
    direction_support_size: tuple[int, ...]
    direction_volume: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class EvolvingCGTrace:
    """Per-epoch diagnostics for the restarted evolving-set solver."""

    active_size: tuple[int, ...]
    active_volume: tuple[float, ...]
    added_size: tuple[int, ...]
    inner_iterations: tuple[int, ...]
    residual_scaled_inf: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class CGResult:
    """Common result record for the exploratory CG solvers."""

    solution: np.ndarray
    residual: np.ndarray
    certified: bool
    termination_reason: str
    edge_operations: float
    local_inner_iterations: int
    outer_restarts: int
    explored_vertices: np.ndarray
    trace: CGTrace | EvolvingCGTrace


def pagerank_matrix(graph: GraphData, alpha: float) -> sp.csr_matrix:
    """Materialize the shared symmetric PageRank matrix for verification."""
    _validate_inputs(graph, alpha, eps_ppr=1.0)
    inverse_sqrt_degree = 1.0 / np.sqrt(graph.degree)
    normalized_adjacency = (
        sp.diags(inverse_sqrt_degree) @ graph.adjacency @ sp.diags(inverse_sqrt_degree)
    )
    diagonal = (1.0 + alpha) / 2.0
    off_diagonal = (1.0 - alpha) / 2.0
    return (diagonal * sp.eye(graph.n) - off_diagonal * normalized_adjacency).tocsr()


def pagerank_rhs(graph: GraphData, alpha: float, source: int) -> np.ndarray:
    """Return ``alpha * D^{-1/2} e_source`` under the shared convention."""
    _validate_inputs(graph, alpha, eps_ppr=1.0)
    if not 0 <= source < graph.n:
        raise ValueError(f"source must lie in [0, {graph.n}), got {source}")
    right_hand_side = np.zeros(graph.n, dtype=float)
    right_hand_side[source] = alpha / np.sqrt(graph.degree[source])
    return right_hand_side


def frontier_sparse_cg(
    graph: GraphData,
    *,
    alpha: float,
    source: int,
    eps_ppr: float,
    max_iterations: int | None = None,
) -> CGResult:
    """Run ordinary CG while scanning only the current direction support.

    This is algebraically standard CG: no residual or direction entry is
    thresholded.  The sparse implementation only avoids graph scans at exact
    zero coordinates.  Dense vector arithmetic is not included in the graph
    edge-operation count.
    """
    _validate_inputs(graph, alpha, eps_ppr)
    iteration_limit = graph.n if max_iterations is None else max_iterations
    if iteration_limit < 0:
        raise ValueError(f"max_iterations must be nonnegative, got {iteration_limit}")

    right_hand_side = pagerank_rhs(graph, alpha, source)
    solution = np.zeros(graph.n, dtype=float)
    residual = right_hand_side.copy()
    direction = residual.copy()
    residual_square = float(residual @ residual)
    certificate_threshold = alpha * eps_ppr

    edge_operations = 0.0
    explored = np.zeros(graph.n, dtype=bool)
    residual_history: list[float] = []
    support_size_history: list[int] = []
    direction_volume_history: list[float] = []
    termination_reason = "iteration_limit"

    for _ in range(iteration_limit):
        if residual_square <= 0.0:
            termination_reason = "exact_zero_residual"
            break

        product, product_work, support = _apply_q_local(graph, alpha, direction)
        explored[support] = True
        edge_operations += product_work
        support_size_history.append(int(support.size))
        direction_volume_history.append(float(np.sum(graph.degree[support])))

        denominator = float(direction @ product)
        if not denominator > 0.0:
            termination_reason = "nonpositive_curvature"
            break

        step = residual_square / denominator
        solution += step * direction
        residual -= step * product
        scaled_residual = _scaled_inf_norm(residual, graph.degree)
        residual_history.append(scaled_residual)
        if scaled_residual <= certificate_threshold:
            termination_reason = "recursive_residual_certificate"
            break

        next_residual_square = float(residual @ residual)
        if next_residual_square <= 0.0:
            residual_square = next_residual_square
            termination_reason = "exact_zero_residual"
            break
        direction = residual + (next_residual_square / residual_square) * direction
        residual_square = next_residual_square

    verified_residual, verification_work = _true_residual(
        graph,
        alpha,
        right_hand_side,
        solution,
    )
    edge_operations += verification_work
    certified = _scaled_inf_norm(verified_residual, graph.degree) <= certificate_threshold
    if certified:
        termination_reason = "verified_residual_certificate"

    return CGResult(
        solution=solution,
        residual=verified_residual,
        certified=certified,
        termination_reason=termination_reason,
        edge_operations=edge_operations,
        local_inner_iterations=len(support_size_history),
        outer_restarts=0,
        explored_vertices=np.flatnonzero(explored),
        trace=CGTrace(
            residual_scaled_inf=tuple(residual_history),
            direction_support_size=tuple(support_size_history),
            direction_volume=tuple(direction_volume_history),
        ),
    )


def restarted_evolving_set_cg(
    graph: GraphData,
    *,
    alpha: float,
    source: int,
    eps_ppr: float,
    inner_tolerance_fraction: float = 0.25,
    max_epochs: int | None = None,
    max_inner_iterations: int | None = None,
) -> CGResult:
    """Run CG epochs on nested principal systems selected by boundary residual.

    At epoch ``j``, CG solves the fixed system on the current explored set
    ``U_j``.  The full residual is then recomputed locally from ``supp(x)``.
    Every outside coordinate violating the note-scoped residual certificate
    is added in one batch, and CG is restarted on the expanded principal
    system.  No live CG direction is projected onto a changing set.
    """
    _validate_inputs(graph, alpha, eps_ppr)
    if not 0.0 < inner_tolerance_fraction < 1.0:
        raise ValueError("inner_tolerance_fraction must lie in (0, 1)")
    epoch_limit = graph.n if max_epochs is None else max_epochs
    if epoch_limit < 1:
        raise ValueError(f"max_epochs must be positive, got {epoch_limit}")
    if max_inner_iterations is not None and max_inner_iterations < 0:
        raise ValueError(f"max_inner_iterations must be nonnegative, got {max_inner_iterations}")

    right_hand_side = pagerank_rhs(graph, alpha, source)
    solution = np.zeros(graph.n, dtype=float)
    active = np.zeros(graph.n, dtype=bool)
    active[source] = True
    certificate_threshold = alpha * eps_ppr
    inner_threshold = inner_tolerance_fraction * certificate_threshold

    edge_operations = 0.0
    total_inner_iterations = 0
    restarts = 0
    active_size_history: list[int] = []
    active_volume_history: list[float] = []
    added_size_history: list[int] = []
    inner_iteration_history: list[int] = []
    residual_history: list[float] = []
    termination_reason = "epoch_limit"
    verified_residual = right_hand_side.copy()

    for _ in range(epoch_limit):
        inner_limit = int(np.count_nonzero(active))
        if max_inner_iterations is not None:
            inner_limit = min(inner_limit, max_inner_iterations)
        solution, inner_work, inner_iterations = _restricted_cg_epoch(
            graph,
            alpha,
            right_hand_side,
            solution,
            active,
            inner_threshold,
            inner_limit,
        )
        edge_operations += inner_work
        total_inner_iterations += inner_iterations

        verified_residual, verification_work = _true_residual(
            graph,
            alpha,
            right_hand_side,
            solution,
        )
        edge_operations += verification_work
        scaled_residual = _scaled_inf_norm(verified_residual, graph.degree)

        active_size_history.append(int(np.count_nonzero(active)))
        active_volume_history.append(float(np.sum(graph.degree[active])))
        inner_iteration_history.append(inner_iterations)
        residual_history.append(scaled_residual)

        if scaled_residual <= certificate_threshold:
            added_size_history.append(0)
            termination_reason = "verified_residual_certificate"
            break

        outside_violations = (~active) & (
            np.abs(verified_residual) > certificate_threshold * np.sqrt(graph.degree)
        )
        added_size = int(np.count_nonzero(outside_violations))
        added_size_history.append(added_size)
        if added_size == 0:
            termination_reason = "uncertified_interior_residual"
            break

        active |= outside_violations
        restarts += 1

    certified = _scaled_inf_norm(verified_residual, graph.degree) <= certificate_threshold
    return CGResult(
        solution=solution,
        residual=verified_residual,
        certified=certified,
        termination_reason=termination_reason,
        edge_operations=edge_operations,
        local_inner_iterations=total_inner_iterations,
        outer_restarts=restarts,
        explored_vertices=np.flatnonzero(active),
        trace=EvolvingCGTrace(
            active_size=tuple(active_size_history),
            active_volume=tuple(active_volume_history),
            added_size=tuple(added_size_history),
            inner_iterations=tuple(inner_iteration_history),
            residual_scaled_inf=tuple(residual_history),
        ),
    )


def _restricted_cg_epoch(
    graph: GraphData,
    alpha: float,
    right_hand_side: np.ndarray,
    initial_solution: np.ndarray,
    active: np.ndarray,
    inner_threshold: float,
    iteration_limit: int,
) -> tuple[np.ndarray, float, int]:
    """Warm-start CG on one fixed principal system."""
    solution = initial_solution.copy()
    solution[~active] = 0.0
    product, edge_operations, _ = _apply_q_local(
        graph,
        alpha,
        solution,
        output_mask=active,
    )
    residual = np.zeros(graph.n, dtype=float)
    residual[active] = right_hand_side[active] - product[active]
    if _scaled_inf_norm(residual[active], graph.degree[active]) <= inner_threshold:
        return solution, edge_operations, 0

    direction = residual.copy()
    residual_square = float(residual @ residual)
    iterations = 0
    for _ in range(iteration_limit):
        product, product_work, _ = _apply_q_local(
            graph,
            alpha,
            direction,
            output_mask=active,
        )
        edge_operations += product_work
        denominator = float(direction @ product)
        if not denominator > 0.0:
            break
        step = residual_square / denominator
        solution += step * direction
        residual -= step * product
        residual[~active] = 0.0
        iterations += 1
        if _scaled_inf_norm(residual[active], graph.degree[active]) <= inner_threshold:
            break
        next_residual_square = float(residual @ residual)
        if next_residual_square <= 0.0:
            break
        direction = residual + (next_residual_square / residual_square) * direction
        direction[~active] = 0.0
        residual_square = next_residual_square
    return solution, edge_operations, iterations


def _true_residual(
    graph: GraphData,
    alpha: float,
    right_hand_side: np.ndarray,
    solution: np.ndarray,
) -> tuple[np.ndarray, float]:
    product, work, _ = _apply_q_local(graph, alpha, solution)
    return right_hand_side - product, work


def _apply_q_local(
    graph: GraphData,
    alpha: float,
    vector: np.ndarray,
    *,
    output_mask: np.ndarray | None = None,
) -> tuple[np.ndarray, float, np.ndarray]:
    """Apply ``Q`` by scanning adjacency lists of exact nonzeros in ``vector``."""
    support = np.flatnonzero(vector != 0.0)
    product = np.zeros(graph.n, dtype=float)
    diagonal = (1.0 + alpha) / 2.0
    off_diagonal = (1.0 - alpha) / 2.0
    inverse_sqrt_degree = 1.0 / np.sqrt(graph.degree)
    edge_operations = 0.0

    for node in support:
        value = vector[node]
        if output_mask is None or output_mask[node]:
            product[node] += diagonal * value
        neighbors = graph.indices[graph.indptr[node] : graph.indptr[node + 1]]
        edge_operations += float(graph.degree[node])
        if output_mask is not None:
            neighbors = neighbors[output_mask[neighbors]]
        product[neighbors] -= (
            off_diagonal * value * inverse_sqrt_degree[node] * inverse_sqrt_degree[neighbors]
        )
    return product, edge_operations, support


def _scaled_inf_norm(vector: np.ndarray, degree: np.ndarray) -> float:
    if vector.size == 0:
        return 0.0
    return float(np.max(np.abs(vector) / np.sqrt(degree)))


def _validate_inputs(graph: GraphData, alpha: float, eps_ppr: float) -> None:
    if not 0.0 < alpha <= 1.0:
        raise ValueError(f"alpha must lie in (0, 1], got {alpha}")
    if not eps_ppr > 0.0:
        raise ValueError(f"eps_ppr must be positive, got {eps_ppr}")
    if np.any(graph.degree <= 0.0):
        raise ValueError("CG PageRank prototypes require a graph without isolated vertices")
