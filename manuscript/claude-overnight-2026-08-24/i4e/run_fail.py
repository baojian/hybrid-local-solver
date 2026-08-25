"""E4: the HONEST FAILURE HUNT -- three families built to break value-guided
admission.
 (a) FAN TRAP        : excluding a vertex is what costs.  K permanent ring
                       vertices that are never admitted but must be re-tested.
 (b) EXPANDER POCKET : the value-admitted region has small volume but
                       treewidth Theta(N) -- a bad shape for the inner solver.
 (c) SHALLOW SUPPORT : eps just under u_max, so S_eps is O(1) but the SOUND
                       gate gamma*eps forces the region out to S_{gamma eps}.
"""
import json, math, sys
import numpy as np
sys.path.insert(0, "/home/claude/work/overnight/i4e")
from common import cell, fam, zoo, GModel, out_measure, vgf_local, DQMeter


def fan_trap(L, K, D, at=20):
    """path 0..L-1 seeded at 0; K 'blockers' of degree D hung on vertex `at`.
    Each blocker is a permanent RING vertex: its value is u_at*c_a/D, tuned
    below the gate, so it is excluded -- but it must be re-tested every round.
    vol(S_eps) grows like 2L + K; |dS| = K + (D-1) per admitted blocker."""
    edges = [(i, i + 1) for i in range(L - 1)]
    nid = L
    for _ in range(K):
        blk = nid
        nid += 1
        edges.append((at, blk))
        for _ in range(D - 1):
            edges.append((blk, nid))
            nid += 1
    return zoo._sym(edges, nid), 0


def exp_pocket(pre, N, deg=3, sd=3):
    """seed - short path - random deg-regular expander on N vertices.
    The pocket has volume deg*N but treewidth Theta(N): LDL fill is N^2."""
    g, _ = zoo.random_regular(N, deg, seed_rng=sd)
    edges = [(i, i + 1) for i in range(pre - 1)]
    off = pre
    for u in g:
        for v in g[u]:
            if u < v:
                edges.append((off + u, off + v))
    edges.append((pre - 1, off))
    return zoo._sym(edges, off + N), 0


out = []
MECH = ("push", "composed", "directDQ", "vgf", "vgfO")
print("=== E4a  FAN TRAP  (exclusion cost): fan_trap(400, K, D=200, at=20) ===")
for K in (10, 50, 200, 800):
    adj, s = fan_trap(400, K, 200, at=20)
    out.append(cell(adj, s, 2.0 ** -10, 1e-4, "fan_trap K=%d" % K, MECH))
print()
print("=== E4b  EXPANDER POCKET  (small volume, treewidth Theta(N)) ===")
for N in (500, 1500, 4000):
    adj, s = exp_pocket(20, N, 3)
    m = GModel(adj, 2.0 ** -8, s)
    x0 = m.solve_exact()
    om = out_measure(m, 1e-5, x0)
    line = "exp_pocket N=%-6d volS_eps=%-7.0f |" % (N, om["volS"])
    for tag, kw in (("VGF/ldl", dict(inner="ldl")),
                    ("VGF/auto", dict(inner="auto"))):
        mt = DQMeter(m.d)
        r = vgf_local(m, 1e-5, mt, x_exact=x0, wall_cap=25.0, **kw)
        e = float(np.max(np.abs(r["x"] - x0) / m.sqd))
        miss = int(np.setdiff1d(om["Sset"],
                                np.flatnonzero(r["x"] != 0)).size)
        line += (" %s W*e=%.4g vol=%.0f R=%d e/eps=%.3g miss=%d %s |"
                 % (tag, mt.total() * 1e-5, r["volS"], r["rounds"],
                    e / 1e-5, miss, r["status"]))
    print(line, flush=True)
    out.append(cell(adj, s, 2.0 ** -8, 1e-5, "exp_pocket N=%d" % N, MECH))
print()
print("=== E4c  SHALLOW SUPPORT  (eps just under u_max; S_eps is O(1)) ===")
print("    the sound gate gamma*eps forces the region out to S_{gamma*eps}")
for a in (2.0 ** -4, 2.0 ** -8, 2.0 ** -12):
    adj, s = zoo.path(40000)
    m = GModel(adj, a, s)
    x0 = m.solve_exact()
    umax = float((x0 * m.sqd / m.d).max())
    for c in (0.5, 0.05):
        eps = c * umax
        out.append(cell(adj, s, a, eps,
                        "shallow a=2^-%d c=%.2f"
                        % (int(round(-math.log2(a))), c), MECH, wall=20.0))
with open("/home/claude/work/overnight/i4e/out/fail.json", "w") as fh:
    json.dump(out, fh, default=str)
print("done")
