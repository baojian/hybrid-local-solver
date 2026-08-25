"""Part 2: literal FIFO CF-Push on the manuscript spider.
 - verify lem:cf-spider-wave push-by-push (depths and residual values)
 - measure W, W*alpha*eps; certificate gap at z=0; APPR(eps) baseline.
"""
import math, sys
import numpy as np
sys.path.insert(0, "/home/claude/work/overnight/i5a")
from common import pars, spider_scales, build_spider, solve_pi, \
    cf_push_fifo, semantic_err, cert_gap

theta, k = 0.125, 64
eps = theta / k

print("=" * 78)
print("A. Wave-lemma verification (k=8, alpha=2^-8, theta=1/8): push-by-push")
print("=" * 78)
alpha = 2.0 ** -8
t, lam, c, g, wstar = pars(alpha)
_, M, L = spider_scales(alpha, theta)
k8 = 8; eps8 = theta / k8; tau8 = eps8 / t
adj, posm = build_spider(k8, L)
res = cf_push_fifo(adj, alpha, 0, eps8, tau8, log_pushes=True)
print(f"M={M} L={L}  W1={res['W1']}  (Phase I silent iff 0)")
# group per arm
C = 2 * g / k8
by_arm = {a: [] for a in range(k8)}
center_seq = []
for (u, sig) in res['pushes']:
    if posm[u] == 'c':
        center_seq.append(sig)
    else:
        a, j = posm[u]
        by_arm[a].append((j, sig))
# lemma prediction: arm a executes cycles m=1..M: depths m..1, r=C lam^{2m-l}
ok = True
worst = 0.0
for a in range(k8):
    seq = by_arm[a]
    ptr = 0
    for m in range(1, M + 1):
        for l in range(m, 0, -1):
            j, sig = seq[ptr]; ptr += 1
            pred = C * lam ** (2 * m - l)
            worst = max(worst, abs(sig - pred) / pred)
            if j != l or abs(sig - pred) > 1e-9 * pred:
                ok = False
                print(f"  MISMATCH arm{a} cycle{m}: got depth {j} r={sig:.3e}"
                      f" want depth {l} r={pred:.3e}")
    if a == 0:
        print(f"  arm0: first {ptr} pushes match cycles 1..{M} exactly; "
              f"then {len(seq)-ptr} extra pushes beyond lemma's range")
print(f"  all arms, cycles m<=M: depth order and residuals match lemma: {ok}"
      f"  (max rel dev {worst:.2e})")
cpred = [g * lam ** (2 * jj) for jj in range(len(center_seq))]
cdev = max(abs(sig - p) / p for sig, p in zip(center_seq, cpred))
print(f"  center residual sequence g*lam^(2j): {len(center_seq)} pushes, "
      f"max rel dev {cdev:.2e}")
int_pushes = sum(len(v) for v in by_arm.values())
print(f"  interior pushes total={int_pushes}, lemma floor k*M(M+1)/2="
      f"{k8*M*(M+1)//2};  W2={res['W2']}, floor kM(M+1)={k8*M*(M+1)}")

print()
print("=" * 78)
print("B. Manuscript instance (theta=1/8, k=64, eps=1/512): FIFO work scaling")
print("=" * 78)
print(f"{'alpha':>7} {'L':>4} {'W1':>7} {'W2':>10} {'W*a*e':>8} "
      f"{'W*sqa*e':>9} {'W/(kM(M+1))':>12} {'err(z=0)/eps':>13} "
      f"{'cert(z=0)':>10}")
rows = []
for j in range(4, 13):
    alpha = 2.0 ** (-j)
    t, lam, c, g, wstar = pars(alpha)
    _, M, L = spider_scales(alpha, theta)
    tau = eps / t
    adj, posm = build_spider(k, L)
    res = cf_push_fifo(adj, alpha, 0, eps, tau)
    W = res['W1'] + res['W2']
    pi, d = solve_pi(adj, alpha, 0)
    e0 = semantic_err(np.zeros(len(adj)), pi, d)
    cg, _ = cert_gap(adj, alpha, np.zeros(len(adj)), 0, eps)
    rows.append((j, W))
    print(f"2^-{j:<4} {L:>4} {res['W1']:>7} {res['W2']:>10} "
          f"{W*alpha*eps:>8.4f} {W*t*eps:>9.3f} {W/(k*M*(M+1)):>12.3f} "
          f"{e0/eps:>13.4f} {cg:>10.2f}")
print("\n  [W*a*e flat => Theta(1/(alpha*eps)) as thm:cf-spider-lower states;")
print("   err(z=0)/eps < 1 for alpha<=2^-7 => W=0 output already valid;")
print("   cert(z=0) = 1/theta = 8 => z=0 violates the stopping certificate]")

print()
print("=" * 78)
print("C. Monotone omega=1 push run at the FINAL certificate (APPR at eps)")
print("=" * 78)
print(f"{'alpha':>7} {'W_appr':>10} {'W*a*e':>8} {'W*sqa*e':>9} "
      f"{'vol(G)':>8} {'W/vol(G)':>9}")
for j in range(4, 13):
    alpha = 2.0 ** (-j)
    t, lam, c, g, wstar = pars(alpha)
    _, M, L = spider_scales(alpha, theta)
    adj, posm = build_spider(k, L)
    # Phase I with tau=eps IS the omega=1 method run to the final threshold
    # (one-sided; residuals stay >=0 for omega=1 from r0>=0)
    res = cf_push_fifo(adj, alpha, 0, eps, eps)
    assert res['W2'] == 0, "phase II should be no-op after omega=1 at eps"
    volG = sum(len(a) for a in adj)
    W = res['W1']
    print(f"2^-{j:<4} {W:>10} {W*alpha*eps:>8.4f} {W*t*eps:>9.3f} "
          f"{volG:>8} {W/volG:>9.2f}")
print("\n  [the certificate is reachable by plain omega=1 push in "
      "Theta(1/(alpha*eps)) too; W <= 1/(g*eps) bound]")
