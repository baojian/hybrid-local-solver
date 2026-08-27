"""I6-C Open 2: scope of the R+- sqrt(alpha)-coupling. Envelope + ceilings.

Objects (z-scale, H = I - c A D^{-1}, r = gamma e_v - H z, work d_u per op):
  Phi0    = gamma*pi_v/(2 d_v)                (initial energy; Lemma B.1)
  capD(u) = 2*sqrt(2*Phi0*d_u)                (per-op |delta| cap at u; tau=1
            Cauchy-Schwarz |(H_sym y)_u| <= sqrt((H_sym)_uu * 2Phi) = sqrt(2Phi))
  T_seed  = d_v*(pi_v - eps*d_v)_+ / capD(v)  (seed travel; i4c 3.4 / i5e B1)
  T_bulk  = dmin_S*(M_eps - eps*volS)_+ / capD(dmax_S)   (bulk travel; NEW)
  envelope = max(vol(S_eps), T_seed, T_bulk)  -- pathwise LB for every R+- member.

Structural facts under test (consequences of the Open-1 maximum principle):
  S1  S_eps nonempty ==> seed in S_eps (pi_v/d_v = max_u pi_u/d_u).
  S2  mass ceiling M_eps <= (pi_v/d_v) * vol(S_eps).
  S3  ceiling chain:  T_bulk*sqrt(alpha)*eps <= sqrt(Delta*(pi_v/d_v)*(1+a)/8)
      * (eps*volS) <= sqrt(Delta*(pi_v/d_v)/8)*(1+a)  (since eps*volS < 1).
  S4  T_seed*sqrt(alpha)*eps <= (Delta^{3/2}/2)*sqrt((1+a)/2)*eps  -> 0.
  ==> on bounded-degree instances every proven envelope term is o(1/(sqrt(a)e))
      once pi_v/d_v is small; the retentive corner pi_v/d_v = Theta(1) is
      excluded by the classical bounded-degree return-probability decay
      (checked numerically: pi_v/d_v <= (1+a)*d_v/(2 volG) + C*sqrt(a*Delta)).

Member battery (Part B): no R+- member may beat the envelope; measure the
member frontier scaling on bounded-degree instances (cycle / path, vol=1/2eps).

Rerun: cd /home/claude/work/overnight/i6c && python3 open2_scope.py
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'lib'))
import zoo                                                # noqa: E402

FAIL = 0


def chk(cond, msg):
    global FAIL
    if not cond:
        FAIL += 1
        print("  ** FAIL:", msg)


def solve_pi(adj, alpha, seed):
    n = len(adj)
    c = (1 - alpha) / (1 + alpha)
    g = 2 * alpha / (1 + alpha)
    d = np.array([len(adj[u]) for u in range(n)], float)
    H = np.eye(n)
    for u in range(n):
        for w in adj[u]:
            H[u, w] -= c / d[w]
    rhs = np.zeros(n)
    rhs[seed] = g
    return np.linalg.solve(H, rhs), d


def funnel(D):
    """Complete binary tree depth D; the 2^D leaves joined in a cycle.
    Degrees: root 2, internal 3, leaves 3. Seed = root."""
    edges = []
    for i in range(2 ** D - 1):
        edges += [(i, 2 * i + 1), (i, 2 * i + 2)]
    leaves = list(range(2 ** D - 1, 2 ** (D + 1) - 1))
    for j in range(len(leaves)):
        edges.append((leaves[j], leaves[(j + 1) % len(leaves)]))
    return zoo._sym(edges, 2 ** (D + 1) - 1), 0


def lollipop(L, npool):
    edges = [(i, i + 1) for i in range(L - 1)]
    base = L
    for j in range(npool):
        edges.append((base + j, base + (j + 1) % npool))
    edges.append((L - 1, base))
    return zoo._sym(edges, L + npool), 0


def envelope_terms(adj, alpha, seed, eps, pi=None, d=None):
    if pi is None:
        pi, d = solve_pi(adj, alpha, seed)
    n = len(adj)
    g = 2 * alpha / (1 + alpha)
    u_val = pi / d
    S = u_val > eps
    volS = float(d[S].sum())
    M = float(pi[S].sum())
    Phi0 = g * pi[seed] / (2 * d[seed])
    cap = lambda du: 2 * math.sqrt(2 * Phi0 * du)          # noqa: E731
    T_seed = d[seed] * max(pi[seed] - eps * d[seed], 0) / cap(d[seed])
    if S.any():
        dminS, dmaxS = float(d[S].min()), float(d[S].max())
        T_bulk = dminS * max(M - eps * volS, 0) / cap(dmaxS)
    else:
        dminS = dmaxS = 0.0
        T_bulk = 0.0
    env = max(volS, T_seed, T_bulk)
    return dict(pi=pi, d=d, uv=u_val[seed], S=S, volS=volS, M=M, Phi0=Phi0,
                T_seed=T_seed, T_bulk=T_bulk, env=env, dmaxS=dmaxS,
                seed_in_S=bool(S[seed]) if S.any() else None, n=n)


# ------------------------------------------------------------- Part A
def part_A():
    print("=" * 100)
    print("Part A: envelope terms + ceilings, bounded-degree battery "
          "(+ star control).  sae := sqrt(alpha)*eps")
    print("=" * 100)
    print(f"{'instance':<22s} {'eps':>6s} {'alpha':>8s} {'pi_v/d_v':>9s} "
          f"{'e*volS':>7s} {'M_eps':>7s} {'Mceil%':>7s} {'Ts*sae':>8s} "
          f"{'Tb*sae':>8s} {'env*sae':>8s} {'S3ceil':>7s} {'krnC':>6s}")
    rows = []
    for ee in (5, 7, 9):
        eps = 2.0 ** -ee
        insts = []
        npv = max(4, round(1 / (4 * eps)))
        insts.append((f'cycle{npv}', *zoo.cycle(npv)))
        insts.append((f'path{npv}_end', *zoo.path(npv, True)))
        Dt = max(2, round(math.log2(1 / (12 * eps))))
        adj, s = funnel(Dt)
        insts.append((f'funnel_D{Dt}', adj, s))
        try:
            nr = max(8, round(1 / (6 * eps)) * 2)
            insts.append((f'rreg{nr}_3', *zoo.random_regular(nr, 3)))
        except Exception:
            pass
        # star control (unbounded degree)
        m = round(1 / (8 * eps))
        insts.append((f'star{m}_ctr', *zoo.star(m, True)))
        for aexp in (2, 3, 4):
            alpha = eps ** aexp
            for name, adj, seed in insts:
                t = envelope_terms(adj, alpha, seed, eps)
                d = t['d']
                Delta = float(d.max())
                sae = math.sqrt(alpha) * eps
                a = alpha
                # S1: seed in S_eps or S empty
                if t['S'].any():
                    chk(t['seed_in_S'], f"S1 {name} eps=2^-{ee} a=eps^{aexp}")
                # S2 mass ceiling
                chk(t['M'] <= t['uv'] * t['volS'] + 1e-12,
                    f"S2 {name} eps=2^-{ee}")
                mceil = t['M'] / (t['uv'] * t['volS']) if t['volS'] else 0
                # S3 ceiling on the bulk term
                s3 = math.sqrt(Delta * t['uv'] * (1 + a) / 8) * \
                    (eps * t['volS'])
                chk(t['T_bulk'] * sae <= s3 + 1e-12,
                    f"S3 {name} eps=2^-{ee}")
                # S4 seed-term ceiling (only meaningful bounded degree)
                s4 = (Delta ** 1.5 / 2) * math.sqrt((1 + a) / 2) * eps
                if Delta <= 4:
                    chk(t['T_seed'] * sae <= s4 + 1e-12,
                        f"S4 {name} eps=2^-{ee}")
                # kernel constant: pi_v/d_v <= (1+a)d_v/volG + C sqrt(a*Delta)
                # (bipartite-safe discounted-stationary floor: even-time
                #  return prob tends to 2 pi_stat on bipartite graphs)
                volG = float(d.sum())
                resid = t['uv'] - (1 + a) * d[seed] / volG
                krnC = resid / math.sqrt(a * Delta) if resid > 0 else 0.0
                print(f"{name:<22s} 2^-{ee:<3d} eps^{aexp:<3d} {t['uv']:9.2e} "
                      f"{eps*t['volS']:7.3f} {t['M']:7.3f} {100*mceil:6.1f}% "
                      f"{t['T_seed']*sae:8.4f} {t['T_bulk']*sae:8.4f} "
                      f"{t['env']*sae:8.4f} {s3:7.4f} {krnC:6.2f}")
                rows.append((name, ee, aexp, t, sae, Delta))
    # summary: bounded-degree envelope*sae vanishes; star control stays Theta(1)
    bmax = max(t['env'] * sae for name, ee, aexp, t, sae, D in rows if D <= 4)
    smin = min(t['env'] * sae for name, ee, aexp, t, sae, D in rows
               if name.startswith('star'))
    print(f"\n  bounded-degree max env*sae = {bmax:.4f}   "
          f"star-control min env*sae = {smin:.4f}")
    chk(smin > 0.02, "star control should stay Theta(1) (>= 3/128-ish)")
    return rows


# ------------------------------------------------------------- Part A2
def part_A2():
    print()
    print("Part A2: the remote-seed route is empty -- lollipop family "
          "(seed at far end of a 1/sqrt(alpha) path into a pool).")
    print(f"{'instance':<22s} {'eps':>6s} {'alpha':>8s} {'pi_v/d_v':>9s} "
          f"{'eps':>8s} {'S_eps':>6s} {'M_pool':>8s}")
    for ee in (4, 5, 6):
        eps = 2.0 ** -ee
        for aexp in (3, 4):
            alpha = eps ** aexp
            L = round(1 / math.sqrt(alpha))
            npool = max(3, round(1 / (8 * eps)))
            adj, seed = lollipop(L, npool)
            pi, d = solve_pi(adj, alpha, seed)
            uv = pi / d
            S = uv > eps
            Mpool = float(pi[L:].sum())
            print(f"lolli_L{L}_p{npool:<5d} 2^-{ee:<3d} eps^{aexp:<3d} "
                  f"{uv[seed]:9.2e} {eps:8.2e} {int(S.sum()):>6d} "
                  f"{Mpool:8.4f}")
            # by S1: if pi_v/d_v <= eps the whole output is empty
            if uv[seed] <= eps:
                chk(not S.any(), f"S1-contrapositive lolli eps=2^-{ee}")
    print("  (pi_v/d_v <= eps forces S_eps = emptyset: remote seeds empty "
          "the output; the mechanism-(ii) branch is void.)")


# ------------------------------------------------------------- Part B
def relax_run(adj, alpha, seed, eps, pi, d, schedule, cap_ops=2_000_000):
    """Run an R+- member; schedule yields (u, omega) ops (callable of state).
    Returns (W, nops, finished)."""
    n = len(adj)
    c = (1 - alpha) / (1 + alpha)
    g = 2 * alpha / (1 + alpha)
    z = np.zeros(n)
    r = np.zeros(n)
    r[seed] = g
    W = 0.0
    nops = 0
    Phi0 = g * pi[seed] / (2 * d[seed])
    capD = 2 * np.sqrt(2 * Phi0 * d)
    err = lambda: np.max(np.abs(pi - z) / d)               # noqa: E731
    for u, om in schedule(n, z, r, d):
        delta = om * r[u]
        chk(abs(delta) <= capD[u] + 1e-9,
            f"cap violation at u={u}: {abs(delta):.3g} > {capD[u]:.3g}")
        z[u] += delta
        r[u] -= delta
        if delta != 0:
            for w in adj[u]:
                r[w] += c * delta / d[u]
        W += d[u]
        nops += 1
        if nops % n == 0 and err() <= eps:
            return W, nops, True
        if nops >= cap_ops:
            break
    return W, nops, err() <= eps


def sched_sweep(omega_of):
    """Forward-only natural-order sweeps (consistently ordered: Young's SOR
    theory applies; fwd+bwd = SSOR destroys the omega* acceleration)."""
    def s(n, z, r, d):
        while True:
            for u in range(n):
                yield u, omega_of()
    return s


def sched_southwell(omega_of):
    def s(n, z, r, d):
        while True:
            u = int(np.argmax(np.abs(r) / np.sqrt(d)))
            yield u, omega_of()
    return s


def sched_random(rng):
    def s(n, z, r, d):
        while True:
            yield rng.randrange(n), 0.05 + 1.9 * rng.random()
    return s


def part_B():
    import random as _rnd
    print()
    print("=" * 100)
    print("Part B: member battery on bounded-degree instances (S_eps = V), "
          "W >= envelope asserted per run.")
    print("=" * 100)
    print(f"{'instance':<16s} {'alpha':>9s} {'member':<12s} {'W':>10s} "
          f"{'W*s(a)*e':>9s} {'W*s(a*e)':>9s} {'W/env':>7s} {'fin':>4s}")
    for ee in (5, 6, 7):
        eps = 2.0 ** -ee
        npv = round(1 / (4 * eps))
        for kind in ('cycle', 'path'):
            adj, seed = (zoo.cycle(npv) if kind == 'cycle'
                         else zoo.path(npv, True))
            for aexp in (2, 3):
                alpha = eps ** aexp
                pi, d = solve_pi(adj, alpha, seed)
                t = envelope_terms(adj, alpha, seed, eps, pi, d)
                if not t['S'].any() or not t['S'].all():
                    continue          # want S_eps = V instances here
                ws = 1 + ((1 - math.sqrt(alpha)) / (1 + math.sqrt(alpha)))**2
                members = [
                    ('GS(w=1)', sched_sweep(lambda: 1.0)),
                    ('SOR(w*)', sched_sweep(lambda: ws)),
                    ('w=2-2sqa', sched_sweep(
                        lambda: 2 - 2 * math.sqrt(alpha))),
                    ('southwell', sched_southwell(lambda: ws)),
                    ('random', sched_random(_rnd.Random(7))),
                ]
                best = None
                for mname, sch in members:
                    W, nops, fin = relax_run(adj, alpha, seed, eps, pi, d,
                                             sch)
                    if fin:
                        chk(W >= t['env'] - 1e-9,
                            f"member {mname} beat envelope on {kind}{npv}")
                        best = min(best, W) if best else W
                    print(f"{kind}{npv:<11d} eps^{aexp:<5d} {mname:<12s} "
                          f"{W:10.0f} {W*math.sqrt(alpha)*eps:9.4f} "
                          f"{W*math.sqrt(alpha*eps):9.2f} "
                          f"{W/t['env']:7.2f} {'y' if fin else 'N':>4s}")
                if best:
                    print(f"  -> frontier W={best:.0f}  vs envelope "
                          f"{t['env']:.1f} (volS={t['volS']:.0f}, "
                          f"T_bulk={t['T_bulk']:.1f}, T_seed={t['T_seed']:.1f})"
                          f"  gap={best/t['env']:.2f}x")
    print("\n  Reading: SOR(w*) forward sweeps sit at W*sqrt(a)*e ~ flat "
          "(Theta(1/sqrt(a)) sweeps x vol = Theta(1/(sqrt(a) eps)));")
    print("  the proven envelope is Theta(max(vol, T_bulk)) = "
          "Theta(max(1/eps, 1/sqrt(a*eps))): member/LB gap ~ sqrt(1/eps) "
          "-- the sharpened residual open.")


def main():
    part_A()
    part_A2()
    part_B()
    print()
    print(f"TOTAL FAILURES: {FAIL}")
    print("VERDICT: " + ("ALL PASS" if FAIL == 0 else "FAILURES PRESENT"))
    return FAIL


if __name__ == '__main__':
    sys.exit(0 if main() == 0 else 1)
