#!/usr/bin/env python3
"""Exact audit of the closed K_{a,b} resolvent and (HK-N) formulas."""

from fractions import Fraction as F
import json

from verify_master_identity import inverse


def matmul(left, right):
    return [[sum((left[i][k] * right[k][j] for k in range(len(right))), F(0))
             for j in range(len(right[0]))] for i in range(len(left))]


def direct_n(a, b):
    n = a + b
    degree = [F(b)] * a + [F(a)] * b
    matrix = [[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        matrix[i][i] = 3 * degree[i]
    for i in range(a):
        for j in range(a, n):
            matrix[i][j] = matrix[j][i] = -1
    matrix_inv = inverse(matrix)
    return [[matrix_inv[i][j] * degree[j] for j in range(n)]
            for i in range(n)], degree


def closed_n(a, b):
    n = a + b
    result = [[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(a):
        for j in range(a):
            result[i][j] = F(int(i == j), 3) + F(1, 24 * a)
        for j in range(a, n):
            result[i][j] = F(1, 8 * b)
    for i in range(a, n):
        for j in range(a):
            result[i][j] = F(1, 8 * a)
        for j in range(a, n):
            result[i][j] = F(int(i == j), 3) + F(1, 24 * b)
    return result


def predicted_n2_offdiag(a, b, i, j):
    if i < a and j < a:
        return F(13, 288 * a)
    if i >= a and j >= a:
        return F(13, 288 * b)
    if i < a and j >= a:
        return F(3, 32 * b)
    return F(3, 32 * a)


def main():
    graph_count = 0
    offdiag_count = 0
    max_ratio = F(0)
    maximizers = []
    for a in range(1, 9):
        for b in range(1, 9):
            direct, degree = direct_n(a, b)
            closed = closed_n(a, b)
            assert direct == closed, (a, b, "N")
            square = matmul(direct, direct)
            volume = sum(degree)
            for i in range(a + b):
                for j in range(a + b):
                    if i == j:
                        continue
                    assert square[i][j] == predicted_n2_offdiag(a, b, i, j)
                    ratio = 4 * volume * square[i][j] / degree[j]
                    assert ratio in (F(13, 36), F(3, 4))
                    if ratio > max_ratio:
                        max_ratio = ratio
                        maximizers = [[a, b, i, j]]
                    elif ratio == max_ratio:
                        maximizers.append([a, b, i, j])
                    offdiag_count += 1
            graph_count += 1
    payload = {
        "arithmetic": "fractions.Fraction",
        "family": "K_{a,b}, 1<=a,b<=8",
        "graphs_passed": graph_count,
        "offdiagonal_formulas_passed": offdiag_count,
        "within_part_hk_ratio": "13/36",
        "cross_part_hk_ratio": "3/4",
        "maximum_hk_ratio": str(max_ratio),
        "number_of_maximizing_ordered_pairs": len(maximizers),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
