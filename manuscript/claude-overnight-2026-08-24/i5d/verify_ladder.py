"""I5-D verify_ladder.py -- single script re-checking every numbered inequality
of findings/i5d_ladder_paper.md on the star family.

Grid: alpha in {2^-4..2^-12}, eps in {2^-4..2^-8}, m = 1/(8 eps) (dyadic, exact).
Instance: centre-seeded star K_{1,m}.  Conventions: z-scale push system
H = I - c_a A D^{-1}, gamma_a = 2 alpha/(1+alpha), r = gamma_a e_v - H z,
work d_u per one-hop op, semantic error max_u |pi_u - z_u|/d_u <= eps.

Checks (numbers refer to the paper's inequalities):
 C1  closed forms pi_c=(1+a)/2, pi_l=(1-a)/(2m), Phi_0=alpha/(2m); elimination
     output is exact (Prop C).
 C2  seed-potential locality: Delta pr(r)_c = -alpha*eta*[u=c] for random
     SIGNED one-hop ops (eq. A.1).
 C3  kappa-step ingredient: r_c * pi_c <= pr(r)_c whenever r >= 0 (eq. A.2),
     and the multiplicative step Psi+ >= (1-kappa)Psi at positive seed ops.
 C4  Theorem A count: every M+- member run has N_c^+ >= LB_A and W >= m*LB_A.
 C5  Corollary A constant: W*alpha*eps >= ln(4)(1-alpha)^2/64.
 C6  energy identity (eq. B.1) per op (mixed abs/rel tolerance for float
     cancellation), plus reduced-state vs full-state reconciliation.
 C7  fast-mode cap |yhat_-| <= sqrt(2 Phi_0/(1+c_a)) (eq. B.2), pathwise.
 C8  displacement cap |delta_c| <= 2 sqrt(alpha(1+alpha)) (eq. B.3), pathwise.
 C9  Theorem B count: every finishing R+- schedule has N_c >= LB_B and
     W >= m*LB_B;  dyadic constant W*sqrt(alpha)*eps >= (1/8)(pi_c-1/8)
     / (2 sqrt(1+alpha)) = 3/(128 sqrt(1+alpha)) at eps m = 1/8.
 C10 R+- upper bounds (2-dim exact block reduction): W(omega*) within the
     proved bound m*ceil(ln(2/(sqrt(a) eps m))/sqrt(a)) (Thm B.5); for
     alpha <= 2^-6 also W(omega->2)*sqrt(a)*eps <= 0.10 (measured member
     frontier; the near-2 member is only claimed there), semantic stop.
 C11 elimination work: W_elim = 3m+1 <= 3/(8 eps)+1, err = 0 (Prop C).
 C12 pathwise residual-mass cap ||r||_1 <= 2 sqrt(alpha/(1+alpha)) (Prop B.6).
 C13 scale dictionary: z = p, r_z = gamma_a * r_mass, delta = alpha*eta, on a
     mirrored random signed op sequence.
Pump adversary (M+- with anti-pushes, sub-grid): counted under C4/C5.

Rerun:  cd /home/claude/work/overnight/i5d && python3 verify_ladder.py
"""
import math
import os
import random
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
for sub in ('lib', 'w1_monotone_lb', 'i4c'):
    sys.path.insert(0, os.path.join(ROOT, sub))
import zoo                                              # noqa: E402
from gpush import GP, pr_matrix, run_queue, run_scan    # noqa: E402
from core import Prob, State, params, omega_star        # noqa: E402

TOL = 1e-9


# ---------------------------------------------------------------- helpers
def work_blocks(alpha, tm, w_of_j, cap=300_000):
    """Exact 2-dim symmetric reduction (i4c/sweep.py): blocks to semantic stop.
    State (e_c, E_L) from (pi_c, c_a*pi_c); centre block then leaf block."""
    c_a, _ = params(alpha)
    pic = (1 + alpha) / 2.0
    ec, EL = pic, c_a * pic
    for N in range(1, cap + 1):
        w = w_of_j(N - 1)
        if N % 2 == 1:
            ec = (1 - w) * ec + w * c_a * EL
        else:
            EL = (1 - w) * EL + w * c_a * ec
        if max(abs(ec), abs(EL)) <= tm:
            return N
    return None


