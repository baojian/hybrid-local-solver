"""I5-C main battery: exact runs, all cells, all variants."""
import sys, json, math, time
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from engine import Inst, path_graph, star_graph, complete_graph
from i3g_core import face_w_exact, run_exact
from i5c_core import run_i5c, face_mom
from i5c_run import analyse5, line5


def caterpillar(m, k):
    n = m + m * k
    adj = [[] for _ in range(n)]

    def ae(a, b):
        adj[a].append(b); adj[b].append(a)
    for i in range(m - 1):
        ae(i, i + 1)
    for i in range(m):
        for j in range(k):
            ae(i, m + i * k + j)
    return [sorted(a) for a in adj]


def btree(depth):
    n = 2 ** (depth + 1) - 1
    adj = [[] for _ in range(n)]
    for i in range(n):
        for c in (2 * i + 1, 2 * i + 2):
            if c < n:
                adj[i].append(c); adj[c].append(i)
    return [sorted(a) for a in adj]


def lock_params(I):
    """Oracle face-calibrated (qr, beta) of the LOCKED face S* (i4a probe)."""
    w, dv, lo, hi = face_w_exact(I.Qt, I.d, I.adj, list(I.Sstar), k=8)
    qr, be = face_mom(I, hi)
    return qr, be, lo, hi


results = {}
t00 = time.time()


def do(name, adj, seed, q, rho, T, variants, c9on=()):
    I = Inst(adj, seed, q, rho)
    qr_lk, be_lk, lo_lk, hi_lk = lock_params(I)
    print("\n=== %s  n=%d |S*|=%d q=%s rho=%s alpha=%s | S*: alpha_S in "
          "[%.6g, %.6g] (x%.3f) qr*=%s beta*=%.6f 1-q=%.6f 1-qr*=%.6f ==="
          % (name, I.n, len(I.Sstar), q, rho, I.alpha, float(lo_lk),
             float(hi_lk), float(lo_lk / I.alpha), qr_lk, float(be_lk),
             float(1 - I.q), float(1 - qr_lk)), flush=True)
    wc = {}
    rr = {}
    for v in variants:
        t0 = time.time()
        kw = dict(wcache=wc, c9=(v in c9on))
        if v == 'fmlock':
            kw.update(beta_fix=be_lk, qr_fix=qr_lk)
        o, wc = analyse5(I, T, v, **kw)
        o['secs'] = time.time() - t0
        print("  " + line5(o) + "  [%.0fs]" % o['secs'], flush=True)
        if o['c9']:
            print("    c9face: C3 %d/%d  C9 %d/%d (worstV=%s)  Vpos %d/%d"
                  % (*o['c9']['C3'], *o['c9']['C9'],
                     ('%.6f' % o['c9']['worstV'])
                     if o['c9']['worstV'] is not None else 'NA',
                     *o['c9']['Vpos']), flush=True)
        if o['retune']:
            print("    retune: " + " ".join(
                "t=%d %.4g->%.4g j=%.4g" % (rj['t'], rj['qr_old'],
                                            rj['qr_new'], rj['jump'])
                for rj in o['retune']), flush=True)
        rr[v] = o
    results[name] = dict(
        n=I.n, nS=len(I.Sstar), q=str(q), rho=str(rho),
        alpha=str(I.alpha), aS_lo=str(lo_lk), aS_hi=str(hi_lk),
        qr_lock=str(qr_lk), beta_lock=str(be_lk),
        runs={v: {kk: vv for kk, vv in o.items() if kk not in ('gam',)}
              for v, o in rr.items()})
    json.dump(results, open('/home/claude/work/overnight/w7_windowed/'
                            'i5c_results.json', 'w'), indent=1, default=str)
    return rr


FULL = ('base', 'face', 'fm', 'fmlock')

# ---------- the six i4a proper-face cells
do('P24 tuned', path_graph(24), [Fr(1)] + [Fr(0)] * 23, Fr(1, 32),
   Fr(65, 4096), 400, ('base', 'face', 'fm', 'fmlock', 'bm'),
   c9on=('fm', 'fmlock'))
do('P16 tuned', path_graph(16), [Fr(1)] + [Fr(0)] * 15, Fr(1, 24),
   Fr(1, 32), 250, FULL)
