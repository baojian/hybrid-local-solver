"""I7-B phase 5: COMPLETE orbit-reduced decision of sup Psi <= 0 on Q4
(3^16 = 43,046,721 sign assignments, reduced by Aut(Q4), |G| = 384),
plus exact verification of the master form

  Psi(y,h) = |M(b+w)|^2_D - m0 <b, Mb>_D - nu^2 |Mh|^2_D - beta <h, G h>_D
  b = Py - nu h,  w = P y_-,  G = m0 I - 2M + M^2.
"""
import sys, time, json, itertools
import numpy as np
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from i6b_class3 import GenInst, hypercube, petersen, cycle
from i7b_hunt import build, psi_star, QS_matrix
from i7b_decide import signspace_feasible

# ---------------------------------------------------------------- master form
def master_check():
    from i7b_tk import psi_terms, proj, dotD
    print('=== master-form verification (exact, random rational y,h) ===')
    rng = np.random.default_rng(5)
    for name, adj, q in [('C6', cycle(6), Fr(1, 4)), ('Pet', petersen(),
                          Fr(1, 10)), ('Q4', hypercube(4), Fr(1, 4))]:
        n = len(adj)
        I = GenInst(adj, [Fr(1, n)] * n, q, Fr(1, 8 * n * n))
        d, vol, be, m0 = I.d, I.vol, I.beta, I.m0
        nu = I.q / (1 + I.q)
        ok = 0
        for trial in range(6):
            y = [Fr(int(rng.integers(-40, 41)), 7) for _ in range(n)]
            h = proj(d, vol, [Fr(int(rng.integers(-40, 41)), 9)
                              for _ in range(n)])
            Ex, Sl, Psi = psi_terms(I, y, h)
            z = proj(d, vol, y)
            b = [z[i] - nu * h[i] for i in range(n)]
            ym = [max(-v, Fr(0)) for v in y]
            w = proj(d, vol, ym)
            bw = [b[i] + w[i] for i in range(n)]
            Mbw = I.Mmv(bw); Mb = I.Mmv(b); Mh = I.Mmv(h)
            MF = (dotD(d, Mbw, Mbw) - m0 * dotD(d, b, Mb)
                  - nu * nu * dotD(d, Mh, Mh)
                  - be * (m0 * dotD(d, h, h) - 2 * dotD(d, h, Mh)
                          + dotD(d, Mh, Mh)))
            ok += (MF == Psi)
        print('  %-4s master==Psi exact: %d/6' % (name, ok))

# ------------------------------------------------------------- Q4 group setup
def q4_group():
    perms = []
    bits = list(itertools.permutations(range(4)))
    for mask in range(16):
        for sig in bits:
            p = np.empty(16, dtype=np.int64)
            for v in range(16):
                u = v ^ mask
                w = 0
                for bpos in range(4):
                    if u >> bpos & 1:
                        w |= 1 << sig[bpos]
                p[v] = w
            perms.append(p)
    return perms          # p[v] = image of vertex v

def _digits(codes):
    x = codes.copy()
    D = np.empty((len(codes), 16), dtype=np.int64)
    for i in range(16):
        D[:, i] = x % 3
        x //= 3
    return D

def orbit_reps():
    perms = q4_group()
    inv = [np.argsort(p) for p in perms]
    # translations = identity bit-perm entries: indices mask*24
    inv_tr = [inv[m * 24] for m in range(16)]
    pow3 = (3 ** np.arange(16)).astype(np.int64)
    NTOT = 3 ** 16
    CH = 1 << 21
    t0 = time.time()
    stage1 = []
    for start in range(0, NTOT, CH):
        codes = np.arange(start, min(start + CH, NTOT), dtype=np.int64)
        D = _digits(codes)
        mn = codes.copy()
        for gi in inv_tr:
            np.minimum(mn, D[:, gi] @ pow3, out=mn)
        stage1.append(codes[mn == codes])
    s1 = np.concatenate(stage1)
    print('  stage1 (16 translations): %d survivors [%.0fs]' %
          (len(s1), time.time() - t0))
    D = _digits(s1)
    mn = s1.copy()
    for gi in inv:
        np.minimum(mn, D[:, gi] @ pow3, out=mn)
    reps = s1[mn == s1]
    print('  canonicalization done: %d orbit reps  [%.0fs]' %
          (len(reps), time.time() - t0))
    return reps

