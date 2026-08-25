import json, sys
import numpy as np

OUT = '/home/claude/work/overnight/w6_incremental'
main = json.load(open(f'{OUT}/results_main.json'))
alph = json.load(open(f'{OUT}/results_alpha.json'))
diag = json.load(open(f'{OUT}/results_diag.json'))

BK = ['COLD-LU', 'CG-COLD', 'CG-WARM', 'INC-LDL', 'TREE-INC',
      'ORACLE-SDD', 'ORACLE-INC']
GR = ['path', 'caterpillar', 'spider', 'btree', 'decoy_hub', 'theta', 'grid']


def tot(r, b):
    v = r['backends'].get(b)
    return v['meter']['total'] if v else None


def fit(ks, ws):
    ks, ws = np.array(ks, float), np.array(ws, float)
    if len(ks) < 2:
        return float('nan')
    A = np.vstack([ks, np.ones_like(ks)]).T
    sl, _ = np.linalg.lstsq(A, np.log2(ws), rcond=None)[0]
    return sl


print('=' * 100)
print('TABLE 1: E(eps), |S|, vol, meanT  (main sweep)  -- saturated points marked *')
print('=' * 100)
for g in GR:
    for a in (1e-2, 1e-4):
        rows = [r for r in main if r['graph'] == g and r['alpha'] == a]
        rows.sort(key=lambda r: r['k'])
        # saturation: |S| unchanged from previous eps
        sat = [False] + [rows[i]['S'] == rows[i-1]['S']
                         for i in range(1, len(rows))]
        es = ' '.join(f"{r['E']}{'*' if s else ''}" for r, s in zip(rows, sat))
        Ss = ' '.join(str(r['S']) for r in rows)
        mT = ' '.join(f"{r['meanT']:.0f}" for r in rows)
        # growth exponents over non-saturated pts
        ks = [r['k'] for r, s in zip(rows, sat) if not s]
        qE = fit(ks, [r['E'] for r, s in zip(rows, sat) if not s])
        qV = fit(ks, [r['volS'] for r, s in zip(rows, sat) if not s])
        print(f"{g:12s} a={a:g}  E: {es}")
        print(f"{'':12s}         |S|: {Ss}   meanT: {mT}   "
              f"E~eps^-{qE:.2f} vol~eps^-{qV:.2f}  "
              f"E/|S*|={rows[-1]['E']/rows[-1]['S']:.2f}  "
              f"volS*(gam*eps)/1={rows[-1]['volS']*0.5*2**-rows[-1]['k']:.3f}")

print()
print('=' * 100)
print('TABLE 2: fitted eps-exponents q (W ~ eps^-q), non-saturated points only')
print('=' * 100)
hdr = f"{'graph':12s} {'alpha':8s}" + ''.join(f'{b:>11s}' for b in BK)
print(hdr)
for g in GR:
    for a in (1e-2, 1e-4):
        rows = [r for r in main if r['graph'] == g and r['alpha'] == a]
        rows.sort(key=lambda r: r['k'])
        sat = [False] + [rows[i]['S'] == rows[i-1]['S']
                         for i in range(1, len(rows))]
        keep = [r for r, s in zip(rows, sat) if not s]
        line = f"{g:12s} {a:<8g}"
        for b in BK:
            ws = [tot(r, b) for r in keep]
            ks = [r['k'] for r, w in zip(keep, ws) if w]
            ws = [w for w in ws if w]
            line += f"{fit(ks, ws):11.2f}" if len(ws) >= 2 else f"{'--':>11s}"
        print(line + f"   ({len(keep)} pts)")

print()
print('=' * 100)
print('TABLE 3: totals at finest non-saturated eps + PRIZE SIZE')
print('=' * 100)
print(f"{'graph':12s} {'alpha':8s} {'eps':7s} {'E':>5s} {'volS':>6s} "
      f"{'sumVol/EV':>9s} {'COLD-LU':>10s} {'CG-WARM':>10s} {'INC-LDL':>10s} "
      f"{'TREE-INC':>10s} {'OR-SDD':>10s} {'OR-INC':>9s} {'PRIZE':>7s} "
      f"{'bestreal/vol':>12s}")
