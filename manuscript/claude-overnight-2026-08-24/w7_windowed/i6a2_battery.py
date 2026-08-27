"""I6-A2: spectral/modal route to the never-triggering lemma -- exact battery.

Reformulation (proved in the finding; verified exactly here):
  Y_t := ct - Qt x_t   (full-space lower residual at the STATE)
  u_t := (1+beta_t) Y_t - beta_t Y_{t-1}      (then zeta(a_t) = u_t exactly)
  TRIGGER(t) fires  <=>  min_{i in S_t = supp(a_t)} u_{t,i} < 0.
  On N stages:  Y_{t+1}|_P = kappa D (x_{t+1} - a_t)|_P = Mm'_P u_t^ext|_P,
                Y_{t+1}|_{off P} <= -kappa d_i a_{t,i} <= 0,
  with P = supp(x_{t+1}), Mm'_P = kappa D_P (Qt_P + kappa D_P)^{-1} >= 0.

Checks per stage (EXACT Fractions unless noted):
  T0   (Delta>0) == (min_{S} u_t < 0)  and spot equality zeta(a)=u
  CA   Y_t >= 0 on S_t;  CAoff: Y_t <= 0 off supp(x_t)
  CB1  Y_t >= (1-qr_t) Y_{t-1}       on S_t   (componentwise floor, strong)
  CB2  Y_t >= ((1-qr_t)/2) Y_{t-1}   on S_t   (floor at sigma=beta/(1+beta))
  CC   u_t >= 0 on S_t   (never-trigger, direct)
  CJ   u_t >= 0 on S_{t+1} = supp(x_{t+1})  (incoming-face margin)
  CG   Y_{t+1} == kappa D (xn - ah) on supp(xn)   (dynamics identity, N stages)
  CNEW j in S_{t+1}\\S_t: Y_{t,j} <= 0 and u_{t+1,j} > 0 (activation lemma)
Per face (exact): inertia n_od := #{eigs of M_S <= crit}, crit = kap qr^2/(1-qr^2)
  ((H-sep) <=> n_od = 1 <=> s_2 <= (1-qr)^2); connectivity.
Per stage (float, Measured): w^(8)-split L=<w,Y>/||w||_D^2 (*-geometry:
  psi = D w), h = Y - L psi, ||h||_*, V-form, certificate
  R_t = d_max C_S V_t / (dn_S (beta m_psi L_{t-1})^2), t_cert.
"""
import sys, json, math, time
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from engine import Inst, path_graph, star_graph, _gauss
from i3g_core import face_w_exact, components
from i5c_core import run_i5c
import numpy as np

OUT = '/home/claude/work/overnight/w7_windowed/i6a2_results.json'


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


def Yvec(I, x):
    """ct - Qt x, full vector, exact, sparse mult."""
    n = I.n
    out = []
    for i in range(n):
        s = I.Qt[i][i] * x[i]
        for j in I.adj[i]:
            if x[j]:
                s += I.Qt[i][j] * x[j]
        out.append(I.ct[i] - s)
    return out


def inertia_below(I, S, crit):
    """Exact count of eigenvalues of M_S = D_S^{-1} Qt_S that are <= crit
    == number of nonpositive eigenvalues of A = Qt_S - crit*D_S (sym).
    Symmetric rational Gaussian elimination with diagonal pivoting;
    2x2 block pivots if needed. Returns (neg, zero, pos)."""
    idx = list(S)
    m = len(idx)
    A = [[I.Qt[a][b] - (crit * I.d[a] if a == b else 0) for b in idx]
         for a in idx]
    # relabel to local
    A = [[A[i][j] for j in range(m)] for i in range(m)]
    neg = zer = pos = 0
    act = list(range(m))
    while act:
        # find nonzero diagonal pivot
        p = next((i for i in act if A[i][i] != 0), None)
        if p is not None:
            piv = A[p][p]
            if piv > 0:
                pos += 1
            else:
                neg += 1
            act.remove(p)
            for i in act:
                if A[i][p] != 0:
                    f = A[i][p] / piv
                    for j in act:
                        A[i][j] -= f * A[p][j]
                    A[i][p] = Fr(0)
            for j in act:
                A[p][j] = Fr(0)
            continue
        # all diagonal zero: find off-diagonal nonzero -> 2x2 block (one +, one -)
        found = None
        for i in act:
            for j in act:
                if i != j and A[i][j] != 0:
                    found = (i, j)
                    break
            if found:
                break
        if not found:
            zer += len(act)
            break
        i0, j0 = found
        pos += 1
        neg += 1
        b = A[i0][j0]
        act.remove(i0)
        act.remove(j0)
        for r in act:
            # eliminate using the 2x2 block [[0,b],[b,0]]
            ci, cj = A[r][i0], A[r][j0]
            if ci == 0 and cj == 0:
                continue
            # x solves block * x = (ci, cj):  x = (cj/b, ci/b)
            xi, xj = cj / b, ci / b
            for c in act:
                A[r][c] -= xi * A[i0][c] + xj * A[j0][c]
        for c in act:
            A[i0][c] = A[j0][c] = Fr(0)
    return neg, zer, pos


