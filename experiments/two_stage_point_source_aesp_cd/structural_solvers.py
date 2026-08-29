"""Fixed-envelope structural linear solvers used by the two-stage experiments."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

import numpy as np


def tree_principal_solve(
    adjacency: list[list[int]],
    envelope: np.ndarray,
    degree: np.ndarray,
    alpha: float,
    source: np.ndarray,
    root: int,
) -> tuple[np.ndarray, int]:
    """Solve a connected induced-tree principal PPR system by leaf LDL."""
    indices = np.flatnonzero(envelope)
    if not envelope[root]:
        raise ValueError("the root must lie in the structural envelope")
    position = {int(vertex): offset for offset, vertex in enumerate(indices)}
    parent = np.full(len(indices), -2, dtype=np.int64)
    root_position = position[root]
    parent[root_position] = -1
    order: list[int] = []
    queue = deque([root_position])
    induced_edges = 0
    while queue:
        local = queue.popleft()
        order.append(local)
        vertex = int(indices[local])
        for neighbor in adjacency[vertex]:
            if not envelope[neighbor]:
                continue
            following = position[neighbor]
            induced_edges += 1
            if parent[following] != -2:
                continue
            parent[following] = local
            queue.append(following)
    induced_edges //= 2
    if len(order) != len(indices) or induced_edges != len(indices) - 1:
        raise ValueError("the retained principal graph is not a tree")

    diagonal = np.full(len(indices), (1.0 + alpha) / 2.0)
    reduced_rhs = source[indices].copy()
    coupling_scale = (1.0 - alpha) / 2.0
    edge_coupling = np.zeros(len(indices))
    arithmetic_work = 0
    for local in reversed(order[1:]):
        ancestor = int(parent[local])
        vertex = int(indices[local])
        parent_vertex = int(indices[ancestor])
        coupling = -coupling_scale / np.sqrt(degree[vertex] * degree[parent_vertex])
        edge_coupling[local] = coupling
        reduced_rhs[ancestor] -= coupling * reduced_rhs[local] / diagonal[local]
        diagonal[ancestor] -= coupling * coupling / diagonal[local]
        if diagonal[ancestor] <= 0.0:
            raise AssertionError("SPD tree elimination produced a nonpositive pivot")
        arithmetic_work += 1

    values = np.zeros(len(indices))
    values[root_position] = reduced_rhs[root_position] / diagonal[root_position]
    for local in order[1:]:
        ancestor = int(parent[local])
        values[local] = (reduced_rhs[local] - edge_coupling[local] * values[ancestor]) / diagonal[
            local
        ]
        arithmetic_work += 1
    output = np.zeros(len(adjacency))
    output[indices] = values
    return output, arithmetic_work


def principal_residual(
    adjacency: list[list[int]],
    envelope: np.ndarray,
    degree: np.ndarray,
    alpha: float,
    source: np.ndarray,
    vector: np.ndarray,
) -> np.ndarray:
    """Materialize the retained principal residual without a sparse library."""
    diagonal = (1.0 + alpha) / 2.0
    coupling = (1.0 - alpha) / 2.0
    residual = np.zeros(len(adjacency))
    for vertex in np.flatnonzero(envelope):
        value = source[vertex] - diagonal * vector[vertex]
        for neighbor in adjacency[int(vertex)]:
            if envelope[neighbor]:
                value += coupling * vector[neighbor] / np.sqrt(degree[vertex] * degree[neighbor])
        residual[vertex] = value
    return residual


def _tridiagonal_solve(
    lower: np.ndarray,
    diagonal: np.ndarray,
    upper: np.ndarray,
    rhs: np.ndarray,
) -> tuple[np.ndarray, int]:
    """Solve an SPD tridiagonal system by a nonpivoted Thomas sweep."""
    size = len(diagonal)
    reduced_diagonal = diagonal.copy()
    reduced_rhs = rhs.copy()
    work = 0
    for index in range(1, size):
        multiplier = lower[index - 1] / reduced_diagonal[index - 1]
        reduced_diagonal[index] -= multiplier * upper[index - 1]
        reduced_rhs[index] -= multiplier * reduced_rhs[index - 1]
        if reduced_diagonal[index] <= 0.0:
            raise AssertionError("SPD tridiagonal elimination lost a positive pivot")
        work += 1
    solution = np.empty(size)
    solution[-1] = reduced_rhs[-1] / reduced_diagonal[-1]
    for index in range(size - 2, -1, -1):
        solution[index] = (
            reduced_rhs[index] - upper[index] * solution[index + 1]
        ) / reduced_diagonal[index]
        work += 1
    return solution, work


def _cyclic_tridiagonal_solve(
    lower: np.ndarray,
    diagonal: np.ndarray,
    upper: np.ndarray,
    corner_first_last: float,
    corner_last_first: float,
    rhs: np.ndarray,
) -> tuple[np.ndarray, int]:
    """Solve a cyclic tridiagonal system by two Thomas sweeps."""
    if len(diagonal) < 3:
        raise ValueError("a simple cycle must have at least three vertices")
    gamma = -diagonal[0]
    modified_diagonal = diagonal.copy()
    modified_diagonal[0] -= gamma
    modified_diagonal[-1] -= corner_first_last * corner_last_first / gamma
    first, work_first = _tridiagonal_solve(lower, modified_diagonal, upper, rhs)
    correction_rhs = np.zeros(len(diagonal))
    correction_rhs[0] = gamma
    correction_rhs[-1] = corner_first_last
    correction, work_second = _tridiagonal_solve(lower, modified_diagonal, upper, correction_rhs)
    factor = (first[0] + corner_last_first * first[-1] / gamma) / (
        1.0 + correction[0] + corner_last_first * correction[-1] / gamma
    )
    return first - factor * correction, work_first + work_second + len(diagonal)


def unicyclic_principal_solve(
    adjacency: list[list[int]],
    envelope: np.ndarray,
    degree: np.ndarray,
    alpha: float,
    source: np.ndarray,
    root: int,
) -> tuple[np.ndarray, int]:
    """Solve a connected induced-unicyclic principal system in linear work.

    Hanging trees are eliminated toward the unique cycle.  The remaining
    cyclic tridiagonal core is solved by two path sweeps, after which the
    hanging-tree values are recovered in reverse elimination order.
    """
    indices = np.flatnonzero(envelope)
    if not envelope[root]:
        raise ValueError("the root must lie in the structural envelope")
    position = {int(vertex): offset for offset, vertex in enumerate(indices)}
    local_neighbors: list[list[int]] = []
    edge_twice = 0
    for vertex in indices:
        neighbors = [
            position[neighbor] for neighbor in adjacency[int(vertex)] if envelope[neighbor]
        ]
        local_neighbors.append(neighbors)
        edge_twice += len(neighbors)
    if edge_twice // 2 != len(indices):
        raise ValueError("the retained principal graph is not unicyclic")

    # A reachability check is useful because edge_count=vertex_count alone
    # permits a disconnected union of components.
    seen = {position[root]}
    queue = deque([position[root]])
    while queue:
        local = queue.popleft()
        for following in local_neighbors[local]:
            if following not in seen:
                seen.add(following)
                queue.append(following)
    if len(seen) != len(indices):
        raise ValueError("the retained principal graph is disconnected")

    diagonal = np.full(len(indices), (1.0 + alpha) / 2.0)
    reduced_rhs = source[indices].copy()
    coupling_scale = (1.0 - alpha) / 2.0

    def coupling(left: int, right: int) -> float:
        return -coupling_scale / np.sqrt(degree[int(indices[left])] * degree[int(indices[right])])

    remaining = np.ones(len(indices), dtype=bool)
    remaining_degree = np.array([len(row) for row in local_neighbors])
    leaves = deque(np.flatnonzero(remaining_degree == 1).tolist())
    eliminated: list[tuple[int, int, float]] = []
    work = 0
    while leaves:
        leaf = leaves.popleft()
        if not remaining[leaf] or remaining_degree[leaf] != 1:
            continue
        parent = next(neighbor for neighbor in local_neighbors[leaf] if remaining[neighbor])
        edge = coupling(leaf, parent)
        reduced_rhs[parent] -= edge * reduced_rhs[leaf] / diagonal[leaf]
        diagonal[parent] -= edge * edge / diagonal[leaf]
        if diagonal[parent] <= 0.0:
            raise AssertionError("unicyclic leaf elimination lost a positive pivot")
        eliminated.append((leaf, parent, edge))
        remaining[leaf] = False
        remaining_degree[leaf] = 0
        remaining_degree[parent] -= 1
        if remaining_degree[parent] == 1:
            leaves.append(parent)
        work += 1

    core = np.flatnonzero(remaining)
    if len(core) < 3 or np.any(remaining_degree[core] != 2):
        raise AssertionError("leaf peeling did not expose one simple cycle")
    core_set = set(core.tolist())
    first = int(core[0])
    cycle_order = [first]
    previous = -1
    current = first
    while True:
        candidates = [
            neighbor
            for neighbor in local_neighbors[current]
            if neighbor in core_set and neighbor != previous
        ]
        if not candidates:
            raise AssertionError("cycle traversal stopped before closing")
        following = candidates[0]
        if following == first:
            break
        cycle_order.append(following)
        previous, current = current, following
        if len(cycle_order) > len(core):
            raise AssertionError("cycle traversal failed to close")
    if len(cycle_order) != len(core):
        raise AssertionError("cycle traversal omitted a core vertex")

    cycle_diagonal = diagonal[cycle_order]
    cycle_rhs = reduced_rhs[cycle_order]
    upper = np.array([coupling(cycle_order[i], cycle_order[i + 1]) for i in range(len(core) - 1)])
    lower = upper.copy()
    corner = coupling(cycle_order[0], cycle_order[-1])
    cycle_values, cycle_work = _cyclic_tridiagonal_solve(
        lower,
        cycle_diagonal,
        upper,
        corner,
        corner,
        cycle_rhs,
    )
    work += cycle_work
    local_values = np.zeros(len(indices))
    local_values[cycle_order] = cycle_values
    for leaf, parent, edge in reversed(eliminated):
        local_values[leaf] = (reduced_rhs[leaf] - edge * local_values[parent]) / diagonal[leaf]
        work += 1
    output = np.zeros(len(adjacency))
    output[indices] = local_values
    return output, work


def tree_or_unicyclic_principal_solve(
    adjacency: list[list[int]],
    envelope: np.ndarray,
    degree: np.ndarray,
    alpha: float,
    source: np.ndarray,
    root: int,
) -> tuple[np.ndarray, int, str]:
    """Dispatch to the exact-linear-work structural solver."""
    vertices = int(np.count_nonzero(envelope))
    edges = (
        sum(
            1
            for vertex in np.flatnonzero(envelope)
            for neighbor in adjacency[int(vertex)]
            if envelope[neighbor]
        )
        // 2
    )
    if edges == vertices - 1:
        output, work = tree_principal_solve(adjacency, envelope, degree, alpha, source, root)
        return output, work, "tree-leaf-ldl"
    if edges == vertices:
        output, work = unicyclic_principal_solve(adjacency, envelope, degree, alpha, source, root)
        return output, work, "unicyclic-peel-cycle"
    raise ValueError("the retained principal graph is neither a tree nor unicyclic")


def reused_structural_backsolve_work(adjacency: list[list[int]], envelope: np.ndarray) -> int:
    """Charge one new right-hand side after structural factors are retained.

    The count deliberately excludes graph discovery, factor construction, and
    the first RPPR solve: all three were already paid by the exact-face
    verifier.  On a tree, a new right-hand side needs one upward and one
    downward sweep.  On a unicyclic graph, peeled tree rows need the same two
    sweeps and the cached cyclic Sherman--Morrison factors need one Thomas
    solve plus one vector correction.  This is an arithmetic-work model, not
    a claim that a fresh implementation silently reuses factors.
    """
    indices = np.flatnonzero(envelope)
    vertices = len(indices)
    if vertices == 0:
        return 0
    position = {int(vertex): offset for offset, vertex in enumerate(indices)}
    local_neighbors = [
        [position[neighbor] for neighbor in adjacency[int(vertex)] if envelope[neighbor]]
        for vertex in indices
    ]
    seen = {0}
    queue = deque([0])
    while queue:
        local = queue.popleft()
        for following in local_neighbors[local]:
            if following not in seen:
                seen.add(following)
                queue.append(following)
    if len(seen) != vertices:
        raise ValueError("the retained principal graph is disconnected")
    edges = sum(len(row) for row in local_neighbors) // 2
    if edges == vertices - 1:
        return 2 * vertices - 1
    if edges != vertices:
        raise ValueError("the retained principal graph is neither a tree nor unicyclic")

    remaining = np.ones(vertices, dtype=bool)
    remaining_degree = np.asarray([len(row) for row in local_neighbors])
    leaves = deque(np.flatnonzero(remaining_degree == 1).tolist())
    peeled = 0
    while leaves:
        leaf = leaves.popleft()
        if not remaining[leaf] or remaining_degree[leaf] != 1:
            continue
        parent = next(neighbor for neighbor in local_neighbors[leaf] if remaining[neighbor])
        remaining[leaf] = False
        remaining_degree[leaf] = 0
        remaining_degree[parent] -= 1
        peeled += 1
        if remaining_degree[parent] == 1:
            leaves.append(parent)
    cycle = vertices - peeled
    if cycle < 3 or np.any(remaining_degree[remaining] != 2):
        raise ValueError("leaf peeling did not expose one simple cycle")
    return 2 * peeled + 3 * cycle + 1


@dataclass(frozen=True)
class TreePrincipalFactors:
    """Reusable leaf-elimination factors for one connected principal tree."""

    indices: np.ndarray
    parent: np.ndarray
    order: tuple[int, ...]
    diagonal: np.ndarray
    edge_coupling: np.ndarray
    global_size: int

    def solve(self, source: np.ndarray) -> tuple[np.ndarray, int]:
        """Apply the retained factors to one new right-hand side."""
        reduced_rhs = source[self.indices].copy()
        for local in reversed(self.order[1:]):
            ancestor = int(self.parent[local])
            reduced_rhs[ancestor] -= (
                self.edge_coupling[local] * reduced_rhs[local] / self.diagonal[local]
            )
        values = np.zeros(len(self.indices))
        root_position = self.order[0]
        values[root_position] = reduced_rhs[root_position] / self.diagonal[root_position]
        for local in self.order[1:]:
            ancestor = int(self.parent[local])
            values[local] = (
                reduced_rhs[local] - self.edge_coupling[local] * values[ancestor]
            ) / self.diagonal[local]
        output = np.zeros(self.global_size)
        output[self.indices] = values
        return output, 2 * len(self.indices) - 1


@dataclass(frozen=True)
class _TridiagonalFactors:
    """Nonpivoted reusable factors of one SPD tridiagonal matrix."""

    multipliers: np.ndarray
    diagonal: np.ndarray
    upper: np.ndarray

    def solve(self, rhs: np.ndarray) -> np.ndarray:
        reduced_rhs = rhs.copy()
        for index in range(1, len(self.diagonal)):
            reduced_rhs[index] -= self.multipliers[index - 1] * reduced_rhs[index - 1]
        solution = np.empty(len(self.diagonal))
        solution[-1] = reduced_rhs[-1] / self.diagonal[-1]
        for index in range(len(self.diagonal) - 2, -1, -1):
            solution[index] = (
                reduced_rhs[index] - self.upper[index] * solution[index + 1]
            ) / self.diagonal[index]
        return solution


@dataclass(frozen=True)
class _CyclicFactors:
    """Reusable Sherman--Morrison factors for a cyclic tridiagonal core."""

    path: _TridiagonalFactors
    correction: np.ndarray
    gamma: float
    corner_last_first: float

    def solve(self, rhs: np.ndarray) -> tuple[np.ndarray, int]:
        first = self.path.solve(rhs)
        factor = (first[0] + self.corner_last_first * first[-1] / self.gamma) / (
            1.0 + self.correction[0] + self.corner_last_first * self.correction[-1] / self.gamma
        )
        values = first - factor * self.correction
        return values, 3 * len(rhs) + 1


@dataclass(frozen=True)
class UnicyclicPrincipalFactors:
    """Reusable leaf and cyclic-core factors for one principal unicyclic graph."""

    indices: np.ndarray
    diagonal: np.ndarray
    eliminated: tuple[tuple[int, int, float], ...]
    cycle_order: np.ndarray
    cycle: _CyclicFactors
    global_size: int

    def solve(self, source: np.ndarray) -> tuple[np.ndarray, int]:
        """Apply the retained factors to one new right-hand side."""
        reduced_rhs = source[self.indices].copy()
        for leaf, parent, edge in self.eliminated:
            reduced_rhs[parent] -= edge * reduced_rhs[leaf] / self.diagonal[leaf]
        cycle_values, cycle_work = self.cycle.solve(reduced_rhs[self.cycle_order])
        local_values = np.zeros(len(self.indices))
        local_values[self.cycle_order] = cycle_values
        for leaf, parent, edge in reversed(self.eliminated):
            local_values[leaf] = (reduced_rhs[leaf] - edge * local_values[parent]) / self.diagonal[
                leaf
            ]
        output = np.zeros(self.global_size)
        output[self.indices] = local_values
        return output, 2 * len(self.eliminated) + cycle_work


def _factor_tridiagonal(
    lower: np.ndarray,
    diagonal: np.ndarray,
    upper: np.ndarray,
) -> _TridiagonalFactors:
    reduced_diagonal = diagonal.copy()
    multipliers = np.empty(max(0, len(diagonal) - 1))
    for index in range(1, len(diagonal)):
        multipliers[index - 1] = lower[index - 1] / reduced_diagonal[index - 1]
        reduced_diagonal[index] -= multipliers[index - 1] * upper[index - 1]
        if reduced_diagonal[index] <= 0.0:
            raise AssertionError("SPD tridiagonal factorization lost a positive pivot")
    return _TridiagonalFactors(multipliers, reduced_diagonal, upper.copy())


def _factor_cyclic(
    lower: np.ndarray,
    diagonal: np.ndarray,
    upper: np.ndarray,
    corner_first_last: float,
    corner_last_first: float,
) -> _CyclicFactors:
    gamma = -diagonal[0]
    modified_diagonal = diagonal.copy()
    modified_diagonal[0] -= gamma
    modified_diagonal[-1] -= corner_first_last * corner_last_first / gamma
    path = _factor_tridiagonal(lower, modified_diagonal, upper)
    correction_rhs = np.zeros(len(diagonal))
    correction_rhs[0] = gamma
    correction_rhs[-1] = corner_first_last
    correction = path.solve(correction_rhs)
    return _CyclicFactors(path, correction, gamma, corner_last_first)


def factor_tree_principal(
    adjacency: list[list[int]],
    envelope: np.ndarray,
    degree: np.ndarray,
    alpha: float,
    root: int,
) -> TreePrincipalFactors:
    """Factor one connected principal tree without committing to a right-hand side."""
    indices = np.flatnonzero(envelope)
    if not envelope[root]:
        raise ValueError("the root must lie in the structural envelope")
    position = {int(vertex): offset for offset, vertex in enumerate(indices)}
    parent = np.full(len(indices), -2, dtype=np.int64)
    root_position = position[root]
    parent[root_position] = -1
    order: list[int] = []
    queue = deque([root_position])
    induced_edges = 0
    while queue:
        local = queue.popleft()
        order.append(local)
        vertex = int(indices[local])
        for neighbor in adjacency[vertex]:
            if not envelope[neighbor]:
                continue
            following = position[neighbor]
            induced_edges += 1
            if parent[following] != -2:
                continue
            parent[following] = local
            queue.append(following)
    induced_edges //= 2
    if len(order) != len(indices) or induced_edges != len(indices) - 1:
        raise ValueError("the retained principal graph is not a tree")

    diagonal = np.full(len(indices), (1.0 + alpha) / 2.0)
    edge_coupling = np.zeros(len(indices))
    coupling_scale = (1.0 - alpha) / 2.0
    for local in reversed(order[1:]):
        ancestor = int(parent[local])
        vertex = int(indices[local])
        parent_vertex = int(indices[ancestor])
        coupling = -coupling_scale / np.sqrt(degree[vertex] * degree[parent_vertex])
        edge_coupling[local] = coupling
        diagonal[ancestor] -= coupling * coupling / diagonal[local]
        if diagonal[ancestor] <= 0.0:
            raise AssertionError("SPD tree factorization produced a nonpositive pivot")
    return TreePrincipalFactors(
        indices,
        parent,
        tuple(order),
        diagonal,
        edge_coupling,
        len(adjacency),
    )


def factor_unicyclic_principal(
    adjacency: list[list[int]],
    envelope: np.ndarray,
    degree: np.ndarray,
    alpha: float,
    root: int,
) -> UnicyclicPrincipalFactors:
    """Factor one connected principal unicyclic graph for repeated right-hand sides."""
    indices = np.flatnonzero(envelope)
    if not envelope[root]:
        raise ValueError("the root must lie in the structural envelope")
    position = {int(vertex): offset for offset, vertex in enumerate(indices)}
    local_neighbors = [
        [position[neighbor] for neighbor in adjacency[int(vertex)] if envelope[neighbor]]
        for vertex in indices
    ]
    if sum(len(row) for row in local_neighbors) // 2 != len(indices):
        raise ValueError("the retained principal graph is not unicyclic")
    seen = {position[root]}
    queue = deque([position[root]])
    while queue:
        local = queue.popleft()
        for following in local_neighbors[local]:
            if following not in seen:
                seen.add(following)
                queue.append(following)
    if len(seen) != len(indices):
        raise ValueError("the retained principal graph is disconnected")

    diagonal = np.full(len(indices), (1.0 + alpha) / 2.0)
    coupling_scale = (1.0 - alpha) / 2.0

    def coupling(left: int, right: int) -> float:
        return -coupling_scale / np.sqrt(degree[int(indices[left])] * degree[int(indices[right])])

    remaining = np.ones(len(indices), dtype=bool)
    remaining_degree = np.asarray([len(row) for row in local_neighbors])
    leaves = deque(np.flatnonzero(remaining_degree == 1).tolist())
    eliminated: list[tuple[int, int, float]] = []
    while leaves:
        leaf = leaves.popleft()
        if not remaining[leaf] or remaining_degree[leaf] != 1:
            continue
        parent = next(neighbor for neighbor in local_neighbors[leaf] if remaining[neighbor])
        edge = coupling(leaf, parent)
        diagonal[parent] -= edge * edge / diagonal[leaf]
        if diagonal[parent] <= 0.0:
            raise AssertionError("unicyclic factorization lost a positive pivot")
        eliminated.append((leaf, parent, edge))
        remaining[leaf] = False
        remaining_degree[leaf] = 0
        remaining_degree[parent] -= 1
        if remaining_degree[parent] == 1:
            leaves.append(parent)

    core = np.flatnonzero(remaining)
    if len(core) < 3 or np.any(remaining_degree[core] != 2):
        raise AssertionError("leaf peeling did not expose one simple cycle")
    core_set = set(core.tolist())
    first = int(core[0])
    cycle_order = [first]
    previous = -1
    current = first
    while True:
        candidates = [
            neighbor
            for neighbor in local_neighbors[current]
            if neighbor in core_set and neighbor != previous
        ]
        if not candidates:
            raise AssertionError("cycle traversal stopped before closing")
        following = candidates[0]
        if following == first:
            break
        cycle_order.append(following)
        previous, current = current, following
        if len(cycle_order) > len(core):
            raise AssertionError("cycle traversal failed to close")
    if len(cycle_order) != len(core):
        raise AssertionError("cycle traversal omitted a core vertex")
    cycle_order_array = np.asarray(cycle_order, dtype=np.int64)
    upper = np.asarray([coupling(cycle_order[i], cycle_order[i + 1]) for i in range(len(core) - 1)])
    corner = coupling(cycle_order[0], cycle_order[-1])
    cycle = _factor_cyclic(
        upper.copy(),
        diagonal[cycle_order_array],
        upper,
        corner,
        corner,
    )
    return UnicyclicPrincipalFactors(
        indices,
        diagonal,
        tuple(eliminated),
        cycle_order_array,
        cycle,
        len(adjacency),
    )


def factor_tree_or_unicyclic_principal(
    adjacency: list[list[int]],
    envelope: np.ndarray,
    degree: np.ndarray,
    alpha: float,
    root: int,
) -> TreePrincipalFactors | UnicyclicPrincipalFactors:
    """Build reusable structural factors for repeated principal solves."""
    vertices = int(np.count_nonzero(envelope))
    edges = (
        sum(
            1
            for vertex in np.flatnonzero(envelope)
            for neighbor in adjacency[int(vertex)]
            if envelope[neighbor]
        )
        // 2
    )
    if edges == vertices - 1:
        return factor_tree_principal(adjacency, envelope, degree, alpha, root)
    if edges == vertices:
        return factor_unicyclic_principal(adjacency, envelope, degree, alpha, root)
    raise ValueError("the retained principal graph is neither a tree nor unicyclic")
