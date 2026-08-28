#!/usr/bin/env python3
"""Exact audit of separated RPPR coordinate-level certificates."""

from fractions import Fraction as F
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "manuscript/notes/aesp_cd_l1_rppr/sections/body/06_lem_aesp_cd_kkt_error.tex"


def solve(a, b):
    n = len(b)
    aug = [list(a[i]) + [b[i]] for i in range(n)]
    for j in range(n):
        k = next(i for i in range(j, n) if aug[i][j])
        aug[j], aug[k] = aug[k], aug[j]
        pivot = aug[j][j]
        aug[j] = [x / pivot for x in aug[j]]
        for i in range(n):
            if i == j or not aug[i][j]:
                continue
            pivot = aug[i][j]
            aug[i] = [x - pivot * y for x, y in zip(aug[i], aug[j])]
    return [row[-1] for row in aug]


def edge(adj, u, v):
    if v not in adj[u]:
        adj[u].append(v)
        adj[v].append(u)


def random_graph(n, rng):
    """Seeded connected unweighted graph, with extra cyclic edges."""
    adj = [[] for _ in range(n)]
    for v in range(1, n):
        edge(adj, v, rng.randrange(v))
    for u in range(n):
        for v in range(u + 1, n):
            if rng.randrange(5) == 0:
                edge(adj, u, v)
    return adj


