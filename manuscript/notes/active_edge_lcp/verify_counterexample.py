#!/usr/bin/env python3
"""Exact-arithmetic audit for the four-vertex face-CG counterexample."""

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


def fmt(vector):
    return "(" + ", ".join(str(value) for value in vector) + ")"


def main():
    # Graph edges: 01, 12, 13, 23.  In degree coordinates y=D^{-1/2}x,
    # H=D^{1/2}QD^{1/2}=(3/5)D-(2/5)A and h=D^{1/2}c.
    degree = [F(1), F(3), F(2), F(2)]
    h = [F(1, 5) * (F(1) - F(1, 1000) * degree[0])] + [
        -F(1, 5) * F(1, 1000) * value for value in degree[1:]
    ]
    adjacency = [
        [0, 1, 0, 0],
        [1, 0, 1, 1],
        [0, 1, 0, 1],
        [0, 1, 1, 0],
    ]
    H = [
        [F(3, 5) * degree[i] if i == j else -F(2, 5) * adjacency[i][j] for j in range(4)]
        for i in range(4)
    ]

    optimum = solve(H, h)
    old_face = solve([row[:3] for row in H[:3]], h[:3]) + [F(0)]
    assert optimum == [F(6983, 17000), F(1983, 17000), F(983, 17000), F(983, 17000)]
    assert old_face == [F(24953, 63000), F(1987, 21000), F(983, 31500), F(0)]
    assert all(value > 0 for value in optimum)

    # Original-x CG represented exactly in degree coordinates.  If
    # z=D^{1/2}r_x and ptilde=D^{1/2}p_x, then
    # y+=a D^{-1}ptilde and z-=a H D^{-1}ptilde.
    y = old_face
    z = add(h, matvec(H, y), F(-1))
    direction = list(z)
    expected_steps = [F(5, 3), F(225, 74), F(259, 120), F(150, 119)]
    expected_y = [
        [F(24953, 63000), F(1987, 21000), F(983, 31500), F(983, 23625)],
        [F(24953, 63000), F(259877, 2331000), F(65861, 1165500), F(10813, 194250)],
        [F(388057, 945000), F(4363, 37800), F(111079, 1890000), F(36371, 630000)],
        optimum,
    ]

    print("graph edges: 01, 12, 13, 23")
    print("degree:", fmt(degree))
    print("exact optimum y*:", fmt(optimum))
    print("exact old-face y0:", fmt(old_face))
    initial_error = add(old_face, optimum, F(-1))
    previous_energy = dot(initial_error, matvec(H, initial_error))
    directions = []
    for iteration in range(4):
        dinv_direction = [value / degree[i] for i, value in enumerate(direction)]
        numerator = dot(z, [value / degree[i] for i, value in enumerate(z)])
        denominator = dot(dinv_direction, matvec(H, dinv_direction))
        step = numerator / denominator
        assert step == expected_steps[iteration]
        y = add(y, dinv_direction, step)
        z_new = add(z, matvec(H, dinv_direction), -step)
        assert y == expected_y[iteration]
        assert all(value > 0 for value in y)

        error = add(y, optimum, F(-1))
        energy = dot(error, matvec(H, error))
        assert energy < previous_energy
        previous_energy = energy
        for old_direction in directions:
            old_dinv = [value / degree[i] for i, value in enumerate(old_direction)]
            assert dot(old_dinv, matvec(H, dinv_direction)) == 0
        directions.append(list(direction))

        signs = "".join("+" if value > 0 else "-" if value < 0 else "0" for value in z_new)
        print(f"iteration {iteration + 1}: a={step}; y={fmt(y)}; residual-signs={signs}")
        if iteration == 2:
            excess = y[2] - optimum[2]
            assert excess == F(30473, 32130000) > 0
            print("coordinate-2 overshoot:", excess)

        if not any(z_new):
            z = z_new
            break
        beta = dot(z_new, [value / degree[i] for i, value in enumerate(z_new)]) / numerator
        direction = add(z_new, direction, beta)
        z = z_new

    assert y == optimum
    assert not any(z)
    print("verdict: iteration 3 is feasible and energy-decreasing but not coordinatewise below y*.")


if __name__ == "__main__":
    main()
