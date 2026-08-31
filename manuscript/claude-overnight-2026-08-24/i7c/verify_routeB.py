"""I7-C: single end-to-end Route-B verification driver.

Re-runs, in one process, the exact evidence base of the Route-B theorem
document (findings/i7c_routeB_theorem.md):

  PART 1  fm-w certified battery, all 19 cells at the i7a horizons
          (rt22b at T=400).  Exact per-stage predicates NF / YPOS / CMP /
          KKT / UID (the composed chain P-A..P-E), inertia-gate census
          (S16 lock face must be REJECTED with n_od=2), float-Measured
          entrance certificate (R<=1, sharp<=1, L-floor, R-decay).
  PART 2  the rt22b counterexample: unmodified fm fires at t=13 (exact
          rationals; negative zeta coordinates re-derived from the recorded
          trial a_13); fire census over T=120 for the packing discussion;
          K8ctl negative control (fm fires); re-tune reconciliation check:
          along every fm run q_r is monotone NONINCREASING and beta monotone
          NONDECREASING (i5c's "downward" = q_r down = beta up = i7a's
          "upward beta re-tune" -- same event, two variable names).
  PART 3  K_n absorption spot grid: n in {2,8,32} x q in {1/10,1/400} x
          seeds {skew, vpulse} at edge rho, + the published K8 pulse
          (the one genuinely partial stage).  All 18 predicates of
          i6b_knproof3 (incl. repaired C17'/C9s), absorption fires,
          J_total < log 2.
  PART 4  class boundary instances (the audit anchors): Q3-eq q=1/3,
          C6-eq q=1/4, Pet-eq q=1/3 (skew seeds).  Master-form identity
          C9M_id, C9M_neg (Psi<=0), and the adversarial-h form C9F,
          exact rationals, at every stage.

Verdict gates on the EXACT predicates only; float certificate values are
reported as Measured.  Everything else exactly as in the source scripts
i7a_fmw.py / i5c_core.py / i6b_knproof3.py / i7b_class4.py.
"""
import sys, json, time, math
from pathlib import Path

HERE = Path(__file__).resolve().parent
CAMPAIGN_ROOT = HERE.parent
sys.path.insert(0, str(CAMPAIGN_ROOT / 'w7_windowed'))
from fractions import Fraction as Fr

OUT = {}
FAILURES = []
t00 = time.time()


def hdr(s):
    print('\n' + '=' * 72 + '\n' + s + '\n' + '=' * 72, flush=True)


# ======================================================================
hdr('PART 1: fm-w certified battery (19 cells, exact chain P-A..P-E)')
from i7a_fmw import ALL, run_fmw
from engine import Inst

HORIZONS = {'K8ctl': 30, 'P12': 200, 'P16': 250, 'P18': 200, 'P20': 250,
            'P24': 250, 'P24rho2': 250, 'P24rho3': 250, 'P30lr': 200,
            'S16': 100, 'bt15': 200, 'bt31': 140, 'cat4_3': 200,
            'cat5_2': 200, 'cat6_2': 160, 'rt16b': 200, 'rt18': 200,
            'rt20a': 160, 'rt22b': 400}
EXACT_KEYS = ('NF', 'YPOS', 'CMP', 'KKT', 'UID', 'MOM', 'PROX')
FLOAT_KEYS = ('RLE1', 'SHARP1', 'LFLOOR')
agg = {k: [0, 0] for k in EXACT_KEYS + FLOAT_KEYS}
rdec_ok = rdec_n = 0
mom_entrances = []
s16_gate = None
cells_out = {}
for name in sorted(HORIZONS):
    adj, seed, q, rho, _T = ALL[name]
    T = HORIZONS[name]
    I = Inst(adj, seed, q, rho)
    o = run_fmw(I, T)
    cells_out[name] = o
    for k in EXACT_KEYS + FLOAT_KEYS:
        a, b = o['checks'][k]
        agg[k][0] += int(a)
        agg[k][1] += int(b)
        if k in EXACT_KEYS and int(a) != int(b):
            FAILURES.append(('P1-' + k, name, o['fails'][:4]))
    rdec_ok += sum(o['rdecay_ok'])
    rdec_n += o['rdecay_n']
    mom_entrances += [dict(cell=name, **m) for m in o['momstarts']]
    if name == 'S16':
        s16_gate = o['gates']
    print('  %-8s T=%-3d NF=%s MOM=%s PROX=%s entr=%d gateJ=%s  [%ss]' %
          (name, T, o['checks']['NF'], o['checks']['MOM'],
           o['checks']['PROX'], len(o['momstarts']),
           {g['size']: (g['J'] if g['gate'] else g['why'])
            for g in o['gates'].values()}, o['secs']), flush=True)
