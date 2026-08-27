"""I7-B phase 1: TK extraction, the Psi-identity, crude-cone TK<0 witnesses,
and the exact stage-level equivalence

    V_{t+1} - (1-q)^2 V_t  ==  Psi(y, h)   with  y = beta*d_t - Delta*1,
                                                h = high(E[t+1])

    Psi(y,h) = Ex - Slack
    Ex    = |M P y_-|^2 + 2<M^2 P y_-, z - nu h>,   z = P y
    Slack = <(z - nu h), M(m0 - M)(z - nu h)> + nu^2 |M h|^2
            + beta <h, (m0 - 2M + M^2) h>
(all D-inner products; M = Mm; P = D-orth projection off 1).

Also: TK = <M phih, M(vh - phih)> == -<P y_+, M^2 P y_->  (verify).
"""
import sys, json, time
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from i6b_class3 import (GenInst, hypercube, petersen, cycle, complete_bipartite,
                        rook, cocktail, circulant, connected)

def dotD(d, u, v):
    return sum(d[i] * u[i] * v[i] for i in range(len(u)))

def proj(d, vol, u):
    m = sum(d[i] * u[i] for i in range(len(u))) / vol
    return [x - m for x in u]

def psi_terms(I, y, h):
    """Exact Psi = Ex - Slack for graph instance I, free y (full vector),
    free h in 1^perp (h will be projected for safety)."""
    n, d, vol, be, nu, m0 = I.n, I.d, I.vol, I.beta, I.q/(1+I.q), I.m0
    h = proj(d, vol, h)
    z = proj(d, vol, y)
    ym = [max(-v, Fr(0)) if isinstance(v, Fr) else max(-v, 0.0) for v in y]
    Pym = proj(d, vol, ym)
    MPym = I.Mmv(Pym)
    M2Pym = I.Mmv(MPym)
    znh = [z[i] - nu * h[i] for i in range(n)]
    Ex = dotD(d, MPym, MPym) + 2 * dotD(d, M2Pym, znh)
    Mznh = I.Mmv(znh)
    Mh = I.Mmv(h)
    M2h = I.Mmv(Mh)
    Slack = (m0 * dotD(d, znh, Mznh) - dotD(d, Mznh, Mznh)
             + nu * nu * dotD(d, Mh, Mh)
             + be * (m0 * dotD(d, h, h) - 2 * dotD(d, h, Mh)
                     + dotD(d, Mh, Mh)))
    return Ex, Slack, Ex - Slack

def tk_of(I, y):
    """TK in both forms: code form and -<P y_+, M^2 P y_->."""
    n, d, vol = I.n, I.d, I.vol
    yp = [max(v, Fr(0)) if isinstance(v, Fr) else max(v, 0.0) for v in y]
    ym = [yp[i] - y[i] for i in range(n)]
    Pyp, Pym = proj(d, vol, yp), proj(d, vol, ym)
    MPyp = I.Mmv(Pyp)
    M2Pyp = I.Mmv(MPyp)
    return -dotD(d, Pym, M2Pyp)

GRAPHS = {
    'C6': (cycle(6), Fr(1, 10)),
    'Q4': (hypercube(4), Fr(1, 10)),
    'Pet': (petersen(), Fr(1, 10)),
}

