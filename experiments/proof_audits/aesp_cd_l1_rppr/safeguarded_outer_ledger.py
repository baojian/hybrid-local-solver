#!/usr/bin/env python3
"""Exact Round-022 audits for the safeguarded AESP-CD outer ledger.

The abstract countermodel below is deliberately not an RPPR trajectory.  The
path traces do use the exact safeguarded shifted-minimizer recurrence, written
in degree-scaled coordinates.  All algebraic state, active-set solves, KKT
tests, support schedules, and signs are checked with ``Fraction``.  Decimal
logarithms are reported only as reproducibility metrics.

The default audit includes the small P4 trace and runs quickly.  Pass
``--with-p7`` to reproduce the longer corroborating P7 scaffolding trace.
Neither trace is a finite-inner implementation or an end-to-end work ledger.
"""

from __future__ import annotations

import argparse
from decimal import Decimal, localcontext
from fractions import Fraction as F
from experiments.proof_audits import note_directory, note_tex_source


def matvec(matrix: list[list[F]], vector: list[F]) -> list[F]:
    """Return an exact matrix-vector product."""
    return [
        sum((matrix[i][j] * vector[j] for j in range(len(vector))), F(0))
        for i in range(len(matrix))
    ]


def dot(left: list[F], right: list[F]) -> F:
    """Return an exact inner product."""
    return sum((a * b for a, b in zip(left, right)), F(0))


