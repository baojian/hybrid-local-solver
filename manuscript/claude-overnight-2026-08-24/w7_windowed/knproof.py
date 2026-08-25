"""I2-C: exact verification of every inequality in the K_n windowed/absorption
theorem draft, on K2, K8 (pulse + small-q), K16, K32. All checks in Fractions.

Lemma tags (see findings/i2c_windowed_proof.md):
  L-A  modal reduction: Q on K_n full face has eigenvalues alpha (1-mode) and
       lambda_h = alpha+(1-alpha)n/(2(n-1)) on 1^perp; master identity
       (Q+kappa I) e_{t+1} = kappa (x*-ell_t).
  L-B  F-collapse: full correction => ell_t = x_t => e_{t+1} = M e_t
       (modal: L_{t+1}=m0 L_t, h_{t+1}=mh h_t).
  L-C  N-stage V-Lyapunov: V_t = |h_t|^2 - p<h_t,h_{t-1}> + s|h_{t-1}|^2,
       V_{t+1} = s V_t exactly on N stages (p=mh(1+beta), s=mh*beta).
  L-D  trigger: Delta_t>0 => min_i [alpha taL + lambda_h tah_i] < 0; and
       alpha*Delta_t = max_i [-(alpha taL + lambda_h tah_i)]_+.
  L-E  oscillation (no low->high pump): |P_h r_t|^2 <= beta^2 |P_h d_t|^2.
  L-F  defect bound (ms 15): Dfin_t <= a_q (|e_{t-1}|_D^2 - |e_t|_D^2),
       and 2 Phi_t >= mu |e_t|_D^2  => log gamma_t <= log(1+a_q(rho_t-1)).
  L-G  absorption certificate (rational):
       (i)  L_t >= (1-q) L_{t-1}
       (ii) C_ta * V_t <= dn_lb * (alpha*beta/lambda_h)^2 * L_{t-1}^2
       with C_ta=(1+beta)^2+beta^2/s, dn_lb=(1-p^2/(4s))/2, requires
       p^2<4s (underdamped) and s<=(1-q)^2; then all stages >= t are N.
"""
import sys, math, json
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from fractions import Fraction as Fr
from engine import Inst, complete_graph

def frdot(u, v):
    return sum(a * b for a, b in zip(u, v))

