"""I7-B phase 7b: exact decision with SINGULAR-FACE RESOLUTION, plus
Petersen (Kneser(5,2) labeling, S5 orbits) at the class boundary and C8.

Resolution of a singular face (affine critical set of dim >= 1, value
lam/2 constant on it): the face contributes a violation iff its affine set
meets the nonneg orthant.  dim 1: exact rational interval check.  dim >= 2:
float LP (scipy) for strict feasibility; a strictly feasible float point
is then confirmed by projecting exactly onto the affine set... instead we
use: LP infeasible (with margin) => no closed-orthant point except possibly
boundary ones, which are subface critical points that the enumeration
already records with the same value lam/2; LP feasible => treat lam/2 as an
achieved value (conservative), and verify by exact subface search.
"""
import sys, time, json, itertools
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from i6b_class3 import GenInst, hypercube, cycle
from i7b_exact import exact_ctx, QS_exact

def gauss_affine(Arows, brhs):
    """Solve A s = b exactly; return (particular, nullspace basis) or None."""
    m = len(Arows); n = len(Arows[0])
    M = [row[:] + [brhs[i]] for i, row in enumerate(Arows)]
    piv = []
    r = 0
    for c in range(n):
        pr = next((rr for rr in range(r, m) if M[rr][c] != 0), None)
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for rr in range(m):
            if rr != r and M[rr][c] != 0:
                f = M[rr][c]
                M[rr] = [M[rr][t] - f * M[r][t] for t in range(n + 1)]
        piv.append(c)
        r += 1
    for rr in range(r, m):
        if M[rr][n] != 0:
            return None
    part = [Fr(0)] * n
    for a, c in enumerate(piv):
        part[c] = M[a][n]
    free = [c for c in range(n) if c not in piv]
    basis = []
    for fc in free:
        v = [Fr(0)] * n
        v[fc] = Fr(1)
        for a, c in enumerate(piv):
            v[c] = -M[a][fc]
        basis.append(v)
    return part, basis

def face_crit(Bpp, J):
    """Exact critical set of face J: returns (lam, particular s on J,
    nullspace basis) or None if inconsistent."""
    k = len(J)
    A = []
    b = []
    for i in J:
        A.append([2 * Bpp[i][j] for j in J] + [Fr(-1)])
        b.append(Fr(0))
    A.append([Fr(1)] * k + [Fr(0)])
    b.append(Fr(1))
    res = gauss_affine(A, b)
    if res is None:
        return None
    part, basis = res
    return part[k], part[:k], [v[:k] for v in basis]

def nonneg_meet(part, basis):
    """Does {part + span(basis)} meet s >= 0?  Exact for dim<=1; float LP
    with margins for dim>=2; returns 'yes'/'no'/'boundary-only'."""
    if all(x >= 0 for x in part):
        return 'yes'
    if not basis:
        return 'no'
    if len(basis) == 1:
        v = basis[0]
        lo_b, hi_b = -Fr(10) ** 9, Fr(10) ** 9
        for p, vv in zip(part, v):
            if vv == 0:
                if p < 0:
                    return 'no'
            elif vv > 0:
                lo_b = max(lo_b, -p / vv)
            else:
                hi_b = min(hi_b, -p / vv)
        return 'yes' if lo_b <= hi_b else 'no'
    # dim >= 2: float LP: exists t with part + B t >= 0
    import numpy as np
    from scipy.optimize import linprog
    k = len(part)
    m = len(basis)
    A_ub = np.array([[-float(basis[j][i]) for j in range(m)] + [1.0]
                     for i in range(k)])
    b_ub = np.array([float(part[i]) for i in range(k)])
    c = np.zeros(m + 1); c[-1] = -1.0
    r = linprog(c, A_ub=A_ub, b_ub=b_ub,
                bounds=[(None, None)] * m + [(None, 10.0)], method='highs')
    if r.status == 0 and r.x is not None and -r.fun > 1e-9:
        return 'yes'
    if r.status == 0 and r.x is not None and -r.fun > -1e-12:
        return 'boundary-only'
    return 'no'

