"""Numerical verification of the shell-volume lemma.

IDENTITY (exact, from summing the RPPR KKT conditions):
    (1-alpha)/2 * T  =  alpha * [ s(S*) - ||pi||_1 - rho*vol(S*) ]
where T = sum_{i notin S*} sum_{h~i} pi_h/d_h  is the total leak flow.

LEMMA:  tau*rho*vol(Shell_tau) + rho*vol(S*)  <=  s(S* u Shell) - ||pi||_1
        so   vol(Shell_tau)/vol(S*) <= (1/tau)*[1/(rho*vol(S*)) - 1] ,
        which contains NO alpha.
"""
import json
import math
import sys

import numpy as np

sys.path.insert(0, "/home/claude/work/overnight/w3_apcg")
sys.path.insert(0, "/home/claude/work/overnight/lib")
from solvers import Model, exact_support_solver     # noqa: E402
import zoo                                          # noqa: E402
import run as RR                                    # noqa: E402


def check(adj, seed, alpha, rho, tau=0.6, tag=""):
    mdl = Model(adj, alpha, seed)
    xs, S = exact_support_solver(mdl, rho)
    Sset = set(S)
    grad = mdl.Q @ xs - mdl.b
    lam = alpha * rho * mdl.sqd
    pi = mdl.sqd * xs
    d = mdl.d
    volS = float(sum(d[v] for v in S))
    mass = float(np.sum(pi))
    T = 0.0
    for i in range(mdl.n):
        if i in Sset:
            continue
        T += sum(pi[h] / d[h] for h in adj[i])
    lhs = (1 - alpha) / 2 * T
    rhs = alpha * (float(np.sum(mdl.s[list(Sset)])) - mass - rho * volS)
    shell = [j for j in range(mdl.n)
             if j not in Sset and -grad[j] >= tau * lam[j]]
    volSh = float(sum(d[j] for j in shell))
    nb = set()
    for v in S:
        for h in adj[v]:
            if h not in Sset:
                nb.add(h)
    volB = float(sum(d[j] for j in nb))
    s_sh = float(np.sum(mdl.s[shell])) if shell else 0.0
    bound = (float(np.sum(mdl.s[list(Sset)])) + s_sh - mass
             - rho * volS) / (tau * rho)
    ratio_bound = (1.0 / tau) * (1.0 / (rho * volS) - 1.0)
    return dict(tag=tag, alpha=alpha, rho=rho, n=mdl.n, volS=volS,
                volShell=volSh, volB=volB, ratio=volSh / volS,
                ratio_B=volB / volS, mass=mass,
                ident_lhs=lhs, ident_rhs=rhs,
                ident_relerr=abs(lhs - rhs) / max(abs(rhs), 1e-300),
                bound_vol=bound, bound_ok=bool(volSh <= bound * (1 + 1e-9)),
                ratio_bound=ratio_bound,
                ratio_bound_ok=bool(volSh / volS <= ratio_bound * (1 + 1e-9)),
                tightness=(volSh / volS) / ratio_bound)


if __name__ == "__main__":
    out = []
    for e in (4, 8, 12):
        a = 2.0 ** -e
        adj, sd = zoo.path(600)
        out.append(check(adj, sd, a, 1 / 400, tag=f"path a2^-{e}"))
        adj, sd = zoo.caterpillar(200, 1)
        out.append(check(adj, sd, a, 1 / 400, tag=f"cat a2^-{e}"))
        adj, sd = zoo.grid(20, 20)
        out.append(check(adj, sd, a, 1 / 400, tag=f"grid a2^-{e}"))
        adj, sd = zoo.binary_tree(7)
        out.append(check(adj, sd, a, 1 / 400, tag=f"btree a2^-{e}"))
    for D in (12, 48, 192):
        for e in (8, 12):
            a = 2.0 ** -e
            adj, sd, hubs = RR.ring_star(m=60, hub_deg=D)
            rho, rel = RR.tune_rho_ring(adj, sd, a, hubs, target_rel=0.95,
                                        iters=24)
            out.append(check(adj, sd, a, rho, tag=f"ring D{D} a2^-{e}"))
    for r in out:
        print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v)
                          for k, v in r.items()}), flush=True)
    json.dump(out, open("/home/claude/work/overnight/w10_i3b/res_lemma.json",
                        "w"), indent=1)
    print("ALL identity ok:", all(r["ident_relerr"] < 1e-6 for r in out))
    print("ALL bound ok:", all(r["ratio_bound_ok"] for r in out))
