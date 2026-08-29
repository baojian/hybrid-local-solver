#!/usr/bin/env python3
"""Exact audit of append-only LDL continuation on endpoint-seeded paths."""

from fractions import Fraction as F


def matvec(matrix, vector):
    return [sum((a * b for a, b in zip(row, vector)), F(0)) for row in matrix]


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


def path_instance(n, alpha, rho):
    degree = [F(1)] + [F(2) for _ in range(n - 2)] + [F(1)]
    beta = (F(1) - alpha) / 2
    matrix = [[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        matrix[i][i] = (F(1) + alpha) * degree[i] / 2
        if i:
            matrix[i][i - 1] = matrix[i - 1][i] = -beta
    rhs = [alpha * (F(1) - rho * degree[0])] + [-alpha * rho * degree[i] for i in range(1, n)]
    return degree, beta, matrix, rhs


def append_only_solve(degree, beta, matrix, rhs):
    pivots = []
    multipliers = [F(0)]
    forward_rhs = []
    active_size = 0
    while active_size < len(rhs):
        i = active_size
        if i == 0:
            pivots.append(matrix[0][0])
            forward_rhs.append(rhs[0])
        else:
            multiplier = -beta / pivots[-1]
            multipliers.append(multiplier)
            pivots.append(matrix[i][i] - multiplier * multiplier * pivots[-1])
            forward_rhs.append(rhs[i] - multiplier * forward_rhs[-1])
        assert pivots[-1] > 0
        active_size += 1

        direct = solve(
            [row[:active_size] for row in matrix[:active_size]],
            rhs[:active_size],
        )
        endpoint_value = forward_rhs[-1] / pivots[-1]
        assert endpoint_value == direct[-1]
        assert all(value > 0 for value in direct)

        if active_size == len(rhs):
            break
        outside_slack = -beta * endpoint_value - rhs[active_size]
        if outside_slack >= 0:
            break

    solution = [F(0) for _ in range(active_size)]
    solution[-1] = forward_rhs[-1] / pivots[-1]
    for i in range(active_size - 2, -1, -1):
        solution[i] = forward_rhs[i] / pivots[i] - multipliers[i + 1] * solution[i + 1]
    return solution


def main():
    cases = 0
    total_active_volume = 0
    maximum_active_size = 0
    for n in range(2, 31):
        for alpha in (F(1, 20), F(1, 5), F(1, 2), F(4, 5)):
            for rho in (F(1, 10**12), F(1, 1000), F(1, 50), F(1, 5), F(4, 5)):
                degree, beta, matrix, rhs = path_instance(n, alpha, rho)
                active_solution = append_only_solve(degree, beta, matrix, rhs)
                full_solution = active_solution + [F(0) for _ in range(n - len(active_solution))]
                slack = [
                    value - target for value, target in zip(matvec(matrix, full_solution), rhs)
                ]
                assert all(value > 0 for value in active_solution)
                assert all(value == 0 for value in slack[: len(active_solution)])
                assert all(value >= 0 for value in slack[len(active_solution) :])
                direct = solve(
                    [row[: len(active_solution)] for row in matrix[: len(active_solution)]],
                    rhs[: len(active_solution)],
                )
                assert direct == active_solution
                cases += 1
                maximum_active_size = max(maximum_active_size, len(active_solution))
                total_active_volume += sum(degree[: len(active_solution)])

    print("graph family: unit-weight endpoint-seeded paths")
    print(f"exact parameter instances checked: {cases}")
    print(f"maximum terminal support size: {maximum_active_size}")
    print(f"aggregate terminal active volume across audit: {total_active_volume}")
    print(
        "verdict: append-only LDL endpoint tests and one final back substitution match every direct face solve."
    )


if __name__ == "__main__":
    main()
