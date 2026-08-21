"""Exact reference backend for response--iterative local-solver experiments.

This module implements the algebraic interface from the response-preconditioned
hybrid note.  It is intentionally a dense correctness oracle, not a scalable
local SDD solver: the full PageRank matrix is materialized, boundary residuals
are read globally, and every response update records a dense-arithmetic charge.

The controller maintains an exact inverse on a settled anchor.  A light set of
new vertices remains in a frontier and is solved by warm-started CG on the
anchor Schur complement.  Once combined degree volume grows geometrically, the
frontier is absorbed into the anchor by the exact bordered-inverse identity.

The stopping rule is note-scoped and matches ``evolving_cg``:

    max_i |b_i - (Qx)_i| / sqrt(d_i) <= alpha * eps_ppr.

No repository-wide residual convention or output-sensitive complexity claim is
adopted here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from src.graphs import GraphData
from src.hybrid_solver_codex.evolving_cg import pagerank_matrix, pagerank_rhs


@dataclass(frozen=True, slots=True)
class ResponseUpdate:
    """Diagnostics for one exact bordered response update."""

    added_vertices: tuple[int, ...]
    anchor_size_before: int
    anchor_size_after: int
    schur_min_eigenvalue: float
    dense_flop_estimate: float


@dataclass(frozen=True, slots=True)
class FrontierSolve:
    """Result of eliminating the anchor and iterating on one frontier."""

    solution: np.ndarray
    iterations: int
    converged: bool
    residual_scaled_inf: float
    warm_started: bool
    schur_build_flop_estimate: float
    iteration_flop_estimate: float


@dataclass(frozen=True, slots=True)
class ResponseHybridWork:
    """Fully separated work ledger for the dense reference implementation."""

    q_edge_operations: float
    boundary_coordinate_reads: int
    response_updates: int
    response_update_dense_flops: float
    schur_build_dense_flops: float
    frontier_iteration_dense_flops: float
    frontier_cg_iterations: int
    active_materialization_writes: int
    final_output_writes: int


@dataclass(frozen=True, slots=True)
class ResponseHybridTrace:
    """Per-epoch anchor, frontier, certificate, and switching diagnostics."""

    anchor_size: tuple[int, ...]
    anchor_volume: tuple[float, ...]
    frontier_size: tuple[int, ...]
    frontier_volume: tuple[float, ...]
    added_size: tuple[int, ...]
    frontier_iterations: tuple[int, ...]
    residual_scaled_inf: tuple[float, ...]
    response_rebuilt: tuple[bool, ...]
    frontier_warm_started: tuple[bool, ...]


@dataclass(frozen=True, slots=True)
class ResponseHybridResult:
    """Terminal state returned by :func:`dense_response_frontier_hybrid`."""

    solution: np.ndarray
    residual: np.ndarray
    certified: bool
    termination_reason: str
    explored_vertices: np.ndarray
    work: ResponseHybridWork
    trace: ResponseHybridTrace

    @property
    def edge_operations(self) -> float:
        """Degree-weighted adjacency scans used by verifier-owned Q products."""
        return self.work.q_edge_operations

    @property
    def local_inner_iterations(self) -> int:
        """Total CG iterations on reduced frontier systems."""
        return self.work.frontier_cg_iterations

    @property
    def outer_restarts(self) -> int:
        """Number of post-initial exact response rebuilds."""
        return max(0, self.work.response_updates - 1)


class DenseNestedResponse:
    """Maintain exact principal inverses by bordered Schur updates.

    The class receives a full dense SPD matrix and therefore acts only as a
    reference oracle.  Vertex order is the order in which vertices are
    absorbed.  ``inverse`` is exposed as a defensive copy for verification.
    """

    def __init__(self, matrix: np.ndarray) -> None:
        dense = np.asarray(matrix, dtype=float)
        if dense.ndim != 2 or dense.shape[0] != dense.shape[1]:
            raise ValueError(f"matrix must be square, got shape {dense.shape}")
        if not np.all(np.isfinite(dense)):
            raise ValueError("matrix must contain only finite entries")
        if not np.allclose(dense, dense.T, rtol=1.0e-12, atol=1.0e-14):
            raise ValueError("matrix must be symmetric")
        self._matrix = dense.copy()
        self._vertices = np.empty(0, dtype=np.int64)
        self._inverse = np.empty((0, 0), dtype=float)

    @property
    def n(self) -> int:
        return int(self._matrix.shape[0])

    @property
    def vertices(self) -> np.ndarray:
        return self._vertices.copy()

    @property
    def inverse(self) -> np.ndarray:
        return self._inverse.copy()

    def expand(self, vertices: Iterable[int] | np.ndarray) -> ResponseUpdate:
        """Absorb new vertices using the exact block-inverse identity."""
        new_vertices = self._validated_new_vertices(vertices)
        if new_vertices.size == 0:
            raise ValueError("response expansion requires at least one new vertex")

        old_vertices = self._vertices
        old_inverse = self._inverse
        old_size = int(old_vertices.size)
        new_size = int(new_vertices.size)
        new_block = self._matrix[np.ix_(new_vertices, new_vertices)]

        if old_size == 0:
            schur = new_block
            schur_inverse = _spd_inverse(schur)
            updated_inverse = schur_inverse
        else:
            coupling = self._matrix[np.ix_(old_vertices, new_vertices)]
            inverse_coupling = old_inverse @ coupling
            schur = new_block - coupling.T @ inverse_coupling
            schur = 0.5 * (schur + schur.T)
            schur_inverse = _spd_inverse(schur)
            top_right = -inverse_coupling @ schur_inverse
            top_left = old_inverse + inverse_coupling @ schur_inverse @ inverse_coupling.T
            updated_inverse = np.block(
                [
                    [top_left, top_right],
                    [top_right.T, schur_inverse],
                ]
            )

        self._vertices = np.concatenate((old_vertices, new_vertices))
        self._inverse = 0.5 * (updated_inverse + updated_inverse.T)
        minimum_eigenvalue = float(np.linalg.eigvalsh(schur)[0])
        return ResponseUpdate(
            added_vertices=tuple(int(vertex) for vertex in new_vertices),
            anchor_size_before=old_size,
            anchor_size_after=old_size + new_size,
            schur_min_eigenvalue=minimum_eigenvalue,
            dense_flop_estimate=_response_update_flops(old_size, new_size),
        )

    def solve_active(self, right_hand_side: np.ndarray) -> np.ndarray:
        """Return the exact current principal solution in ambient coordinates."""
        rhs = self._validated_rhs(right_hand_side)
        solution = np.zeros(self.n, dtype=float)
        if self._vertices.size:
            solution[self._vertices] = self._inverse @ rhs[self._vertices]
        return solution

    def reduced_frontier_system(
        self,
        right_hand_side: np.ndarray,
        frontier: Iterable[int] | np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Return the anchor Schur complement and its reduced right-hand side."""
        rhs = self._validated_rhs(right_hand_side)
        frontier_vertices = self._validated_new_vertices(frontier)
        frontier_block = self._matrix[np.ix_(frontier_vertices, frontier_vertices)]
        if self._vertices.size == 0:
            return frontier_block, rhs[frontier_vertices].copy()

        coupling = self._matrix[np.ix_(self._vertices, frontier_vertices)]
        inverse_coupling = self._inverse @ coupling
        schur = frontier_block - coupling.T @ inverse_coupling
        reduced_rhs = rhs[frontier_vertices] - coupling.T @ (self._inverse @ rhs[self._vertices])
        return 0.5 * (schur + schur.T), reduced_rhs

    def lift_frontier_vector(
        self,
        frontier: Iterable[int] | np.ndarray,
        frontier_vector: np.ndarray,
    ) -> np.ndarray:
        """Lift a Schur-frontier vector into the current ambient face.

        If the settled anchor is ``S`` and ``frontier`` is ``B``, this
        returns the vector with frontier block ``y`` and anchor block
        ``-Q_SS^{-1} Q_SB y``.  Multiplication by ``Q`` therefore vanishes
        on ``S``.  The method is a dense diagnostic realization of the
        orthogonal lifted-frontier operator used in the accompanying note;
        it is not a locality claim.
        """
        frontier_vertices = self._validated_new_vertices(frontier)
        values = np.asarray(frontier_vector, dtype=float)
        if values.shape != (frontier_vertices.size,) or not np.all(np.isfinite(values)):
            raise ValueError(
                "frontier_vector must be finite and match the number of frontier vertices"
            )

        lifted = np.zeros(self.n, dtype=float)
        lifted[frontier_vertices] = values
        if self._vertices.size and frontier_vertices.size:
            coupling = self._matrix[np.ix_(self._vertices, frontier_vertices)]
            lifted[self._vertices] = -(self._inverse @ coupling @ values)
        return lifted

    def normalized_frontier_lift(
        self,
        frontier: Iterable[int] | np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Return an energy-orthonormal basis for one lifted frontier.

        The returned ambient matrix is L K^{-1/2}, where K is the exact
        frontier Schur complement and L is the frontier lift. Its columns are
        orthonormal in the full-matrix energy inner product. Bases produced at
        successive nested expansions are mutually energy-orthogonal.
        """
        frontier_vertices = self._validated_new_vertices(frontier)
        frontier_size = int(frontier_vertices.size)
        if frontier_size == 0:
            return np.empty((self.n, 0), dtype=float), np.empty((0, 0), dtype=float)

        frontier_block = self._matrix[np.ix_(frontier_vertices, frontier_vertices)]
        if self._vertices.size:
            coupling = self._matrix[np.ix_(self._vertices, frontier_vertices)]
            inverse_coupling = self._inverse @ coupling
            schur = frontier_block - coupling.T @ inverse_coupling
        else:
            inverse_coupling = np.empty((0, frontier_size), dtype=float)
            schur = frontier_block
        schur = 0.5 * (schur + schur.T)
        inverse_square_root = _spd_inverse_square_root(schur)

        basis = np.zeros((self.n, frontier_size), dtype=float)
        basis[frontier_vertices, :] = inverse_square_root
        if self._vertices.size:
            basis[self._vertices, :] = -(inverse_coupling @ inverse_square_root)
        return basis, schur

    def solve_with_frontier(
        self,
        right_hand_side: np.ndarray,
        frontier: Iterable[int] | np.ndarray,
        degree: np.ndarray,
        *,
        tolerance: float,
        initial_solution: np.ndarray | None = None,
        max_iterations: int | None = None,
    ) -> FrontierSolve:
        """Eliminate the anchor and run ordinary CG on the frontier Schur system."""
        rhs = self._validated_rhs(right_hand_side)
        degrees = np.asarray(degree, dtype=float)
        if degrees.shape != (self.n,) or np.any(degrees <= 0.0):
            raise ValueError("degree must be positive and match the matrix dimension")
        if not np.isfinite(tolerance) or tolerance <= 0.0:
            raise ValueError("tolerance must be finite and positive")
        frontier_vertices = self._validated_new_vertices(frontier)
        frontier_size = int(frontier_vertices.size)
        if max_iterations is None:
            iteration_limit = frontier_size
        else:
            if max_iterations < 0:
                raise ValueError("max_iterations must be nonnegative")
            iteration_limit = max_iterations

        if initial_solution is None:
            initial = np.zeros(self.n, dtype=float)
        else:
            initial = np.asarray(initial_solution, dtype=float)
            if initial.shape != (self.n,) or not np.all(np.isfinite(initial)):
                raise ValueError("initial_solution must be finite and match the matrix dimension")

        if frontier_size == 0:
            return FrontierSolve(
                solution=self.solve_active(rhs),
                iterations=0,
                converged=True,
                residual_scaled_inf=0.0,
                warm_started=False,
                schur_build_flop_estimate=0.0,
                iteration_flop_estimate=0.0,
            )

        schur, reduced_rhs = self.reduced_frontier_system(rhs, frontier_vertices)
        frontier_solution = initial[frontier_vertices].copy()
        warm_started = bool(np.any(frontier_solution != 0.0))
        frontier_residual = reduced_rhs - schur @ frontier_solution
        direction = frontier_residual.copy()
        residual_square = float(frontier_residual @ frontier_residual)
        iterations = 0

        while (
            _scaled_inf(frontier_residual, degrees[frontier_vertices]) > tolerance
            and iterations < iteration_limit
            and residual_square > 0.0
        ):
            product = schur @ direction
            denominator = float(direction @ product)
            if denominator <= 0.0:
                break
            step = residual_square / denominator
            frontier_solution += step * direction
            frontier_residual -= step * product
            iterations += 1
            next_residual_square = float(frontier_residual @ frontier_residual)
            if next_residual_square <= 0.0:
                residual_square = next_residual_square
                break
            direction = frontier_residual + (next_residual_square / residual_square) * direction
            residual_square = next_residual_square

        solution = np.zeros(self.n, dtype=float)
        solution[frontier_vertices] = frontier_solution
        if self._vertices.size:
            coupling = self._matrix[np.ix_(self._vertices, frontier_vertices)]
            solution[self._vertices] = self._inverse @ (
                rhs[self._vertices] - coupling @ frontier_solution
            )

        active_vertices = np.concatenate((self._vertices, frontier_vertices))
        active_residual = (
            rhs[active_vertices]
            - self._matrix[np.ix_(active_vertices, active_vertices)] @ solution[active_vertices]
        )
        scaled_residual = _scaled_inf(active_residual, degrees[active_vertices])
        anchor_size = int(self._vertices.size)
        return FrontierSolve(
            solution=solution,
            iterations=iterations,
            converged=scaled_residual <= tolerance,
            residual_scaled_inf=scaled_residual,
            warm_started=warm_started,
            schur_build_flop_estimate=_schur_build_flops(anchor_size, frontier_size),
            iteration_flop_estimate=float(iterations * (2 * frontier_size**2 + 8 * frontier_size)),
        )

    def _validated_new_vertices(
        self,
        vertices: Iterable[int] | np.ndarray,
    ) -> np.ndarray:
        raw = np.asarray(list(vertices) if not isinstance(vertices, np.ndarray) else vertices)
        if raw.ndim != 1:
            raise ValueError("vertices must be one-dimensional")
        if raw.size == 0:
            return np.empty(0, dtype=np.int64)
        if not np.issubdtype(raw.dtype, np.integer):
            raise ValueError("vertices must contain integers")
        values = raw.astype(np.int64, copy=False)
        if np.any(values < 0) or np.any(values >= self.n):
            raise ValueError(f"vertices must lie in [0, {self.n})")
        if np.unique(values).size != values.size:
            raise ValueError("vertices must not contain duplicates")
        if np.intersect1d(values, self._vertices, assume_unique=False).size:
            raise ValueError("frontier vertices must be disjoint from the settled anchor")
        return values.copy()

    def _validated_rhs(self, right_hand_side: np.ndarray) -> np.ndarray:
        rhs = np.asarray(right_hand_side, dtype=float)
        if rhs.shape != (self.n,) or not np.all(np.isfinite(rhs)):
            raise ValueError("right_hand_side must be finite and match the matrix dimension")
        return rhs


def dense_response_frontier_hybrid(
    graph: GraphData,
    *,
    alpha: float,
    source: int,
    eps_ppr: float,
    rebuild_volume_factor: float = 2.0,
    probe_frontier_before_rebuild: bool = True,
    inner_tolerance_fraction: float = 0.25,
    max_epochs: int | None = None,
    max_frontier_iterations: int | None = None,
) -> ResponseHybridResult:
    """Run the exact-response/warm-frontier reference controller.

    ``rebuild_volume_factor=1`` absorbs every detected batch immediately and
    gives the pure persistent-response endpoint.  ``math.inf`` never rebuilds
    after the source and gives the exact-anchor/iterative-frontier endpoint.
    Intermediate factors implement geometric heavy/light switching.  With
    ``probe_frontier_before_rebuild=True``, every new frontier receives one
    converged Schur-CG solve before it can be absorbed; a heavy but easy batch
    can therefore certify without an unnecessary dense response update.
    """
    _validate_controller_inputs(
        graph,
        alpha=alpha,
        source=source,
        eps_ppr=eps_ppr,
        rebuild_volume_factor=rebuild_volume_factor,
        probe_frontier_before_rebuild=probe_frontier_before_rebuild,
        inner_tolerance_fraction=inner_tolerance_fraction,
        max_epochs=max_epochs,
        max_frontier_iterations=max_frontier_iterations,
    )
    epoch_limit = graph.n + 1 if max_epochs is None else max_epochs
    matrix = pagerank_matrix(graph, alpha).toarray()
    right_hand_side = pagerank_rhs(graph, alpha, source)
    response = DenseNestedResponse(matrix)
    initial_update = response.expand([source])
    frontier = np.empty(0, dtype=np.int64)
    solution = np.zeros(graph.n, dtype=float)
    residual = right_hand_side.copy()
    certificate_threshold = alpha * eps_ppr
    inner_threshold = inner_tolerance_fraction * certificate_threshold

    q_edge_operations = 0.0
    boundary_coordinate_reads = 0
    response_updates = 1
    response_update_flops = initial_update.dense_flop_estimate
    schur_build_flops = 0.0
    frontier_iteration_flops = 0.0
    frontier_iterations_total = 0
    active_materialization_writes = 0

    anchor_size_history: list[int] = []
    anchor_volume_history: list[float] = []
    frontier_size_history: list[int] = []
    frontier_volume_history: list[float] = []
    added_size_history: list[int] = []
    frontier_iteration_history: list[int] = []
    residual_history: list[float] = []
    response_rebuilt_history: list[bool] = []
    warm_started_history: list[bool] = []
    termination_reason = "epoch_limit"

    for _ in range(epoch_limit):
        anchor = response.vertices
        frontier_limit = max_frontier_iterations
        frontier_solve = response.solve_with_frontier(
            right_hand_side,
            frontier,
            graph.degree,
            tolerance=inner_threshold,
            initial_solution=solution,
            max_iterations=frontier_limit,
        )
        solution = frontier_solve.solution
        active = np.concatenate((anchor, frontier))
        active_mask = np.zeros(graph.n, dtype=bool)
        active_mask[active] = True
        active_materialization_writes += int(active.size)
        residual, verifier_work = _local_true_residual(
            graph,
            alpha,
            right_hand_side,
            solution,
            active,
        )
        scaled_residual = _scaled_inf(residual, graph.degree)
        q_edge_operations += verifier_work
        boundary_coordinate_reads += graph.n
        schur_build_flops += frontier_solve.schur_build_flop_estimate
        frontier_iteration_flops += frontier_solve.iteration_flop_estimate
        frontier_iterations_total += frontier_solve.iterations

        anchor_volume = float(np.sum(graph.degree[anchor]))
        frontier_volume = float(np.sum(graph.degree[frontier]))
        anchor_size_history.append(int(anchor.size))
        anchor_volume_history.append(anchor_volume)
        frontier_size_history.append(int(frontier.size))
        frontier_volume_history.append(frontier_volume)
        frontier_iteration_history.append(frontier_solve.iterations)
        residual_history.append(scaled_residual)
        warm_started_history.append(frontier_solve.warm_started)

        if scaled_residual <= certificate_threshold:
            added_size_history.append(0)
            response_rebuilt_history.append(False)
            termination_reason = "verified_residual_certificate"
            break
        if not frontier_solve.converged:
            added_size_history.append(0)
            response_rebuilt_history.append(False)
            termination_reason = "frontier_iteration_limit"
            break

        response_rebuilt = False
        if probe_frontier_before_rebuild and frontier.size:
            combined_volume = anchor_volume + frontier_volume
            if combined_volume >= rebuild_volume_factor * anchor_volume:
                update = response.expand(frontier)
                response_updates += 1
                response_update_flops += update.dense_flop_estimate
                frontier = np.empty(0, dtype=np.int64)
                response_rebuilt = True

        outside_violations = (~active_mask) & (
            np.abs(residual) > certificate_threshold * np.sqrt(graph.degree)
        )
        additions = np.flatnonzero(outside_violations).astype(np.int64, copy=False)
        if additions.size == 0:
            added_size_history.append(0)
            response_rebuilt_history.append(response_rebuilt)
            termination_reason = "uncertified_without_boundary_violation"
            break

        added_size_history.append(int(additions.size))
        frontier = np.concatenate((frontier, additions))
        if not probe_frontier_before_rebuild:
            combined_volume = anchor_volume + float(np.sum(graph.degree[frontier]))
            if combined_volume >= rebuild_volume_factor * anchor_volume:
                update = response.expand(frontier)
                response_updates += 1
                response_update_flops += update.dense_flop_estimate
                frontier = np.empty(0, dtype=np.int64)
                response_rebuilt = True
        response_rebuilt_history.append(response_rebuilt)

    certified = _scaled_inf(residual, graph.degree) <= certificate_threshold
    explored_vertices = np.concatenate((response.vertices, frontier))
    work = ResponseHybridWork(
        q_edge_operations=q_edge_operations,
        boundary_coordinate_reads=boundary_coordinate_reads,
        response_updates=response_updates,
        response_update_dense_flops=response_update_flops,
        schur_build_dense_flops=schur_build_flops,
        frontier_iteration_dense_flops=frontier_iteration_flops,
        frontier_cg_iterations=frontier_iterations_total,
        active_materialization_writes=active_materialization_writes,
        final_output_writes=int(np.count_nonzero(solution)),
    )
    return ResponseHybridResult(
        solution=solution,
        residual=residual,
        certified=certified,
        termination_reason=termination_reason,
        explored_vertices=explored_vertices,
        work=work,
        trace=ResponseHybridTrace(
            anchor_size=tuple(anchor_size_history),
            anchor_volume=tuple(anchor_volume_history),
            frontier_size=tuple(frontier_size_history),
            frontier_volume=tuple(frontier_volume_history),
            added_size=tuple(added_size_history),
            frontier_iterations=tuple(frontier_iteration_history),
            residual_scaled_inf=tuple(residual_history),
            response_rebuilt=tuple(response_rebuilt_history),
            frontier_warm_started=tuple(warm_started_history),
        ),
    )


def _spd_inverse(matrix: np.ndarray) -> np.ndarray:
    try:
        factor = np.linalg.cholesky(matrix)
    except np.linalg.LinAlgError as error:
        raise ValueError("new Schur block must be positive definite") from error
    identity = np.eye(matrix.shape[0], dtype=float)
    return np.linalg.solve(factor.T, np.linalg.solve(factor, identity))


def _spd_inverse_square_root(matrix: np.ndarray) -> np.ndarray:
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    if eigenvalues.size and eigenvalues[0] <= 0.0:
        raise ValueError("new Schur block must be positive definite")
    return (eigenvectors * (eigenvalues**-0.5)) @ eigenvectors.T


def _local_true_residual(
    graph: GraphData,
    alpha: float,
    right_hand_side: np.ndarray,
    solution: np.ndarray,
    active: np.ndarray,
) -> tuple[np.ndarray, float]:
    """Recompute ``b - Qx`` by scanning adjacency only from the active set."""
    product = np.zeros(graph.n, dtype=float)
    diagonal = (1.0 + alpha) / 2.0
    off_diagonal = (1.0 - alpha) / 2.0
    inverse_sqrt_degree = 1.0 / np.sqrt(graph.degree)
    edge_operations = 0.0
    for node in active:
        value = solution[node]
        product[node] += diagonal * value
        neighbors = graph.indices[graph.indptr[node] : graph.indptr[node + 1]]
        product[neighbors] -= (
            off_diagonal * value * inverse_sqrt_degree[node] * inverse_sqrt_degree[neighbors]
        )
        edge_operations += float(graph.degree[node])
    return right_hand_side - product, edge_operations


def _scaled_inf(vector: np.ndarray, degree: np.ndarray) -> float:
    if vector.size == 0:
        return 0.0
    return float(np.max(np.abs(vector) / np.sqrt(degree)))


def _response_update_flops(anchor_size: int, frontier_size: int) -> float:
    return float(
        frontier_size**3 + 2 * anchor_size**2 * frontier_size + 4 * anchor_size * frontier_size**2
    )


def _schur_build_flops(anchor_size: int, frontier_size: int) -> float:
    if anchor_size == 0 or frontier_size == 0:
        return 0.0
    return float(
        anchor_size**2 * frontier_size
        + anchor_size * frontier_size**2
        + anchor_size**2
        + anchor_size * frontier_size
    )


def _validate_controller_inputs(
    graph: GraphData,
    *,
    alpha: float,
    source: int,
    eps_ppr: float,
    rebuild_volume_factor: float,
    probe_frontier_before_rebuild: bool,
    inner_tolerance_fraction: float,
    max_epochs: int | None,
    max_frontier_iterations: int | None,
) -> None:
    if not 0.0 < alpha <= 1.0:
        raise ValueError(f"alpha must lie in (0, 1], got {alpha}")
    if not eps_ppr > 0.0:
        raise ValueError(f"eps_ppr must be positive, got {eps_ppr}")
    if not 0 <= source < graph.n:
        raise ValueError(f"source must lie in [0, {graph.n}), got {source}")
    if np.any(graph.degree <= 0.0):
        raise ValueError("response reference requires a graph without isolated vertices")
    if np.isnan(rebuild_volume_factor) or rebuild_volume_factor < 1.0:
        raise ValueError("rebuild_volume_factor must be at least 1 or positive infinity")
    if not isinstance(probe_frontier_before_rebuild, bool):
        raise ValueError("probe_frontier_before_rebuild must be a boolean")
    if not 0.0 < inner_tolerance_fraction < 1.0:
        raise ValueError("inner_tolerance_fraction must lie in (0, 1)")
    if max_epochs is not None and max_epochs < 1:
        raise ValueError("max_epochs must be positive")
    if max_frontier_iterations is not None and max_frontier_iterations < 0:
        raise ValueError("max_frontier_iterations must be nonnegative")
