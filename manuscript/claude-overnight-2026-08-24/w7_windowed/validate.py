"""Validate the reconstruction against exact facts from Rounds 026/027 + P4/P3."""
import sys, time
from fractions import Fraction as Fr
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from engine import Inst, complete_graph, path_graph, Jseq
import math

ASTAR = Fr(6929307, 98509850)

def k8_pulse():
    print("=== V1: K_8 reachable pulse (Round 026, q=1/10, alpha=1/101) ===")
    adj = complete_graph(8)
    s = [Fr(363437, 651088)] + [Fr(41093, 651088)] * 7
    I = Inst(adj, s, q=Fr(1, 10), rho=Fr(1, 112), alpha=Fr(1, 101))
    # known targets
    x1_t = [Fr(11009, 22788080)] + [Fr(3763, 113940400)] * 7
    x2_t = [Fr(89111, 81386000)] + [Fr(10523, 81386000)] * 7
    g2_t = Fr(57072309867, 51440146040)
    g3_t = Fr(192036347475007, 168765931042095)
    D2_t = Fr(191403, 1253344400)
    ratio_t = Fr(48663286609745269, 139594225)
    xs_t = [Fr(5693, 569702)] + [Fr(2500, 284851)] * 7
    print("  x* matches:", I.xstar == xs_t)
    recs = I.run(8, bankA=ASTAR)
    # replay x_1, x_2 by re-running and capturing states: recompute directly
    x1 = I.obstacle_solve(I.ct, I.kappa, [Fr(0)] * 8)
    # stage1: d = x1, a = x1 + beta x1, check N, then solve
    word = ''.join(r['cls'] for r in recs)
    print("  word[0:8]:", word, " (target N N P F N N ...)")
    print("  x_1 matches:", x1 == x1_t)
    # x_2: from run with ell_1
    be = I.beta
    a1 = [x1[i] + be * x1[i] for i in range(8)]
    # stage 1 had class N so ell_1 = a1
    x2 = I.obstacle_solve(I.ct, I.kappa, a1)
    print("  x_2 matches:", x2 == x2_t)
    print("  Delta_2 matches:", recs[2]['Delta'] == D2_t,
          "(got", recs[2]['Delta'], ")")
    print("  gamma_2 matches:", recs[2]['gamma'] == g2_t,
          "(got", recs[2]['gamma'], ")")
    print("  gamma_3 matches:", recs[3]['gamma'] == g3_t)
    al = I.alpha
    r_ratio = recs[2]['Dfin'] / (al**2 * recs[2]['Delta']**2)
    print("  Dfin_2/(al^2 Del_2^2) matches:", r_ratio == ratio_t,
          "(got", r_ratio, ")")
    J = Jseq(recs)
    print("  J_8 = %.6f < 2log2 = %.6f: %s" %
          (J[-1], 2 * math.log(2), J[-1] < 2 * math.log(2)))
    ok = (I.xstar == xs_t and x1 == x1_t and x2 == x2_t and
          recs[2]['Delta'] == D2_t and recs[2]['gamma'] == g2_t and
          recs[3]['gamma'] == g3_t and r_ratio == ratio_t and
          word.startswith('NNPFNN'))
    print("  V1 OVERALL:", "PASS" if ok else "FAIL")
    return ok

