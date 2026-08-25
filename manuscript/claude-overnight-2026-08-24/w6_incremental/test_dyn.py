"""Unit sanity for SEG-LDL: exactness of queries on a small comb + btree,
including a forced full_rebuild, against dense solves of every prefix."""
import sys
import numpy as np

sys.path.insert(0, '/home/claude/work/overnight/lib')
sys.path.insert(0, '/home/claude/work/overnight/w6_incremental')
from model import Model
from meter import Meter
import dyn_ldl
from dyn_ldl import DynTree


def comb(B, T):
    edges = [(i, i + 1) for i in range(B - 1)]
    nid = B
    for i in range(B):
        prev = i
        for _ in range(T):
            edges.append((prev, nid)); prev = nid; nid += 1
    adj = {u: set() for u in range(nid)}
    for u, v in edges:
        adj[u].add(v); adj[v].add(u)
    return {u: sorted(adj[u]) for u in range(nid)}, 0


def check(adj, seed, alpha, admit_order, force_rebuild_every=None):
    mo = Model(adj, alpha, seed)
    m = Meter(adj)
    dt = DynTree(mo, m)
    S = [seed]
    inS = {seed}
    maxerr = 0.0
    for step, v in enumerate(admit_order):
        par = [u for u in adj[v] if u in inS]
        assert len(par) == 1
        dt.admit(v, par[0])
        S.append(v); inS.add(v)
        if force_rebuild_every and (step + 1) % force_rebuild_every == 0:
            dt.full_rebuild()
        if (step + 1) % 7 == 0 or step == len(admit_order) - 1:
            idx = np.array(S)
            Qs = mo.Q[idx][:, idx].toarray()
            xs = np.linalg.solve(Qs, mo.b[idx])
            for k, u in enumerate(S):
                xq, _lev = dt.query_x(u, charge=False)
                maxerr = max(maxerr, abs(xq - xs[k]) / max(abs(xs[k]), 1e-300))
    return maxerr, dt


def bfs_order(adj, seed):
    seen = {seed}
    out = []
    q = [seed]
    while q:
        u = q.pop(0)
        for w in adj[u]:
            if w not in seen:
                seen.add(w); out.append(w); q.append(w)
    return out


adjc, s = comb(5, 4)
orderc = bfs_order(adjc, s)
for alpha in (0.25, 2.0 ** -8):
    e1, dt1 = check(adjc, s, alpha, orderc)
    print(f"comb  alpha={alpha:.6f} relerr={e1:.3e} levmax={max(dt1.levels)} paths={len(dt1.paths)}")
    assert e1 < 1e-9, e1
    e2, dt2 = check(adjc, s, alpha, orderc, force_rebuild_every=5)
    print(f"comb+rebuild alpha={alpha:.6f} relerr={e2:.3e} rebuilds={dt2.rebuilds}")
    assert e2 < 1e-9, e2

# btree depth 5, interleaved (BFS) admission
n = 2 ** 6 - 1
edges = []
for i in range(n):
    for c in (2 * i + 1, 2 * i + 2):
        if c < n:
            edges.append((i, c))
adjb = {u: set() for u in range(n)}
for u, v in edges:
    adjb[u].add(v); adjb[v].add(u)
adjb = {u: sorted(adjb[u]) for u in range(n)}
orderb = bfs_order(adjb, 0)
e3, dt3 = check(adjb, 0, 2.0 ** -6, orderb)
print(f"btree alpha=2^-6 relerr={e3:.3e} levmax={max(dt3.levels)} paths={len(dt3.paths)}")
assert e3 < 1e-9, e3
e4, dt4 = check(adjb, 0, 2.0 ** -6, orderb, force_rebuild_every=9)
print(f"btree+rebuild relerr={e4:.3e} rebuilds={dt4.rebuilds} levmax={max(dt4.levels)}")
assert e4 < 1e-9, e4

# deep path for scale sanity (log2 bookkeeping, no under/overflow)
np_ = 3000
adjp = {u: sorted({u - 1, u + 1} & set(range(np_))) for u in range(np_)}
mo = Model(adjp, 2.0 ** -10, 0)
m = Meter(adjp)
dt = DynTree(mo, m)
inS = {0}
for v in range(1, np_):
    dt.admit(v, v - 1)
    inS.add(v)
x0 = mo.solve_exact()
errs = []
for u in (0, 1, np_ // 2, np_ - 2, np_ - 1):
    xq, _ = dt.query_x(u, charge=False)
    errs.append(abs(xq - x0[u]) / max(abs(x0[u]), 1e-300))
print(f"path3000 alpha=2^-10 relerr={max(errs):.3e} (values down to {x0[np_-1]:.2e})")
assert max(errs) < 1e-8, errs
print("ALL UNIT TESTS PASS")
