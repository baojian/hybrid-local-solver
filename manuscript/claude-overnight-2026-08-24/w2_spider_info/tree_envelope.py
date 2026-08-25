"""I2-E, part 4: does interval-envelope estimation extend to trees?

MONOTONE SCALAR-LOAD LEMMA (the whole extension rests on this).
Root the tree at the seed v.  For a non-root vertex w with parent p put
R_w = u_w / u_p.  The balance equation d_w u_w = c(u_p + sum_{children x} u_x)
gives the continued fraction

    R_w = c / ( d_w - c * sum_{x child of w} R_x ),        R_root-eq:
    u_v = gamma / ( d_v - c * sum_{x child of v} R_x ),
    u_w = u_v * prod_{edges v->w} R.

R_w is INCREASING in every child's R_x, and u_v and every u_w are increasing
in every R.  A probe transcript fixes d and the child set at every scanned
vertex and leaves each FRONTIER vertex (id known, unscanned) with a completion
free.  Over completions,
    R_frontier in [ R_min(D), c ],
    R_max = c    : the frontier vertex is a leaf (pure reflection),
    R_min(D)     : infinite D-regular continuation, the root in (0,1) of
                   (D-1) c R^2 - D R + c = 0;  R_min = 0 if degrees unbounded.
Because everything is monotone in the R's, the coordinatewise MAXIMUM over all
consistent completions is attained at the single closure "every frontier = leaf"
and the MINIMUM at "every frontier = infinite D-regular tree".  Two closed-form
evaluations give exact per-coordinate intervals -- exactly as on spiders, with
psi(m) replaced by the subtree continued fraction.  D=2 recovers R_min = lambda.

CERTIFICATE.  Output midpoint at scanned vertices, 0 elsewhere.  Valid iff
  (T1) width(v) = u_v^max - u_v^min <= 2 eps  for every scanned v, and
  (T2) u_w^max <= eps for every frontier w
       (this also covers every unseen vertex below w, since u_x <= c*u_w^max).

STRATEGY.  Best-first: scan the frontier vertex of largest u^max.  This is the
adaptive uncertainty allocation the spider's round-robin specialises to.
"""
import sys, math, heapq
sys.path.insert(0, "/home/claude/work/overnight/w2_spider_info")
from formulas import lam_of_alpha, params


def R_min_of_D(c, D):
    if D <= 1:
        return 0.0
    if D == 2:
        return (1 - math.sqrt(1 - c * c)) / c
    a, b, cc = (D - 1) * c, -float(D), c
    return (-b - math.sqrt(b * b - 4 * a * cc)) / (2 * a)


class TreeOracle:
    """adj: dict id -> list of neighbour ids.  Root is `root`."""

    def __init__(self, adj, root=0):
        self.adj, self.root, self.scans = adj, root, 0

    def scan(self, v):
        self.scans += 1
        return list(self.adj[v])


def envelope(children, deg, frontier, root, c, gamma, Rlo, Rhi):
    """Post-order evaluation of (u^min, u^max) for every known vertex."""
    order, stack = [], [root]
    while stack:
        v = stack.pop()
        order.append(v)
        stack.extend(children[v])
    Rmin, Rmax = {}, {}
    for v in reversed(order):                       # leaves of the known tree up
        if v == root:
            continue
        if v in frontier:
            Rmin[v], Rmax[v] = Rlo, Rhi
        else:
            smin = sum(Rmin[x] for x in children[v])
            smax = sum(Rmax[x] for x in children[v])
            # R = c/(d - c*S): increasing in S  => min uses smin, max uses smax
            Rmin[v] = c / (deg[v] - c * smin)
            Rmax[v] = c / (deg[v] - c * smax)
    smin = sum(Rmin[x] for x in children[root])
    smax = sum(Rmax[x] for x in children[root])
    umin = {root: gamma / (deg[root] - c * smin)}
    umax = {root: gamma / (deg[root] - c * smax)}
    for v in order:
        for x in children[v]:
            umin[x] = umin[v] * Rmin[x]
            umax[x] = umax[v] * Rmax[x]
    return umin, umax


def estimate(adj, alpha, eps, D=None, root=0, cap=2_000_000):
    """Best-first interval-envelope estimator.  Returns (scans, umid, frontier)."""
    lam, s = lam_of_alpha(alpha)
    lam = float(lam)
    c, gamma = params(lam)
    Rhi = c
    Rlo = R_min_of_D(c, D) if D else 0.0
    orc = TreeOracle(adj, root)

    nb = orc.scan(root)
    deg = {root: len(nb)}
    children = {root: list(nb)}
    parent = {x: root for x in nb}
    frontier = set(nb)
    for x in nb:
        children[x] = []

    while orc.scans < cap:
        umin, umax = envelope(children, deg, frontier, root, c, gamma, Rlo, Rhi)
        bad = None
        best = eps
        for w in frontier:                          # (T2)
            if umax[w] > best:
                best, bad = umax[w], w
        if bad is None:                             # (T2) holds; check (T1)
            wide = [v for v in umin if v not in frontier
                    and umax[v] - umin[v] > 2 * eps]
            if not wide:
                mid = {v: (umin[v] + umax[v]) / 2 for v in umin
                       if v not in frontier}
                return orc.scans, mid, frontier, (umin, umax)
            bad = max(wide, key=lambda v: umax[v] - umin[v])
            # widening is driven by the frontier below `bad`: pick the heaviest
            cands = [w for w in frontier if umax[w] > 0]
            bad = max(cands, key=lambda w: umax[w]) if cands else None
            if bad is None:
                mid = {v: (umin[v] + umax[v]) / 2 for v in umin
                       if v not in frontier}
                return orc.scans, mid, frontier, (umin, umax)
        nb = orc.scan(bad)
        frontier.discard(bad)
        deg[bad] = len(nb)
        kids = [x for x in nb if x != parent[bad]]
        children[bad] = kids
        for x in kids:
            parent[x] = bad
            children[x] = []
            frontier.add(x)
    raise RuntimeError("cap exceeded")


