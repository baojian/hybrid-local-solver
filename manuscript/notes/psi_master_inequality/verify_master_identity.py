#!/usr/bin/env python3
"""Exact-rational audit of Lemma lem:psi-master-identity.

The audit is independent of the Fable scripts.  It constructs the scaled
PageRank resolvent directly, samples deterministic rational points in the full
algebraic cap domain, and compares the Lyapunov difference with Psi using only
fractions.Fraction arithmetic.
"""

from fractions import Fraction as F
import json


def inverse(matrix):
    n = len(matrix)
    aug = [row[:] + [F(int(i == j)) for j in range(n)] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next(row for row in range(col, n) if aug[row][col])
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [entry / scale for entry in aug[col]]
        for row in range(n):
            if row == col or not aug[row][col]:
                continue
            scale = aug[row][col]
            aug[row] = [aug[row][j] - scale * aug[col][j] for j in range(2 * n)]
    return [row[n:] for row in aug]


def matvec(matrix, vector):
    return [sum((entry * vector[j] for j, entry in enumerate(row)), F(0)) for row in matrix]


def cycle(n):
    return [{(i - 1) % n, (i + 1) % n} for i in range(n)]


def complete_bipartite(a, b):
    return [set(range(a, a + b)) for _ in range(a)] + [set(range(a)) for _ in range(b)]


def build(adj, q):
    n = len(adj)
    degree = [F(len(row)) for row in adj]
    alpha = q * q / (1 + q * q)
    kappa = 1 - 2 * alpha
    beta = (1 - q) / (1 + q)
    nu = q / (1 + q)
    qt = [[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        qt[i][i] = (1 + alpha) * degree[i] / 2
        for j in adj[i]:
            qt[i][j] = -(1 - alpha) / 2
    shifted = [
        [qt[i][j] + (kappa * degree[i] if i == j else 0) for j in range(n)] for i in range(n)
    ]
    shifted_inv = inverse(shifted)
    resolvent = [[kappa * shifted_inv[i][j] * degree[j] for j in range(n)] for i in range(n)]
    return degree, resolvent, beta, nu, 1 - q * q


def dot_d(degree, left, right):
    return sum((degree[i] * left[i] * right[i] for i in range(len(degree))), F(0))


def project(degree, vector):
    mean = dot_d(degree, [F(1)] * len(degree), vector) / sum(degree)
    return [entry - mean for entry in vector]


def add(*vectors):
    return [sum(entries, F(0)) for entries in zip(*vectors)]


def scale(c, vector):
    return [c * entry for entry in vector]


def lyapunov(degree, resolvent, beta, current, previous):
    m_previous = matvec(resolvent, previous)
    return (
        dot_d(degree, current, current)
        - (1 + beta) * dot_d(degree, current, m_previous)
        + beta * dot_d(degree, previous, m_previous)
    )


def audit_case(name, adj, q, trials=7):
    degree, resolvent, beta, nu, m0 = build(adj, q)
    n = len(adj)
    passed = 0
    for trial in range(trials):
        y = [F(((i + 2) * (trial + 3)) % 13 - 6, trial + 4) for i in range(n)]
        raw_h = [F(((i + 5) * (trial + 2)) % 17 - 8, trial + 5) for i in range(n)]
        h = project(degree, raw_h)
        z = project(degree, y)
        y_minus = [max(-entry, F(0)) for entry in y]
        w = project(degree, y_minus)
        bvec = add(z, scale(-nu, h))

        previous = add(h, scale(1 / beta, z))
        following = matvec(resolvent, add(h, scale(-1, z), scale(-1, w)))
        lhs = lyapunov(degree, resolvent, beta, following, h) - (1 - q) ** 2 * lyapunov(
            degree, resolvent, beta, h, previous
        )

        mbw = matvec(resolvent, add(bvec, w))
        mb = matvec(resolvent, bvec)
        mh = matvec(resolvent, h)
        m2h = matvec(resolvent, mh)
        gh = add(scale(m0, h), scale(-2, mh), m2h)
        psi = (
            dot_d(degree, mbw, mbw)
            - m0 * dot_d(degree, bvec, mb)
            - nu * nu * dot_d(degree, mh, mh)
            - beta * dot_d(degree, h, gh)
        )

        delta = max([F(0)] + [-entry for entry in y])
        displacement = [(entry + delta) / beta for entry in y]
        assert all(entry >= 0 for entry in displacement)
        assert all(y[i] == beta * displacement[i] - delta for i in range(n))
        assert lhs == psi, (name, trial, lhs, psi)
        passed += 1
    return {"case": name, "q": str(q), "trials": trials, "passed": passed}


def main():
    cases = [
        ("C5", cycle(5), F(1, 5)),
        ("K2,3", complete_bipartite(2, 3), F(1, 4)),
        ("K3,4", complete_bipartite(3, 4), F(2, 7)),
    ]
    results = [audit_case(name, adj, q) for name, adj, q in cases]
    payload = {
        "arithmetic": "fractions.Fraction",
        "identity": "V_next-(1-q)^2 V=Psi",
        "total_trials": sum(item["trials"] for item in results),
        "total_passed": sum(item["passed"] for item in results),
        "cases": results,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
