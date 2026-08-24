#!/usr/bin/env python3
"""Exact Round-026 audits for persistent Q-energy and reachable K8 mixing.

The checker uses ``Fraction`` throughout.  It verifies the persistent-row
fixed-residual identity, the two Q-energy truncation inequalities, the exact
dense-seed K8 replay, both positive inflation factors, the pre-gate tests,
and the algebraic all-time no-correction suffix.  It does not claim the open
graph-uniform net exponent or an unconditional solver resource vector.
"""

from __future__ import annotations

from fractions import Fraction as F
from experiments.proof_audits import note_directory, note_tex_source


Vector = list[F]
Matrix = list[list[F]]
Pair = tuple[F, F]
PairMatrix = tuple[tuple[F, F], tuple[F, F]]


def matvec(matrix: Matrix, vector: Vector) -> Vector:
    """Return an exact matrix-vector product."""
    return [
        sum((matrix[i][j] * vector[j] for j in range(len(vector))), F(0))
        for i in range(len(matrix))
    ]


def dot(left: Vector, right: Vector) -> F:
    """Return an exact Euclidean inner product."""
    return sum((a * b for a, b in zip(left, right)), F(0))


def pair_mv(matrix: PairMatrix, vector: Pair) -> Pair:
    """Apply a two-value complete-graph reduction."""
    return (
        matrix[0][0] * vector[0] + matrix[0][1] * vector[1],
        matrix[1][0] * vector[0] + matrix[1][1] * vector[1],
    )


def pair_inverse(matrix: PairMatrix) -> PairMatrix:
    """Invert an exact two-by-two matrix."""
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    return (
        (matrix[1][1] / determinant, -matrix[0][1] / determinant),
        (-matrix[1][0] / determinant, matrix[0][0] / determinant),
    )


def pair_multiply(left: PairMatrix, right: PairMatrix) -> PairMatrix:
    """Multiply exact two-by-two matrices."""
    return tuple(
        tuple(sum((left[i][k] * right[k][j] for k in range(2)), F(0)) for j in range(2))
        for i in range(2)
    )  # type: ignore[return-value]


def pair_add(left: PairMatrix, right: PairMatrix) -> PairMatrix:
    """Add exact two-by-two matrices."""
    return tuple(tuple(left[i][j] + right[i][j] for j in range(2)) for i in range(2))  # type: ignore[return-value]


def pair_scale(scale: F, matrix: PairMatrix) -> PairMatrix:
    """Scale an exact two-by-two matrix."""
    return tuple(tuple(scale * matrix[i][j] for j in range(2)) for i in range(2))  # type: ignore[return-value]


def weighted_pair_dot(left: Pair, right: Pair, multiplicity: int = 7) -> F:
    """Inner product for one source value and repeated nonsource values."""
    return left[0] * right[0] + multiplicity * left[1] * right[1]


def complete_reduction(q: F) -> tuple[F, F, F, PairMatrix, PairMatrix, PairMatrix]:
    """Return alpha, kappa, beta, Q, its resolvent, and envelope Hessian."""
    alpha = q * q / (1 + q * q)
    kappa = 1 - 2 * alpha
    beta = (1 - q) / (1 + q)
    diagonal = (1 + alpha) / 2
    off_diagonal = -(1 - alpha) / 14
    matrix: PairMatrix = (
        (diagonal, 7 * off_diagonal),
        (off_diagonal, diagonal + 6 * off_diagonal),
    )
    identity: PairMatrix = ((F(1), F(0)), (F(0), F(1)))
    shifted = pair_add(matrix, pair_scale(kappa, identity))
    inverse = pair_inverse(shifted)
    mapping = pair_scale(kappa, inverse)
    envelope = pair_multiply(pair_scale(kappa, matrix), inverse)
    return alpha, kappa, beta, matrix, mapping, envelope


