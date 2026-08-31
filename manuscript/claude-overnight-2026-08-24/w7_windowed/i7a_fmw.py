"""I7-A: composed never-triggering proof -- the certified-warmup variant fm-w.

MODIFICATION (task option (ii), legal): after every face change, run J_S pure
proximal stages (beta_t = 0) on the new face S before enabling the certified
face momentum beta(S); enable momentum on S only if the exact inertia gate
passes (exactly one mode of D_S^{-1} Qt_S at or below crit = kap qr^2/(1-qr^2)
per connected component, with a strictly separated bracket lam_2 >= th_lo >
crit).  J_S is the explicit warmup length

    J_S = 1 + ceil( log(R0bound_S) / (2 log(1/mu+_S)) ),  (per component, max)
    R0bound_S = C_S A_S^2 / (4 dn-_S m_psi^2 beta),   A_S = ||psi||_*^2/m_psi,
    mu+_S = m2+_S/(1-qr^2) < 1,  m2+_S = kap/(kap+th_lo),
    dn-_S = 1 - (1+beta) sqrt(m2+_S) / (2 sqrt(beta)) > 0,
    C_S   = (1+beta)^2 + beta (kap+1)/kap   (s_min >= beta kap/(kap+1)),

with psi the face Perron direction (implemented via the exact-rational w^(k)
proxy; certified entrywise Perron brackets are flagged as the remaining
engineering item; J enters only logarithmically).

PROOF SKELETON (see findings/i7a_never_trigger_complete.md):
 P-A  (LCP comparison) never-fire at t  =>  x_{t+1} >= a_t  (exact M-matrix
      subsolution comparison; new lemma, closes the class-2 induction).
 P-B  beta=0 stage: u_t = Y_t = kap D (x_t - a_{t-1}) >= 0 on supp(x_t)
      => never fires.  Unconditional; covers all change stages + warmups,
      entering coordinates included (activation lemma subsumed).
 P-C  cone bound ||h||_*/L <= A_S for any Y >= 0 on S.
 P-D  prox contraction (h/L) *= m_2/m_S <= mu+ per warmup solve;
      V_{t*} <= (beta/4)||h_{t*-1}||^2 at the first momentum stage
      => R_{t*} <= R0bound * mu+^{2(J-1)} <= 1 and L-floor holds at t*.
 P-E  A2 fixed-face propagation theorem (PROVED, i6a2 SS4) from t* to the
      end of the segment (per component; blocks decouple).
 => every stage of every run is N: Delta_t = 0 exactly, J_T^fin = 0.

This script: run_fmw (exact Fractions), per-stage exact checks (NF, YPOS,
CMP, KKT, UID), exact rational inertia gate + lam_2 bisection, float modal
certificate check at momentum stages (R_t*, L-floor, sharp form, R decay).
"""
import sys, json, time, math
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from engine import Inst, path_graph, star_graph, complete_graph, _gauss
from i3g_core import face_w_exact, components
from i5c_core import face_mom
from i6a1_checks import CELLS, caterpillar, btree, random_tree
import numpy as np


# ---------------- exact inertia (count modes of D^-1 Qt_S <= theta) --------
def inertia_le(I, comp, theta):
    """# eigenvalues of (D^-1 Qt) restricted to comp that are <= theta
    = # nonpositive eigenvalues of Qt_comp - theta*D_comp (exact rational)."""
    idx = list(comp)
    m = len(idx)
    A = [[I.Qt[a][b] - (theta * I.d[a] if a == b else Fr(0)) for b in idx]
         for a in idx]
    neg = zer = pos = 0
    act = list(range(m))
    while act:
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
            continue
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
            ci, cj = A[r][i0], A[r][j0]
            if ci == 0 and cj == 0:
                continue
            xi, xj = cj / b, ci / b
            for s in act:
                A[r][s] -= xi * A[i0][s] + xj * A[j0][s]
            A[r][i0] = A[r][j0] = Fr(0)
    return neg + zer


def simple_frac(x, den=1 << 20):
    return Fr(round(x * den), den)


def lam2_lower(I, comp, crit, rounds=12):
    """Certified lower bracket th_lo for lam_2 on component comp, given the
    gate inertia_le(crit) == 1 already holds.  Returns th_lo > crit with
    inertia_le(th_lo) == 1 (so lam_2 > th_lo), exact rational."""
    lo = crit
    hi = min(Fr(2), 2 * crit if crit > 0 else Fr(1, 2))
    while inertia_le(I, comp, hi) < 2:
        lo = hi
        hi = 2 * hi
        if hi > 4:            # lam_max <= 1 < 4 always; safety
            return lo
    for _ in range(rounds):
        mid = (lo + hi) / 2
        mids = simple_frac(float(mid))
        if not (lo < mids < hi):
            mids = mid
        if inertia_le(I, comp, mids) < 2:
            lo = mids
        else:
            hi = mids
    return lo


