"""I2-E: information UPPER bound on spiders -- interval-certified estimator.

Model: adjacency-list scans; scanning a discovered vertex reveals its full
neighbor list (ids + degree). Seed = center. Computation is free; only scans
are counted. Promise class: spiders (center, k arms, arbitrary unknown
lengths L_a >= 1, adversarially chosen); INF = "longer than anything the
algorithm can reach" (the all-completions supremum).

--------------------------------------------------------------------------
ENVELOPE (exact, from the closed forms in formulas.py)
--------------------------------------------------------------------------
State per arm:
  open(m):  depths 1..m scanned (all degree 2); head id at depth m+1 known,
            unscanned.  Consistent completions: L_a in {m+1, m+2, ...}.
  done(L):  leaf found at depth L (scanned, degree 1).  psi exact.
Write, for arm a, m_a = (shortest consistent L_a) - 1  (= m if open at m,
= L-1 if done at L), and

    phi(m) = 2 lam^{2m+2} / (1 + lam^{2m+2})  in (0, c*lam],
    theta(m) = 2 lam^{m+1} / (1 + lam^{2m+2}),      phi = lam^{m+1} theta.

MASTER IDENTITY (sympy-verified):   u0 = (s/k) / (1 - (1/k) sum_a phi(m_a)).
  * psi(m) decreasing in m => u0 and every u_j simultaneously maximized by the
    closure G^max (every open arm ends at its head, L=m+1) and minimized by
    G^min (every open arm infinite).  Two closed-form evaluations therefore
    give EXACT per-coordinate intervals over all consistent completions.

CERTIFICATE (output = midpoint on scanned vertices, 0 elsewhere):
  C1 center            (u0max - u0min)/2 <= eps
  C2 open-arm head     u0max * theta(m) <= eps                (output 0 there)
  C3 unseen below head u0max * theta(m+1) <= eps              (implied by C2)
  C4 scanned coords, open arm:  u0max*g_j(m+1) - u0min*lam^j <= 2 eps
       W(j) satisfies W'' = (ln lam)^2 W, so W is convex wherever positive =>
       no interior positive maximum => checking j=1 and j=m suffices.
  C5 scanned coords, done arm:  (u0max-u0min)*g_1(L) <= 2 eps  (implied by C1
       since g_1 <= c < 1)
All of C2,C3,C4 are monotone DECREASING in m at fixed (u0max,u0min), so only
the SHALLOWEST open arm needs checking.  Under round-robin depth doubling the
open arms occupy at most two distinct depths, so the whole certificate is
O(1) arithmetic per probe (state: two phi-sums, two (depth,count) slots).

--------------------------------------------------------------------------
COMPLEXITY (derived in findings/i2e_info_upper.md)
--------------------------------------------------------------------------
For k arms all open at depth m the certificate collapses to the SCALAR
condition       y/(1-y^2) <= beta,      y = lam^{m+1},  beta = k eps/(2 s),
whose extremal cost is  T*eps = t/(2 sinh t)  at t = 2 s m, sup = 1/2 (t->0).
=> T <= (1/2 + o(1))/eps with exact stopping, <= (1+o(1))/eps with doubling.
No 1/sqrt(alpha) factor and no log factor.
"""
import sys, math, random
from fractions import Fraction
sys.path.insert(0, "/home/claude/work/overnight/w2_spider_info")
sys.path.insert(0, "/home/claude/work/overnight/lib")
from formulas import lam_of_alpha, params, psi

INF = None


def g(lam, j, L):
    """u_j/u_0 for an arm of length L (L=INF => lam^j)."""
    if L is INF:
        return lam ** j
    return (lam ** j + lam ** (2 * L - j)) / (1 + lam ** (2 * L))


class SpiderOracle:
    """Counts scans.  scan_arm(a,depth) is legal only if depth-1 was scanned."""

    def __init__(self, Ls):
        self.Ls = Ls
        self.scans = 0

    def scan_center(self):
        self.scans += 1
        return len(self.Ls)

    def scan_arm(self, a, depth):
        self.scans += 1
        L = self.Ls[a]
        return 'leaf' if (L is not INF and depth == L) else 'cont'


