"""Unit sanity for HSEG-LDL (dyn_ldl2.HDynTree): exactness of x-queries on
every admitted prefix vs dense solves, on admission orders that force many
heavy-path swaps.  Also re-runs the SEG-LDL (dyn_ldl) checks."""
import sys, random
import numpy as np

sys.path.insert(0, '/home/claude/work/overnight/lib')
sys.path.insert(0, '/home/claude/work/overnight/w6_incremental')
from model import Model
from meter import Meter
from dyn_ldl import DynTree
from dyn_ldl2 import HDynTree
import i2b


def check(adj, seed, alpha, admit_order, cls=HDynTree, every=7):
    mo = Model(adj, alpha, seed)
    m = Meter(adj)
    dt = cls(mo, m)
    S = [seed]
    inS = {seed}
    maxerr = 0.0
    for step, v in enumerate(admit_order):
        par = [u for u in adj[v] if u in inS]
        assert len(par) == 1, (v, par)
        dt.admit(v, par[0])
        S.append(v); inS.add(v)
        if (step + 1) % every == 0 or step == len(admit_order) - 1:
            idx = np.array(S)
            Qs = mo.Q[idx][:, idx].toarray()
            xs = np.linalg.solve(Qs, mo.b[idx])
            for k, u in enumerate(S):
                xq, _ = dt.query_x(u, charge=False)
                maxerr = max(maxerr, abs(xq - xs[k]) / max(abs(xs[k]), 1e-300))
    return maxerr, dt


def bfs_order(adj, seed):
    seen = {seed}; out = []; q = [seed]
    while q:
        u = q.pop(0)
        for w in adj[u]:
            if w not in seen:
                seen.add(w); out.append(w); q.append(w)
    return out


def rand_order(adj, seed, rng):
    inS = {seed}
    front = list(adj[seed])
    out = []
    while front:
        i = rng.randrange(len(front))
        v = front.pop(i)
        if v in inS:
            continue
        inS.add(v); out.append(v)
        front.extend(w for w in adj[v] if w not in inS)
    return out


def comb_teeth_first(B, T):
    """Admission order that interleaves teeth AHEAD of the backbone: exactly
    the order the real gate produces (deg-2 teeth beat deg-3 backbone)."""
    adj, s = i2b.comb(B, T)
    tooth = {i: [B + i * T + j for j in range(T)] for i in range(B)}
    order = []
    inS = {0}
    for d in range(1, B + T + 2):
        batch = []
        for i in range(B):
            j = d - i          # tooth vertex at depth j in tooth i
            if 1 <= j <= T and i in inS or (1 <= j <= T and i < d):
                batch.append(tooth[i][j - 1])
        if d < B:
            batch.append(d)    # backbone vertex admitted AFTER its teeth
        for v in batch:
            par = [u for u in adj[v] if u in inS]
            if len(par) == 1:
                order.append(v); inS.add(v)
    return adj, s, order


fails = []
rng = random.Random(3)

# 1. comb, BFS order
adjc, s = i2b.comb(6, 5)
for alpha in (0.25, 2.0 ** -8):
    e, dt = check(adjc, s, alpha, bfs_order(adjc, s))
    print(f"comb-bfs      a={alpha:.5f} relerr={e:.2e} levmax={max(dt.levels)} "
          f"swaps={dt.swaps} moved={dt.swap_moved}")
    if e > 1e-9: fails.append(('comb-bfs', alpha, e))

# 2. comb, teeth-before-backbone (the adversarial order)
adjt, st, ordt = comb_teeth_first(6, 5)
for alpha in (0.25, 2.0 ** -8):
    e, dt = check(adjt, st, alpha, ordt)
    print(f"comb-teeth1st a={alpha:.5f} relerr={e:.2e} levmax={max(dt.levels)} "
          f"swaps={dt.swaps} moved={dt.swap_moved}")
    if e > 1e-9: fails.append(('comb-teeth', alpha, e))
    e0, dt0 = check(adjt, st, alpha, ordt, cls=DynTree)
    print(f"   (SEG-LDL v1 same order: levmax={max(dt0.levels)} "
          f"paths={len(dt0.paths)})")

# 3. binary tree
n = 2 ** 6 - 1
edges = [(i, c) for i in range(n) for c in (2 * i + 1, 2 * i + 2) if c < n]
adjb = {u: set() for u in range(n)}
for u, v in edges:
    adjb[u].add(v); adjb[v].add(u)
adjb = {u: sorted(adjb[u]) for u in range(n)}
e, dt = check(adjb, 0, 2.0 ** -6, bfs_order(adjb, 0))
print(f"btree         relerr={e:.2e} levmax={max(dt.levels)} swaps={dt.swaps}")
if e > 1e-9: fails.append(('btree', e))

# 4. star (every admission is a new light child of the root)
adjs = {0: list(range(1, 41))}
adjs.update({i: [0] for i in range(1, 41)})
e, dt = check(adjs, 0, 2.0 ** -6, list(range(1, 41)), every=3)
print(f"star40        relerr={e:.2e} levmax={max(dt.levels)} swaps={dt.swaps}")
if e > 1e-9: fails.append(('star', e))

# 5. random recursive tree, random admission order
adjr, sr = i2b.rrt(120, 11)
e, dt = check(adjr, sr, 2.0 ** -6, rand_order(adjr, sr, rng), every=5)
print(f"rrt120        relerr={e:.2e} levmax={max(dt.levels)} swaps={dt.swaps} "
      f"moved={dt.swap_moved}")
if e > 1e-9: fails.append(('rrt', e))

# 6. deep path (log2 bookkeeping)
np_ = 4000
adjp = {u: sorted({u - 1, u + 1} & set(range(np_))) for u in range(np_)}
mo = Model(adjp, 2.0 ** -12, 0)
dt = HDynTree(mo, Meter(adjp))
for v in range(1, np_):
    dt.admit(v, v - 1)
x0 = mo.solve_exact()
errs = [abs(dt.query_x(u, charge=False)[0] - x0[u]) / max(abs(x0[u]), 1e-300)
        for u in (0, 1, np_ // 2, np_ - 2, np_ - 1)]
print(f"path4000      relerr={max(errs):.2e} (min value {x0[np_-1]:.2e}) "
      f"swaps={dt.swaps}")
if max(errs) > 1e-8: fails.append(('path', max(errs)))

print("FAILS:", fails if fails else "none — ALL UNIT TESTS PASS")