def check_persistent_driver_identity() -> None:
    """Audit exact residual cancellation and its Q-energy consequence."""
    alpha = F(1, 26)
    beta = F(2, 3)
    kappa = F(12, 13)
    matrix = [
        [F(1 + alpha, 2), -F(1 - alpha, 4), -F(1 - alpha, 4)],
        [-F(1 - alpha, 4), F(1 + alpha, 2), -F(1 - alpha, 4)],
        [-F(1 - alpha, 4), -F(1 - alpha, 4), F(1 + alpha, 2)],
    ]
    current_error = [F(1), F(1), F(1)]
    displacement = [F(3, 20), F(1, 100), F(1, 100)]
    previous_error = [a + b for a, b in zip(current_error, displacement)]
    current_u = matvec(matrix, current_error)
    previous_u = matvec(matrix, previous_error)
    assert all(value >= 0 for value in current_u)

    # Split each exact active-row residual into arbitrary finite s and a.
    current_a = [F(1, 500), F(1, 600), F(1, 700)]
    previous_a = [F(1, 450), F(1, 550), F(1, 650)]
    current_s = [(value - residual) / kappa for value, residual in zip(current_u, current_a)]
    previous_s = [(value - residual) / kappa for value, residual in zip(previous_u, previous_a)]
    assert all(value >= 0 for value in current_s + previous_s)

    finite_driver = [
        max(
            F(0),
            kappa * (beta * old_step - (1 + beta) * new_step)
            + beta * old_residual
            - (1 + beta) * new_residual,
        )
        for old_step, new_step, old_residual, new_residual in zip(
            previous_s,
            current_s,
            previous_a,
            current_a,
        )
    ]
    collapsed_u = [
        max(F(0), beta * old_value - (1 + beta) * new_value)
        for old_value, new_value in zip(previous_u, current_u)
    ]
    q_displacement = matvec(matrix, displacement)
    assert finite_driver == collapsed_u
    assert all(
        value <= beta * max(F(0), q_value) for value, q_value in zip(finite_driver, q_displacement)
    )

    old_energy = dot(previous_error, previous_u)
    new_energy = dot(current_error, current_u)
    displacement_energy = dot(displacement, q_displacement)
    assert old_energy - new_energy >= displacement_energy
    assert dot(finite_driver, finite_driver) <= beta * beta * displacement_energy


def complete_matrix(size: int, alpha: F) -> Matrix:
    """Return the normalized K_size RPPR matrix."""
    diagonal = (1 + alpha) / 2
    off_diagonal = -(1 - alpha) / (2 * (size - 1))
    return [[diagonal if i == j else off_diagonal for j in range(size)] for i in range(size)]


def check_truncation_q_energy() -> None:
    """Check both boundary-aware truncations on exact regular-graph samples."""
    alpha = F(1, 17)
    beta = F(3, 4)
    matrix = complete_matrix(4, alpha)
    displacement = [F(2, 5), F(1, 3), F(1, 4), F(1, 7)]
    base_energy = dot(displacement, matvec(matrix, displacement))
    for cap in (F(0), F(1, 20), F(1, 5), F(1)):
        correction = [min(beta * value, cap) for value in displacement]
        surviving = [beta * value - clipped for value, clipped in zip(displacement, correction)]
        assert dot(correction, matvec(matrix, correction)) <= beta * beta * base_energy
        assert dot(surviving, matvec(matrix, surviving)) <= beta * beta * base_energy


def modes(vector: Pair) -> Pair:
    """Return constant mean and source-orthogonal amplitude on K8."""
    mean = (vector[0] + 7 * vector[1]) / 8
    return mean, vector[0] - mean


def mode_values(constant: F, high: F) -> Pair:
    """Return source/common values from constant and orthogonal amplitudes."""
    return constant + high, constant - high / 7


