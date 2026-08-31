#!/usr/bin/env python3
"""Exact audit of the margin-free safe-pivot-or-stop dichotomy.

The matrices are rational tridiagonal Stieltjes matrices with
``(1/5) I <= Q <= I``.  All comparisons, face solves, objective gaps, and
threshold tests use ``Fraction`` arithmetic; no floating-point sign decides a
branch.
"""

from fractions import Fraction as F


def matvec(matrix, vector):
    return [sum((a * b for a, b in zip(row, vector)), F(0)) for row in matrix]


def dot(left, right):
    return sum((a * b for a, b in zip(left, right)), F(0))


def add(left, right, scale=F(1)):
    return [a + scale * b for a, b in zip(left, right)]


def solve(matrix, rhs):
    augmented = [list(row) + [value] for row, value in zip(matrix, rhs)]
    n = len(rhs)
    for column in range(n):
        pivot = next(row for row in range(column, n) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            scale = augmented[row][column]
            augmented[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(augmented[row], augmented[column])
            ]
    return [row[-1] for row in augmented]


def principal(matrix, indices):
    return [[matrix[i][j] for j in indices] for i in indices]


def face_vector(matrix, rhs, indices):
    vector = [F(0) for _ in rhs]
    values = solve(principal(matrix, indices), [rhs[i] for i in indices])
    for index, value in zip(indices, values):
        vector[index] = value
    return vector


def objective(matrix, rhs, vector):
    return dot(vector, matvec(matrix, vector)) / 2 - dot(rhs, vector)


def path_matrix(n):
    matrix = [[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        matrix[i][i] = F(3, 5)
        if i:
            matrix[i][i - 1] = matrix[i - 1][i] = -F(1, 5)
    return matrix


def reachable_faces(matrix, rhs):
    faces = []
    active = [0]
    while True:
        vector = face_vector(matrix, rhs, active)
        residual = add(matvec(matrix, vector), rhs, F(-1))
        faces.append((list(active), vector, residual))
        negative = [i for i in range(len(rhs)) if i not in active and residual[i] < 0]
        if not negative:
            return faces
        active.extend(negative)
        active.sort()


def main():
    mu = F(1, 5)
    perturbation_patterns = (
        lambda i: F(i + 1),
        lambda i: -F(i + 1),
        lambda i: F(i + 1) if i % 2 else -F(i + 1),
    )
    pivot_cases = 0
    stop_cases = 0
    checked_cases = 0
    telescope_cases = 0
    largest_gap_ratio = F(0)

    for n in range(4, 13):
        matrix = path_matrix(n)
        for rho in (F(1, 1000), F(1, 50), F(1, 20), F(1, 10)):
            rhs = [F(1, 5) - rho] + [-rho for _ in range(n - 1)]
            faces = reachable_faces(matrix, rhs)
            optimum = faces[-1][1]
            optimum_support = {i for i, value in enumerate(optimum) if value > 0}
            energy_motion = F(0)
            slack_motion = F(0)
            for old, new in zip(faces, faces[1:]):
                displacement = add(new[1], old[1], F(-1))
                slack_displacement = matvec(matrix, displacement)
                energy_motion += dot(displacement, slack_displacement)
                slack_motion += dot(slack_displacement, slack_displacement)
            assert energy_motion == 2 * (
                objective(matrix, rhs, faces[0][1]) - objective(matrix, rhs, faces[-1][1])
            )
            assert slack_motion <= energy_motion
            telescope_cases += 1
            for active, exact_face, exact_slack in faces:
                boundary = [
                    i for i in range(n) if i not in active and any(matrix[i][j] < 0 for j in active)
                ]
                assert len(boundary) <= 1
                for tau in (F(1, 200), F(1, 50), F(1, 10)):
                    eps_obj = tau * tau / (2 * mu)
                    for pattern in perturbation_patterns:
                        scale = F(1, 10)
                        while True:
                            trial = list(exact_face)
                            for local_index, index in enumerate(active):
                                trial[index] += scale * pattern(local_index)
                            face_residual = [
                                value
                                for index, value in enumerate(
                                    add(matvec(matrix, trial), rhs, F(-1))
                                )
                                if index in active
                            ]
                            certified_error = (
                                sum((abs(value) for value in face_residual), F(0)) / mu
                            )
                            multiplier = 5 if boundary else 1
                            if multiplier * certified_error <= tau:
                                break
                            scale /= 2

                        approximate_slack = add(matvec(matrix, trial), rhs, F(-1))
                        # The exact rational intervals
                        # [hat_w-E/2, hat_w+E/2] have width E<2E and contain
                        # every approximate key.  E also upper-bounds the
                        # exact-face solution/slack error because
                        # ||r||_2/mu <= ||r||_1/mu = E.
                        certified = [
                            index
                            for index in boundary
                            if approximate_slack[index] + certified_error / 2 < -certified_error
                        ]
                        checked_cases += 1
                        if certified:
                            pivot_cases += 1
                            for index in certified:
                                assert exact_slack[index] < 0
                                assert index in optimum_support
                        else:
                            stop_cases += 1
                            feasible = [max(value, F(0)) for value in trial]
                            gap = objective(matrix, rhs, feasible) - objective(matrix, rhs, optimum)
                            assert gap <= eps_obj
                            largest_gap_ratio = max(largest_gap_ratio, gap / eps_obj)

    assert pivot_cases > 0
    assert stop_cases > 0
    print("matrix family: tridiagonal Stieltjes, (1/5)I <= Q <= I")
    print(f"exact cases checked: {checked_cases}")
    print(f"certified safe-pivot branches: {pivot_cases}")
    print(f"certified objective-stop branches: {stop_cases}")
    print(f"exact energy/slack telescopes checked: {telescope_cases}")
    print(f"largest exact gap/eps_obj on a stop branch: {largest_gap_ratio}")
    print(
        "verdict: every threshold report was support-safe; every no-report projection met the objective target."
    )


if __name__ == "__main__":
    main()
