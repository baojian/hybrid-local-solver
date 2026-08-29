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
        diagonal = (1 + alpha) / 2
        assert all(
            response[position]
            == alpha / diagonal
            + coupling
            / (diagonal * degree[vertex])
            * sum(
                adjacency[vertex][neighbor] * response[face.index(neighbor)]
                for neighbor in face
            )
            for position, vertex in enumerate(face)
        )

        # A truncated killed-walk Neumann series is a positive, fully local
        # finite ground certificate with an exact one-sided residual.
        theta = (1 - alpha) / (1 + alpha)
        walk_steps = 4
        walk_power = [F(1) for _ in face]
        walk_ground = [F(0) for _ in face]
        theta_power = F(1)
        killed_walk = [
            [
                F(adjacency[vertex][neighbor]) / degree[vertex]
                for neighbor in face
            ]
            for vertex in face
        ]
        for _ in range(walk_steps):
            walk_ground = [
                walk_ground[i] + (1 - theta) * theta_power * walk_power[i]
                for i in range(len(face))
            ]
            walk_power = [
                sum(killed_walk[i][j] * walk_power[j] for j in range(len(face)))
                for i in range(len(face))
            ]
            theta_power *= theta
        walk_residual = [
            alpha * degree[face[i]]
            - sum(principal[i][j] * walk_ground[j] for j in range(len(face)))
            for i in range(len(face))
        ]
        expected_walk_residual = [
            alpha * degree[face[i]] * theta_power * walk_power[i]
            for i in range(len(face))
        ]
        assert walk_residual == expected_walk_residual, (
            face,
            walk_residual,
            expected_walk_residual,
        )
        assert all(value > 0 for value in walk_ground)
        assert all(
            F(0) <= walk_residual[i]
            <= theta_power * alpha * degree[face[i]]
            for i in range(len(face))
        )
        assert all(
            walk_ground[i] <= response[i]
            <= walk_ground[i] / (1 - theta_power)
            for i in range(len(face))
        )
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
            epsilon_ground = F(1, 20)
            ground_residual = [
                epsilon_ground
                * alpha
                * degree[vertex]
                * F(position + 1, len(face) + 1)
                for position, vertex in enumerate(face)
            ]
            ground_error = solve(principal, ground_residual)
            approximate_ground = [
                response[i] - ground_error[i] for i in range(len(face))
            ]
            assert all(value > 0 for value in approximate_ground)
            recovered_residual = [
                alpha * degree[face[i]]
                - sum(
                    principal[i][j] * approximate_ground[j]
                    for j in range(len(face))
                )
                for i in range(len(face))
            ]
            assert recovered_residual == ground_residual
            assert all(
                F(0) <= recovered_residual[i]
                <= epsilon_ground * alpha * degree[face[i]]
                for i in range(len(face))
            )
            assert all(
                approximate_ground[i]
                <= response[i]
                <= approximate_ground[i] / (1 - epsilon_ground)
                for i in range(len(face))
            )
            phi_approximate: F | None = None
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
                approximate_denominator = min(
                    sum(
                        degree[face[i]] * approximate_ground[i]
                        for i in left
                    ),
                    sum(
                        degree[face[i]] * approximate_ground[i]
                        for i in right
                    ),
                )
                approximate_ratio = (
                    coupling
                    * sum(
                        adjacency[face[i]][face[j]]
                        * approximate_ground[i]
                        * approximate_ground[j]
                        for i in left
                        for j in right
                    )
                    / approximate_denominator
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
                phi_approximate = (
                    approximate_ratio
                    if phi_approximate is None
                    else min(phi_approximate, approximate_ratio)
                )
            assert (
                phi_ground is not None
                and phi_ambient is not None
                and phi_approximate is not None
            )
            assert phi_ground >= coupling * survival_lower**2 * phi_ambient
            assert phi_ground >= (1 - epsilon_ground) * phi_approximate

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


def check_endpoint_kernel(
    adjacency: list[list[F]], degree: list[int], alpha: F
) -> int:
    """Audit the reversible endpoint kernel and residual variance proxy."""
    size = len(degree)
    termination = 2 * alpha / (1 + alpha)
    continuation = 1 - termination
    walk_system = [
        [
            F(i == j) - continuation * adjacency[i][j] / degree[j]
            for j in range(size)
        ]
        for i in range(size)
    ]
    columns = [
        solve(walk_system, [F(i == source) for i in range(size)])
        for source in range(size)
    ]
    kernel = [
        [termination * columns[source][vertex] for source in range(size)]
        for vertex in range(size)
    ]
    assert all(sum(kernel[vertex][source] for vertex in range(size)) == 1 for source in range(size))
    assert all(entry >= 0 for row in kernel for entry in row)
    assert all(
        kernel[v][u] / degree[v] == kernel[u][v] / degree[u]
        for u in range(size)
        for v in range(size)
    )

    threshold = F(1, 20)
    residual = [
        threshold * degree[i] * F(i + 1, size + 1) for i in range(size)
    ]
    assert sum(residual) <= 1
    assert all(residual[i] / degree[i] <= threshold for i in range(size))
    correction = [
        sum(kernel[v][u] * residual[u] for u in range(size))
        for v in range(size)
    ]
    assert all(correction[v] / degree[v] <= threshold for v in range(size))
    return size


def check_rank_one_inverse_certificate() -> tuple[F, F, F, F]:
    """Audit the conductance-certified inverse split on an exact K3 face."""
    q = F(1, 16)
    alpha = q * q / (1 + q * q)
    p, coupling = (1 + alpha) / 2, (1 - alpha) / 2
    size, degree = 3, 2
    conductance = coupling
    assert conductance * conductance >= 2 * alpha / q
    high_eigenvalue = p + coupling / 2
    assert high_eigenvalue >= alpha * (1 + q) / q
    hessian = [
        [p * degree if i == j else -coupling for j in range(size)]
        for i in range(size)
    ]
    qbar = [[entry / degree for entry in row] for row in hessian]
    rhs = [F(7, 11), F(-2, 13), F(5, 17)]
    transformed_rhs = [value / degree for value in rhs]
    solution = solve(qbar, transformed_rhs)
    mean = sum(transformed_rhs) / size
    high_rhs = [value - mean for value in transformed_rhs]
    high_solution = [value - mean / alpha for value in solution]
    assert sum(high_rhs) == 0 and sum(high_solution) == 0
    inverse_high_bound = q / (alpha * (1 + q))
    high_rhs_square = sum(value * value for value in high_rhs)
    assert (
        sum(value * value for value in high_solution)
        <= inverse_high_bound**2 * high_rhs_square
    )
    # Avoid relying only on the square-root comparison above: its squared
    # rational form is the exact certificate used by the theorem.
    assert all(
        high_solution[i] ** 2
        <= inverse_high_bound**2 * high_rhs_square
        for i in range(size)
    )
    # A retained nonnegative exterior row inherits one simultaneous scalar
    # interval, exactly as in the reporter corollary.
    exterior_row = [F(2, 7), F(3, 10), F(5, 12)]
    propagated_high = sum(
        exterior_row[i] * high_solution[i] for i in range(size)
    )
    assert propagated_high**2 <= (
        inverse_high_bound**2 * high_rhs_square * sum(exterior_row) ** 2
    )
    # The theorem uses the sharper Euclidean radius; the rational L1 radius
    # below avoids introducing square roots while still certifying both signs.
    coordinate_row_band = inverse_high_bound * sum(exterior_row) * sum(
        abs(value) for value in high_rhs
    )
    assert abs(propagated_high) <= coordinate_row_band
    approximate_response = mean / alpha * sum(exterior_row)
    positive_key = -approximate_response + coordinate_row_band + F(1, 19)
    negative_key = -approximate_response - coordinate_row_band - F(1, 23)
    assert positive_key + approximate_response - coordinate_row_band > 0
    assert negative_key + approximate_response + coordinate_row_band < 0

    # The finite ground certificate must suffice without exact h.  A uniform
    # shrink realizes the extremal one-sided residual sandwich exactly.
    eps_h = F(1, 5)
    c_h = 1 / (1 - eps_h)
    approximate_ground = [1 - eps_h] * size
    approximate_weight = [degree * value for value in approximate_ground]
    approximate_volume = sum(approximate_weight)
    approximate_mean = (
        sum(
            approximate_weight[i] * transformed_rhs[i]
            for i in range(size)
        )
        / approximate_volume
    )
    assert approximate_mean == mean
    centered = [value - approximate_mean for value in transformed_rhs]
    first_moment = (
        sum(approximate_weight[i] * abs(centered[i]) for i in range(size))
        / approximate_volume
    )
    sigma_square = sum(
        approximate_weight[i] * centered[i] ** 2 for i in range(size)
    )
    ground_radius = [
        approximate_ground[i]
        / alpha
        * (c_h - 1)
        * (abs(approximate_mean) + c_h * first_moment)
        for i in range(size)
    ]
    high_radius_square = [
        (c_h * inverse_high_bound) ** 2
        * approximate_ground[i]
        / degree
        * sigma_square
        for i in range(size)
    ]
    finite_center = [
        approximate_mean / alpha * approximate_ground[i]
        for i in range(size)
    ]
    for i in range(size):
        excess = max(abs(solution[i] - finite_center[i]) - ground_radius[i], 0)
        assert excess**2 <= high_radius_square[i]
    return alpha, inverse_high_bound, coordinate_row_band, eps_h


def main() -> None:
    source = note_tex_source("aesp_cd_l1_rppr")
    assert r"\label{prop:aesp-cd-point-source-homotopy-reorder}" in source
    assert r"\label{eq:aesp-cd-point-source-homotopy-mix}" in source
    assert r"\label{lem:aesp-cd-point-source-ground-state-normalization}" in source
    assert r"\label{prop:aesp-cd-proper-face-ground-conjugacy}" in source
    assert r"\label{eq:aesp-cd-proper-face-doob-laplacian}" in source
    assert r"\label{cor:aesp-cd-proper-face-conductance-gap}" in source
    assert r"\label{cor:aesp-cd-proper-face-leakage-conductance}" in source
    assert r"\label{cor:aesp-cd-proper-face-finite-ground-certificate}" in source
    assert r"\label{prop:aesp-cd-proper-face-walk-ground-certificate}" in source
    assert r"\label{cor:aesp-cd-proper-face-conductance-alignment-tail}" in source
    assert r"\label{prop:aesp-cd-proper-clique-conductance-witness}" in source
    assert r"\label{prop:aesp-cd-point-source-literal-walk-sampling-stop}" in source
    assert r"\label{cor:aesp-cd-proper-face-rank-one-inverse}" in source
    assert r"\label{cor:aesp-cd-proper-face-finite-rank-one-inverse}" in source

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
    endpoint_vertices = check_endpoint_kernel(adjacency, degree, alpha)
    rank_one_alpha, rank_one_bound, row_band, ground_eps = (
        check_rank_one_inverse_certificate()
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
    print("  finite one-sided ground residual certificate: exact on every face")
    print("  killed-walk finite ground construction: exact on every face")
    print(f"  reversible residual endpoint variance proxy: exact on {endpoint_vertices} vertices")
    print(
        "  conductance-certified rank-one inverse: "
        f"alpha={rank_one_alpha}, high_inverse_bound={rank_one_bound}, "
        f"row_band={row_band}, finite_ground_eps={ground_eps}"
    )
    print(
        "  proper-clique conductance witness: "
        f"alpha={witness_alpha}, h_nondist={witness_response}, "
        f"Phi_lower={witness_conductance}"
    )


if __name__ == "__main__":
    main()
