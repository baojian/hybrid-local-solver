#!/usr/bin/env python3
"""Exact-rational hard-lift/source-reservoir counterexample.

Run with SymPy available, for example

    uv run --with sympy python green_lift_exact.py
"""

import sympy as sp


def main():
    alpha = sp.Rational(1, 10**6)
    root = sp.Rational(1, 1000)
    beta = sp.Rational(999, 1001)
    a = (1 + alpha) / 2
    c = (1 - alpha) / 2

    # The central tree plus private leaves has 39 vertices.  These are its
    # eight central degrees; the omitted leaves affect only the diagonal.
    degree = [5, 8, 4, 6, 7, 7, 5, 3]
    central_edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (4, 6), (5, 7)]
    old_face = list(range(7))
    new_face = list(range(8))

    def matrices(vertices):
        index = {v: i for i, v in enumerate(vertices)}
        adjacency = sp.zeros(len(vertices))
        for u, v in central_edges:
            if u in index and v in index:
                adjacency[index[u], index[v]] = 1
                adjacency[index[v], index[u]] = 1
        diagonal = sp.diag(*[degree[v] for v in vertices])
        hmat = a * diagonal - c * adjacency
        hard = 2 * root * diagonal + (1 - root) * hmat
        return diagonal, hmat, hard

    d_old, h_old, k_old = matrices(old_face)
    d_new, h_new, k_new = matrices(new_face)
    e_old = sp.zeros(7, 1)
    e_old[0] = 1
    e_new = sp.zeros(8, 1)
    e_new[0] = 1
    source_degree = degree[0]

    green_old = source_degree * h_old.inv() * e_old
    green_new = source_degree * h_new.inv() * e_new

    random_walk_q = d_old.inv() * h_old
    richardson = sp.eye(7) - random_walk_q
    previous = sp.zeros(7, 1)
    current = sp.zeros(7, 1)
    for _ in range(13):
        following = richardson * ((1 + beta) * current - beta * previous)
        following += e_old
        previous, current = current, following
    raw_error = green_old - current

    inverse_lift = k_new.inv()[:7, :7] - k_old.inv()
    lift = sp.factor((raw_error.T * d_old * inverse_lift * d_old * raw_error)[0] / source_degree)
    reservoir_old = sp.factor(
        (green_old.T * d_old * k_old.inv() * d_old * green_old)[0] / source_degree
    )
    reservoir_new = sp.factor(
        (green_new.T * d_new * k_new.inv() * d_new * green_new)[0] / source_degree
    )
    increment = sp.factor(reservoir_new - reservoir_old)
    difference = sp.factor(lift - increment)

    assert lift > 0 and increment > 0 and difference > 0
    assert lift / increment > sp.Rational(112, 100)
    print("lift =", sp.N(lift, 30))
    print("reservoir increment =", sp.N(increment, 30))
    print("ratio =", sp.N(lift / increment, 30))


if __name__ == "__main__":
    main()