def k2_family(n=100):
    print("=== V2: K_2 family (Round 027, q=1/%d) ===" % n)
    adj = [[1], [0]]
    q = Fr(1, n)
    I = Inst(adj, [Fr(1, 2), Fr(1, 2)], q=q, rho=Fr(1, 16))
    ok = True
    t1 = I.xstar == [Fr(7, 16), Fr(7, 16)]
    print("  x* = 7/16*(1,1):", t1); ok &= t1
    T = 8
    recs = I.run(T, bankA=ASTAR)
    word = ''.join(r['cls'] for r in recs)
    t2 = word == 'N' * T
    print("  no corrections (word=%s):" % word, t2); ok &= t2
    # e_t = (1+tq)(1-q)^t e_0  -> e2 = dotD(e,e) = (1+tq)^2 (1-q)^{2t} S
    S = I.dotD(I.xstar, I.xstar)
    t3 = all(recs[t]['e2'] == (1 + t * q)**2 * (1 - q)**(2 * t) * S
             for t in range(T))
    print("  e_t = (1+tq)(1-q)^t e_0:", t3); ok &= t3
    # Phi_t closed form (mu/2)(1-q)^{2t}((1+tq)^2+1) S
    t4 = all(recs[t]['Phi'] == I.mu / 2 * (1 - q)**(2 * t) *
             ((1 + t * q)**2 + 1) * S for t in range(T))
    print("  Phi_t closed form:", t4); ok &= t4
    t5 = all(recs[t]['EQ'] == I.alpha * (1 - q)**(2 * t) * (1 + t * q)**2 * S
             for t in range(T))
    print("  EQ_t closed form:", t5); ok &= t5
    # Psi_3/Psi_2 identity
    th, bq, A = 1 - q, (1 - q * q) / 2, ASTAR
    tgt = th**2 * (bq * th**2 * ((1 + 3 * q)**2 + 1) + (A / q) * (1 + 2 * q)**2) \
        / (bq * th**2 * ((1 + 2 * q)**2 + 1) + (A / q) * (1 + q)**2)
    got = recs[3]['Psi'] / recs[2]['Psi']
    t6 = got == tgt
    print("  Psi_3/Psi_2 exact identity:", t6); ok &= t6
    loss = 1 - got
    bound = (4 + 2 / ASTAR) * q * q
    t7 = 0 <= loss <= bound
    print("  0 <= 1-Psi3/Psi2 = %.3e <= (4+2/A*)q^2 = %.3e:" %
          (float(loss), float(bound)), t7); ok &= t7
    print("  V2 OVERALL:", "PASS" if ok else "FAIL")
    return ok

def k8_qfam(q=Fr(1, 100)):
    print("=== V3: K_8 small-q family (Round 026, q=%s) ===" % q)
    adj = complete_graph(8)
    al = q * q / (1 + q * q)
    lam_h = (4 + 3 * al) / 7
    # s_i = (1/16)(1 + (Q e0)_i/alpha), e0 = 1 + 12q^2 v
    v = [Fr(1)] + [Fr(-1, 7)] * 7
    Qe0 = [al + 12 * q * q * lam_h * v[i] for i in range(8)]
    s = [(1 + Qe0[i] / al) / 16 for i in range(8)]
    ok = all(x > 0 for x in s) and sum(s) == 1
    print("  s > 0, sums to 1:", ok)
    I = Inst(adj, s, q=q, rho=Fr(1, 112))
    e0 = [1 + 12 * q * q * v[i] for i in range(8)]
    t1 = I.xstar == [e0[i] / 112 for i in range(8)]
    print("  x*hat = e0/112:", t1); ok &= t1
    recs = I.run(6)
    word = ''.join(r['cls'] for r in recs)
    t2 = word.startswith('NNF')
    print("  word = %s (target NNF...):" % word, t2); ok &= t2
    S0 = Fr(7, 112**2)
    t3 = recs[2]['Dfin'] > 28 * q * S0
    print("  Dfin_2 > 28q*7/112^2:", t3, "(Dfin_2 = %.6e, bound %.6e)" %
          (float(recs[2]['Dfin']), float(28 * q * S0))); ok &= t3
    drop = recs[1]['EQ'] - recs[2]['EQ']
    t4 = drop < 197 * q**4 * S0
    print("  EQ_1-EQ_2 < 197q^4*7/112^2:", t4, "(drop %.6e, bound %.6e)" %
          (float(drop), float(197 * q**4 * S0))); ok &= t4
    rat = recs[2]['Dfin'] / drop
    t5 = rat > 28 / (197 * q**3)
    print("  Dfin_2/drop = %.4e > 28/(197q^3) = %.4e:" %
          (float(rat), float(28 / (197 * q**3))), t5); ok &= t5
    t6 = recs[2]['gamma'] > 1
    print("  gamma_2 = %.6f > 1:" % float(recs[2]['gamma']), t6); ok &= t6
    print("  gam list:", [float(r['gamma']) for r in recs])
    print("  V3 OVERALL:", "PASS" if ok else "FAIL")
    return ok

if __name__ == '__main__':
    t0 = time.time()
    r1 = k8_pulse()
    r2 = k2_family(100)
    r3 = k8_qfam(Fr(1, 100))
    print("elapsed %.1fs" % (time.time() - t0))
    print("SUMMARY: V1=%s V2=%s V3=%s" % (r1, r2, r3))