for g in GR:
    for a in (1e-2, 1e-4):
        rows = [r for r in main if r['graph'] == g and r['alpha'] == a]
        rows.sort(key=lambda r: r['k'])
        sat = [False] + [rows[i]['S'] == rows[i-1]['S']
                         for i in range(1, len(rows))]
        keep = [r for r, s in zip(rows, sat) if not s]
        r = keep[-1]
        pr = tot(r, 'ORACLE-SDD') / tot(r, 'ORACLE-INC')
        best = min(w for w in [tot(r, b) for b in
                               ('COLD-LU', 'CG-WARM', 'INC-LDL', 'TREE-INC')]
                   if w)
        sv = r['sum_volSt'] / (r['E'] * r['volS'])
        ti = tot(r, 'TREE-INC')
        print(f"{g:12s} {a:<8g} 2^-{r['k']:<4d} {r['E']:>5d} {r['volS']:>6d} "
              f"{sv:>9.2f} {tot(r,'COLD-LU'):>10d} {tot(r,'CG-WARM'):>10d} "
              f"{tot(r,'INC-LDL'):>10d} "
              f"{ti if ti else 0:>10d} "
              f"{tot(r,'ORACLE-SDD'):>10.0f} {tot(r,'ORACLE-INC'):>9.0f} "
              f"{pr:>7.1f} {best/r['volS']:>12.1f}")

print()
print('=' * 100)
print('TABLE 4: warm-start value law (pooled per-round samples, main sweep)')
print('=' * 100)
samp = []
for r in main:
    bw, bc = r['backends'].get('CG-WARM'), r['backends'].get('CG-COLD')
    if not bw or 'iters' not in bw:
        continue
    for iw, ic, ri, r0w, r0c in zip(bw['iters'], bc['iters'], bw['rel_inc'],
                                    bw['r0'], bc['r0']):
        if ic > 0:
            tol = 0.10 * r['alpha'] * r['eps']
            samp.append((iw, ic, ri, r0w / tol, r0c / tol,
                         r['graph'], r['alpha']))
print(f'pooled rounds: {len(samp)}')
bins = [0, 1e-4, 1e-3, 1e-2, 0.1, 0.3, 1.0, 10]
print(f"{'rel_inc bin':>18s} {'n':>6s} {'med it_warm':>12s} "
      f"{'med it_cold':>12s} {'med ratio c/w':>14s}")
for lo, hi in zip(bins[:-1], bins[1:]):
    ss = [s for s in samp if lo <= s[2] < hi]
    if not ss:
        continue
    iw = np.median([s[0] for s in ss]); ic = np.median([s[1] for s in ss])
    rat = np.median([s[1] / max(s[0], 1) for s in ss])
    print(f"[{lo:8.0e},{hi:8.0e}) {len(ss):>6d} {iw:>12.1f} {ic:>12.1f} "
          f"{rat:>14.2f}")
# log-ratio law: iters_warm/iters_cold vs log(r0w/tol)/log(r0c/tol)
xs, ys = [], []
for iw, ic, ri, aw, ac, g, a in samp:
    if iw > 3 and ic > 3 and aw > 1.5 and ac > 1.5:
        xs.append(np.log(aw) / np.log(ac)); ys.append(iw / ic)
xs, ys = np.array(xs), np.array(ys)
if len(xs):
    c = np.corrcoef(xs, ys)[0, 1]
    sl = np.polyfit(xs, ys, 1)
    print(f"log-ratio law: iters_w/iters_c vs ln(r0w/tol)/ln(r0c/tol): "
          f"corr={c:.3f} slope={sl[0]:.2f} intercept={sl[1]:.2f} "
          f"(n={len(xs)})")

print()
print('=' * 100)
print('TABLE 5: alpha sweep at eps=2^-8')
print('=' * 100)
print(f"{'graph':8s} {'alpha':7s} {'E':>5s} {'|S|':>5s} {'volS':>6s} "
      f"{'it_w':>7s} {'it_c':>7s} {'up_mean':>8s} {'W_cgw':>10s} "
      f"{'W_cold':>10s} {'W_incldl':>10s} {'W_tree':>10s} {'W_orsdd':>10s} "
      f"{'W_orinc':>9s}")
for g in ('path', 'btree', 'grid'):
    rows = [r for r in alph if r['graph'] == g]
    rows.sort(key=lambda r: r['j'])
    for r in rows:
        bw = r['backends']['CG-WARM']; bc = r['backends']['CG-COLD']
        ti = r['backends'].get('TREE-INC', {})
        up = ti.get('up_mean', float('nan'))
        tt = tot(r, 'TREE-INC')
        print(f"{g:8s} 2^-{r['j']:<4d} {r['E']:>5d} {r['S']:>5d} "
              f"{r['volS']:>6d} {np.mean(bw['iters']):>7.1f} "
              f"{np.mean(bc['iters']):>7.1f} {up:>8.1f} "
              f"{tot(r,'CG-WARM'):>10d} {tot(r,'COLD-LU'):>10d} "
              f"{tot(r,'INC-LDL'):>10d} {tt if tt else 0:>10d} "
              f"{tot(r,'ORACLE-SDD'):>10.0f} {tot(r,'ORACLE-INC'):>9.0f}")
    # alpha exponents (drop saturated |S| repeats)
    keep = []
    for i, r in enumerate(rows):
        if i == 0 or r['S'] != rows[i-1]['S']:
            keep.append(r)
    js = [r['j'] for r in keep]
    for lab, arr in [('it_cold', [np.mean(r['backends']['CG-COLD']['iters'])
                                  for r in keep]),
                     ('it_warm', [np.mean(r['backends']['CG-WARM']['iters'])
                                  for r in keep]),
                     ('up_mean', [r['backends'].get('TREE-INC', {})
                                  .get('up_mean') for r in keep])]:
        if all(v for v in arr):
            print(f"   {g} {lab} ~ alpha^-{fit(js, arr):.2f}")

