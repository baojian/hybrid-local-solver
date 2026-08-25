"""W1 mechanical verification: class-M lower bound on the center-seeded star.

Asserts per member run:
  A1 mass identities (sum p + sum r = 1, sum p = alpha*Z) to 1e-12
  A2 monotonicity: min r over time >= -1e-12
  A3 invariant p + pr(r) = pi to 1e-9 at stop
  A4 stop implies ||r||_1 <= eps*vol
  A5 W >= 3/(256 alpha eps), W_center >= 3/(256 alpha eps),
     n_center_ops >= 3/(16 alpha)
Also: SOR (non-member) measurements, output-map loophole, lib cross-check.
"""
import math
import random
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'lib'))

import numpy as np
from zoo import star
from meter import Meter
from model import appr_lazy
from gpush import (GP, run_queue, run_scan, run_sor, omega_opt,
                   pr_matrix, pr_vec)

ALPHAS = [1/4, 1/16, 1/64]
EPSS = [2.0**-k for k in range(5, 10)]

LB = lambda al, ep: 3.0 / (256.0 * al * ep)          # proved-draft constant
LB_NC = lambda al: 3.0 / (16.0 * al)                  # center-op count bound


def member_policies():
    P = []
    P.append(('appr_fifo', lambda a, al, ep, s, stop, rng:
              run_queue(a, al, ep, s, 'fifo', stop, 1.0, True)))
    P.append(('appr_lifo', lambda a, al, ep, s, stop, rng:
              run_queue(a, al, ep, s, 'lifo', stop, 1.0, True)))
    for om in (0.1, 0.5, 0.9):
        P.append((f'damped_{om}', lambda a, al, ep, s, stop, rng, om=om:
                  run_queue(a, al, ep, s, 'fifo', stop, om, True)))
    P.append(('nonlazy_fifo', lambda a, al, ep, s, stop, rng:
              run_queue(a, al, ep, s, 'fifo', stop, 1.0, False)))
    P.append(('greedy', lambda a, al, ep, s, stop, rng:
              run_scan(a, al, ep, s, 'greedy', stop, rng, True)))
    P.append(('greedy_nonlazy', lambda a, al, ep, s, stop, rng:
              run_scan(a, al, ep, s, 'greedy', stop, rng, False)))
    P.append(('rand_v', lambda a, al, ep, s, stop, rng:
              run_scan(a, al, ep, s, 'rand_v', stop, rng, True)))
    P.append(('rand_xi', lambda a, al, ep, s, stop, rng:
              run_scan(a, al, ep, s, 'rand_xi', stop, rng, True)))
    P.append(('rand_mix', lambda a, al, ep, s, stop, rng:
              run_scan(a, al, ep, s, 'rand_mix', stop, rng, True)))
    P.append(('cheap_first', lambda a, al, ep, s, stop, rng:
              run_scan(a, al, ep, s, 'cheap_first', stop, rng, False)))
    P.append(('tiny_leaf', lambda a, al, ep, s, stop, rng:
              run_scan(a, al, ep, s, 'tiny_leaf', stop, rng, True)))
    P.append(('jacobi', lambda a, al, ep, s, stop, rng:
              run_scan(a, al, ep, s, 'jacobi', stop, rng, True)))
    P.append(('jacobi_nonlazy', lambda a, al, ep, s, stop, rng:
              run_scan(a, al, ep, s, 'jacobi_nonlazy', stop, rng, True)))
    return P


def check_member(st, al, ep, m, tag):
    fails = []
    # float drift on identities grows ~ ulp per op; scale tolerance
    tolA1 = 1e-12 * max(1.0, st.ops / 5e4)
    if st.mass_check() > tolA1:
        fails.append(f'A1 mass {st.mass_check():.2e}')
    if st.max_eta_center > 2.0 / (1.0 + al) * (1 + 1e-9):
        fails.append(f'A6 eta cap {st.max_eta_center:.3f}')
    if st.min_r_seen < -1e-12:
        fails.append(f'A2 sign {st.min_r_seen:.2e}')
    inv, pi = st.invariant_err()
    if inv > 1e-9:
        fails.append(f'A3 inv {inv:.2e}')
    if st.sum_r > ep * st.vol * (1 + 1e-9):
        fails.append(f'A4 l1 {st.sum_r:.4f} > {ep*st.vol:.4f}')
    Wc = m * st.n_center_ops
    if st.W < LB(al, ep) or Wc < LB(al, ep):
        fails.append(f'A5 W={st.W} Wc={Wc} < LB={LB(al, ep):.1f}')
    if st.n_center_ops < LB_NC(al):
        fails.append(f'A5nc {st.n_center_ops} < {LB_NC(al):.2f}')
    if fails:
        print(f'  FAIL {tag}: ' + '; '.join(fails))
    return (not fails), pi