def solve_linear(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    """Solve one nonsingular rational system by exact elimination."""
    n = len(rhs)
    augmented = [list(matrix[i]) + [rhs[i]] for i in range(n)]
    for column in range(n):
        pivot = next(
            (row for row in range(column, n) if augmented[row][column]),
            None,
        )
        if pivot is None:
            raise ArithmeticError("singular active block")
        augmented[column], augmented[pivot] = (
            augmented[pivot],
            augmented[column],
        )
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(n):
            if row == column or not augmented[row][column]:
                continue
            scale = augmented[row][column]
            augmented[row] = [
                augmented[row][entry] - scale * augmented[column][entry] for entry in range(n + 1)
            ]
    return [augmented[row][-1] for row in range(n)]


def solve_stieltjes_obstacle(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    """Solve x>=0, Mx-rhs>=0, x_i(Mx-rhs)_i=0 exactly."""
    n = len(rhs)
    active = {index for index, value in enumerate(rhs) if value > 0}
    seen: set[tuple[int, ...]] = set()
    for _ in range(10_000):
        signature = tuple(sorted(active))
        if signature in seen:
            raise ArithmeticError("active-set cycle")
        seen.add(signature)

        point = [F(0) for _ in range(n)]
        if active:
            indices = sorted(active)
            solution = solve_linear(
                [[matrix[i][j] for j in indices] for i in indices],
                [rhs[i] for i in indices],
            )
            nonpositive = [indices[k] for k, value in enumerate(solution) if value <= 0]
            if nonpositive:
                active.remove(min(nonpositive))
                continue
            for index, value in zip(indices, solution):
                point[index] = value

        product = matvec(matrix, point)
        violated = [
            index for index in range(n) if index not in active and rhs[index] - product[index] > 0
        ]
        if violated:
            active.add(min(violated))
            continue

        slack = [product[index] - rhs[index] for index in range(n)]
        assert all(value >= 0 for value in point)
        assert all(value >= 0 for value in slack)
        assert all(point[index] * slack[index] == 0 for index in range(n))
        return point
    raise ArithmeticError("active-set iteration cap")


def path_matrices(
    n: int,
    seed: int,
    q: F,
    rho: F,
) -> tuple[list[int], F, F, list[list[F]], list[F], list[list[F]]]:
    """Build the exact RPPR and shifted matrices in degree-scaled coordinates."""
    degree = [1] + [2] * (n - 2) + [1]
    q_squared = q * q
    alpha = q_squared / (1 + q_squared)
    kappa = (1 - q_squared) / (1 + q_squared)
    matrix = [[F(0) for _ in range(n)] for _ in range(n)]
    for index in range(n):
        matrix[index][index] = F(1 + alpha, 2) * degree[index]
    for index in range(n - 1):
        matrix[index][index + 1] = matrix[index + 1][index] = -F(1 - alpha, 2)
    load = [alpha * ((F(1) if index == seed else F(0)) - rho * degree[index]) for index in range(n)]
    shifted = [
        [matrix[i][j] + (kappa * degree[i] if i == j else 0) for j in range(n)] for i in range(n)
    ]
    return degree, alpha, kappa, matrix, load, shifted


def weighted_norm_squared(vector: list[F], degree: list[int]) -> F:
    """Return the source-coordinate Euclidean norm in scaled coordinates."""
    return sum(
        (F(degree[index]) * value * value for index, value in enumerate(vector)),
        F(0),
    )


def objective(point: list[F], matrix: list[list[F]], load: list[F]) -> F:
    """Return the exact degree-scaled obstacle objective."""
    return dot(point, matvec(matrix, point)) / 2 - dot(load, point)


def shifted_minimizer(
    center: list[F],
    degree: list[int],
    kappa: F,
    shifted: list[list[F]],
    load: list[F],
) -> list[F]:
    """Return the exact shifted obstacle minimizer."""
    rhs = [load[index] + kappa * degree[index] * center[index] for index in range(len(degree))]
    return solve_stieltjes_obstacle(shifted, rhs)


def envelope(
    center: list[F],
    degree: list[int],
    kappa: F,
    shifted: list[list[F]],
    load: list[F],
    matrix: list[list[F]],
) -> F:
    """Return the exact Moreau-envelope value."""
    point = shifted_minimizer(center, degree, kappa, shifted, load)
    displacement = [point[index] - center[index] for index in range(len(center))]
    return objective(point, matrix, load) + kappa * weighted_norm_squared(displacement, degree) / 2


def decimal_log(value: F) -> Decimal:
    """Evaluate log of a positive rational at fixed high decimal precision."""
    assert value > 0
    with localcontext() as context:
        context.prec = 80
        ratio = Decimal(value.numerator) / Decimal(value.denominator)
        return +ratio.ln()


def check_abstract_countermodel(q: F, cycles: int = 20) -> tuple[Decimal, Decimal]:
    """Audit the exact abstract two-step ledger countermodel."""
    assert 0 < q <= F(1, 10)
    alpha = q * q / (1 + q * q)
    kappa = (1 - q * q) / (1 + q * q)
    beta = (1 - q) / (1 + q)
    a = (1 - q) / q
    c = (1 + q) / q
    tau = F(5, 2) * q * q
    contraction = 1 - tau * (1 + F(3, 2) * beta)
    assert contraction >= F(15, 16)

    p_odd = (1 - tau) ** 2 + (1 - F(5, 2) * q) ** 2
    h_scale = F(15, 4) * q * (1 - q) ** 2 / (1 + q)
    p_even = contraction**2 + (contraction - h_scale) ** 2
    polynomial = 8 - 69 * q + 418 * q**2 - 750 * q**3 + 430 * q**4 - 225 * q**5 - 100 * q**6
    assert (1 - q) * p_odd - p_even == q * polynomial / (16 * (1 + q) ** 2)
    assert polynomial > 0
    assert 2 * (1 - q) - p_odd == q * (12 - 5 * q - 25 * q**3) / 4
    assert p_even <= (1 - q) * p_odd
    assert p_odd <= 2 * (1 - q)

    x = F(0)
    x_star = F(1)
    previous_ell = F(0)
    previous_s = F(0)
    total_correction = F(0)
    total_inflation = Decimal(0)

    # The scalar start-mass ledger is included as an abstract number ledger.
    ell_increments: list[F] = []
    for cycle in range(1, cycles + 1):
        error = x_star - x

        d_odd = tau * error
        x_odd = x + d_odd
        s_odd = x_odd - previous_ell
        assert s_odd == d_odd
        collapse_odd = max(beta * previous_s - (1 + beta) * s_odd, F(0))
        assert collapse_odd == 0
        delta_odd = kappa * collapse_odd / alpha
        r_odd = min(beta * d_odd, delta_odd)
        assert r_odd == 0
        ell_odd = x_odd + beta * d_odd
        ell_increments.append(ell_odd - previous_ell)
        e_odd = x_star - x_odd
        phi_odd_scaled = e_odd**2 + (e_odd - a * d_odd) ** 2
        assert phi_odd_scaled == error**2 * p_odd

        d_even = F(3, 2) * beta * d_odd
        x_even = x_odd + d_even
        s_even = x_even - ell_odd
        assert s_even == beta * d_odd / 2
        collapse_even = beta * s_odd - (1 + beta) * s_even
        assert collapse_even == beta * (1 - beta) * d_odd / 2 > 0
        delta_even = kappa * collapse_even / alpha
        r_even = min(beta * d_even, delta_even)
        assert r_even == beta * d_even
        ell_even = x_even + beta * d_even - r_even
        assert ell_even == x_even
        ell_increments.append(ell_even - ell_odd)

        assert x <= x_odd <= ell_odd <= x_even <= ell_even <= x_star
        e_even = x_star - x_even
        y_even = x_even + beta * d_even
        assert y_even < x_star
        h_even = c * r_even
        assert h_even == a * d_even
        normalized = h_even / e_even
        assert F(5, 2) * q <= normalized <= F(2, 5)
        defect = h_even * (2 * e_even - h_even)
        assert defect > 0

        phi_even_scaled = e_even**2 + (e_even - a * d_even) ** 2
        assert phi_even_scaled == error**2 * p_even
        assert phi_even_scaled <= (1 - q) * phi_odd_scaled
        gamma = 1 + defect / phi_even_scaled
        assert gamma == 2 * e_even**2 / phi_even_scaled > 1
        assert decimal_log(gamma) >= Decimal(q.numerator) / Decimal(q.denominator)
        total_inflation += decimal_log(gamma)

        total_correction += r_even
        x = x_even
        previous_ell = ell_even
        previous_s = s_even
        assert x_star - x == contraction * error
        assert contraction**2 * error**2 * p_odd <= ((1 - q) * 2 * e_even**2)

    assert all(increment >= 0 for increment in ell_increments)
    assert sum(ell_increments, F(0)) == previous_ell < 1
    assert alpha + kappa * sum(ell_increments, F(0)) <= alpha + kappa
    assert total_correction <= beta * x < beta
    assert total_inflation >= cycles * Decimal(q.numerator) / Decimal(q.denominator)

    final_phi_ratio = F(2, 1) / (contraction ** (2 * (cycles - 1)) * p_even)
    progress = decimal_log(final_phi_ratio)
    return total_inflation, progress


def simulate_path(
    n: int,
    seed: int,
    q: F,
    rho: F,
    stages: int,
) -> dict[str, object]:
    """Run the exact safeguarded recurrence on one path."""
    degree, alpha, kappa, matrix, load, shifted = path_matrices(n, seed, q, rho)
    beta = (1 - q) / (1 + q)
    mu = kappa * q * q
    optimum = solve_stieltjes_obstacle(matrix, load)
    optimum_value = objective(optimum, matrix, load)
    zero = [F(0)] * n
    previous = zero[:]
    point = zero[:]
    correction_stages: list[int] = []
    positive_stages: list[int] = []
    support_history: list[tuple[int, ...]] = []
    potentials: list[F] = []
    gammas: list[F] = []
    inflation = Decimal(0)

    for stage in range(stages + 1):
        support_history.append(tuple(index for index, value in enumerate(point) if value))
        displacement = [point[index] - previous[index] for index in range(n)]
        extrapolate = [point[index] + beta * displacement[index] for index in range(n)]
        lower_residual = [
            load[index] - value for index, value in enumerate(matvec(matrix, extrapolate))
        ]
        support = [index for index, value in enumerate(extrapolate) if value]
        delta = max(
            [F(0)] + [-lower_residual[index] / (alpha * degree[index]) for index in support]
        )
        lower = [max(F(0), extrapolate[index] - delta) for index in range(n)]
        center = [max(point[index], lower[index]) for index in range(n)]
        correction = [extrapolate[index] - center[index] for index in range(n)]
        if any(correction):
            correction_stages.append(stage)

        momentum = [point[index] + (1 / q - 1) * displacement[index] for index in range(n)]
        corrected_momentum = [
            momentum[index] - (1 + q) * correction[index] / q for index in range(n)
        ]
        potential = (
            envelope(point, degree, kappa, shifted, load, matrix)
            - optimum_value
            + mu
            * weighted_norm_squared(
                [momentum[index] - optimum[index] for index in range(n)],
                degree,
            )
            / 2
        )
        assert potential > 0 or point == optimum
        potentials.append(potential)
        if potential:
            defect = weighted_norm_squared(
                [corrected_momentum[index] - optimum[index] for index in range(n)],
                degree,
            ) - weighted_norm_squared(
                [momentum[index] - optimum[index] for index in range(n)],
                degree,
            )
            gamma = 1 + mu * defect / (2 * potential)
            assert 0 <= gamma <= 2
        else:
            gamma = F(1)
        gammas.append(gamma)
        if gamma > 1:
            positive_stages.append(stage)
            inflation += decimal_log(gamma)

        if stage == stages:
            break
        next_point = shifted_minimizer(center, degree, kappa, shifted, load)
        assert all(
            point[index] <= center[index] <= next_point[index] <= optimum[index]
            for index in range(n)
        )
        previous, point = point, next_point

    return {
        "degree": degree,
        "optimum": optimum,
        "support_history": support_history,
        "correction_stages": correction_stages,
        "positive_stages": positive_stages,
        "potentials": potentials,
        "gammas": gammas,
        "inflation": inflation,
        "progress": decimal_log(potentials[0] / potentials[-1]),
    }


def check_p4() -> dict[str, object]:
    """Reproduce the exact clean P4 trace through stage 500."""
    output = simulate_path(4, 0, F(1, 8), F(7, 40), 500)
    assert output["degree"] == [1, 2, 2, 1]
    assert output["optimum"] == [
        F(16513, 423720),
        F(37, 2568),
        F(713, 423720),
        F(0),
    ]

    support_history = output["support_history"]
    assert support_history[0] == ()
    assert support_history[1] == (0,)
    assert all(value == (0, 1) for value in support_history[2:7])
    assert all(value == (0, 1, 2) for value in support_history[7:])

    expected_corrections = [3, 7, 14]
    for index in range(44):
        expected_corrections.extend([21 + 11 * index, 22 + 11 * index, 25 + 11 * index])
    assert output["correction_stages"] == expected_corrections
    assert output["positive_stages"] == [25 + 11 * index for index in range(44)]
    assert len(output["correction_stages"]) == 135
    assert len(output["positive_stages"]) == 44

    inflation = output["inflation"]
    progress = output["progress"]
    assert abs(inflation - Decimal("1.023645592839495300681440396")) < Decimal("5e-27")
    assert abs(progress - Decimal("348.2581722210201407831286779723")) < Decimal("5e-28")
    return output


def check_p7() -> dict[str, object]:
    """Reproduce the longer corroborating P7 scaffolding trace."""
    output = simulate_path(7, 0, F(1, 5), F(1, 20), 800)
    assert output["degree"] == [1, 2, 2, 2, 2, 2, 1]
    assert output["optimum"] == [
        F(55266739, 362793870),
        F(594736, 6718405),
        F(17005619, 362793870),
        F(139236, 6718405),
        F(2137219, 362793870),
        F(0),
        F(0),
    ]

    support_history = output["support_history"]
    assert support_history[0] == ()
    assert support_history[1] == (0, 1)
    assert all(value == (0, 1, 2) for value in support_history[2:5])
    assert all(value == (0, 1, 2, 3) for value in support_history[5:9])
    assert all(value == (0, 1, 2, 3, 4) for value in support_history[9:])
    assert len(output["correction_stages"]) == 122
    assert len(output["positive_stages"]) == 39
    assert output["positive_stages"][-1] == 796

    inflation = output["inflation"]
    progress = output["progress"]
    assert abs(inflation - Decimal("7.294522704368255655469798574")) < Decimal("5e-27")
    assert abs(progress - Decimal("521.4681823472578687827214440085")) < Decimal("5e-28")
    return output


def decimal_ratio(left: Decimal, right: Decimal) -> Decimal:
    """Return one high-precision diagnostic ratio."""
    with localcontext() as context:
        context.prec = 30
        return +(left / right)


def check_source_guardrails() -> None:
    """Keep the durable theorem labels and narrow scopes attached to the audit."""
    directory = note_directory("aesp_cd_l1_rppr")
    main_text = note_tex_source("aesp_cd_l1_rppr")
    readme_text = (directory / "README.md").read_text(encoding="utf-8")
    main_scope = " ".join(main_text.split())
    readme_scope = " ".join(readme_text.split())
    for anchor in (
        "prop:aesp-cd-ledger-only-insufficient",
        "eq:aesp-cd-fixed-operator-relation",
        "prop:aesp-cd-p4-late-inflation",
    ):
        assert anchor in main_text
    assert "not an exact proximal trajectory" in main_scope
    assert "no fixed Stieltjes operator $Q$" in main_scope
    assert "finite exact trace" in main_scope
    assert "not an asymptotic counterexample" in main_scope
    assert "finite-inner or end-to-end work lower bound" in main_scope
    assert "not an RPPR instance or an exact-proximal trajectory" in readme_scope
    assert "prove no infinite periodicity" in readme_scope
    assert "finite-inner work theorem" in readme_scope


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--with-p7",
        action="store_true",
        help="also run the longer exact P7 corroboration trace",
    )
    args = parser.parse_args()
    check_source_guardrails()

    print("abstract ledger-only countermodel")
    for q in (F(1, 100), F(1, 20), F(1, 10)):
        inflation, progress = check_abstract_countermodel(q)
        print(f"  q={q}: cycles=20, I={inflation:.15f}, log-potential-progress={progress:.15f}")

    p4 = check_p4()
    p4_inflation = p4["inflation"]
    p4_progress = p4["progress"]
    assert isinstance(p4_inflation, Decimal)
    assert isinstance(p4_progress, Decimal)
    print("exact P4 finite trace")
    print(
        "  degree=(1,2,2,1), support=(empty; {0}; {0,1}; {0,1,2}), "
        "corrections=135, positive=44, last-positive=498"
    )
    print(
        f"  I_500={p4_inflation:.16f}, "
        f"log(Phi_0/Phi_500)={p4_progress:.16f}, "
        f"I/progress={decimal_ratio(p4_inflation, p4_progress):.16f}, "
        f"I/(qT)={decimal_ratio(p4_inflation, Decimal('62.5')):.16f}"
    )

    if args.with_p7:
        p7 = check_p7()
        p7_inflation = p7["inflation"]
        p7_progress = p7["progress"]
        assert isinstance(p7_inflation, Decimal)
        assert isinstance(p7_progress, Decimal)
        print("exact P7 corroborating finite trace")
        print(
            "  degree=(1,2,2,2,2,2,1), support additions at 1,2,5,9, "
            "corrections=122, positive=39, last-positive=796"
        )
        print(f"  I_800={p7_inflation:.16f}, log(Phi_0/Phi_800)={p7_progress:.16f}")

    print(
        "scope: exact algebraic audit/scaffolding only; no RPPR realization "
        "for the abstract sequence and no finite-inner or end-to-end work "
        "theorem for either path trace"
    )


if __name__ == "__main__":
    main()