def pump_run(adj, alpha, eps, m, K=4.0):
    """M+- adversary: pump ||r||_1 to K by anti-pushes, then solve (coord stop).
    Returns (state, n_positive_centre_ops)."""
    st = GP(adj, alpha, 0, center=0)
    guard = 0
    while st.sum_r < K and guard < 3000:
        guard += 1
        rc = st.r[0]
        if rc > 1e-13:
            for w in range(1, st.n):
                st.gp(w, -2.0 * (rc / m) / (1.0 - alpha))
        mn = min(st.r[w] for w in range(1, st.n))
        if mn > 1e-13:
            st.gp(0, -2.0 * m * mn / (1.0 - alpha))
        else:
            break
    npos_c = 0
    guard = 0
    while guard < 2_000_000:
        guard += 1
        act = [u for u in range(st.n) if st.r[u] >= eps * st.d[u]]
        if not act:
            break
        if 0 in act:
            st.gp(0, st.cap(0)); st.r[0] = 0.0; npos_c += 1
        for w in act:
            if w != 0 and st.r[w] >= eps:
                st.gp(w, st.cap(w)); st.r[w] = 0.0
    return st, npos_c


def battery_schedules(alpha, rng):
    """Block generators: yield ('c', omega) = one centre op, or ('L', omega)
    = one full leaf sweep 1..m (m ops of cost 1)."""
    om = omega_star(alpha)
    lam = (1 - math.sqrt(alpha)) / (1 + math.sqrt(alpha))

    def alt(wfun):
        j = 0
        while True:
            w = wfun(j)
            yield ('c', w)
            yield ('L', w)
            j += 1

    scheds = {
        'sor*': alt(lambda j: om),
        'gs': alt(lambda j: 1.0),
        'near2': alt(lambda j: 2.0 - 1e-9),
        'fix1.5': alt(lambda j: 1.5),
        'cheb': alt(lambda j: min(1.999999, 1.0 + lam * lam *
                                  (1 - 0.9 * math.cos(2 * math.pi * j / 17)))),
        'rand': alt(lambda j: rng.uniform(0.05, 1.95)),
    }

    def leafheavy():
        while True:
            yield ('c', om)
            for _ in range(4):
                yield ('L', om)
    scheds['leafhv'] = leafheavy()
    return scheds