do('P20 tuned', path_graph(20), [Fr(1)] + [Fr(0)] * 19, Fr(1, 32),
   Fr(7, 256), 250, FULL)
do('P12 tuned', path_graph(12), [Fr(1)] + [Fr(0)] * 11, Fr(1, 20),
   Fr(5, 128), 200, FULL, c9on=('fm',))
do('cat5_2', caterpillar(5, 2), [Fr(1)] + [Fr(0)] * 14, Fr(1, 20),
   Fr(5, 128), 200, FULL)
do('S16 leaf', star_graph(16), [Fr(0), Fr(1)] + [Fr(0)] * 14, Fr(1, 20),
   Fr(5, 128), 150, FULL)

# ---------- new proper-face cells (screened: |S*| < n required)
print("\n\n#### screening new cells", flush=True)
cand = [
    ('P28 q32', path_graph(28), [Fr(1)] + [Fr(0)] * 27, Fr(1, 32),
     Fr(3, 256)),
    ('P18 q24', path_graph(18), [Fr(1)] + [Fr(0)] * 17, Fr(1, 24),
     Fr(11, 512)),
    ('cat4_3', caterpillar(4, 3), [Fr(1)] + [Fr(0)] * 15, Fr(1, 24),
     Fr(9, 256)),
    ('bt15 root', btree(3), [Fr(1)] + [Fr(0)] * 14, Fr(1, 20), Fr(3, 64)),
    ('bt15 leaf', btree(3), [Fr(0)] * 7 + [Fr(1)] + [Fr(0)] * 7, Fr(1, 20),
     Fr(5, 256)),
    ('S12 center', star_graph(12), [Fr(1)] + [Fr(0)] * 11, Fr(1, 16),
     Fr(1, 24)),
]
picked = []
for nm, adj, seed, q, rho in cand:
    try:
        I = Inst(adj, seed, q, rho)
    except AssertionError:
        print("  %-12s: bad params" % nm, flush=True)
        continue
    ok = 1 < len(I.Sstar) < I.n
    print("  %-12s n=%d |S*|=%d  proper=%s" % (nm, I.n, len(I.Sstar), ok),
          flush=True)
    if ok:
        picked.append((nm, adj, seed, q, rho))
for nm, adj, seed, q, rho in picked[:4]:
    do(nm, adj, seed, q, rho, 200, ('base', 'face', 'fm', 'fmlock'))

# ---------- K_n / interior-face regression: fm == base bit-identically
print("\n\n#### interior-face regression: fm == base bit-exactly", flush=True)
reg = []
for (nm, adj, seed, q, rho, T) in [
        ('K8 pulse', complete_graph(8),
         [Fr(363437, 651088)] + [Fr(41093, 651088)] * 7, Fr(1, 10),
         Fr(1, 112), 16),
        ('K2 n=100', complete_graph(2), [Fr(1, 2), Fr(1, 2)], Fr(1, 100),
         Fr(1, 16), 20),
        ('K16 unif', complete_graph(16), [Fr(1, 16)] * 16, Fr(1, 10),
         Fr(1, 480), 14),
        ('Q3 skew', [[1, 2, 4], [0, 3, 5], [0, 3, 6], [1, 2, 7],
                     [0, 5, 6], [1, 4, 7], [2, 4, 7], [3, 5, 6]],
         [Fr(1, 2)] + [Fr(1, 14)] * 7, Fr(1, 10), Fr(1, 336), 16)]:
    I = Inst(adj, seed, q, rho)
    ra = run_i5c(I, T, variant='base')
    rb = run_i5c(I, T, variant='fm')
    same = (len(ra) == len(rb)) and all(
        a['Delta'] == b['Delta'] and a['rh'] == b['rh'] and a['xn'] == b['xn']
        and a['beta'] == b['beta'] for a, b in zip(ra, rb))
    print("  %-10s n=%-3d |S*|=%-3d T=%d  fm==base: %s" %
          (nm, I.n, len(I.Sstar), T, same), flush=True)
    reg.append(dict(name=nm, n=I.n, identical=bool(same)))
results['regression_fm_eq_base'] = reg
json.dump(results, open('/home/claude/work/overnight/w7_windowed/'
                        'i5c_results.json', 'w'), indent=1, default=str)
print("\nTOTAL [%.0fs]" % (time.time() - t00), flush=True)
