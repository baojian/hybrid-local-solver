"""I3-B task 4: can vol(shell_tau(S*)) / vol(S*) grow with alpha^{-1}?

Construction: HUB LADDER on a path core.  Core = path v_0..v_L (v_0 = seed),
every core vertex carries ONE pendant hub of degree D_t (hub + D_t-1 dead
leaves).  Key fact that makes this exactly computable on a tiny system:

  a hub with x_hub = 0 influences the core ONLY through the core degree
  d_t = 3 (2 path neighbours + 1 hub).  Its degree D_t does not enter
  Q_SS, b_S or lambda_S at all.

So the core solution x is a function of L alone, and each hub's KKT ratio
    rel_t(D) = -grad_hub/lambda_hub = (1-alpha) x_t / (2 alpha rho D sqrt(d_t))
is exactly tunable per position: pick D_t = floor((1-alpha) x_t /
(2 tau alpha rho sqrt(d_t))) to place hub t exactly at KKT ratio tau (just
outside S* for tau < 1).  This is the "geometric ladder" of hub degrees: one
degree per position, all simultaneously marginal, no interaction, so the
feedback that killed I2-A section 7 (a hub entering S* truncates the
diffusion) cannot occur.

Then   vol(shell_tau) = sum_t D_t ,   vol(S*) = sum_t d_t = 3|core*| - 2.

Validated against a real graph build + exact_support_solver.
"""
import math
import sys

import numpy as np

sys.path.insert(0, "/home/claude/work/overnight/w3_apcg")
sys.path.insert(0, "/home/claude/work/overnight/lib")
from solvers import Model, exact_support_solver     # noqa: E402


def core_solve(alpha, rho, L, hub_every=1):
    """Exact RPPR solution on the ladder core (path v_0..v_{L-1}, degree 3
    where a hub is attached, 2 otherwise, 1 at the far end if no hub).
    Returns (x, d, S) with S the active prefix set (list of indices)."""
    d = np.empty(L)
    has_hub = np.array([(t % hub_every == 0) for t in range(L)])
    for t in range(L):
        deg = 0
        if t > 0:
            deg += 1
        if t < L - 1:
            deg += 1
        if has_hub[t]:
            deg += 1
        d[t] = deg
    sqd = np.sqrt(d)
    c = (1.0 + alpha) / 2.0
    off = -(1.0 - alpha) / 2.0
    b = np.zeros(L)
    b[0] = alpha / sqd[0]
    lam = alpha * rho * sqd
    # active set: prefix 0..k-1 (monotone decreasing profile)
    def solve_prefix(k):
        idx = np.arange(k)
        main = np.full(k, c)
        sub = off / np.sqrt(d[idx[:-1]] * d[idx[1:]]) if k > 1 else \
            np.zeros(0)
        A = np.diag(main) + np.diag(sub, 1) + np.diag(sub, -1)
        rhs = b[:k] - lam[:k]
        return np.linalg.solve(A, rhs)

    lo, hi = 1, L
    best = None
    while lo <= hi:                       # largest k with all x>0
        mid = (lo + hi) // 2
        xk = solve_prefix(mid)
        if np.min(xk) > 0:
            best = (mid, xk)
            lo = mid + 1
        else:
            hi = mid - 1
    k, xk = best
    x = np.zeros(L)
    x[:k] = xk
    # KKT check on the next core vertex
    if k < L:
        g = off / math.sqrt(d[k] * d[k - 1]) * x[k - 1] - b[k]
        assert -g <= lam[k] + 1e-14, ("core KKT", -g, lam[k])
    return x, d, k, has_hub


def ladder_stats(alpha, rho, tau, L=None, hub_every=1):
    if L is None:
        L = int(40.0 / math.sqrt(alpha)) + 60
    x, d, k, has_hub = core_solve(alpha, rho, L, hub_every)
    volS = float(np.sum(d[:k]))
    pi = np.sqrt(d) * x
    mass = float(np.sum(pi[:k]))
    Ds, rels = [], []
    for t in range(k):
        if not has_hub[t]:
            continue
        Dmax = (1.0 - alpha) * x[t] / (2.0 * tau * alpha * rho *
                                       math.sqrt(d[t]))
        D = math.floor(Dmax)
        if D < 1:
            continue
        Ds.append(D)
        rels.append((1.0 - alpha) * x[t] /
                    (2.0 * alpha * rho * D * math.sqrt(d[t])))
    volShell = float(sum(Ds))
    ub = (0.5 * mass) / (tau * alpha * rho)      # the lemma
    return dict(alpha=alpha, rho=rho, tau=tau, L=L, core_len=k,
                vol_S=volS, vol_shell=volShell, n_hubs=len(Ds),
                ratio=volShell / volS, mass=mass, ub=ub,
                ub_ratio=ub / volS,
                max_rel=max(rels) if rels else 0.0,
                min_rel=min(rels) if rels else 0.0,
                Dmax=max(Ds) if Ds else 0, Dmin=min(Ds) if Ds else 0)


