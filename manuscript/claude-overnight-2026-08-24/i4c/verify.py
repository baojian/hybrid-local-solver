"""E3: adversarial verification of the two pathwise inequalities behind the
R+/- class lower bound, on the FULL star (no symmetry assumed), plus a
schedule battery measuring N_c (centre ops) and W against the bound.

Claims (per-op, any omega in (0,2), any adaptive/randomised policy):
 (P1) energy identity   Phi(e)-Phi(e^+) = [w(2-w)/2] r_u^2/d_u      (exact)
 (P2) fast-mode cap     |yhat_-| <= B_- := sqrt(2 Phi_0/(1+c_a))     (all t)
 (P3) per-centre-op cap |Delta z_c| = w|r_c| <= 2 sqrt(alpha(1+alpha))
 (P4) hence  N_c >= (pi_c - eps*m) / (2 sqrt(alpha(1+alpha))) >= 3/(16 sqrt(a(1+a)))
"""
import math, sys, os, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lib'))
import zoo
from core import Prob, State, omega_star, params

def star_modes(m):
    n = m + 1
    ph = np.zeros(n); ph[0] = math.sqrt(m); ph[1:] = -1.0
    return ph / math.sqrt(2*m)          # phi_- (N-eigenvalue -1)

def phi_of(P, e):
    return float(0.5 * e @ (P.H @ e / P.d))

def battery(alpha, m, eps, rng, nsched=40, maxops=400000):
    adj, seed = zoo.star(m)
    P = Prob(adj, alpha, seed)
    c_a, g_a = params(alpha)
    pim = P.pi
    phim = star_modes(m)
    Phi0 = phi_of(P, pim)
    Bm = math.sqrt(2*Phi0/(1+c_a))
    cap = 2*math.sqrt(alpha*(1+alpha))
    LB_Nc = (pim[0] - eps*m) / cap
    om = omega_star(alpha)
    res = []
    viol = dict(P1=0.0, P2=0.0, P3=0.0, P4=0)

    def sched_iter(name):
        """yields (u, omega) generators for named schedules"""
        if name == 'sor_alt':
            while True:
                yield (0, om)
                for l in range(1, m+1): yield (l, om)
        if name == 'gs_alt':
            while True:
                yield (0, 1.0)
                for l in range(1, m+1): yield (l, 1.0)
        if name.startswith('fix_'):
            w = float(name[4:])
            while True:
                yield (0, w)
                for l in range(1, m+1): yield (l, w)
        if name == 'near2':                       # omega -> 2 pumping
            w = 2 - 1e-6
            while True:
                yield (0, w)
                for l in range(1, m+1): yield (l, w)
        if name == 'near2_alpha':                 # omega = 2 - alpha
            w = max(1e-9, 2 - alpha)
            while True:
                yield (0, w)
                for l in range(1, m+1): yield (l, w)
        if name == 'cheb':                        # varying omega, Chebyshev-like
            j = 0
            lam = (1-math.sqrt(alpha))/(1+math.sqrt(alpha))
            while True:
                w = 1.0 + lam*lam*(1 - 0.9*math.cos(2*math.pi*j/17))
                w = min(1.999999, max(1e-6, w))
                yield (0, w)
                for l in range(1, m+1): yield (l, w)
                j += 1
        if name == 'rand':
            while True:
                w = rng.uniform(0.01, 1.999)
                yield (0, w)
                w2 = rng.uniform(0.01, 1.999)
                for l in range(1, m+1): yield (l, w2)
        if name == 'centre_burst':                # many centre ops in a row
            while True:
                for _ in range(5): yield (0, om)
                for l in range(1, m+1): yield (l, om)
        if name == 'leaf_heavy':                  # cheap leaf ops, few centre ops
            while True:
                yield (0, om)
                for _ in range(4):
                    for l in range(1, m+1): yield (l, om)
        if name == 'partial_leaf':                # asymmetric: half the leaves
            half = list(range(1, m//2+1)); other = list(range(m//2+1, m+1))
            while True:
                yield (0, om)
                for l in half: yield (l, om)
                yield (0, om)
                for l in other: yield (l, om)
        if name == 'greedy':
            pass

    names = ['sor_alt','gs_alt','fix_0.5','fix_1.5','fix_1.9','near2',
             'near2_alpha','cheb','rand','centre_burst','leaf_heavy',
             'partial_leaf','greedy']
    for name in names:
        st = State(P)
        Nc = 0; done = False
        prevPhi = phi_of(P, pim - st.z)
        it = None if name == 'greedy' else sched_iter(name)
        for k in range(maxops):
            if name == 'greedy':
                # Gauss-Southwell on |r_u|/sqrt(d_u), omega = omega_*
                sc = np.abs(st.r)/np.sqrt(P.d)
                u = int(np.argmax(sc)); w = om
            else:
                u, w = next(it)
            e_before = pim - st.z
            r_before = st.r[u]
            Phi_b = phi_of(P, e_before)
            st.op(u, w)
            e_after = pim - st.z
            Phi_a = phi_of(P, e_after)
            # P1
            pred = 0.5*w*(2-w)*r_before**2/P.d[u]
            viol['P1'] = max(viol['P1'], abs((Phi_b-Phi_a)-pred)/max(1e-300, abs(pred)+1e-30))
            # P2
            ym = float((e_after/np.sqrt(P.d)) @ phim)
            viol['P2'] = max(viol['P2'], abs(ym)/Bm)
            if u == 0:
                Nc += 1
                viol['P3'] = max(viol['P3'], abs(w*r_before)/cap)
            if P.err(st.z) <= eps:
                done = True; break
        if done and Nc < LB_Nc - 1e-9: viol['P4'] += 1
        res.append(dict(name=name, done=done, Nc=Nc, W=st.W, nops=st.nops))
    return P, dict(Phi0=Phi0, Bm=Bm, cap=cap, LB_Nc=LB_Nc,
                   LB_W=LB_Nc*m, viol=viol, res=res, m=m, eps=eps, alpha=alpha)

if __name__ == '__main__':
    rng = np.random.default_rng(5)
    print('='*100)
    print('E3  full star: pathwise inequalities + schedule battery.  m = 1/(8 eps)')
    print('='*100)
    allout = []
    for e in (6, 8, 10, 12):
        alpha = 2.0**-e
        for eps in (2.0**-5, 2.0**-6):
            m = int(1/(8*eps))
            P, D = battery(alpha, m, eps, rng)
            v = D['viol']
            print(f"alpha=2^-{e:<2d} eps=2^-{int(-math.log2(eps)):<2d} m={m:<4d}  "
                  f"Phi0={D['Phi0']:.4e} cap={D['cap']:.4e} LB_Nc={D['LB_Nc']:.2f} "
                  f"LB_W={D['LB_W']:.1f}")
            print(f"   max rel dev of energy identity (P1) : {v['P1']:.3e}")
            print(f"   max |yhat_-| / B_-            (P2) : {v['P2']:.4f}   (must be <= 1)")
            print(f"   max |w r_c| / cap             (P3) : {v['P3']:.4f}   (must be <= 1)")
            print(f"   schedules violating N_c >= LB (P4) : {v['P4']}")
            row = []
            for r in D['res']:
                row.append(f"{r['name']}:{'ok' if r['done'] else 'INC'} "
                           f"Nc={r['Nc']} W={r['W']:.0f} Nc/LB={r['Nc']/D['LB_Nc']:.2f}")
            print('   ' + ' | '.join(row))
            allout.append(D)
    json.dump([{k: (v if k != 'res' else v) for k, v in D.items()} for D in allout],
              open('out/verify.json','w'), indent=1, default=str)