# ---------------- face gate + warmup length ----------------
def face_gate_J(I, S, w, qr, be, jfix=None):
    """Per-face momentum gate + certified warmup length J (max over comps).
    Returns dict(gate=bool, J=int or None, detail per comp)."""
    kap = I.kappa
    if qr >= 1 or be == 0:
        return dict(gate=False, J=None, why='beta=0 calibration')
    crit = kap * qr * qr / (1 - qr * qr)
    dets = []
    Jmax = 1
    for comp in components(I.adj, S):
        if len(comp) == 1:
            dets.append(dict(m=1, J=1))
            continue
        nle = inertia_le(I, comp, crit)
        if nle != 1:
            return dict(gate=False, J=None,
                        why='n_od=%d on comp size %d' % (nle, len(comp)))
        th_lo = lam2_lower(I, comp, crit)
        if th_lo <= crit:
            return dict(gate=False, J=None, why='no strict lam2 bracket')
        m2p = kap / (kap + th_lo)
        mup = m2p / (1 - qr * qr)          # certified < 1
        # constants from w (exact rationals; float for J only)
        mpsi = min(math.sqrt(I.d[i]) * float(w[i]) for i in comp)
        psi2 = sum(float(I.d[i]) * float(w[i]) ** 2 for i in comp)
        A = psi2 / mpsi
        bef = float(be)
        dnm = 1 - (1 + bef) * math.sqrt(float(m2p)) / (2 * math.sqrt(bef))
        C = (1 + bef) ** 2 + bef * (float(kap) + 1) / float(kap)
        R0 = C * A * A / (4 * dnm * mpsi * mpsi * bef)
        J = 1 + max(0, math.ceil(math.log(max(R0, 1.0))
                                 / (2 * math.log(1 / float(mup)))))
        dets.append(dict(m=len(comp), m2p=float(m2p), mup=float(mup),
                         dnm=dnm, A=A, mpsi=mpsi, C=C, R0=R0, J=J))
        Jmax = max(Jmax, J)
    return dict(gate=True, J=(jfix if jfix is not None else Jmax), dets=dets,
                Jcert=Jmax, crit=crit)


# ---------------- float modal machinery for the certificate check ----------
def modal_data(I, S):
    idx = list(S)
    m = len(idx)
    d = np.array([float(I.d[i]) for i in idx])
    Qt = np.array([[float(I.Qt[a][b]) for b in idx] for a in idx])
    B = Qt / np.sqrt(d)[:, None] / np.sqrt(d)[None, :]
    lam, Z = np.linalg.eigh(B)          # B z = lam z ;  phi_k = D^{1/2} z_k
    kap = float(I.kappa)
    mk = kap / (kap + lam)              # decreasing in lam: mk[0] = Perron
    z1 = Z[:, 0]
    if z1.sum() < 0:
        Z = -Z
    return idx, d, lam, Z, mk


def modal_coords(dat, Yfull):
    idx, d, lam, Z, mk = dat
    y = np.array([float(Yfull[i]) for i in idx]) / np.sqrt(d)
    return Z.T @ y                       # coords in *-orthonormal basis


