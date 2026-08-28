#!/usr/bin/env python3
"""Exact rational RPPR decoy for blind factor-two envelope prefetch.

The audit works in hat coordinates, where both the RPPR Hessian and the
degree-weighted threshold right-hand side are rational.  This removes the
square roots from the high-degree decoy demand test.
"""

from __future__ import annotations

from fractions import Fraction as F

from experiments.proof_audits import note_tex_source


Matrix = list[list[F]]
Vector = list[F]


def solve(matrix: Matrix, rhs: Vector) -> Vector:
    """Solve a small rational system by exact Gauss-Jordan elimination."""
    size = len(rhs)
    work = [row[:] + [value] for row, value in zip(matrix, rhs, strict=True)]
    for column in range(size):
        pivot = next(row for row in range(column, size) if work[row][column])
        work[column], work[pivot] = work[pivot], work[column]
        diagonal = work[column][column]
        work[column] = [entry / diagonal for entry in work[column]]
        for row in range(size):
            if row == column:
                continue
            multiplier = work[row][column]
            if multiplier:
                work[row] = [
                    entry - multiplier * pivot_entry
                    for entry, pivot_entry in zip(work[row], work[column], strict=True)
                ]
    return [work[row][-1] for row in range(size)]


def strict_decoy() -> None:
    # G_M is the path s-a-u-h with M-1 leaves attached to h.
    alpha = F(1, 5)
    rho = F(1, 20)
    decoy_degree = 100
    size = decoy_degree + 3
    source, first, anchor, decoy = range(4)
    leaves = tuple(range(4, size))
    degree = [1, 2, 2, decoy_degree, *([1] * (decoy_degree - 1))]
    adjacency = [set() for _ in range(size)]

    def add_edge(left: int, right: int) -> None:
        adjacency[left].add(right)
        adjacency[right].add(left)

    add_edge(source, first)
    add_edge(first, anchor)
    add_edge(anchor, decoy)
    for leaf in leaves:
        add_edge(decoy, leaf)
    assert [len(neighbors) for neighbors in adjacency] == degree

    diagonal = (1 + alpha) / 2
    coupling = (1 - alpha) / 2
    hessian = [[F(0)] * size for _ in range(size)]
    for vertex in range(size):
        hessian[vertex][vertex] = diagonal * degree[vertex]
        for neighbor in adjacency[vertex]:
            hessian[vertex][neighbor] = -coupling
    rhs = [
        alpha * (F(vertex == source) - rho * degree[vertex])
        for vertex in range(size)
    ]
    assert diagonal == F(3, 5)
    assert coupling == F(2, 5)
    rho_bound = (1 - alpha) ** 2 / (alpha**2 + 10 * alpha + 5)
    assert rho_bound == F(1, 11)
    assert 0 < rho < rho_bound
    assert all(
        hessian[i][i]
        > sum(abs(hessian[i][j]) for j in range(size) if j != i)
        for i in range(size)
    )

    # The singleton face has a strict certified violation at a.
    source_value = rhs[source] / hessian[source][source]
    first_key = rhs[first] + coupling * source_value
    assert source_value == F(19, 60)
    assert first_key == F(8, 75) > 0

    # The prefix {s,a} has a strict certified violation at u.
    prefix = [source, first]
    prefix_matrix = [[hessian[i][j] for j in prefix] for i in prefix]
    prefix_solution = solve(prefix_matrix, [rhs[i] for i in prefix])
    anchor_key = rhs[anchor] + coupling * prefix_solution[-1]
    assert prefix_solution == [F(11, 28), F(4, 35)]
    assert anchor_key == F(9, 350) > 0

    # The full three-coordinate active face is strictly interior.
    support = [source, first, anchor]
    support_matrix = [[hessian[i][j] for j in support] for i in support]
    support_solution = solve(support_matrix, [rhs[i] for i in support])
    assert support_solution == [F(2, 5), F(1, 8), F(1, 40)]
    assert all(value > 0 for value in support_solution)

    # In hat coordinates the radical-free decoy condition is
    #   key_h = alpha*rho*(Gamma-M),
    #   Gamma = coupling*x_u/(alpha*rho).
    gamma_demand = coupling * support_solution[-1] / (alpha * rho)
    decoy_key = -alpha * rho * decoy_degree + coupling * support_solution[-1]
    assert gamma_demand == 1
    assert decoy_degree > gamma_demand
    assert decoy_key == alpha * rho * (gamma_demand - decoy_degree)
    assert decoy_key == F(-99, 100) < 0
    assert all(rhs[leaf] == F(-1, 100) < 0 for leaf in leaves)

    # The padded three-coordinate point is therefore the exact global KKT
    # solution, with all decoy coordinates strictly inactive.
    padded = [*support_solution, *([F(0)] * (size - len(support_solution)))]
    residual = [
        rhs[i] - sum(hessian[i][j] * padded[j] for j in range(size))
        for i in range(size)
    ]
    assert all(residual[i] == 0 for i in support)
    assert residual[decoy] == decoy_key < 0
    assert all(residual[leaf] == F(-1, 100) < 0 for leaf in leaves)
    support_volume = sum(degree[i] for i in support)
    assert support_volume == 5

    # After a is active, admitting the unique violation u grows volume only
    # from 3 to 5.  A blind factor-two search anchored at u must next swallow
    # its unique outward neighbor h, paying h's full ambient degree.
    old_volume = degree[source] + degree[first]
    admitted_volume = old_volume + degree[anchor]
    outward = adjacency[anchor] - set(support)
    explored_volume = admitted_volume + degree[decoy]
    assert old_volume == 3
    assert admitted_volume == 5 < 2 * old_volume
    assert outward == {decoy}
    assert explored_volume == 105
    assert F(explored_volume, support_volume) == 21 > 20


def check_source_scope() -> None:
    source = note_tex_source("aesp_cd_l1_rppr")
    assert "prop:aesp-cd-rppr-speculative-decoy" in source
    assert "eq:aesp-cd-rppr-speculative-decoy" in source
    assert "support-sensitive blind doubling" in source


def main() -> None:
    strict_decoy()
    check_source_scope()
    print("Strict RPPR speculative-decoy audit passed")
    print("  alpha=1/5, rho=1/20, M=100; radical-free demand Gamma=1")
    print("  exact support {s,a,u}: volume 5; h and 99 leaves strictly inactive")
    print("  blind factor-two anchor prefetch: explored volume 105, ratio 21")


if __name__ == "__main__":
    main()