def rppr(adj, alpha, rho):
    n = len(adj)
    degree = [len(row) for row in adj]
    diagonal, coupling = (1 + alpha) / 2, (1 - alpha) / 2
    h = [[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        h[i][i] = diagonal * degree[i]
        for j in adj[i]:
            h[i][j] = -coupling
    ell = [
        alpha * ((1 if i == 0 else 0) - rho * degree[i])
        for i in range(n)
    ]
    return degree, coupling, h, ell


def restricted(h, ell, active):
    ids = sorted(active)
    val = solve(
        [[h[i][j] for j in ids] for i in ids],
        [ell[i] for i in ids],
    )
    return dict(zip(ids, val))


def boundary(adj, active):
    return sorted({v for u in active for v in adj[u] if v not in active})


def trace(adj, h, ell):
    """Exact nested-face trace, admitting the least positive boundary id."""
    active = {0}
    out = []
    for _ in range(len(adj) + 1):
        y = restricted(h, ell, active)
        assert all(value > 0 for value in y.values())
        frontier = boundary(adj, active)
        out.append((set(active), y, frontier))
        x = [y.get(i, F(0)) for i in range(len(adj))]
        keys = {
            v: ell[v] - sum(h[v][j] * x[j] for j in range(len(adj)))
            for v in frontier
        }
        positive = [v for v in frontier if keys[v] > 0]
        if not positive:
            break
        active.add(min(positive))
    else:
        raise AssertionError("nested trace did not terminate")
    return out


def round_down(value, delta, epsilon):
    if value < delta:
        return F(0)
    level = delta
    while level * (1 + epsilon) <= value:
        level *= 1 + epsilon
    return level


def rounded_state(y, alpha, rho, coupling, gamma):
    epsilon = gamma / 8
    delta = gamma * alpha * rho / (8 * coupling)
    return {
        i: round_down(value, delta, epsilon)
        for i, value in y.items()
    }


def audit_row(
    adj,
    degree,
    alpha,
    rho,
    coupling,
    active,
    y,
    v,
    gamma,
    rounded=None,
):
    epsilon = gamma / 8
    delta = gamma * alpha * rho / (8 * coupling)
    if rounded is None:
        rounded = rounded_state(y, alpha, rho, coupling, gamma)
    response = coupling * sum(
        y.get(i, F(0)) for i in adj[v] if i in active
    )
    rounded_response = coupling * sum(
        rounded.get(i, F(0)) for i in adj[v] if i in active
    )
    threshold = alpha * rho * degree[v]
    upper = (
        (1 + epsilon) * rounded_response
        + coupling * degree[v] * delta
    )
    assert rounded_response <= response <= upper

    negative = response <= (1 - gamma) * threshold
    positive = response >= (1 + gamma) * threshold
    if negative:
        assert upper < threshold and response - threshold < 0
    if positive:
        assert rounded_response > threshold and response - threshold > 0
    return negative, positive, rounded_response, upper, threshold


def main():
    source = SOURCE.read_text()
    assert r"\label{prop:aesp-cd-separated-level-reporter}" in source
    assert r"\epsilon=\gamma/8" in source
    assert r"\delta=\gamma\alpha\rho/(8c)" in source

    rng = random.Random(20260829)
    graphs = [
        random_graph(n, rng)
        for n in range(5, 9)
        for _ in range(2)
    ]
    params = [
        (F(1, 5), F(1, 80)),
        (F(1, 5), F(1, 24)),
        (F(1, 3), F(1, 60)),
        (F(1, 9), F(1, 100)),
    ]
    gammas = (F(1), F(1, 2), F(1, 4), F(1, 8))
    rows = separated = negative = positive = checkpoints = 0

    for adj in graphs:
        for alpha, rho in params:
            degree, coupling, h, ell = rppr(adj, alpha, rho)
            if ell[0] <= 0:
                continue
            previous = None
            for active, y, frontier in trace(adj, h, ell):
                assert all(
                    F(0) <= value <= F(1, degree[i])
                    for i, value in y.items()
                )
                if previous is not None:
                    assert all(y[i] >= previous[i] for i in previous)
                previous = y

                for gamma in gammas:
                    rounded = rounded_state(
                        y, alpha, rho, coupling, gamma
                    )
                    verdicts = [
                        audit_row(
                            adj,
                            degree,
                            alpha,
                            rho,
                            coupling,
                            active,
                            y,
                            v,
                            gamma,
                            rounded,
                        )
                        for v in frontier
                    ]
                    rows += len(verdicts)
                    if verdicts and all(n or p for n, p, *_ in verdicts):
                        checkpoints += 1
                    for negative_flag, positive_flag, *_ in verdicts:
                        if negative_flag or positive_flag:
                            separated += 1
                            negative += negative_flag
                            positive += positive_flag

    # At b=0 (alpha=1), every nonseed sign is the static -rho*d_v.
    adj = random_graph(8, rng)
    degree, coupling, h, ell = rppr(adj, F(1), F(1, 20))
    assert coupling == 0
    for _, _, frontier in trace(adj, h, ell):
        assert all(
            ell[v] == -F(1, 20) * degree[v] < 0
            for v in frontier
        )

    # Near-margin STOP: on P2 with alpha=1/5 and rho=b=2/5, the
    # boundary response equals its threshold. Separation fails, and the
    # rounded enclosure correctly straddles the threshold.
    adj = [[1], [0]]
    alpha, rho, gamma = F(1, 5), F(2, 5), F(1, 4)
    degree, coupling, h, ell = rppr(adj, alpha, rho)
    active, y, frontier = trace(adj, h, ell)[0]
    result = audit_row(
        adj,
        degree,
        alpha,
        rho,
        coupling,
        active,
        y,
        frontier[0],
        gamma,
    )
    negative_flag, positive_flag, rounded_response, upper, threshold = result
    assert not negative_flag and not positive_flag
    assert rounded_response < threshold <= upper

    # A coarse-bin STOP on an actual RPPR path w-o-v-z.  The source value
    # stays in the dyadic bin [1/4,1/2), while v changes from a negative to a
    # positive key.  The theorem's gamma-scaled fine levels do register the
    # crossing and certify both signs.
    adj = [[1, 2], [0], [0, 3], [2]]
    alpha, rho = F(1, 2), F(13, 180)
    degree, coupling, h, ell = rppr(adj, alpha, rho)
    before_active, after_active = {0}, {0, 1}
    before = restricted(h, ell, before_active)
    after = restricted(h, ell, after_active)
    assert before[0] == F(77, 270)
    assert after[0] == F(449, 1530)
    assert F(1, 4) <= before[0] < after[0] < F(1, 2)
    before_key = ell[2] - sum(h[2][i] * before[i] for i in before_active)
    after_key = ell[2] - sum(h[2][i] * after[i] for i in after_active)
    assert before_key == -F(1, 1080)
    assert after_key == F(7, 6120)
    gamma = F(1, 100)
    before_rounded = rounded_state(before, alpha, rho, coupling, gamma)
    after_rounded = rounded_state(after, alpha, rho, coupling, gamma)
    assert before_rounded[0] != after_rounded[0]
    assert audit_row(
        adj,
        degree,
        alpha,
        rho,
        coupling,
        before_active,
        before,
        2,
        gamma,
        before_rounded,
    )[0]
    assert audit_row(
        adj,
        degree,
        alpha,
        rho,
        coupling,
        after_active,
        after,
        2,
        gamma,
        after_rounded,
    )[1]

    assert checkpoints > 50
    assert separated > 500 and negative and positive
    print(
        "PASS separated-level reporter exact audit:",
        f"rows={rows}, separated={separated},",
        f"all-separated checkpoints={checkpoints},",
        f"negative={negative}, positive={positive},",
        "c=0 static, near-margin=STOP, coarse-bin RPPR STOP",
    )


if __name__ == "__main__":
    main()