# ---------------- the fm-w run with exact proof checks ----------------
def run_fmw(I, T, jfix=None, k=8, den=10**14, collect_modal=True):
    n = I.n
    q, al, kap = I.q, I.alpha, I.kappa
    d, Qt, ct, xs = I.d, I.Qt, I.ct, I.xstar
    xm = [Fr(0)] * n
    x = [Fr(0)] * n
    wcache, mcache, gcache, dcache = {}, {}, {}, {}
    out = []
    prevS0 = None
    stable = 0
    Yprev = None                 # Y_{t-1} full space (exact)
    C = {kk: [0, 0] for kk in ('NF', 'YPOS', 'CMP', 'KKT', 'UID', 'MOM',
                               'PROX', 'RLE1', 'LFLOOR', 'SHARP1')}
    gates = {}
    momstarts = []
    rdecay = []
    fails = []
    prev_mom = False
    Rprev = None
    t0 = time.time()
    for t in range(T):
        dh = [x[i] - xm[i] for i in range(n)]
        S0 = tuple(i for i in range(n) if x[i] > 0 or dh[i] > 0)
        if S0 != prevS0:
            stable = 0
        # else stable was incremented after last solve
        be = Fr(0)
        qr = Fr(1)
        g = None
        if S0:
            if S0 not in wcache:
                wcache[S0] = face_w_exact(Qt, d, I.adj, list(S0), k=k, den=den)
            if S0 not in mcache:
                mcache[S0] = face_mom(I, wcache[S0][3])
            qr, beF = mcache[S0]
            if stable >= 1 and S0 not in gcache:
                gcache[S0] = face_gate_J(I, S0, wcache[S0][0], qr, beF,
                                         jfix=jfix)
                gates[S0] = dict(size=len(S0), gate=gcache[S0]['gate'],
                                 J=gcache[S0].get('J'),
                                 Jcert=gcache[S0].get('Jcert'),
                                 why=gcache[S0].get('why'))
            g = gcache.get(S0)
            if g and g['gate'] and stable >= g['J']:
                be = beF
        is_mom = (be > 0)
        ah = [x[i] + be * dh[i] for i in range(n)]
        S = tuple(i for i in range(n) if ah[i] > 0)
        # exact Y_t
        Y = [ct[i] - sum(Qt[i][j] * x[j] for j in range(n) if x[j] != 0)
             for i in range(n)]
        # trigger (face cap, as i5c fm)
        Delta = Fr(0)
        w, dv = {}, {}
        if S:
            wv, dvv, cwlo, cwhi = wcache[S0] if S == S0 else \
                face_w_exact(Qt, d, I.adj, list(S), k=k, den=den)
            w, dv = wv, dvv
            zeta = {}
            for i in S:
                zt = ct[i] - sum(Qt[i][j] * ah[j] for j in S)
                zeta[i] = zt
                if zt < 0:
                    cand = -zt / dv[i]
                    if cand > Delta:
                        Delta = cand
            # UID: zeta(a_t) == (1+be) Y_t - be Y_{t-1} on S (exact identity)
            if Yprev is not None:
                ok = all(zeta[i] == (1 + be) * Y[i] - be * Yprev[i]
                         for i in S)
                C['UID'][1] += 1
                C['UID'][0] += ok
                if not ok:
                    fails.append(('UID', t))
        C['NF'][1] += 1
        C['NF'][0] += (Delta == 0)
        if Delta != 0:
            fails.append(('NF', t))
        # YPOS: Y_t >= 0 on supp(x_t)  (exact)
        if t >= 1:
            ok = all(Y[i] >= 0 for i in range(n) if x[i] > 0)
            C['YPOS'][1] += 1
            C['YPOS'][0] += ok
            if not ok:
                fails.append(('YPOS', t))
        C['MOM' if is_mom else 'PROX'][1] += 1
        C['MOM' if is_mom else 'PROX'][0] += (Delta == 0)
        # modal certificate at momentum stages (float, Measured)
        if is_mom and collect_modal and Yprev is not None:
            key = S0
            if key not in dcache:
                dcache[key] = modal_data(I, S0)
            dat = dcache[key]
            yt = modal_coords(dat, Y)
            yp = modal_coords(dat, Yprev)
            mk = dat[4]
            bef = float(be)
            L, Lp = yt[0], yp[0]
            hk, hp = yt[1:], yp[1:]
            pk = (1 + bef) * mk[1:]
            sk = bef * mk[1:]
            V = float(np.sum(hk**2 - pk * hk * hp + sk * hp**2))
            m2, mS = mk[1], mk[0]
            dn = 1 - (1 + bef) * math.sqrt(m2) / (2 * math.sqrt(bef))
            smin = float(sk[-1])
            Cc = (1 + bef)**2 + bef**2 / smin
            # mpsi = min_i phi_1,i / sqrt(d_i) = min_i z1_i (phi = D^{1/2} z)
            mpsi = float(np.min(dat[3][:, 0]))
            qrf = float(mcache[S0][0])
            R = Cc * V / (dn * mpsi**2 * bef**2 * Lp**2) if Lp > 0 else 0.0
            lfloor = (L >= (1 - qrf) * Lp > 0)
            # sharp componentwise form
            hvec_t = np.array([float(Y[i]) for i in dat[0]]) / np.sqrt(dat[1]) \
                - L * dat[3][:, 0]
            hvec_p = np.array([float(Yprev[i]) for i in dat[0]]) / \
                np.sqrt(dat[1]) - Lp * dat[3][:, 0]
            comb = (1 + bef) * hvec_t - bef * hvec_p
            sharp = float(np.max(np.abs(comb) / (bef * Lp * dat[3][:, 0]))) \
                if Lp > 0 else 0.0
            first = not prev_mom
            if first:
                momstarts.append(dict(t=t, S=len(S0), R=R, sharp=sharp,
                                      L=L, Lp=Lp, lfloor=bool(lfloor),
                                      J=g['J'], stable=stable))
                C['RLE1'][1] += 1
                C['RLE1'][0] += (R <= 1)
                if R > 1:
                    fails.append(('RLE1', t, R))
                C['SHARP1'][1] += 1
                C['SHARP1'][0] += (sharp <= 1)
            C['LFLOOR'][1] += 1
            C['LFLOOR'][0] += bool(lfloor)
            if not lfloor:
                fails.append(('LFLOOR', t))
            if Rprev is not None and not first:
                s2 = bef * m2
                rate = s2 / (1 - qrf)**2
                rdecay.append((t, R, Rprev, rate,
                               bool(R <= rate * Rprev * (1 + 1e-9))))
            Rprev = R
        else:
            Rprev = None
        prev_mom = is_mom
        # solve
        ellh = ah  # never-fire expected; retraction only if Delta>0
        if Delta != 0:
            cap = [Delta * w.get(i, Fr(0)) for i in range(n)]
            rh = [min(be * dh[i], cap[i]) for i in range(n)]
            ellh = [ah[i] - rh[i] for i in range(n)]
        xn = I.obstacle_solve(ct, kap, ellh, warm=S or None)
        # CMP: x_{t+1} >= a_t  (exact; LCP comparison conclusion)
        ok = all(xn[i] >= ah[i] for i in range(n))
        C['CMP'][1] += 1
        C['CMP'][0] += ok
        if not ok:
            fails.append(('CMP', t))
        # KKT on supp(xn) (exact)
        ok = all(ct[i] - sum(Qt[i][j] * xn[j] for j in range(n) if xn[j] != 0)
                 == kap * d[i] * (xn[i] - ellh[i])
                 for i in range(n) if xn[i] > 0)
        C['KKT'][1] += 1
        C['KKT'][0] += ok
        if not ok:
            fails.append(('KKT', t))
        newS0 = tuple(i for i in range(n)
                      if xn[i] > 0 or (xn[i] - x[i]) > 0)
        if newS0 == S0:
            stable += 1
        out.append(dict(t=t, cls=('N' if Delta == 0 else 'X'), mom=is_mom,
                        S=S0, beta=be))
        prevS0 = S0
        Yprev = Y
        xm, x = x, xn
    # convergence diagnostic (float): D-weighted err vs xstar
    err = math.sqrt(sum(float(d[i]) * float(xs[i] - x[i])**2
                        for i in range(n)))
    nchg = sum(1 for a, b in zip(out, out[1:]) if a['S'] != b['S'])
    seglens = []
    cur = 1
    for a, b in zip(out, out[1:]):
        if a['S'] == b['S']:
            cur += 1
        else:
            seglens.append(cur)
            cur = 1
    seglens.append(cur)
    return dict(T=len(out), checks={kk: tuple(v) for kk, v in C.items()},
                fails=fails[:40], nfails=len(fails),
                gates={str(len(k)) + ':' + str(k[:3]) + '..': v
                       for k, v in gates.items()},
                momstarts=momstarts, rdecay_ok=[r[4] for r in rdecay],
                rdecay_n=len(rdecay),
                nchanges=nchg, seglens=seglens, err=err,
                secs=round(time.time() - t0, 1))


