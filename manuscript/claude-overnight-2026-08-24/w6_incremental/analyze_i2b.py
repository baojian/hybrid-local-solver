"""I2-B analysis: W/vol tables + fitted exponents W ~ vol^q per backend."""
import json, math, sys
import numpy as np

R = json.load(open('/home/claude/work/overnight/w6_incremental/res_final.json'))
BK = ['COLD-LU', 'INC-LDL', 'TREE-INC', 'SEG-LDL', 'HSEG-LDL',
      'ORACLE-SDD', 'ORACLE-INC']


def W(r, k):
    v = r['bk'].get(k)
    if not v or 'error' in v:
        return None
    if v.get('capped'):
        return None
    return v.get('total', v.get('Wvol', 0) * r['volS'])


print("=" * 108)
print("A. COMB MATRIX  (W / vol(S*), eps tuned so |S*| <= 2500)")
print("=" * 108)
print(f"{'B':>4} {'T':>4} {'alpha':>7} {'eps':>6} {'|S*|':>6} {'vol':>6} "
      f"{'E':>5} | " + " ".join(f"{k:>10}" for k in BK[:5]))
for r in R:
    if r.get('kind') != 'matrix':
        continue
    row = []
    for k in BK[:5]:
        v = r['bk'].get(k)
        if not v or 'error' in v:
            row.append(f"{'--':>10}")
        elif v.get('capped'):
            row.append(f"{'>' + str(int(v['total'] / r['volS'])):>10}")
        else:
            row.append(f"{v['Wvol']:10.1f}")
    print(f"{r['Bbone']:>4} {r['T']:>4} 2^{int(math.log2(r['alpha'])):>5} "
          f"2^{int(math.log2(r['eps'])):>4} {r['S']:>6} {r['volS']:>6} "
          f"{r['E']:>5} | " + " ".join(row))

print()
print("=" * 108)
print("B. SCALING FITS   W ~ C * vol^q   (log-log LS over each series)")
print("=" * 108)
tags = []
for r in R:
    if r.get('kind') == 'scale' and r['tag'] not in tags:
        tags.append(r['tag'])
print(f"{'series':>26} {'alpha':>7} {'#pts':>5} {'vol range':>14} | "
      + " ".join(f"{k:>16}" for k in BK[:5]))
for t in tags:
    rs = [r for r in R if r.get('tag') == t and r.get('kind') == 'scale']
    if len(rs) < 3:
        continue
    vols = np.array([r['volS'] for r in rs], float)
    cells = []
    for k in BK[:5]:
        ws = [W(r, k) for r in rs]
        ok = [i for i, w in enumerate(ws) if w]
        if len(ok) < 3:
            cells.append(f"{'capped/--':>16}")
            continue
        x = np.log(vols[ok]); y = np.log(np.array([ws[i] for i in ok]))
        q, c = np.polyfit(x, y, 1)
        cells.append(f"q={q:5.2f} C={math.exp(c):7.1f}".rjust(16))
    print(f"{t:>26} 2^{int(math.log2(rs[0]['alpha'])):>5} {len(rs):>5} "
          f"{int(vols.min()):>6}-{int(vols.max()):<7} | " + " ".join(cells))

print()
print("=" * 108)
print("C. TREE ZOO  (W / vol(S*))     [theta is NOT a tree: tree backends N/A]")
print("=" * 108)
print(f"{'family':>13} {'alpha':>7} {'|S*|':>6} {'vol':>6} {'E':>5} | "
      + " ".join(f"{k:>10}" for k in BK))
for r in R:
    if r.get('kind') != 'zoo':
        continue
    row = []
    for k in BK:
        v = r['bk'].get(k)
        if not v or 'error' in v:
            row.append(f"{'--':>10}")
        elif v.get('capped'):
            row.append(f"{'>' + str(int(v['total'] / r['volS'])):>10}")
        else:
            row.append(f"{v.get('total', v.get('Wvol', 0) * r['volS']) / r['volS']:10.1f}")
    print(f"{r['family']:>13} 2^{int(math.log2(r['alpha'])):>5} {r['S']:>6} "
          f"{r['volS']:>6} {r['E']:>5} | " + " ".join(row))

print()
print("=" * 108)
print("D. HSEG-LDL alpha-stability of the constant C = W/vol (zoo + matrix)")
print("=" * 108)
fam = {}
for r in R:
    v = r['bk'].get('HSEG-LDL')
    if not v or 'error' in v:
        continue
    key = r['tag']
    fam.setdefault(key, {})[int(math.log2(r['alpha']))] = (
        v['Wvol'], v['lev_mean'], v['lev_max'], v['swaps'],
        v['swap_moved'] / max(r['S'], 1))
for key, d in fam.items():
    if len(d) < 2:
        continue
    ws = [d[a][0] for a in sorted(d)]
    print(f"{key:>26} | " + "  ".join(
        f"a=2^{a}: {d[a][0]:7.1f} (lev {d[a][1]:.2f}/{d[a][2]}, sw {d[a][3]},"
        f" mv/S {d[a][4]:.2f})" for a in sorted(d, reverse=True)))
    print(f"{'':>26}   spread max/min = {max(ws)/min(ws):.2f}")

print()
print("=" * 108)
print("E. certificates (max over all configs)")
print("=" * 108)
for k in BK[:5]:
    cs = [r['bk'][k].get('cert', 0) for r in R
          if k in r['bk'] and 'cert' in r['bk'][k]]
    ss = [r['bk'][k].get('sem', 0) for r in R
          if k in r['bk'] and 'sem' in r['bk'][k]]
    ve = [r['bk'][k].get('verr', 0) for r in R
          if k in r['bk'] and 'verr' in r['bk'][k]]
    eps = [r['eps'] for r in R if k in r['bk'] and 'sem' in r['bk'][k]]
    if not cs:
        continue
    marg = min((e - s) for e, s in zip(eps, ss))
    print(f"{k:>10}: n={len(cs):3d}  max cert/(alpha*eps) ratio ok, "
          f"max sem={max(ss):.3e}, min(eps-sem)={marg:.3e}, "
          f"max query relerr={max(ve) if ve else 0:.2e}")
