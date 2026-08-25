"""E4: how loose is the repository's sufficient certificate?

For the zero-extended exact restricted solve on the BFS ball of radius R we
measure, exactly:
   theta(R) = max_v |r_v| / d_v      (push-scale residual; r = gamma s - M pi)
   err(R)   = max_v |pi_v - pihat_v| / d_v
   A(R)     = err(R) / theta(R)   in [0, (1+alpha)/(2 alpha)]
The stated certificate  ||D^{-1/2}(Qx-b)||_inf < alpha*eps  is exactly
theta < 2 alpha eps/(1+alpha), i.e. it ASSUMES the worst-case A = (1+a)/(2a).
If A = O(1) the certificate over-pays by ~1/alpha in value, hence by the
corresponding extra region volume in work.
"""
import json, math, sys
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
sys.path.insert(0, "/home/claude/work/overnight/i4d")
import fam
from fam import GModel

OUT = "/home/claude/work/overnight/i4d/out"


def amp_curve(adj, seed, alpha, eps, tag, Rs=None):
    m = GModel(adj, alpha, seed)
    x0 = spla.spsolve(m.Q.tocsc(), m.b)
    pi = x0 * m.sqd
    u = pi / m.d
    volSeps = float(m.d[u > eps].sum())
    # BFS shells
    dist = np.full(m.n, -1, np.int64); dist[seed] = 0
    fr = np.array([seed]); shells = [fr]; r = 0
    while fr.size:
        nb = np.unique(np.concatenate(
            [m.indices[m.indptr[v]:m.indptr[v+1]] for v in fr]))
        nb = nb[dist[nb] < 0]
        if nb.size == 0: break
        dist[nb] = r + 1; shells.append(nb); fr = nb; r += 1
    a = (1 - alpha) / 2.0
    ca = (1 - alpha) / (1 + alpha); ga = 2 * alpha / (1 + alpha)
    out = []
    if Rs is None:
        Rs = sorted(set([int(round(x)) for x in
                         np.geomspace(1, max(2, len(shells) - 2), 14)]))
    for R in Rs:
        if R >= len(shells) - 1: break
        S = np.concatenate(shells[:R + 1])
        QS = m.Q[S][:, S].tocsc()
        xs = spla.spsolve(QS, m.b[S])
        xh = np.zeros(m.n); xh[S] = xs
        pih = xh * m.sqd
        # push-scale residual r = gamma s - (I - ca A D^{-1}) pihat
        rr = -(pih - ca * (m.A @ (pih / m.d)))
        rr[seed] += ga
        theta = float(np.max(np.abs(rr) / m.d))
        err = float(np.max(np.abs(pih - pi) / m.d))
        out.append(dict(tag=tag, alpha=alpha, eps=eps, R=R,
                        volS=float(m.d[S].sum()), theta=theta, err=err,
                        A=err / theta if theta > 0 else float("nan"),
                        worst=(1 + alpha) / (2 * alpha), volSeps=volSeps))
    return out


def main():
    rows = []
    cases = [
        ("path",   lambda: fam.zoo.path(6000, seed_end=True)),
        ("spider", lambda: fam.zoo.spider(16, 400)),
        ("star",   lambda: fam.zoo.star(20000)),
        ("catpil", lambda: fam.zoo.caterpillar(4000, arm=1)),
        ("btree",  lambda: fam.zoo.binary_tree(14)),
        ("grid2d", lambda: fam.fast_grid(161, 161)),
        ("rrt",    lambda: fam.rrt(20000)),
        ("exp3reg",lambda: fam.zoo.random_regular(4000, 3)),
    ]
    for name, mk in cases:
        adj, seed = mk()
        for alpha in (2.0 ** -4, 2.0 ** -8, 2.0 ** -12):
            try:
                rows += amp_curve(adj, seed, alpha, 1e-6, name)
            except Exception as e:
                print(name, alpha, "EXC", e, flush=True)
        print(name, "done", flush=True)
        del adj
    json.dump(rows, open(f"{OUT}/amp.json", "w"))
    print("\n%-9s %7s | %-42s" % ("family", "alpha", "A = err/theta  (min .. max over R)"))
    for name, _ in cases:
        for alpha in (2.0 ** -4, 2.0 ** -8, 2.0 ** -12):
            rs = [r for r in rows if r["tag"] == name and r["alpha"] == alpha
                  and np.isfinite(r["A"])]
            if not rs: continue
            As = [r["A"] for r in rs]
            print("%-9s 2^%-5.0f | A in [%.3f, %.3f]   worst-case bound %.3g   "
                  "ratio to worst = %.2e"
                  % (name, math.log2(alpha), min(As), max(As),
                     rs[0]["worst"], max(As) / rs[0]["worst"]))


main()