def validate(alpha, rho, tau, L, hub_every=1, cap_nodes=400000):
    """Build the REAL ladder graph and check with exact_support_solver that
    (i) S* is exactly the core prefix, (ii) every hub has KKT ratio ~tau."""
    x, d, k, has_hub = core_solve(alpha, rho, L, hub_every)
    Ds = {}
    for t in range(L):
        if not has_hub[t] or t >= k:
            Ds[t] = 1 if has_hub[t] else 0
            continue
        Dmax = (1.0 - alpha) * x[t] / (2.0 * tau * alpha * rho *
                                       math.sqrt(d[t]))
        Ds[t] = max(1, math.floor(Dmax))
    ntot = L + sum(v for v in Ds.values() if v)
    if ntot > cap_nodes:
        return dict(skipped=True, ntot=ntot)
    edges = [(t, t + 1) for t in range(L - 1)]
    nid = L
    hubs = {}
    for t in range(L):
        if not has_hub[t]:
            continue
        h = nid; nid += 1
        edges.append((t, h))
        hubs[t] = h
        for _ in range(Ds[t] - 1):
            edges.append((h, nid)); nid += 1
    adj = {u: set() for u in range(nid)}
    for u, v in edges:
        adj[u].add(v); adj[v].add(u)
    adj = {u: sorted(adj[u]) for u in range(nid)}
    mdl = Model(adj, alpha, 0)
    xs, S = exact_support_solver(mdl, rho)
    grad = mdl.Q @ xs - mdl.b
    lam = alpha * rho * mdl.sqd
    rels = {t: float(-grad[h] / lam[h]) for t, h in hubs.items() if t < k}
    Sset = set(S)
    core_star = sorted(v for v in S if v < L)
    hub_in = [t for t, h in hubs.items() if h in Sset]
    err = float(np.max(np.abs(xs[:k] - x[:k]))) if k else 0.0
    volS = sum(int(mdl.d[v]) for v in S)
    shell = [h for t, h in hubs.items()
             if t < k and float(-grad[h] / lam[h]) >= tau * 0.98]
    volshell = sum(int(mdl.d[h]) for h in shell)
    return dict(skipped=False, n=nid, core_pred=k,
                core_star=len(core_star), hub_in_Sstar=len(hub_in),
                x_err=err, vol_S=volS, vol_shell=volshell,
                ratio=volshell / volS,
                max_rel=max(rels.values()) if rels else 0.0,
                min_rel=min(rels.values()) if rels else 0.0)


if __name__ == "__main__":
    import json
    out = {"ladder": [], "validate": []}
    rho = 1.0 / 200
    for e in (4, 6, 8, 10, 12, 14, 16):
        alpha = 2.0 ** -e
        r = ladder_stats(alpha, rho, tau=0.6)
        r["alpha_e"] = e
        out["ladder"].append(r)
        print("ladder", json.dumps({k: (round(v, 4) if isinstance(v, float)
                                        else v) for k, v in r.items()}),
              flush=True)
    # fixed-alpha rho sweep (is the growth alpha or just 1/(alpha rho)?)
    for e in (8, 12):
        alpha = 2.0 ** -e
        for rr in (1 / 50, 1 / 200, 1 / 800):
            r = ladder_stats(alpha, rr, tau=0.6)
            r["alpha_e"] = e
            out["ladder"].append(r)
            print("rho-sweep", json.dumps({k: (round(v, 4)
                                                if isinstance(v, float)
                                                else v)
                                           for k, v in r.items()}), flush=True)
    for e in (4, 6, 8):
        alpha = 2.0 ** -e
        L = int(40.0 / math.sqrt(alpha)) + 60
        v = validate(alpha, rho, 0.6, L)
        v["alpha_e"] = e
        out["validate"].append(v)
        print("validate", json.dumps({k: (round(x, 6)
                                          if isinstance(x, float) else x)
                                      for k, x in v.items()}), flush=True)
    json.dump(out, open("/home/claude/work/overnight/w10_i3b/res_shell.json",
                        "w"), indent=1)
