"""E4: the general-graph form of the seed-op lower bound, and its verification.

  Phi_0 = gamma_a pi_v / (2 d_v)   (exact, since e_0 = pi, r_0 = gamma_a e_v)
  for any spectral projector P = P_{>= mu0} of H_sym = I - c_a D^{-1/2}AD^{-1/2}:
      |Delta z_v| = w|r_v| <= 2 sqrt(gamma_a pi_v / mu0) / ||P e_v||
  => N_v >= (pi_v - eps d_v) / cap_v ,   W >= d_v N_v.
Also E4.b: high-precision check of the energy identity (P1) with mpmath.
"""
import math, os, sys, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lib'))
import zoo
from core import Prob, State, omega_star, params

def cap_v(P, v):
    """best per-seed-op displacement cap over spectral thresholds mu0."""
    n = P.n
    Hs = (np.eye(n) - P.c_a * (np.diag(1/np.sqrt(P.d)) @ P.A.toarray() @ np.diag(1/np.sqrt(P.d))))
    mu, V = np.linalg.eigh(Hs)
    w = V[v, :]**2                       # |<phi_k, e_v>|^2
    Phi0 = 0.5*P.g_a*P.pi[v]/P.d[v]
    best = np.inf; bmu = None
    order = np.argsort(mu)
    for i in range(n):
        mu0 = mu[order[i]]
        if mu0 <= 1e-14: continue
        Pn = math.sqrt(w[order[i:]].sum())
        if Pn < 1e-12: continue
        c = 2*math.sqrt(P.d[v])*math.sqrt(2*Phi0/mu0)/Pn
        if c < best: best, bmu = c, mu0
    return best, bmu, Phi0, mu, V

def run_batch(name, adj, seed, alpha, eps, scheds, rng, maxops=200000):
    P = Prob(adj, alpha, seed)
    cap, mu0, Phi0, mu, V = cap_v(P, seed)
    LB_Nv = max(0.0, (P.pi[seed] - eps*P.d[seed]))/cap
    out = []
    for sname, gen in scheds.items():
        st = State(P); Nv = 0; capviol = 0.0; done = False
        it = gen(P)
        for k in range(maxops):
            u, w = next(it) if not callable(gen) or True else (None, None)
            rb = st.r[u]
            st.op(u, w)
            if u == seed:
                Nv += 1
                capviol = max(capviol, abs(w*rb)/cap)
            if P.err(st.z) <= eps: done = True; break
        out.append(dict(s=sname, done=done, Nv=Nv, W=st.W, capviol=capviol,
                        ok=(not done) or Nv >= LB_Nv - 1e-9))
    return P, cap, mu0, LB_Nv, out

def mk_scheds(alpha, rng):
    om = omega_star(alpha)
    def alt(w):
        def g(P):
            n = P.n
            while True:
                for u in range(n): yield (u, w)
        return g
    def randsched(P):
        n = P.n
        while True:
            yield (int(rng.integers(0, n)), float(rng.uniform(0.02, 1.98)))
    def greedy(P):
        while True:
            pass
    def gs_greedy(P):
        while True:
            sc = np.abs(P.dummy_r)/1
            yield (0, 1.0)
    return {'sweep_w*': alt(om), 'sweep_1': alt(1.0), 'sweep_1.99': alt(1.99),
            'sweep_near2': alt(2-1e-8), 'random': randsched}