def stage_verify(name, adj, q, seedkind='skew', T=14):
    """Run the actual recurrence; at every stage t>=1 verify:
       (A) TK(code) == -<P y_+, M^2 P y_->
       (B) Vn - (1-q)^2 V == Psi(y, h)  exactly."""
    n = len(adj)
    dmax = max(len(a) for a in adj)
    if seedkind == 'skew':
        s = [Fr(1, 2)] + [Fr(1, 2 * (n - 1))] * (n - 1)
    else:
        s = [Fr(1, n)] * n
    rho = min(s) / (2 * dmax)
    I = GenInst(adj, s, q, rho)
    if not (I.H0 and I.interior):
        print('%s: H0/interior fail, skip' % name); return
    recs, xs = I.run(T, diag=False)
    d, vol, be, nu = I.d, I.vol, I.beta, I.q / (1 + I.q)
    E = [[I.xstar[i] - xs[k][i] for i in range(n)] for k in range(len(xs))]
    okA = okB = okC = tot = 0
    tkvals = []
    for t in range(1, T - 1):
        rec = recs[t]
        dt, Delta, cls = rec['dt'], rec['Delta'], rec['cls']
        hm = proj(d, vol, E[t]); h = proj(d, vol, E[t + 1])
        hn = proj(d, vol, E[t + 2])
        y = [be * dt[i] - Delta for i in range(n)]
        # V forms
        def Vf(u, v):
            Mv = I.Mmv(v)
            return dotD(d, u, u) - (1 + be) * dotD(d, u, Mv) + be * dotD(d, v, Mv)
        V, Vn = Vf(h, hm), Vf(hn, h)
        # (A) TK two forms
        phi = [max(be * dt[i] - Delta, Fr(0)) for i in range(n)]
        phih = proj(d, vol, phi)
        co = [hm[i] - (1 + be) / (2 * be) * h[i] for i in range(n)]
        vh = [be * co[i] + nu * h[i] for i in range(n)]
        Mphi = I.Mmv(phih)
        TKcode = dotD(d, Mphi, I.Mmv(vh)) - dotD(d, Mphi, Mphi)
        TKnew = tk_of(I, y)
        okA += TKcode == TKnew
        # (B) Psi identity
        Ex, Sl, Psi = psi_terms(I, y, h)
        okB += (Vn - (1 - I.q) ** 2 * V) == Psi
        # (C) z = beta P d_t == beta (hm - h)
        z = proj(d, vol, [be * dt[i] for i in range(n)])
        okC += all(z[i] == be * (hm[i] - h[i]) for i in range(n))
        tot += 1
        if cls in 'PFC':
            tkvals.append((t, cls, float(TKnew), float(Psi)))
    print('%-6s word=%s  TK-eq %d/%d  Psi-id %d/%d  z-id %d/%d' %
          (name, ''.join(r['cls'] for r in recs)[:12], okA, tot, okB, tot,
           okC, tot))
    for t, cls, tk, ps in tkvals[:6]:
        print('    t=%-2d %s TK=%+.3e Psi=%+.3e' % (t, cls, tk, ps))
    return okA == tot and okB == tot and okC == tot

def crude_witness(name, adj, q):
    """(H-K)-violating pair -> crude-cone config with TK < 0; report Psi
    there too (with h = 0)."""
    n = len(adj)
    I = GenInst(adj, [Fr(1, n)] * n, q, Fr(1, 4 * n * n))
    d, vol, m0 = I.d, I.vol, I.m0
    # M^2 entries, find worst (i,j): (M^2)_{ij} vs m0^2 d_j / vol
    M2 = [[sum(I.Mm[i][k] * I.Mm[k][j] for k in range(n)) for j in range(n)]
          for i in range(n)]
    worst, wij = None, None
    for i in range(n):
        for j in range(n):
            if i == j: continue
            rat = M2[i][j] * vol / (m0 * m0 * d[j])
            if worst is None or rat > worst:
                worst, wij = rat, (i, j)
    i, j = wij
    print('%-6s worst (H-K) ratio = %.4f at pair %s (adjacent: %s)' %
          (name, float(worst), wij, j in adj[i]))
    if worst <= 1:
        return None
    # crude-cone stage: y = 1_i - tau 1_j ; scan tau
    best = None
    for tau_num in range(1, 401):
        tau = Fr(tau_num, 100)
        y = [Fr(0)] * n
        y[i] = Fr(1); y[j] = -tau
        tk = tk_of(I, y)
        Ex, Sl, Psi = psi_terms(I, y, [Fr(0)] * n)
        if best is None or tk < best[1]:
            best = (tau, tk, Psi)
    tau, tk, Psi = best
    print('        witness y = 1_%d - %s*1_%d :  TK = %s < 0;  Psi(h=0) = %.6f'
          % (i, tau, j, float(tk), float(Psi)))
    return (i, j, tau, tk, Psi)

if __name__ == '__main__':
    t0 = time.time()
    print('=== (A,B) stage-level identity verification (exact) ===')
    allok = True
    for nm, (adj, q) in GRAPHS.items():
        for sk in ('skew', 'unif'):
            r = stage_verify(nm + '-' + sk, adj, q, sk)
            allok = allok and bool(r)
    print('ALL IDENTITIES:', 'PASS' if allok else 'FAIL')
    print('\n=== crude-cone TK<0 witnesses on (H-K)-failing graphs ===')
    wit = {}
    for nm, (adj, q) in GRAPHS.items():
        wit[nm] = crude_witness(nm, adj, q)
    json.dump({k: (None if v is None else
                   [v[0], v[1], str(v[2]), str(v[3]), float(v[4])])
               for k, v in wit.items()},
              open('/home/claude/work/overnight/w7_windowed/i7b_witness.json',
                   'w'), indent=1, default=str)
    print('[%.1fs]' % (time.time() - t0))