class Estimator:
    """Depth-doubling round robin with an O(1)-per-probe interval certificate."""

    def __init__(self, lam, eps, tol=0.0):
        self.lam = lam
        self.c, self.gamma = params(lam)
        self.eps = eps * (1 - tol)

    # ---- certificate primitives -------------------------------------
    def theta(self, m):
        lam = self.lam
        return 2 * lam ** (m + 1) / (1 + lam ** (2 * m + 2))

    def run(self, oracle, trace=False):
        lam, c, eps = self.lam, self.c, self.eps
        k = oracle.scan_center()

        # ---- incremental state (all O(1) to update) ----
        arms = [[0, False] for _ in range(k)]      # [depth m_a, done?]
        sum_max = k * psi(lam, 0)                  # sum psi(m_a) : closure L=m+1
        sum_min = k * lam                          # open arms -> psi(inf)=lam
        # open arms live at <=2 distinct depths under doubling; track counts
        open_cnt = {0: k}
        done_g1_max = 0.0
        self.binding = None

        def cert():
            u0max = self.gamma / (k - c * sum_max)
            u0min = self.gamma / (k - c * sum_min)
            w0 = u0max - u0min
            if w0 > 2 * eps:
                self.binding = 'C1'
                return False
            if done_g1_max and w0 * done_g1_max > 2 * eps:
                self.binding = 'C5'
                return False
            live = [m for m, n in open_cnt.items() if n]
            if live:
                m = min(live)                       # monotone => shallowest binds
                if u0max * self.theta(m) > eps:
                    self.binding = 'C2'
                    return False
                if u0max * self.theta(m + 1) > eps:
                    self.binding = 'C3'
                    return False
                for j in ((1, m) if m >= 1 else ()):
                    if u0max * g(lam, j, m + 1) - u0min * lam ** j > 2 * eps:
                        self.binding = 'C4'
                        return False
            self.binding = 'certified'
            return True

        if cert():
            return self.finish(k, arms, oracle)
        r = 0
        while True:
            target = 1 << r
            for a in range(k):
                m, done = arms[a]
                if done or m >= target:
                    continue
                v = m
                leaf = False
                while m < target:
                    if oracle.scan_arm(a, m + 1) == 'leaf':
                        m += 1
                        leaf = True
                        break
                    m += 1
                open_cnt[v] -= 1
                if leaf:
                    arms[a] = [m, True]
                    p = psi(lam, m - 1)
                    sum_max += p - psi(lam, v)
                    sum_min += p - lam
                    g1 = g(lam, 1, m)
                    if g1 > done_g1_max:
                        done_g1_max = g1
                else:
                    arms[a] = [m, False]
                    sum_max += psi(lam, m) - psi(lam, v)
                    open_cnt[m] = open_cnt.get(m, 0) + 1
                if cert():
                    return self.finish(k, arms, oracle)
            open_cnt = {m: n for m, n in open_cnt.items() if n}
            if not open_cnt:                        # every arm resolved
                assert cert()
                return self.finish(k, arms, oracle)
            r += 1

    def finish(self, k, arms, oracle):
        lam = self.lam
        sum_max = sum(psi(lam, m if not d else m - 1) for m, d in arms)
        sum_min = sum((lam if not d else psi(lam, m - 1)) for m, d in arms)
        u0max = self.gamma / (k - self.c * sum_max)
        u0min = self.gamma / (k - self.c * sum_min)
        out = {'k': k, 'u0_mid': (u0max + u0min) / 2, 'arms': [],
               'scans': oracle.scans, 'binding': self.binding}
        for m, d in arms:
            if not d:
                prof = [(u0max * g(lam, j, m + 1) + u0min * lam ** j) / 2
                        for j in range(1, m + 1)]
            else:
                prof = [((u0max + u0min) / 2) * g(lam, j, m)
                        for j in range(1, m + 1)]
            out['arms'].append((d, m, prof))
        return out