FRESH = {
    # short-segment-heavy adversarial cells (screened by i7a_screen)
    'rt20a': (random_tree(20, 3), [Fr(1)] + [Fr(0)] * 19, Fr(1, 24),
              Fr(1, 64), 160),
    'rt22b': (random_tree(22, 7), [Fr(0)] * 5 + [Fr(1)] + [Fr(0)] * 16,
              Fr(1, 28), Fr(1, 96), 160),
    'P30lr': (path_graph(30), [Fr(1)] + [Fr(0)] * 29, Fr(1, 40),
              Fr(1, 128), 200),
    'cat6_2': (caterpillar(6, 2), [Fr(1)] + [Fr(0)] * 17, Fr(1, 24),
               Fr(1, 48), 160),
    'bt31': (btree(4), [Fr(1)] + [Fr(0)] * 30, Fr(1, 24), Fr(1, 40), 140),
}
ALL = dict(CELLS)
ALL.update(FRESH)


if __name__ == '__main__':
    name = sys.argv[1]
    jfix = None
    Tov = None
    for a in sys.argv[2:]:
        if a.startswith('J'):
            jfix = int(a[1:])
        else:
            Tov = int(a)
    adj, seed, q, rho, T = ALL[name]
    if Tov:
        T = Tov
    I = Inst(adj, seed, q, rho)
    o = run_fmw(I, T, jfix=jfix)
    o['cell'] = name
    o['nS'] = len(I.Sstar)
    o['n'] = I.n
    o['proper'] = 0 < len(I.Sstar) < I.n
    print(json.dumps(o, default=str))
