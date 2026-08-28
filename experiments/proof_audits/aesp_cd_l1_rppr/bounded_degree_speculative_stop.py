#!/usr/bin/env python3
"""Exact bounded-degree speculative-envelope overshoot certificate."""

from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "manuscript/notes/aesp_cd_l1_rppr/sections/body/06_lem_aesp_cd_kkt_error.tex"


def solve(a, b):
    n = len(b)
    aug = [list(a[i]) + [b[i]] for i in range(n)]
    for j in range(n):
        k = next(i for i in range(j, n) if aug[i][j])
        aug[j], aug[k] = aug[k], aug[j]
        z = aug[j][j]
        aug[j] = [x / z for x in aug[j]]
        for i in range(n):
            if i == j or not aug[i][j]:
                continue
            z = aug[i][j]
            aug[i] = [x - z * y for x, y in zip(aug[i], aug[j])]
    return [row[-1] for row in aug]


def edge(adj, u, v):
    adj[u].append(v)
    adj[v].append(u)


def comb(k):
    """A k-vertex spine with one leaf at each internal spine vertex."""
    adj = [[] for _ in range(k)]
    for i in range(k - 1):
        edge(adj, i, i + 1)
    for i in range(1, k - 1):
        adj.append([])
        edge(adj, i, len(adj) - 1)
    return adj


def obstacle(h, c, universe):
    universe = sorted(universe)
    active = {i for i in universe if c[i] > 0}
    while True:
        ids = sorted(active)
        val = solve(
            [[h[i][j] for j in ids] for i in ids],
            [c[i] for i in ids],
        )
        neg = {i for i, z in zip(ids, val) if z <= 0}
        if neg:
            active -= neg
            continue
        x = [F(0) for _ in c]
        for i, z in zip(ids, val):
            x[i] = z
        key = [
            c[i] - sum(h[i][j] * x[j] for j in range(len(c)))
            for i in range(len(c))
        ]
        viol = {i for i in universe if i not in active and key[i] > 0}
        if not viol:
            return x, key
        active |= viol


def main():
    source = SOURCE.read_text()
    assert r"\label{prop:aesp-cd-speculative-envelope-doubling}" in source
    assert r"\label{thm:aesp-cd-hard-cap-dynamic-oracle}" in source

    adj = comb(8)
    n = len(adj)
    degree = [len(row) for row in adj]
    assert n == 14 and max(degree) == 3 and sum(degree) == 26

    q = F(1, 8)
    alpha = q * q / (1 + q * q)
    rho = F(1, 13)
    h = [[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        h[i][i] = (1 + alpha) * degree[i] / 2
        for j in adj[i]:
            h[i][j] = -(1 - alpha) / 2
    c = [
        alpha * ((1 if i == 0 else 0) - rho * degree[i])
        for i in range(n)
    ]

    envelopes = [
        {0},
        {0, 1},
        {0, 1, 2, 3},
        {0, 1, 2, 3, 4, 5, 6, 8},
        set(range(n)),
    ]
    anchors = [1, 2, 8, 9]
    volumes = [sum(degree[i] for i in u) for u in envelopes]
    assert volumes == [1, 4, 10, 20, 26]
    assert all(volumes[j + 1] >= 2 * volumes[j] for j in range(3))

    keys = []
    for u, anchor in zip(envelopes, anchors):
        _, key = obstacle(h, c, u)
        assert anchor not in u and any(anchor in adj[i] for i in u)
        assert key[anchor] > 0
        keys.append(key[anchor])

    xstar, final_key = obstacle(h, c, set(range(n)))
    support = {i for i, z in enumerate(xstar) if z > 0}
    assert support == {0, 1, 2, 8, 9}
    support_volume = sum(degree[i] for i in support)
    assert support_volume == 9
    assert all(z <= 0 for i, z in enumerate(final_key) if i not in support)
    assert F(sum(degree), support_volume) == F(26, 9)
    print(
        "PASS bounded-degree speculative stop:",
        "max_degree=3, envelope_volumes=1,4,10,20,26,",
        "support_volume=9, explored/support=26/9,",
        "anchor_keys=" + ",".join(str(z) for z in keys),
    )


if __name__ == "__main__":
    main()