def check_reachable_k8_pulse() -> None:
    """Replay the exact dense-seed K8 pulse and its infinite suffix guardrail."""
    q = F(1, 10)
    alpha, kappa, beta, matrix, mapping, envelope = complete_reduction(q)
    rho = F(1, 112)
    optimum: Pair = (F(5693, 569702), F(2500, 284851))
    seed: Pair = (F(363437, 651088), F(41093, 651088))
    assert seed[0] + 7 * seed[1] == 1
    assert min(seed) > 0
    assert pair_mv(matrix, optimum) == (
        alpha * (seed[0] - 7 * rho) / 7,
        alpha * (seed[1] - 7 * rho) / 7,
    )

    previous: Pair = (F(0), F(0))
    point: Pair = (F(0), F(0))
    records = []
    for stage in range(20):
        displacement = (point[0] - previous[0], point[1] - previous[1])
        trial = (
            point[0] + beta * displacement[0],
            point[1] + beta * displacement[1],
        )
        trial_error = (optimum[0] - trial[0], optimum[1] - trial[1])
        residual = pair_mv(matrix, trial_error)
        delta = max(F(0), -residual[0] / alpha, -residual[1] / alpha)
        caps = (beta * displacement[0], beta * displacement[1])
        correction = (min(caps[0], delta), min(caps[1], delta))
        center = (trial[0] - correction[0], trial[1] - correction[1])
        if correction == (F(0), F(0)):
            phase = "N"
        elif correction == caps:
            phase = "F"
        else:
            phase = "P0" if -residual[0] >= -residual[1] else "P1"

        error = (optimum[0] - point[0], optimum[1] - point[1])
        momentum_error = (
            error[0] - (1 / q - 1) * displacement[0],
            error[1] - (1 / q - 1) * displacement[1],
        )
        corrected_error = (
            momentum_error[0] + (1 + q) * correction[0] / q,
            momentum_error[1] + (1 + q) * correction[1] / q,
        )
        potential = (
            weighted_pair_dot(error, pair_mv(envelope, error))
            + kappa * q * q * weighted_pair_dot(momentum_error, momentum_error)
        ) / 2
        defect = weighted_pair_dot(corrected_error, corrected_error) - weighted_pair_dot(
            momentum_error,
            momentum_error,
        )
        gamma = 1 + kappa * q * q * defect / (2 * potential)
        gate = max(pair_mv(matrix, error))
        records.append(
            (phase, point, error, residual, delta, caps, correction, defect, potential, gamma, gate)
        )

        center_error = (optimum[0] - center[0], optimum[1] - center[1])
        next_error = pair_mv(mapping, center_error)
        next_point = (optimum[0] - next_error[0], optimum[1] - next_error[1])
        previous, point = point, next_point

    assert records[1][1] == (F(11009, 22788080), F(3763, 113940400))
    assert records[2][1] == (F(89111, 81386000), F(10523, 81386000))
    assert [record[0] for record in records[:5]] == ["N", "N", "P0", "F", "N"]
    assert all(record[0] == "N" for record in records[4:])

    stage_two = records[2]
    assert stage_two[3] == (
        -F(191403, 126587784400),
        F(12270123, 126587784400),
    )
    assert stage_two[4] == F(191403, 1253344400)
    assert stage_two[5] == (F(392121, 783340250), F(22437, 284851000))
    assert stage_two[4] < stage_two[5][0]
    assert stage_two[4] > stage_two[5][1]
    assert stage_two[9] == F(57072309867, 51440146040) > 1

    stage_three = records[3]
    assert stage_three[4] == F(479606913, 62667220000)
    assert stage_three[5] == (
        F(4543516557, 13786788400000),
        F(1024681671, 13786788400000),
    )
    assert stage_three[4] > max(stage_three[5])
    assert stage_three[9] == F(192036347475007, 168765931042095) > 1

    # The displayed defect ratio uses the original coordinates, adding the
    # common regular degree factor seven to the reduced weighted defect.
    defect_ratio = 7 * stage_two[7] / (alpha * alpha * stage_two[4] * stage_two[4])
    assert defect_ratio == F(48663286609745269, 139594225) > 10**8

    expected_gates = (
        F(40343, 57539902),
        F(10791, 22788080),
        F(12213423, 57539902000),
        F(1024681671, 11507980400000),
    )
    assert tuple(record[10] for record in records[:4]) == expected_gates
    assert all(value > alpha * F(1, 1000) for value in expected_gates)

    constant, high = modes(stage_three[2])
    assert constant == F(556598061, 65108800000)
    assert high == -F(38318427, 716196800000)
    assert high / constant == -F(17521, 2799533)
    initial_amplitude_square = (high / constant) ** 2 * F(407, 400)
    assert initial_amplitude_square == F(11358461317, 284995818839600)
    assert initial_amplitude_square < F(49, 4477) ** 2
    # For every later trial t=3+k (k>=1), the envelope is maximal at k=1:
    # (11/7)*(sqrt(7/11))^(k+1)/(1+(k+1)/10) = 5/6 there.
    first_trial_envelope = F(11, 7) * F(7, 11) / (1 + F(2, 10))
    assert first_trial_envelope == F(5, 6)
    assert initial_amplitude_square * first_trial_envelope**2 < F(49, 4477) ** 2