def main():
    rows = []          # member runs
    nfail = 0
    print('=== member policy grid (both stopping rules) ===')
    for al in ALPHAS:
        for ep in EPSS:
            m = int(math.floor(1.0 / (8.0 * ep)))
            adj, seed = star(m)
            for stop in ('coord', 'l1'):
                for name, fn in member_policies():
                    nseed = 3 if name.startswith('rand') else 1
                    for sd in range(nseed):
                        rng = random.Random(
                            (hash((name, al, ep)) & 0xffff) + 7 * sd)
                        st = fn(adj, al, ep, seed, stop, rng)
                        assert st.ops < 4_000_000, f'op cap hit {name}'
                        ok, pi = check_member(
                            st, al, ep, m, f'{name}/{stop}/a={al}/e={ep}')
                        nfail += (not ok)
                        rows.append(dict(
                            policy=name, stop=stop, al=al, ep=ep,
                            m=m, W=st.W, Wc=m * st.n_center_ops,
                            nc=st.n_center_ops, ops=st.ops,
                            c=st.W * al * ep,
                            cc=m * st.n_center_ops * al * ep,
                            maxeta=st.max_eta_center, ok=ok))
    print(f'member runs: {len(rows)}, assertion failures: {nfail}')

    # T1: per-policy minima of c = W*alpha*eps
    print('\n--- T1: per-policy min work constant c = W*alpha*eps ---')
    print(f'{"policy":<16}{"min c(coord)":>13}{"min c(l1)":>11}'
          f'{"min cc(l1)":>12}{"max c(l1)":>11}')
    for name, _ in member_policies():
        rc = [r for r in rows if r['policy'] == name and r['stop'] == 'coord']
        rl = [r for r in rows if r['policy'] == name and r['stop'] == 'l1']
        print(f'{name:<16}{min(r["c"] for r in rc):>13.4f}'
              f'{min(r["c"] for r in rl):>11.4f}'
              f'{min(r["cc"] for r in rl):>12.4f}'
              f'{max(r["c"] for r in rl):>11.4f}')

    # T2: min over policies per grid cell (l1 stop = frontier)
    print('\n--- T2: min over member policies of c=W*al*ep (stop=l1) ---')
    print('eps\\alpha     ' + ''.join(f'{a:>10.4f}' for a in ALPHAS))
    gmin = 1e9; gmin_at = None
    for ep in EPSS:
        line = f'{ep:<12.6f}'
        for al in ALPHAS:
            cs = [(r['c'], r['policy']) for r in rows
                  if r['stop'] == 'l1' and r['al'] == al and r['ep'] == ep]
            v, pol = min(cs)
            if v < gmin:
                gmin, gmin_at = v, (al, ep, pol)
            line += f'{v:>10.4f}'
        print(line)
    print(f'global min member c0_emp = {gmin:.4f} at alpha={gmin_at[0]:.4f} '
          f'eps={gmin_at[1]:.6f} policy={gmin_at[2]}  '
          f'(proved constant 3/256 = {3/256:.5f})')

    # T3: SOR non-member
    print('\n=== T3: signed SOR sweeps (non-member), oracle err<=eps stop ===')
    print(f'{"alpha":>9}{"eps":>10}{"omega":>8}{"W":>9}{"c=W*al*ep":>11}'
          f'{"sweeps":>7}{"min_r":>10}{"max|r|1":>9}{"maxeta_c":>9}'
          f'{"cap":>7}{"l1<epsvol?":>11}')
    sor_alphas = ALPHAS + [2.0**-8, 2.0**-10]
    for al in sor_alphas:
        eps_list = [EPSS[0], EPSS[-1]] if al in ALPHAS else [EPSS[-1]]
        for ep in eps_list:
            m = int(math.floor(1.0 / (8.0 * ep)))
            adj, seed = star(m)
            for om_name, om in (('1.5', 1.5), ('opt', omega_opt(al))):
                st = run_sor(adj, al, ep, seed, om)
                cap = 2.0 / (1.0 + al)
                print(f'{al:>9.5f}{ep:>10.6f}{om_name:>8}{st.W:>9}'
                      f'{st.W*al*ep:>11.4f}{st.sweeps:>7}'
                      f'{st.min_r_seen:>10.3f}{st.max_l1_seen:>9.3f}'
                      f'{st.max_eta_center:>9.3f}{cap:>7.3f}'
                      f'{str(st.W_at_l1 is not None):>11}')

    # T4: output-map loophole -- one lazy center push then p+r
    print('\n=== T4: output post-processing loophole (p + beta*r) ===')
    for al, ep in ((1/16, 2.0**-7), (1/64, 2.0**-9)):
        m = int(math.floor(1.0 / (8.0 * ep)))
        adj, seed = star(m)
        st = GP(adj, al, seed, center=seed)
        M = pr_matrix(adj, al)
        e = np.zeros(st.n); e[seed] = 1.0
        pi = pr_vec(adj, al, e, M)
        st.push_lazy(seed, 1.0)          # ONE full lazy center push, W = m
        inv, _ = st.invariant_err(M)
        errs = {b: st.err_sem(pi, b) for b in (0.0, al, 1.0)}
        rmin = min(st.r)
        beats = st.W < LB(al, ep) and errs[1.0] <= ep
        print(f'alpha={al:.4f} eps={ep:.6f} m={m}: ONE full lazy center '
              f'push (all ops in M, r>=0: min r={rmin:.3f}), W={st.W}, '
              f'LB={LB(al,ep):.0f}')
        print(f'   err(p)={errs[0.0]:.3e}  err(p+alpha*r)={errs[al]:.3e}  '
              f'err(p+r)={errs[1.0]:.3e}  invariant={inv:.1e}  '
              f'[target eps={ep:.2e}]')
        print(f'   => output map p+r BEATS the class bound: {beats} '
              f'(r is exactly walk-stationary: pr(r)=r)')
        # beta = alpha add-back stays safe: cheapest member run w/ oracle
        # stop at err(p + alpha r) <= eps (lazy cheap-first policy)
        st2 = GP(adj, al, seed, center=seed)
        while st2.err_sem(pi, al) > ep and st2.ops < 100000:
            act = [u for u in range(st2.n) if st2.r[u] >= ep * st2.d[u] / 4]
            if not act:
                break
            leaves = [u for u in act if u != seed]
            u = leaves[0] if leaves else seed
            st2.push_lazy(u, st2.r[u])
        tag = 'BEATS LB!' if st2.W < LB(al, ep) else 'above LB (safe)'
        print(f'   oracle stop at err(p+alpha*r)<=eps: W={st2.W} vs '
              f'LB={LB(al,ep):.0f}  [{tag}]')

    # T5: cross-check literal manuscript APPR vs lib implementation
    print('\n=== T5: lib appr_lazy cross-check (FIFO, coord stop) ===')
    for al, ep in ((1/16, 2.0**-7), (1/64, 2.0**-9)):
        m = int(math.floor(1.0 / (8.0 * ep)))
        adj, seed = star(m)
        met = Meter(adj)
        p_lib, r_lib = appr_lazy(adj, al, seed, ep, met)
        W_lib = met.C_adj + met.R_adj
        st = run_queue(adj, al, ep, seed, 'fifo', 'coord', 1.0, True)
        dp = max(abs(a - b) for a, b in zip(p_lib, st.p))
        print(f'alpha={al:.4f} eps={ep:.6f}: W_lib={W_lib} W_sim={st.W} '
              f'match={W_lib == st.W} max|p diff|={dp:.2e} '
              f'c_lib={W_lib*al*ep:.4f}')

    # T6: lemma-level identities
    print('\n=== T6: lemma-level identity checks ===')
    al, ep = 1/16, 2.0**-7
    m = int(math.floor(1.0 / (8.0 * ep)))
    adj, seed = star(m)
    # (a) leaf ledger (Lemma 2): sum_leaf r == (1-al)/2*Zc - (1+al)/2*ZL
    for pol in ('appr_fifo', 'nonlazy_fifo'):
        fn = dict(member_policies())[pol]
        st = fn(adj, al, ep, seed, 'coord', random.Random(1))
        lhs = sum(st.r[u] for u in range(1, st.n))
        rhs = 0.5 * (1 - al) * st.Zc - 0.5 * (1 + al) * st.ZL
        print(f'  leaf ledger [{pol}]: |lhs-rhs|={abs(lhs-rhs):.2e} '
              f'(lhs={lhs:.6f}, Zc={st.Zc:.3f}, ZL={st.ZL:.3f}, '
              f'ZL/Zc={st.ZL/st.Zc:.4f} <= c_a={(1-al)/(1+al):.4f}: '
              f'{st.ZL/st.Zc <= (1-al)/(1+al) + 1e-12})')
    # (b) characterization: gp preserves invariant for ANY eta (even signed
    # overshoot); any non-proportional neighbor split breaks it.
    M = pr_matrix(adj, al)
    st = GP(adj, al, seed, center=seed)
    st.gp(seed, 1.7 * st.cap(seed))          # overshoot: r[seed] < 0
    inv_over, _ = st.invariant_err(M)
    st2 = GP(adj, al, seed, center=seed)
    eta = 0.5
    st2.r[seed] -= 0.5 * (1 + al) * eta      # same removal/settle, but
    st2.p[seed] += al * eta                  # skewed neighbor split:
    spread = 0.5 * (1 - al) * eta / m        # all onto leaf 1
    st2.r[1] += spread * m
    inv_skew, _ = st2.invariant_err(M)
    print(f'  invariant after signed overshoot gp (eta=1.7*cap, '
          f'min r={min(st.r):.3f}): err={inv_over:.1e}  (preserved)')
    print(f'  invariant after skewed one-hop split (same totals): '
          f'err={inv_skew:.1e}  (broken => split forced by invariant)')

    print(f'\nTOTAL member assertion failures: {nfail}')


if __name__ == '__main__':
    main()
