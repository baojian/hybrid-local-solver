"""E5: two-sided Theta on the star.  m = 1/(8 eps); oracle (semantic) stop.
Symmetric-block simulator (exact 2-dim reduction, verified against the full
star in E3), so large m is cheap.  Work = m per block."""
import math, json
import numpy as np
from core import params, omega_star

def work_blocks(alpha, tm, w_of_j, cap=4_000_000):
    c, g = params(alpha); pic = (1+alpha)/2.0
    ec, EL = pic, c*pic
    for N in range(1, cap+1):
        w = w_of_j(N-1)
        if N % 2 == 1: ec = (1-w)*ec + w*c*EL
        else:          EL = (1-w)*EL + w*c*ec
        if max(abs(ec), abs(EL)) <= tm: return N
    return None

print('='*104)
print('E5  centre-seeded star K_{1,m}, m = floor(1/(8 eps)) : two-sided Theta(1/(sqrt(a) eps))')
print('    LB (proved, whole class R+/-) : W >= m*(pi_c - eps m)/(2 sqrt(a(1+a)))')
print('    UB (member)                   : alternating blocks, omega -> 2  /  omega = omega_*')
print('='*104)
print(f"{'alpha':>11s} {'eps':>10s} {'m':>7s} {'LB_W':>10s} {'W(w*)':>10s} "
      f"{'W(near2)':>10s} {'UB/LB':>7s} {'LB*sqa*eps':>11s} {'W(near2)*sqa*eps':>17s} "
      f"{'vol(S_eps)':>10s}")
rows=[]
for e in (6, 8, 10, 12, 14):
    alpha = 2.0**-e; sa = math.sqrt(alpha); om = omega_star(alpha)
    for ee in (5, 7, 9):
        eps = 2.0**-ee; m = int(1/(8*eps)); tm = eps*m
        pic = (1+alpha)/2
        LB_Nc = (pic - tm)/(2*math.sqrt(alpha*(1+alpha)))
        LB_W = m*LB_Nc
        N1 = work_blocks(alpha, tm, lambda j, om=om: om)
        N2 = work_blocks(alpha, tm, lambda j: 2-1e-12)
        W1, W2 = (N1*m if N1 else None), (N2*m if N2 else None)
        vol = 2*m
        print(f"{alpha:11.3e} {eps:10.5f} {m:7d} {LB_W:10.1f} {str(W1):>10s} "
              f"{str(W2):>10s} {(W2/LB_W if W2 else float('nan')):7.2f} "
              f"{LB_W*sa*eps:11.5f} {(W2*sa*eps if W2 else float('nan')):17.5f} "
              f"{vol:10d}")
        rows.append(dict(alpha=alpha, eps=eps, m=m, LB_W=LB_W, W_sor=W1, W_near2=W2))
json.dump(rows, open('out/sweep.json','w'), indent=1)
print()
print('  flat  LB*sqa*eps  and  W*sqa*eps  columns  =>  both sides are Theta(1/(sqrt(a) eps)).')