if __name__ == '__main__':
    rng = np.random.default_rng(7)
    print('='*110)
    print('E4.a  general-graph seed-op bound:  N_v >= (pi_v - eps d_v)/cap_v ,  cap_v from the fast-mode cap')
    print('='*110)
    print(f"{'graph':>18s} {'alpha':>10s} {'eps':>9s} {'d_v':>5s} {'pi_v':>8s} "
          f"{'pi_v/g_a':>9s} {'cap_v':>9s} {'2sqrt(a)':>9s} {'LB_Nv':>8s} "
          f"{'LB_W':>9s} {'min Nv obs':>10s} {'max cap use':>11s} {'viol':>5s}")
    fams = []
    for m in (8, 16, 32):
        fams.append((f'star({m})',) + zoo.star(m))
    fams.append(('path(40)',) + zoo.path(40))
    fams.append(('spider(4,10)',) + zoo.spider(4, 10))
    fams.append(('spider(16,4)',) + zoo.spider(16, 4))
    fams.append(('cater(10)',) + zoo.caterpillar(10))
    fams.append(('bintree(4)',) + zoo.binary_tree(4))
    fams.append(('grid(6,6)',) + zoo.grid(6, 6))
    fams.append(('rrt(30,3)',) + zoo.random_regular(30, 3))
    fams.append(('complete(12)',) + zoo.complete(12))
    nviol = 0; rows=[]
    for (gname, adj, seed) in fams:
        for e in (6, 10):
            alpha = 2.0**-e
            P0 = Prob(adj, alpha, seed)
            eps = float(P0.pi[seed]/P0.d[seed]/4.0)     # keeps the seed well inside S_eps
            scheds = mk_scheds(alpha, rng)
            P, cap, mu0, LB, out = run_batch(gname, adj, seed, alpha, eps, scheds, rng)
            bad = [o for o in out if not o['ok']]
            nviol += len(bad)
            minNv = min([o['Nv'] for o in out if o['done']], default=-1)
            mcap = max(o['capviol'] for o in out)
            print(f"{gname:>18s} {alpha:10.3e} {eps:9.3e} {P.d[seed]:5.0f} "
                  f"{P.pi[seed]:8.4f} {P.pi[seed]/P.g_a:9.2f} {cap:9.4f} "
                  f"{2*math.sqrt(alpha):9.4f} {LB:8.2f} {LB*P.d[seed]:9.1f} "
                  f"{minNv:10d} {mcap:11.4f} {len(bad):5d}")
            rows.append(dict(g=gname, alpha=alpha, eps=eps, cap=cap, LB=LB,
                             minNv=minNv, maxcap=mcap, nbad=len(bad)))
    print(f'  -> total violations of the per-op cap or of N_v >= LB : {nviol}')
    json.dump(rows, open('out/general.json','w'), indent=1)

    print()
    print('='*110)
    print('E4.b  high-precision check of the energy identity  Phi(e)-Phi(e+) = [w(2-w)/2] r_u^2/d_u')
    print('='*110)
    try:
        from mpmath import mp, mpf
        mp.dps = 60
        for e in (6, 12):
            alpha = 2.0**-e
            adj, seed = zoo.star(8)
            n = len(adj); d = [mpf(len(adj[u])) for u in range(n)]
            c_a = (1-mpf(2)**-e)/(1+mpf(2)**-e); g_a = 2*mpf(2)**-e/(1+mpf(2)**-e)
            # exact pi on the star
            pic = (1+mpf(2)**-e)/2; pil = c_a*pic/8
            pi = [pic] + [pil]*8
            z = [mpf(0)]*n; r = [mpf(0)]*n; r[seed] = g_a
            def Phi():
                E = [pi[i]-z[i] for i in range(n)]
                s = mpf(0)
                for i in range(n):
                    s += E[i]*E[i]/d[i]
                    for w_ in adj[i]:
                        s -= c_a*E[i]*E[w_]/(d[i]*d[w_])
                return s/2
            worst = mpf(0)
            rr = np.random.default_rng(2)
            for k in range(200):
                u = int(rr.integers(0, n)); w = mpf(float(rr.uniform(0.001, 1.999)))
                pb = Phi(); rb = r[u]
                delta = w*r[u]; z[u] += delta; r[u] -= delta
                for ww in adj[u]: r[ww] += c_a*delta/d[u]
                pa = Phi()
                pred = w*(2-w)/2*rb*rb/d[u]
                if pred != 0:
                    worst = max(worst, abs((pb-pa)-pred)/abs(pred))
            print(f'  alpha=2^-{e}: max relative deviation over 200 random signed ops '
                  f'(60 dps) = {mp.nstr(worst, 5)}')
    except ImportError:
        print('  mpmath unavailable; skipped')
