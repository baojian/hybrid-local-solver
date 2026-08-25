# I5-C — Face-calibrated momentum, exact: the Route-B closer attempt

**VERDICT: face-calibrated momentum, made exact and certified, does not merely
make absorption fire on proper faces — it makes the safeguard NEVER FIRE AT
ALL.** In exact Fractions, with the certified rational calibration below, the
per-stage face-calibrated variant (`fm`) ran **2 550 stages across 9
proper-face cells (incl. the 400-stage P24 spec cell and a baseline-cap
control) with 0 corrections, 0 retractions, `J_T = 0` exactly, and the matched
face floor `L^w_t >= (1-q_r) L^w_{t-1}` holding at 2 330/2 330 stage pairs.**
The two proper-face obstructions isolated by I3-C/I4-A — L-E (fixed by the
face-aligned cap) and L-H (face underdamping, fixed here) — are now both
closed, with proofs for the calibration lemmas and 68 800/68 800 exact safety
checks. Three honest negatives, all sharpened below: **(1)** the momentum
calibration direction stated in I4-A §6 has its inequality backwards (the
correct lemma is `m_S >= 1-q_S^2  <=>  alpha_S >= alpha`); **(2)** the
`mu_2 >= 2q`-class spectral hypothesis does **not** transfer to these faces
(its face analogue fails on all six i4a cells) — absorption happens anyway,
so a proper-face theorem must take the "drop (Hgap)" route or prove the
safeguard never triggers; **(3)** I4-A's "and is FASTER" is **refuted as an
iteration-count claim**: `fm` is 25–60 % slower to fixed accuracy on every
cell tested (exact crossing times), because the smaller `beta` slows the
pre-lock support sweep and the overdamped Perron root `z_+ > 1-q_S` governs
post-lock; the asymptotic rate does beat the baseline (`z_+ = 0.9619 <
0.9682` on P24) but the crossover is beyond `T = 4800`.

Code: `w7_windowed/{i5c_core, i5c_run, i5c_main, i5c_slope, i5c_c9proj}.py`.
Data: `i5c_results.json`, `i5c_slope.json`, `i5c_main.log`,
`i5c_knregress.log`. Exact battery 1 283 s + regressions. Everything exact
Fractions except `i5c_slope.py` and the face-gap table (§6), which are float
and labelled Measured.

---

## 1. The exact algorithm (certified, no floats anywhere)

At stage `t`, face `S_t = supp(x_t) ∪ supp(d_t)` (`= supp(x_t)` under the
monotone invariant — verified as a safety flag). From the certified rational
Collatz–Wielandt bracket of `i3g_core.face_w_exact` (`k = 8` inverse-iteration
steps, per component), take the **upper** end `ub >= alpha_S` and set

```
q_r    = smallest k/M with (k/M)^2 >= ub/(1-ub),  M = 1000  (q_r <= 1)
beta_t = (1-q_r)/(1+q_r)          (beta_t = 0 when q_r = 1, i.e. ub >= 1/2)
q_r    = q, beta_t = beta          when ub <= alpha  (<=> S_t = V, Lemma A)
```

cache per face; combine with the face-aligned cap (trigger denominator
`Qt_S w`, cap direction `w`). Everything is a Fraction; the per-face
**overdamping certificate** `kappa/(kappa+ub) >= 1 - q_r^2` is asserted at
construction and re-verified: **110/110 faces** (all `fm`/`bm` runs).

**Calibration direction — settled.** The task sheet guessed "a LOWER bound on
`alpha_S` gives a conservative `beta_S`". It is the opposite. Monotone safety
does not involve `beta` (§3), so both directions are *safe*; what `beta_t`
controls is **damping**, and the overdamped side requires
`q_r^2 >= alpha_S/(kappa+alpha_S)` — an inequality certified by an UPPER
bound on `alpha_S` (Lemma C) and violated in general by a lower one (taking
`lo = alpha` reproduces exactly the underdamped configuration I4-A refuted).
Lower end = weaker `q_r` = more momentum = back to oscillation.

## 2. The three lemmas

