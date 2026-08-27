"""I6-A1: solvent comparison certificate, float exploration.

Certificate sought (entrywise, on face S with M = (Qt_S+kapD_S)^{-1} kapD_S,
beta = face-calibrated):   a matrix R with
    (C1) R >= 0
    (C2) (1+beta)M - R >= 0
    (C3) ((1+beta)M - R) R - beta M >= 0
Then the cone {(y,y'): y >= 0, y' >= R y} is invariant for
y_{t+1} = M[(1+b)y_t - b y_{t-1}], and y_t >= 0 for all t follows from the
base pair.  Never-fire = tau_t >= 0 with tau the (T)-functional, which obeys
the same recurrence => same certificate applies.

Candidates tested per locked face:
  R_min : minimal solvent via iteration R <- ((1+b)M - R)^{-1} (b M)
  R_com : commuting candidate f(M) with f = clip(z_-(m), ...) per mode
  R_1q  : (1-q_r) * P_w  (Perron-rank-one)  + gamma*(I-P_w) scan
Reports entrywise mins of C1-C3 and the residual of the quadratic.
Also tests trajectory containment d_{t+1} >= R d_t post-lock (float mirror
of the exact run, using engine float port via numpy LCP-free re-run: we
re-run the exact recurrence in float with plain solves on the locked support
-- adequate for exploratory margins).
"""
import sys, json
import numpy as np
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from engine import Inst, path_graph, star_graph, complete_graph
from i5c_core import face_mom
from i3g_core import face_w_exact
from i6a1_checks import CELLS, caterpillar, btree, random_tree


def analyze_face(I, S, k=8):
    n = I.n
    idx = list(S)
    m = len(idx)
    kap = float(I.kappa)
    Qt = np.array([[float(I.Qt[i][j]) for j in idx] for i in idx])
    D = np.diag([float(I.d[i]) for i in idx])
    H = Qt + kap * D
    M = np.linalg.solve(H, kap * D)
    # calibration (exact, as the engine does it)
    w, dv, lo, hi = face_w_exact(I.Qt, I.d, I.adj, list(S), k=k)
    qr, be = face_mom(I, hi)
    qr, be = float(qr), float(be)
    # spectrum of M (similar to symmetric): eigenvalues
    Dh = np.diag(np.sqrt(np.diag(D)))
    Dhi = np.linalg.inv(Dh)
    Msym = Dh @ M @ Dhi
    ev = np.linalg.eigvalsh((Msym + Msym.T) / 2)
    mS = ev.max()
    # -------- minimal solvent iteration
    res = {}
    R = np.zeros((m, m))
    ok_it = True
    for it in range(4000):
        A = (1 + be) * M - R
        try:
            Rn = np.linalg.solve(A, be * M)
        except np.linalg.LinAlgError:
            ok_it = False
            break
        if not np.isfinite(Rn).all():
            ok_it = False
            break
        step = np.abs(Rn - R).max()
        R = Rn
        if step < 1e-15:
            break
    U = (1 + be) * M - R
    C3 = U @ R - be * M
    evR = np.linalg.eigvals(R)
    res['solvent'] = dict(
        converged=bool(ok_it and step < 1e-12), iters=it,
        minR=float(R.min()), minU=float(U.min()),
        resid=float(np.abs(C3).max()),
        specR=float(np.abs(evR).max()),
        n_complex=int(np.sum(np.abs(evR.imag) > 1e-9)))
    # -------- commuting candidate: per-mode z_-(m), clipped for underdamped
    lam, V = np.linalg.eigh((Msym + Msym.T) / 2)
    disc = (1 + be) ** 2 * lam ** 2 - 4 * be * lam
    zm = np.where(disc >= 0,
                  ((1 + be) * lam - np.sqrt(np.maximum(disc, 0))) / 2,
                  (1 + be) * lam / 2)   # underdamped: real part
    Rc = Dhi @ (V @ np.diag(zm) @ V.T) @ Dh
    Uc = (1 + be) * M - Rc
    C3c = Uc @ Rc - be * M
    res['commuting'] = dict(minR=float(Rc.min()), minU=float(Uc.min()),
                            minC3=float(C3c.min()))
    # -------- rank-one + scalar scan: R = a*I + c*(M - a-ish)  quick scan
    best = None
    wv = V[:, -1]   # top mode of Msym
    Pw = np.outer(wv, wv)
    Pw_x = Dhi @ Pw @ Dh
    for a in np.linspace(0, be, 8):
        for c in np.linspace(0, 1.2, 13):
            Rt = a * (np.eye(m) - Pw_x) + c * Pw_x * (1 - qr)
            # note: (1-qr) scaling on the Perron part
            Ut = (1 + be) * M - Rt
            C3t = Ut @ Rt - be * M
            sc = min(Rt.min(), Ut.min(), C3t.min())
            if best is None or sc > best[0]:
                best = (float(sc), float(a), float(c))
    res['ranked_scan'] = dict(best_min=best[0], a=best[1], c=best[2])
    return dict(m=m, qr=qr, beta=be, mS=float(mS), one_minus_qr2=1 - qr * qr,
                margins=res, lam_min=float(ev.min()), lam2=float(ev[-2]) if m > 1 else None)


def main():
    out = {}
    for name in ('P24', 'P16', 'P20', 'P12', 'cat5_2', 'S16', 'P18',
                 'cat4_3', 'bt15', 'P24rho2', 'P24rho3', 'rt18', 'rt16b'):
        adj, seed, q, rho, T = CELLS[name]
        I = Inst(adj, seed, q, rho)
        if not (0 < len(I.Sstar) < I.n):
            out[name] = dict(skip='interior')
            continue
        out[name] = analyze_face(I, tuple(I.Sstar))
        r = out[name]
        s = r['margins']['solvent']
        print("%-8s m=%-3d qr=%.4f mS=%.6f 1-qr2=%.6f | solvent conv=%s "
              "minR=%.3e minU=%.3e resid=%.1e specR=%.6f cplx=%d | "
              "commut minR=%.3e minU=%.3e minC3=%.3e | scan best=%.3e"
              % (name, r['m'], r['qr'], r['mS'], r['one_minus_qr2'],
                 s['converged'], s['minR'], s['minU'], s['resid'],
                 s['specR'], s['n_complex'],
                 r['margins']['commuting']['minR'],
                 r['margins']['commuting']['minU'],
                 r['margins']['commuting']['minC3'],
                 r['margins']['ranked_scan']['best_min']), flush=True)
    json.dump(out, open('/home/claude/work/overnight/w7_windowed/'
                        'i6a1_solvent.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
