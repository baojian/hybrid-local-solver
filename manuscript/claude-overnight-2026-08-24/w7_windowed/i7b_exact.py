"""I7-B phase 7: EXACT instance-level proof of  sup Psi <= 0  by rational
face-KKT enumeration (no eigensolves).

For the quadratic form q(s) = s^T B'' s on the simplex {s >= 0, 1^T s = 1},
the maximum is attained in the relative interior of some face J, where
2(B'' s)_i = lam (i in J), 1^T s = 1 — a rational linear system; the value
there is lam/2 (exactly, since q(s) = s.(B''s) = lam/2).  Enumerating all
faces of all mixed sign-pairs (P, N) gives the exact max of Psi* over the
union of pattern cones; pairs with P or N empty are proved <= 0 by the
per-mode algebra (N-/F-lemma).  Rational throughout.
"""
import sys, time, json, itertools
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from i6b_class3 import GenInst, hypercube, cycle, petersen

def exact_ctx(adj, q):
    n = len(adj)
    I = GenInst(adj, [Fr(1, n)] * n, Fr(q), Fr(1, 8 * n * n))
    d, vol = I.d, I.vol
    m0, be = I.m0, I.beta
    nu = I.q / (1 + I.q)
    M = I.Mm
    def mat_mul(A, B):
        return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)]
                for i in range(n)]
    def mat_add(A, B, ca=1, cb=1):
        return [[ca * A[i][j] + cb * B[i][j] for j in range(n)]
                for i in range(n)]
    Iden = [[Fr(1) if i == j else Fr(0) for j in range(n)] for i in range(n)]
    P = [[(Fr(1) if i == j else Fr(0)) - d[j] / vol for j in range(n)]
         for i in range(n)]
    M2 = mat_mul(M, M)
    A_op = mat_add(mat_mul(M, Iden), M2, m0, -1)      # m0 M - M^2 = M(m0-M)
    G = mat_add(mat_add(Iden, M, m0, -2), M2)         # m0 - 2M + M^2
    S = mat_add(mat_mul(M, Iden), G, nu * nu * m0, be)
    # S_reg = S + J, J u = (d.u/vol) 1
    S_reg = [[S[i][j] + d[j] / vol for j in range(n)] for i in range(n)]
    # invert S_reg
    Aug = [row[:] + [Fr(1) if k == i else Fr(0) for k in range(n)]
           for i, row in enumerate(S_reg)]
    for c in range(n):
        p = next(r for r in range(c, n) if Aug[r][c] != 0)
        Aug[c], Aug[p] = Aug[p], Aug[c]
        pv = Aug[c][c]
        Aug[c] = [x / pv for x in Aug[c]]
        for r in range(n):
            if r != c and Aug[r][c] != 0:
                f = Aug[r][c]
                Aug[r] = [Aug[r][k] - f * Aug[c][k] for k in range(2 * n)]
    Sinv = [row[n:] for row in Aug]
    return dict(n=n, I=I, d=d, vol=vol, m0=m0, be=be, nu=nu, M=M, P=P,
                M2=M2, A=A_op, Sinv=Sinv,
                mm=mat_mul, ma=mat_add)

def QS_exact(ctx, N):
    n, d, nu = ctx['n'], ctx['d'], ctx['nu']
    mm = ctx['mm']
    P, M, A, Sinv = ctx['P'], ctx['M'], ctx['A'], ctx['Sinv']
    R = [[Fr(-1) if (i == j and i in N) else Fr(0) for j in range(n)]
         for i in range(n)]
    PR = mm(P, R)
    T1 = mm(M, PR)
    T2 = mm(M, T1)
    AzP = mm(A, P)
    # B = T1^T D T1 + T2^T D P + P^T D T2 - P^T D AzP + nu^2 L^T D Sinv L
    def tdm(X, Y):        # X^T D Y
        return [[sum(X[k][i] * d[k] * Y[k][j] for k in range(n))
                 for j in range(n)] for i in range(n)]
    L = [[AzP[i][j] - T2[i][j] for j in range(n)] for i in range(n)]
    DSL = mm([[d[i] * Sinv[i][j] / 1 for j in range(n)] for i in range(n)], L)
    # careful: L^T (D Sinv) L: D Sinv is symmetric
    B1 = tdm(T1, T1)
    B2 = tdm(T2, P)
    B4 = tdm(P, AzP)
    B5 = [[sum(L[k][i] * DSL[k][j] for k in range(n)) for j in range(n)]
          for i in range(n)]
    B = [[B1[i][j] + B2[i][j] + B2[j][i] - B4[i][j] + nu * nu * B5[i][j]
          for j in range(n)] for i in range(n)]
    return [[(B[i][j] + B[j][i]) / 2 for j in range(n)] for i in range(n)]

