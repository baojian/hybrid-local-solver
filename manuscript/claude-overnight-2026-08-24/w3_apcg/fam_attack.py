"""I2-A adversarial families for carry-mode growing-support APCG.

(a) marginal_ring: endpoint-seeded core path with many hubs (hub node +
    (hub_deg-1) leaves) attached at consecutive positions chosen so every
    hub's KKT ratio (-grad_j / lam_j at the hub-free optimum, with the
    attachment degree corrected to 3) lies in a band strictly BELOW 1:
    every hub is a barely-outside decoy graded ~sqrt(2*alpha) per position.
(b) staircase: plain endpoint-seeded path (one admission at a time).
(c) lollipop: clique K_h head + path tail, seeded inside the clique.
(d) k8_embedded: K_8 with the Round-026 pulse seed distribution, path tail
    attached at node 0; alpha = q^2/(1+q^2).
"""
import math
import sys

import numpy as np

sys.path.insert(0, "/home/claude/work/overnight/w3_apcg")
sys.path.insert(0, "/home/claude/work/overnight/lib")
from solvers import Model, exact_support_solver     # noqa: E402
import zoo                                          # noqa: E402


def _sym(edges, n):
    adj = {u: set() for u in range(n)}
    for u, v in edges:
        if u != v:
            adj[u].add(v)
            adj[v].add(u)
    return {u: sorted(adj[u]) for u in range(n)}


def _build_ring(core, pos, hub_deg):
    edges = [(i, i + 1) for i in range(core - 1)]
    nid = core
    hubs = []
    for k in pos:
        hub = nid
        nid += 1
        edges.append((k, hub))
        for _ in range(hub_deg - 1):
            edges.append((hub, nid))
            nid += 1
        hubs.append(hub)
    return _sym(edges, nid), hubs, nid


def marginal_ring(alpha, rho, core=420, hub_deg=256, max_hubs=40,
                  spacing=2):
    """Swath of pendant hubs (hub + hub_deg-1 leaves) straddling the
    REALIZED support boundary of the attached graph (interaction included:
    positions from the hub-free boundary L0, swath [0.45*L0, L0+2],
    exact-solve determines which land inside/outside).
    Returns (adj, seed, meta)."""
    adj0, seed = zoo.path(core, seed_end=True)
    mdl0 = Model(adj0, alpha, seed)
    _, S0 = exact_support_solver(mdl0, rho)
    L0 = max(S0)
    lo = max(1, int(0.45 * L0))
    hi = min(core - 2, L0 + 2)
    pos = list(range(lo, hi + 1, spacing))
    if len(pos) > max_hubs:                 # keep the ones nearest boundary
        pos = pos[-max_hubs:]
    adj, hubs, nid = _build_ring(core, pos, hub_deg)
    meta = dict(positions=pos, hubs=hubs, hub_deg=hub_deg, n=nid,
                core=core, L0=int(L0))
    return adj, seed, meta


def check_ring(mdl, rho, meta):
    """Exact-solve the ring graph; report which hubs are inside S*, min/max
    hub slack relative to lam among outside hubs."""
    xstar, S = exact_support_solver(mdl, rho)
    Sset = set(S)
    grad = mdl.Q @ xstar - mdl.b
    info = []
    for k, h in zip(meta["positions"], meta["hubs"]):
        lamh = mdl.alpha * rho * mdl.sqd[h]
        rel = float(-grad[h] / lamh)          # >1 => violates => in S*
        info.append(dict(pos=k, hub=h, inS=h in Sset, rel=rel))
    outs = [i["rel"] for i in info if not i["inS"]]
    ins = sum(1 for i in info if i["inS"])
    return xstar, S, dict(hubs_in_Sstar=ins,
                          max_rel_outside=max(outs) if outs else None,
                          min_rel_outside=min(outs) if outs else None,
                          detail=info)


def lollipop(head=16, tail=360):
    edges = [(i, j) for i in range(head) for j in range(i + 1, head)]
    prev = 0
    nid = head
    for _ in range(tail):
        edges.append((prev, nid))
        prev = nid
        nid += 1
    return _sym(edges, nid), 1          # seed inside the clique, not junction


def k8_embedded(tail=260):
    edges = [(i, j) for i in range(8) for j in range(i + 1, 8)]
    prev = 0
    nid = 8
    for _ in range(tail):
        edges.append((prev, nid))
        prev = nid
        nid += 1
    adj = _sym(edges, nid)
    # Round-026 K8 pulse seed distribution (validated in w7_windowed)
    s0 = 363437.0 / 651088.0
    si = 41093.0 / 651088.0
    seed = {0: s0}
    for i in range(1, 8):
        seed[i] = si
    return adj, seed


def q_alpha(q):
    return q * q / (1.0 + q * q)


# ------------------------------------------------------------------ (a2)
# Symmetric marginal-hub ring: the sharp version.  Star core (center seed,
# m core leaves); every core leaf carries a pendant HUB of degree hub_deg.
# By symmetry ALL hubs have identical KKT ratio, so a single rho tunes the
# whole ring to the activation breakpoint simultaneously: if momentum
# overshoot trips the gate, it trips it for all m hubs at once and the
# spurious volume is m*hub_deg vs vol(S*) = 3m.

def ring_star(m=100, hub_deg=64):
    """center 0 (deg m); core leaves 1..m (deg 2); hub_k (deg hub_deg)
    pendant on leaf k, with hub_deg-1 dead leaves.  Returns (adj, seed, meta)."""
    edges = [(0, k) for k in range(1, m + 1)]
    nid = m + 1
    hubs = []
    for k in range(1, m + 1):
        hub = nid
        nid += 1
        edges.append((k, hub))
        for _ in range(hub_deg - 1):
            edges.append((hub, nid))
            nid += 1
        hubs.append(hub)
    meta = dict(hubs=hubs, m=m, hub_deg=hub_deg, n=nid,
                core=[0] + list(range(1, m + 1)))
    return _sym(edges, nid), 0, meta


def hub_rel(mdl, rho, hubs):
    """(xstar, S, max over hubs of -grad_j/lam_j, #hubs in S*)."""
    xstar, S = exact_support_solver(mdl, rho)
    grad = mdl.Q @ xstar - mdl.b
    lam = mdl.alpha * rho * mdl.sqd
    rels = [float(-grad[h] / lam[h]) for h in hubs]
    return xstar, S, max(rels), sum(1 for h in hubs if h in set(S))


def tune_rho_breakpoint(adj, seed, alpha, hubs, target_rel=0.98,
                        lo=1e-7, hi=0.25, iters=44):
    """Bisect rho so the hubs sit just BELOW activation: returns (rho, rel).
    Support shrinks with rho, so 'no hub in S*' is monotone increasing in rho."""
    mk = lambda r: Model(adj, alpha, seed)          # noqa: E731
    mdl = Model(adj, alpha, seed)
    def out(r):
        _, S, rel, nin = hub_rel(mdl, r, hubs)
        return nin == 0, rel
    ok_hi, _ = out(hi)
    if not ok_hi:
        return hi, out(hi)[1]
    ok_lo, _ = out(lo)
    if ok_lo:
        return lo, out(lo)[1]
    # bisect for rho_c (smallest rho with no hub inside)
    for _ in range(iters):
        mid = math.sqrt(lo * hi)
        o, _ = out(mid)
        if o:
            hi = mid
        else:
            lo = mid
    # walk up from rho_c until rel <= target_rel (marginal but safely outside)
    r = hi
    for _ in range(60):
        o, rel = out(r)
        if o and rel <= target_rel:
            return r, rel
        r *= 1.004
    return r, out(r)[1]