print('\n  aggregate over 19 cells:')
for k in EXACT_KEYS:
    a, b = agg[k]
    print('    %-6s %5d/%-5d exact   %s' % (k, a, b,
                                            'PASS' if a == b else 'FAIL'))
for k in FLOAT_KEYS:
    a, b = agg[k]
    print('    %-6s %5d/%-5d float (Measured)' % (k, a, b))
print('    R-decay pairs ok (float, tol 1e-9): %d/%d' % (rdec_ok, rdec_n))
worstR = max((m['R'] for m in mom_entrances), default=None)
print('    momentum entrances: %d, worst entrance R = %s' %
      (len(mom_entrances), worstR))
s16_rej = any((not g['gate']) and str(g.get('why', '')).startswith('n_od=2')
              for g in (s16_gate or {}).values())
print('    S16 all-overdamped lock face rejected by gate (n_od=2): %s'
      % s16_rej)
if not s16_rej:
    FAILURES.append(('P1-GATE', 'S16', s16_gate))
if not (worstR is None or worstR <= 1):
    FAILURES.append(('P1-RLE1', 'entrance R>1', worstR))
OUT['part1'] = dict(agg={k: tuple(v) for k, v in agg.items()},
                    rdecay=(rdec_ok, rdec_n), entrances=mom_entrances,
                    s16_gate_rejected=s16_rej)

# ======================================================================
hdr('PART 2: the rt22b counterexample (unmodified fm) + re-tune direction')
from i5c_core import run_i5c

adj, seed, q, rho, _ = ALL['rt22b']
I = Inst(adj, seed, q, rho)
recs = run_i5c(I, 120, 'fm', stop_on_unsafe=False)
fires = [(r['t'], r['cls'], float(r['Delta'])) for r in recs if r['Delta'] > 0]
print('  rt22b (n=22, q=1/28, rho=1/96, interior |S*|=%d): %d fires in T=120'
      % (len(I.Sstar), len(fires)))
for t, c, dl in fires:
    print('    fire t=%-3d class=%s Delta=%.6e' % (t, c, dl))
r13 = recs[13]
neg = []
for i in r13['S']:
    z = I.ct[i] - sum(I.Qt[i][j] * r13['ah'][j] for j in r13['S'])
    if z < 0:
        neg.append((i, float(z)))
print('  stage 13: class=%s Delta=%s  negative zeta coords: %s' %
      (r13['cls'], float(r13['Delta']), neg))
ok_ce = (len(fires) >= 1 and fires[0][0] == 13 and r13['cls'] == 'F'
         and len(neg) >= 1)
print('  counterexample reproduced (first fire at t=13, class F): %s' % ok_ce)
if not ok_ce:
    FAILURES.append(('P2-CE', 'rt22b', fires[:3]))
# retraction mass after the fires (packing discussion; Measured)
retr = sum(float(sum(Fr(v) for v in r['rh'])) for r in recs if r['rnz'])
print('  total retraction mass sum_t 1^T r_t = %.3e ; last fire t=%s ; '
      'stages 14..119 fire-free: %s' %
      (retr, fires[-1][0] if fires else None,
       all(r['Delta'] == 0 for r in recs[14:])))