def validate(lam, Ls, out, eps):
    """max_i |uhat_i - u_i| / eps over every vertex of the TRUE graph
    (uhat = 0 at unscanned vertices).  <=1 means certified eps-valid."""
    c, gamma = params(lam)
    k = len(Ls)
    su0 = gamma / (k - c * sum(lam if L is INF else psi(lam, L - 1) for L in Ls))
    worst = abs(out['u0_mid'] - su0) / eps
    for a, L in enumerate(Ls):
        d, m, prof = out['arms'][a]
        top = (m + 3) if L is INF else L
        for j in range(1, top + 1):
            ut = su0 * g(lam, j, L)
            hat = prof[j - 1] if j <= len(prof) else 0
            worst = max(worst, abs(hat - ut) / eps)
        if L is INF:
            worst = max(worst, su0 * lam ** (m + 4) / eps)   # unseen tail sup
    return worst


def run_case(alpha, eps, Ls, exact=False):
    lam, s = lam_of_alpha(alpha)
    if exact:
        est = Estimator(lam, Fraction(eps), 0)
        orc = SpiderOracle(Ls)
        out = est.run(orc)
        return out['scans'], validate(lam, Ls, out, Fraction(eps)), out['binding']
    est = Estimator(float(lam), float(eps), 1e-9)
    orc = SpiderOracle(Ls)
    out = est.run(orc)
    return out['scans'], validate(float(lam), Ls, out, float(eps)), out['binding']


# --------------------------- theory predictions ---------------------------

def m_needed(lam, s, k, eps):
    """Smallest integer depth m with the all-open certificate satisfied:
    y/(1-y^2) <= beta, y = lam^{m+1}, beta = k eps/(2s)."""
    beta = k * eps / (2 * s)
    ystar = (-1 + math.sqrt(1 + 4 * beta * beta)) / (2 * beta)
    if lam >= ystar:                       # m = 0 already fails
        need = math.log(ystar) / math.log(lam) - 1
        return max(0, math.ceil(need - 1e-12))
    return 0


def predicted_max_T(lam, s, eps):
    """max over k of k*m_needed (exact stopping) and of k*2^ceil(log2 m) (doubling)."""
    best_exact = (0, 0, 0)
    best_dbl = (0, 0, 0)
    for m in range(0, 400):
        # largest k for which depth m is still required (depth m-1 insufficient)
        if m == 0:
            continue
        y = lam ** m                        # need y/(1-y^2) > beta at depth m-1
        beta_max = y / (1 - y * y)
        k = math.floor(2 * s * beta_max / eps)
        if k < 1:
            continue
        if k * m > best_exact[0]:
            best_exact = (k * m, k, m)
        D = 1 << max(0, (m - 1).bit_length())
        if k * D > best_dbl[0]:
            best_dbl = (k * D, k, m)
    return best_exact, best_dbl


# ------------------------------ experiments ------------------------------

def worst_k_search(alpha, eps, verbose=False):
    """Dense search over k for the all-INF spider (the LP-extremal family)."""
    lam, s = lam_of_alpha(alpha)
    lamf, sf, epsf = float(lam), float(s), float(eps)
    cands = set()
    kmax = max(4, int(2.5 / epsf))
    kk = 1
    while kk <= kmax:                       # log grid
        cands.add(kk)
        kk = max(kk + 1, int(kk * 1.25))
    for m in range(0, 200):                 # regime boundaries k_max(m)
        y = lamf ** max(m, 1)
        kb = 2 * sf * (y / (1 - y * y)) / epsf
        if kb < 1:
            break
        for d in (-2, -1, 0, 1, 2):
            if 1 <= int(kb) + d <= kmax:
                cands.add(int(kb) + d)
    best = (0, None, None, None)
    for k in sorted(cands):
        scans, slack, bind = run_case(alpha, eps, [INF] * k)
        assert slack <= 1.0 + 1e-6, (alpha, eps, k, slack)
        if scans > best[0]:
            best = (scans, k, slack, bind)
    return best


