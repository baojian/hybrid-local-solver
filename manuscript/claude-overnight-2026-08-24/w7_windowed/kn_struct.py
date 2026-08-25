"""I2-C addendum: (A) structural inequalities of the K_n theorem as exact
rational statements in (n,q) alone; (B) CC-stage exact decay; (C) window
telescope table.  No floating point in the decision steps.
"""
import sys, math, json
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from kn_modal import KnModal


def params(n, q):
    al = q * q / (1 + q * q)
    kap = 1 - 2 * al
    be = (1 - q) / (1 + q)
    lam = al + (1 - al) * Fr(n, 2 * (n - 1))
    mh = kap / (kap + lam)
    return al, kap, be, lam, mh, mh * (1 + be), mh * be


print("== A1. algebraic identities (exact, symbolic-by-instance) ==")
bad = []
for n in (2, 3, 4, 8, 16, 32, 64, 1024):
    for q in (Fr(1, 2), Fr(1, 3), Fr(1, 8), Fr(1, 10), Fr(1, 100), Fr(1, 400),
              Fr(1, 4000)):
        al, kap, be, lam, mh, p, s = params(n, q)
        m0 = kap / (kap + al)
        chi = mh * mh - p * mh + s
        ok = [
            m0 == 1 - q * q,                              # low-mode gain
            m0 * (1 + be) == 2 * (1 - q) and m0 * be == (1 - q) ** 2,
            chi == s * (1 - mh),                          # chi(mh) = s(1-mh)
            1 - p * p / (4 * s) == 1 - mh / (1 - q * q),  # discriminant form
            (p * p < 4 * s) == (lam > al),                # underdamped <=> ..
            (s <= (1 - q) ** 2) == (mh <= 1 - q * q),
            lam > al,
        ]
        if not all(ok):
            bad.append((n, str(q), ok))
print("   identities hold on %d (n,q) cells; failures: %s" %
      (8 * 7, bad if bad else "none"))

print("\n== A2. C16  s*(2-mh) <= (1-q)^2  (F-stage contraction) ==")
print("   worst case is n -> infinity (lam_h decreasing in n => mh maximal).")
rows = []
for q in (Fr(1, 2), Fr(51, 100), Fr(52, 100), Fr(55, 100), Fr(6, 10),
          Fr(1, 3), Fr(1, 4), Fr(1, 8), Fr(1, 10), Fr(1, 100), Fr(1, 400)):
    al = q * q / (1 + q * q)
    kap = 1 - 2 * al
    be = (1 - q) / (1 + q)
    lam_inf = (1 + al) / 2                       # n -> infinity
    mh = kap / (kap + lam_inf)
    s = mh * be
    lhs, rhs = s * (2 - mh), (1 - q) ** 2
    rows.append((str(q), float(lhs), float(rhs), lhs <= rhs))
for r in sorted(rows, key=lambda r: -Fr(r[0])):
    print("   q=%-8s LHS=%.6f  (1-q)^2=%.6f   %s" %
          (r[0], r[1], r[2], "OK" if r[3] else "FAIL"))
# exact threshold: largest q on a fine grid where it still holds
thr = None
for k in range(2, 200):
    q = Fr(k, 200)
    al = q * q / (1 + q * q); kap = 1 - 2 * al; be = (1 - q) / (1 + q)
    mh = kap / (kap + (1 + al) / 2); s = mh * be
    if s * (2 - mh) <= (1 - q) ** 2:
        thr = q
print("   holds for every q on the 1/200-grid up to q =", thr,
      "(fails above); n-finite is strictly easier.")
# check finite n monotonicity: mh decreasing in n
mono = all(params(n, Fr(1, 10))[4] > params(n + 1, Fr(1, 10))[4]
           for n in range(2, 40))
print("   mh strictly decreasing in n (q=1/10, n=2..40):", mono)

print("\n== B. CC stages: Delta <= beta*min_i d_i  =>  V_{t+1} = s V_t ==")


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def split(v, n):
    m = sum(v) / n
    return m, [v[i] - m for i in range(n)]


tot = [0, 0]
detail = []
fams = []
for n in (2, 4, 8, 16, 32):
    for q in (Fr(1, 10), Fr(1, 100), Fr(1, 400)):
        for nm, seed in (('skew', [Fr(1, 2)] + [Fr(1, 2 * (n - 1))] * (n - 1)),
                         ('ramp', [Fr(i + 1, n * (n + 1) // 2)
                                   for i in range(n)])):
            rho = min(seed) / (2 * (n - 1))
            fams.append(('K%d q=1/%d %s' % (n, int(1 / q), nm), n, seed, q,
                         rho, 26 if q == Fr(1, 10) else 44))
fams.append(('K8 pulse', 8, [Fr(363437, 651088)] + [Fr(41093, 651088)] * 7,
             Fr(1, 10), Fr(1, 112), 20))
wins = []
for (nm, n, seed, q, rho, T) in fams:
    K = KnModal(n, seed, q, rho,
                alpha=Fr(1, 101) if nm == 'K8 pulse' else None)
    recs, xs = K.run(T)
    E = [[K.xstar[i] - xs[k][i] for i in range(n)] for k in range(len(xs))]
    s, p = K.s, K.p
    V = {}
    for t in range(1, len(xs) - 1):
        Lm, hm = split(E[t], n); L, h = split(E[t + 1], n)
        V[t] = dot(h, h) - p * dot(h, hm) + s * dot(hm, hm)
    for t in range(1, T - 1):
        rec = recs[t]
        if rec['cls'] == 'N':
            continue
        mnd = min(rec['dt'])
        if rec['Delta'] <= K.beta * mnd:            # CC stage
            tot[1] += 1
            ok = (V[t + 1] == s * V[t]) and all(x == rec['Delta']
                                                for x in rec['r'])
            tot[0] += ok
            if not ok:
                detail.append((nm, t))
    # window telescope, w = ceil(1/q)
    w = math.ceil(1 / q)
    J, rowsw = 0.0, []
    for t, r in enumerate(recs):
        if r['gamma'] > 1:
            J += math.log(r['gamma'])
        rowsw.append(J)
    nw = T // w
    per = [rowsw[(j + 1) * w - 1] - (rowsw[j * w - 1] if j else 0.0)
           for j in range(nw)]
    wins.append((nm, w, [round(v, 6) for v in per], round(rowsw[-1], 6)))
print("   CC stages found: %d ; V_{t+1}==s*V_t and r==Delta*1 on %d of them %s"
      % (tot[1], tot[0], "" if not detail else detail[:5]))

print("\n== C. window telescope, w=ceil(1/q): per-window inflation (nats) ==")
for (nm, w, per, tot_) in wins[:8] + wins[-3:]:
    print("   %-22s w=%-4d J_total=%.6f  windows: %s" %
          (nm, w, tot_, per[:4]))
print("   (every window after the first contributes exactly 0)")
