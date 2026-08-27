# I7-C — The Route-B theorem document: packing for the actual finite recurrence

**Campaign iteration 7, direction I7-C. Assembly and verification only — no new
research claims beyond the cited components.** This document composes the
campaign's Route-B results (I2-C, I4-A, I5-C, I6-A1, I6-A2, I6-B, I7-A, I7-B)
into one auditable statement, in the repository's vocabulary
(`notes/_shared/problem_definition/README.md`,
`tex/shared/source_aligned_problem.tex`), against the repository's Route-B
target: for the safeguarded AESP-CD recurrence actually implemented, the
actual-finite net exponent

```
J_T^fin <= (1 - c) q T + B,        q = sqrt(alpha/(1-alpha)),
```

with `c` bounded away from 0 and `B` bounded — the "windowed / spectrally
split low-Dirichlet Lyapunov" item on the `aesp_cd_l1_rppr` Route-B queue.

Status vocabulary. Campaign labels are used throughout: **Proved-draft** =
complete proof text plus exhaustive exact-rational machine verification on
every tested instance, written by the campaign and **not yet independently
audited**; on the repository's ladder (Source / Proved / Conditional /
Measured / Open / Refuted) every Proved-draft item should enter as
*Conditional (pending audit)*, never directly as Proved. **Measured** = exact
or float computation, no proof. **Refuted** = exact counterexample.
**Open** = neither. All arithmetic backing exact counts is `fractions.Fraction`
end-to-end unless a row is explicitly labelled float.

---

## 1. Executive statement

The Route-B packing target is now established, campaign-grade, in three
nested senses. Everything below is stated for the RPPR working surrogate
(`F_rho`, obstacle/prox form, exact inner solves) and its **inflation
ledger** — the `eps_pg`-side bookkeeping of the safeguarded recurrence. No
`eps_ppr` output-semantics claim is made anywhere in this document (§5.4,
item 6 of the acceptance checklist).

**(i) On `K_n`, for the ORIGINAL recurrence, unconditionally.** For every
`n >= 2`, every seed with `s_i > rho d_i` (H0), every
`q = sqrt(alpha/(1-alpha)) <= 1/2`: corrections stop at a finite,
a-priori-bounded stage `t_abs <= 12` on the whole 140-instance grid, and

```
J_T^fin <= B <= 0.36918 < log 2       for all T,   i.e.  c = 1.
```

**No open links remain**: the last one (C9 at genuinely partial stages) was
closed by the clip identity + truncation-covariance lemma (I6-B), which also
showed the previously published partial-stage bound was structurally wrong
(fails 47/53 on a purpose-built battery) and replaced it with a margin law
`<= max(theta_F, mh/m0) < 1`. Status: **Proved-draft**, verified exactly on
140 instances (7,130 stage checks per universal predicate), 18/18 predicates.

**(ii) On the class (H0) + (Hgap) + (PSI), with `c = 1` (Theorem B'').** For
connected `G`, `q <= 1/2`, interior seeds (H0), spectral gap
`mu_2(L_sym) >= 2q` (Hgap), and the stage-free variational condition **(PSI)**
`sup_{y,h} Psi_{G,q} <= 0` (the master form: the exact identity
`V_{t+1} - (1-q)^2 V_t = Psi(y_t, h_t)` holds at every stage), absorption
fires and `J_T^fin <= B` with `c = 1`. Coverage of (PSI): all `K_n`
(subsumed); the entire (H-K) kernel subclass (`K_{a,b}`, cocktail, rook,
`Q_3`, several circulants, Kneser(6,2), Paley 13/17, T(5)); **exact rational
instance proofs** on `(C6,1/10)`, `(C6,1/4 = boundary)`, `(C8,1/8)`,
`(Q3,1/3 = boundary)`, `(Petersen,1/3 = boundary)` — sharp with equality
`sup Psi = 0` exactly at `mu_2 = 2q`, attained at mixed one-up/set-down
patterns; complete float decisions (every sign pattern / Aut-orbit pair,
incl. all `3^16` assignments on `Q_4`); zero violations in a 20-family
adversarial sweep. Status: **Proved-draft modulo (PSI)**; analytic (PSI) for
all in-class `(G,q)` simultaneously is the single Open residue.

**(iii) For the MODIFIED algorithm `fm-w`, on every tested instance class,
`J_T^fin = 0` exactly.** The variant — face-aligned retraction cap +
upper-CW face-calibrated momentum + `J_S` pure-prox warmup stages after each
face change + exact-rational inertia gate — has a composed never-triggering
theorem: with exact solves, **`Delta_t = 0` at every stage of every run**
(3,840/3,840 stages over 19 cells including five fresh adversarial
short-segment cells), so every stage is N, `gamma_t = 1`, and
`J_T^fin = 0` **exactly**, with `c = 1` and `B` = the single measured
initialization re-tune jump. No restriction on `alpha` beyond
`kappa = 1 - 2 alpha > 0`; no (H-sep) assumption (it became a checked gate);
proper and interior faces alike. The modification is **legal** (the safety
theorem holds for any certified cap direction `w > 0` with `Qt_S w > 0`, and
is stage-local in `beta_t >= 0` — 68,800/68,800 safety-flag checks),
**implementable** entirely in exact rational arithmetic (certified CW
brackets, exact inertia bisection; no eigensolver, no floats in any
load-bearing predicate), and **provably necessary**: the unmodified variant's
never-triggering claim is **Refuted** by the exact counterexample `rt22b`
(random tree, `n = 22`), which fires at `t = 13`, three stages after face
lock — so any unmodified statement must carry an entrance condition.
Status: **Proved-draft** (theorem + verification); **Refuted** (unmodified
claim, exact witness).

Precision note carried through this document: rt22b refutes
**never-triggering** of the unmodified variant, **not** the packing bound
itself. On rt22b the unmodified variant's fires *cease* (measured: the single
fire at `t = 13` in `T = 120`; stages 14..119 fire-free — §5.2), so
`J_T^fin` is a one-event constant on that instance and packing with `c = 1`
is not contradicted; its exact ledger value under the i2c `gamma`
accounting has not been computed (Open as a number, bounded as a mechanism).

---

## 2. The algorithm `fm-w`

One safeguarded obstacle stage, exact arithmetic, per-face cached
certificates. `Qt = D^{1/2} Q D^{1/2}` (hat coordinates), `kappa = 1-2alpha`,
`ct = alpha(s - rho d)` scaled to hat units, `x_{-1} = x_0 = 0`.

