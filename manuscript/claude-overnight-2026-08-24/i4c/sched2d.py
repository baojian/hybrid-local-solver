"""E2: star K_{1,m} reduced 2-dim error dynamics.  Minimum #blocks over
omega-schedules, vs the proved LB N_c >= (pi_c - eps m)/(2 sqrt(a(1+a))).

Error map (e_c, E_L), e_0 = pi_c (1, c_a),  c=c_a:
   centre op(w): e_c <- (1-w) e_c + w c E_L
   leaf   op(w): E_L <- (1-w) E_L + w c e_c
Target |e_c| <= eps*m and |E_L| <= eps*m  with m = 1/(8 eps) => eps*m = 1/8.
"""
import math, json
import numpy as np
from scipy.optimize import minimize
from core import params, omega_star

def rollout(alpha, pat, ws):
    c, g = params(alpha)
    pic = (1+alpha)/2.0
    ec, EL = pic, c*pic
    hist = []
    for ch, w in zip(pat, ws):
        if ch == 'C': ec = (1-w)*ec + w*c*EL
        else:         EL = (1-w)*EL + w*c*ec
        hist.append((ec, EL))
    return ec, EL, hist

def alt(N, start='C'):
    return ''.join((start if i%2==0 else ('L' if start=='C' else 'C')) for i in range(N))

def n_blocks(alpha, ws_fn, tm=0.125, cap=400000):
    """#blocks for an alternating schedule whose j-th omega is ws_fn(j)."""
    c, g = params(alpha); pic = (1+alpha)/2.0
    ec, EL = pic, c*pic
    for N in range(1, cap+1):
        w = ws_fn(N-1)
        if N % 2 == 1: ec = (1-w)*ec + w*c*EL
        else:          EL = (1-w)*EL + w*c*ec
        if max(abs(ec), abs(EL)) <= tm: return N
    return None

def cheb_omegas(alpha):
    """Golub-Varga cyclic-Chebyshev semi-iteration realised as variable SOR."""
    rho, _ = params(alpha)
    w = 1.0
    ws = []
    for _ in range(400000):
        ws.append(w)
        w = 1.0/(1.0 - rho*rho*w/4.0)
    return ws

def opt_min_blocks(alpha, tm=0.125, Nmax=3000, rng=None, tries=6):
    """warm-started decreasing search for the minimum feasible N."""
    def obj(x, pat):
        ws = 2.0/(1.0+np.exp(-x))
        ec, EL, _ = rollout(alpha, pat, ws)
        return max(abs(ec), abs(EL))/tm
    # upper bracket: chebyshev
    cw = cheb_omegas(alpha)
    Nhi = n_blocks(alpha, lambda j: cw[j], tm)
    if Nhi is None or Nhi > Nmax: return None, None, Nhi
    best = Nhi; bestw = None
    N = Nhi
    while N > 1:
        Ntry = N - 1
        pat = alt(Ntry)
        starts = [np.log(np.clip(np.array(cw[:Ntry]),1e-9,2-1e-9)/(2-np.clip(np.array(cw[:Ntry]),1e-9,2-1e-9)))]
        om = omega_star(alpha)
        starts.append(np.full(Ntry, math.log(om/(2-om))))
        if bestw is not None and len(bestw) >= Ntry:
            bw = np.clip(bestw[:Ntry], 1e-9, 2-1e-9)
            starts.append(np.log(bw/(2-bw)))
        for _ in range(tries):
            starts.append(rng.normal(1.0, 2.0, Ntry))
        ok = False
        for s0 in starts:
            s0 = np.clip(np.asarray(s0,dtype=float), -14, 14)
            r = minimize(obj, s0, args=(pat,), method='L-BFGS-B',
                         options=dict(maxiter=3000, maxfun=6000))
            if r.fun < 1.0:
                best = Ntry; bestw = 2.0/(1.0+np.exp(-r.x)); ok = True; break
        if not ok: break
        N = Ntry
    return best, bestw, Nhi

if __name__ == '__main__':
    rng = np.random.default_rng(3)
    tm = 0.125
    print('='*112)
    print('E2  star, 2-dim exact reduction: MIN #blocks over omega-schedules   (each block costs m; eps*m = 1/8)')
    print('='*112)
    print(f"{'alpha':>12s} {'1/sqrt(a)':>9s} {'N_sor(w*)':>9s} {'N_cheb':>7s} "
          f"{'N_opt':>7s} {'LB_Nc(proved)':>13s} {'N_opt/(1/sqa)':>13s} "
          f"{'N_sor/(1/sqa)':>13s} {'N_opt/LB':>9s} {'max w':>8s}")
    rows=[]
    for e in range(6, 15):
        alpha = 2.0**-e
        sa = math.sqrt(alpha)
        om = omega_star(alpha)
        Nsor = n_blocks(alpha, lambda j, om=om: om, tm)
        cw = cheb_omegas(alpha)
        Ncheb = n_blocks(alpha, lambda j: cw[j], tm)
        Nopt, wopt, _ = (None, None, None)
        if Ncheb is not None and Ncheb <= 2500:
            Nopt, wopt, _ = opt_min_blocks(alpha, tm, rng=rng)
        pic = (1+alpha)/2.0
        LB = (pic - tm)/(2*math.sqrt(alpha*(1+alpha)))
        mw = (max(wopt) if wopt is not None else float('nan'))
        print(f"{alpha:12.4e} {1/sa:9.2f} {str(Nsor):>9s} {str(Ncheb):>7s} "
              f"{str(Nopt):>7s} {LB:13.2f} "
              f"{(Nopt*sa if Nopt else float('nan')):13.3f} "
              f"{(Nsor*sa if Nsor else float('nan')):13.3f} "
              f"{(Nopt/LB if Nopt else float('nan')):9.3f} {mw:8.5f}")
        rows.append(dict(alpha=alpha, Nsor=Nsor, Ncheb=Ncheb, Nopt=Nopt, LB=LB,
                         ws=(list(map(float,wopt)) if wopt is not None else None)))
    json.dump(rows, open('out/sched2d.json','w'), indent=1)
    print()
    print('  N_sor*sqrt(a) growing  => SOR(w*) is Theta(log(1/a)/sqrt(a)).')
    print('  N_opt*sqrt(a) flat     => the true class optimum is Theta(1/sqrt(a)) and the LB is tight.')
