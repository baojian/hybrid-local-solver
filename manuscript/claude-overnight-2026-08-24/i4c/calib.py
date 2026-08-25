"""E1: calibration.  (a) Does the candidate family have a nontrivial output?
   (b) Is one forward SOR(omega_*) sweep on a path an EXACT solve?"""
import math, sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lib'))
import zoo
from core import Prob, State, omega_star, lam_of

def hdr(s): print('='*78); print(s); print('='*78)

hdr('E1.a  candidate families: is S_eps nonempty / saturating?  (theta = eps*k)')
print(f"{'family':>22s} {'alpha':>10s} {'eps':>10s} {'vol(S_eps)':>11s} "
      f"{'|S|':>6s} {'vol*eps':>8s} {'vol(G)':>8s} {'pi_v/d_v/eps':>13s}")
rows=[]
for alpha in (2.0**-6, 2.0**-8, 2.0**-10, 2.0**-12):
    t = math.sqrt(alpha)
    theta = 0.125
    # manuscript long spider: k = theta/eps arms, L = Theta(1/sqrt(alpha))
    for eps in (2.0**-6, 2.0**-8):
        k = max(2, int(theta/eps))
        L = max(2, int(round(1.0/t)))
        if k*L > 90000: continue
        adj, seed = zoo.spider(k, L)
        P = Prob(adj, alpha, seed)
        v, ns = P.vol_S_eps(eps)
        print(f"{'spider(k=t/e,L=1/sqa)':>22s} {alpha:10.6g} {eps:10.6g} {v:11.1f} "
              f"{ns:6d} {v*eps:8.3f} {2*k*L:8d} {P.pi[seed]/P.d[seed]/eps:13.4f}")
        rows.append(('spider_manuscript',alpha,eps,v*eps))
    # star K_{1,m}, m = 1/(8 eps)
    for eps in (2.0**-6, 2.0**-8, 2.0**-10):
        m = int(1.0/(8*eps))
        adj, seed = zoo.star(m)
        P = Prob(adj, alpha, seed)
        v, ns = P.vol_S_eps(eps)
        print(f"{'star(m=1/8e)':>22s} {alpha:10.6g} {eps:10.6g} {v:11.1f} "
              f"{ns:6d} {v*eps:8.3f} {2*m:8d} {P.pi[seed]/P.d[seed]/eps:13.4f}")
    # path seeded at end, long
    for eps in (2.0**-8,):
        n = min(20000, int(6.0/t))
        adj, seed = zoo.path(n)
        P = Prob(adj, alpha, seed)
        v, ns = P.vol_S_eps(eps)
        print(f"{'path(6/sqa)':>22s} {alpha:10.6g} {eps:10.6g} {v:11.1f} "
              f"{ns:6d} {v*eps:8.3f} {2*n:8d} {P.pi[seed]/P.d[seed]/eps:13.4f}")
    # spider tuned so S_eps saturates:  k = sqrt(alpha)/(4 eps)
    for eps in (2.0**-8,):
        k = max(2, int(t/(4*eps)))
        L = max(2, int(round(1.0/t)))
        if k*L <= 90000:
            adj, seed = zoo.spider(k, L)
            P = Prob(adj, alpha, seed)
            v, ns = P.vol_S_eps(eps)
            print(f"{'spider(k=sqa/4e)':>22s} {alpha:10.6g} {eps:10.6g} {v:11.1f} "
                  f"{ns:6d} {v*eps:8.3f} {2*k*L:8d} {P.pi[seed]/P.d[seed]/eps:13.4f}")

hdr('E1.b  one forward SOR(omega_*) sweep on a path = exact solve?')
print(f"{'alpha':>10s} {'n':>7s} {'T (swept)':>9s} {'max|z-pi|/d on [0,T)':>21s} "
      f"{'err(z)':>11s} {'pi_{T}/2':>11s} {'W':>8s} {'vol(S_eps)':>11s}")
for alpha in (2.0**-6, 2.0**-8, 2.0**-10, 2.0**-12):
    t = math.sqrt(alpha); om = omega_star(alpha)
    n = min(30000, int(10.0/t))
    adj, seed = zoo.path(n)
    P = Prob(adj, alpha, seed)
    T = n//2
    st = State(P)
    for j in range(T):
        st.op(j, om)
    loc = float(np.max(np.abs(P.pi[:T]-st.z[:T])/P.d[:T]))
    eps = P.pi[T]/P.d[T]
    v,_ = P.vol_S_eps(eps*0.999)
    print(f"{alpha:10.6g} {n:7d} {T:9d} {loc:21.4e} {P.err(st.z):11.4e} "
          f"{eps:11.4e} {st.W:8.0f} {v:11.1f}")
print('  loc = accuracy INSIDE the swept prefix; if ~1e-15 the sweep is exact there.')

hdr('E1.c  path: work of one-sweep SOR(omega_*) to reach a target eps, vs vol(S_eps)')
print(f"{'alpha':>10s} {'eps':>10s} {'vol(S_eps)':>11s} {'W_sweep':>9s} "
      f"{'W/vol(S)':>9s} {'W*eps':>9s} {'1/(sqa*eps)':>12s}")
for alpha in (2.0**-6, 2.0**-8, 2.0**-10, 2.0**-12):
    t = math.sqrt(alpha); om = omega_star(alpha)
    n = min(40000, int(14.0/t))
    adj, seed = zoo.path(n)
    P = Prob(adj, alpha, seed)
    for eps in (2.0**-10, 2.0**-14):
        v, ns = P.vol_S_eps(eps)
        if v == 0: 
            print(f"{alpha:10.6g} {eps:10.6g} {v:11.1f}   (S_eps empty)")
            continue
        st = State(P); Wt=None
        for j in range(n-1):
            st.op(j, om)
            if st.err() <= eps:
                Wt = st.W; break
        print(f"{alpha:10.6g} {eps:10.6g} {v:11.1f} {str(Wt):>9s} "
              f"{(Wt/v if Wt else float('nan')):9.3f} {(Wt*eps if Wt else float('nan')):9.4f} "
              f"{1.0/(t*eps):12.1f}")