```
state:  x_{t-1}, x_t;  per-face caches w(S), (q_r(S), beta(S)), gate(S), J_S
stage t:
  d_t  = x_t - x_{t-1};             S_t = supp(x_t) ∪ supp(d_t)
  # ---- certified face constants (computed once per distinct face) ----
  w(S) = w^(8):  8 exact inverse-iteration steps  w <- normalize(Qt_S^{-1} D_S w),
         rounded to bounded denominator, Qt_S w > 0 re-verified exactly
         [safety needs only w > 0, Qt_S w > 0 — any such w is legal]
  CW bracket:  lo = min_i (Qt_S w)_i/(d_i w_i)  <=  alpha_S  <=  hi = max_i (...)
  q_r  = smallest k/M (M = 1000) with (k/M)^2 >= hi/(1-hi);  q_r <- q if hi <= alpha
  beta(S) = (1-q_r)/(1+q_r)         [= 0 if q_r = 1]
  GATE(S), per connected component C of S (exact rational):
         crit = kappa q_r^2/(1-q_r^2)
         require  inertia(Qt_C - crit D_C) = exactly one mode <= crit     (H-sep, checked)
         and a strict bracket lam_2 > th_lo > crit from ~12 exact inertia bisections
         fail  =>  face runs prox-only forever (beta = 0): unconditionally safe (T5)
  J_S (per component, max):  m2+ = kappa/(kappa+th_lo),  mu+ = m2+/(1-q_r^2) < 1,
         m_psi = min_i psi_i/sqrt(d_i),  A_S = ||psi||_*^2/m_psi   (psi = Perron dir,
             implemented via the exact w^(8) proxy; certified entrywise Perron
             brackets are the one engineering residue — they enter only in a log),
         dn-_S = 1 - (1+beta) sqrt(m2+)/(2 sqrt(beta)) > 0,
         C_S = (1+beta)^2 + beta(kappa+1)/kappa,
         R0  = C_S A_S^2 / (4 dn-_S m_psi^2 beta),
         J_S = 1 + ceil( log R0 / (2 log(1/mu+)) )
  # ---- momentum schedule (the modification) ----
  beta_t = beta(S_t)  if stable_t >= J_S and GATE(S_t) passes,  else 0
           (stable_t = # consecutive completed solves with S unchanged)
  # ---- trial, safeguard, solve (unchanged from fm / the i2c recurrence) ----
  a_t  = x_t + beta_t d_t
  zeta(a_t)_i = ct_i - (Qt a_t)_i            on S = supp(a_t)
  Delta_t = max(0, max_i [-zeta(a_t)_i]_+ / (Qt_S w)_i)       (face cap denominator)
  r_t  = min(beta_t d_t, Delta_t * w)  componentwise;   ell_t = a_t - r_t
  x_{t+1} = ObstacleSolve(Qt + kappa D, ct + kappa D ell_t, x >= 0)   (exact LCP)
```

**Theorem S (safety — legality of every ingredient).** [I4-A §1 recovered,
audited, completed; I5-C §3] For any `w > 0` on `S = supp(a_t)` with
`Qt_S w > 0` componentwise (both established constructively and re-verified
exactly for the rounded `w^(8)`), and any stage-varying `beta_t >= 0`, under
(H-mono) `d_t >= 0`, `0 <= x_t <= x*` and (H-Mmat) `kappa >= 0`:
`x_t <= ell_t <= x*`, hence `x_t <= x_{t+1} <= x*`. Safety is **stage-local
in `beta`** (the theorem's two uses of `beta_t` are structural, never
coupling `beta_t` to `beta_{t-1}`), which is what makes per-face
recalibration and the warmup schedule legal. Rational approximations to the
Perron direction are legal: `(H-pos)` is re-verified exactly after rounding,
with fallback to the unrounded vector. Status: Proved-draft;
68,800/68,800 exact safety-flag checks (8 flags x 8,600 stages, 24 runs)
plus 23,100/23,100 in the i4a battery.

Cost of the modification (honest): I5-C §8 measured `fm` 25–60% slower than
the `alpha`-calibrated baseline to fixed accuracy on every cell (exact
crossing times), winning only asymptotically (`z_+ = 0.9619 < 0.9682` on
P24, crossover beyond `T = 4800`); `fm-w`-cert additionally spends
`sum_S J_S` warmup prox stages, and the certified `J_S` is large on
near-critical faces (paths 86–900, so the path family ran prox-only within
battery horizons — still zero fires, but convergence there matched prox).
The purchased good is *regularity*: zero corrections, zero inflation,
`J_T^fin = 0` exactly.

---

## 3. The theorem chain

Numbered statements with hypotheses, status, verification count, and where
the proof lives. "Battery" = the 19-cell fm-w battery (3,840 cert stages)
unless stated. File paths are relative to the campaign root
`manuscript/claude-overnight-2026-08-24/`.

**T0 (Safety; legality).** As Theorem S above. *Hypotheses:* (H-mono),
(H-Mmat), (H-pos). *Status:* Proved-draft. *Proof:* `findings/i4a_face_and_class.md`
§1 (four-gap audit table) + `findings/i5c_face_momentum.md` §3
(stage-locality in beta); code `w7_windowed/i3g_core.py` (docstring proof +
`face_w_exact`).

**T1 (Trigger predicate — cap-free subsolution form).** With `dv_i > 0`,
`Delta_t = 0 <=> zeta(a_t)_i >= 0` for all `i in supp(a_t)`: the trial is a
subsolution on its own support. Cap direction and trigger denominator scale
the *size* of a positive `Delta_t`, never its vanishing — never-triggering is
cap-free, and the `x*`-based "trial error >= 0" formulation is a consequence,
not the mechanism. *Status:* Proved-draft. *Verification:* T0 2,041/2,041
(i6a2); `pos_den` at every battery stage. *Proof:*
`findings/i6a1_never_trigger_induction.md` §1;
`findings/i6a2_never_trigger_spectral.md` §1.

**T2 (Residual identity).** `Y_t := ct - Qt x_t`; then
`zeta(a_t) = (1+beta_t) Y_t - beta_t Y_{t-1}` exactly, so never-fire at `t`
`<=> Y_t >= [(1-q_r)/2] Y_{t-1}` componentwise on `S_t`. *Status:*
Proved-draft (affine algebra). *Verification:* UID 3,821/3,821 (battery),
2,041/2,041 (i6a2). *Proof:* `findings/i6a2_never_trigger_spectral.md` §1.

