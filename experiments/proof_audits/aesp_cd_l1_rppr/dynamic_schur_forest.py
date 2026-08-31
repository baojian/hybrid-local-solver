#!/usr/bin/env python3
"""Exact audit of pinned/free Schur messages on a small forest.

The message calculation is deliberately independent of the dense Fraction
reference solve. A deterministic toggle/query trace compares the two after
every update and checks the positive-unpin monotonicity statement.
"""

from fractions import Fraction as F
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "manuscript/notes/aesp_cd_l1_rppr/sections/body/06_lem_aesp_cd_kkt_error.tex"


def solve(a, b):
    """Exact dense Gaussian elimination."""
    n = len(b)
    aug = [list(a[i]) + [b[i]] for i in range(n)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if aug[i][j])
        aug[j], aug[pivot] = aug[pivot], aug[j]
        z = aug[j][j]
        aug[j] = [x / z for x in aug[j]]
        for i in range(n):
            if i == j or not aug[i][j]:
                continue
            z = aug[i][j]
            aug[i] = [x - z * y for x, y in zip(aug[i], aug[j])]
    return [aug[i][-1] for i in range(n)]


def restricted_solution(h, b, free):
    free = sorted(free)
    out = [F(0) for _ in b]
    if not free:
        return out
    sub = [[h[i][j] for j in free] for i in free]
    val = solve(sub, [b[i] for i in free])
    for i, z in zip(free, val):
        out[i] = z
    return out


def dense_marginal(h, b, free, v):
    """Marginal for a pinned v after eliminating the current free set."""
    free = sorted(free)
    if not free:
        return h[v][v], b[v]
    sub = [[h[i][j] for j in free] for i in free]
    hv = [h[i][v] for i in free]
    hb = solve(sub, hv)
    xb = solve(sub, [b[i] for i in free])
    sigma = h[v][v] - sum(h[v][i] * z for i, z in zip(free, hb))
    delta = b[v] - sum(h[v][i] * z for i, z in zip(free, xb))
    return sigma, delta


def tree_summary(adj, h, b, allowed, root):
    """Eliminate an allowed tree component toward root via scalar messages."""
    allowed = set(allowed)

    def rec(u, parent):
        au, ell = h[u][u], b[u]
        for w in adj[u]:
            if w == parent or w not in allowed:
                continue
            aw, ew = rec(w, u)
            edge = h[u][w]
            au -= edge * edge / aw
            ell -= edge * ew / aw
        assert au > 0
        return au, ell

    return rec(root, None)


def oracle_marginal(adj, h, b, free, v):
    allowed = set(free) | {v}
    return tree_summary(adj, h, b, allowed, v)


def objective(h, b, x):
    return sum(
        x[i] * h[i][j] * x[j]
        for i in range(len(x))
        for j in range(len(x))
    ) / 2 - sum(bi * xi for bi, xi in zip(b, x))


def fixed_value(h, b, free, v, t):
    free = sorted(free)
    x = [F(0) for _ in b]
    x[v] = t
    if free:
        sub = [[h[i][j] for j in free] for i in free]
        rhs = [b[i] - h[i][v] * t for i in free]
        for i, z in zip(free, solve(sub, rhs)):
            x[i] = z
    return objective(h, b, x)


def build_instance():
    # Two forest components; rational edge weights and positive grounding make
    # H a strictly SPD Stieltjes matrix.
    edges = [
        (0, 1, F(1, 2)),
        (1, 2, F(2, 3)),
        (1, 3, F(3, 5)),
        (3, 4, F(4, 7)),
        (5, 6, F(5, 8)),
        (6, 7, F(3, 4)),
        (6, 8, F(2, 5)),
        (8, 9, F(7, 9)),
    ]
    n = 10
    adj = [[] for _ in range(n)]
    h = [[F(0) for _ in range(n)] for _ in range(n)]
    ground = [
        F(1, 3), F(2, 5), F(3, 7), F(1, 2), F(4, 9),
        F(2, 7), F(5, 11), F(3, 8), F(4, 13), F(5, 12),
    ]
    for i, z in enumerate(ground):
        h[i][i] += z
    for u, v, w in edges:
        adj[u].append(v)
        adj[v].append(u)
        h[u][u] += w
        h[v][v] += w
        h[u][v] -= w
        h[v][u] -= w
    # Positive b maximally exercises the monotone positive-unpin conclusion.
    b = [F(k, 7 + (k % 3)) for k in (2, 3, 5, 4, 7, 6, 8, 3, 9, 5)]
    return adj, h, b


def connected_to(adj, v, allowed):
    seen, stack = set(), [v]
    while stack:
        u = stack.pop()
        if u in seen or u not in allowed:
            continue
        seen.add(u)
        stack.extend(adj[u])
    return seen


def audit_state(adj, h, b, free):
    ref = restricted_solution(h, b, free)
    pins = set(range(len(b))) - set(free)
    checked = 0
    for v in sorted(pins):
        sigma, delta = dense_marginal(h, b, free, v)
        smsg, dmsg = oracle_marginal(adj, h, b, free, v)
        assert (smsg, dmsg) == (sigma, delta)
        assert sigma > 0
        # Three exact samples verify the scalar marginal polynomial.
        c0 = fixed_value(h, b, free, v, F(0))
        for t in (F(-2, 3), F(1, 2), F(5, 4)):
            got = fixed_value(h, b, free, v, t)
            assert got == c0 + sigma * t * t / 2 - delta * t
        if delta > 0:
            new = restricted_solution(h, b, set(free) | {v})
            assert new[v] == delta / sigma > 0
            reached = connected_to(adj, v, set(free) | {v})
            for i in free:
                assert new[i] >= ref[i]
                if i in reached:
                    assert new[i] > ref[i]
                else:
                    assert new[i] == ref[i]
        checked += 1
    return checked


def main():
    text = SOURCE.read_text()
    assert r"\label{prop:aesp-cd-dynamic-schur-forest}" in text
    assert "The explicit $Q$ term is essential" in text

    adj, h, b = build_instance()
    free = {0, 2, 5, 7}
    rng = random.Random(20260829)
    queries = audit_state(adj, h, b, free)
    toggles = 0
    # Every mark update is followed by fresh exact comparisons of all named
    # pinned queries.
    for _ in range(32):
        if len(free) == len(b) or (free and rng.random() < 0.4):
            v = rng.choice(sorted(free))
            free.remove(v)
        else:
            v = rng.choice(sorted(set(range(len(b))) - free))
            free.add(v)
        toggles += 1
        queries += audit_state(adj, h, b, free)

    print(
        "PASS dynamic Schur forest exact audit:",
        f"vertices={len(b)}, toggles={toggles}, pinned_queries={queries}",
    )


if __name__ == "__main__":
    main()
