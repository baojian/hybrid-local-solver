"""Exact check of the four-cycle MSE momentum witness."""

from fractions import Fraction as F


def matrix_vector(matrix, vector):
    return [
        sum((matrix[i][j] * vector[j] for j in range(len(vector))), F(0))
        for i in range(len(vector))
    ]


def add(left, right):
    return [x + y for x, y in zip(left, right)]


def subtract(left, right):
    return [x - y for x, y in zip(left, right)]


def scale(value, vector):
    return [value * x for x in vector]


def positive_part(vector):
    return [max(F(0), x) for x in vector]


def solve(matrix, rhs):
    """Gauss-Jordan elimination over the rational numbers."""
    n = len(rhs)
    augmented = [list(matrix[i]) + [rhs[i]] for i in range(n)]
    for column in range(n):
        pivot = next(i for i in range(column, n) if augmented[i][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        pivot_value = augmented[column][column]
        augmented[column] = [value / pivot_value for value in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            multiplier = augmented[row][column]
            augmented[row] = [
                augmented[row][j] - multiplier * augmented[column][j]
                for j in range(n + 1)
            ]
    return [augmented[i][-1] for i in range(n)]


alpha = F(1, 4)
rho = F(1, 10)
n = 4

# On the 2-regular four-cycle, scaling x by sqrt(2) makes both Q and h
# rational without changing any MSE momentum parameter.
Q = [[F(0) for _ in range(n)] for _ in range(n)]
for i in range(n):
    Q[i][i] = (1 + alpha) / 2
    Q[i][(i - 1) % n] -= (1 - alpha) / 4
    Q[i][(i + 1) % n] -= (1 - alpha) / 4

R = [[F(i == j) - Q[i][j] for j in range(n)] for i in range(n)]
h = [alpha * (F(i == 0) - 2 * rho) for i in range(n)]


def fixed_point_step(x):
    return positive_part(add(matrix_vector(R, x), h))


def maximal_extrapolation(previous, current):
    direction = subtract(current, previous)
    q_direction = matrix_vector(Q, direction)
    residual = subtract(h, matrix_vector(Q, current))
    ratios = [
        residual[i] / q_direction[i]
        for i in range(n)
        if current[i] > 0 and q_direction[i] > 0
    ]
    theta = min(ratios)
    extrapolated = add(current, scale(theta, direction))
    return theta, extrapolated, fixed_point_step(extrapolated)


x0 = [F(0)] * n
x1 = fixed_point_step(x0)
theta1, z1, x2 = maximal_extrapolation(x0, x1)
theta2, z2, x3 = maximal_extrapolation(x1, x2)

assert x1 == [F(1, 5), F(0), F(0), F(0)]
assert theta1 == F(3, 5)
assert z1 == [F(8, 25), F(0), F(0), F(0)]
assert x2 == [F(8, 25), F(1, 100), F(0), F(1, 100)]
assert theta2 == F(1, 19)
assert theta2 < F(1, 3)  # Strongly-convex Nesterov momentum at alpha=1/4.

active = [0, 1, 3]
restricted_q = [[Q[i][j] for j in active] for i in active]
restricted_h = [h[i] for i in active]
restricted_solution = solve(restricted_q, restricted_h)
x_star = [F(0)] * n
for index, value in zip(active, restricted_solution):
    x_star[index] = value

assert x_star == [F(68, 205), F(4, 205), F(0), F(4, 205)]
gradient = subtract(matrix_vector(Q, x_star), h)
assert all(gradient[i] == 0 for i in active)
assert gradient[2] == F(7, 164) > 0
assert all(x2[i] <= x_star[i] for i in range(n))
assert all(z2[i] <= x_star[i] for i in range(n))
assert all(x3[i] <= x_star[i] for i in range(n))

print("exact MSE small-momentum witness verified")
