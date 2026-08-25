"""I5-E exact checks (Fractions, no floats).

E1. Star tau formula:  U = {c} + j leaves  =>  tau_c(U) = 1/(1 - c_a^2 j/m).
E2. Global identity    tau_v(V) = pi_v / gamma_a   (any graph; star + spider).
E3. Block energy identity: for the omega-block step on any U and any state,
      Phi(e) - Phi(e+) = [omega(2-omega)/2] * r_U^T (H_UU D_U)^{-1} r_U,
    with Phi(e) = 1/2 e^T D^{-1} H e   (exact rationals).
E4. Cap lemma exact, one adversarial run on the star (m=6, alpha=1/4):
      |dz_c| <= omega * sqrt(gamma*pi_c*tau)  -- compare squares rationally.
"""
from fractions import Fraction as Fr
import itertools, sys

sys.path.insert(0, "/home/claude/work/overnight/lib")
import zoo


def build_H(adj, alpha):
    n = len(adj)
    c = (1 - alpha) / (1 + alpha)
    d = [Fr(len(adj[u])) for u in range(n)]
    H = [[Fr(0)] * n for _ in range(n)]
    for i in range(n):
        H[i][i] = Fr(1)
        for j in adj[i]:
            H[i][j] -= c / d[j]
    return H, d, c


def solve(M, rhs):
    n = len(M)
    M = [row[:] for row in M]; r = rhs[:]
    for col in range(n):
        piv = next(i for i in range(col, n) if M[i][col] != 0)
        M[col], M[piv] = M[piv], M[col]; r[col], r[piv] = r[piv], r[col]
        inv = 1 / M[col][col]
        M[col] = [v * inv for v in M[col]]; r[col] *= inv
        for i in range(n):
            if i != col and M[i][col] != 0:
                f = M[i][col]
                M[i] = [vi - f * vc for vi, vc in zip(M[i], M[col])]
                r[i] -= f * r[col]
    return r


def restrict(M, U):
    return [[M[i][j] for j in U] for i in U]


def tau_exact(H, U, v):
    i = U.index(v)
    e = [Fr(0)] * len(U); e[i] = Fr(1)
    return solve(restrict(H, U), e)[i]


def phi(H, d, e):
    n = len(H)
    He = [sum(H[i][j] * e[j] for j in range(n)) for i in range(n)]
    return sum(e[i] * He[i] / d[i] for i in range(n)) / 2


ok = fail = 0
def chk(name, cond):
    global ok, fail
    if cond: ok += 1
    else:
        fail += 1
        print("  FAIL:", name)

# ---- E1: star tau formula ----
for m, alpha in [(6, Fr(1, 4)), (6, Fr(1, 16)), (9, Fr(1, 8))]:
    adj, seed = zoo.star(m)
    H, d, c = build_H(adj, alpha)
    for j in range(m + 1):
        U = [0] + list(range(1, 1 + j))
        t = tau_exact(H, U, 0)
        chk(f"E1 star m={m} a={alpha} j={j}", t == 1 / (1 - c * c * Fr(j, m)))
print(f"E1 star tau closed form: checked m in (6,9), all j, 3 alphas")

# ---- E2: tau_v(V) = pi_v/gamma ----
for name, (adj, seed) in [("star6", zoo.star(6)), ("spider", zoo.spider(3, 3)),
                          ("path7", zoo.path(7)), ("theta", zoo.theta_graph(2, 3, 4))]:
    for alpha in [Fr(1, 4), Fr(1, 16)]:
        H, d, c = build_H(adj, alpha)
        g = 2 * alpha / (1 + alpha)
        rhs = [Fr(0)] * len(adj); rhs[seed] = g
        pi = solve(H, rhs)
        t = tau_exact(H, list(range(len(adj))), seed)
        chk(f"E2 {name} a={alpha}", t == pi[seed] / g)
print("E2 tau_v(V) = pi_v/gamma: 4 graphs x 2 alphas")

# ---- E3: block energy identity ----
adj, seed = zoo.spider(3, 3)
alpha = Fr(1, 8)
H, d, c = build_H(adj, alpha)
g = 2 * alpha / (1 + alpha)
rhs = [Fr(0)] * len(adj); rhs[seed] = g
pi = solve(H, rhs)
# arbitrary rational state
z = [Fr(i % 3, 7) - Fr(i % 2, 5) for i in range(len(adj))]
r = [rhs[i] - sum(H[i][j] * z[j] for j in range(len(adj))) for i in range(len(adj))]
e = [pi[i] - z[i] for i in range(len(adj))]
for U, om in [([0, 1, 2], Fr(1)), ([0, 1, 4, 7], Fr(3, 2)), ([2, 3], Fr(1, 3)),
              ([0], Fr(19, 10))]:
    G = restrict(H, U)
    delta = solve(G, [r[u] for u in U])
    z2 = z[:]
    for i, u in enumerate(U):
        z2[u] = z[u] + om * delta[i]
    e2 = [pi[i] - z2[i] for i in range(len(adj))]
    # rhs of identity: r_U^T (H_UU D_U)^{-1} r_U
    HD = [[G[i][j] * d[U[j]] for j in range(len(U))] for i in range(len(U))]
    q = solve(HD, [r[u] for u in U])
    diss = om * (2 - om) / 2 * sum(r[U[i]] * q[i] for i in range(len(U)))
    chk(f"E3 U={U} om={om}", phi(H, d, e) - phi(H, d, e2) == diss)
print("E3 block energy identity Phi-Phi+ = [om(2-om)/2] r_U^T (H_UU D_U)^{-1} r_U: 4 blocks")

# ---- E4: cap lemma, exact adversarial run on star ----
m, alpha = 6, Fr(1, 4)
adj, seed = zoo.star(m)
H, d, c = build_H(adj, alpha)
g = 2 * alpha / (1 + alpha)
rhs = [Fr(0)] * len(adj); rhs[seed] = g
pi = solve(H, rhs)
gpv = g * pi[0]
z = [Fr(0)] * len(adj)
r = rhs[:]
schedule = [([0, 1, 2], Fr(19, 10)), ([3], Fr(1)), ([0, 1, 2, 3, 4], Fr(3, 2)),
            ([1, 2, 3, 4, 5, 6], Fr(1)), ([0], Fr(19, 10)), ([0, 1, 2, 3, 4, 5], Fr(1)),
            ([0, 1], Fr(19, 10)), ([2, 3, 4, 5, 6], Fr(1)), ([0, 1, 2, 3, 4, 5, 6], Fr(1))]
maxratio2 = Fr(0)
for U, om in schedule:
    G = restrict(H, U)
    delta = solve(G, [r[u] for u in U])
    if 0 in U:
        i = U.index(0)
        t = tau_exact(H, U, 0)
        dz2 = (om * delta[i]) ** 2
        cap2 = om * om * gpv * t          # cap_a squared
        chk(f"E4 op U={U}", dz2 <= cap2)
        if cap2 > 0:
            maxratio2 = max(maxratio2, dz2 / cap2)
    for i, u in enumerate(U):
        z[u] += om * delta[i]
    r = [rhs[i] - sum(H[i][j] * z[j] for j in range(len(adj))) for i in range(len(adj))]
print(f"E4 exact cap on 9-op adversarial star run: max (dz_c/cap_a)^2 = "
      f"{float(maxratio2):.6f} (must be <= 1)")

print(f"\nTOTAL: {ok} pass / {fail} fail")