def mixed_configs(alpha, eps, seed=0):
    lam, s = lam_of_alpha(alpha)
    sf, epsf = float(s), float(eps)
    kstar = max(2, int(2 * sf / (math.e * epsf)))
    khalf = max(2, int(1 / (2 * epsf)))
    rng = random.Random(seed)
    cfgs = {
        'all-INF k=k*=2s/(e eps)': [INF] * kstar,
        'all-INF k=1/(2eps)': [INF] * khalf,
        'all-INF k=1/(4eps)': [INF] * max(2, khalf // 2),
        'star (all L=1) k=1/(2eps)': [1] * khalf,
        'star (all L=1) k=4/eps': [1] * max(2, int(4 / epsf)),
        'half L=1 / half INF': [1] * (khalf // 2) + [INF] * (khalf // 2),
        '90% L=1 / 10% INF': [1] * int(0.9 * khalf)
                             + [INF] * (khalf - int(0.9 * khalf)),
        'geometric lengths': [1 << (i % 10) for i in range(kstar)],
        'all L=2': [2] * khalf,
        'all L=1/(2s) (medium)': [max(1, int(1 / (2 * sf)))] * kstar,
        'one INF + (k-1) L=1, k=1/(2s)': [INF] + [1] * max(1, int(1 / (2 * sf))),
    }
    rows = []
    for name, Ls in cfgs.items():
        scans, slack, bind = run_case(alpha, eps, Ls)
        assert slack <= 1.0 + 1e-6, (name, slack)
        rows.append((name, len(Ls), scans, scans * float(eps), bind))
    worst = (0, None, None)
    for _ in range(40):
        k = max(2, int(khalf * rng.choice([0.25, 0.5, 1.0, 1.5])))
        Ls = [rng.choice([1, 1, 2, 3, 8, 32, INF, INF]) for _ in range(k)]
        scans, slack, bind = run_case(alpha, eps, Ls)
        assert slack <= 1.0 + 1e-6
        if scans > worst[0]:
            worst = (scans, k, bind)
    rows.append((f'worst of 40 random multisets', worst[1], worst[0],
                 worst[0] * float(eps), worst[2]))
    return rows


def minimax(alpha, eps, iters=300, seed=0):
    """Two-block exhaustive + hill-climbing local search for the worst input."""
    lam, s = lam_of_alpha(alpha)
    sf, epsf = float(s), float(eps)
    lens = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, INF]
    kbase = max(2, int(1 / (2 * epsf)))
    best = (0, None)
    for k in sorted({2, 4, 8, kbase // 8, kbase // 4, kbase // 2,
                     int(kbase * 0.75), kbase, int(kbase * 1.5), 2 * kbase}):
        if k < 1:
            continue
        for l1 in lens:
            for frac in (0.0, 0.25, 0.5, 0.75, 1.0):
                n1 = int(k * frac)
                for l2 in lens:
                    Ls = [l1] * n1 + [l2] * (k - n1)
                    if not Ls:
                        continue
                    sc, sl, bd = run_case(alpha, eps, Ls)
                    assert sl <= 1.0 + 1e-6
                    if sc > best[0]:
                        best = (sc, (k, l1, n1, l2, k - n1, bd))
    # hill-climb on the champion multiset
    k, l1, n1, l2, n2, _ = best[1]
    cur = [l1] * n1 + [l2] * n2
    cur_s = best[0]
    rng = random.Random(seed)
    for _ in range(iters):
        cand = list(cur)
        op = rng.random()
        if op < 0.4 and cand:
            i = rng.randrange(len(cand))
            cand[i] = rng.choice(lens)
        elif op < 0.7:
            cand.append(rng.choice(lens))
        elif cand:
            cand.pop(rng.randrange(len(cand)))
        if not cand:
            continue
        sc, sl, bd = run_case(alpha, eps, cand)
        assert sl <= 1.0 + 1e-6
        if sc > cur_s:
            cur, cur_s = cand, sc
    return best, (cur_s, len(cur), sorted(set(str(x) for x in cur)))


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    ALPHAS = [Fraction(1, 1 << a) for a in (4, 6, 8, 10, 12)]
    EPSS = [Fraction(1, 1 << e) for e in (4, 6, 8, 10)]

    if which in ('all', 'grid'):
        print("=== I2-E: interval-certified spider estimator ===")
        print("\n-- 1. worst-case-over-k probe count, all-INF spiders --")
        print(f"{'alpha':>8} {'eps':>8} {'1/eps':>7} {'T':>8} {'T*eps':>7} "
              f"{'k_worst':>8} {'bind':>5}  {'pred_exact':>10} {'pred_dbl':>9}")
        data = []
        for alpha in ALPHAS:
            lam, s = lam_of_alpha(alpha)
            for eps in EPSS:
                if eps >= s:                # trivial cell: all-zero output valid
                    continue
                T, k, sl, bd = worst_k_search(alpha, eps)
                pe, pd = predicted_max_T(float(lam), float(s), float(eps))
                data.append((float(alpha), float(eps), T, k))
                print(f"2^-{alpha.denominator.bit_length()-1:<5d} "
                      f"2^-{eps.denominator.bit_length()-1:<5d} "
                      f"{1/float(eps):7.0f} {T:8d} {T*float(eps):7.4f} "
                      f"{k:8d} {bd:>5}  {pe[0]*float(eps):10.4f} "
                      f"{pd[0]*float(eps):9.4f}")
        cs = [T * e for _, e, T, _ in data]
        print(f"\n  T*eps over grid: min={min(cs):.4f} max={max(cs):.4f}"
              f"   (theory: exact-stop sup 1/2, doubling sup ~1)")
        # log-log fit of T vs 1/eps at fixed alpha
        print("\n  slope of log T vs log(1/eps) (fixed alpha):")
        for alpha in ALPHAS:
            pts = [(math.log(1 / e), math.log(T))
                   for a, e, T, _ in data if a == float(alpha)]
            if len(pts) < 2:
                continue
            n = len(pts)
            mx = sum(p[0] for p in pts) / n
            my = sum(p[1] for p in pts) / n
            sl = (sum((p[0] - mx) * (p[1] - my) for p in pts)
                  / sum((p[0] - mx) ** 2 for p in pts))
            print(f"    alpha=2^-{alpha.denominator.bit_length()-1:<3d} "
                  f"slope={sl:.4f}  (n={n})")

    if which in ('all', 'mixed'):
        for alpha, eps in ((Fraction(1, 256), Fraction(1, 1024)),
                           (Fraction(1, 4096), Fraction(1, 1024))):
            print(f"\n-- 2. mixed/adversarial configs "
                  f"(alpha={alpha}, eps={eps}) --")
            for name, k, sc, se, bd in mixed_configs(alpha, eps):
                print(f"   {name:32s} k={k!s:>7s} T={sc:7d} T*eps={se:7.4f} "
                      f"bind={bd}")

    if which in ('all', 'minimax'):
        for alpha, eps in ((Fraction(1, 16), Fraction(1, 256)),
                           (Fraction(1, 256), Fraction(1, 256))):
            print(f"\n-- 3. minimax over configurations "
                  f"(alpha={alpha}, eps={eps}) --")
            best, hc = minimax(alpha, eps)
            k, l1, n1, l2, n2, bd = best[1]
            print(f"   two-block worst: T={best[0]}  T*eps={best[0]*float(eps):.4f}"
                  f"  k={k} ({n1}x L={l1}, {n2}x L={l2}) bind={bd}")
            print(f"   hill-climb worst: T={hc[0]}  T*eps={hc[0]*float(eps):.4f}"
                  f"  k={hc[1]}  lengths={hc[2]}")

    if which in ('all', 'exact'):
        print("\n-- 4. exact-Fraction re-validation of champions --")
        for alpha, eps, Ls, tag in (
                (Fraction(1, 16), Fraction(1, 128), [INF] * 64, 'all-INF'),
                (Fraction(1, 256), Fraction(1, 256), [INF] * 128, 'all-INF'),
                (Fraction(1, 256), Fraction(1, 256), [1] * 60 + [INF] * 60,
                 'half/half'),
                (Fraction(1, 64), Fraction(1, 512), [1] * 200, 'star')):
            sc, sl, bd = run_case(alpha, eps, Ls, exact=True)
            print(f"   alpha={str(alpha):>9} eps={str(eps):>8} {tag:>10} "
                  f"k={len(Ls):4d}: T={sc:6d} maxerr/eps={float(sl):.6f} "
                  f"{'VALID' if sl <= 1 else 'INVALID'}  bind={bd}")
