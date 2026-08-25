import math, sys
import numpy as np
sys.path.insert(0, "/home/claude/work/overnight/i4d")
import fam
from fam import GModel
from amglib import VecMeter, amg_local, push_c, direct_local

class DQMeter(VecMeter):
    def ring_scan(self, idx):
        k = len(idx)
        if k: self.C_resp += float(k); self.solve += float(k)

def cell(adj, seed, a, eps, tag, mechs, W=10.0):
    m = GModel(adj, a, seed); x0 = m.solve_exact()
    u = x0*m.sqd/m.d; S = np.flatnonzero(u > eps)
    volS = float(m.d[S].sum())
    nb = np.unique(np.concatenate([m.indices[m.indptr[v]:m.indptr[v+1]]
                                   for v in S])) if S.size else np.array([],int)
    inS = np.zeros(m.n,bool); inS[S]=True; B = nb[~inS[nb]]
    line = "%-20s n=%-8d vol(S)=%-7.0f volS*eps=%-6.3f vol(dS)*eps=%-9.4g |" % (
        tag, m.n, volS, volS*eps, float(m.d[B].sum())*eps)
    for w in mechs:
        try:
            if w == "push":
                r = push_c(m, eps); Wt, x, st = r["W"], r["x"], "cert"
            elif w in ("direct","directDQ"):
                mt=(DQMeter if w.endswith("DQ") else VecMeter)(m.d)
                r=direct_local(m,eps,mt,wall_cap=W); Wt,x,st=mt.total(),r["x"],r["status"]
            else:
                mt=(DQMeter if w.endswith("DQ") else VecMeter)(m.d)
                r=amg_local(m,eps,mt,wall_cap=W); Wt,x,st=mt.total(),r["x"],r["status"]
            e = float(np.max(np.abs(x-x0)/m.sqd))
            line += " %s:%.4g%s" % (w, Wt*eps, "" if (e<=eps and st=="cert") else "!")
        except Exception as ex:
            line += " %s:EXC" % w
    print(line, flush=True)

print("A1 HIDDEN HUB  (S_eps fixed at a 6-path; ONE boundary vertex of degree M)")
for M in (1000, 10000, 100000):
    adj, s = fam.hidden_hub(6, M)
    cell(adj, s, 2.0**-6, 1e-3, "hidden_hub M=%d"%M,
         ("push","direct","directDQ","amg","amgDQ"))
print("\nA2 BALL TRAP  (support = path prefix; K_M clique hung at depth 60)")
for M in (100, 300, 600):
    eps=1e-3; a=7.4*eps*eps
    adj, s = fam.ball_trap(400, M, at=60)
    cell(adj, s, a, eps, "ball_trap M=%d"%M, ("push","directDQ","amgDQ"))
