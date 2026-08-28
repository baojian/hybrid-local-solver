#!/usr/bin/env python3
"""Exact audit of rooted-tree singleton threshold messages."""

from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "manuscript/notes/aesp_cd_l1_rppr/sections/body/06_lem_aesp_cd_kkt_error.tex"


def solve(a, b):
    """Exact dense Gaussian elimination, used only as the reference path."""
    n = len(b)
    if n == 0:
        return []
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
    adj[u].append(v)
    adj[v].append(u)


def path(n):
    adj = [[] for _ in range(n)]
    for i in range(n - 1):
        edge(adj, i, i + 1)
    return adj


def binary(depth):
    n = 2 ** (depth + 1) - 1
    adj = [[] for _ in range(n)]
    for u in range((n - 1) // 2):
        edge(adj, u, 2 * u + 1)
        edge(adj, u, 2 * u + 2)
    return adj


def spider(lengths):
    adj = [[]]
    for length in lengths:
        prev = 0
        for _ in range(length):
            adj.append([])
            edge(adj, prev, len(adj) - 1)
            prev = len(adj) - 1
    return adj


def broom(handle, leaves):
    adj = path(handle + 1)
    center = handle
    for _ in range(leaves):
        adj.append([])
        edge(adj, center, len(adj) - 1)
    return adj


def weighted_star(strict):
    """Unequal couplings with three exactly equal root thresholds."""
    adj = [[] for _ in range(4)]
    weights = [F(1, 3), F(2, 5), F(3, 7)]
    h = [[F(0) for _ in range(4)] for _ in range(4)]
    for v, weight in enumerate(weights, 1):
        edge(adj, 0, v)
        h[0][0] += weight
        h[v][v] += weight
        h[0][v] = h[v][0] = -weight
    grounds = (F(1, 2), F(2, 3), F(3, 4), F(4, 5))
    for i, ground in enumerate(grounds):
        h[i][i] += ground
    ell = [(2 if strict else 1) * h[0][0], *[-weight for weight in weights]]
    return adj, h, ell


def rooted(adj, root=0):
    parent = [None] * len(adj)
    order = [root]
    for u in order:
        for v in sorted(adj[u]):
            if v == parent[u]:
                continue
            assert parent[v] is None and v != root
            parent[v] = u
            order.append(v)
    assert len(order) == len(adj)
    children = [[] for _ in adj]
    for v in order[1:]:
        children[parent[v]].append(v)
    return parent, children, order


def rppr(adj, alpha, rho, root=0):
    n = len(adj)
    degree = [len(row) for row in adj]
    diagonal, coupling = (1 + alpha) / 2, (1 - alpha) / 2
    h = [[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        h[i][i] = diagonal * degree[i]
        for j in adj[i]:
            h[i][j] = -coupling
    ell = [
        alpha * ((1 if i == root else 0) - rho * degree[i])
        for i in range(n)
    ]
    return h, ell


def restricted(h, ell, active):
    ids = sorted(active)
    val = solve(
        [[h[i][j] for j in ids] for i in ids],
        [ell[i] for i in ids],
    )
    return dict(zip(ids, val))


def obstacle(h, ell):
    """Independent exact active-set solve on the full vertex set."""
    n = len(ell)
    active = {i for i in range(n) if ell[i] > 0}
    for _ in range(8 * n + 8):
        z = restricted(h, ell, active)
        bad = {i for i, value in z.items() if value <= 0}
        if bad:
            active -= bad
            continue
        x = [z.get(i, F(0)) for i in range(n)]
        key = [
            ell[i] - sum(h[i][j] * x[j] for j in range(n))
            for i in range(n)
        ]
        violations = {
            i for i in range(n) if i not in active and key[i] > 0
        }
        if not violations:
            return x
        active |= violations
    raise AssertionError("active set did not converge")


def boundary(children, active):
    return sorted(
        v for u in active for v in children[u] if v not in active
    )


def dense_conditioned(h, ell, active, root, value):
    """Dense reference solve on U with z_root fixed to value."""
    rest = sorted(set(active) - {root})
    out = {root: value}
    if rest:
        rhs = [ell[i] - h[i][root] * value for i in rest]
        val = solve([[h[i][j] for j in rest] for i in rest], rhs)
        out.update(zip(rest, val))
    return out


def dense_thresholds(h, ell, active, root, children):
    """Independently recover every boundary threshold from two dense solves."""
    z0 = dense_conditioned(h, ell, active, root, F(0))
    z1 = dense_conditioned(h, ell, active, root, F(1))
    rows = []
    for v in boundary(children, active):

        def key(z):
            return ell[v] - sum(h[v][u] * z[u] for u in active)

        at_zero, at_one = key(z0), key(z1)
        slope = at_one - at_zero
        assert slope > 0
        rows.append((-at_zero / slope, v))
    return sorted(rows)


def threshold_messages(h, ell, active, root, parent, children, order):
    """Literal bottom-up theorem recurrence, separate from dense references."""
    a, b, s, r, theta, label, tau = {}, {}, {}, {}, {}, {}, {}
    negative_b = []
    for u in reversed(order):
        if u not in active:
            continue
        a[u] = h[u][u] - sum(s[w] for w in children[u] if w in active)
        b[u] = ell[u] + sum(r[w] for w in children[u] if w in active)
        assert a[u] > 0
        if u != root and b[u] < 0:
            negative_b.append(u)

        candidates = []
        for w in children[u]:
            if w not in active:
                beta = -h[u][w]
                assert beta > 0
                candidates.append((-ell[w] / beta, w))
            elif label[w] is not None:
                candidates.append((tau[w], label[w]))
        if candidates:
            theta[u], label[u] = min(candidates)
        else:
            theta[u], label[u] = None, None

        if u != root:
            beta = -h[parent[u]][u]
            s[u] = beta * beta / a[u]
            r[u] = beta * b[u] / a[u]
            tau[u] = (
                None
                if label[u] is None
                else (a[u] * theta[u] - b[u]) / beta
            )
    return a, b, theta[root], label[root], negative_b


def audit(name, adj, h, ell, expected_equality=False):
    root = 0
    assert ell[root] > 0
    assert all(ell[i] <= 0 for i in range(1, len(ell)))
    parent, children, order = rooted(adj, root)
    active = {root}
    labels = []
    negative_seen = set()
    competitions = ties = 0
    equality = False

    for _ in range(len(adj) + 1):
        a, b, theta, label, negative = threshold_messages(
            h, ell, active, root, parent, children, order
        )
        negative_seen.update(negative)
        direct = restricted(h, ell, active)
        assert all(value > 0 for value in direct.values())
        assert direct[root] == b[root] / a[root]

        # Top-down message recovery must reproduce every dense coordinate.
        message_value = {root: direct[root]}
        for u in order[1:]:
            if u in active:
                beta = -h[parent[u]][u]
                message_value[u] = (
                    b[u] + beta * message_value[parent[u]]
                ) / a[u]
                assert message_value[u] == direct[u]

        rows = dense_thresholds(h, ell, active, root, children)
        if len(rows) > 1:
            competitions += 1
        if rows and sum(value == rows[0][0] for value, _ in rows) > 1:
            ties += 1
        if rows:
            assert (theta, label) == rows[0]
        else:
            assert theta is None and label is None

        root_value = direct[root]
        if label is not None and root_value > theta:
            x = [direct.get(i, F(0)) for i in range(len(adj))]
            selected_key = ell[label] - sum(
                h[label][j] * x[j] for j in range(len(adj))
            )
            assert selected_key > 0
            labels.append(label)
            active.add(label)
            continue

        if label is not None and root_value == theta:
            equality = True
        x = [direct.get(i, F(0)) for i in range(len(adj))]
        assert all(
            ell[v] - sum(h[v][j] * x[j] for j in range(len(adj))) <= 0
            for v in boundary(children, active)
        )
        break
    else:
        raise AssertionError("singleton trace did not terminate")

    xstar = obstacle(h, ell)
    support = {i for i, value in enumerate(xstar) if value > 0}
    assert active == support
    assert len(set(labels)) == len(labels)
    if expected_equality:
        assert equality
    return {
        "name": name,
        "support": len(support),
        "steps": len(labels),
        "negative_b": len(negative_seen),
        "competitions": competitions,
        "ties": ties,
        "equality": equality,
        "labels": labels,
    }


def main():
    source = SOURCE.read_text()
    assert r"\label{thm:aesp-cd-tree-singleton-threshold}" in source
    assert "valid singleton positive-subset trace" in source
    assert "canonical" in source and "all-violations batches" in source

    cases = []
    graphs = [
        ("P8", path(8)),
        ("T15", binary(3)),
        ("spider", spider([2, 3, 4])),
        ("broom", broom(3, 5)),
    ]
    params = [
        (F(1, 5), F(1, 40)),
        (F(1, 5), F(1, 12)),
        (F(1, 3), F(1, 24)),
        (F(1, 9), F(1, 60)),
        (F(1, 5), F(1, 1000)),
    ]
    for graph_name, adj in graphs:
        for alpha, rho in params:
            h, ell = rppr(adj, alpha, rho)
            cases.append(
                audit(f"{graph_name}:a={alpha}:r={rho}", adj, h, ell)
            )

    # An exact-zero P8 boundary key must remain inactive.
    adj = path(8)
    h, ell = rppr(adj, F(1, 5), F(1, 4))
    zero = audit("P8-exact-zero", adj, h, ell, expected_equality=True)
    cases.append(zero)

    # Generic unequal edge weights test beta propagation independently of the
    # RPPR specialization. The first star thresholds tie exactly at one.
    adj, h, ell = weighted_star(strict=False)
    generic_zero = audit(
        "weighted-star-exact-tie-zero",
        adj,
        h,
        ell,
        expected_equality=True,
    )
    cases.append(generic_zero)
    adj, h, ell = weighted_star(strict=True)
    generic_strict = audit("weighted-star-strict-tie", adj, h, ell)
    cases.append(generic_strict)

    assert any(row["negative_b"] for row in cases)
    assert any(row["competitions"] for row in cases)
    assert any(row["ties"] for row in cases)
    assert zero["support"] == 1 and zero["steps"] == 0
    assert generic_zero["support"] == 1 and generic_zero["steps"] == 0
    assert generic_strict["support"] == 4
    assert generic_strict["labels"] == [1, 2, 3]
    print(
        "PASS rooted-tree singleton threshold messages:",
        f"cases={len(cases)}, admissions={sum(x['steps'] for x in cases)},",
        f"negative-B nodes={sum(x['negative_b'] for x in cases)},",
        f"competition states={sum(x['competitions'] for x in cases)},",
        f"tie states={sum(x['ties'] for x in cases)}, exact-zero=inactive",
    )


if __name__ == "__main__":
    main()