# ---------------------------------------------------------------- one cell
def run_cell(ea, ee, do_pump):
    alpha, eps = 2.0 ** -ea, 2.0 ** -ee
    m = int(round(1.0 / (8.0 * eps)))
    assert abs(m - 1.0 / (8.0 * eps)) < 1e-12          # dyadic grid: exact
    n = m + 1
    adj, _ = zoo.star(m)
    c_a, g_a = params(alpha)
    kap = 4.0 * alpha / (1.0 + alpha) ** 2
    pic = (1.0 + alpha) / 2.0
    P = Prob(adj, alpha, 0)
    pi = P.pi
    ok = {}
    info = {}

    # ---- C1: closed forms + elimination exactness
    c1 = (abs(pi[0] - pic) <= 1e-11
          and float(np.max(np.abs(pi[1:] - (1 - alpha) / (2 * m)))) <= 1e-12)
    Phi0 = P.phi(pi)
    c1 &= abs(Phi0 - alpha / (2 * m)) <= 1e-12
    z_el = np.empty(n)
    z_el[0] = g_a / (1.0 - c_a * c_a)
    z_el[1:] = c_a * z_el[0] / m
    err_el = P.err(z_el)
    c1 &= err_el <= 1e-11
    ok['C1'] = c1

    # ---- C2/C3: potential identity + kappa ingredient (random signed M+- run)
    Mop = pr_matrix(adj, alpha)
    phirow = alpha * np.linalg.inv(Mop)[0]              # pr(e_u)_c over u
    rng = random.Random(10007 * ea + ee)
    st = GP(adj, alpha, 0, center=0)
    c2 = c3 = True
    for _ in range(300):
        cand = [u for u in range(n) if st.r[u] > 1e-14]
        if not cand:
            break
        u = rng.choice(cand)
        if rng.random() < 0.45:
            mn = min(st.r[w] for w in adj[u])
            eta = -rng.uniform(0, 1) * 2.0 * mn * st.d[u] / (1 - alpha)
        else:
            eta = rng.uniform(0, 1) * 2.0 * st.r[u] / (1 + alpha)
        r_np = np.array(st.r)
        before = float(phirow @ r_np)
        c3 &= st.r[0] * pic <= before + 1e-10           # r_c*pi_c <= pr(r)_c
        st.gp(u, eta)
        after = float(phirow @ np.array(st.r))
        pred = -alpha * eta if u == 0 else 0.0
        c2 &= abs((after - before) - pred) <= 1e-10
        if u == 0 and eta > 0 and before > 1e-13:
            c3 &= after >= (1 - kap) * before - 1e-10   # multiplicative step
        c3 &= min(st.r) >= -1e-11
    ok['C2'], ok['C3'] = c2, c3

    # ---- C4/C5: Theorem A on member runs (+ pump on sub-grid)
    lbA = math.log((1 + alpha) / (2 * eps * m)) / (-math.log(1.0 - kap))
    consA = math.log(4.0) * (1 - alpha) ** 2 / 64.0
    members = [
        ('appr_fifo', run_queue(adj, alpha, eps, 0, 'fifo', 'coord', lazy=True)),
        ('greedy_nl', run_scan(adj, alpha, eps, 0, 'greedy', 'coord', lazy=False)),
        ('cheap1st', run_scan(adj, alpha, eps, 0, 'cheap_first', 'coord')),
    ]
    runsA = [(nm, s, s.n_center_ops) for nm, s in members]
    if do_pump:
        s, npos = pump_run(adj, alpha, eps, m, K=4.0)
        runsA.append(('pump_K4', s, npos))
    c4 = c5 = True
    minNcr = minWc = float('inf')
    for nm, s, npos in runsA:
        errv = s.err_sem(pi)
        c4 &= errv <= eps * (1 + 1e-9)
        c4 &= s.min_r_seen >= -1e-9
        c4 &= npos >= lbA - TOL and s.W >= m * lbA - TOL
        c5 &= s.W * alpha * eps >= consA * (1 - 1e-12)
        minNcr = min(minNcr, npos / lbA)
        minWc = min(minWc, s.W * alpha * eps)
    ok['C4'], ok['C5'] = c4, c5
    info['NcA/LB'] = minNcr
    info['WaeA'] = minWc
    info['lbA'] = lbA

    # ---- C6-C9, C12: R+- battery (z scale, full star as ground truth;
    # O(1) trackers from the exact symmetric reduction (e_c, e_l, r_c, r_l),
    # reconciled against the full state every 1024 ops and at stop.
    capB = 2.0 * math.sqrt(alpha * (1 + alpha))
    lbB = (pic - eps * m) / capB
    Bm = math.sqrt(2 * Phi0 / (1 + c_a))
    l1cap = 2.0 * math.sqrt(alpha / (1 + alpha))
    sq2m = math.sqrt(2.0 * m)
    rngb = random.Random(90001 * ea + ee)

    def phi_red(ec, el):
        return 0.5 * ec * ec / m + 0.5 * m * el * el - c_a * ec * el

    c6 = c7 = c8 = c9 = c12 = True
    maxE = maxY = maxD = maxL1 = 0.0
    minNcB = float('inf')
    blocks_cap = 2 * (int(1.5 / alpha) + 400)
    for name, it in battery_schedules(alpha, rngb).items():
        stz = State(P)
        ec, el = pic, (1 - alpha) / (2 * m)      # e = pi - z at z = 0
        rc, rl = g_a, 0.0                        # r = gamma_a e_c
        Nc = 0
        done = False
        for k in range(blocks_cap):
            kind, w = next(it)
            Phib = phi_red(ec, el)
            if kind == 'c':
                dd = stz.op(0, w)                # ground truth full state
                ec -= dd; rc *= (1 - w); rl += c_a * dd / m
                Nc += 1
                maxD = max(maxD, abs(dd) / capB)
                pred = 0.5 * w * (2 - w) * (dd / w) ** 2 / m
            else:
                # full leaf sweep: sibling leaf ops never touch r_l, so every
                # leaf op in the sweep relaxes the same r_l; aggregate the
                # sweep's exact energy identity (m identical per-op terms).
                dd = w * rl
                for l in range(1, m + 1):
                    stz.op(l, w)
                el -= dd; rc += c_a * dd * m     # m ops, each adds c_a*dd/1
                rl *= (1 - w)
                pred = m * 0.5 * w * (2 - w) * (dd / w) ** 2 if w > 0 else 0.0
            Phia = phi_red(ec, el)
            maxE = max(maxE, abs((Phib - Phia) - pred)
                       / max(1e-12, Phib, abs(pred)))
            maxY = max(maxY, abs(ec - m * el) / sq2m / Bm)
            maxL1 = max(maxL1, (abs(rc) + m * abs(rl)) / l1cap)
            if max(abs(ec) / m, abs(el)) <= eps:
                done = True
            if (k & 63) == 0 or done:            # reconcile vs full state
                e_full = pi - stz.z
                recon = (abs(e_full[0] - ec) <= 1e-8
                         and float(np.max(np.abs(e_full[1:] - el))) <= 1e-8
                         and abs(stz.r[0] - rc) <= 1e-8
                         and abs(P.err(stz.z)
                                 - max(abs(ec) / m, abs(el))) <= 1e-8)
                c6 &= recon
            if done:
                break
        if done:
            c9 &= Nc >= lbB - TOL and stz.W >= m * lbB - TOL
            minNcB = min(minNcB, Nc / lbB)
    c6 &= maxE <= 1e-6
    c7 &= maxY <= 1 + 1e-9
    c8 &= maxD <= 1 + 1e-9
    c12 &= maxL1 <= 1 + 1e-9
    ok['C6'], ok['C7'], ok['C8'], ok['C9'], ok['C12'] = c6, c7, c8, c9, c12
    info['NcB/LB'] = minNcB
    info['maxY'] = maxY
    info['maxD'] = maxD
    info['maxL1'] = maxL1
    info['lbB'] = lbB

    # ---- C10: R+- upper bounds via exact 2-dim reduction
    tm = eps * m
    om = omega_star(alpha)
    N1 = work_blocks(alpha, tm, lambda j: om)
    N2 = work_blocks(alpha, tm, lambda j: 2.0 - 1e-12)
    ubB_blocks = math.ceil(math.log(2.0 / (math.sqrt(alpha) * eps * m))
                           / math.sqrt(alpha))
    c10 = N1 is not None and N1 <= ubB_blocks
    if ea >= 6:      # near-2 member frontier is claimed for alpha <= 2^-6
        c10 &= (N2 is not None
                and N2 * m * math.sqrt(alpha) * eps <= 0.10)
    ok['C10'] = c10
    info['W2sae'] = (N2 * m * math.sqrt(alpha) * eps) if N2 else float('nan')
    info['N1sa'] = (N1 * math.sqrt(alpha)) if N1 else float('nan')

    # ---- C11: elimination work
    W_el = 3 * m + 1
    ok['C11'] = (W_el <= 3.0 / (8 * eps) + 1 + 1e-9) and err_el <= 1e-11
    info['Wel'] = W_el

    # ---- C13: scale dictionary on a mirrored random signed sequence
    rngd = random.Random(777 * ea + ee)
    gm = GP(adj, alpha, 0, center=0)
    zz = np.zeros(n)
    rz = np.zeros(n); rz[0] = g_a
    c13 = True
    for _ in range(120):
        cand = [u for u in range(n) if gm.r[u] > 1e-14]
        if not cand:
            break
        u = rngd.choice(cand)
        if rngd.random() < 0.4:
            mn = min(gm.r[w] for w in adj[u])
            eta = -rngd.uniform(0, 1) * 2.0 * mn * gm.d[u] / (1 - alpha)
        else:
            eta = rngd.uniform(0, 1) * 2.0 * gm.r[u] / (1 + alpha)
        gm.gp(u, eta)
        delta = alpha * eta
        zz[u] += delta
        rz[u] -= delta
        for w in adj[u]:
            rz[w] += c_a * delta / gm.d[u]
        c13 &= (abs(zz[u] - gm.p[u]) <= 1e-11
                and float(np.max(np.abs(rz - g_a * np.array(gm.r)))) <= 1e-11)
    ok['C13'] = c13

    return alpha, eps, m, ok, info


