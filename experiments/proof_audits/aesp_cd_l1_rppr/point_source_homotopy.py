#!/usr/bin/env python3
"""Exact audit of point-source homotopy mixing and breakpoint reordering."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations
from random import Random

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
) -> tuple[int, int]:
    """Audit every connected root-containing principal face exactly."""
    size = len(degree)
    checked = 0
    admission_replays = 0
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

        # A one-coordinate face extension reuses the same nonnegative response
        # column as the obstacle pivot.  Both exact and finite one-sided
        # ground residuals replay by a block identity.
        for new_vertex in range(size):
            if new_vertex in face or not any(
                adjacency[new_vertex][vertex] for vertex in face
            ):
                continue
            response_rhs = [-hessian[vertex][new_vertex] for vertex in face]
            pivot_response = solve(principal, response_rhs)
            schur = hessian[new_vertex][new_vertex] + sum(
                hessian[new_vertex][face[i]] * pivot_response[i]
                for i in range(len(face))
            )
            numerator = alpha * degree[new_vertex] - sum(
                hessian[new_vertex][face[i]] * response[i]
                for i in range(len(face))
            )
            exact_time = numerator / schur
            extended_face = [*face, new_vertex]
            extended_matrix = [
                [hessian[i][j] for j in extended_face] for i in extended_face
            ]
            extended_ground = solve(
                extended_matrix,
                [alpha * degree[i] for i in extended_face],
            )
            replayed_ground = [
                response[i] + exact_time * pivot_response[i]
                for i in range(len(face))
            ] + [exact_time]
            assert replayed_ground == extended_ground
            assert F(0) < exact_time <= 1

            eps_replay = F(1, 100)
            response_eps = F(1, 200)
            finite_ground = [(1 - eps_replay) * value for value in response]
            finite_response = [
                (1 - response_eps) * value for value in pivot_response
            ]
            finite_ground_residual = [
                alpha * degree[face[i]]
                - sum(
                    principal[i][j] * finite_ground[j]
                    for j in range(len(face))
                )
                for i in range(len(face))
            ]
            finite_response_residual = [
                response_rhs[i]
                - sum(
                    principal[i][j] * finite_response[j]
                    for j in range(len(face))
                )
                for i in range(len(face))
            ]
            finite_schur = hessian[new_vertex][new_vertex] + sum(
                hessian[new_vertex][face[i]] * finite_response[i]
                for i in range(len(face))
            )
            finite_numerator = alpha * degree[new_vertex] - sum(
                hessian[new_vertex][face[i]] * finite_ground[i]
                for i in range(len(face))
            )
            finite_time = finite_numerator / finite_schur
            finite_extended_ground = [
                finite_ground[i] + finite_time * finite_response[i]
                for i in range(len(face))
            ] + [finite_time]
            extended_residual = [
                alpha * degree[extended_face[i]]
                - sum(
                    extended_matrix[i][j] * finite_extended_ground[j]
                    for j in range(len(extended_face))
                )
                for i in range(len(extended_face))
            ]
            assert extended_residual == [
                finite_ground_residual[i]
                + finite_time * finite_response_residual[i]
                for i in range(len(face))
            ] + [F(0)]
            assert F(0) < finite_time <= exact_time
            assert all(value >= 0 for value in extended_residual)
            admission_replays += 1
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
    return checked, admission_replays


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
        inverse_high_bound**2
        * high_rhs_square
        * sum(value * value for value in exterior_row)
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

    # On an unweighted graph the row-specific dual radius collapses to the
    # single ground coupling s_v.  Here h=1 and an exterior vertex sees two
    # of the three K3 vertices.
    graph_row = [coupling, F(0), coupling]
    ground = [F(1)] * size
    ground_coupling = sum(
        graph_row[i] * ground[i] for i in range(size)
    )
    dual_radius_squared = sum(
        graph_row[i] ** 2 * ground[i] / degree for i in range(size)
    )
    assert dual_radius_squared <= coupling * ground_coupling
    # Young majorants turn a scalar square-root band into an affine score.
    # Use the lower endpoint of a factor-two bin so the check stays rational.
    band = F(7, 13)
    tangent = band / 2
    for scalar in (F(1), F(3, 2), F(2)):
        majorant = tangent * scalar + band * band / (4 * tangent)
        assert majorant * majorant >= band * band * scalar

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


def check_lazy_rank_one_reporter() -> int:
    """Audit the cumulative 2x2 normalization behind the lazy reporter."""

    def multiply(left: list[list[F]], right: list[list[F]]) -> list[list[F]]:
        return [
            [
                sum(left[i][k] * right[k][j] for k in range(2))
                for j in range(2)
            ]
            for i in range(2)
        ]

    def apply(matrix: list[list[F]], point: list[F]) -> list[F]:
        return [sum(matrix[i][j] * point[j] for j in range(2)) for i in range(2)]

    def inverse(matrix: list[list[F]]) -> list[list[F]]:
        determinant_value = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        return [
            [matrix[1][1] / determinant_value, -matrix[0][1] / determinant_value],
            [-matrix[1][0] / determinant_value, matrix[0][0] / determinant_value],
        ]

    normalized = [
        [F(1, 3), F(-1, 5)],
        [F(2, 7), F(-1, 11)],
        [F(3, 8), F(-2, 9)],
    ]
    current = [point[:] for point in normalized]
    cumulative = [[F(1), F(0)], [F(0), F(1)]]
    stages = ((F(5, 4), F(2, 3)), (F(7, 6), F(1, 5)), (F(9, 8), F(4, 7)))
    checks = 0
    for stage, (scale, shear) in enumerate(stages):
        transform = [[scale, F(0)], [shear, F(1)]]
        cumulative = multiply(transform, cumulative)
        current = [apply(transform, point) for point in current]
        direction = [cumulative[1][0], cumulative[1][1]]
        lazy_keys = [
            point[0] * direction[0] + point[1] * direction[1]
            for point in normalized
        ]
        assert lazy_keys == [point[1] for point in current]
        assert max(range(len(current)), key=lambda i: lazy_keys[i]) == max(
            range(len(current)),
            key=lambda i: current[i][1],
        )
        checks += len(current)

        if stage == 0:
            inserted_current = [F(5, 12), F(-1, 17)]
            inserted_normalized = apply(inverse(cumulative), inserted_current)
            normalized.append(inserted_normalized)
            current.append(inserted_current)
    return checks


def check_complete_prefix_rank_one() -> int:
    """Audit exact rank-one pivot responses on every proper K7 prefix."""
    size = 7
    degree = size - 1
    alpha = F(1, 17)
    p, coupling = (1 + alpha) / 2, (1 - alpha) / 2
    checks = 0
    for face_size in range(1, size):
        principal = [
            [
                p * degree if i == j else -coupling
                for j in range(face_size)
            ]
            for i in range(face_size)
        ]
        eigenvalue = p * degree - coupling * (face_size - 1)
        ground = solve(principal, [alpha * degree] * face_size)
        response = solve(principal, [coupling] * face_size)
        assert ground == [alpha * degree / eigenvalue] * face_size
        assert response == [coupling / eigenvalue] * face_size
        assert response == [
            coupling / (alpha * degree) * value for value in ground
        ]
        checks += 1
    return checks


def check_complete_rank_one_fixed_target() -> int:
    """Replay a full K7 RPPR trace using only the rank-one scalar formulas."""
    size = 7
    degree = size - 1
    alpha = F(1, 17)
    rho = F(1, 1000)
    p, coupling = (1 + alpha) / 2, (1 - alpha) / 2
    hessian = [
        [
            p * degree if i == j else -coupling
            for j in range(size)
        ]
        for i in range(size)
    ]
    load = [
        alpha * F(i == 0) - alpha * rho * degree
        for i in range(size)
    ]
    face = [0]
    admissions = 0
    total_ground_coupling = F(0)
    while len(face) < size:
        principal = [[hessian[i][j] for j in face] for i in face]
        ground = solve(principal, [alpha * degree] * len(face))
        active = solve(principal, [load[i] for i in face])
        volume = degree * sum(ground)
        new_vertex = min(set(range(size)) - set(face))
        coupling_rhs = [-hessian[i][new_vertex] for i in face]
        response = solve(principal, coupling_rhs)
        ground_coupling = sum(
            -hessian[new_vertex][face[i]] * ground[i]
            for i in range(len(face))
        )
        total_ground_coupling += ground_coupling
        gamma = ground_coupling / (alpha * volume)
        assert response == [gamma * value for value in ground]
        pivot = hessian[new_vertex][new_vertex] - gamma * ground_coupling
        key = load[new_vertex] - sum(
            hessian[new_vertex][face[i]] * active[i]
            for i in range(len(face))
        )
        assert key > 0 and pivot > 0
        active_time = key / pivot
        ground_time = (alpha * degree + ground_coupling) / pivot
        extended = [*face, new_vertex]
        extended_matrix = [[hessian[i][j] for j in extended] for i in extended]
        direct_active = solve(extended_matrix, [load[i] for i in extended])
        direct_ground = solve(extended_matrix, [alpha * degree] * len(extended))
        assert direct_active == [
            active[i] + active_time * response[i] for i in range(len(face))
        ] + [active_time]
        assert direct_ground == [
            ground[i] + ground_time * response[i] for i in range(len(face))
        ] + [ground_time]
        assert degree * sum(direct_ground) == (
            (1 + ground_time * gamma) * volume + degree * ground_time
        )
        face = extended
        admissions += 1
    assert solve(hessian, load) == direct_active
    assert total_ground_coupling <= coupling * size * (size - 1) / 2
    return admissions


def check_random_point_source_mass_clock() -> tuple[int, int, F]:
    """Audit the rational premises of the point-source pivot-mass clock."""
    rng = Random(20260829)
    traces = 0
    admissions = 0
    largest_cauchy_ratio = F(0)
    for size in range(3, 8):
        for _ in range(25):
            edges = {(vertex, vertex + 1) for vertex in range(size - 1)}
            edges.update(
                (left, right)
                for left in range(size)
                for right in range(left + 2, size)
                if rng.randrange(4) == 0
            )
            adjacency = [[F(0)] * size for _ in range(size)]
            degree = [0] * size
            for left, right in edges:
                adjacency[left][right] = adjacency[right][left] = 1
                degree[left] += 1
                degree[right] += 1
            alpha = rng.choice((F(1, 9), F(1, 5), F(2, 7), F(1, 3)))
            rho = rng.choice((F(1, 40), F(1, 24), F(1, 16)))
            diagonal, coupling = (1 + alpha) / 2, (1 - alpha) / 2
            hessian = [
                [
                    diagonal * degree[i]
                    if i == j
                    else -coupling * adjacency[i][j]
                    for j in range(size)
                ]
                for i in range(size)
            ]
            load = [alpha * (F(i == 0) - rho * degree[i]) for i in range(size)]
            if load[0] <= 0:
                continue

            face = [0]
            sum_degree_mass = F(0)
            sum_coordinate_mass = F(0)
            sum_pivot_weighted_mass = F(0)
            sum_pivot_coupling = F(0)
            while True:
                principal = [[hessian[i][j] for j in face] for i in face]
                active = solve(principal, [load[i] for i in face])
                assert all(value > 0 for value in active)
                exterior_keys = {
                    vertex: load[vertex]
                    - sum(
                        hessian[vertex][face[i]] * active[i]
                        for i in range(len(face))
                    )
                    for vertex in range(size)
                    if vertex not in face
                }
                positive = [vertex for vertex, key in exterior_keys.items() if key > 0]
                if not positive:
                    terminal = [F(0)] * size
                    for i, vertex in enumerate(face):
                        terminal[vertex] = active[i]
                    break

                winner = max(positive, key=lambda vertex: (exterior_keys[vertex], -vertex))
                ground = solve(principal, [alpha * degree[i] for i in face])
                pivot_coupling = coupling * sum(
                    adjacency[winner][face[i]] * ground[i]
                    for i in range(len(face))
                )
                assert F(0) < pivot_coupling <= coupling * degree[winner]
                extended = [*face, winner]
                enlarged = solve(
                    [[hessian[i][j] for j in extended] for i in extended],
                    [load[i] for i in extended],
                )
                coordinate = enlarged[-1]
                assert coordinate > 0
                assert all(enlarged[i] >= active[i] for i in range(len(face)))
                sum_degree_mass += degree[winner] * coordinate
                sum_coordinate_mass += coordinate
                sum_pivot_weighted_mass += coordinate * pivot_coupling
                sum_pivot_coupling += pivot_coupling
                face = extended
                admissions += 1

            unregularized = solve(hessian, [alpha * F(i == 0) for i in range(size)])
            assert sum(degree[i] * unregularized[i] for i in range(size)) == 1
            assert all(F(0) <= terminal[i] <= unregularized[i] for i in range(size))
            assert sum_degree_mass <= sum(
                degree[i] * terminal[i] for i in range(size)
            ) <= 1
            assert sum_coordinate_mass <= sum(terminal) <= 1
            assert sum_pivot_weighted_mass <= coupling * sum_degree_mass <= coupling
            induced_edges = sum(
                adjacency[i][j]
                for i in face
                for j in face
                if i < j
            )
            assert sum_pivot_coupling <= coupling * induced_edges
            cauchy_ratio = sum_degree_mass * sum_coordinate_mass
            assert cauchy_ratio <= 1
            largest_cauchy_ratio = max(largest_cauchy_ratio, cauchy_ratio)
            traces += 1
    return traces, admissions, largest_cauchy_ratio


def check_high_degree_refresh_algebra() -> tuple[F, F, F, F]:
    """Exact square-degree calibration of the high-degree rate corollary."""
    alpha, q, epsilon = F(1, 9), F(1, 3), F(1, 10)
    coupling = (1 - alpha) / 2
    degrees = (81, 144)
    charges = (F(9), F(16))
    square_roots = (9, 12)
    total = sum(charges, F(0))
    half_weighted = sum(
        (charge / root for charge, root in zip(charges, square_roots, strict=True)),
        F(0),
    )
    assert all(degree >= 1 / alpha**2 for degree in degrees)
    assert half_weighted <= alpha * total
    eta = alpha * epsilon
    refresh_term = (
        coupling**2 * q / (alpha * (1 + q) * eta) * half_weighted
    )
    target_term = total / (q * epsilon)
    assert refresh_term <= target_term

    # The symmetric sufficient condition puts the same square-degree lower
    # bound on admitted pivots instead of refreshed rows.  Its exact Cauchy
    # premise is sum xi <= alpha^2 sum d*xi.
    pivot_coordinates = (F(1, 162), F(1, 288))
    pivot_degree_mass = sum(
        degree * coordinate
        for degree, coordinate in zip(degrees, pivot_coordinates, strict=True)
    )
    pivot_coordinate_mass = sum(pivot_coordinates, F(0))
    assert pivot_degree_mass <= 1
    assert pivot_coordinate_mass <= alpha**2 * pivot_degree_mass
    clock_square_upper = coupling * pivot_degree_mass * pivot_coordinate_mass
    assert clock_square_upper <= alpha**2 * coupling

    # Exact low-low K2 calibration: point-source mass alone gives only a
    # Theta(sqrt(alpha)) clock, not the O(alpha) target condition.
    diagonal = (1 + alpha) / 2
    rho = coupling / 2
    root_ground = alpha / diagonal
    pivot_coupling = coupling * root_ground
    root_active = alpha * (1 - rho) / diagonal
    key = -alpha * rho + coupling * root_active
    schur = diagonal - coupling**2 / diagonal
    coordinate = key / schur
    assert schur == alpha / diagonal
    assert coordinate == coupling - rho == coupling / 2
    low_clock_square = coordinate**2 * pivot_coupling
    assert low_clock_square == coupling**3 * alpha / (4 * diagonal)
    return (
        half_weighted / total,
        refresh_term / target_term,
        clock_square_upper / coupling,
        low_clock_square / alpha,
    )


def check_high_gap_sparse_pivot_gray_stop() -> tuple[F, list[F], F, F]:
    """Certify that high gap alone does not make sparse pivots rank one."""
    face_size = 8
    q = F(1, 4)
    alpha = q * q / (1 + q * q)
    p, coupling = (1 + alpha) / 2, (1 - alpha) / 2
    degree = [face_size, face_size, *([face_size - 1] * (face_size - 2))]
    hessian = [
        [
            p * degree[i] if i == j else -coupling
            for j in range(face_size)
        ]
        for i in range(face_size)
    ]
    ground = solve(hessian, [alpha * value for value in degree])
    weight = [F(degree[i]) / ground[i] for i in range(face_size)]
    threshold = alpha * (1 + q) / q
    shifted = [
        [
            hessian[i][j] - threshold * weight[i] * F(i == j)
            for j in range(face_size)
        ]
        for i in range(face_size)
    ]

    # Exact no-pivot LDL inertia: one negative direction (the ground) and
    # seven positive directions certify that every high eigenvalue exceeds
    # alpha*(1+q)/q.
    lower = [[F(0)] * face_size for _ in range(face_size)]
    diagonal: list[F] = []
    for i in range(face_size):
        pivot = shifted[i][i] - sum(
            lower[i][k] ** 2 * diagonal[k] for k in range(i)
        )
        assert pivot
        diagonal.append(pivot)
        lower[i][i] = 1
        for j in range(i + 1, face_size):
            lower[j][i] = (
                shifted[j][i]
                - sum(
                    lower[j][k] * lower[i][k] * diagonal[k]
                    for k in range(i)
                )
            ) / pivot
    assert sum(value < 0 for value in diagonal) == 1
    assert sum(value > 0 for value in diagonal) == face_size - 1

    rhs = [coupling, *([F(0)] * (face_size - 1))]
    response = solve(hessian, rhs)
    transformed_rhs = [rhs[i] / degree[i] for i in range(face_size)]
    ground_weight = [degree[i] * ground[i] for i in range(face_size)]
    mean = sum(
        ground_weight[i] * transformed_rhs[i] for i in range(face_size)
    ) / sum(ground_weight)
    retained_leaf_error = response[1] - mean / alpha * ground[1]
    assert retained_leaf_error < 0

    # Balance two clique coordinates with two exterior leaves each.  A pivot
    # leaf at coordinate zero then gives opposite high-mode corrections to
    # two retained leaf rows whose old (ground-coupling,key) states coincide.
    balanced_degree = [face_size + 1, face_size + 1, *([face_size - 1] * 6)]
    balanced_hessian = [
        [
            p * balanced_degree[i] if i == j else -coupling
            for j in range(face_size)
        ]
        for i in range(face_size)
    ]
    balanced_ground = solve(
        balanced_hessian, [alpha * value for value in balanced_degree]
    )
    assert balanced_ground[0] == balanced_ground[1] == F(543, 911)
    balanced_weight = [
        F(balanced_degree[i]) / balanced_ground[i] for i in range(face_size)
    ]
    balanced_shifted = [
        [
            balanced_hessian[i][j]
            - threshold * balanced_weight[i] * F(i == j)
            for j in range(face_size)
        ]
        for i in range(face_size)
    ]
    balanced_lower = [[F(0)] * face_size for _ in range(face_size)]
    balanced_diagonal: list[F] = []
    for i in range(face_size):
        pivot = balanced_shifted[i][i] - sum(
            balanced_lower[i][k] ** 2 * balanced_diagonal[k]
            for k in range(i)
        )
        assert pivot
        balanced_diagonal.append(pivot)
        balanced_lower[i][i] = 1
        for j in range(i + 1, face_size):
            balanced_lower[j][i] = (
                balanced_shifted[j][i]
                - sum(
                    balanced_lower[j][k]
                    * balanced_lower[i][k]
                    * balanced_diagonal[k]
                    for k in range(i)
                )
            ) / pivot
    assert sum(value < 0 for value in balanced_diagonal) == 1
    assert sum(value > 0 for value in balanced_diagonal) == face_size - 1

    balanced_rhs = [coupling, *([F(0)] * (face_size - 1))]
    balanced_response = solve(balanced_hessian, balanced_rhs)
    balanced_transformed_rhs = [
        balanced_rhs[i] / balanced_degree[i] for i in range(face_size)
    ]
    balanced_ground_weight = [
        balanced_degree[i] * balanced_ground[i] for i in range(face_size)
    ]
    balanced_mean = sum(
        balanced_ground_weight[i] * balanced_transformed_rhs[i]
        for i in range(face_size)
    ) / sum(balanced_ground_weight)
    same_vertex_error = (
        balanced_response[0] - balanced_mean / alpha * balanced_ground[0]
    )
    other_vertex_error = (
        balanced_response[1] - balanced_mean / alpha * balanced_ground[1]
    )
    assert same_vertex_error == F(21150, 276523) > 0
    assert other_vertex_error == F(-3706, 276523) < 0
    assert (
        coupling * balanced_ground[0]
        == coupling * balanced_ground[1]
        == F(4344, 15487)
    )
    exterior_ground_couplings = [
        coupling * balanced_ground[0],
        coupling * balanced_ground[0],
        coupling * balanced_ground[1],
        coupling * balanced_ground[1],
    ]
    assert sum(exterior_ground_couplings) <= coupling * sum(balanced_degree)
    # Degenerate old boxes replay both opposite gray updates through the
    # same four-scalar monotone interval.
    scalar = coupling * balanced_ground[0]
    key = F(1, 10)
    ground_time, active_time = F(1, 3), F(2, 5)
    gamma = balanced_mean / alpha
    scale, shear = 1 + ground_time * gamma, active_time * gamma
    delta_pair = [
        coupling * same_vertex_error,
        coupling * other_vertex_error,
    ]
    product_coefficient = q * coupling / (alpha * (1 + q))
    pivot_coupling = scalar
    assert all(
        delta * delta
        <= product_coefficient**2 * scalar * pivot_coupling
        for delta in delta_pair
    )
    finite_ground = [F(4, 5) * value for value in balanced_ground]
    finite_weight = [
        balanced_degree[i] * finite_ground[i] for i in range(face_size)
    ]
    finite_mean = sum(
        finite_weight[i] * balanced_transformed_rhs[i]
        for i in range(face_size)
    ) / sum(finite_weight)
    finite_sigma_square = sum(
        finite_weight[i] * (balanced_transformed_rhs[i] - finite_mean) ** 2
        for i in range(face_size)
    )
    finite_pivot_coupling = coupling * finite_ground[0]
    finite_row_coupling = coupling * finite_ground[1]
    finite_volume = sum(finite_weight)
    finite_first_moment = sum(
        finite_weight[i] * abs(balanced_transformed_rhs[i] - finite_mean)
        for i in range(face_size)
    ) / finite_volume
    assert finite_mean == finite_pivot_coupling / finite_volume
    assert finite_first_moment <= 2 * finite_mean
    assert finite_sigma_square <= coupling * finite_pivot_coupling
    finite_dual_square = coupling * coupling * finite_ground[1] / balanced_degree[1]
    assert finite_dual_square <= coupling * finite_row_coupling
    gray_radius = max(abs(value) for value in delta_pair)
    lower_scalar = max(scalar, scale * scalar - ground_time * gray_radius)
    upper_scalar = scale * scalar + ground_time * gray_radius
    lower_key = max(key, key + shear * scalar - active_time * gray_radius)
    upper_key = key + shear * scalar + active_time * gray_radius
    for delta in delta_pair:
        exact_scalar = scale * scalar + ground_time * delta
        exact_key = key + shear * scalar + active_time * delta
        assert lower_scalar <= exact_scalar <= upper_scalar
        assert lower_key <= exact_key <= upper_key
    return (
        retained_leaf_error,
        diagonal,
        same_vertex_error,
        other_vertex_error,
    )


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
    assert r"\label{prop:aesp-cd-proper-face-ground-admission-replay}" in source
    assert r"\label{cor:aesp-cd-proper-face-conductance-alignment-tail}" in source
    assert r"\label{prop:aesp-cd-proper-clique-conductance-witness}" in source
    assert r"\label{prop:aesp-cd-point-source-literal-walk-sampling-stop}" in source
    assert r"\label{cor:aesp-cd-proper-face-rank-one-inverse}" in source
    assert r"\label{cor:aesp-cd-proper-face-unweighted-row-band}" in source
    assert r"\label{cor:aesp-cd-proper-face-gray-coupling-packing}" in source
    assert r"\label{cor:aesp-cd-proper-face-pivot-coupling-budget}" in source
    assert r"\label{cor:aesp-cd-point-source-cumulative-gray-key}" in source
    assert r"\label{cor:aesp-cd-point-source-clocked-gray-refresh}" in source
    assert r"\label{cor:aesp-cd-point-source-high-degree-gray-refresh}" in source
    assert r"\label{prop:aesp-cd-point-source-low-degree-clock-stop}" in source
    assert r"\label{cor:aesp-cd-proper-face-dyadic-gray-reporter}" in source
    assert r"\label{prop:aesp-cd-proper-face-four-scalar-gray-replay}" in source
    assert r"\label{cor:aesp-cd-proper-face-finite-rank-one-inverse}" in source
    assert r"\label{prop:aesp-cd-proper-face-lazy-rank-one-reporter}" in source
    assert r"\label{cor:aesp-cd-complete-prefix-rank-one-reporter}" in source
    assert r"\label{cor:aesp-cd-exact-rank-one-trace-discovery}" in source
    assert r"\label{prop:aesp-cd-exact-rank-one-admission-characterization}" in source
    assert r"\label{prop:aesp-cd-high-gap-sparse-pivot-gray-stop}" in source
    assert r"\label{prop:aesp-cd-high-gap-two-state-gray-stop}" in source

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

    ground_faces, admission_replays = check_ground_state_normalization(
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
    lazy_reporter_checks = check_lazy_rank_one_reporter()
    complete_prefix_checks = check_complete_prefix_rank_one()
    complete_trace_admissions = check_complete_rank_one_fixed_target()
    mass_clock_traces, mass_clock_admissions, largest_clock_cauchy_ratio = (
        check_random_point_source_mass_clock()
    )
    (
        half_degree_ratio,
        high_degree_target_ratio,
        high_pivot_clock_square_ratio,
        low_degree_clock_square_ratio,
    ) = check_high_degree_refresh_algebra()
    (
        sparse_pivot_error,
        sparse_pivot_inertia,
        same_state_positive_error,
        same_state_negative_error,
    ) = check_high_gap_sparse_pivot_gray_stop()

    print("PASS point-source homotopy breakpoint audit")
    print("  first tied batch: {1,4} at 5/96; next winner: 3 at 185/4231")
    print("  exact nonnegative rank-one mixing for surviving rows {2,5}")
    print("  strict priority reversal: 5>2 before, 2>5 after")
    print(f"  canonical proper-face ground normalization: {ground_faces} connected faces")
    print(f"  exact/finite ground admission replays: {admission_replays}")
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
    print(f"  lazy rank-one planar reporter checks: {lazy_reporter_checks}")
    print(f"  exact complete-prefix rank-one faces: {complete_prefix_checks}")
    print(f"  output-linear complete-graph trace admissions: {complete_trace_admissions}")
    print(
        "  exact random point-source mass clocks: "
        f"traces={mass_clock_traces}, admissions={mass_clock_admissions}, "
        f"largest rational Cauchy ratio={largest_clock_cauchy_ratio}"
    )
    print(
        "  high-degree refresh calibration: "
        f"F_1/2/F={half_degree_ratio}, refresh/target={high_degree_target_ratio}, "
        f"pivot clock^2/c={high_pivot_clock_square_ratio}, "
        f"low-low K2 clock^2/alpha={low_degree_clock_square_ratio}"
    )
    print(f"  high-gap sparse-pivot gray STOP: retained error={sparse_pivot_error}")
    print(
        "  identical scalar row-state STOP: "
        f"errors=({same_state_positive_error},{same_state_negative_error})"
    )
    print(f"    exact shifted LDL pivots: {sparse_pivot_inertia}")
    print(
        "  proper-clique conductance witness: "
        f"alpha={witness_alpha}, h_nondist={witness_response}, "
        f"Phi_lower={witness_conductance}"
    )


if __name__ == "__main__":
    main()
