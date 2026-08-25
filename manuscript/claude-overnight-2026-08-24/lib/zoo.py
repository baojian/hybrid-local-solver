"""Adversarial graph zoo. All graphs: {node: sorted neighbor list}, 0..n-1."""
import random


def _sym(edges, n):
    adj = {u: set() for u in range(n)}
    for u, v in edges:
        if u != v:
            adj[u].add(v); adj[v].add(u)
    return {u: sorted(adj[u]) for u in range(n)}


def star(m, center_seed=True):
    """K_{1,m}: node 0 = center, 1..m leaves. Returns (adj, seed)."""
    edges = [(0, i) for i in range(1, m + 1)]
    return _sym(edges, m + 1), (0 if center_seed else 1)


def path(n, seed_end=True):
    edges = [(i, i + 1) for i in range(n - 1)]
    return _sym(edges, n), (0 if seed_end else n // 2)


def spider(k, L):
    """k arms of length L; node 0 = center (seed). Arm a vertex j:
    1 + a*L + j for j in 0..L-1."""
    edges = []
    for a in range(k):
        prev = 0
        for j in range(L):
            v = 1 + a * L + j
            edges.append((prev, v)); prev = v
    return _sym(edges, 1 + k * L), 0


def caterpillar(m, arm=1):
    """Branch caterpillar: backbone b_1..b_m (0..m-1), each with a pendant
    leaf (m..2m-1); seed at b_0. arm>1 extends the pendant to a path."""
    edges = [(i, i + 1) for i in range(m - 1)]
    nid = m
    for i in range(m):
        prev = i
        for _ in range(arm):
            edges.append((prev, nid)); prev = nid; nid += 1
    return _sym(edges, nid), 0


def theta_graph(l1, l2, l3):
    """Two hub nodes joined by three internally disjoint paths with l1,l2,l3
    internal vertices. Smallest 2-connected non-tree beyond a cycle."""
    edges = []
    nid = 2
    for L in (l1, l2, l3):
        prev = 0
        for _ in range(L):
            edges.append((prev, nid)); prev = nid; nid += 1
        edges.append((prev, 1))
    return _sym(edges, nid), 0


def cycle(n):
    edges = [(i, (i + 1) % n) for i in range(n)]
    return _sym(edges, n), 0


def double_cycle(t):
    """Two cycles of length 2t joined by a perfect matching (prism graph)."""
    n = 2 * t
    edges = [(i, (i + 1) % n) for i in range(n)]
    edges += [(i + n, (i + 1) % n + n) for i in range(n)]
    edges += [(i, i + n) for i in range(n)]
    return _sym(edges, 2 * n), 0


def complete(n):
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    return _sym(edges, n), 0


def decoy_hub(path_len, hub_deg):
    """Endpoint-seeded path with one high-degree hub hanging off the middle:
    the evolving_support_cg decoy pattern."""
    edges = [(i, i + 1) for i in range(path_len - 1)]
    mid = path_len // 2
    nid = path_len
    hub = nid; nid += 1
    edges.append((mid, hub))
    for _ in range(hub_deg - 1):
        edges.append((hub, nid)); nid += 1
    return _sym(edges, nid), 0


def binary_tree(depth):
    n = 2 ** (depth + 1) - 1
    edges = []
    for i in range(n):
        for c in (2 * i + 1, 2 * i + 2):
            if c < n:
                edges.append((i, c))
    return _sym(edges, n), 0


def random_regular(n, deg, seed_rng=17):
    rng = random.Random(seed_rng)
    while True:
        stubs = [v for v in range(n) for _ in range(deg)]
        rng.shuffle(stubs)
        edges = set()
        ok = True
        for i in range(0, len(stubs), 2):
            u, v = stubs[i], stubs[i + 1]
            if u == v or (min(u, v), max(u, v)) in edges:
                ok = False; break
            edges.add((min(u, v), max(u, v)))
        if ok:
            return _sym(list(edges), n), 0


def grid(w, h):
    def nid(x, y): return y * w + x
    edges = []
    for y in range(h):
        for x in range(w):
            if x + 1 < w: edges.append((nid(x, y), nid(x + 1, y)))
            if y + 1 < h: edges.append((nid(x, y), nid(x, y + 1)))
    return _sym(edges, w * h), 0