# --------------------------- exact ground truth ---------------------------

def exact_u(adj, alpha, root=0):
    """u = pi/d for the lazy degree-scaled system (D - cA)u = gamma e_root."""
    ids = sorted(adj)
    idx = {v: i for i, v in enumerate(ids)}
    n = len(ids)
    c, gamma = params(float(lam_of_alpha(alpha)[0]))
    M = [[0.0] * n for _ in range(n)]
    b = [0.0] * n
    for v in ids:
        i = idx[v]
        M[i][i] = len(adj[v])
        for w in adj[v]:
            M[i][idx[w]] -= c
    b[idx[root]] = gamma
    for i in range(n):                               # Gaussian elimination
        p = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[p] = M[p], M[i]
        b[i], b[p] = b[p], b[i]
        for r in range(i + 1, n):
            f = M[r][i] / M[i][i]
            if f:
                for cc in range(i, n):
                    M[r][cc] -= f * M[i][cc]
                b[r] -= f * b[i]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
    return {v: x[idx[v]] for v in ids}


# ------------------------------- families ---------------------------------

def spider(Ls):
    adj = {0: []}
    nid = 1
    for L in Ls:
        prev = 0
        for _ in range(L):
            adj[nid] = [prev]
            adj[prev].append(nid)
            prev = nid
            nid += 1
    return adj


def caterpillar(spine, legs):
    """path of `spine` vertices off the root, each carrying `legs` pendants."""
    adj = {0: []}
    nid, prev = 1, 0
    for _ in range(spine):
        adj[nid] = [prev]
        adj[prev].append(nid)
        v, prev, nid = nid, nid, nid + 1
        for _ in range(legs):
            adj[nid] = [v]
            adj[v].append(nid)
            nid += 1
    return adj


def bintree(depth):
    adj = {0: []}
    nid, cur = 1, [0]
    for _ in range(depth):
        nxt = []
        for v in cur:
            for _ in range(2):
                adj[nid] = [v]
                adj[v].append(nid)
                nxt.append(nid)
                nid += 1
        cur = nxt
    return adj


def broom(handle, bristles):
    """path of `handle` vertices then a star of `bristles` leaves."""
    adj = {0: []}
    nid, prev = 1, 0
    for _ in range(handle):
        adj[nid] = [prev]
        adj[prev].append(nid)
        prev, nid = nid, nid + 1
    for _ in range(bristles):
        adj[nid] = [prev]
        adj[prev].append(nid)
        nid += 1
    return adj


def validate_tree(adj, alpha, eps, scans, mid, frontier):
    u = exact_u(adj, alpha)
    worst = 0.0
    for v in adj:
        hat = mid.get(v, 0.0)
        worst = max(worst, abs(hat - u[v]) / eps)
    return worst


if __name__ == "__main__":
    import itertools
    print("=== I2-E part 4: interval-envelope estimator on TREES ===")
    print("best-first frontier scan; D = max degree used for R_min\n")
    print(f"{'family':>26} {'n':>6} {'alpha':>8} {'eps':>8} {'T':>6} "
          f"{'T*eps':>7} {'err/eps':>8} {'ok':>5}")
    rows = []
    for aexp in (4, 8):
        alpha = 1 / (1 << aexp)
        for eexp in (5, 6, 7):
            eps = 1 / (1 << eexp)
            fams = [
                ('spider k=8 L=12', spider([12] * 8), 2),
                ('spider k=24 L=6', spider([6] * 24), 2),
                ('path L=60', spider([60]), 2),
                ('caterpillar 20x2', caterpillar(20, 2), 4),
                ('caterpillar 30x1', caterpillar(30, 1), 3),
                ('bintree depth 7', bintree(7), 3),
                ('broom 25+40', broom(25, 40), 41),
                ('mixed spider', spider([1, 2, 3, 5, 8, 13, 21, 34]), 2),
            ]
            for name, adj, D in fams:
                T, mid, fr, _ = estimate(adj, alpha, eps, D=D)
                err = validate_tree(adj, alpha, eps, T, mid, fr)
                ok = err <= 1.0 + 1e-9
                rows.append((name, len(adj), alpha, eps, T, T * eps, err, ok))
                print(f"{name:>26} {len(adj):6d} {alpha:8.5f} {eps:8.5f} "
                      f"{T:6d} {T*eps:7.4f} {err:8.4f} {str(ok):>5}")
    bad = [r for r in rows if not r[7]]
    print(f"\n  {len(rows)-len(bad)}/{len(rows)} outputs eps-VALID against the "
          f"exact linear solve")
    print(f"  max T*eps over all tree families = {max(r[5] for r in rows):.4f}")
    print(f"  max err/eps                      = {max(r[6] for r in rows):.4f}")
