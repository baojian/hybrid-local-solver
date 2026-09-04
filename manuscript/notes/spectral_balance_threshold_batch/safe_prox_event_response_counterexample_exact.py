#!/usr/bin/env python3
"""Exact arithmetic audit for SAFE_PROX_EVENT_RESPONSE_COUNTEREXAMPLE.md.

Only the one-parameter powers of ``delta`` and ``epsilon`` are suppressed.
All displayed coefficient identities are checked using Fraction arithmetic.
"""

from fractions import Fraction as F


def matvec(matrix: list[list[F]], vector: list[F]) -> list[F]:
    return [sum((row[j] * vector[j] for j in range(len(vector))), F(0)) for row in matrix]


def solve(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    augmented = [row[:] + [rhs[i]] for i, row in enumerate(matrix)]
    size = len(matrix)
    for column in range(size):
        pivot = next(row for row in range(column, size) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [entry / scale for entry in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            scale = augmented[row][column]
            augmented[row] = [
                augmented[row][j] - scale * augmented[column][j] for j in range(size + 1)
            ]
    return [augmented[i][-1] for i in range(size)]


def dot(left: list[F], right: list[F]) -> F:
    return sum((x * y for x, y in zip(left, right)), F(0))


def main() -> None:
    q_matrix = [
        [F(9, 16), F(-7, 32), F(-7, 32)],
        [F(-7, 32), F(9, 16), F(-7, 32)],
        [F(-7, 32), F(-7, 32), F(9, 16)],
    ]
    ones = [F(1), F(1), F(1)]
    assert matvec(q_matrix, ones) == [F(1, 8)] * 3

    # sqrt(2) times the canonical source-0 optimum and load at rho=1/100.
    scaled_optimum = [F(21, 50), F(13, 50), F(13, 50)]
    scaled_load = [F(49, 400), F(-1, 400), F(-1, 400)]
    assert matvec(q_matrix, scaled_optimum) == scaled_load

    # tau/epsilon=(2,3,4), direction/delta=ones.  The starting slack
    # coefficient follows from Q_ij min(tau_i,tau_j).
    freeze = [F(2), F(3), F(4)]
    starting_slack = [
        sum(
            (q_matrix[i][j] * min(freeze[i], freeze[j]) for j in range(3)),
            F(0),
        )
        for i in range(3)
    ]
    assert starting_slack == [F(1, 4), F(19, 32), F(37, 32)]

    old_center_slack = [starting_slack[i] + matvec(q_matrix, starting_slack)[i] for i in range(3)]
    assert old_center_slack == [F(1, 128), F(635, 1024), F(1661, 1024)]
    assert all(entry > 0 for entry in old_center_slack)

    error = solve(q_matrix, starting_slack)
    assert error == [F(24, 5), F(131, 25), F(149, 25)]

    delta = F(1, 100)
    epsilon_max = F(1, 100)
    # Since sqrt(2)<3/2, min_i x*_i > 13/75.  This verifies positivity
    # of x^- uniformly over the stated parameter interval.
    assert delta * (F(1) + epsilon_max * max(error)) < F(13, 75)

    # The raw barrier violation is positive throughout the interval.  Its
    # quotient by alpha is at most theta*delta and hence below y because x>0.
    assert F(1, 16) - epsilon_max * max(starting_slack) > 0

    accepted = freeze
    final_slack = [starting_slack[i] - matvec(q_matrix, accepted)[i] for i in range(3)]
    assert final_slack == [F(21, 32), F(7, 32), F(0)]

    # Direct event simulation: initial pressure 1/8; after vertex zero
    # freezes the remaining-row pressure is 11/32; after vertex one freezes
    # the final pressure is 9/16.
    assert starting_slack[0] / F(1, 8) == freeze[0]
    row_one_at_first_event = starting_slack[1] - freeze[0] * F(1, 8)
    assert freeze[0] + row_one_at_first_event / F(11, 32) == freeze[1]
    row_two_at_second_event = (
        starting_slack[2] - freeze[0] * F(1, 8) - (freeze[1] - freeze[0]) * F(11, 32)
    )
    assert freeze[1] + row_two_at_second_event / F(9, 16) == freeze[2]

    # Scalar ray and barrier have coefficient 2*ones.  Reflection is s/a.
    scalar_and_barrier = [F(2)] * 3
    reflection = [entry / F(9, 16) for entry in starting_slack]
    assert reflection == [F(4, 9), F(19, 18), F(37, 18)]
    assert all(scalar_and_barrier[i] <= accepted[i] for i in range(3))
    assert all(reflection[i] <= accepted[i] for i in range(3))

    variation = sum(
        (-q_matrix[i][j] * abs(freeze[i] - freeze[j]) for i in range(3) for j in range(i + 1, 3)),
        F(0),
    )
    assert variation == F(7, 8)

    identity_plus_q = [
        [q_matrix[i][j] + (F(1) if i == j else F(0)) for j in range(3)] for i in range(3)
    ]
    response = solve(identity_plus_q, final_slack)
    assert response == [F(238, 513), F(112, 513), F(49, 513)]
    response_q = matvec(q_matrix, response)
    response_energy = dot(response, response) + F(1, 2) * dot(response, response_q)
    assert response_energy == F(876169, 2807136)

    error_norm_squared = dot(error, error)
    assert error_norm_squared == F(53762, 625)
    whole_future_bound = (F(1) + F(25, 64)) * error_norm_squared
    assert whole_future_bound == F(2392409, 20000)
    divergence_coefficient = variation / whole_future_bound
    assert divergence_coefficient == F(17500, 2392409)

    print("all exact identities verified")
    print(f"V/(delta^2 epsilon) = {variation}")
    print(f"immediate response energy/(delta^2 epsilon^2) = {response_energy}")
    print(f"whole-future upper-bound coefficient = {whole_future_bound}")
    print(f"V/whole-future-energy >= ({divergence_coefficient})/epsilon")


if __name__ == "__main__":
    main()