# ---------------------------------------------------------------- driver
def main():
    keys = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10',
            'C11', 'C12', 'C13']
    fails = {k: 0 for k in keys}
    ncells = 0
    print('=' * 118)
    print('I5-D  verify_ladder  --  star K_{1,m}, m = 1/(8 eps);'
          '  checks C1-C13 (see header);  . = pass, X = FAIL')
    print('=' * 118)
    hdr = (f"{'alpha':>7s} {'eps':>6s} {'m':>3s} | "
           + ' '.join(f'{k:>4s}' for k in keys)
           + f" | {'NcA/LB':>7s} {'W*ae>=':>7s} {'NcB/LB':>7s} {'W2*sae':>7s} "
             f"{'N(w*)sa':>8s} {'maxY':>6s} {'maxD':>6s} {'max|r|1':>8s}")
    print(hdr)
    t_rows = []
    for ea in range(4, 13):
        for ee in range(4, 9):
            do_pump = (ea in (4, 8, 12)) and (ee in (4, 6, 8))
            alpha, eps, m, ok, info = run_cell(ea, ee, do_pump)
            ncells += 1
            for k in keys:
                if not ok[k]:
                    fails[k] += 1
            row = (f'2^-{ea:<4d} 2^-{ee:<3d} {m:>3d} | '
                   + ' '.join(f"{'.' if ok[k] else 'X':>4s}" for k in keys)
                   + f" | {info['NcA/LB']:7.3f} {info['WaeA']:7.4f} "
                     f"{info['NcB/LB']:7.3f} {info['W2sae']:7.4f} "
                     f"{info['N1sa']:8.3f} {info['maxY']:6.3f} "
                     f"{info['maxD']:6.3f} {info['maxL1']:8.3f}")
            print(row, flush=True)
            t_rows.append(row)
    print('-' * 118)
    total_fail = sum(fails.values())
    print(f'cells: {ncells}   checks per cell: {len(keys)}   '
          f'FAILED cell-checks: {total_fail}')
    if total_fail:
        for k in keys:
            if fails[k]:
                print(f'  {k}: {fails[k]} failing cells')
    else:
        print('ALL PASS: every numbered inequality holds on every grid cell.')
    print()
    print('Constant floors asserted:  W*alpha*eps >= ln(4)(1-alpha)^2/64 '
          f'= {math.log(4)/64:.4f}*(1-alpha)^2  (Cor A.5, all members incl. '
          'pump);')
    print('  N_c >= (pi_c - eps m)/(2 sqrt(alpha(1+alpha))) and W >= m*that '
          '(Thm B.4, all finishing schedules);')
    print('  W(omega*) <= m*ceil(ln(2/(sqrt(a) eps m))/sqrt(a)) (Thm B.5);  '
          'W(omega->2)*sqrt(a)*eps <= 0.10 (member frontier);')
    print('  pathwise ||r||_1 <= 2 sqrt(alpha/(1+alpha)) (Prop B.6);  '
          '|yhat_-| and |delta_c| caps (Lem B.2/B.3).')


if __name__ == '__main__':
    main()
