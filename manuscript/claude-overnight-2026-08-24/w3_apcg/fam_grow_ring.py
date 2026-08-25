"""Growing marginal shell: path core + a hub at every other position whose
degree is tuned so that EVERY hub sits at the same KKT ratio `target` just
below 1.  Since rel_j is exactly proportional to 1/d_j, two rescaling passes
converge.  The shell then has Theta(alpha^{-1/2}) hubs each of volume
Theta(1/(alpha*rho)) -> shell volume / vol(S*) grows like 1/alpha."""
import sys

import numpy as np

sys.path.insert(0, "/home/claude/work/overnight/w3_apcg")
sys.path.insert(0, "/home/claude/work/overnight/lib")
from solvers import Model, exact_support_solver     # noqa: E402
from fam_attack import _sym                         # noqa: E402
import zoo                                          # noqa: E402


def build(core, degs_by_pos):
    edges = [(i, i + 1) for i in range(core - 1)]
    nid = core
    hubs = {}
    for k, dk in sorted(degs_by_pos.items()):
        hub = nid
        nid += 1
        edges.append((k, hub))
        for _ in range(max(1, dk) - 1):
            edges.append((hub, nid))
            nid += 1
        hubs[k] = hub
    return _sym(edges, nid), hubs, nid


def grow_ring(alpha, rho, core=900, spacing=2, target=0.97, dmin=3,
              dmax=20000, passes=12, cap_n=400000, damp=0.55, boost=1.6):
    """Returns (adj, seed, meta) with every hub at rel ~ target."""
    adj0, sd = zoo.path(core, seed_end=True)
    m0 = Model(adj0, alpha, sd)
    _, S0 = exact_support_solver(m0, rho)
    L = max(S0)
    pos = list(range(1, min(L + 2, core - 2), spacing))
    degs = {k: dmin for k in pos}
    for _ in range(passes):
        adj, hubs, n = build(core, degs)
        mdl = Model(adj, alpha, sd)
        xstar, S = exact_support_solver(mdl, rho)
        grad = mdl.Q @ xstar - mdl.b
        lam = alpha * rho * mdl.sqd
        new = {}
        Sset = set(S)
        for k in pos:
            h = hubs[k]
            rel = float(-grad[h] / lam[h])
            if h in Sset:
                # inside S*: measured rel is pinned at 1; push the hub out
                f = boost
            else:
                # rel is exactly proportional to 1/d_h at fixed core values;
                # damp to tame the feedback through the diffusion
                f = max(0.25, min(4.0, rel / target)) ** damp
            new[k] = int(min(dmax, max(dmin, round(degs[k] * f))))
        if sum(new.values()) > cap_n:
            sc = cap_n / sum(new.values())
            new = {k: max(dmin, int(v * sc)) for k, v in new.items()}
        degs = new
    adj, hubs, n = build(core, degs)
    return adj, sd, dict(hubs=sorted(hubs.values()), pos=pos, degs=degs, n=n,
                         core=core, L=int(L))
