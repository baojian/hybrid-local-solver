"""I2-B final campaign: comb matrix, comb/caterpillar/path scaling, tree zoo."""
import sys, json, time
import numpy as np

sys.path.insert(0, '/home/claude/work/overnight/lib')
sys.path.insert(0, '/home/claude/work/overnight/w6_incremental')
from model import Model
import zoo, core, i2b

WANT = ['COLD-LU', 'INC-LDL', 'TREE-INC', 'SEG-LDL', 'HSEG-LDL']
ALPHAS = [2.0 ** -6, 2.0 ** -10, 2.0 ** -14]
OUT = '/home/claude/work/overnight/w6_incremental/res_final.json'
out = []
t00 = time.time()


def show(rec, tag):
    print(f"[{time.time()-t00:6.1f}s] {tag} a=2^{int(np.log2(rec['alpha']))} "
          f"eps=2^{int(np.log2(rec['eps']))} S={rec['S']} vol={rec['volS']} "
          f"E={rec['E']} meanT={rec['meanT']:.1f}", flush=True)
    for k in WANT:
        v = rec['bk'].get(k)
        if not v:
            continue
        x = ''
        if 'lev_mean' in v:
            x = (f" lev={v['lev_mean']:.2f}/{v['lev_max']}"
                 f" adm/v={v['admit_nodes_total']/max(rec['S'],1):.1f}"
                 f" q/q={v['query_nodes_total']/max(v['nqueries'],1):.1f}")
            if 'swaps' in v:
                x += f" sw={v['swaps']} mv/S={v['swap_moved']/max(rec['S'],1):.2f}"
        if k == 'INC-LDL' and 'nnzL' in v:
            x = f" nnzL/S={v['nnzL']/max(rec['S'],1):.1f}"
        print(f"    {k:9s} W/vol={v.get('Wvol', float('nan')):10.2f}"
              f"{' CAP@%.2f' % v['frac'] if v.get('capped') else ''}"
              f"{v.get('error','')}{x}", flush=True)


def go(mo, eps, tr, tag, extra, want=WANT, cap=(2e6, 2e8)):
    w = [x for x in want if core.is_tree(mo.adj)
         or x not in ('TREE-INC', 'SEG-LDL', 'HSEG-LDL')]
    rec = i2b.run_all(mo, eps, w, keep_Q=False, tr=tr, verbose=False,
                      inc_cap=cap)
    rec['tag'] = tag
    rec.update(extra)
    show(rec, tag)
    out.append(rec)
    json.dump(out, open(OUT, 'w'))
    return rec


def tuned(adj, seed, a, tag, extra, cap_S=2500, **kw):
    mo = Model(adj, a, seed)
    eps, tr = i2b.tune_eps_trace(mo, cap_S, keep_Q=False)
    return go(mo, eps, tr, tag, extra, **kw)


def series(adj, seed, a, tag, extra, lo=200, hi=9000, tlimit=1e9, **kw):
    mo = Model(adj, a, seed)
    prev = -1
    for k in range(2, 40):
        if time.time() - t00 > tlimit:
            break
        tr = core.grow_trace(mo, 2.0 ** -k, keep_Q=False)
        sz = len(tr['S'])
        if sz == prev or sz < lo:
            prev = sz; continue
        if sz > hi:
            break
        prev = sz
        go(mo, 2.0 ** -k, tr, tag, dict(extra, kind='scale'), **kw)


# ----------------------------------------------------- 1. comb (B,alpha) matrix
for B in [32, 128, 512]:
    for a in ALPHAS:
        T = max(2, int(round(1.0 / np.sqrt(a))))
        adj, s = i2b.comb(B, T)
        tuned(adj, s, a, f'comb(B={B},T={T})',
              dict(family='comb', Bbone=B, T=T, kind='matrix'))

# ----------------------------------------------------- 2. scaling series
for B, a in [(512, 2.0 ** -14), (512, 2.0 ** -10), (32, 2.0 ** -14)]:
    T = max(2, int(round(1.0 / np.sqrt(a))))
    adj, s = i2b.comb(B, T)
    series(adj, s, a, f'combscale(B={B},T={T})',
           dict(family='comb', Bbone=B, T=T), tlimit=330)
adjc, sc = zoo.caterpillar(6000, 1)
series(adjc, sc, 2.0 ** -14, 'catscale', dict(family='caterpillar'), tlimit=430)
adjp, sp = zoo.path(12000)
series(adjp, sp, 2.0 ** -14, 'pathscale', dict(family='path'), tlimit=480)

# ----------------------------------------------------- 3. tree zoo
FAM = [('path', lambda: zoo.path(8000), ALPHAS),
       ('caterpillar', lambda: zoo.caterpillar(4000, 1), ALPHAS),
       ('spider', lambda: zoo.spider(8, 800), ALPHAS),
       ('btree', lambda: zoo.binary_tree(12), [2.0 ** -10]),
       ('rrt2000', lambda: i2b.rrt(2000, 7), ALPHAS),
       ('theta', lambda: zoo.theta_graph(200, 200, 200), ALPHAS)]
for name, fn, als in FAM:
    adj, s = fn()
    for a in als:
        tuned(adj, s, a, name, dict(family=name, kind='zoo'),
              cap=(6e5, 6e7) if name in ('btree', 'rrt2000') else (2e6, 2e8))
print(f"TOTAL {time.time()-t00:.1f}s")
