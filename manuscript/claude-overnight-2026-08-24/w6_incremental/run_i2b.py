"""I2-B main run: comb matrix + comb scaling + full tree zoo, all backends."""
import sys, json, time
import numpy as np

sys.path.insert(0, '/home/claude/work/overnight/lib')
sys.path.insert(0, '/home/claude/work/overnight/w6_incremental')
from model import Model
import zoo, core, i2b

WANT = ['COLD-LU', 'INC-LDL', 'TREE-INC', 'SEG-LDL', 'HSEG-LDL']
ALPHAS = [2.0 ** -6, 2.0 ** -10, 2.0 ** -14]
OUT = '/home/claude/work/overnight/w6_incremental/res_i2b.json'
out = []
t00 = time.time()
BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 900.0


def show(rec, tag):
    ln = f"[{time.time()-t00:6.1f}s] {tag} a=2^{int(np.log2(rec['alpha']))} " \
         f"eps=2^{int(np.log2(rec['eps']))} S={rec['S']} vol={rec['volS']} " \
         f"E={rec['E']}"
    print(ln, flush=True)
    for k in WANT:
        v = rec['bk'].get(k)
        if not v:
            continue
        extra = ''
        if k in ('SEG-LDL', 'HSEG-LDL') and 'lev_mean' in v:
            extra = (f" lev={v['lev_mean']:.2f}/{v['lev_max']}"
                     f" adm/v={v['admit_nodes_total']/max(rec['S'],1):.1f}"
                     f" q/q={v['query_nodes_total']/max(v['nqueries'],1):.1f}")
            if 'swaps' in v:
                extra += f" swaps={v['swaps']} moved={v['swap_moved']}"
        if k == 'INC-LDL' and 'nnzL' in v:
            extra = f" nnzL/S={v['nnzL']/max(rec['S'],1):.1f}"
        print(f"    {k:9s} W/vol={v.get('Wvol', float('nan')):10.2f}"
              f"{' CAP@%.2f' % v['frac'] if v.get('capped') else ''}"
              f"{v.get('error','')}{extra}", flush=True)


def go(adj, seed, alpha, tag, cap_S, extra=None, want=WANT):
    mo = Model(adj, alpha, seed)
    eps, tr = i2b.tune_eps_trace(mo, cap_S, keep_Q=False)
    w = list(want)
    if not core.is_tree(adj):
        w = [x for x in w if x not in ('TREE-INC', 'SEG-LDL', 'HSEG-LDL')]
    rec = i2b.run_all(mo, eps, w, keep_Q=False, tr=tr, verbose=False,
                      inc_cap=(6e6, 8e8))
    rec['tag'] = tag
    rec.update(extra or {})
    show(rec, tag)
    out.append(rec)
    json.dump(out, open(OUT, 'w'))
    return rec


# ---------------------------------------------------------------- 1. comb
for B in [32, 128, 512]:
    for a in ALPHAS:
        T = max(2, int(round(1.0 / np.sqrt(a))))
        adj, s = i2b.comb(B, T)
        go(adj, s, a, f'comb(B={B},T={T})', 2500,
           dict(family='comb', Bbone=B, T=T, kind='matrix'))

# ---------------------------------------------------------------- 2. scaling
for B in [512, 32]:
    for a in [2.0 ** -10, 2.0 ** -14]:
        T = max(2, int(round(1.0 / np.sqrt(a))))
        adj, s = i2b.comb(B, T)
        mo = Model(adj, a, s)
        prev = -1
        for k in range(2, 40):
            if time.time() - t00 > BUDGET * 0.55:
                break
            tr = core.grow_trace(mo, 2.0 ** -k, keep_Q=False)
            sz = len(tr['S'])
            if sz == prev or sz < 200:
                prev = sz; continue
            if sz > 9000:
                break
            prev = sz
            rec = i2b.run_all(mo, 2.0 ** -k, WANT, keep_Q=False, tr=tr,
                              verbose=False, inc_cap=(6e6, 8e8))
            rec['tag'] = f'combscale(B={B},T={T})'
            rec.update(family='comb', Bbone=B, T=T, kind='scale')
            show(rec, rec['tag'])
            out.append(rec)
            json.dump(out, open(OUT, 'w'))

# ---------------------------------------------------------------- 3. zoo
FAM = [
    ('path', lambda: zoo.path(8000)),
    ('caterpillar', lambda: zoo.caterpillar(4000, 1)),
    ('spider', lambda: zoo.spider(8, 800)),
    ('btree', lambda: zoo.binary_tree(12)),
    ('rrt2000', lambda: i2b.rrt(2000, 7)),
    ('theta', lambda: zoo.theta_graph(200, 200, 200)),
]
for name, fn in FAM:
    adj, s = fn()
    for a in ALPHAS:
        if time.time() - t00 > BUDGET:
            print('BUDGET STOP'); break
        go(adj, s, a, name, 2500, dict(family=name, kind='zoo'))
print(f"TOTAL {time.time()-t00:.1f}s")
