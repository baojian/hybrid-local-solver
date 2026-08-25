"""I5-E battery.

A. tau-geometry profiles (Q2):
   path:   tau_0(prefix_b) vs b  -> linear growth, saturation at pi_0/gamma,
           half-saturation scale b*(alpha).
   spider: tau_hub(hub + t arm-prefixes of depth p) vs (t, p)
           -> test  tau = 1/(1 - (t/k) sigma(p)),  sigma(p) -> 1-Theta(sqrt(a)).
   double star: tau_c1 before/after the block crosses the bridge.
B. cap battery: policies on star/path/spider/double-star, assert util <= 1.
C. min-work curves vs B (path, spider), W_vol; star covered by star_law.py
   (greedy cross-check here).
"""
import math, json, sys
import numpy as np

sys.path.insert(0, "/home/claude/work/overnight/i5e")
sys.path.insert(0, "/home/claude/work/overnight/lib")
import zoo
from core import Prob, BlockState, params, omega_star

OUT = {}

def double_star(m1, m2):
    edges = [(0, i) for i in range(2, 2 + m1)] + [(1, i) for i in range(2 + m1, 2 + m1 + m2)]
    edges.append((0, 1))
    n = 2 + m1 + m2
    adj = {u: set() for u in range(n)}
    for u, v in edges:
        adj[u].add(v); adj[v].add(u)
    return {u: sorted(adj[u]) for u in adj}, 0


# ---------- A. tau profiles ----------
def tau_profiles():
    print("== A1. path: tau_0(prefix b), saturation scale ==")
    print(f"{'alpha':>8} {'pi0/gamma':>10} {'tau(2)':>8} {'tau(8)':>8} {'tau(32)':>8} "
          f"{'tau(128)':>9} {'tau(512)':>9} {'b_half':>7} {'b*sqrt(a)':>9}")
    rows = []
    for k in [6, 8, 10, 12, 14]:
        a = 2.0 ** -k
        P = Prob(*[*zoo.path(1600)], alpha=a) if False else Prob(zoo.path(1600)[0], a, 0)
        full = P.g_a and P.pi[0] / P.g_a
        taus = {b: P.tau(0, list(range(b))) for b in [2, 8, 32, 128, 512]}
        bh = next((b for b in range(1, 1600) if P.tau(0, list(range(b))) >= full / 2), None)
        rows.append(dict(alpha=a, full=full, taus=taus, b_half=bh))
        print(f"{a:8.1e} {full:10.2f} {taus[2]:8.3f} {taus[8]:8.3f} {taus[32]:8.3f} "
              f"{taus[128]:9.3f} {taus[512]:9.3f} {bh:7d} {bh*math.sqrt(a):9.3f}")
    OUT["path_tau"] = rows

    print("\n== A2. spider k=8: tau_hub(t arms x depth p); model 1/(1-(t/k)sig(p)) ==")
    k_arms, L = 8, 160
    adj, seed = zoo.spider(k_arms, L)
    print(f"{'alpha':>8} {'p':>4} {'sig(p)':>8} " + " ".join(f"t={t:>2}" for t in [1, 2, 4, 6, 8])
          + "   [entries: tau measured / model]")
    rows = []
    for a in [2.0 ** -6, 2.0 ** -10, 2.0 ** -14]:
        P = Prob(adj, a, seed)
        for p in [1, 4, 16, 64, 160]:
            # sigma(p) from t=1 exactly: tau(1 arm) = 1/(1 - (1/k) sig)
            def U_of(t):
                U = [0]
                for arm in range(t):
                    U += [1 + arm * L + j for j in range(p)]
                return U
            t1 = P.tau(0, U_of(1))
            sig = (1 - 1 / t1) * k_arms
            entry = []
            worst = 0.0
            for t in [1, 2, 4, 6, 8]:
                tm = P.tau(0, U_of(t))
                model = 1 / (1 - (t / k_arms) * sig)
                worst = max(worst, abs(tm / model - 1))
                entry.append(f"{tm:7.2f}/{model:7.2f}")
            rows.append(dict(alpha=a, p=p, sig=sig, maxreldev=worst))
            print(f"{a:8.1e} {p:4d} {sig:8.5f} " + " ".join(entry) + f"   maxdev {worst:.1e}")
        full = P.pi[0] / P.g_a
        print(f"    pi_hub/gamma = {full:.3f}; tau(all arms, p=L) = {P.tau(0, U_of(8)):.3f}")
    OUT["spider_tau"] = rows

    print("\n== A3. double star m1=m2=40: the bridge jump ==")
    adj, seed = double_star(40, 40)
    for a in [2.0 ** -6, 2.0 ** -12]:
        P = Prob(adj, a, seed)
        U_own = [0] + list(range(2, 42))              # c1 + own leaves
        U_bridge = U_own + [1]                        # + c2 (no far leaves)
        U_all = list(range(len(adj)))
        print(f"  alpha={a:.1e}: tau(c1+own)={P.tau(0,U_own):8.3f}  "
              f"tau(+c2)={P.tau(0,U_bridge):8.3f}  tau(V)={P.tau(0,U_all):8.3f} "
              f"= pi/g={P.pi[0]/P.g_a:8.3f}")