def decide_q4(q, reps, tol=1e-11):
    adj = hypercube(4)
    ctx = build(adj, q)
    n = 16
    pow3 = (3 ** np.arange(16)).astype(np.int64)
    QS_cache = {}
    n_mixed = n_poslam = 0
    worst_feas = -np.inf
    violations, near = [], []
    t0 = time.time()
    for ci, code in enumerate(reps):
        x = int(code)
        dg = []
        for i in range(16):
            dg.append(x % 3); x //= 3
        P = frozenset(i for i in range(16) if dg[i] == 1)
        N = frozenset(i for i in range(16) if dg[i] == 2)
        if not P or not N:
            continue
        n_mixed += 1
        if N not in QS_cache:
            if len(QS_cache) > 300000:
                QS_cache.clear()
            QS_cache[N] = QS_matrix(ctx, N)
        idx = sorted(P | N)
        B = QS_cache[N][np.ix_(idx, idx)]
        ev, V = np.linalg.eigh(B)
        if ev[-1] <= tol:
            continue
        pos = [k for k in range(len(ev)) if ev[k] > tol]
        # cluster by value
        used = set()
        for k in pos:
            if k in used:
                continue
            cols = [j for j in pos if abs(ev[j] - ev[k]) < 1e-8]
            used.update(cols)
            n_poslam += 1
            c = signspace_feasible(V[:, cols], P, N, idx)
            if c is not None:
                y = np.zeros(16)
                yr = V[:, cols] @ c
                for kk, i in enumerate(idx):
                    y[i] = yr[kk]
                tv = psi_star(ctx, y / np.linalg.norm(y))
                if tv > tol:
                    violations.append((sorted(P), sorted(N), float(ev[k]),
                                       float(tv), y.tolist()))
                else:
                    near.append((sorted(P), sorted(N), float(ev[k]),
                                 float(tv)))
                worst_feas = max(worst_feas, tv)
        if ci % 20000 == 0:
            sys.stdout.write('\r  q=%s decide %6d/%d mixed=%d poslam=%d '
                             'viol=%d [%.0fs]' %
                             (q, ci, len(reps), n_mixed, n_poslam,
                              len(violations), time.time() - t0))
            sys.stdout.flush()
    print('\r  Q4 q=%-8s mixed orbit pairs %7d  pos-lam %7d  '
          'violations %d  %s   [%.0fs]' %
          (q, n_mixed, n_poslam, len(violations),
           'SUP<=0' if not violations else 'VIOLATED', time.time() - t0))
    if near:
        print('     sign-feasible-but-true<=0 events: %d (max true %.2e)'
              % (len(near), max(t for *_, t in near)))
    if violations:
        for Pp, Nn, lam, tv, y in violations[:5]:
            print('     VIOL P=%s N=%s lam=%.3e true=%.3e' % (Pp, Nn, lam, tv))
    return dict(q=str(q), n_mixed=n_mixed, n_poslam=n_poslam,
                violations=violations, near=near[:20])

if __name__ == '__main__':
    master_check()
    reps = orbit_reps()
    np.save('/home/claude/work/overnight/w7_windowed/i7b_q4_reps.npy', reps)
    out = []
    for q in ('1/10', '1/4'):
        out.append(decide_q4(q, reps))
    json.dump(out, open('/home/claude/work/overnight/w7_windowed/'
                        'i7b_q4_decide.json', 'w'), indent=1, default=str)