# re-tune direction ALONG THE FACE CHAIN (first nonempty face onward).
# Stage 0 has S = {} and reports the global (q, beta) by code convention;
# the move global -> first face is the i5c SS5 one-time initialization jump,
# not a face re-tune, and is reported separately.
chain = []
for r in recs:
    if not r['S']:
        continue
    if not chain or (r['qr'], r['beta']) != chain[-1][1]:
        chain.append((r['t'], (r['qr'], r['beta'])))
mono_qr = all(a[1][0] >= b[1][0] for a, b in zip(chain, chain[1:]))
mono_be = all(a[1][1] <= b[1][1] for a, b in zip(chain, chain[1:]))
print('  initialization (empty face, global calib) -> first face: '
      '(q_r,beta) (%s,%s) -> (%s,%s) at t=%d   [the i5c one-time jump]' %
      (recs[0]['qr'], recs[0]['beta'], chain[0][1][0], chain[0][1][1],
       chain[0][0]))
print('  face-chain re-tunes (%d): q_r nonincreasing=%s, '
      'beta nondecreasing=%s' % (len(chain) - 1, mono_qr, mono_be))
print('  lock re-tune: (q_r,beta) %s -> %s at t=%d '
      '[= "downward" in q_r (i5c) = "upward" in beta (i7a)]' %
      (tuple(map(str, chain[-2][1])), tuple(map(str, chain[-1][1])),
       chain[-1][0]))
if not (mono_qr and mono_be):
    FAILURES.append(('P2-RETUNE', 'rt22b', chain))
# K8ctl negative control: unmodified fm fires there too
adjK, seedK, qK, rhoK, TK = ALL['K8ctl']
recK = run_i5c(Inst(adjK, seedK, qK, rhoK), 16, 'fm', stop_on_unsafe=False)
firesK = [r['t'] for r in recK if r['Delta'] > 0]
print('  K8ctl control: unmodified fm fires at t=%s (fm-w above: NF 30/30)'
      % firesK[:6])
if not firesK:
    FAILURES.append(('P2-K8CTL', 'expected fires, saw none', None))
OUT['part2'] = dict(fires=fires, neg13=neg, retn=retr,
                    retunes=len(chain) - 1, mono=(mono_qr, mono_be),
                    k8ctl_fires=firesK)

# ======================================================================
hdr('PART 3: K_n absorption spot grid (n in {2,8,32} x q in {1/10,1/400})')
from i6b_knproof3 import analyze, seeds_for, KEYS as KNKEYS

aggK = {k: [0, 0] for k in KNKEYS}
Ts = {Fr(1, 10): 26, Fr(1, 400): 90}
rows = []
for n in (2, 8, 32):
    for qv in (Fr(1, 10), Fr(1, 400)):
        sd = seeds_for(n, qv)
        for sn in ('skew', 'vpulse'):
            if sn not in sd:
                continue
            seed = sd[sn]
            rho = Fr(9, 10) * min(seed) / (n - 1)  # edge regime
            nm = 'K%d q=1/%d %s/edge' % (n, int(1 / qv), sn)
            res, _, _ = analyze(nm, n, seed, qv, rho, Ts[qv])
            rows.append(res)
res, _, _ = analyze('K8 pulse (published)', 8,
                    [Fr(363437, 651088)] + [Fr(41093, 651088)] * 7,
                    Fr(1, 10), Fr(1, 112), 20, alpha=Fr(1, 101))
rows.append(res)
for r in rows:
    for k in KNKEYS:
        aggK[k][0] += r['checks'][k][0]
        aggK[k][1] += r['checks'][k][1]
    print('  %-26s t_abs=%-3s J_total=%.5f word=%s%s' %
          (r['name'], r.get('t_abs'), r.get('J_total', 0),
           r.get('word', '')[:24],
           '  Pcert=%.3f' % r['Pcert_ratio'][0] if r.get('Pcert_ratio')
           else ''))
    if r['fails']:
        FAILURES.append(('P3', r['name'], r['fails'][:3]))
print('\n  aggregate (%d instances):' % len(rows))
for k in KNKEYS:
    a, b = aggK[k]
    if b:
        print('    %-14s %4d/%-4d %s' % (k, a, b,
                                         'PASS' if a == b else 'FAIL'))