def face_info(I, S, qr, ub, wS):
    """Per-face spectral data. n_od exact; floats Measured."""
    idx = list(S)
    m = len(idx)
    comps = components(I.adj, idx)
    kap = I.kappa
    info = dict(size=m, ncomp=len(comps), qr=float(qr), ub=float(ub))
    if qr >= 1:
        info.update(beta0=True, n_od=m, crit=None)
        return info
    crit = kap * qr * qr / (1 - qr * qr)
    neg, zer, pos = inertia_below(I, idx, crit)
    info['n_od'] = neg + zer          # eigs <= crit
    info['n_od_strict'] = neg
    info['crit'] = float(crit)
    # floats
    D = np.array([float(I.d[i]) for i in idx])
    Q = np.array([[float(I.Qt[a][b]) for b in idx] for a in idx])
    Ms = Q / D[:, None]
    ev = np.sort(np.linalg.eigvals(Ms).real)
    be = float((1 - qr) / (1 + qr))
    info['lam'] = [float(ev[0]), float(ev[1]) if m > 1 else None,
                   float(ev[-1])]
    if m > 1:
        m2 = float(kap) / (float(kap) + ev[1])
        info['s2'] = be * m2
        info['s2_ok'] = bool(be * m2 <= float((1 - qr) ** 2))
    info['one_minus_qr_sq'] = float((1 - qr) ** 2)
    w = np.array([float(wS[i]) for i in idx])
    info['spread'] = float(w.max() / w.min())
    info['m_psi'] = float(np.min(np.sqrt(D) * w))     # min_i sqrt(d_i) w_i
    info['d_max'] = float(D.max())
    return info


