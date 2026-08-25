"""Part 3: can the instance be repaired so the semantic task is nontrivial
while keeping the wave and Omega(1/(alpha*eps))?

Repair A (calibrated center seed):  theta_run = 2*sqrt(a) (fixed ratio C=2),
   shorter arms L = ceil(0.2/sqrt(a)) so zeta = lam^{2L} ~ e^{-0.8} keeps
   u0 > eps.  S_eps nonempty (center + arm prefix), bypass tau*k=2>1 holds.
Repair B (pendant seed): fixed theta = 1/8, eps = gamma_alpha,
   k = round(theta/eps), L = M+1, seed at pendant p of degree 1 on center.
Band point: the original construction at non-dyadic alpha inside
   [0.01073, 0.015625) where S_eps is nonempty.
"""
import math, sys
import numpy as np
sys.path.insert(0, "/home/claude/work/overnight/i5a")
from common import pars, spider_scales, build_spider, solve_pi, \
    cf_push_fifo, semantic_err, cert_gap

print("=" * 78)
print("REPAIR A: center seed, theta_run=2*sqrt(a), L=ceil(0.2/sqrt(a)), k=64")
print("=" * 78)
k = 64
print(f"{'alpha':>7} {'L':>5} {'u0/eps':>8} {'|S_eps|':>8} {'volS':>6} "
      f"{'W1':>6} {'W2':>9} {'W*a*e':>9} {'W*sqa*e':>9} {'err0/eps':>9}")
for j in range(4, 13):
    alpha = 2.0 ** (-j)
    t, lam, c, g, wstar = pars(alpha)
    theta_run = 2 * t
    eps = theta_run / k
    tau = eps / t          # tau*k = 2 > 1: Phase-I bypass at the center
    L = int(math.ceil(0.2 / t))
    adj, posm = build_spider(k, L)
    pi, d = solve_pi(adj, alpha, 0)
    u = pi / d
    S = u >= eps
    res = cf_push_fifo(adj, alpha, 0, eps, tau)
    W = res['W1'] + res['W2']
    print(f"2^-{j:<4} {L:>5} {u[0]/eps:>8.4f} {int(S.sum()):>8} "
          f"{int(d[S].sum()):>6} {res['W1']:>6} {res['W2']:>9} "
          f"{W*alpha*eps:>9.4f} {W*t*eps:>9.4f} {u.max()/eps:>9.4f}")
print("  [S_eps nonempty incl. arm prefix; if W*a*e decays while W*sqa*e is"
      " ~flat, the Omega(1/(alpha*eps)) does NOT survive this calibration]")

print()
print("=" * 78)
print("REPAIR B: pendant seed, theta=1/8, eps=gamma_a, k=round(theta/eps), "
      "L=M+1")
print("=" * 78)
theta = 0.125
print(f"{'alpha':>7} {'k':>5} {'L':>4} {'u_p/eps':>8} {'u_v/eps':>8} "
      f"{'|S_eps|':>8} {'W1':>4} {'W2':>10} {'W*a*e':>8} "
      f"{'intp/[kM(M+1)/2]':>17} {'err(zp)/eps':>12}")
for j in range(6, 13):
    alpha = 2.0 ** (-j)
    t, lam, c, g, wstar = pars(alpha)
    eps = g
    kk = int(round(theta / eps))
    tau = eps / t
    _, M, L = spider_scales(alpha, theta)
    adj, posm = build_spider(kk, L, pendant=True)
    p = 1 + kk * L
    pi, d = solve_pi(adj, alpha, p)
    u = pi / d
    S = u >= eps
    Sset = [posm[i] for i in np.where(S)[0]]
    # single-write semantic output: z = pi_p e_p
    zp = np.zeros(len(adj)); zp[p] = pi[p]
    ep = semantic_err(zp, pi, d)
    res = cf_push_fifo(adj, alpha, p, eps, tau, log_pushes=True)
    W = res['W1'] + res['W2']
    intp = sum(1 for (uu, s_) in res['pushes']
               if posm[uu] not in ('c', 'p'))
    floor = kk * M * (M + 1) // 2
    print(f"2^-{j:<4} {kk:>5} {L:>4} {u[p]/eps:>8.4f} {u[0]/eps:>8.4f} "
          f"{int(S.sum()):>8} {res['W1']:>4} {res['W2']:>10} "
          f"{W*alpha*eps:>8.4f} {intp/floor:>17.3f} {ep/eps:>12.5f}")
    if j == 8:
        print(f"        S_eps content: {Sset};  z=0 err/eps = "
              f"{u.max()/eps:.4f} (INVALID);  cert(z=0) gap = "
              f"{cert_gap(adj, alpha, np.zeros(len(adj)), p, eps)[0]:.1f}")
print("  [u_p/eps>1: z=0 invalid; err(zp)/eps<1: ONE output write is a valid"
      " semantic answer; W*a*e ~flat: Omega(1/(alpha*eps)) survives;")
print("   intp/[kM(M+1)/2] >= 1: triangular wave count intact]")

print()
print("=" * 78)
print("BAND POINTS: original construction, non-dyadic alpha in the nonempty "
      "band (theta=1/8, k=64)")
print("=" * 78)
theta, k = 0.125, 64
eps = theta / k
print(f"{'alpha':>8} {'sqrt(a)':>8} {'u0/eps':>8} {'|S_eps|':>8} {'W':>8} "
      f"{'W*a*e':>8} {'bypass tau*k':>12}")
for alpha in (0.0110, 0.0120, 0.0135, 0.0150):
    t, lam, c, g, wstar = pars(alpha)
    tau = eps / t
    _, M, L = spider_scales(alpha, theta)
    adj, posm = build_spider(k, L)
    pi, d = solve_pi(adj, alpha, 0)
    u = pi / d
    res = cf_push_fifo(adj, alpha, 0, eps, tau)
    W = res['W1'] + res['W2']
    print(f"{alpha:>8.4f} {t:>8.4f} {u[0]/eps:>8.4f} "
          f"{int((u>=eps).sum()):>8} {W:>8} {W*alpha*eps:>8.4f} "
          f"{tau*k:>12.3f}")
print("  [band exists only at alpha in [0.0107, 0.0156): a fixed window, "
      "no alpha->0 family]")
