# I6-A1 — Never-triggering lemma, induction/comparison route

**VERDICT: PROVED-except-one-step.** The trigger analysis is now an exact,
fully verified reduction: never-firing at stage `t+1` is EQUIVALENT to a
componentwise three-term linear inequality in the increments
`d_t = x_t - x_{t-1}` alone (`x*`-free, cap-free, face-local), and that
inequality is the positivity of one canonical solution of the SAME two-term
recurrence `y_{t+1} = M_S[(1+b)y_t - b y_{t-1}]` that drives the iteration.
Everything around this one positivity statement is proved and exactly
verified (reduction identities 2 803/2 803, base case, face-change stages,
one-step propagation, calibration algebra). The one remaining step — the
positivity of that canonical trajectory — is shown to be UNPROVABLE by any of
the one-step componentwise certificates on the task sheet: the sandwich, the
componentwise floor, the alignment cone, and the matrix-solvent comparison
are each REFUTED by exact counterexamples on fresh instances. The minimal
failing inequality is isolated below (§6), with its two counterexample stages
and the weaker facts that still hold. The correct remaining mechanism is
spectral (Perron domination), i.e. exactly sibling I6-A2's route.

Code: `w7_windowed/{i6a1_checks,i6a1_floors,i6a1_solvent}.py`; data
`w7_windowed/i6a1_out/*.json`, `i6a1_solvent.json`. Exact Fractions
everywhere except `i6a1_solvent.py` (float, labelled Measured-float).
Battery: 8 of the 9 i5c proper-face cells re-verified exactly (S16 re-run
timed out; i5c's record stands) + K8 negative control + 4 fresh instances:
P24 at two new rho breakpoints (15/1024, came out interior; 17/1024, proper
`|S*|=22`) and two random trees (rt18, proper `|S*|=11/18`; rt16b, interior
`16/16`). The two fresh interior cells also never fire (calibration inert
there, `q_r = q`), while K8 fires — see §7(c).

---

## 1. The trigger predicate, extracted verbatim

`engine.py:149-159` (baseline) and `i5c_core.py:136-171` (fm/bm variants)
share one predicate. Stage `t`, hat coordinates:

```
dh = x_t - x_{t-1};  a_t = x_t + beta_t*dh;  S_t = supp(a_t)
zeta(a_t)_i = ct_i - (Qt a_t)_i                     for i in S_t
Delta_t = max(0, max_{i in S_t} [-zeta(a_t)_i]_+ / dv_i)
```

with `dv_i = alpha*d_i` (base/bm) or `(Qt_S w)_i` (face cap). Since
`dv_i > 0` (verified flag `pos_den`),

> **Delta_t = 0  <=>  zeta(a_t)_i >= 0 for all i in supp(a_t)** — the trial
> is a subsolution on its own support. The cap direction and trigger
> denominator affect only the SIZE of a positive `Delta`, never whether it is
> zero. Never-triggering is therefore cap-free, and `fm`/`bm` agreeing (both
> 0 corrections, i5c) is explained, not a coincidence.

**Step-1 correction to the task sheet.** "Trial error `>= 0`" is NOT the
never-fire condition. `etilde_t >= 0` (no overshoot) is a *consequence* of
never-fire plus the safety theorem (`ell = a <= x*`), not the mechanism; the
right statement is the subsolution one, `zeta(a_t) >= 0` on `S_t`, and it is
`x*`-free (below). Candidates built on the error vector are the wrong
variables.

## 2. The exact reduction chain (all PROVED, engine-verified)

Hypotheses used: exact obstacle solves; monotone invariant (`d_t >= 0`, supp
nondecreasing, `S_t = supp(x_t)` — the i5c safety flags, stage-local in
`beta_t >= 0`); `kappa = 1-2alpha > 0`.

**R1 (KKT identity).** On `supp(x_{t+1})`:
`ct_i - (Qt x_{t+1})_i = kappa d_i (x_{t+1} - ell_t)_i`. Immediate from the
interior rows of the prox obstacle solve. Engine: **2 816/2 816** stages
(all 12 completed cells, including the firing K8 stages — the identity is
retraction-agnostic).

**R2 (trigger formula, face-change-proof).** If stage `t` never fired
(`ell_t = a_t`), then on `S_{t+1}`:

```
zeta(a_{t+1}) = kappa D (d_{t+1} - beta_t d_t) - beta_{t+1} Qt d_{t+1}   (T-gen')
```

and never-fire at `t+1` `<=>` `(T-gen') >= 0` on `S_{t+1}`. Note `x*` and
`ct` have cancelled: the trigger lives entirely in increment space. Engine:
**2 803/2 803** consecutive-stage identities (all cells, all face changes
included), worst margin over never-fire cells `+1e-12 .. +1e-27` (positive,
razor-thin: any proof must be exact).

**R3 (same-face reduction).** If additionally stages `t-1, t` solve interior
on the same face `S` (so `(Qt_S + kappa D_S)(x_{t+1}-x_t) = kappa D_S
(a_t - a_{t-1})`, i.e. `d_{t+1} = M_S u_t`, `u_t = (1+b)d_t - b d_{t-1}`,
`M_S = (Qt_S + kappa D_S)^{-1} kappa D_S`), then

```
zeta(a_{t+1})|_S = kappa D tau_{t+1},
tau_{t+1} := (1+b)d_{t+1} - b(2+b) d_t + b^2 d_{t-1}                      (T)
```

so never-fire `<=>` `tau_{t+1} >= 0` componentwise. Crucially the solve
difference kills `ct` and `x*`: **R3 is valid pre-lock on every maximal
same-face segment**, not just post-lock. `M_S >= 0` entrywise
(`Qt_S + kappa D_S` is a strictly diagonally dominant Z-matrix, hence an
M-matrix, inverse `>= 0`), `M_S` is `D`-self-adjoint, substochastic
(`M_S 1 <= m 1`), spectral radius `m_S = kappa/(kappa+alpha_S)`.

**R4 (exact algebra of (T)).** With `b = (1-q_r)/(1+q_r)`:
`(1+b)(1-q_r) - b = b`; `b(2+b) - b^2 = 2b`; `2b/(1+b) = 1-q_r`; and the
two decompositions

```
tau_{t+1} = (1+b) sigma_{t+1} + b^2 delta_t ,   sigma_{t+1} = d_{t+1}-(1-q_r)d_t ,
                                                delta_t = d_{t-1}-d_t ;
tau_{t+1} = (1+b) c_t - b c_{t-1} ,             c_t = d_{t+1} - b d_t .
```

So: floor slack can be traded against the previous decrement, and never-fire
is EXACTLY the weak `c`-floor `c_t >= [b/(1+b)] c_{t-1} = [(1-q_r)/2] c_{t-1}`.
[Sandwich `=>` (T) is the special case: `delta_t >= 0` and `sigma_{t+1} >= 0`
suffice — proved, but the sandwich itself is refuted as an invariant, §5.]

**R5 (self-similarity / the 2-cycle).** On a same-face segment, `tau`
satisfies the SAME recurrence `tau_{t+1} = M_S[(1+b)tau_t - b tau_{t-1}]`,
via the closed 2-cycle `tau_{t+1} = (1+b)c_t - b c_{t-1}`,
`c_{t+1} = M_S tau_{t+1}` (both exact). Hence:

> **The never-triggering lemma is equivalent to: one canonical solution of
> the driving two-term recurrence (the trigger sequence itself, with
> explicitly computable initial data per face segment) stays componentwise
> nonnegative.** The problem is exactly self-similar; no information is lost
> in this reduction.

**R6 (one-step propagation — the induction step that IS available).**
If `tau_t >= 0` and `(1+b)tau_t >= b tau_{t-1}` componentwise, then
`tau_{t+1} = M_S[(1+b)tau_t - b tau_{t-1}] >= 0` (`M_S >= 0`). One line.

**R7 (calibration enters exactly here).** Per overdamped mode
`m >= 1-q_r^2` of `M_S`: the modal roots are real and `z_-(m) > b`
(proof: `p(b) = b^2(1-m) > 0` and the vertex `m(1+b)/2 >= (1-q_r^2)(1+b)/2
> b` since `1-q_r^2 > 1-q_r = 2b/(1+b)`); at `zeta = 1-q_r` (inside the root
interval) the slack is `p(1-q_r) = -b[m-(1-q_r^2)] <= 0`, i.e. the scalar
floor propagates with exactly the certified margin `m_S - (1-q_r^2)` of
Lemma C. Underdamped modes have `|z| = sqrt(mb)`. This is why the UPPER-end
CW calibration is the safe direction (confirms i5c §1), and why the scalar
(Perron-projected) theory is clean while the componentwise one is not.

## 3. Base case and face changes (Steps 3-4): verified, and reduced

* **Base `t = 1`** (`ell_0 = 0`, `d_1 = x_1`): `(T-gen')` reads
  `kappa d_i x_{1,i} >= beta_1 (Qt x_1)_i` on `S_1`. Holds in all 12
  never-fire cells (contained in the R2 counts). No special-casing needed:
  R2 covers `t = 0` onward.
* **Face changes.** R2 needs no same-face assumption; never-fire at the 145
  change stages of the battery is verified directly through it. On entering
  coordinates `(Qt d_{t+1})_i <= 0` at **133/145** changes (then never-fire
  is trivial there since `kappa d_i (d_{t+1} - b d_t)_i = kappa d_i d_{t+1,i}
  >= 0`); the 12 exceptions still satisfy (T-gen') with margin. Downward
  re-tunes (`beta` increases along the chain) appear in (T-gen') only through
  `beta_{t+1}`, and smaller `q_r` tightens nothing structurally: the
  change-stage inequality is verified, not yet proved. **A face-change lemma
  remains open but is now a finite, explicitly stated per-stage inequality**
  — not a bookkeeping problem.

## 4. What is TRUE on the battery (exact, 13 cells)

12 cells re-run to completion (S16 exact re-run timed out; its 150-stage
never-fire record is i5c's). 10 proper-face cells (2 350 stages) + 2
interior controls (450) + K8:

| check | count | note |
|---|---|---|
| NF (`Delta = 0`) | **2 350/2 350** proper + **450/450** interior-control | reproduces i5c + 2 fresh proper (P24rho3, rt18) + 2 fresh interior (P24rho2, rt16b) |
| R1 KKT | 2 816/2 816 | incl. K8 firing stages |
| R2 trigger formula | 2 803/2 803 | incl. all 145 face changes |
| (T) `tau >= 0` same-face | **2 509/2 509** (never-fire cells) | worst margins `1e-8..1e-28` |
| `c_t >= 0` | 1 559/1 559 (8-cell floor battery) | `= M tau >= 0`, consistent |
| `c`-floor at `(1-q_r)/2` | 1 498/1 498 | `<=>` NF, consistent |
| K8 negative control | NF 14/16, TT 11/13, worst `-4.0e-4` | the reduction detects firing exactly |

## 5. REFUTED closing candidates (exact counterexamples)

* **Upper sandwich** `d_{t+1} <= d_t`: fails massively pre-lock in every
  cell (momentum growth phase), e.g. P24 302/378. Task candidate (iii) dead.
* **Componentwise floor** `d_{t+1} >= (1-q_r) d_t`: holds on all six
  original i5c cells (lucky family!) but **fails on fresh instances**:
  cat5_2 191/193, cat4_3 190/193, rt18 188/190, rt16b 191/192, P24rho2
  171/227. Task candidate (i) dead — and with it the i5c hope that the
  measured `w`-floor upgrades componentwise.
* **Alignment cones** `M_S d_t >= (1-q_r^2) d_t` (and the `u`-version):
  fail at most stages everywhere (worst ratio 0.80–0.84; P12 68/198). The
  floor, where it holds, does NOT hold via alignment. Task candidate (ii)'s
  cap-conversion route dead (also: in never-fire runs the cap never acts, so
  it cannot transfer anything).
* **Matrix-solvent comparison** (this route's named hope): a matrix `R >= 0`
  with `(1+b)M - R >= 0` and `((1+b)M - R)R >= bM` entrywise would make
  `{y' >= Ry}` invariant and close everything. **No such `R` exists on any
  proper-face cell**: the minimal-solvent iteration diverges (12–16 complex
  pencil roots — underdamped modes obstruct real solvents), the commuting
  candidate has `min entry C3 ~ -0.17`, scans fail. (Measured-float,
  `i6a1_solvent.json`.) The scalar shadow survives (R7) but no entrywise
  matrix version does.
* **Strong ladder floors** `tau_{t+1} >= b tau_t`, `c_{t+1} >= b c_t`: fail
  broadly (e.g. P18 143/184).

## 6. The minimal failing inequality — isolated

The needed hypothesis of R6, the **tau-floor**

```
(1+b) tau_t >= b tau_{t-1}    componentwise, same face                 (ZFh)
```

holds at **1 565/1 567** same-face pairs across 8 cells — and fails at
exactly two: rt16b `t=3` (coord 3, ratio 0.9926 of threshold, face 2 stages
old) and cat4_3 `t=75` (coord 3, ratio 0.841, two stages after the `t=73`
face change). Both failures are **young-face transients**, and both are
absorbed one step later by M-mixing (`tau_{t+1} = M[(1+b)tau_t - b tau_{t-1}]
>= 0` holds because the resolvent row-mixes the deficit against neighboring
slack). So:

> **Minimal missing lemma (exact statement).** For the trigger sequence
> `tau` on each maximal same-face segment (initial data: the two stages
> after face entry, explicitly computable), the solution of
> `y_{t+1} = M_S[(1+b)y_t - b y_{t-1}]` stays `>= 0`. A componentwise
> one-step certificate is impossible (§5, and ZFh's counterexamples); the
> mechanism must quantify M-mixing or Perron domination with the certified
> margin `m_S - (1-q_r^2) > 0` and high-mode decay `sqrt(m b) < z_+` —
> i.e. the I6-A2 spectral route, for which R5 hands over a clean,
> self-contained problem: positivity of ONE explicit trajectory of the
> resolvent momentum recurrence.

## 7. What is proved end-to-end (conditional theorem)

> **Theorem (never-triggering, conditional).** Exact solves, monotone
> invariant, per-stage upper-end CW calibration `beta_t` (i5c §1), start
> `x_{-1} = x_0 = 0`. Suppose at every same-face stage pair the tau-floor
> (ZFh) holds, and at every face-change stage `(T-gen') >= 0` holds. Then
> `Delta_t = 0` for all `t`: no corrections, no retractions, `J_T^fin = 0`
> exactly, and the Route-B packing target `J_T^fin <= (1-c) q T + B` holds
> trivially (with `B` the one-time `t=1` re-tune jump of i5c §5). All
> hypotheses are per-stage checkable online in exact rationals; both are
> theorems-in-waiting, not safety assumptions — the safeguard remains sound
> regardless (i3g safety is beta-stage-local and cap-covered).

*Proof.* Induction on `t` via R2/R3/R6; base by R2 at `t=0,1`; face changes
by hypothesis; within faces by R6. Corollary `J_T^fin = 0`: no retraction
`=>` `Dfin_t = 0 =>` `gamma_t = 1` at every stage (engine identity). ∎

Scope honesty: (a) **exact solves only** — with inexact inner solves R1
acquires a residual `eps_in`-term, so (T-gen') becomes
`zeta(a_{t+1}) >= -(1+beta) eps_in`-ish and never-fire degrades to
"fires only below the inexactness scale"; the reduction survives but the
zero-corrections conclusion becomes `Delta_t = O(eps_in)`; (b) all of this
is the RPPR surrogate inflation ledger — no `eps_ppr` output-semantics claim;
(c) rt16b/P24rho2 show never-fire also occurs on interior faces where
`q_r = q` (calibration inert), while K8 fires: face-calibration is
sufficient-side machinery on these families, not necessary, and the lemma's
eventual hypotheses should not pretend otherwise.

## 8. Evidence labels

**Proved-draft:** R1–R7 (algebra + M-matrix facts; engine verification as
tabulated); the conditional theorem §7; refutation counterexamples §5 (exact
stages named in `i6a1_out/*.json`).
**Measured:** solvent nonexistence (float); NEWNEG 133/145; the tau-floor
1 565/1 567 status and its young-face failure pattern.
**Refuted-draft:** sandwich, componentwise floor, alignment cones, entrywise
solvent certificates, strong ladder floors — as closing invariants.
**Open:** the minimal missing lemma of §6 (trajectory positivity /
quantified M-mixing); the face-change-stage inequality as a lemma; inexact
inner solves.