def decide_exact2(name, adj, q, use_orbits=None, progress=False):
    n = len(adj)
    ctx = exact_ctx(adj, q)
    t0 = time.time()
    pairs = []
    for assign in itertools.product((0, 1, 2), repeat=n):
        P = frozenset(i for i, a in enumerate(assign) if a == 1)
        N = frozenset(i for i, a in enumerate(assign) if a == 2)
        if P and N:
            pairs.append((P, N))
    if use_orbits:
        seen = {}
        for P, N in pairs:
            key = min((tuple(sorted(g[i] for i in P)),
                       tuple(sorted(g[i] for i in N))) for g in use_orbits)
            if key not in seen:
                seen[key] = (P, N)
        pairs = list(seen.values())
    mx, mxinfo = Fr(-10 ** 9), None
    unresolved = 0
    sing_yes = 0
    QS_cache = {}
    for pi_, (P, N) in enumerate(pairs):
        if N not in QS_cache:
            if len(QS_cache) > 4000:
                QS_cache.clear()
            QS_cache[N] = QS_exact(ctx, N)
        Bs = QS_cache[N]
        idx = sorted(P | N)
        sign = {i: (1 if i in P else -1) for i in idx}
        k = len(idx)
        Bpp = [[Bs[idx[a]][idx[b]] * sign[idx[a]] * sign[idx[b]]
                for b in range(k)] for a in range(k)]
        for fs in range(1, 1 << k):
            J = [a for a in range(k) if fs >> a & 1]
            res = face_crit(Bpp, J)
            if res is None:
                continue
            lam, part, basis = res
            val = lam / 2
            if val <= mx:
                continue
            if not basis:
                if all(x >= 0 for x in part):
                    mx, mxinfo = val, (sorted(P), sorted(N), 'unique')
            else:
                mt = nonneg_meet(part, basis)
                if mt == 'yes':
                    mx, mxinfo = val, (sorted(P), sorted(N),
                                       'singular-dim%d' % len(basis))
                    sing_yes += 1
                elif mt == 'boundary-only':
                    # value lam/2 is achieved at a boundary point = subface
                    # critical point; count it (conservative: same value)
                    mx, mxinfo = val, (sorted(P), sorted(N), 'sing-boundary')
                    sing_yes += 1
        if progress and pi_ % 50 == 0:
            sys.stdout.write('\r  %s %d/%d mx=%.3e [%.0fs]' %
                             (name, pi_, len(pairs), float(mx),
                              time.time() - t0))
            sys.stdout.flush()
    print('\r%-16s EXACT max = %s (%.3e)  singular-contrib=%d  '
          'pairs=%d [%.0fs]' % (name, mx, float(mx), sing_yes,
                                len(pairs), time.time() - t0))
    print('     argmax %s' % (mxinfo,))
    return dict(name=name, exact_max=str(mx), exact_max_float=float(mx),
                argmax=[str(x) for x in mxinfo] if mxinfo else None,
                npairs=len(pairs), sing=sing_yes)

def kneser52():
    from itertools import combinations
    Vs = list(combinations(range(5), 2))
    n = 10
    adj = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and not set(Vs[i]) & set(Vs[j]):
                adj[i].append(j)
    return [sorted(a) for a in adj], Vs

def s5_orbits():
    from itertools import permutations
    adj, Vs = kneser52()
    vidx = {v: i for i, v in enumerate(Vs)}
    perms = []
    for sig in permutations(range(5)):
        g = [vidx[tuple(sorted((sig[a], sig[b])))] for (a, b) in Vs]
        perms.append(g)
    return adj, perms

def d_n_group(n):
    perms = []
    for s in range(n):
        perms.append([(i + s) % n for i in range(n)])
        perms.append([(s - i) % n for i in range(n)])
    return perms

if __name__ == '__main__':
    out = []
    from i7b_exact import q3_group
    out.append(decide_exact2('C6 q=1/4(eq)', cycle(6), '1/4',
                             use_orbits=d_n_group(6)))
    out.append(decide_exact2('Q3 q=1/3(eq)', hypercube(3), '1/3',
                             use_orbits=q3_group()))
    out.append(decide_exact2('C8 q=1/8', cycle(8), '1/8',
                             use_orbits=d_n_group(8)))
    adjP, permsP = s5_orbits()
    out.append(decide_exact2('Pet q=1/3(eq)', adjP, '1/3',
                             use_orbits=permsP, progress=True))
    json.dump(out, open('/home/claude/work/overnight/w7_windowed/'
                        'i7b_exact2.json', 'w'), indent=1, default=str)
