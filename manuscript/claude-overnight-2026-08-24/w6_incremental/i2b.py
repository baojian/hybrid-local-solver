"""I2-B harness: COMB adversary + all-backend comparison for SEG-LDL.

comb(B, T): backbone b_0..b_{B-1} (path), each b_i carries a pendant path
(tooth) of T vertices.  Seed at b_0 (one backbone end).  With T ~ c/sqrt(alpha)
the teeth are exactly as "deep in value" as the backbone is long, so the
value-ordered admission interleaves backbone growth with ~sqrt(vol) teeth.
"""
import sys, time, math, json, random
import numpy as np

sys.path.insert(0, '/home/claude/work/overnight/lib')
sys.path.insert(0, '/home/claude/work/overnight/w6_incremental')
from model import Model
from meter import Meter
import core
import dyn_ldl
import dyn_ldl2


def comb(B, T):
    """Backbone length B, teeth of T vertices each. Seed = backbone end 0."""
    edges = [(i, i + 1) for i in range(B - 1)]
    nid = B
    for i in range(B):
        prev = i
        for _ in range(T):
            edges.append((prev, nid)); prev = nid; nid += 1
    adj = {u: set() for u in range(nid)}
    for u, v in edges:
        adj[u].add(v); adj[v].add(u)
    return {u: sorted(adj[u]) for u in range(nid)}, 0


def rrt(n, rng_seed=7):
    """Random recursive tree: vertex i attaches to uniform j<i."""
    rng = random.Random(rng_seed)
    adj = {u: set() for u in range(n)}
    for i in range(1, n):
        j = rng.randrange(i)
        adj[i].add(j); adj[j].add(i)
    return {u: sorted(adj[u]) for u in range(n)}, 0


def est_S(model, x0, eps):
    """Cheap proxy for |S*|: #{v : x0_v / sqd_v >= 0.5*alpha*eps}."""
    return int(np.sum(x0 / model.sqd >= 0.5 * model.alpha * eps))


def tune_eps(model, lo_target, hi_target, x0=None, emin=-26, emax=-2):
    """Pick eps = 2^-k whose proxy active-set size lands in [lo,hi]."""
    if x0 is None:
        x0 = model.solve_exact()
    best, bestk = None, None
    for k in range(-emax, -emin + 1):
        eps = 2.0 ** (-k)
        s = est_S(model, x0, eps)
        if lo_target <= s <= hi_target:
            return eps, s
        if s < hi_target:
            best, bestk = s, eps
    return (bestk if bestk is not None else 2.0 ** emin), (best or 0)


def tune_eps_trace(model, cap_S, keep_Q=False, kmax=34, tmax=90.0):
    """Finest eps=2^-k whose ACTUAL grown active set has |S*| <= cap_S.
    Returns (eps, trace).  The greedy loop under-estimates x, so a value
    proxy is unusable; we grow the real trace (cheap: cost ~ final run)."""
    prev = None
    for k in range(0, kmax + 1):
        eps = 2.0 ** -k
        t0 = time.time()
        tr = core.grow_trace(model, eps, keep_Q=keep_Q)
        sz = len(tr['S'])
        if sz > cap_S or time.time() - t0 > tmax:
            if prev is not None:
                return prev
            return eps, tr
        prev = (eps, tr)
    return prev


def run_all(model, eps, want, keep_Q=False, inc_cap=(4e6, 4e8), verbose=True,
            tr=None):
    t0 = time.time()
    if tr is None:
        tr = core.grow_trace(model, eps, keep_Q=keep_Q)
    adj = model.adj
    rounds = tr['rounds']
    E = sum(1 for r in rounds if r['T'])
    volS = rounds[-1]['volS']
    rec = dict(eps=eps, alpha=model.alpha, n=model.n, S=len(tr['S']),
               volS=volS, cvolS=core.cvol(adj, tr['S']), E=E,
               nrounds=len(rounds),
               meanT=float(np.mean([len(r['T']) for r in rounds if r['T']]))
               if E else 0.0,
               trace_wall=time.time() - t0, bk={})
    om = Meter(adj); core.outer_charge(model, tr, om)
    rec['outer'] = om.total()
    ol = core.oracle_ledgers(model, tr)
    rec['bk']['ORACLE-SDD'] = dict(total=ol['sdd'])
    rec['bk']['ORACLE-INC'] = dict(total=ol['inc'])
    for name in want:
        t1 = time.time()
        try:
            if name == 'COLD-LU':
                d = core.replay_cold_lu(model, tr); tot = d['meter']['total']
            elif name == 'INC-LDL':
                d = dyn_ldl.replay_inc_ldl_capped(model, tr, nnzcap=inc_cap[0],
                                                  respcap=inc_cap[1])
                tot = d['meter']['total']
            elif name == 'TREE-INC':
                d = core.replay_tree_inc(model, tr); tot = d['meter']['total']
            elif name == 'SEG-LDL':
                d = dyn_ldl.replay_seg_ldl(model, tr); tot = d['meter']['total']
            elif name == 'HSEG-LDL':
                d = dyn_ldl2.replay_hseg(model, tr); tot = d['meter']['total']
            elif name == 'CG-WARM':
                d = core.replay_cg(model, tr, warm=True); tot = d['meter']['total']
            else:
                continue
            d = {k: v for k, v in d.items() if k != 'meter'}
            d['total'] = float(tot)
            d['Wvol'] = float(tot) / volS
            d['wall'] = time.time() - t1
            rec['bk'][name] = d
        except Exception as ex:
            rec['bk'][name] = dict(error=f"{type(ex).__name__}: {ex}"[:200],
                                  wall=time.time() - t1)
        if verbose:
            b = rec['bk'][name]
            print(f"    {name:9s} W/vol={b.get('Wvol', float('nan')):12.2f}"
                  f" {'CAPPED' if b.get('capped') else ''}"
                  f"{b.get('error', '')} ({b.get('wall', 0):.1f}s)", flush=True)
    rec['reroot'] = dyn_ldl.reroot_ledger(model, tr)
    return rec