def run_kn(name, n, seed, q, rho, T, alpha=None):
    I = Inst(complete_graph(n), seed, q, rho, alpha=alpha)
    al, kap, be, mu, qq = I.alpha, I.kappa, I.beta, I.mu, I.q
    lam_h = al + (1 - al) * Fr(n, 2 * (n - 1))
    m0 = kap / (kap + al)
    mh = kap / (kap + lam_h)
    p, s = mh * (1 + be), mh * be
    aq = (1 - qq) / qq
    # structural rational preconditions of L-G
    underd = p * p < 4 * s
    slow = s <= (1 - qq) ** 2
    assert m0 == 1 - qq * qq
    # full-support optimum?
    fullsupp = all(v > 0 for v in I.xstar)
    # ct == Qt x*: interior optimum identity
    ctok = all(I.ct[i] == sum(I.Qt[i][j] * I.xstar[j] for j in range(n))
               for i in range(n)) if fullsupp else False
    recs = I.run(T, bankA=None, collect=True)
    # rebuild exact states by replay (engine does not store x_t; rerun states)
    xs = [[Fr(0)] * n, [Fr(0)] * n]
    xm, x = xs[0][:], xs[1][:]
    for t in range(T):
        dh = [x[i] - xm[i] for i in range(n)]
        ah = [x[i] + be * dh[i] for i in range(n)]
        supp_a = [i for i in range(n) if ah[i] > 0]
        Delta = Fr(0)
        for i in supp_a:
            zt = I.ct[i] - sum(I.Qt[i][j] * ah[j] for j in supp_a)
            if zt < 0:
                Delta = max(Delta, -zt / (al * I.d[i]))
        rh = [min(be * dh[i], Delta) for i in range(n)]
        ellh = [ah[i] - rh[i] for i in range(n)]
        xn = I.obstacle_solve(I.ct, kap, ellh, warm=supp_a or None)
        xm, x = x, xn
        xs.append(x[:])
    # xs[t+1] = x_t  (xs[0]=x_{-1}, xs[1]=x_0)
    E = [[I.xstar[i] - xs[k][i] for i in range(n)] for k in range(len(xs))]
    # face lock: first t with x_{t-1}>0 and x_t>0
    tF = None
    for t in range(1, T):
        if all(v > 0 for v in xs[t]) and all(v > 0 for v in xs[t + 1]):
            tF = t; break
    res = dict(name=name, n=n, q=str(qq), tF=tF, fullsupp=fullsupp, ct_eq=ctok,
               underdamped=bool(underd), s_le=bool(slow), checks={}, fails=[])
    ck = res['checks']
    for k in ('C1_master', 'C2_Fcollapse', 'C3_Nlinear', 'C4_Vdecay',
              'C5_oscil', 'C6_trigger', 'C7_defect', 'C8_philb'):
        ck[k] = [0, 0]   # [passed, tested]
    C_ta = (1 + be) ** 2 + be * be / s
    dn_lb = (1 - p * p / (4 * s)) / 2
    wh2 = (al * be / lam_h) ** 2
    tabs = None
    word = ''.join(r['cls'] for r in recs)
    for t in range(tF if tF is not None else T, T - 1):
        em, e, en = E[t], E[t + 1], E[t + 2]     # e_{t-1}, e_t, e_{t+1}
        Lm, L = frdot(em, [Fr(1)] * n) / n, frdot(e, [Fr(1)] * n) / n
        Ln = frdot(en, [Fr(1)] * n) / n
        hm = [em[i] - Lm for i in range(n)]
        h = [e[i] - L for i in range(n)]
        hn = [en[i] - Ln for i in range(n)]
        d = [em[i] - e[i] for i in range(n)]
        ta = [(1 + be) * e[i] - be * em[i] for i in range(n)]
        taL = frdot(ta, [Fr(1)] * n) / n
        tah = [ta[i] - taL for i in range(n)]
        rec = recs[t]
        Delta, cls = rec['Delta'], rec['cls']
        r = [min(be * d[i], Delta) for i in range(n)]
        ell = [xs[t + 1][i] + be * d[i] - r[i] for i in range(n)]
        def tick(key, ok, msg=''):
            ck[key][1] += 1
            if ok: ck[key][0] += 1
            else: res['fails'].append((t, key, msg))
        # C1 master: (Qt + kap D) e_{t+1} = kap D (x*-ell)
        lhs = [sum(I.Qt[i][j] * en[j] for j in range(n)) +
               kap * I.d[i] * en[i] for i in range(n)]
        rhs = [kap * I.d[i] * (I.xstar[i] - ell[i]) for i in range(n)]
        tick('C1_master', lhs == rhs)
        if cls == 'F':
            okF = (ell == xs[t + 1]) and \
                all((kap + lam_h) * hn[i] == kap * h[i] for i in range(n)) \
                and (kap + al) * Ln == kap * L
            tick('C2_Fcollapse', okF)
        if cls == 'N':
            ok3 = all(v == 0 for v in r) and \
                all((kap + lam_h) * hn[i] ==
                    kap * ((1 + be) * h[i] - be * hm[i]) for i in range(n)) \
                and (kap + al) * Ln == kap * ((1 + be) * L - be * Lm)
            tick('C3_Nlinear', ok3)
            V = frdot(h, h) - p * frdot(h, hm) + s * frdot(hm, hm)
            Vn = frdot(hn, hn) - p * frdot(hn, h) + s * frdot(h, h)
            tick('C4_Vdecay', Vn == s * V)
        rL = frdot(r, [Fr(1)] * n) / n
        rh_ = [r[i] - rL for i in range(n)]
        dL = frdot(d, [Fr(1)] * n) / n
        dh_ = [d[i] - dL for i in range(n)]
        tick('C5_oscil', frdot(rh_, rh_) <= be * be * frdot(dh_, dh_))
        modal = [al * taL + lam_h * tah[i] for i in range(n)]
        Dmodal = max(max((-v for v in modal), default=Fr(0)), Fr(0)) / al
        okT = (Dmodal == Delta) and (Delta == 0 or min(modal) < 0)
        tick('C6_trigger', okT)
        e2m = sum(I.d[i] * em[i] * em[i] for i in range(n))
        e2 = sum(I.d[i] * e[i] * e[i] for i in range(n))
        tick('C7_defect', rec['Dfin'] <= aq * (e2m - e2))
        tick('C8_philb', 2 * rec['Phi'] >= mu * e2)
        # absorption certificate L-G at stage t
        V = frdot(h, h) - p * frdot(h, hm) + s * frdot(hm, hm)
        if tabs is None and underd and slow and \
           L >= (1 - qq) * Lm and C_ta * V <= dn_lb * wh2 * Lm * Lm:
            tabs = t
    res['t_abs'] = tabs
    res['word'] = word
    if tabs is not None:
        res['suffix_all_N'] = all(c == 'N' for c in word[tabs:])
        Jpre = 0.0; gams = []
        for t in range(tabs):
            g = recs[t]['gamma']
            if g > 1:
                Jpre += math.log(g); gams.append((t, str(g)))
        res['J_pre_abs'] = Jpre
        res['inflation_stages'] = gams
        res['J_frozen'] = all(recs[t]['gamma'] <= 1 for t in range(tabs, T))
    return res, recs, I