print()
print('=' * 100)
print('TABLE 6: diagonal regime alpha = eps (the 1/eps^2 shape test)')
print('=' * 100)
for g in ('path', 'caterpillar'):
    rows = [r for r in diag if r['graph'] == g]
    rows.sort(key=lambda r: r['k'])
    print(f"{g}: k, E, volS, then totals")
    for r in rows:
        ti = tot(r, 'TREE-INC')
        print(f"  2^-{r['k']:<3d} E={r['E']:>4d} vol={r['volS']:>5d} "
              f"COLD={tot(r,'COLD-LU'):>8d} CGW={tot(r,'CG-WARM'):>9d} "
              f"INCLDL={tot(r,'INC-LDL'):>7d} TREE={ti:>8d} "
              f"ORSDD={tot(r,'ORACLE-SDD'):>9.0f} "
              f"ORINC={tot(r,'ORACLE-INC'):>7.0f}")
    ks = [r['k'] for r in rows]
    line = '  exponents (W ~ eps^-q): '
    for b in BK:
        ws = [tot(r, b) for r in rows]
        if all(ws):
            line += f"{b}:{fit(ks, ws):.2f}  "
    print(line)
    print(f"  E ~ eps^-{fit(ks, [r['E'] for r in rows]):.2f}, "
          f"vol ~ eps^-{fit(ks, [r['volS'] for r in rows]):.2f}")

print()
print('=' * 100)
print('TABLE 7: INC-LDL structure detail (finest non-sat eps, both alphas)')
print('=' * 100)
print(f"{'graph':12s} {'alpha':8s} {'volS':>6s} {'nnzL':>9s} {'append':>9s} "
      f"{'gate':>9s} {'lazygate':>9s} {'maxD':>6s} {'miss':>5s} "
      f"{'appd/vol':>8s} {'gate/vol':>8s}")
for g in GR:
    for a in (1e-2, 1e-4):
        rows = [r for r in main if r['graph'] == g and r['alpha'] == a]
        rows.sort(key=lambda r: r['k'])
        sat = [False] + [rows[i]['S'] == rows[i-1]['S']
                         for i in range(1, len(rows))]
        keep = [r for r, s in zip(rows, sat) if not s]
        r = keep[-1]
        b = r['backends']['INC-LDL']
        if b.get('capped'):
            print(f"{g:12s} {a:<8g} CAPPED"); continue
        print(f"{g:12s} {a:<8g} {r['volS']:>6d} {b['nnzL']:>9d} "
              f"{b['append_total']:>9d} {b['gate_total']:>9d} "
              f"{b['lazy_gate_total']:>9d} {b['gate_maxD']:>6d} "
              f"{b['lazy_miss']:>5d} {b['append_total']/r['volS']:>8.1f} "
              f"{b['gate_total']/r['volS']:>8.1f}")

print()
print('=' * 100)
print('TABLE 8: outer ledger (repeated boundary scans) share, finest eps')
print('=' * 100)
for g in GR:
    for a in (1e-2, 1e-4):
        rows = [r for r in main if r['graph'] == g and r['alpha'] == a]
        rows.sort(key=lambda r: r['k'])
        r = rows[-1]
        o = r.get('outer')
        if o:
            print(f"{g:12s} a={a:<8g} outer={o['total']:>9d} "
                  f"C_adj={o['C_adj']:>7d} R_adj={o['R_adj']:>8d} "
                  f"C_rec={o['C_rec']:>8d}  R_adj/vol={o['R_adj']/r['volS']:.1f}")

# btree CG puzzle check
print()
r = [x for x in main if x['graph'] == 'btree' and x['alpha'] == 1e-4
     and x['k'] == 10][0]
bw = r['backends']['CG-WARM']; bc = r['backends']['CG-COLD']
print('btree a=1e-4 eps=2^-10 per-round iters warm:', bw['iters'])
print('                       per-round iters cold:', bc['iters'])
print('                       rel_inc:', [f'{v:.2g}' for v in bw['rel_inc']])
