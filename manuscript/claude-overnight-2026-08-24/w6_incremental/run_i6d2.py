"""I6-D part 2: (a) ell*(C) scaling of the tree path-end adversary;
(b) re-run the 5 scaling series + tree zoo with the FINAL rule (HDynTreeFW,
full-walk sizes, hysteresis 2), lazy variant alongside for comparison."""
import sys, math, time, json
import numpy as np

sys.path.insert(0, '/home/claude/work/overnight/lib')
sys.path.insert(0, '/home/claude/work/overnight/w6_incremental')
from model import Model
from meter import Meter
import core, zoo, i2b
import dyn_ldl2
from i6d_amort import HDynTreeFW, replay_cls

OUT = '/home/claude/work/overnight/w6_incremental/res_i6d2.json'
res = {'cert': [], 'series': [], 'zoo': []}
t00 = time.time()

# ---------------- (a) ell*(C) for C < 2 on trees
print('== cert: ell*(C) on trees (path-end adversary) ==', flush=True)
for a in [2.0 ** -4, 2.0 ** -6, 2.0 ** -8, 2.0 ** -10, 2.0 ** -12]:
    lam = (1 - math.sqrt(a)) / (1 + math.sqrt(a))
    Lmax = int(max(40, 12.0 / math.sqrt(a)))
    m = 50
    nlong = m + 6 * Lmax
    padj = {u: sorted({u - 1, u + 1} & set(range(nlong)))
            for u in range(nlong)}
    mo_l = Model(padj, a, 0)
    idx = np.arange(m)
    Qs = mo_l.Q[idx][:, idx].toarray()
    xh = np.linalg.solve(Qs, mo_l.b[idx])
    xl = np.zeros(nlong); xl[:m] = xh
    el = mo_l.semantic_err(xl)
    Cs = [1.1, 1.25, 1.5, 1.75, 2.0]
    ells = {}
    for ell in range(1, 4 * Lmax):
        ns = m + ell
        adx = {u: sorted({u - 1, u + 1} & set(range(ns))) for u in range(ns)}
        mo_s = Model(adx, a, 0)
        xs = np.zeros(ns); xs[:m] = xh
        r = mo_s.semantic_err(xs) / el
        for C in Cs:
            if C not in ells and r <= C:
                ells[C] = ell
        if len(ells) == len(Cs):
            break
    row = dict(alpha=a, lam=lam,
               ell=[(C, ells.get(C), (ells.get(C, 0)) * math.sqrt(a),
                     1 + math.log(1.0 / (C - 1)) / (2 * math.log(1 / lam))
                     if C > 1 else None) for C in Cs])
    res['cert'].append(row)
    print(f"  a=2^{int(math.log2(a))}: " + '  '.join(
        f"C={C}: ell*={e} (elle*sqrt a={s:.2f}, pred {p:.1f})"
        for C, e, s, p in row['ell']), flush=True)

# ---------------- (b) scaling series + zoo with the final rule
def hrun(mo, eps, tr, tag, fam):
    volS = tr['rounds'][-1]['volS']
    S = len(tr['S'])
    lg = math.log2(max(volS, 4))
    row = dict(tag=tag, family=fam, alpha=mo.alpha, eps=eps, S=S, volS=volS)
    for name, cls in [('FW', HDynTreeFW), ('LAZY', dyn_ldl2.HDynTree)]:
        d = replay_cls(mo, tr, cls)
        tot = d['meter']['total']
        row[name] = dict(W=tot, Wvol=tot / volS, Wvlog2=tot / (volS * lg * lg),
                         lev_mean=d['lev_mean'], lev_max=d['lev_max'],
                         swaps=d['swaps'], moved=d['swap_moved'],
                         mv_S=d['swap_moved'] / S, cert=d['cert'],
                         sem=d['sem'])
    f, z = row['FW'], row['LAZY']
    print(f"[{time.time()-t00:5.0f}s] {tag:24s} a=2^{int(math.log2(mo.alpha))}"
          f" eps=2^{int(math.log2(eps))} S={S:5d} vol={volS:6d} | FW W/vol="
          f"{f['Wvol']:7.1f} W/(vol lg^2)={f['Wvlog2']:5.2f} lev="
          f"{f['lev_mean']:.2f}/{f['lev_max']} sw={f['swaps']:3d} mv/S="
          f"{f['mv_S']:.3f} | LAZY W/vol={z['Wvol']:7.1f} "
          f"sw={z['swaps']:3d} mv/S={z['mv_S']:.3f}", flush=True)
    return row


def series(adj, seed, a, tag, fam, lo=200, hi=9000, tlimit=100):
    t0 = time.time()
    mo = Model(adj, a, seed)
    prev = -1
    for k in range(2, 40):
        if time.time() - t0 > tlimit:
            break
        tr = core.grow_trace(mo, 2.0 ** -k, keep_Q=False)
        sz = len(tr['S'])
        if sz == prev or sz < lo:
            prev = sz; continue
        if sz > hi:
            break
        prev = sz
        res['series'].append(hrun(mo, 2.0 ** -k, tr, tag, fam))
        json.dump(res, open(OUT, 'w'))


print('== scaling series (final rule) ==', flush=True)
for B, a in [(512, 2.0 ** -14), (512, 2.0 ** -10), (32, 2.0 ** -14)]:
    T = max(2, int(round(1.0 / np.sqrt(a))))
    adj, s = i2b.comb(B, T)
    series(adj, s, a, f'combscale(B={B},T={T})', 'comb', tlimit=75)
adjc, sc = zoo.caterpillar(6000, 1)
series(adjc, sc, 2.0 ** -14, 'catscale', 'caterpillar', tlimit=75)
adjp, sp = zoo.path(12000)
series(adjp, sp, 2.0 ** -14, 'pathscale', 'path', tlimit=75)

print('== tree zoo (final rule) ==', flush=True)
ALPHAS = [2.0 ** -6, 2.0 ** -10, 2.0 ** -14]
FAM = [('path', lambda: zoo.path(8000), ALPHAS),
       ('caterpillar', lambda: zoo.caterpillar(4000, 1), ALPHAS),
       ('spider', lambda: zoo.spider(8, 800), ALPHAS),
       ('btree', lambda: zoo.binary_tree(12), [2.0 ** -10]),
       ('rrt2000', lambda: i2b.rrt(2000, 7), ALPHAS)]
for name, fn, als in FAM:
    adj, s = fn()
    for a in als:
        mo = Model(adj, a, s)
        eps, tr = i2b.tune_eps_trace(mo, 2500, keep_Q=False)
        res['zoo'].append(hrun(mo, eps, tr, name, name))
        json.dump(res, open(OUT, 'w'))

# constants summary over everything with the FW rule
allrows = res['series'] + res['zoo']
c2 = [r['FW']['Wvlog2'] for r in allrows]
mv = [r['FW']['mv_S'] for r in allrows]
print(f"\nFW over {len(allrows)} configs: W/(vol lg^2 vol) in "
      f"[{min(c2):.2f}, {max(c2):.2f}] median {sorted(c2)[len(c2)//2]:.2f}; "
      f"mv/S max {max(mv):.3f}; certified {len(allrows)}/{len(allrows)}",
      flush=True)
res['summary'] = dict(n=len(allrows), c2min=min(c2), c2max=max(c2),
                      c2med=sorted(c2)[len(c2) // 2], mvmax=max(mv))
json.dump(res, open(OUT, 'w'))
print(f"TOTAL {time.time()-t00:.1f}s -> {OUT}", flush=True)
