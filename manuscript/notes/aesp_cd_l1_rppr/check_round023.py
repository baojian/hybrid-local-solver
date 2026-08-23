#!/usr/bin/env python3
"""Exact Round-023 audit for the fixed-operator P4 tail.

The checker uses rational arithmetic for the prefix replay, phase word,
invariant cone, harmful-defect box, and finite-inner scalar obstruction.
It makes no floating-point sign decision and claims no finite-inner rate.
"""

from __future__ import annotations

from fractions import Fraction as F
from pathlib import Path

import check_round022 as r22


Matrix = list[list[F]]
Vector = list[F]


def identity(size: int) -> Matrix:
    return [[F(i == j) for j in range(size)] for i in range(size)]


def matrix_add(left: Matrix, right: Matrix) -> Matrix:
    return [[left[i][j] + right[i][j] for j in range(len(left[0]))] for i in range(len(left))]


def matrix_scale(scale: F, matrix: Matrix) -> Matrix:
    return [[scale * value for value in row] for row in matrix]


def matrix_multiply(left: Matrix, right: Matrix) -> Matrix:
    return [
        [
            sum((left[i][k] * right[k][j] for k in range(len(right))), F(0))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def transpose(matrix: Matrix) -> Matrix:
    return [list(column) for column in zip(*matrix)]


def inverse(matrix: Matrix) -> Matrix:
    columns = [
        r22.solve_linear(matrix, [F(i == j) for i in range(len(matrix))])
        for j in range(len(matrix))
    ]
    return transpose(columns)


def diagonal(values: list[F]) -> Matrix:
    return [[values[i] if i == j else F(0) for j in range(len(values))] for i in range(len(values))]


def affine_recurrence(current: Matrix, previous: Matrix, beta: F) -> Matrix:
    return matrix_add(matrix_scale(1 + beta, current), matrix_scale(-beta, previous))


def exact_prefix(stages: int = 55) -> tuple[dict[int, Vector], dict[int, str], Vector]:
    """Replay the full P4 recurrence and classify stages exactly."""
    degree, alpha, kappa, matrix, load, shifted = r22.path_matrices(4, 0, F(1, 8), F(7, 40))
    beta = F(7, 9)
    optimum = r22.solve_stieltjes_obstacle(matrix, load)
    previous = [F(0)] * 4
    point = [F(0)] * 4
    points: dict[int, Vector] = {}
    phases: dict[int, str] = {}

    for stage in range(stages + 1):
        points[stage] = point[:]
        displacement = [point[i] - previous[i] for i in range(4)]
        extrapolate = [point[i] + beta * displacement[i] for i in range(4)]
        residual = [load[i] - value for i, value in enumerate(r22.matvec(matrix, extrapolate))]
        support = [i for i, value in enumerate(extrapolate) if value > 0]
        row_values = {i: -residual[i] / (alpha * degree[i]) for i in support}
        delta = max([F(0), *row_values.values()])
        lower = [max(F(0), extrapolate[i] - delta) for i in range(4)]
        center = [max(point[i], lower[i]) for i in range(4)]
        correction = [extrapolate[i] - center[i] for i in range(4)]

        active = (0, 1, 2)
        caps = [beta * displacement[i] for i in range(4)]
        if stage < 44:
            phase = "C" if any(correction) else "N"
        elif all(correction[i] == 0 for i in active):
            phase = "N"
        elif all(correction[i] == caps[i] > 0 for i in active):
            phase = "F"
        else:
            maximizers = [i for i, value in row_values.items() if value == delta]
            assert len(maximizers) == 1
            assert all(F(0) < correction[i] < caps[i] for i in active)
            phase = f"P{maximizers[0]}"
        phases[stage] = phase

        assert all(point[i] <= center[i] <= optimum[i] for i in range(4))
        if stage == stages:
            break
        next_point = r22.shifted_minimizer(center, degree, kappa, shifted, load)
        assert all(center[i] <= next_point[i] <= optimum[i] for i in range(4))
        previous, point = point, next_point

    return points, phases, optimum


def phase_margins(
    previous: Matrix,
    current: Matrix,
    phase: str,
    rays: list[Vector],
    active_q: Matrix,
    alpha: F,
    beta: F,
    degree: list[F],
) -> list[F]:
    """Return all strict linear decision margins on the cone rays."""
    trial = affine_recurrence(current, previous, beta)
    margins: list[F] = []
    expected_row = None
    if phase.startswith("F") or phase.startswith("P"):
        expected_row = int(phase[1:])

    for ray in rays:
        old_error = r22.matvec(previous, ray)
        error = r22.matvec(current, ray)
        trial_error = r22.matvec(trial, ray)
        displacement = [old_error[i] - error[i] for i in range(3)]
        residual = r22.matvec(active_q, trial_error)
        delta_rows = [-residual[i] / (alpha * degree[i]) for i in range(3)]
        margins.extend(displacement)

        if phase == "N":
            margins.extend(residual)
            continue

        assert expected_row is not None
        delta = delta_rows[expected_row]
        margins.append(delta)
        margins.extend(delta - delta_rows[i] for i in range(3) if i != expected_row)
        if phase.startswith("F"):
            margins.extend(delta - beta * displacement[i] for i in range(3))
        else:
            margins.extend(beta * displacement[i] - delta for i in range(3))

    assert all(value > 0 for value in margins)
    return margins


def polynomial_coefficients(matrix: Matrix) -> list[F]:
    """Coefficients of [1,r,s,r^2,rs,s^2] for x^T M x, x=(1,r,s)."""
    return [
        matrix[0][0],
        matrix[0][1] + matrix[1][0],
        matrix[0][2] + matrix[2][0],
        matrix[1][1],
        matrix[1][2] + matrix[2][1],
        matrix[2][2],
    ]


def interval_quadratic(matrix: Matrix) -> tuple[F, F]:
    """Exact monomial interval bound on the invariant ratio rectangle."""
    r_low, r_high = F(997, 1000), F(998, 1000)
    s_low, s_high = F(856, 1000), F(857, 1000)
    monomial_bounds = [
        (F(1), F(1)),
        (r_low, r_high),
        (s_low, s_high),
        (r_low * r_low, r_high * r_high),
        (r_low * s_low, r_high * s_high),
        (s_low * s_low, s_high * s_high),
    ]
    lower = F(0)
    upper = F(0)
    for coefficient, (lo, hi) in zip(polynomial_coefficients(matrix), monomial_bounds):
        if coefficient >= 0:
            lower += coefficient * lo
            upper += coefficient * hi
        else:
            lower += coefficient * hi
            upper += coefficient * lo
    return lower, upper


def check_infinite_p4_tail() -> dict[str, F]:
    """Verify the prefix, invariant cone, exact word, and defect floor."""
    degree_full, alpha, kappa, q_full, _, shifted_full = r22.path_matrices(4, 0, F(1, 8), F(7, 40))
    beta = F(7, 9)
    degree = [F(value) for value in degree_full[:3]]
    active_q = [row[:3] for row in q_full[:3]]
    active_h = [row[:3] for row in shifted_full[:3]]
    d_matrix = diagonal(degree)
    h_inverse = inverse(active_h)
    m_matrix = matrix_multiply(h_inverse, matrix_scale(kappa, d_matrix))
    expected_m = [
        [F(245, 352), F(21, 88), F(7, 176)],
        [F(21, 176), F(63, 88), F(21, 176)],
        [F(7, 352), F(21, 176), F(119, 176)],
    ]
    assert m_matrix == expected_m
    r_zero = [
        [F(-32), F(32), F(0)],
        [F(-33), F(33), F(0)],
        [F(-33), F(32), F(1)],
    ]

    points, phases, optimum = exact_prefix()
    expected = ["F", "N", "N", "F", *("N" for _ in range(6)), "P0", "F"]
    assert [phases[stage] for stage in range(44, 56)] == expected
    error_44 = [optimum[i] - points[44][i] for i in range(3)]
    assert all(value > 0 for value in error_44)
    assert F(997, 1000) <= error_44[1] / error_44[0] <= F(998, 1000)
    assert F(856, 1000) <= error_44[2] / error_44[0] <= F(857, 1000)

    rays = [
        [F(1), r, s] for r in (F(997, 1000), F(998, 1000)) for s in (F(856, 1000), F(857, 1000))
    ]
    i_matrix = identity(3)
    previous = i_matrix
    current = m_matrix
    all_margins: list[F] = []
    decision_word = ["N", "N", "F2", *("N" for _ in range(6)), "P0"]
    phase_starts: list[tuple[Matrix, Matrix, str]] = []
    for phase in decision_word:
        phase_starts.append((previous, current, phase))
        all_margins.extend(
            phase_margins(previous, current, phase, rays, active_q, alpha, beta, degree)
        )
        trial = affine_recurrence(current, previous, beta)
        if phase == "N":
            following = matrix_multiply(m_matrix, trial)
        elif phase.startswith("F"):
            following = matrix_multiply(m_matrix, current)
        else:
            following = matrix_multiply(m_matrix, matrix_multiply(r_zero, trial))
        previous, current = current, following
    word_map = current
    all_margins.extend(phase_margins(previous, current, "F0", rays, active_q, alpha, beta, degree))
    assert min(all_margins) >= F(1, 200)

    a_zero = identity(3)
    a_one = m_matrix
    a_two = matrix_multiply(m_matrix, affine_recurrence(a_one, a_zero, beta))
    a_three = matrix_multiply(m_matrix, affine_recurrence(a_two, a_one, beta))
    b_values = [a_three, matrix_multiply(m_matrix, a_three)]
    for _ in range(6):
        b_values.append(
            matrix_multiply(
                m_matrix,
                affine_recurrence(b_values[-1], b_values[-2], beta),
            )
        )
    formula_map = matrix_multiply(
        m_matrix,
        matrix_multiply(
            r_zero,
            affine_recurrence(b_values[7], b_values[6], beta),
        ),
    )
    assert formula_map == word_map

    image_scales: list[F] = []
    image_first_ratios: list[F] = []
    image_second_ratios: list[F] = []
    for ray in rays:
        image = r22.matvec(word_map, ray)
        assert all(value > 0 for value in image)
        image_scales.append(image[0])
        image_first_ratios.append(image[1] / image[0])
        image_second_ratios.append(image[2] / image[0])
    assert F(1, 48) < min(image_scales)
    assert max(image_scales) < F(11, 500)
    assert F(1247, 1250) < min(image_first_ratios)
    assert max(image_first_ratios) < F(9977, 10000)
    assert F(107, 125) < min(image_second_ratios)
    assert max(image_second_ratios) < F(2141, 2500)
    assert F(997, 1000) < min(image_first_ratios)
    assert max(image_first_ratios) < F(998, 1000)
    assert F(856, 1000) < min(image_second_ratios)
    assert max(image_second_ratios) < F(857, 1000)

    error_55 = [optimum[i] - points[55][i] for i in range(3)]
    assert r22.matvec(word_map, error_44) == error_55

    # The harmful phase is the second full phase, at stage 47.
    previous_harmful, current_harmful, phase = phase_starts[2]
    assert phase == "F2"
    displacement = matrix_add(previous_harmful, matrix_scale(-1, current_harmful))
    a_q = F(7)
    h_matrix = matrix_scale(a_q, displacement)
    defect_matrix = matrix_add(
        matrix_add(
            matrix_multiply(transpose(current_harmful), matrix_multiply(d_matrix, h_matrix)),
            matrix_multiply(transpose(h_matrix), matrix_multiply(d_matrix, current_harmful)),
        ),
        matrix_scale(
            -1,
            matrix_multiply(transpose(h_matrix), matrix_multiply(d_matrix, h_matrix)),
        ),
    )
    envelope_hessian = matrix_add(
        matrix_scale(kappa, d_matrix),
        matrix_scale(
            -kappa * kappa,
            matrix_multiply(d_matrix, matrix_multiply(h_inverse, d_matrix)),
        ),
    )
    momentum_error = matrix_add(current_harmful, matrix_scale(-a_q, displacement))
    mu_envelope = kappa * F(1, 64)
    potential_matrix = matrix_scale(
        F(1, 2),
        matrix_add(
            matrix_multiply(
                transpose(current_harmful),
                matrix_multiply(envelope_hessian, current_harmful),
            ),
            matrix_scale(
                mu_envelope,
                matrix_multiply(
                    transpose(momentum_error),
                    matrix_multiply(d_matrix, momentum_error),
                ),
            ),
        ),
    )
    defect_lower, defect_upper = interval_quadratic(defect_matrix)
    potential_lower, potential_upper = interval_quadratic(potential_matrix)
    assert defect_lower >= F(1, 5)
    assert potential_upper <= F(2, 25)
    gamma_minus_one = mu_envelope * F(1, 5) / (2 * F(2, 25))
    assert gamma_minus_one == F(315, 16640)
    assert gamma_minus_one / 2 == F(315, 33280)

    return {
        "minimum_phase_margin": min(all_margins),
        "minimum_defect": defect_lower,
        "maximum_potential": potential_upper,
        "minimum_image_scale": min(image_scales),
        "maximum_image_scale": max(image_scales),
    }


def check_c2_residual_obstruction() -> None:
    """Check a rational instance of the scalar C2 equality example."""
    mu = F(1)
    kappa = F(1)
    delta = F(1, 4)
    p = F(1)
    a_ratio = F(1, 2)  # sqrt(delta*kappa/mu)
    point = p / (1 + a_ratio)
    error = p - point
    gap = mu * error * error / 2
    relative_rhs = delta * kappa * point * point / 2
    residual = mu * error
    assert point == F(2, 3)
    assert gap == relative_rhs == F(1, 18)
    assert residual == F(1, 3) > 0


def check_source_guardrails() -> None:
    """Keep theorem labels and their deliberately narrow scopes durable."""
    directory = Path(__file__).resolve().parent
    main_text = (directory / "main.tex").read_text(encoding="utf-8")
    readme_text = (directory / "README.md").read_text(encoding="utf-8")
    status_text = (directory / "STATUS.md").read_text(encoding="utf-8")
    main_scope = " ".join(main_text.split())
    combined_scope = " ".join((readme_text + " " + status_text).split())
    for anchor in (
        "prop:aesp-cd-p4-infinite-inflation",
        "eq:aesp-cd-p4-infinite-word",
        "eq:aesp-cd-p4-infinite-inflation-floor",
        "eq:aesp-cd-p4-infinite-error-contraction",
        "lem:aesp-cd-finite-inner-identities",
        "prop:aesp-cd-c2-residual-stop",
        "cor:aesp-cd-dual-inner-stop",
        "cor:aesp-cd-conditional-finite-acceptance",
    ):
        assert anchor in main_text
    assert "one fixed RPPR instance" in main_scope
    assert "does not refute an accuracy-logarithmic allowance" in main_scope
    assert "no $q\\downarrow0$ scaling obstruction" in main_scope
    assert "no finite-inner work theorem" in main_scope
    assert "actual finite" in main_scope
    assert "horizon-uniform" in combined_scope
    assert "geometrically" in combined_scope
    assert "no finite-inner" in combined_scope
    assert "net" in combined_scope


def main() -> None:
    check_source_guardrails()
    metrics = check_infinite_p4_tail()
    check_c2_residual_obstruction()
    print("Round-023 exact fixed-operator audit passed")
    print("  P4 phase word: F N N F N^6 P0, repeating from stage 44")
    print(
        "  exact cone certificate: "
        f"min-margin={float(metrics['minimum_phase_margin']):.8f}, "
        f"word-scale in ({float(metrics['minimum_image_scale']):.8f}, "
        f"{float(metrics['maximum_image_scale']):.8f})"
    )
    print(
        "  interval certificate: "
        f"defect>={float(metrics['minimum_defect']):.8f}, "
        f"potential<={float(metrics['maximum_potential']):.8f}"
    )
    print(
        "  consequence: I_(44+11N) >= (315/33280)N; error contracts "
        "geometrically; no q-scaling or finite-inner rate claim"
    )


if __name__ == "__main__":
    main()
