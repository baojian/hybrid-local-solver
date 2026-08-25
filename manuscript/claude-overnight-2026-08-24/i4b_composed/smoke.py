import sys, time
sys.path.insert(0, "/home/claude/work/overnight/i4b_composed")
sys.path.insert(0, "/home/claude/work/overnight/i3a_amg")
sys.path.insert(0, "/home/claude/work/overnight/lib")
import numpy as np
import zoo
from amglib import GModel, support_stats
from ledger import Ledger
from composed import composed_solve, wy_active

cases = [
    ("path", *zoo.path(4000)),
    ("star", *zoo.star(20000)),
    ("btree", *zoo.binary_tree(13)),
    ("theta", *zoo.theta_graph(300, 400, 500)),
    ("prism", *zoo.double_cycle(400)),
]


def grid(w, h):
    adj = {}
    for y in range(h):
        for x in range(w):
            u = y * w + x
            nb = []
            if x: nb.append(u - 1)
            if x + 1 < w: nb.append(u + 1)
            if y: nb.append(u - w)
            if y + 1 < h: nb.append(u + w)
            adj[u] = sorted(nb)
    return adj, (h // 2) * w + w // 2


cases.append(("grid2d", *grid(101, 101)))
cases.append(("rr3", *zoo.random_regular(4000, 3)))

for name, adj, seed in cases:
    for alpha in (2 ** -4, 2 ** -8):
        eps = 1e-6
        m = GModel(adj, alpha, seed)
        st = support_stats(m, eps)
        if st["nS"] == 0:
            print(f"{name} a={alpha} degenerate"); continue
        led = Ledger(m.d)
        t0 = time.perf_counter()
        r = composed_solve(m, eps, led, wall_cap=25.0)
        err = m.semantic_err(r["x"])
        v = led.vector()
        print(f"{name:8s} a=2^{int(np.log2(alpha)):<4d} volS={st['volS']:8.0f} "
              f"| {r['status']:5s} rd={r['rounds']:3d} flips={r['flips']} "
              f"routes={''.join('E' if x=='elim' else 'A' for x in r['routes'])[:24]} "
              f"nS={r['nS']:6d} volReg={r['volS']:8.0f} "
              f"W/vol={v['W']/max(st['volS'],1):8.1f} tri%={100*v['ctl_triage']/max(v['W'],1):4.1f} "
              f"e/eps={err/eps:.3f} [{time.perf_counter()-t0:.1f}s]", flush=True)