maxJ = max(r.get('J_total', 0) for r in rows)
allabs = all(r.get('t_abs') is not None for r in rows)
print('    absorption fired in all: %s ; max J_total = %.5f < log2 = %.5f: %s'
      % (allabs, maxJ, math.log(2), maxJ < math.log(2)))
if not allabs or maxJ >= math.log(2):
    FAILURES.append(('P3-ABS', 'absorption/J', (allabs, maxJ)))
OUT['part3'] = dict(agg={k: tuple(v) for k, v in aggK.items()},
                    maxJ=maxJ, all_absorbed=allabs)

# ======================================================================
hdr('PART 4: class boundary instances -- master form Psi (exact rationals)')
from i6b_class3 import hypercube, cycle, petersen, seeds_for as cseeds
from i7b_class4 import run_case

CLS = [('Q3-eq  q=1/3 (mu2=2q)', hypercube(3), Fr(1, 3), Fr(2, 3)),
       ('C6-eq  q=1/4 (mu2=2q)', cycle(6), Fr(1, 4), Fr(1, 2)),
       ('Pet-eq q=1/3 (mu2=2q)', petersen(), Fr(1, 3), Fr(2, 3))]
aggC = {k: [0, 0] for k in ('C9M_id', 'C9M_neg', 'C9F')}
for nm, adj, qv, mu2 in CLS:
    n = len(adj)
    dmax = max(len(a) for a in adj)
    s, rho = cseeds(n, dmax, 'skew')
    r = run_case(nm, adj, s, qv, rho, 18, mu2)
    if r is None:
        FAILURES.append(('P4', nm, 'skipped (not interior/H0)'))
        print('  %-24s SKIPPED' % nm)
        continue
    for k in aggC:
        aggC[k][0] += r['cnt'][k][0]
        aggC[k][1] += r['cnt'][k][1]
        if r['cnt'][k][0] != r['cnt'][k][1]:
            FAILURES.append(('P4-' + k, nm, r['cnt'][k]))
    print('  %-24s in_class=%s word=%s  %s' %
          (nm, r['in_class'], r['word'],
           {k: tuple(r['cnt'][k]) for k in aggC}))
print('\n  aggregate:')
for k in aggC:
    a, b = aggC[k]
    print('    %-8s %3d/%-3d exact %s' % (k, a, b,
                                          'PASS' if a == b else 'FAIL'))
OUT['part4'] = {k: tuple(v) for k, v in aggC.items()}

# ======================================================================
hdr('VERDICT')
OUT['failures'] = FAILURES
OUT['secs'] = round(time.time() - t00, 1)
if FAILURES:
    print('  FAIL — %d gated check groups failed:' % len(FAILURES))
    for f in FAILURES[:10]:
        print('   ', f)
else:
    print('  ALL GATED (EXACT) CHECKS PASS.')
    print('  fm-w: NF %d/%d; P-A CMP %d/%d; P-B YPOS %d/%d; KKT %d/%d; '
          'UID %d/%d' % (tuple(agg['NF']) + tuple(agg['CMP'])
                         + tuple(agg['YPOS']) + tuple(agg['KKT'])
                         + tuple(agg['UID'])))
    print('  counterexample rt22b: first fire t=13 class F (unmodified fm); '
          'fm-w on same cell: NF 400/400.')
    print('  K_n spot: all predicates pass, absorption %s, max J_total '
          '%.5f < log 2.' % (allabs, maxJ))
    print('  class boundary (Q3/C6/Petersen at mu2=2q): C9M_id %d/%d, '
          'C9M_neg %d/%d, C9F %d/%d.'
          % (tuple(aggC['C9M_id']) + tuple(aggC['C9M_neg'])
             + tuple(aggC['C9F'])))
print('  total %.1fs' % OUT['secs'])
output_path = HERE / 'verify_routeB.json'
with output_path.open('w') as output_file:
    json.dump(OUT, output_file, indent=1, default=str)
print('  saved i7c/verify_routeB.json')
