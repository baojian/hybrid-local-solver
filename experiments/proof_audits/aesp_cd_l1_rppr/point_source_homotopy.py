#!/usr/bin/env python3
"""Exact audit of point-source homotopy mixing and breakpoint reordering."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations

from experiments.proof_audits import note_tex_source


def solve(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    size = len(rhs)
    work = [row[:] + [value] for row, value in zip(matrix, rhs, strict=True)]
    for column in range(size):
        pivot = next(row for row in range(column, size) if work[row][column])
        work[column], work[pivot] = work[pivot], work[column]
        diagonal = work[column][column]
        work[column] = [entry / diagonal for entry in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                entry - multiplier * pivot_entry
                for entry, pivot_entry in zip(work[row], work[column], strict=True)
            ]
    return [row[-1] for row in work]


def breakpoint_data(
    hessian: list[list[F]], degree: list[int], face: set[int], alpha: F
) -> tuple[dict[int, tuple[F, F]], dict[int, F]]:
    indices = sorted(face)
    principal = [[hessian[i][j] for j in indices] for i in indices]
    source_response = solve(principal, [alpha * F(i == 0) for i in indices])
    degree_response = solve(principal, [alpha * degree[i] for i in indices])
    pairs: dict[int, tuple[F, F]] = {}
    thresholds: dict[int, F] = {}
    for vertex in range(len(degree)):
        if vertex in face:
            continue
        intercept = -sum(
            hessian[vertex][i] * source_response[position]
            for position, i in enumerate(indices)
        )
        slope = alpha * degree[vertex] - sum(
            hessian[vertex][i] * degree_response[position]
            for position, i in enumerate(indices)
        )
        assert slope > 0
        if intercept > 0:
            pairs[vertex] = (intercept, slope)
            thresholds[vertex] = intercept / slope
    return pairs, thresholds


def determinant(matrix: list[list[F]]) -> F:
    """Exact determinant with row pivoting."""
    size = len(matrix)
    if size == 0:
        return F(1)
    work = [row[:] for row in matrix]
    value = F(1)
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column]),
            None,
        )
        if pivot is None:
            return F(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            value = -value
        diagonal = work[column][column]
        value *= diagonal
        for row in range(column + 1, size):
            multiplier = work[row][column] / diagonal
            for index in range(column + 1, size):
                work[row][index] -= multiplier * work[column][index]
    return value


def assert_psd(matrix: list[list[F]]) -> None:
    """Use the all-principal-minors characterization of symmetric PSD."""
    size = len(matrix)
    assert all(matrix[i][j] == matrix[j][i] for i in range(size) for j in range(size))
    for order in range(1, size + 1):
        for indices in combinations(range(size), order):
            principal = [[matrix[i][j] for j in indices] for i in indices]
            assert determinant(principal) >= 0


def check_ground_state_normalization(
    hessian: list[list[F]],
    degree: list[int],
    adjacency: list[list[F]],
    alpha: F,
) -> int:
    """Audit every connected root-containing principal face exactly."""
    size = len(degree)
    checked = 0
    for mask in range(1, 1 << size):
        if not mask & 1:
            continue
        face = [vertex for vertex in range(size) if mask & (1 << vertex)]
        reached = {face[0]}
        queue = [face[0]]
        for vertex in queue:
            for neighbor in face:
                if adjacency[vertex][neighbor] and neighbor not in reached:
                    reached.add(neighbor)
                    queue.append(neighbor)
        if len(reached) != len(face):
            continue

        principal = [[hessian[i][j] for j in face] for i in face]
        response = solve(principal, [alpha * degree[i] for i in face])
        assert all(F(0) < value <= 1 for value in response)
        coupling = (1 - alpha) / 2
        internal_degree = [
            sum(adjacency[vertex][neighbor] for neighbor in face)
            for vertex in face
        ]
        leakage = max(
            F(degree[vertex] - internal_degree[position], degree[vertex])
            for position, vertex in enumerate(face)
        )
        survival_lower = alpha / (alpha + coupling * leakage)
        assert min(response) >= survival_lower
        mass = [F(degree[i], 1) / response[position] for position, i in enumerate(face)]
        assert all(
            sum(principal[row][column] * response[column] for column in range(len(face)))
            == alpha * mass[row] * response[row]
            for row in range(len(face))
        )

        lower = [
            [
                principal[i][j] - alpha * mass[i] * F(i == j)
                for j in range(len(face))
            ]
            for i in range(len(face))
        ]
        upper = [
            [
                mass[i] * F(i == j) - principal[i][j]
                for j in range(len(face))
            ]
            for i in range(len(face))
        ]
        assert_psd(lower)
        assert_psd(upper)

        shift = F(3, 5)
        shifted = [
            [
                principal[i][j] + shift * mass[i] * F(i == j)
                for j in range(len(face))
            ]
            for i in range(len(face))
        ]
        resolvent = solve(shifted, [shift * mass[i] * response[i] for i in range(len(face))])
        expected_factor = shift / (shift + alpha)
        assert resolvent == [expected_factor * value for value in response]

        # Exact diagonal conjugacy to a constant-ground normalized operator.
        qbar = [
            [
                principal[i][j] * response[j] / degree[face[i]]
                for j in range(len(face))
            ]
            for i in range(len(face))
        ]
        dbar = [F(degree[vertex], 1) * response[i] for i, vertex in enumerate(face)]
        assert all(sum(row) == alpha for row in qbar)
        assert all(qbar[i][j] <= 0 for i in range(len(face)) for j in range(len(face)) if i != j)
        assert all(
            dbar[i] * qbar[i][j] == dbar[j] * qbar[j][i]
            for i in range(len(face))
            for j in range(len(face))
        )
        edge_weight = [
            [
                coupling * adjacency[face[i]][face[j]] * response[i] * response[j]
                for j in range(len(face))
            ]
            for i in range(len(face))
        ]
        laplacian = [
            [
                (
                    sum(edge_weight[i])
                    if i == j
                    else -edge_weight[i][j]
                )
                for j in range(len(face))
            ]
            for i in range(len(face))
        ]
        conjugated_ground_shift = [
            [
                dbar[i] * (qbar[i][j] - alpha * F(i == j))
                for j in range(len(face))
            ]
            for i in range(len(face))
        ]
        assert conjugated_ground_shift == laplacian
        probe = [F(2 * i - 3, 7) for i in range(len(face))]
        dirichlet = sum(
            edge_weight[i][j] * (probe[i] - probe[j]) ** 2
            for i in range(len(face))
            for j in range(i + 1, len(face))
        )
        quadratic = sum(
            probe[i] * laplacian[i][j] * probe[j]
            for i in range(len(face))
            for j in range(len(face))
        )
        assert quadratic == dirichlet

        if len(face) > 1:
            phi_ground: F | None = None
            phi_ambient: F | None = None
            for cut_mask in range(1, (1 << len(face)) - 1):
                left = [i for i in range(len(face)) if cut_mask & (1 << i)]
                right = [i for i in range(len(face)) if not cut_mask & (1 << i)]
                cut_edges = sum(adjacency[face[i]][face[j]] for i in left for j in right)
                ambient_denominator = min(
                    sum(degree[face[i]] for i in left),
                    sum(degree[face[i]] for i in right),
                )
                ground_denominator = min(
                    sum(dbar[i] for i in left),
                    sum(dbar[i] for i in right),
                )
                ambient_ratio = cut_edges / ambient_denominator
                ground_ratio = (
                    coupling
                    * sum(
                        adjacency[face[i]][face[j]] * response[i] * response[j]
                        for i in left
                        for j in right
                    )
                    / ground_denominator
                )
                phi_ambient = (
                    ambient_ratio
                    if phi_ambient is None
                    else min(phi_ambient, ambient_ratio)
                )
                phi_ground = (
                    ground_ratio
                    if phi_ground is None
                    else min(phi_ground, ground_ratio)
                )
            assert phi_ground is not None and phi_ambient is not None
            assert phi_ground >= coupling * survival_lower**2 * phi_ambient

        # The ground-state Laplacian induces an exact reversible Markov
        # kernel.  This is the premise needed by the weighted-conductance
        # certificate: row sums are one, every entry is nonnegative, and
        # dbar is a reversible measure.
        kernel = [
            [F(i == j) - laplacian[i][j] / dbar[i] for j in range(len(face))]
            for i in range(len(face))
        ]
        assert all(sum(row) == 1 for row in kernel)
        assert all(entry >= 0 for row in kernel for entry in row)
        assert all(
            dbar[i] * kernel[i][j] == dbar[j] * kernel[j][i]
            for i in range(len(face))
            for j in range(len(face))
        )
        assert all(
            sum(edge_weight[i]) <= dbar[i]
            for i in range(len(face))
        )

        # A generic shifted solve agrees in the two coordinate systems.
        target = [F(11 + 2 * i, 10) for i in range(len(face))]
        load = [
            sum(principal[i][j] * target[j] for j in range(len(face)))
            for i in range(len(face))
        ]
        center = [F(i + 1, 13) for i in range(len(face))]
        shifted_rhs = [load[i] + shift * mass[i] * center[i] for i in range(len(face))]
        shifted_solution = solve(shifted, shifted_rhs)
        conjugate_shifted = [
            [qbar[i][j] + shift * F(i == j) for j in range(len(face))]
            for i in range(len(face))
        ]
        z_center = [center[i] / response[i] for i in range(len(face))]
        bar_load = [load[i] / degree[face[i]] for i in range(len(face))]
        z_solution = solve(
            conjugate_shifted,
            [bar_load[i] + shift * z_center[i] for i in range(len(face))],
        )
        assert shifted_solution == [response[i] * z_solution[i] for i in range(len(face))]

        # The h-cap is exactly a constant cap after conjugacy and publishes a
        # lower subsolution below the chosen positive exact solution.
        trial = [
            target[i] + F((i % 3) - 1, 5) + F(len(face), 17)
            for i in range(len(face))
        ]
        violation = [
            sum(principal[i][j] * trial[j] for j in range(len(face))) - load[i]
            for i in range(len(face))
        ]
        cap = max([F(0), *(violation[i] / (alpha * degree[face[i]]) for i in range(len(face)))])
        published = [max(F(0), trial[i] - cap * response[i]) for i in range(len(face))]
        z_trial = [trial[i] / response[i] for i in range(len(face))]
        assert published == [response[i] * max(F(0), z_trial[i] - cap) for i in range(len(face))]
        residual = [
            load[i] - sum(principal[i][j] * published[j] for j in range(len(face)))
            for i in range(len(face))
        ]
        assert all(residual[i] >= 0 for i in range(len(face)) if published[i] > 0)
        assert all(published[i] <= target[i] for i in range(len(face)))
        checked += 1
    return checked


def check_proper_clique_conductance_witness() -> tuple[F, F, F]:
    """Audit the closed two-orbit proper-clique witness exactly."""
    q = F(1, 256)
    alpha = q * q / (1 + q * q)
    # Here alpha=1/65537, so this is exactly ceil(1/alpha).
    clique_size = (alpha.denominator + alpha.numerator - 1) // alpha.numerator
    assert clique_size >= 1 / alpha
    response_nondistinguished_numerator = (
        2 * alpha * clique_size * ((1 + alpha) * clique_size - 2 * alpha)
    )
    response = response_nondistinguished_numerator / (
        response_nondistinguished_numerator + (1 - alpha) ** 2
    )
    assert response >= F(3, 4)
    conductance_lower = (
        (1 - alpha)
        / 2
        * F(clique_size - 1, clique_size)
        * response
        / 2
    )
    assert conductance_lower >= F(27, 256)
    threshold_squared = 2 * alpha / q
    assert conductance_lower * conductance_lower > threshold_squared
    return alpha, response, conductance_lower


def main() -> None:
    source = note_tex_source("aesp_cd_l1_rppr")
    assert r"\label{prop:aesp-cd-point-source-homotopy-reorder}" in source
    assert r"\label{eq:aesp-cd-point-source-homotopy-mix}" in source
    assert r"\label{lem:aesp-cd-point-source-ground-state-normalization}" in source
    assert r"\label{prop:aesp-cd-proper-face-ground-conjugacy}" in source
    assert r"\label{eq:aesp-cd-proper-face-doob-laplacian}" in source
    assert r"\label{cor:aesp-cd-proper-face-conductance-gap}" in source
    assert r"\label{cor:aesp-cd-proper-face-leakage-conductance}" in source
    assert r"\label{cor:aesp-cd-proper-face-conductance-alignment-tail}" in source
    assert r"\label{prop:aesp-cd-proper-clique-conductance-witness}" in source

    size, alpha = 6, F(2, 7)
    edges = ((0, 1), (0, 3), (0, 4), (1, 2), (1, 3), (2, 3), (2, 5), (3, 4), (4, 5))
    adjacency = [[F(0)] * size for _ in range(size)]
    degree = [0] * size
    for left, right in edges:
        adjacency[left][right] = adjacency[right][left] = 1
        degree[left] += 1
        degree[right] += 1
    diagonal, coupling = (1 + alpha) / 2, (1 - alpha) / 2
    hessian = [
        [
            diagonal * degree[i] if i == j else -coupling * adjacency[i][j]
            for j in range(size)
        ]
        for i in range(size)
    ]

    _, first = breakpoint_data(hessian, degree, {0}, alpha)
    assert first == {1: F(5, 96), 3: F(5, 123), 4: F(5, 96)}
    assert {vertex for vertex, value in first.items() if value == max(first.values())} == {1, 4}

    face = {0, 1, 4}
    old_pairs, old = breakpoint_data(hessian, degree, face, alpha)
    assert old == {2: F(25, 2517), 3: F(185, 4231), 5: F(25, 1838)}
    assert max(old, key=old.get) == 3
    winner = 3
    new_pairs, new = breakpoint_data(hessian, degree, face | {winner}, alpha)
    assert new == {2: F(975, 53696), 5: F(1025, 64318)}
    assert old[5] > old[2] and new[2] > new[5]

    # Independently recover each nonnegative mixture coefficient from A and
    # verify that the same value updates B.
    winner_intercept, winner_slope = old_pairs[winner]
    for vertex in (2, 5):
        old_intercept, old_slope = old_pairs[vertex]
        new_intercept, new_slope = new_pairs[vertex]
        gamma = (new_intercept - old_intercept) / winner_intercept
        assert gamma >= 0
        assert new_slope == old_slope + gamma * winner_slope
        assert old[vertex] <= new[vertex] <= old[winner]

    ground_faces = check_ground_state_normalization(
        hessian,
        degree,
        adjacency,
        alpha,
    )
    assert ground_faces == 25
    witness_alpha, witness_response, witness_conductance = (
        check_proper_clique_conductance_witness()
    )

    print("PASS point-source homotopy breakpoint audit")
    print("  first tied batch: {1,4} at 5/96; next winner: 3 at 185/4231")
    print("  exact nonnegative rank-one mixing for surviving rows {2,5}")
    print("  strict priority reversal: 5>2 before, 2>5 after")
    print(f"  canonical proper-face ground normalization: {ground_faces} connected faces")
    print("  h-cap / W-shift conjugacy: exact on every connected face")
    print("  conjugated ground shift: exact weighted graph Laplacian")
    print("  ground walk: stochastic, nonnegative, and exactly reversible")
    print("  leakage survival and ordinary-conductance comparison: exact on every face")
    print(
        "  proper-clique conductance witness: "
        f"alpha={witness_alpha}, h_nondist={witness_response}, "
        f"Phi_lower={witness_conductance}"
    )


if __name__ == "__main__":
    main()