def solve_face(Bpp, J):
    """KKT on face J: 2(B s)_i = lam (i in J), sum_J s = 1.
    Return list of (value, s, flag) — value = lam/2 when a solution with
    s >= 0 on J exists; flag marks singular-with-negative-particular."""
    k = len(J)
    # unknowns: s_0..s_{k-1}, lam
    rows = []
    for a, i in enumerate(J):
        row = [2 * Bpp[i][j] for j in J] + [Fr(-1), Fr(0)]
        rows.append(row)
    rows.append([Fr(1)] * k + [Fr(0), Fr(1)])
    m, nn = k + 1, k + 1
    # gauss with consistency
    piv_cols = []
    r = 0
    for c in range(nn):
        pr = next((rr for rr in range(r, m) if rows[rr][c] != 0), None)
        if pr is None:
            continue
        rows[r], rows[pr] = rows[pr], rows[r]
        pv = rows[r][c]
        rows[r] = [x / pv for x in rows[r]]
        for rr in range(m):
            if rr != r and rows[rr][c] != 0:
                f = rows[rr][c]
                rows[rr] = [rows[rr][t] - f * rows[r][t] for t in range(nn + 1)]
        piv_cols.append(c)
        r += 1
        if r == m:
            break
    # consistency
    for rr in range(r, m):
        if rows[rr][nn] != 0:
            return []                      # inconsistent: no critical point
    sol = [Fr(0)] * nn
    for a, c in enumerate(piv_cols):
        sol[c] = rows[a][nn]
    s = sol[:k]; lam = sol[k]
    if all(x >= 0 for x in s):
        return [(lam / 2, s, 'ok')]
    if r < m:
        return [(lam / 2, s, 'SING-NEG')]  # flag: affine set, particular < 0
    return []                              # unique solution, not in cone

def decide_exact(name, adj, q, use_orbits=None):
    n = len(adj)
    ctx = exact_ctx(adj, q)
    t0 = time.time()
    verts = list(range(n))
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
    mx = Fr(-10**9)
    mxinfo = None
    nflag = 0
    QS_cache = {}
    for (P, N) in pairs:
        if N not in QS_cache:
            QS_cache[N] = QS_exact(ctx, N)
        Bs = QS_cache[N]
        idx = sorted(P | N)
        sign = {i: (1 if i in P else -1) for i in idx}
        k = len(idx)
        Bpp = [[Bs[idx[a]][idx[b]] * sign[idx[a]] * sign[idx[b]]
                for b in range(k)] for a in range(k)]
        for fs in range(1, 1 << k):
            J = [a for a in range(k) if fs >> a & 1]
            for val, s, flag in solve_face(Bpp, J):
                if flag == 'SING-NEG':
                    if val > 0:
                        nflag += 1
                    continue
                if val > mx:
                    mx = val
                    mxinfo = (sorted(P), sorted(N), [str(x) for x in s], flag)
    print('%-14s EXACT max over mixed-pair cones = %s (%.3e)  '
          'flags(sing,lam>0)=%d  pairs=%d  [%.0fs]' %
          (name, mx, float(mx), nflag, len(pairs), time.time() - t0))
    print('     at P=%s N=%s' % (mxinfo[0], mxinfo[1]))
    return dict(name=name, exact_max=str(mx), exact_max_float=float(mx),
                nflag=nflag, npairs=len(pairs), argmax=mxinfo)

def q3_group():
    perms = []
    for mask in range(8):
        for sig in itertools.permutations(range(3)):
            g = []
            for v in range(8):
                u = v ^ mask
                w = 0
                for b in range(3):
                    if u >> b & 1:
                        w |= 1 << sig[b]
                g.append(w)
            perms.append(g)
    return perms

if __name__ == '__main__':
    out = []
    out.append(decide_exact('C6 q=1/10', cycle(6), '1/10'))
    out.append(decide_exact('C6 q=1/4(eq)', cycle(6), '1/4'))
    out.append(decide_exact('Q3 q=1/3(eq)', hypercube(3), '1/3',
                            use_orbits=q3_group()))
    json.dump(out, open('/home/claude/work/overnight/w7_windowed/'
                        'i7b_exact.json', 'w'), indent=1, default=str)