def check_q_family_bank_stop() -> None:
    """Audit the small-q reachable prefix separating raw defect and Q-energy."""
    for q in (F(1, 100), F(1, 101), F(1, 200), F(1, 1000)):
        alpha, kappa, beta, matrix, mapping, envelope = complete_reduction(q)
        high_eigenvalue = (4 + 3 * alpha) / 7
        high_amplitude = 12 * q * q
        unscaled_error = mode_values(F(1), high_amplitude)
        scale = F(1, 112)
        optimum = tuple(scale * value for value in unscaled_error)
        q_error = pair_mv(matrix, unscaled_error)
        assert q_error[0] > 0 and q_error[1] > 0
        assert (q_error[1] > 0) == (84 * q * q < 1)
        seed = tuple((1 + value / alpha) / 16 for value in q_error)
        assert seed[0] + 7 * seed[1] == 1
        assert min(seed) > 0
        assert pair_mv(matrix, optimum) == (
            alpha * (seed[0] - F(1, 16)) / 7,
            alpha * (seed[1] - F(1, 16)) / 7,
        )

        low_mapping = 1 - q * q
        high_mapping = kappa / (kappa + high_eigenvalue)
        low_trial = (1 + beta) * low_mapping - beta
        high_trial = (1 + beta) * high_mapping - beta
        low_two_step = low_mapping * low_trial
        high_two_step = high_mapping * high_trial
        assert low_two_step == 1 - 3 * q * q + 2 * q**3
        assert 0 < high_mapping < 1
        assert 0 < high_trial < F(3, 10)

        first_trial_error = mode_values(scale * low_trial, scale * high_trial * high_amplitude)
        assert min(pair_mv(matrix, first_trial_error)) > 0
        first_error = mode_values(scale * low_mapping, scale * high_mapping * high_amplitude)
        second_error = mode_values(scale * low_two_step, scale * high_two_step * high_amplitude)
        first_point = tuple(optimum[i] - first_error[i] for i in range(2))
        second_point = tuple(optimum[i] - second_error[i] for i in range(2))
        assert min(first_point) > 0 and min(second_point) > 0

        displacement = tuple(first_error[i] - second_error[i] for i in range(2))
        assert min(displacement) > 0
        sigma = beta * (2 + beta)
        low_filter = alpha * (sigma * alpha - kappa) / (kappa + alpha) ** 2
        high_filter = (
            high_eigenvalue * (sigma * high_eigenvalue - kappa) / (kappa + high_eigenvalue) ** 2
        )
        assert low_filter == -q * q + q**4 * (1 + sigma)
        assert sigma >= F(29, 10)
        assert high_filter >= F(23, 245)
        source_filter = low_filter + high_filter * high_amplitude
        assert source_filter >= F(31, 245) * q * q
        delta = kappa * scale * source_filter / alpha
        caps = tuple(beta * value for value in displacement)
        assert delta > scale / 10
        assert max(caps) <= scale * 14 * q * q < scale / 10

        momentum_error = tuple(second_error[i] - (1 - q) * displacement[i] / q for i in range(2))
        defect = weighted_pair_dot(second_error, second_error) - weighted_pair_dot(
            momentum_error,
            momentum_error,
        )
        low_defect_unscaled = 32 * q * (1 - q) ** 4 * (1 + q)
        high_defect_unscaled = defect / scale**2 - low_defect_unscaled
        assert abs(high_defect_unscaled) <= F(8, 7) * (144 * q * q + 288 * q**3)
        assert defect / scale**2 > 28 * q

        stage_energy_drop = 8 * alpha * (low_mapping**2 - low_two_step**2)
        stage_energy_drop += (
            F(8, 7) * high_eigenvalue * high_amplitude**2 * (high_mapping**2 - high_two_step**2)
        )
        assert stage_energy_drop < 197 * q**4
        assert (defect / scale**2) / stage_energy_drop > F(28, 197) / q**3

        potential = (
            weighted_pair_dot(second_error, pair_mv(envelope, second_error))
            + kappa * q * q * weighted_pair_dot(momentum_error, momentum_error)
        ) / 2
        gamma = 1 + kappa * q * q * defect / (2 * potential)
        assert gamma > 1
        if q == F(1, 100):
            assert gamma == F(476021161902906, 466879074517519)
        assert low_two_step / 112 > F(1, 1000)


def check_source_guardrails() -> None:
    """Keep the new package attached to its deliberately incomplete scope."""
    directory = note_directory("aesp_cd_l1_rppr")
    main_text = note_tex_source("aesp_cd_l1_rppr")
    readme_text = (directory / "README.md").read_text(encoding="utf-8")
    status_text = (directory / "STATUS.md").read_text(encoding="utf-8")
    combined = " ".join((main_text + " " + readme_text + " " + status_text).split())
    for anchor in (
        "lem:aesp-cd-persistent-square-ledger",
        "lem:aesp-cd-truncation-q-energy",
        "prop:aesp-cd-k8-reachable-pulse",
        "prop:aesp-cd-k8-q-bank-stop",
        "eq:aesp-cd-k8-reachable-gammas",
    ):
        assert anchor in main_text
    for phrase in (
        "actual finite",
        "persistent",
        "Euclidean collateral",
        "not an additive-resistant obstruction",
        "does not refute",
        "do not supply a bound",
        "No graph-uniform exact accelerated solver",
    ):
        assert phrase in combined
    assert "persistent_q_energy" in readme_text


def main() -> None:
    check_persistent_driver_identity()
    check_truncation_q_energy()
    check_reachable_k8_pulse()
    check_q_family_bank_stop()
    check_source_guardrails()
    print("Round-026 exact persistent-energy audit passed")
    print("  persistent rows: finite residuals cancel into u_t = Q e_t")
    print("  window bank: controller squares, corrections, and surviving momentum telescope")
    print("  reachable K8: N,N,P0,F,N^infinity with two positive pre-gate gammas")
    print("  small-q K8: a raw same-window Q-energy payment needs Omega(1/q^3)")
    print("  scope: the Euclidean collateral/net-exponent interface remains open")


if __name__ == "__main__":
    main()