# ---------- B/C. policies ----------
def run_policy(P, policy, eps, max_ops=60000, check_every=1):
    S = BlockState(P, track_cap=True)
    t = 0
    for U, om in policy(P, S):
        S.op(U, om)
        t += 1
        if t % check_every == 0 and S.err() <= eps:
            return S, True
        if t >= max_ops:
            break
    return S, S.err() <= eps


def pol_coord_sweep(prefix, omega):
    def gen(P, S):
        while True:
            for u in prefix:
                yield [u], omega
    return gen


def pol_window(prefix, b, omega):
    wins = [prefix[i:i + b] for i in range(0, len(prefix), b)]
    def gen(P, S):
        while True:
            for w in wins:
                yield w, omega
    return gen


def pol_greedy(B, omega):
    def gen(P, S):
        while True:
            score = np.abs(S.r) / np.sqrt(P.d)
            U = np.argsort(-score)[:B]
            yield np.sort(U), omega
    return gen


def path_curves():
    print("\n== C1. path min-work vs B  (n=1600, seed end, eps=2^-9) ==")
    eps = 2.0 ** -9
    adj, seed = zoo.path(1600)
    rows = []
    print(f"{'alpha':>8} {'volS':>6} {'B':>5} {'best policy':>14} {'ops':>7} "
          f"{'W_vol':>9} {'W/volS':>8} {'W_S1/volS':>9} {'utilA':>7}")
    for a in [2.0 ** -6, 2.0 ** -10, 2.0 ** -14]:
        P = Prob(adj, a, seed)
        Se = P.S_eps(eps)
        volS = float(P.d[Se].sum())
        ell = int(Se.max()) + 1 if len(Se) else 1
        pre = list(range(min(1600, ell + 30)))
        for B in [1, 4, 16, 64, 256]:
            cands = []
            if B == 1:
                for om in [1.0, omega_star(a), 1.9]:
                    cands.append((f"coord om={om:.2f}", pol_coord_sweep(pre, om)))
            else:
                for om in [1.0, 1.9]:
                    cands.append((f"win{B} om={om:.1f}", pol_window(pre, B, om)))
                cands.append((f"greedy{B}", pol_greedy(B, 1.0)))
            best = None
            for name, pol in cands:
                S, done = run_policy(P, pol, eps, max_ops=120000,
                                     check_every=max(1, len(pre) // (2 * B)))
                if done and (best is None or S.W_vol < best[1].W_vol):
                    best = (name, S)
            if best is None:
                print(f"{a:8.1e} {volS:6.0f} {B:5d}  none converged")
                continue
            name, S = best
            rows.append(dict(alpha=a, B=B, W=S.W_vol, W1=S.W_S1, volS=volS,
                             ops=S.nops, util=S.max_util_a, pol=name))
            print(f"{a:8.1e} {volS:6.0f} {B:5d} {name:>14} {S.nops:7d} "
                  f"{S.W_vol:9.0f} {S.W_vol/volS:8.2f} {S.W_S1/volS:9.2f} "
                  f"{S.max_util_a:7.3f}")
    OUT["path_curves"] = rows


def spider_curves():
    print("\n== C2. spider k=8 L=160 hub seed, min-work vs B (eps=2^-11; "
          "at eps=2^-9 S_eps is EMPTY for alpha<=2^-14, cf. I4-C sec 6.1) ==")
    eps = 2.0 ** -11
    k_arms, L = 8, 160
    adj, seed = zoo.spider(k_arms, L)
    rows = []
    print(f"{'alpha':>8} {'volS':>6} {'B':>5} {'best policy':>16} {'ops':>7} "
          f"{'W_vol':>9} {'W/volS':>8} {'utilA':>7}")
    for a in [2.0 ** -6, 2.0 ** -10, 2.0 ** -14]:
        P = Prob(adj, a, seed)
        Se = P.S_eps(eps)
        volS = float(P.d[Se].sum())
        if volS == 0:
            print(f"{a:8.1e}   S_eps EMPTY (z=0 correct at W=0) — skipped")
            continue
        pdepth = 1 + int(max((s - 1) % L for s in Se if s != 0)) if len(Se) > 1 else 1
        depth_work = min(L, pdepth + 10)
        allv = [0] + [1 + arm * L + j for arm in range(k_arms) for j in range(depth_work)]
        for B in [1, 9, 33, 129, 1 + 8 * depth_work]:
            cands = []
            if B == 1:
                for om in [omega_star(a), 1.9]:
                    cands.append((f"coord om={om:.2f}", pol_coord_sweep(allv, om)))
            else:
                p = (B - 1) // k_arms
                if p >= 1:
                    hubU = [0] + [1 + arm * L + j for arm in range(k_arms) for j in range(p)]
                    rest = [u for u in allv if u not in set(hubU)]
                    def mk(hubU=hubU, rest=rest):
                        def gen(P, S):
                            while True:
                                yield hubU, 1.9
                                for u in rest:
                                    yield [u], 1.0
                        return gen
                    cands.append((f"hub+8x{p} om=1.9", mk()))
                    def mk1(hubU=hubU, rest=rest):
                        def gen(P, S):
                            while True:
                                yield hubU, 1.0
                                for u in rest:
                                    yield [u], 1.0
                        return gen
                    cands.append((f"hub+8x{p} om=1.0", mk1()))
                cands.append((f"greedy{B}", pol_greedy(B, 1.0)))
            best = None
            for name, pol in cands:
                S, done = run_policy(P, pol, eps, max_ops=80000,
                                     check_every=max(1, len(allv) // max(1, B)))
                if done and (best is None or S.W_vol < best[1].W_vol):
                    best = (name, S)
            if best is None:
                print(f"{a:8.1e} {volS:6.0f} {B:5d}  none converged")
                continue
            name, S = best
            rows.append(dict(alpha=a, B=B, W=S.W_vol, volS=volS, ops=S.nops,
                             util=S.max_util_a, pol=name))
            print(f"{a:8.1e} {volS:6.0f} {B:5d} {name:>16} {S.nops:7d} "
                  f"{S.W_vol:9.0f} {S.W_vol/volS:8.2f} {S.max_util_a:7.3f}")
    OUT["spider_curves"] = rows


def star_greedy_check():
    print("\n== C3. star m=64: greedy top-B vs c+j policy (does greedy beat it?) ==")
    eps = 2.0 ** -9
    adj, seed = zoo.star(64)
    for a in [2.0 ** -10]:
        P = Prob(adj, a, seed)
        for B in [8, 33, 65]:
            S, done = run_policy(P, pol_greedy(B, 1.0), eps, max_ops=40000)
            S2, done2 = run_policy(P, pol_greedy(B, 1.9), eps, max_ops=40000)
            w = min([x.W_vol for x, d in [(S, done), (S2, done2)] if d] or [float("inf")])
            print(f"  alpha={a:.1e} B={B:3d}: greedy W_vol={w:9.0f}  "
                  f"utilA={max(S.max_util_a, S2.max_util_a):.3f}")


if __name__ == "__main__":
    tau_profiles()
    path_curves()
    spider_curves()
    star_greedy_check()
    json.dump(OUT, open("/home/claude/work/overnight/i5e/out/battery.json", "w"))
    print("\nsaved out/battery.json")