**T3 (Increment reduction (T-gen')).** If stage `t` never fired, then on
`S_{t+1}`: `zeta(a_{t+1}) = kappa D (d_{t+1} - beta_t d_t) -
beta_{t+1} Qt d_{t+1}` — `x*` and `ct` cancel; the trigger lives in
increment space; valid across face changes. On a fixed face this closes to
the three-term form (T) and the exact 2-cycle self-similarity (R5): the
trigger sequence solves the driving recurrence itself. *Status:*
Proved-draft. *Verification:* R2 2,803/2,803 consecutive-stage identities
(worst never-fire margins `+1e-12..+1e-27` — any proof must be exact);
(T) 2,509/2,509. *Proof:* `findings/i6a1_never_trigger_induction.md` §2
(R1–R5); code `w7_windowed/i6a1_checks.py`.

**T4 (P-A: LCP subsolution comparison — the new lemma).** Let
`A = Qt + kappa D` (strictly diagonally dominant Z-matrix, hence M-matrix)
and let `x` solve the LCP `x >= 0, Ax - r >= 0, x^T(Ax - r) = 0`. If
`v >= 0` satisfies `(Av - r)_i <= 0` wherever `v_i > 0`, then `x >= v`.
Applied with `v = a_t`: **never-fire at `t` implies
`x_{t+1} >= a_t >= x_t`** — the monotone invariant is self-sustained along
the induction rather than imported. *Status:* Proved-draft (complete
5-line proof: index set `E = {v_i > x_i}`, sign bookkeeping,
`A_{EE}^{-1} >= 0`). *Verification:* CMP 3,840/3,840, plus its predicted
failure at the one fired J2-control stage. *Proof:*
`findings/i7a_never_trigger_complete.md` §2 P-A.

**T5 (P-B: prox stages never fire — unconditional).** If stage `t` never
fired then `Y_{t+1} = kappa D (x_{t+1} - a_t) >= 0` on `supp(x_{t+1})` (KKT
+ T4); a `beta = 0` stage has trigger vector `zeta = Y >= 0` on its support:
it cannot fire. Covers `t <= 1` (eliminating the `alpha <= 1/5` base-case
restriction of I6-A2), every face-change stage, every warmup stage, entering
coordinates (subsuming the activation lemma), and prox-only gated faces.
*Status:* Proved-draft. *Verification:* YPOS 3,821/3,821; NF at prox stages
3,269/3,269. *Proof:* `findings/i7a_never_trigger_complete.md` §2 P-B.

**T6 (P-C: cone bound).** For any `Y >= 0` supported on `S`, in the
`*`-inner product with Perron direction `psi > 0`: the Perron coefficient
`L` and orthogonal part `h` satisfy `||h||_*/L <= ||psi||_*^2/m_psi = A_S`.
One line (`ell_1 >= ell_2`). *Status:* Proved-draft. *Proof:*
`findings/i7a_never_trigger_complete.md` §2 P-C.

**T7 (Calibration lemmas A–D).** (A) Interlacing: `alpha_S >= alpha`,
strict for proper `S` in connected `G`; nested faces give monotonicity.
(B) Exact identity `(1-q_S^2) - m_S = 2 alpha_S (alpha - alpha_S) /
((1-alpha_S)(kappa+alpha_S))`, hence `m_S >= 1-q_S^2 <=> alpha_S >= alpha`
(sign of I4-A §6(b) corrected). (C) Certified rational overdamping: the
**upper** CW end `hi >= alpha_S` with `q_r^2 >= hi/(1-hi)` gives
`m_S >= kappa/(kappa+hi) >= 1-q_r^2` — upper-end calibration is the safe
direction; lower-end reproduces the refuted underdamped configuration.
(D) Scalar floor step: `m_S >= 1-q_r^2` and `h_t >= (1-q_r) h_{t-1} > 0`
give `h_{t+1} >= (1-q_r) h_t`. *Status:* Proved-draft. *Verification:*
288/288 strict brackets, 200/200 + 200/200 identity substitutions, 110/110
overdamping certificates, 2,330/2,330 matched floors. *Proof:*
`findings/i5c_face_momentum.md` §2.

**T8 (Modal structure and the gate).** With `beta = (1-q_r)/(1+q_r)`:
`4beta/(1+beta)^2 = 1-q_r^2` exactly; mode `k` of the face recurrence is
overdamped iff `lam_k <= crit = kappa q_r^2/(1-q_r^2)`; generically only the
Perron mode is (78/79 battery faces); `z_+` is strictly increasing in `m`
(the Perron root governs), `z_-` strictly decreasing (which **refutes** the
entrywise factorization bridge `Z_- >= 0` in both spectral regimes); the
load-bearing equivalence `n_od = 1 <=> lam_2 > crit <=> m_2 < 1-q_r^2 <=>
s_2 < (1-q_r)^2` makes (H-sep) an exact-inertia certificate — in `fm-w` a
**checked gate**, not an assumption; its one battery violator (the S16
all-overdamped lock face) is rejected by the gate and runs prox-only
(safe by T5). *Status:* Proved-draft (incl. gate correctness);
factorization bridge Refuted. *Verification:* exact inertia 79/79 faces;
identities 200/200. *Proof:* `findings/i6a2_never_trigger_spectral.md`
§3, §5; gate implementation `w7_windowed/i7a_fmw.py:inertia_le,lam2_lower`.

**T9 (P-D: warmup contraction and the entrance certificate — the gap,
closed).** On a stable face a prox solve maps `Y -> Mm'_S Y`, contracting
the modal ratio by `m_2/m_S <= mu+ := m2+/(1-q_r^2) < 1` per stage (T7
Lemma C + the gate's `m_2 <= m2+`). After the certified `J_S` warmup solves,
at the first momentum stage `t*`:
`R_{t*} <= R0 * mu+^{2(J_S-1)} <= 1` and the L-floor holds — i.e. the
entrance data of the segment satisfies the propagation certificate (i)+(ii)
of T10. Exact structural identity: **`mu+ = s_2/(1-q_r)^2`** (from
`beta(1-q_r^2) = (1-q_r)^2`) — one warmup stage contracts the certificate at
the *square* of the per-stage momentum decay rate: the warmup is the reach
corollary's prefix spent where never-firing is free, at half length.
Nothing needs `x*`, properness, or a global spectral hypothesis; the
degenerate branch `Y|_S = 0` is stationary. *Status:* Proved-draft.
*Verification:* entrance `R <= 1` at 8/8 first momentum stages (float,
largest 0.26; K8 formula audit: predicted 0.80, measured 0.257), sharp form
8/8, L-floor 571/571; negative control: `J = 2` warmup violates the norm
certificate at 183/183 entrances and produces exactly one fire (rt22b,
`t = 34`) from a sharp-violating entrance, while all 176 sharp-certified
entrances launched fire-free segments. *Proof:*
`findings/i7a_never_trigger_complete.md` §2 P-D.

**T10 (P-E: fixed-face propagation).** [= I6-A2 §4 theorem, unchanged.] On a
face satisfying the gate, if at stage `t` (i) `L_t >= (1-q_r) L_{t-1} > 0`
and (ii) `R_t <= 1`, then `Delta_t = 0` and (i),(ii) hold again at `t+1`
with `R_{t+1} <= [s_2/(1-q_r)^2] R_t < R_t`: no stage of the remaining
segment triggers. Reach corollary: a no-correction prefix of explicit length
`K` upgrades itself to a never-triggering tail. Per-component application
licensed by block-diagonality. *Status:* Proved-draft. *Verification:*
571 momentum stages across 8 cells, 0 fires; R-decay at 100% of checkable
pairs (227/227 on rt22b-400) modulo float underflow noise on bt15/bt31.
*Proof:* `findings/i6a2_never_trigger_spectral.md` §4.

**T11 (The composed never-triggering theorem for `fm-w`, and the Route-B
corollary).** For the RPPR obstacle recurrence with exact solves, start
`x_{-1} = x_0 = 0`, face cap, certified calibration, gate and warmup as in
§2: **every stage of every run has `Delta_t = 0`**; every stage is N,
`r_t = 0`, `Dfin_t = 0`, `gamma_t = 1`, and **`J_T^fin = 0` exactly** — the
Route-B packing `J_T^fin <= (1-c) qT + B` holds with `c = 1` and `B` = the
one-time initialization re-tune jump measured in I5-C §5 (0.22–2.81 nats,
an artifact of starting the schedule at `q` rather than the first face's
`q_r`). The i2c/i4a Open links (P), (F) are vacuous on this variant. No
hypothesis on `alpha` beyond `kappa > 0`; disconnected faces per component.
*Proof structure:* induction; prox stages by T5; entrances by T9; segment
tails by T10; monotone invariant self-sustained by T4; gate failures fall
back to T5 forever. *Status:* Proved-draft. *Verification:* NF
3,840/3,840 over 19 cells (incl. K8ctl, the pre-modification firing cell,
and rt22b, the counterexample cell, at `T = 400` with 228 consecutive
momentum stages after a certified `J = 149` warmup — entrance
`R = 1.7e-4`). *Proof:* `findings/i7a_never_trigger_complete.md` §2.

**T12 (Necessity: the unmodified variant is refuted).** Instance `rt22b`:
random tree, `n = 22` (generator `random_tree(22, 7)`, i.e. seed 11 in the
finding's prose = Python `Random(7)` stream; the driver reproduces it from
the committed generator), seed vertex 5, `q = 1/28`, `rho = 1/96`
(interior, `|S*| = 22`). Literal `fm` (I5-C's algorithm, exact rationals):
admission burst `t = 1..10` with a face change at every stage (support
4 -> 22), lock at `t = 10` with the final re-tune
(`beta: 227/273 -> 27/29`, i.e. `q_r: 23/250 -> 1/28 = q`), then at
`t = 13` (lock face three stages old):

```
zeta(a_13)_8 = -2.50e-6 < 0,   zeta(a_13)_10 = -3.32e-6 < 0,
Delta_13 = 2.61e-3 > 0,  class F (full retraction), exact rationals.
```

Hence the unconditional never-triggering lemma for unmodified `fm` is
**Refuted**; any future unmodified statement must carry an entrance
condition. The mechanism is the young-face transient that I6-A1's tau-floor
near-failures (rt16b ratio 0.9926, cat4_3 ratio 0.841) had flagged; K8ctl
is the same disease. **Scope of the refutation:** it kills never-triggering,
*not* the packing inequality — on rt22b the fires cease (single fire at
`t = 13` in `T = 120`, stages 14..119 fire-free, total retraction mass
`sum_t 1^T r_t = 2.05e-3`, verified by the driver),
so `J_T^fin` is a finite one-event constant there; its numeric value in the
i2c `gamma` ledger has not been computed (Open as a number). *Status:*
Refuted-draft with exact witness, machine-reproduced
(`run_i5c(Inst(rt22b), 20, 'fm')`). *Proof/data:*
`findings/i7a_never_trigger_complete.md` §3; driver Part 2.

**T13 (The `K_n` absorption theorem — COMPLETE).** `G = K_n`, `n >= 2`,
(H0), `q <= 1/2`, the ORIGINAL recurrence (baseline cap, global `beta`).
Then `V_{t+1} <= (1-q)^2 V_t` at every stage — N/clean stages by the exact
companion identity `V_{t+1} = s V_t`; F stages by the pure `(n,q)`
inequality `s(2-mh) <= (1-q)^2` (`<=> q <= 1/2`, equality at `q = 1/2`);
**genuinely partial stages by the clip identity
`ell_t = x_t + (beta d_t - Delta_t 1)_+` plus the truncation-covariance
lemma `Var_pi(psi(v)) <= Cov_pi(psi(v), v)` for nondecreasing 1-Lipschitz
`psi`** — with the margin law `V_{t+1}/((1-q)^2 V_t) <= max(theta_F, mh/m0)
< 1`, approaching 1 only through the F-channel that is already the sharp
`q = 1/2` boundary. Consequently the absorption certificate fires at
`t_abs <= 12` (a-priori bound `<= 22`), all later stages are N,
`gamma_t = 1`, and `J_T^fin <= B <= 0.36918 < log 2` for all `T`: packing
with `c = 1`. The old partial-stage bound (C17) is simultaneously shown
structurally wrong (fails 47/53 on the manufactured P-stage battery; the
published `K_8` pulse at 0.979 was the luckiest case). *Status:*
Proved-draft, **no Open links**. *Verification:* 140-instance grid, 18/18
predicates, 7,130 stage checks per universal predicate; 103-stage P-battery;
repaired bound 103/103 with margin <= 0.87. *Proof:*
`findings/i2c_windowed_proof.md` §1–4 (lemma chain C1–C16) +
`findings/i6b_c9_closure.md` §3 (C9', the closure) and §6 Theorem A.

**T14 (The master form and Theorem B'').** Define, for `y = beta d_t -
Delta_t 1` and high part `h_t`, the stage-free quadratic functional

```
Psi(y,h) = |Mm(b+w)|_D^2 - m0 <b, Mm b>_D - nu^2 |Mm h|_D^2 - beta <h, G h>_D,
b = P y - nu h,  w = P(y_-),  nu = q/(1+q),  G = m0 I - 2 Mm + Mm^2 .
```

Then **identically, at every stage of the safeguarded recurrence, for any
cap and any history: `V_{t+1} - (1-q)^2 V_t = Psi(y_t, h_t)`**. Unmixed
sign patterns are unconditionally safe (N-lemma `y >= 0`, F-lemma
`y <= 0`, both per-mode); therefore **(PSI)** `sup_{y,h} Psi_{G,q} <= 0`
implies C9 at every stage, absorption, and packing with `c = 1`
(Theorem B'': connected `G`, (H0), (Hgap) `mu_2 >= 2q`, (PSI)). The kernel
route is settled: cone-TK `>= 0` is *equivalent* to the entrywise (H-K),
with exact in-cone `TK < 0` witnesses on every (H-K)-failing graph — TK was
the wrong invariant, and (H-K) survives only as a sufficient subclass
(`(H-K) => (PSI)`). *Status:* Proved-draft modulo (PSI); identity exact.
*Verification:* C9M_id 1,696/1,696 stages (82 instances, incl.
out-of-class); C9M_neg 1,360/1,360 in class; C9F (adversarial-`h` form,
exact `S^{-1}` solve per stage) 1,360/1,360. *Proof:*
`findings/i7b_tk_closure.md` §1–2, §6.

**T15 ((PSI) coverage map).** (1) All `K_n` (subsumed by T13). (2) The
(H-K) subclass — a pure, `q`-free graph condition
`4 vol ((3D-A)^{-1}D)^2_{ij} <= d_j` — proved: `K_{a,b}`, cocktail, rook,
`Q_3`, `Circ_8/12`, Kneser(6,2), Paley13/17, T(5). (3) Exact rational
instance proofs (KKT face enumeration + Fourier–Motzkin closure of all 194
degenerate faces): `(C6,1/10)` strict, `(C6,1/4)` sharp `= 0`, `(C8,1/8)`
strict, `(Q3,1/3)` sharp, `(Petersen,1/3)` sharp — the boundary maximizers
are mixed one-vertex-up / set-down patterns, so the class theorem is tight
through the P-channel too. (4) Complete float decisions (tol 1e-11, every
disjoint sign pair / Aut-orbit pair): `Q4` at `q = 1/10` and boundary
`1/4` (all `3^16` assignments via 131,299 orbit pairs), Petersen (3 q's),
C6–C12 cycles, circulants, RR(12,3), T(5). (5) Adversarial sweep, 20
further families (Q5, Q6, Kneser(7,3), Paley, Shrikhande, random regular,
long cycles): zero violations, while (H-K)/(H-K1) die wholesale. *Status:*
(2)–(3) Proved-draft; (4) Decided-float-complete; (5) Measured. *Open:*
analytic (PSI) for all in-class `(G,q)` — the natural attack is the
distance-regular family programme at the exact boundary extremals.
*Proof:* `findings/i7b_tk_closure.md` §4–6.

**Dependency graph.** T11 (fm-w, `J = 0`) uses T0–T10. T13 (`K_n`) is
self-contained (C1–C16 + C9'). B'' (T14) uses the i4a general certificate
(S1–S3, verified 1,696/1,696 + 1,086/1,086) + T14/T15. The three headline
clauses of §1 are logically independent; they share only the safeguarded
recurrence and the trigger predicate T1.

### 3.1 The re-tune direction, reconciled (I5-C "downward" vs I7-A "upward")

Both notes describe the **same event with opposite variable conventions**;
the data conflict is nil. Along any `fm`/`fm-w` run the face chain is
nondecreasing (monotone invariant, T4), nested faces make `alpha_S`
nonincreasing (T7 Lemma A), hence the certified `hi` and `q_r` are
**nonincreasing** and `beta = (1-q_r)/(1+q_r)` is **nondecreasing** along
the chain. I5-C §5 named re-tunes by `q_r` ("downward" = `q_r` decreases —
the only direction that occurs) and measured that these re-tunes *release*
the re-tuned Lyapunov (jump < 1 at 85/85, the one positive jump being the
`t = 1` initialization). I7-A §3 named the rt22b lock re-tune by `beta`
("upward beta re-tune", `227/273 -> 27/29`) — which is the *same* move:
`q_r: 23/250 -> 1/28 = q` (rt22b is interior, so the lock face is `V` and
Lemma A's `S = V` branch forces `q_r = q` exactly). Verified by the driver
(Part 2) on the rt22b fm run: along the face chain (`t >= 1`) the ten
distinct calibrations are `q_r = 51/200, 49/200, 229/1000, 223/1000,
89/500, 21/125, 157/1000, 129/1000, 23/250, 1/28` — monotone nonincreasing,
`beta` monotone nondecreasing, lock re-tune exactly as stated. One
bookkeeping convention surfaced by the check: at stage 0 the face is empty
and the code reports the *global* `(q, beta)`; the move from that
placeholder to the first (small, high-`alpha_S`) face *raises* `q_r` —
this is not a face re-tune but exactly I5-C §5's measured **one-time
initialization jump** (the only positive Lyapunov jump, 0.22–2.81 nats),
an artifact of starting the schedule at `q`.
The two claims also concern different quantities: I5-C's 85/85 is about the
**Lyapunov jump at the re-tune stage** (no inflation); I7-A's fire is about
the **trigger three stages later** (a young-face transient under freshly
increased momentum, which the safeguard then correctly intercepts). Fixing
the document convention: *a re-tune's direction refers to `q_r`; every
re-tune that occurs is downward in `q_r` and therefore upward in `beta`;
downward-in-`q_r` re-tunes release Lyapunov (Measured 85/85) and are
precisely the events after which the unmodified variant may fire (Refuted
example rt22b) — which is why `fm-w` inserts its warmup exactly there.*

---

## 4. What this means for the repository's Route-B program

The Route-B blocker, as the assessment records it, asked for a **windowed /
spectrally split Lyapunov for the ACTUAL finite recurrence** — the
actual-finite net exponent `J_T^fin <= (1-c)qT + B` on low-Dirichlet faces,
after Rounds 026–027 had exhausted one-step banks against the `K_2`
(critically damped low mode) and `K_8` (high-band pulse) template families.
The campaign's answer is threefold, and sharper than the question:

1. **For the original recurrence the target is TRUE with `c = 1` — no
   window needed — on `K_n` (unconditional) and on the (Hgap)+(PSI) class.**
   Absorption is strictly stronger than any windowed statement: window 0
   carries all inflation, every later window contributes exactly 0 nats.
   The `K_2` STOP family is *explained* (the low mode is exactly critically
   damped, `(z-(1-q))^2`; one-step banks must lose `O(q^2)` per stage —
   i2c L-S), and the `K_8` STOP family is *absorbed* (its pulse cell is the
   grid's single genuinely partial stage; the clip identity + truncation
   covariance close it with margin law `< 1`, and the old 2.1%-margin bound
   is diagnosed as structurally wrong rather than tight). Both families now
   sit inside the proved 140-instance grid.

2. **In general the original recurrence's never-triggering is
   FALSE-adjacent — rt22b fires — but firing does not refute packing.**
   What rt22b refutes is the hope that the unmodified recurrence never needs
   its safeguard; the packing bound itself remains unrefuted everywhere
   (on rt22b the fire is a single event; on the sustained-correction path
   families the measured windowed slope is 0.056–0.126 << 1 under the face
   cap — i4a §2.4). The honest general status of the ORIGINAL recurrence's
   packing on proper faces is therefore: **Measured (slopes far below
   threshold), Open as a theorem** — that open question is now *optional*,
   because:

3. **A small, legal, exactly-implementable modification makes the safeguard
   provably idle** (`J_T^fin = 0`, T11), which trivializes packing on every
   instance class tested, with no `alpha` restriction and no spectral
   hypothesis (the gate checks (H-sep) and falls back safely). The price is
   real and measured: 25–60% more iterations than baseline to fixed
   accuracy, plus warmup stages whose certified length is large on
   near-critical faces (asymptotically the face rate `z_+ < sqrt(m_S beta)`
   still wins). The modification is not cosmetic — T12 proves the unmodified
   variant genuinely needs an entrance condition.

**Promotion path (what to audit first).**

1. T4 (P-A) — five lines, new, everything downstream leans on it.
2. T9's identity `mu+ = s_2/(1-q_r)^2` and the `J_S` formula constants
   (this is where an error would silently break T11 while the battery
   still passes).
3. The clip identity + truncation-covariance lemma (T13's closure) — short,
   self-contained, and it retires the C15/C17 scaffolding.
4. The master-form identity (T14) at one hand-checked stage.
5. The audit anchors (§6): rt22b at `t = 13` (exact fire), Petersen
   `q = 1/3` and C6 `q = 1/4` (exact `sup Psi = 0` sharpness), and the
   S16 gate rejection (`n_od = 2`).

**Against the repository's theorem-acceptance checklist** (for the headline
T11, stated honestly):

1. *Graph class / access / seeds / regime:* any connected simple `G`
   (per-component otherwise); whole-graph arrays in the verification code —
   **no adjacency-list locality claim**; arbitrary nonnegative seeds tested
   with single-seed and pulse families; `alpha in (0, 1/2)` (`kappa > 0`),
   `rho > 0`.
2. *Output representation / accuracy namespace:* iterates of the RPPR
   obstacle recurrence; all statements in the **`eps_pg`-side inflation
   ledger of the surrogate**; no `eps_ppr` conversion supplied here.
3. *Guarantee type:* deterministic.
4. *Support evolution:* nested (monotone, self-sustained by T4);
   at most `|S*|` face changes.
5. *Inverse primitive:* exact obstacle (LCP) solves as a primitive — the
   theorem quantifies over exact inner solves; inexactness degrades
   `Delta_t = 0` to `Delta_t = O(eps_in)` (Open, §5.4).
6. *Charged operations:* NOT yet assembled into a work theorem — see the
   sketch below. T11 controls **inflation, not total work.**
7. *Preprocessing/storage:* per distinct face (<= `|S*|`): one `w^(8)`
   build (8 exact triangular solves), one CW bracket (free), ~12
   exact-inertia bisections, one `J_S` evaluation; caches of size `O(|S|)`.
8. *Uniformity:* T11 is **algorithm-specific and graph-uniform in
   hypothesis** (no spectral assumption), but its verification is a
   19-cell battery — the theorem text quantifies over all instances,
   pending audit; T13 is graph-specific (`K_n`) and unconditional;
   B'' is conditional on (PSI).

**The missing work theorem (sketch, honest).** Never-triggering removes the
retraction/inflation term; an end-to-end `O_tilde(.)` statement still needs:
(a) an **outer iteration count**: pre-lock <= `|S*|` segments, each with
`J_S` warmup prox stages (rate `m_S` per stage) plus an accelerated tail at
rate `z_+(m_S)`; summing needs a bound on `sum_S J_S` — currently the
certified `J_S` pays `A_S^2/dn-_S` and can reach ~900 on near-critical path
faces, so the assembled count is *not* yet `O_tilde(1/sqrt(alpha_S))`
unless the sharp componentwise entrance certificate (empirically
`t_lock + <= 7`, 176/176) is proved to propagate — **that single inequality
is the remaining mathematical residue for practical acceleration with a
complete proof**; (b) a **per-stage charge**: each obstacle solve, trigger
evaluation, and certificate build charged in the repository's ledger
(scans of `S_t` cost `vol(S_t)`; the exact LCP solve must be replaced by a
charged iterative/persistent primitive with (a)'s inexactness handled);
(c) the **RPPR -> PPR bridge**: choice of `rho` vs `eps_ppr` and the
output-error conversion, which this campaign deliberately did not touch.
Slotting (a)–(c) into the repository's existing terminal-bridge and gate
machinery is the natural next direction; nothing in T11 obstructs it.

---

## 5. Verification ledger

### 5.1 Predicate table (every load-bearing inequality in the chain)

Counts are exact-rational checks unless marked (f) = float/Measured.
Locations are relative to the campaign root
`manuscript/claude-overnight-2026-08-24/`.

| # | predicate | statement (short) | count | code |
|---|---|---|---|---|
| L1 | NF | `Delta_t = 0`, fm-w cert, 19 cells | 3,840/3,840 | `w7_windowed/i7a_fmw.py` (`run_fmw`), data `i7a_out/*_cert.json` |
| L2 | YPOS | `Y_t >= 0` on `supp(x_t)` | 3,821/3,821 | same |
| L3 | CMP | `x_{t+1} >= a_t` (P-A conclusion) | 3,840/3,840 | same |
| L4 | KKT | interior-row identity on `supp(x_{t+1})` | 3,840/3,840 | same |
| L5 | UID | `zeta(a_t) = (1+b)Y_t - bY_{t-1}` on `S_t` | 3,821/3,821 | same |
| L6 | GATE | exact inertia certificates, all momentum faces; S16 lock face rejected (`n_od = 2`) | all faces | `i7a_fmw.py:inertia_le,lam2_lower` |
| L7 | RLE1 (f) | entrance `R_{t*} <= 1` | 8/8 (max 0.26) | `run_fmw` momstarts |
| L8 | SHARP1 (f) | sharp entrance form <= 1 | 8/8 | same |
| L9 | LFLOOR (f) | `L_t >= (1-q_r)L_{t-1} > 0` at momentum stages | 571/571 | same |
| L10 | RDECAY (f) | `R_{t+1} <= (s_2/(1-q_r)^2) R_t` | 513/563 aggregate; the 50 non-ok pairs are all on bt15 (38) / bt31 (12) at state error ~1e-21 (double underflow; exact claims unaffected); 100% on every other cell incl. 227/227 on rt22b-400 | same |
| L11 | J2 control | `J = 2`: NF 3,599/3,600 (fire rt22b `t=34`); `R <= 1` 0/183; sharp 176/183; all 176 sharp entrances fire-free | as listed | `i7a_out/*_J2.json` |
| L12 | CE | rt22b, unmodified fm: first fire `t = 13`, class F, `Delta = 2.61e-3` | exact, reproduced | `i5c_core.py:run_i5c`; driver Part 2 |
| L13 | R1 KKT | i6a1 reduction | 2,816/2,816 | `w7_windowed/i6a1_checks.py` |
| L14 | R2 (T-gen') | trigger formula incl. 145 face changes | 2,803/2,803 | same |
| L15 | (T) | three-term same-face inequality | 2,509/2,509 | same |
| L16 | c-floor | `c_t >= [(1-q_r)/2] c_{t-1}` (= NF) | 1,498/1,498 | `i6a1_floors.py` |
| L17 | ZFh | tau-floor (motivating near-failures) | 1,565/1,567 | same |
| L18 | T0/CA/CAoff/CC/CG | i6a2 residual frame | 2,041/2,041 each | `i6a2_battery.py` |
| L19 | CNEW | activation lemma both halves | 89/89 + 89/89 | same |
| L20 | inertia | `n_od = 1` on 78/79 faces; the equivalence chain | 79/79 | same |
| L21 | safety flags | 8 flags, fm/bm battery | 68,800/68,800 | `i5c_core.py`, `i5c_results.json` |
| L22 | C10f | matched face floor `L^w` | 2,330/2,330 | same |
| L23 | certs | per-face overdamping certificates | 110/110 | same |
| L24 | Lemma A strict | CW `lo > alpha` on proper faces | 288/288 | same |
| L25 | re-tunes | downward-in-`q_r` Lyapunov jumps < 1 | 85/85 (f, exact arith, formula-level choice) | `i5c_main.py` §5 |
| L26 | C3face/C9face | post-lock exactness / V-decay | 273/273, 251/251 | `i5c_c9proj.py` |
| L27 | L-E face | face-geometry oscillation bound at correcting stages | 211/211 (worst ratio exactly 1) | `i4a_half1.py` |
| L28 | S1/S2/S3 | general absorption certificate steps | 1,696 + 1,696 + 1,086, all | `i4a_half2.py` |
| L29 | C16 | `s_2(2-m_2) <= (1-q)^2 <=> mu_2 >= 2q` | 82/82, sharp at eq | same |
| L30 | K_n chain | C1–C14, C16 (i2c) | 7,130 per universal predicate, 140 inst | `knproof2.py`, rerun `i6b_knproof3.py` |
| L31 | census | 53 F + 1 P + 0 CC on the K_n grid | 54/54 | same |
| L32 | C9' | clip-identity proof bound at every correcting stage | 54/54 (grid) + 103/103 (P-battery) | `i6b_knproof3.py`, `i6b_pgen.py` |
| L33 | old C17 | REFUTED: fails 47/53, up to 7.76x | exact | `i6b_pgen.py` |
| L34 | (H-K) census | kernel condition per graph | 8/11 families hold | `i6b_cgen.py` |
| L35 | routes A/B | class P-stages | 50/50 (worst 0.870) | `i6b_class3.py` |
| L36 | C9M_id | master-form identity, every stage | 1,696/1,696 | `i7b_class4.py` |
| L37 | C9M_neg | `Psi <= 0` in class | 1,360/1,360 | same |
| L38 | C9F | adversarial-`h` form <= 0 (exact `S^{-1}`) | 1,360/1,360 | same |
| L39 | TK witnesses | in-cone `TK < 0` on Q4/Pet/C6 | 3 exact rationals | `i7b_tk.py` |
| L40 | (PSI) exact | 5 instances incl. 3 sharp boundaries | complete face enum + Fourier–Motzkin | `i7b_exact.py`, `i7b_exact2.py` |
| L41 | (PSI) decided (f) | Q4 both q (131,299 orbit pairs = all 3^16), + §3 list | 0 violations, tol 1e-11 | `i7b_q4.py`, `i7b_decide.py` |
| L42 | sweep (f) | 20 adversarial families | 0 violations; (H-K)/(H-K1) fail x14/x10 | `i7b_sweep.py` |

Refuted-invariant negative space (what an auditor must NOT try to reprove):
upper sandwich, componentwise `(1-q_r)` floor, alignment cones, entrywise
matrix solvents, strong ladder floors (i6a1 §5); CB1, CJ, the entrywise
factorization bridge `Z_-` (i6a2 §5–6); lower-CW-end calibration, "face
calibration is faster" as an iteration count, (Hgap_S) transfer (i5c);
old C17, sign assumptions on `Cov(phih, h)` (i6b); TK `>= 0` beyond (H-K),
the doubled-orthant relaxation (i7b).

### 5.2 The single runnable driver

`i7c/verify_routeB.py` re-runs, in one process:
the 19-cell fm-w certified battery (rt22b at `T = 400`) with the full exact
chain (L1–L6) and the Measured certificate (L7–L10); the rt22b
counterexample and fire census under unmodified `fm` (`T = 120`) plus the
re-tune monotonicity check of §3.1 and the K8ctl control; a `K_n` absorption
spot grid (`n in {2,8,32} x q in {1/10,1/400}`, skew + vpulse seeds at edge
`rho`, plus the published K8 pulse with its genuinely partial stage) through
all 18 predicates of `i6b_knproof3.py`; and the three class boundary
anchors (`Q3` at `q = 1/3`, `C6` at `q = 1/4`, Petersen at `q = 1/3`, all
at `mu_2 = 2q` exactly) through the exact master-form checks
C9M_id / C9M_neg / C9F. The verdict gates on the exact predicates; float
certificate values are printed as Measured. Output of the run performed for
this document (`i7c/verify_routeB.log`, results `i7c/verify_routeB.json`):

```

========================================================================
PART 1: fm-w certified battery (19 cells, exact chain P-A..P-E)
========================================================================
  K8ctl    T=30  NF=(30, 30) MOM=(21, 21) PROX=(9, 9) entr=1 gateJ={8: 8}  [0.1s]
  P12      T=200 NF=(200, 200) MOM=(0, 0) PROX=(200, 200) entr=0 gateJ={3: 10, 4: 19, 5: 31, 6: 47, 7: 68, 8: 94, 9: 124, 10: 160}  [1.1s]
  P16      T=250 NF=(250, 250) MOM=(0, 0) PROX=(250, 250) entr=0 gateJ={3: 10, 4: 19, 5: 31, 6: 47, 7: 68, 8: 94, 9: 124, 10: 160, 11: 201, 12: 248}  [2.6s]
  P18      T=200 NF=(200, 200) MOM=(0, 0) PROX=(200, 200) entr=0 gateJ={3: 10, 4: 19, 5: 31, 6: 47, 7: 68, 8: 94, 9: 124, 10: 160, 11: 201, 12: 248, 13: 301}  [2.1s]
  P20      T=250 NF=(250, 250) MOM=(0, 0) PROX=(250, 250) entr=0 gateJ={3: 10, 4: 19, 5: 31, 6: 47, 7: 68, 8: 94, 9: 124, 10: 160, 11: 202, 12: 248, 13: 301}  [3.3s]
  P24      T=250 NF=(250, 250) MOM=(0, 0) PROX=(250, 250) entr=0 gateJ={3: 10, 4: 19, 5: 31, 6: 47, 7: 68, 8: 94, 9: 124, 10: 160, 11: 202, 12: 248, 13: 301, 14: 359, 15: 424, 16: 495}  [5.4s]
  P24rho2  T=250 NF=(250, 250) MOM=(0, 0) PROX=(250, 250) entr=0 gateJ={3: 10, 4: 19, 5: 31, 6: 47, 7: 68, 8: 94, 9: 124, 10: 160, 11: 202, 12: 248, 13: 301, 14: 359, 15: 424, 16: 495, 17: 569}  [6.0s]
  P24rho3  T=250 NF=(250, 250) MOM=(0, 0) PROX=(250, 250) entr=0 gateJ={3: 10, 4: 19, 5: 31, 6: 47, 7: 68, 8: 94, 9: 124, 10: 160, 11: 202, 12: 248, 13: 301, 14: 359, 15: 424, 16: 495}  [5.3s]
  P30lr    T=200 NF=(200, 200) MOM=(0, 0) PROX=(200, 200) entr=0 gateJ={4: 19, 5: 31, 6: 47, 7: 68, 8: 94, 9: 124, 10: 160, 11: 201, 12: 248, 13: 301, 14: 359, 15: 424, 16: 495, 17: 570, 18: 654, 19: 744}  [5.4s]
  S16      T=100 NF=(100, 100) MOM=(0, 0) PROX=(100, 100) entr=0 gateJ={1: 'beta=0 calibration', 2: 'n_od=2 on comp size 2'}  [0.1s]
  bt15     T=200 NF=(200, 200) MOM=(118, 118) PROX=(82, 82) entr=1 gateJ={3: 37, 7: 66}  [0.6s]
  bt31     T=140 NF=(140, 140) MOM=(69, 69) PROX=(71, 71) entr=1 gateJ={3: 37, 7: 66}  [0.5s]
  cat4_3   T=200 NF=(200, 200) MOM=(44, 44) PROX=(156, 156) entr=1 gateJ={4: 10, 5: 15, 8: 46, 9: 61, 12: 81, 13: 105}  [2.0s]
  cat5_2   T=200 NF=(200, 200) MOM=(50, 50) PROX=(150, 150) entr=1 gateJ={4: 14, 6: 34, 7: 44, 9: 58, 10: 77}  [1.4s]
  cat6_2   T=160 NF=(160, 160) MOM=(0, 0) PROX=(160, 160) entr=0 gateJ={4: 14, 6: 34, 7: 44, 9: 58, 10: 76, 12: 97, 13: 124, 15: 150, 16: 186, 18: 248}  [3.2s]
  rt16b    T=200 NF=(200, 200) MOM=(39, 39) PROX=(161, 161) entr=1 gateJ={4: 22, 8: 74, 10: 90, 12: 109, 14: 117, 16: 109}  [4.1s]
  rt18     T=200 NF=(200, 200) MOM=(2, 2) PROX=(198, 198) entr=1 gateJ={4: 17, 5: 30, 6: 39, 7: 48, 8: 56, 9: 89, 10: 90, 11: 106}  [2.0s]
  rt20a    T=160 NF=(160, 160) MOM=(0, 0) PROX=(160, 160) entr=0 gateJ={5: 13, 7: 31, 8: 75, 9: 84, 10: 92, 12: 166, 15: 203, 16: 251, 18: 277, 19: 315, 20: 321}  [4.7s]
  rt22b    T=400 NF=(400, 400) MOM=(228, 228) PROX=(172, 172) entr=1 gateJ={10: 86, 13: 165, 15: 165, 18: 156, 20: 193, 22: 149}  [45.6s]

  aggregate over 19 cells:
    NF      3840/3840  exact   PASS
    YPOS    3821/3821  exact   PASS
    CMP     3840/3840  exact   PASS
    KKT     3840/3840  exact   PASS
    UID     3821/3821  exact   PASS
    MOM      571/571   exact   PASS
    PROX    3269/3269  exact   PASS
    RLE1       8/8     float (Measured)
    SHARP1     8/8     float (Measured)
    LFLOOR   571/571   float (Measured)
    R-decay pairs ok (float, tol 1e-9): 513/563
    momentum entrances: 8, worst entrance R = 0.25752705426163447
    S16 all-overdamped lock face rejected by gate (n_od=2): True

========================================================================
PART 2: the rt22b counterexample (unmodified fm) + re-tune direction
========================================================================
  rt22b (n=22, q=1/28, rho=1/96, interior |S*|=22): 1 fires in T=120
    fire t=13  class=F Delta=2.609040e-03
  stage 13: class=F Delta=0.00260904021970138  negative zeta coords: [(8, -2.5008320623640466e-06), (10, -3.323618114269274e-06)]
  counterexample reproduced (first fire at t=13, class F): True
  total retraction mass sum_t 1^T r_t = 2.047e-03 ; last fire t=13 ; stages 14..119 fire-free: True
  initialization (empty face, global calib) -> first face: (q_r,beta) (1/28,27/29) -> (51/200,149/251) at t=1   [the i5c one-time jump]
  face-chain re-tunes (9): q_r nonincreasing=True, beta nondecreasing=True
  lock re-tune: (q_r,beta) ('23/250', '227/273') -> ('1/28', '27/29') at t=10 [= "downward" in q_r (i5c) = "upward" in beta (i7a)]
  K8ctl control: unmodified fm fires at t=[2, 3] (fm-w above: NF 30/30)

========================================================================
PART 3: K_n absorption spot grid (n in {2,8,32} x q in {1/10,1/400})
========================================================================
  K2 q=1/10 skew/edge        t_abs=1   J_total=0.00000 word=NNNNNNNNNNNNNNNNNNNNNNNN
  K2 q=1/400 skew/edge       t_abs=1   J_total=0.00000 word=NNNNNNNNNNNNNNNNNNNNNNNN
  K8 q=1/10 skew/edge        t_abs=6   J_total=0.21984 word=NNNFNNNNNNNNNNNNNNNNNNNN
  K8 q=1/10 vpulse/edge      t_abs=6   J_total=0.21933 word=NNNFNNNNNNNNNNNNNNNNNNNN
  K8 q=1/400 skew/edge       t_abs=8   J_total=0.00496 word=NNFNNNNNNNNNNNNNNNNNNNNN
  K8 q=1/400 vpulse/edge     t_abs=9   J_total=0.00496 word=NNFNNNNNNNNNNNNNNNNNNNNN
  K32 q=1/10 skew/edge       t_abs=7   J_total=0.32391 word=NNFNNFNNNNNNNNNNNNNNNNNN
  K32 q=1/10 vpulse/edge     t_abs=6   J_total=0.36918 word=NNFNNFNNNNNNNNNNNNNNNNNN
  K32 q=1/400 skew/edge      t_abs=11  J_total=0.00989 word=NNFNFNNNNNNNNNNNNNNNNNNN
  K32 q=1/400 vpulse/edge    t_abs=8   J_total=0.01240 word=NNFNNFNNNNNNNNNNNNNNNNNN
  K8 pulse (published)       t_abs=5   J_total=0.23307 word=NNPFNNNNNNNNNNNNNNNN  Pcert=0.629

  aggregate (11 instances):
    C1_master       578/578  PASS
    C2_Fcollapse     13/13   PASS
    C3_Nlinear      564/564  PASS
    C4_Vdecay       564/564  PASS
    C5_oscil        578/578  PASS
    C6_trigger      578/578  PASS
    C7_defect       578/578  PASS
    C8_philb        578/578  PASS
    C9_Vcontract    578/578  PASS
    C10_lowfloor    578/578  PASS
    C11_monotone    578/578  PASS
    C12_struct       11/11   PASS
    C13_absorb       11/11   PASS
    C14_Rgeom       564/564  PASS
    C15_corrclass    14/14   PASS
    C16_Fcontract    11/11   PASS
    C17_Pcert         1/1    PASS
    C9s_corr         14/14   PASS
    absorption fired in all: True ; max J_total = 0.36918 < log2 = 0.69315: True

========================================================================
PART 4: class boundary instances -- master form Psi (exact rationals)
========================================================================
  Q3-eq  q=1/3 (mu2=2q)    in_class=True word=NNNNNNNNNNNNNNNNNN  {'C9M_id': (16, 16), 'C9M_neg': (16, 16), 'C9F': (16, 16)}
  C6-eq  q=1/4 (mu2=2q)    in_class=True word=NNNNNNNNNNNNNNNNNN  {'C9M_id': (16, 16), 'C9M_neg': (16, 16), 'C9F': (16, 16)}
  Pet-eq q=1/3 (mu2=2q)    in_class=True word=NNNNNNNNNNNNNNNNNN  {'C9M_id': (16, 16), 'C9M_neg': (16, 16), 'C9F': (16, 16)}

  aggregate:
    C9M_id    48/48  exact PASS
    C9M_neg   48/48  exact PASS
    C9F       48/48  exact PASS

========================================================================
VERDICT
========================================================================
  ALL GATED (EXACT) CHECKS PASS.
  fm-w: NF 3840/3840; P-A CMP 3840/3840; P-B YPOS 3821/3821; KKT 3840/3840; UID 3821/3821
  counterexample rt22b: first fire t=13 class F (unmodified fm); fm-w on same cell: NF 400/400.
  K_n spot: all predicates pass, absorption True, max J_total 0.36918 < log 2.
  class boundary (Q3/C6/Petersen at mu2=2q): C9M_id 48/48, C9M_neg 48/48, C9F 48/48.
  total 109.5s
  saved i7c/verify_routeB.json
```

### 5.3 What the driver deliberately does not re-run

The full 140-instance `K_n` grid, the 82-instance class battery, the
103-stage P-battery, the Q4 orbit enumeration, and the exact (PSI) instance
proofs are multi-minute-to-multi-hour artifacts; their committed outputs are
`w7_windowed/i6b_knproof3_results.json`, `i6b_class3.json`,
`i6b_pbattery.json`, `i7b_q4_decide.json`, `i7b_exact*.json`, and each is
reproducible by running the named script with no arguments.

### 5.4 Open list (genuinely open after this document)

1. **Analytic (PSI)** for all in-class `(G,q)` — sole hypothesis of B'';
   family programme at the exact boundary extremals is set up.
2. **Sharp componentwise entrance propagation** — would shrink `J_S` to
   `O(1)` and make `fm-w` practically accelerated with a complete proof;
   empirical record 176/176 + `tcs = t_lock + <= 7` on 9/9 cells. The
   refuted-invariant lists fence off the approaches that cannot work.
3. **Certified entrywise Perron brackets** for `A_S`, `1/m_psi`
   (standard M-matrix technology; enters `J_S` only in a log) —
   engineering, not mathematics.
4. **Inexact inner solves:** all conclusions degrade to
   `Delta_t = O(eps_in)`; no quantitative theorem yet.
5. **Finite precision:** every claim is exact-rational; no floating-point
   stability analysis exists.
6. **Work-ledger integration:** the end-to-end charged work theorem
   (outer count x per-stage charges + RPPR->PPR bridge) — sketched in §4;
   never-triggering supplies only the inflation term `J_T^fin = 0`.
7. **`J_T^fin` of unmodified `fm` on rt22b** as a number (mechanism
   bounded, ledger value uncomputed); more broadly, packing for the
   ORIGINAL recurrence on proper faces remains Measured-only
   (slopes 0.056–0.126), now optional.
8. **Two-block momentum on all-overdamped faces** (gate-failing faces run
   prox-only — safe and convergent, not accelerated).

---

## 6. Honesty footer

Everything here is campaign-labeled and **unaudited**: "Proved-draft" means
a complete proof text plus exact-rational machine verification of every
load-bearing inequality on every tested instance — it is not a refereed
proof, and on the repository's ladder it should enter as Conditional until
an independent audit passes. All exact counts are `fractions.Fraction`
end-to-end; float appears only in explicitly Measured rows (modal
certificate values, `J_S` evaluation, decided-not-proved (PSI) instances).
The verification is battery-based; theorem texts quantify beyond the
batteries and that gap is exactly what an audit must close. The recommended
audit anchors, in order: **the rt22b counterexample** (exact fire at
`t = 13` — if this does not reproduce, I7-A's §3 is wrong and T12/T11's
motivation collapses); **the sharp boundary cases** Petersen `q = 1/3` and
`C6` `q = 1/4` (exact `sup Psi = 0` — if either is not tight, T14/T15's
sharpness analysis is wrong); the **S16 gate rejection** (`n_od = 2` — the
one (H-sep) violator, distinguishing gate from assumption); and the
**single K_n P stage** (published K8 pulse, true ratio 0.456 vs old bound
0.979 vs repaired bound — the case that exposed C17). This document makes
no claim in the `eps_ppr` output namespace, no adjacency-list locality
claim, no charged-work claim, and no claim that any of this resolves the
repository-wide residual-convention decision.
