import sys, time
import numpy as np
sys.path.insert(0, "/home/claude/work/overnight/i4e")
sys.path.insert(0, "/home/claude/work/overnight/i4d")
sys.path.insert(0, "/home/claude/work/overnight/i3a_amg")
sys.path.insert(0, "/home/claude/work/overnight/lib")
import fam
from amglib import GModel, push_c, direct_local
from vgf import vgf_local, DQMeter, out_measure

def run(adj, seed, a, eps, tag):
    m = GModel(adj, a, seed)
    x0 = m.solve_exact()
    om = out_measure(m, eps, x0)
    line = f"{tag:28s} n={m.n:7d} volS_eps={om['volS']:8.0f} nS={om['nS']:6d} |"
    for mode, kw in (("VGF", dict(gate_mode="sound")),
                     ("VGFopt", dict(gate_mode="opt")),
                     ("VGF-O", dict(gate_mode="sound", oracle=True))):
        mt = DQMeter(m.d)
        t = time.perf_counter()
        r = vgf_local(m, eps, mt, x_exact=x0, wall_cap=30.0, **kw)
        e = float(np.max(np.abs(r["x"] - x0) / m.sqd))
        miss = int(np.setdiff1d(om["Sset"],
                                np.flatnonzero(r["x"] != 0)).size)
        line += (f" {mode}:W*e={mt.total()*eps:.4g} vol={r['volS']:.0f}"
                 f" cv={r.get('cert_vol',0):.0f} R={r['rounds']} "
                 f"e/eps={e/eps:.3g} {r['status']}{'MISS%d' % miss if miss else ''}"
                 f" [{time.perf_counter()-t:.1f}s] |")
    p = push_c(m, eps)
    ep = float(np.max(np.abs(p["x"] - x0) / m.sqd))
    line += f" push:W*e={p['W']*eps:.4g} e/eps={ep/eps:.3g}"
    print(line, flush=True)

print("--- smoke ---")
import zoo
run(*fam.rrt(2000), 2.0**-8, 1e-5, "rrt2000 a=2^-8")
adj, s = zoo.path(4000); run(adj, s, 2.0**-8, 1e-5, "path4000 a=2^-8")
adj, s = zoo.star(2000); run(adj, s, 2.0**-4, 1e-5, "star2000 a=2^-4")
adj, s = fam.fast_grid(120, 120); run(adj, s, 2.0**-8, 1e-5, "grid2d120 a=2^-8")
adj, s = fam.ball_trap(400, 300, at=60); run(adj, s, 7.4e-6, 1e-3, "balltrap M=300")
adj, s = fam.hidden_hub(6, 10000); run(adj, s, 2.0**-6, 1e-3, "hiddenhub M=1e4")
