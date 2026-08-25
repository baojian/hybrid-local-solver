"""I5-E star interpolation: W(B) on centre-seeded K_{1,m}.

Member family (in R_B, B = j+1): alternate
  BLOCK op on U = {c} + j leaves  (omega_b)   with
  OUT-PASS: singleton relax of each of the m-j outside leaves (omega_l).
By leaf symmetry the dynamics are exactly 3-dim: (z_c, z_in, z_out).
Exact reduced maps (derived from H z = gamma e_c restricted):
  block:  T_c = (gamma + c(m-j) z_out) / (1 - c^2 j/m);  T_in = c T_c / m
          z_c <- (1-om) z_c + om T_c ;  z_in <- (1-om) z_in + om T_in
  pass:   z_out <- (1-om) z_out + om c z_c / m
pi_c = (1+alpha)/2, pi_leaf = c pi_c/m.  Stop: semantic err <= eps = 1/(8m).

Charging per block op: W_vol += m + j ; per out-pass: W_vol += m - j.
LB per centre op (cap lemma):  |dz_c| <= 2 sqrt(alpha * tau), tau = 1/(1-c^2 j/m)
  => N_c >= (pi_c - 1/8) / (2 sqrt(alpha tau))    [gamma*pi_c = alpha exactly]
  => W_vol >= (m + j) * N_c_LB   (every centre op costs >= vol(U) = m+j... >= m)
"""
import math, json, sys
import numpy as np

sys.path.insert(0, "/home/claude/work/overnight/i5e")
sys.path.insert(0, "/home/claude/work/overnight/lib")
import zoo
from core import Prob, BlockState, params


def reduced_run(m, j, alpha, om_b, om_l, max_ops=2_000_000):
    c, g = params(alpha)
    pi_c = (1 + alpha) / 2.0
    pi_l = c * pi_c / m
    eps = 1.0 / (8.0 * m)
    zc = zi = zo = 0.0
    tau = 1.0 / (1.0 - c * c * j / m)
    Nc = 0; W = 0.0
    def err():
        worst = abs(pi_c - zc) / m
        if j: worst = max(worst, abs(pi_l - zi))
        if m - j: worst = max(worst, abs(pi_l - zo))
        return worst
    for t in range(max_ops):
        if err() <= eps:
            return Nc, W, True
        # block op
        Tc = (g + c * (m - j) * zo) * tau
        Ti = c * Tc / m
        zc = (1 - om_b) * zc + om_b * Tc
        zi = (1 - om_b) * zi + om_b * Ti
        Nc += 1; W += m + j
        if err() <= eps:
            return Nc, W, True
        if m - j:
            zo = (1 - om_l) * zo + om_l * c * zc / m
            W += m - j
    return Nc, W, False


def best_over_omega(m, j, alpha):
    best = None
    oms = [1.0, 1.5, 1.8, 1.9, 1.95, 1.99, 1.999, 2 - 1e-6]
    for ob in oms:
        for ol in [1.0, 1.9, 2 - 1e-6]:
            Nc, W, done = reduced_run(m, j, alpha, ob, ol)
            if done and (best is None or W < best[1]):
                best = (Nc, W, ob, ol)
    return best


def crosscheck():
    """Reduced 3-dim dynamics == full simulator (m=12, j=5, omega mix)."""
    m, j, alpha = 12, 5, 2.0 ** -4
    adj, seed = zoo.star(m)
    P = Prob(adj, alpha, seed)
    S = BlockState(P, track_cap=True)
    U = [0] + list(range(1, 1 + j))
    outs = list(range(1 + j, m + 1))
    c, g = params(alpha)
    zc = zi = zo = 0.0
    tau = 1.0 / (1.0 - c * c * j / m)
    worst = 0.0
    for t in range(40):
        Tc = (g + c * (m - j) * zo) * tau; Ti = c * Tc / m
        zc = (1 - 1.9) * zc + 1.9 * Tc; zi = (1 - 1.9) * zi + 1.9 * Ti
        S.op(U, 1.9)
        worst = max(worst, abs(S.z[0] - zc), abs(S.z[1] - zi))
        for u in outs:
            S.op([u], 1.0)
        zo = c * zc / m
        worst = max(worst, abs(S.z[m] - zo))
    print(f"crosscheck reduced-vs-full (40 rounds, omega=1.9): max dev = {worst:.3e}; "
          f"cap util a/b = {S.max_util_a:.4f}/{S.max_util_b:.4f}")


def main():
    crosscheck()
    m = 64                      # eps = 1/(8m) = 2^-9
    eps = 1 / (8 * m)
    print(f"\n== star W(B) law, m={m}, eps=1/(8m); x(j) = 1 - c^2 j/m ==")
    print(f"{'alpha':>7} {'j':>4} {'beta':>6} {'sqrt(x/a)':>9} {'N_c':>6} "
          f"{'N_LB':>8} {'N/N_LB':>7} {'W_vol':>9} {'W_LB':>9} {'W/W_LB':>7} "
          f"{'W*sq(a)*e/sq(x)':>15} {'om_b':>7}")
    results = []
    for k in [6, 8, 10, 12, 14]:
        alpha = 2.0 ** -k
        c, g = params(alpha)
        pi_c = (1 + alpha) / 2
        for j in [0, 16, 32, 48, 56, 60, 62, 63, 64]:
            x = 1 - c * c * j / m
            tau = 1 / x
            NLB = (pi_c - 1/8) / (2 * math.sqrt(alpha * tau))
            WLB = (m + j) * NLB
            r = best_over_omega(m, j, alpha)
            if r is None:
                print(f"{alpha:7.1e} {j:4d}  FAILED"); continue
            Nc, W, ob, ol = r
            const = W * math.sqrt(alpha) * eps / math.sqrt(x)
            results.append(dict(alpha=alpha, j=j, Nc=Nc, W=W, NLB=NLB, WLB=WLB,
                                x=x, const=const, om_b=ob))
            print(f"{alpha:7.1e} {j:4d} {j/m:6.3f} {math.sqrt(x/alpha):9.2f} "
                  f"{Nc:6d} {NLB:8.2f} {Nc/NLB:7.2f} {W:9.0f} {WLB:9.1f} "
                  f"{W/WLB:7.2f} {const:15.4f} {ob:7.4f}")
    json.dump(results, open("/home/claude/work/overnight/i5e/out/star_law.json", "w"))
    # the B >= m+1 endpoint: one full block
    print("\nfull block j=m: one op, W_vol = 2m =", 2 * m, " (exact solve, err=0)")


if __name__ == "__main__":
    main()