> **Lemma A (interlacing; classical).** `alpha_S := lambda_min(D_S^{-1/2}
> Qt_S D_S^{-1/2})` is the bottom eigenvalue of a principal submatrix of
> `Q = alpha I + (1-alpha)/2 L_sym` (full-graph degrees), so by
> Cauchy interlacing / Rayleigh restriction `alpha_S >= lambda_min(Q) =
> alpha`. For connected `G` and proper `S` the inequality is strict: a
> restricted minimizer attaining `alpha` would be an `alpha`-eigenvector of
> `Q`, but that eigenspace is `span{D^{1/2} 1} > 0`, which vanishes nowhere.
> The same argument on nested faces gives `S ⊆ S' => alpha_{S'} <= alpha_S`
> (used in §5). **Status: Proved-draft (classical).** Engine: strictness
> certified via the rational CW lower end, `lo > alpha` on **288/288**
> distinct proper faces across all runs.

> **Lemma B (calibration identity — I4-A §6(b), sign corrected).** For
> `kappa = 1-2alpha`, `m_S = kappa/(kappa+alpha_S)`, `q_S^2 =
> alpha_S/(1-alpha_S)`:
> ```
> (1 - q_S^2) - m_S = 2 alpha_S (alpha - alpha_S) / ((1-alpha_S)(kappa+alpha_S)).
> ```
> Hence `m_S >= 1-q_S^2  <=>  alpha_S >= alpha`, equality iff `alpha_S =
> alpha`. I4-A asked to "prove `m_S <= 1-q_S^2`, which reduces to `alpha_S >=
> alpha`" — the displayed inequality is **backwards** (its own P24 numbers,
> `m_S = 0.997861 > 0.997855 = 1-q_S^2`, and its phrase "on the safe side"
> agree with `>=`). Overdamping of the face low mode is `m_S >= 4beta_S/
> (1+beta_S)^2 = 1-q_S^2`, i.e. exactly the `>=` direction, i.e. exactly
> `alpha_S >= alpha` — Lemma A's conclusion. **Status: Proved-draft**
> (cross-multiplication; 200/200 exact random rational substitutions).

> **Lemma C (certified overdamping at rational `q_r`).** If `ub >= alpha_S`,
> `ub >= alpha`, and `q_r^2 >= ub/(1-ub)`, then `m_S >= kappa/(kappa+ub) >=
> 1-q_r^2`, so `z^2 - m_S(1+beta_t) z + m_S beta_t` has real roots.
> *Proof.* `1-q_r^2 <= (1-2ub)/(1-ub)`; apply Lemma B with `alpha_S -> ub`
> to get `kappa/(kappa+ub) >= (1-2ub)/(1-ub)` from `ub >= alpha`; and `m` is
> decreasing in `alpha_S <= ub`. **Status: Proved-draft**; engine 110/110.

> **Lemma D (face floor step).** With `beta = (1-q_r)/(1+q_r)` the exact
> identity `(1+beta) - beta/(1-q_r) = 1/(1+q_r)` (verified 200/200) gives:
> if `m_S >= 1-q_r^2` and `h_t >= (1-q_r) h_{t-1} > 0`, then the N-stage
> low-mode recurrence `h_{t+1} = m_S(1+beta)h_t - m_S beta h_{t-1}` yields
> `h_{t+1} >= (m_S/(1+q_r)) h_t >= (1-q_r) h_t > 0`. **Status: Proved-draft**
> (scalar step). The vector-level floor on the certified `w`-functional is
> the engine check `C10f[q_r]`: **2 330/2 330** same-face stage pairs
> (`fm`+`bm`, all cells, pre- and post-lock), worst ratios strictly above
> `1-q_r`. Under the global calibration the same floor fails wholesale
> (base/face: e.g. 163/378, 164/378 on P24) — L-H repaired by momentum, not
> by the cap, exactly as I4-A predicted.

## 3. Safety-in-beta audit (the legality of the whole move)

The I4-A Safety Theorem involves `beta_t` in **exactly two places**:

* **(b1)** the *same* `beta_t` in the trial `a_t = x_t + beta_t d_t` and in
  the cap `r_i = min(beta_t dh_i, Delta_w w_i)` — case (ii) (`ell_i = x_i`)
  and the monotone half (`r_i <= beta_t dh_i`) are structural in this, not in
  the value;
* **(b2)** `beta_t >= 0` (case (i): `a_i = 0` with `x_i, beta_t dh_i >= 0`;
  at `beta_t = 0` case (i) follows from (H-mono) alone).

Case (iii) (the M-matrix step through `Delta_w`), the supersolution step
(H-Mmat), and (H-pos) never mention `beta`. No hypothesis couples `beta_t` to
`beta_{t-1}`. **Hence the theorem holds verbatim for any stage-varying
`beta_t >= 0`: safety is stage-local in `beta`.** One caveat made explicit:
the *lower* half of the induction (`d_{t+1} >= 0`, the docstring's "hence")
rests on `ell_t >= x_t` plus prox monotonicity through a subsolution property
of the state `x_t`; that invariant does not involve `beta_t` either, but its
maintenance is not re-derived here — it is verified exactly at every stage.
Engine: **68 800/68 800 safety-flag checks (8 flags x 8 600 stages, 24 runs,
0 violations)**, including the new flag `face_eq: S_t = supp(x_t)`.

## 4. The exact results

All exact Fractions. `corr` = stages with `Delta > 0`; `r!=0` = stages with an
actual retraction; `speed` = first `t` with `||x*-x_t||_D^2 <= eps ||x*||_D^2`.

### 4.1 P24 spec cell (q = 1/32, rho = 65/4096, alpha = 1/1025, |S*| = 23; T = 400)

| variant | corr / r!=0 | last | N/C/P/F | C10f matched (post) | od | J_T exact | tface | t@1e-4/8/12 |
|---|---|---|---|---|---|---|---|---|
| base | 16 / 16 | 389 | 384/1/10/5 | 163/378 (134/324) | 0/21 | 1.03597 | 75 | 114/199/301 |
| face (cap only) | 20 / 20 | 373 | 380/5/5/10 | 164/378 (140/329) | 0/21 | 1.07712 | 70 | 116/196/304 |
| **fm (cap+mom)** | **0 / 0** | — | **400/0/0/0** | **378/378 (276/276)** | **21/21** | **0.00000** | 123 | 153/271/387 |
| fmlock (oracle) | 2 / 2 | 52 | 398/0/0/2 | 378/378 (283/283) | 1/21 | 0.30432 | 116 | 147/265/381 |
| bm (base cap+mom) | **0 / 0** | — | 400/0/0/0 | 378/378 (276/276) | 21/21 | 0.00000 | 123 | 153/271/387 |

`bm` (baseline `w = 1` cap, face momentum) also never corrects: **exactly as
I4-A guessed, the decisive ingredient for L-H/absorption is the momentum; the
cap is what repairs L-E** (and it remains necessary for the L-E half of any
proof — under `fm` there are no correcting stages left to test L-E on).

Float mirror, `T = 4800` (Measured): base `J = 17.894`, slope `0.12552`, 244
corrections; face `8.598` / `0.05592` / 151; **fm `0.00000` / `0.00000` / 0**;
fmlock `0.304` / `0.000` / 2 (last `t = 52`). The i2c counterexample-threshold
slope 1 is now 0. Exact word (all-N, 400 stages) agrees with the float
mirror's prefix.

### 4.2 All nine proper-face cells (exact)

`fm`: corrections **0/0 in every cell** — P24 (T=400), P16 (250), P20 (250),
P12 (200), cat5_2 (200), S16 leaf (150), and the new cells P18 endpoint
(q=1/24, rho=11/512, |S*|=17/18, T=200), cat4_3 (q=1/24, rho=9/256,
|S*|=13/16), bt15 root (binary tree, q=1/20, rho=3/64, |S*|=7/15,
`alpha_S/alpha = 51.9`). Matched floor 2 330/2 330; per-face certificates
110/110; `J_T = 0.00000` exactly in all nine. `fmlock`: finite `t_abs` in all
cells — last retraction at t = 52/36/40/32/23/—/41/67/— , `J_T <= 0.317 <
log 2` always. Screening note: P28 (rho=3/256), bt15 leaf-seed and S12
center-seed came out interior (`|S*| = n`) and were excluded.

### 4.3 Regressions

* `fm == base` **bit-identically** (Delta, r, x_{t+1}, beta at every stage)
  on interior-face cells K8 pulse, K2 n=100, K16 unif, Q3 skew — the `ub <=
  alpha` branch (Lemma A makes it exactly the `S = V` case) forces `q_r = q`.
* `knproof2.py` full 140-instance K_n battery: **bit-for-bit the recorded
  state** — 16 predicates at 100 %, `C15 53/54` (the one known published P
  stage), `C13 140/140`, max `J_total 0.36918`, max `t_abs 12`.

### 4.4 Post-lock face machinery (exact; supersedes the buggy in-battery c9face)

The in-battery `c9face` used a wrong quadratic form (`b<Mm v, Mm v>` for
`b<v, Mm v>`); corrected standalone runs (`i5c_c9proj.py` variant, `k = 16`
unrounded `w`):

* **C3face** (N-linearity `e_{t+1} = Mm_S ta_t` on the locked face): 93/93
  (P24), 86/86 (P12), 94/94 (fmlock P24) — **exact**; post-lock the iteration
  *is* the interior face recurrence, no boundary terms.
* **C9face** (V-decay on `w^perp`): P12 **137/137**, worst ratio
  `0.799992 = s_2^S` to 6 digits; P24 **114/114**, worst `0.898543 <
  (1-q_r)^2 = 0.908209`; `V >= 0` 138/138 + 115/115. The K_n V-machinery
  transfers verbatim to the locked face with face constants.

## 5. Re-tuning: the hunted catch, measured exactly — and it telescopes

* **Face changes are bounded**: `S_t = supp(x_t)` is nondecreasing (monotone
  invariant) and `⊆ S*`, so the face chain is monotone with at most
  `|S*|` changes. Engine: chain monotone **8 600/8 600** stage checks;
  changes = 21/12/15/10/6/2/15/6/2 per cell, each `<= |S*|`. Not unbounded.
* **`q_r` is monotone nonincreasing along the chain** (nested faces, Lemma A),
  so `beta_t` only ever increases: observed in every run.
* **Inflation at face changes: none in the working certificate.** `gamma_t = 1`
  exactly at every face-change stage of every `fm` run (no retraction => no
  defect), so `J_T = 0` *including* all re-tuning stages.
* **The re-tuned Lyapunov jump**: at each change, the state-based
  `Phi^{(q_r)} = gapE + (mu(q_r)/2)||z^{(q_r)} - x*||_D^2` was evaluated
  exactly under old and new parameters. Result: across all cells, **every
  downward re-tune has jump < 1** (85/85; it *releases* Lyapunov), and the
  only positive jump is the one-time `t = 1` initialization (global `q` ->
  first face), worth `log-jump = 0.22–2.81` nats per run — a bounded,
  one-time cost, absorbable in O~(.), and an artifact of starting the
  schedule at `q` rather than at the first face's `q_r`. **Measured** (exact
  arithmetic, formula-level choice of `mu(q_r)`); the clean lemma "downward
  re-tunes never inflate" is a conjecture the data supports 85/85.

## 6. What does NOT transfer: the class-spectral hypothesis (honest negative)

Float check (Measured) of the C16-analogue on the locked faces — `s_2^S(2 -
m_2^S) <= (1-q_r)^2`, the F-stage contraction bound that defined the i4a
class: **fails on all six i4a cells** (P24 `0.9101 > 0.9082`, P16 `0.8613 >
0.8575`, P20 `0.8881 > 0.8855`, P12 `0.8365 > 0.8317`, cat5_2 `0.7557 >
0.7500`, S16 leaf `0.1099 > 0.0524`). Equivalently `lam_2^S` sits well below
the `kappa q_r/(1-q_r)` threshold (P24: `0.0114` vs `0.0492`). So a
proper-face absorption theorem **cannot** be the i4a class theorem
instantiated on the face: on these cells absorption (indeed
never-correcting) happens *without* (Hgap_S), consistent with i4a §4.6's
finding that the F-bound is sufficient, not necessary. The N-stage V-decay
`s_2^S <= (1-q_r)^2` *does* hold on the tested cells (§4.4) — it is only the
F-stage certified bound that fails, and `fm` has no F stages.

## 7. Absorption lemma on proper faces — current status and the missing piece

> **Theorem sketch (proper-face absorption, face-calibrated; conditional).**
> Let `S*` be proper, `t >= t_F` with `S_t = S*` and `x_t` interior on `S*`
> (C3face — exact). Take the face-aligned cap and `beta` from §1 (Lemma C:
> overdamped). Then: L-E holds in face geometry at every correcting stage
> (I3-C Perron-truncation lemma — per-stage, `beta`-value-free); the low-mode
> floor holds by Lemma D; N-stage V-decay holds at `(1-q_r)^2` (engine-exact,
> proof = i4a operator identity with face constants); and the K_n absorption
> certificate (S1–S3 with `C_gen, dn_gen, d_min(S), lam_max^S` and trigger
> denominator `Qt_S w`) fires at finite `t_abs` provided **(P)** the P-stage
> closing inequality (the same single Open link as K_n) and **(F)** a bound
> on V-growth at F/C stages replacing (Hgap_S), which fails here (§6).

What the data actually shows is stronger and suggests the right theorem is
different: **under both fixes the safeguard never triggers** (`Delta_t = 0`
for all `t`, 2 550/2 550 exact stages, 9 cells — including the entire
pre-lock phase, where faces change 2–21 times). If provable — e.g. by
showing the trial `a_t` stays a subsolution (`zeta(a_t) >= 0` on `S_t`) under
face-calibrated damping — then (P) and (F) are vacuous on proper faces, and
the Route-B net packing holds with `c = 1` and `B = O(log(1/q))` (the one
initialization jump). That is the sharpest promotion target, and it is a
different (and cleaner) statement than transplanting the K_n absorption
machinery.

**Still needed for a general theorem:** (1) the never-triggering lemma (or,
failing that, an F/C-stage V-bound without (Hgap_S) — i4a §6.3's route);
(2) the downward-re-tune lemma of §5 (jump <= 1, or merely summable);
(3) pre-lock floor bookkeeping across face changes (the floor was verified
across same-face pairs; changes need the §5 jump control); (4) the work
ledger: one certified face solve per distinct face (<= |S*| of them, k = 8
exact triangular solves each) plus the CW bracket (free) and the `M`-grid
square root (O(log M)); (5) honesty about `eps`: everything here is the RPPR
surrogate's inflation ledger (`eps_pg`-side); no claim about `eps_ppr`
output semantics is being made.

## 8. Speed — the trade, measured exactly

Exact stage counts to relative `e2 <= 1e-8` (`1e-12`): P24 base 199 (301) vs
fm 271 (387); P16 125 vs 166; P20 157 vs 213; P12 91 vs 138; cat5_2 71 vs 91;
S16 16 vs 25; P18 161 vs 198; cat4_3 79 vs 102; bt15 27 vs 35. **`fm` is
25–60 % slower on every cell**; `fmlock` nearly identical to `fm`. Causes,
quantified on P24: later lock (`tface` 123 vs 75 — weak early momentum slows
the support sweep; on singleton faces `ub >= 1/2` forces `beta_t = 0`), and
post-lock governing root `z_+ ≈ 0.9619` (not `1-q_S = 0.9537`). Since
`z_+ < sqrt(m_S beta) = 0.9682` (base's modulus), `fm` wins asymptotically,
but not by `T = 4800` (float: t@1e-16 = 503 vs 388). I4-A §3.1's "and is
FASTER" — which was argued from `1-q_S < 1-q` — is **Refuted-draft** as an
iteration-count claim and survives only as the (correct) floor-constant
comparison. The gain purchased is *regularity*: zero inflation, exact
absorption, a floor that holds 100 %.

## 9. Evidence labels

**Proved-draft:** Lemmas A–D (+ engine verification 288/288, 200/200+200/200,
110/110, 2 330/2 330); safety stage-locality in `beta` (§3; 68 800/68 800);
bit-exact interior-face backward compatibility (4/4); C3face exactness
(273/273 across the three checked runs); corrected C9face/V-decay
(251/251, worst = `s_2^S`).
**Measured:** zero-correction behaviour itself (2 550/2 550 exact stages — a
measurement, not yet a lemma); the re-tune jump table (one positive
initialization jump per run; 85/85 downward jumps < 1); the float slope/J
table and face-gap table (§6); asymptotic-root speed analysis.
**Refuted-draft:** I4-A §6(b)'s inequality as written (`m_S <= 1-q_S^2` —
sign backwards, Lemma B); "face calibration is faster" as an iteration-count
claim (§8); (Hgap_S) transfer (§6); lower-CW-end calibration safety (§1).
**Open:** the never-triggering lemma; downward-re-tune lemma; P-stage closing
(unchanged, but vacuous on every `fm` run observed); pre-lock floor across
changes; whether the thin overdamping margins (`m_S` vs `1-q_r^2`, 0.3–0.6 %
on tuned paths) can degenerate on adversarial faces.