def run_cell(name, adj, seed, q, rho, T):
    t0 = time.time()
    I = Inst(adj, seed, q, rho)
    recs = run_i5c(I, T, variant='fm')
    n = I.n
    kap = I.kappa
    # per-stage Y
    Ys = [Yvec(I, r['x']) for r in recs]
    Ys.append(Yvec(I, recs[-1]['xn']))
    res = dict(name=name, n=n, nS=len(I.Sstar), T=len(recs),
               secs_run=time.time() - t0)
    cnt = {k: [0, 0] for k in
           ('T0', 'CA', 'CAoff', 'CB1', 'CB2', 'CC', 'CJ', 'CG',
            'CNEWy', 'CNEWu', 'CB1_change', 'CB2_change')}
    worstCB = None       # worst componentwise ratio min Y_t/Y_{t-1} (same face)
    faces = {}
    wc = {}
    stages_float = []
    Sprev = None
    ncorr = 0
    for t, r in enumerate(recs):
        S, x, xn, ah, be, qr = (r['S'], r['x'], r['xn'], r['ah'],
                                r['beta'], r['qr'])
        if r['Delta'] > 0:
            ncorr += 1
        Y, Ym, Yn = Ys[t], Ys[t - 1] if t > 0 else None, Ys[t + 1]
        suppx = tuple(i for i in range(n) if x[i] > 0)
        suppn = tuple(i for i in range(n) if xn[i] > 0)
        if not S:
            Sprev = S
            continue
        # u_t on full space
        u = None
        if Ym is not None:
            u = [(1 + be) * Y[i] - be * Ym[i] for i in range(n)]
            # T0: trigger predicate
            cnt['T0'][1] += 1
            cnt['T0'][0] += ((r['Delta'] > 0) == any(u[i] < 0 for i in S))
            # CC
            cnt['CC'][1] += 1
            cnt['CC'][0] += all(u[i] >= 0 for i in S)
            # CJ
            cnt['CJ'][1] += 1
            cnt['CJ'][0] += all(u[i] >= 0 for i in suppn)
            # CB floors on S_t
            same = (S == Sprev)
            for nm, c in (('CB1', 1 - qr), ('CB2', (1 - qr) / 2)):
                ok = all(Y[i] >= c * Ym[i] for i in S)
                key = nm if same else nm + '_change'
                cnt[key][1] += 1
                cnt[key][0] += ok
            if same:
                rats = [Y[i] / Ym[i] for i in S if Ym[i] > 0]
                if rats:
                    mr = min(rats)
                    worstCB = mr if worstCB is None else min(worstCB, mr)
        # CA
        cnt['CA'][1] += 1
        cnt['CA'][0] += all(Y[i] >= 0 for i in S)
        cnt['CAoff'][1] += 1
        cnt['CAoff'][0] += all(Y[i] <= 0 for i in range(n) if i not in suppx)
        # CG (dynamics identity; ell=ah iff Delta=0)
        if r['Delta'] == 0:
            cnt['CG'][1] += 1
            cnt['CG'][0] += all(Yn[i] == kap * I.d[i] * (xn[i] - ah[i])
                                for i in suppn)
        # CNEW: activation coords
        newc = [j for j in suppn if j not in suppx]
        for j in newc:
            cnt['CNEWy'][1] += 1
            cnt['CNEWy'][0] += (Y[j] <= 0)
            if t + 1 < len(recs):
                ben = recs[t + 1]['beta']
                un = (1 + ben) * Yn[j] - ben * Y[j]
                cnt['CNEWu'][1] += 1
                cnt['CNEWu'][0] += (un > 0)
        # --- per-face info (once)
        if S not in faces:
            key = (S, 8)
            if key not in wc:
                wc[key] = face_w_exact(I.Qt, I.d, I.adj, list(S), k=8)
            wS, dv, lo, hi = wc[key]
            faces[S] = face_info(I, S, qr, hi, wS)
            faces[S]['t_first'] = t
        # --- float certificate quantities (w^(8)-split), Measured
        wS = wc[(S, 8)][0]
        idx = list(S)
        wf = np.array([float(wS[i]) for i in idx])
        Df = np.array([float(I.d[i]) for i in idx])
        Yf = np.array([float(Y[i]) for i in idx])
        psi = Df * wf
        nps = float((Df * wf * wf).sum())        # ||psi||_*^2 = ||w||_D^2
        L = float((wf * Yf).sum()) / nps
        h = Yf - L * psi
        hn = math.sqrt(float((h * h / Df).sum()))
        # sharp componentwise bridge: max_i |(1+b)h_i - b hm_i| / (b Lm psi_i)
        sf = dict(t=t, S=len(S), L=L, hn=hn, qr=float(qr),
                  be=float(be), change=(S != Sprev), h=h, psi=psi)
        stages_float.append(sf)
        Sprev = S
    # --- certificate scan (float): R_t over same-face consecutive pairs
    cert = []       # (t, ok_norm, ratio_norm, ratio_sharp, hL, Lfloor_ok)
    prev = None
    for sf in stages_float:
        t = sf['t']
        fc = faces[recs[t]['S']]
        if prev is not None and not sf['change'] and prev['L'] > 0 \
                and fc.get('crit') is not None and fc['size'] > 1:
            be = sf['be']
            s2 = fc['s2']
            m2 = s2 / be
            p2 = m2 * (1 + be)
            dn = 1 - p2 / (2 * math.sqrt(s2))
            smin = be * float(I.kappa) / (float(I.kappa) + fc['lam'][2])
            CS = (1 + be) ** 2 + be ** 2 / smin
            # conservative V_ub = (||h_t|| + sqrt(s2)||h_{t-1}||)^2
            Vub = (sf['hn'] + math.sqrt(s2) * prev['hn']) ** 2
            lhs = math.sqrt(fc['d_max'] * CS * Vub / max(dn, 1e-300))
            rhs = be * fc['m_psi'] * prev['L']
            # sharp componentwise: |(1+b)h - b hm|_i vs b*Lm*psi_i
            num = np.abs((1 + be) * sf['h'] - be * prev['h'])
            rsharp = float(np.max(num / (be * prev['L'] * sf['psi'])))
            lf = (sf['L'] >= (1 - sf['qr']) * prev['L'] > 0)
            cert.append((t, bool(lhs <= rhs),
                         lhs / rhs if rhs > 0 else float('inf'),
                         rsharp, sf['hn'] / abs(sf['L']) if sf['L'] else -1,
                         bool(lf)))
        prev = sf
    # t_cert: first t such that cert holds for all later same-face stages
    tc = tcs = None
    nlf = [0, 0]
    for t, ok, rat, rs, hL, lf in cert:
        if ok and tc is None:
            tc = t
        if not ok:
            tc = None
        if rs <= 1 and tcs is None:
            tcs = t
        if rs > 1:
            tcs = None
        nlf[1] += 1
        nlf[0] += lf
    res['checks'] = cnt
    res['ncorr'] = ncorr
    res['worstCB_ratio'] = float(worstCB) if worstCB is not None else None
    res['faces'] = {str(k): v for k, v in faces.items()}
    res['nfaces'] = len(faces)
    res['n_od_list'] = [v.get('n_od') for v in faces.values()]
    res['t_cert'] = tc
    res['t_cert_sharp'] = tcs
    res['cert_frac'] = (sum(1 for c in cert if c[1]), len(cert))
    res['sharp_frac'] = (sum(1 for c in cert if c[3] <= 1), len(cert))
    res['Lfloor_frac'] = tuple(nlf)
    res['cert_end'] = cert[-1][2] if cert else None
    res['sharp_end'] = cert[-1][3] if cert else None
    res['hL_end'] = cert[-1][4] if cert else None
    res['cert_trace'] = [(c[0], round(c[2], 3), round(c[3], 3),
                          round(c[4], 4)) for c in cert[:: max(1, len(cert) // 40)]]
    res['secs'] = time.time() - t0
    return res


CELLS = [
    ('P24', lambda: path_graph(24), 24, Fr(1, 32), Fr(65, 4096), 400),
    ('P16', lambda: path_graph(16), 16, Fr(1, 24), Fr(1, 32), 250),
    ('P20', lambda: path_graph(20), 20, Fr(1, 32), Fr(7, 256), 250),
    ('P12', lambda: path_graph(12), 12, Fr(1, 20), Fr(5, 128), 200),
    ('cat5_2', lambda: caterpillar(5, 2), 15, Fr(1, 20), Fr(5, 128), 200),
    ('S16leaf', lambda: star_graph(16), 16, Fr(1, 20), Fr(5, 128), 150),
    ('P18', lambda: path_graph(18), 18, Fr(1, 24), Fr(11, 512), 200),
    ('cat4_3', lambda: caterpillar(4, 3), 16, Fr(1, 24), Fr(9, 256), 200),
    ('bt15root', lambda: btree(3), 15, Fr(1, 20), Fr(3, 64), 200),
]


def main(which=None):
    allres = {}
    order = CELLS if which is None else [c for c in CELLS if c[0] in which]
    # small cells first so results stream in
    order = sorted(order, key=lambda c: c[5] * c[2])
    for nm, g, n, q, rho, T in order:
        adj = g()
        seed = [Fr(0)] * n
        seed[1 if nm == 'S16leaf' else 0] = Fr(1)
        r = run_cell(nm, adj, seed, q, rho, T)
        allres[nm] = r
        ck = r['checks']

        def f(k):
            return '%d/%d' % tuple(ck[k])
        print("%-8s T=%d corr=%d | T0 %s CA %s CAoff %s CC %s CJ %s CG %s | "
              "CB1 %s CB2 %s (chg %s / %s) worstCB=%.6f | CNEW y%s u%s | "
              "n_od=%s Lfloor=%s | tc=%s tcs=%s cert %s sharp %s "
              "end(c/s/hL)=%.3g/%.3g/%.3g [%.0fs]"
              % (nm, r['T'], r['ncorr'], f('T0'), f('CA'), f('CAoff'),
                 f('CC'), f('CJ'), f('CG'), f('CB1'), f('CB2'),
                 f('CB1_change'), f('CB2_change'),
                 r['worstCB_ratio'] or -1, f('CNEWy'), f('CNEWu'),
                 sorted(set(r['n_od_list'])), '%d/%d' % r['Lfloor_frac'],
                 r['t_cert'], r['t_cert_sharp'],
                 '%d/%d' % r['cert_frac'], '%d/%d' % r['sharp_frac'],
                 r['cert_end'] or -1, r['sharp_end'] or -1,
                 r['hL_end'] or -1, r['secs']), flush=True)
        json.dump(allres, open(OUT, 'w'), indent=1, default=str)
    print("ALL DONE", flush=True)


if __name__ == '__main__':
    main(sys.argv[1:] or None)