def show(res):
    print("== %s (n=%d, q=%s) ==" % (res['name'], res['n'], res['q']))
    print("  fullsupp=%s ct=Qt.x* %s underdamped(p^2<4s)=%s s<=(1-q)^2=%s"
          % (res['fullsupp'], res['ct_eq'], res['underdamped'], res['s_le']))
    print("  face lock t_F=%s  word=%s" % (res['tF'], res['word'][:24]))
    for k, (a, b) in res['checks'].items():
        print("    %-12s %d/%d %s" % (k, a, b, "OK" if a == b else "FAIL"))
    if res.get('t_abs') is not None:
        print("  ABSORPTION CERT fires at t_abs=%d; suffix all-N: %s; "
              "J frozen: %s" % (res['t_abs'], res['suffix_all_N'],
                                res['J_frozen']))
        print("  J_pre_abs=%.6f  inflation stages: %s" %
              (res['J_pre_abs'],
               [(t, g[:24]) for t, g in res['inflation_stages']]))
    else:
        print("  ABSORPTION CERT did not fire in horizon")
    if res['fails']:
        print("  FAILURES:", res['fails'][:6])

out = {}
# --- K2 killer family (uniform seed, rho=1/16), n=100 exact ---
res, recs, _ = run_kn("K2 n=100", 2, [Fr(1, 2), Fr(1, 2)], Fr(1, 100),
                      Fr(1, 16), 26)
show(res); out['K2'] = {k: v for k, v in res.items() if k != 'fails'}

# --- K8 reachable pulse (q=1/10, alpha=1/101, rho=1/112, published seed) ---
seed = [Fr(363437, 651088)] + [Fr(41093, 651088)] * 7
res, recs, I = run_kn("K8 pulse", 8, seed, Fr(1, 10), Fr(1, 112), 14,
                      alpha=Fr(1, 101))
show(res)
g2, g3 = recs[2]['gamma'], recs[3]['gamma']
print("  exact gamma_2 == 57072309867/51440146040:",
      g2 == Fr(57072309867, 51440146040))
print("  exact gamma_3 == 192036347475007/168765931042095:",
      g3 == Fr(192036347475007, 168765931042095))
out['K8pulse'] = {k: v for k, v in res.items() if k != 'fails'}

# --- K8 small-q family (q=1/100, rho=1/112, dense seed) ---
def vpulse_seed(n, q, cv):
    al = q * q / (1 + q * q)
    lam_h = al + (1 - al) * Fr(n, 2 * (n - 1))
    v = [Fr(1)] + [Fr(-1, n - 1)] * (n - 1)
    s = []
    for i in range(n):
        Qe0 = al + cv * q * q * lam_h * v[i]
        s.append((1 + Qe0 / al) / (2 * n))
    return s

q = Fr(1, 100)
res, recs, _ = run_kn("K8-q q=1/100", 8, vpulse_seed(8, q, 12), q,
                      Fr(1, 112), 14)
show(res); out['K8q'] = {k: v for k, v in res.items() if k != 'fails'}

# --- K16, K32 v-pulse analogues (q=1/50, cv=40) exact ---
q = Fr(1, 50)
res, recs, _ = run_kn("K16 cv=40", 16, vpulse_seed(16, q, 40), q,
                      Fr(1, 2 * 16 * 15), 12)
show(res); out['K16'] = {k: v for k, v in res.items() if k != 'fails'}
res, recs, _ = run_kn("K32 cv=40", 32, vpulse_seed(32, q, 40), q,
                      Fr(1, 2 * 32 * 31), 12)
show(res); out['K32'] = {k: v for k, v in res.items() if k != 'fails'}

json.dump(out, open('/home/claude/work/overnight/w7_windowed/knproof_results.json', 'w'),
          indent=1, default=str)
print("\nsaved knproof_results.json")
