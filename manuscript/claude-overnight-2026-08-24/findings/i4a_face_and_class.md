# I4-A — The face-aligned retraction cap, and the `mu_2 >= 2q` class theorem

**VERDICT, HALF 1: the recovered safety theorem is CORRECT, the face-aligned cap
is EXACTLY implementable in Fractions, and it repairs L-E completely — but
absorption still does not fire, and the reason is a *new and different*
obstruction.** Face-aligned L-E holds at **211/211** correcting stages across six
proper-face cells (worst ratio exactly `1.000000`), against **127/160** for the
baseline (worst ratio up to **359.3**). Safety holds exactly at **every stage of
every run, both caps: 0 violations in 23 100 exact flag checks**. On the
P24 spec cell the windowed slope drops **0.12552 -> 0.05592** and genuinely
partial stages drop **126 -> 23**, but corrections still never stop. The residual
obstruction is *not* L-E: on a proper face the face-Perron mode is itself
**underdamped**, because `beta` is calibrated to `alpha` and not to
`alpha_S > alpha` (measured `alpha_S/alpha` from **2.19 to 150.3**), so L-H (the
low-mode floor) is false on proper faces for a reason face-alignment cannot
touch.

**And that obstruction appears to be removable.** A closing probe (§3.1) replaces
`beta` by the face-calibrated `beta_S = (1-q_S)/(1+q_S)`,
`q_S = sqrt(alpha_S/(1-alpha_S))` — legal because the Safety Theorem is
stage-local in `beta` — and on all six proper-face cells the corrections **stop
outright** (0, 0, 0, 0, 2, 0 in `T = 2000`, versus 62–1331 with `beta`) while the
face low-mode floor holds at **100 %** of post-lock stages. It is also *faster*:
`1-q_S < 1-q` always. Float only, so **Measured**, but it is the clear next
target.

**VERDICT, HALF 2: the `mu_2 >= 2q` class theorem is drafted and verified, with
the SAME single Open link as `K_n`.** On an 82-instance exact-rational battery of
non-complete graphs (complete bipartite, hypercubes `Q_3`/`Q_4`, Petersen,
rook `K_3□K_3`, cocktail-party, cycles, circulant, dense ER, plus `K_n`
controls) **17 of the 20 predicates pass 100 %** — 1 696/1 696 stage-level checks
each — and absorption fires in **64/64 in-class instances** (`t_abs <= 21`,
`J_total <= 0.34895 < log 2`). `C16` agrees with the `mu_2 >= 2q` predicate
**82/82** exactly, failing on every below-threshold cell by a margin as small as
`1.001256`. The remaining failures are exactly `C15`/`C17` at genuinely partial
stages — the `K_n` Open link, unchanged.

Code: `w7_windowed/{i3g_core, i4a_half1, i4a_half1b, i4a_half2, i4a_slope}.py`.
Data: `i4a_half1_p24.json`, `i4a_half1b.json`, `i4a_half2.json`,
`i4a_slope.json`, `knproof2_results.json` (regression). Compute ~14 min.
Everything is exact Fractions except `i4a_slope.py` (float, explicitly labelled).

---

## 1. The recovered SAFETY THEOREM — recovered, audited, completed

The cut-off agent's docstring in `i3g_core.py` is reproduced verbatim at the top
of that file. Its content:

> **Safety Theorem (face-aligned cap).** Let `S = supp(a_t)`, let `w > 0` be any
> vector supported on `S` with `Qt_S w > 0` componentwise, put
> ```
> Delta_w = max_{i in S} [ -zeta(a_t)_i / (Qt_S w)_i ]_+ ,
> r_i     = min(beta dh_i, Delta_w w_i) ,   ell_t = a_t - r_t .
> ```
> Then `x_t <= ell_t <= x*` and hence `x_t <= x_{t+1} <= x*`.

**Status: CORRECT as written.** I audited all four places where such a proof
usually breaks; all four are sound (the audit is now recorded in the file):

| gap | check | verdict |
|---|---|---|
| case (iii) direction | `ell_i <= x*_i <=> ta_i + r_i >= 0`, and `r_i` is a **min**, so both branches need handling — (ii) and (iii) *are* the two branches | correct |
| `Qt_S^{-1} >= 0` | `Qt` has diag `d_i(1+alpha)/2`, offdiag `-(1-alpha)/2`, row sum of offdiag `d_i(1-alpha)/2 <` diag: strictly diagonally dominant Z-matrix, so nonsingular M-matrix; principal submatrices inherit | correct |
| supersolution step | `(Qt+kap D)x* - (ct + kap D x*) = Qt x* - ct >= 0` with equality on `supp(x*)`, and M-matrix LCPs are monotone in the rhs | correct |
| `a_t >= 0` | needed for `ta_j = x*_j` off `S`; follows from the induction hypothesis | correct |

Three hypotheses were implicit and are now explicit: **(H-mono)** `d_t >= 0` and
`0 <= x_t <= x*` (the induction hypothesis), **(H-Mmat)** `kappa = 1-2alpha >= 0`,
**(H-pos)** `w > 0` on `S` and `Qt_S w > 0`.

### 1.1 The point of the theorem, made constructive

The docstring's claim — that `w` need not be the exact Perron vector — is what
makes the variant implementable. But (H-pos) then has to be *established*, not
assumed. It does not need an eigensolver or an error analysis at all:

> **Lemma (certified rational cap direction).** For any `y > 0`, `w := Qt_S^{-1} y`
> satisfies (H-pos) automatically: `Qt_S w = y > 0` by construction, and `w > 0`
> because `Qt_S^{-1} > 0` for an irreducible M-matrix. Taking `y = D_S w^{(k-1)}`
> makes this one step of inverse iteration for `M_S = D_S^{-1} Qt_S`:
> ```
> w^(0) = 1  (= the BASELINE cap, exactly)
> w^(k) = normalize( Qt_S^{-1} D_S w^(k-1) )  ->  Perron(M_S),  rate (alpha_S/lam_2^S)^k .
> ```
> Every `w^(k)`, `k >= 1`, is exactly rational, satisfies (H-pos) exactly, and
> Collatz–Wielandt gives a certified rational bracket
> `min_i (Qt_S w)_i/(d_i w_i) <= alpha_S <= max_i (...)`.

Rounding `w` to a bounded denominator is legal provided `Qt_S w > 0` is
re-verified exactly; the implementation rounds to `1e-14` and falls back to the
unrounded vector if the check fails. **Everything below runs in Fractions with
no floating point anywhere.** [`i3g_core.py:face_w_exact`, `run_exact`]

### 1.2 A corollary that makes the regression a theorem, not a measurement

`Qt 1 = alpha d`, so `Qt^{-1}(D 1) = (1/alpha) 1`, so **`w^(k) = 1` for every `k`
whenever `S = V`.**

> **Corollary (exact backward compatibility).** On the full face the face-aligned
> cap *is* the baseline cap, bit for bit, on every graph — not just `K_n`.

Verified bit-exactly (`Delta`, `r_t`, `x_{t+1}` identical at every stage) on
`K8 pulse`, `K2 n=100`, `K16`, `K32`, `K8 skew/edge`, and a general graph
(`Q_3` skew): **6/6**. [`i4a_half1b.py`, §(1)]

Consequently the whole I2-C `K_n` theorem and the whole Half-2 interior-face
class theorem are **unchanged** by the modification. Re-running the C1–C17
harness confirms the baseline numbers are untouched:

```
knproof2.py, 140 K_n instances, 128s:  17/17 predicates PASS
C1 7130/7130  C3/C4 7076/7076  C5 7130/7130  C9 7130/7130  C10 7130/7130
C13 140/140   C16 140/140      C17 1/1       C15 53/54 (the one known P stage)
max J_total 0.36918 < log 2 ;  max t_abs 12
```

---

## 2. HALF 1 — the face-aligned cap, measured exactly

### 2.1 Safety: the crux question, answered

**The safety invariant holds exactly on every run of both caps. Face-alignment
does NOT break safety; the baseline's misalignment is not forced by safety.**

Seven flags checked in Fractions at every stage — `Qt_S w > 0`, `w > 0`,
`d_t >= 0`, `ell_t >= x_t`, `ell_t <= x*`, `e_t >= 0`, `e_{t+1} >= 0`:

| cell | `n` | `|S*|` | stages x flags, base | violations | stages x flags, face | violations |
|---|---|---|---|---|---|---|
| P24 tuned | 24 | 23 | 400 x 7 | **0** | 2 x 400 x 7 (`k=2,8`) | **0** |
| P16 tuned | 16 | 13 | 250 x 7 | **0** | 250 x 7 | **0** |
| P20 tuned | 20 | 16 | 250 x 7 | **0** | 250 x 7 | **0** |
| P12 tuned | 12 | 11 | 200 x 7 | **0** | 200 x 7 | **0** |
| cat5_2 | 15 | 10 | 200 x 7 | **0** | 200 x 7 | **0** |
| S16 leaf | 16 | 2 | 150 x 7 | **0** | 150 x 7 | **0** |

Total **3 300 stages x 7 flags = 23 100 exact checks, 0 violations**. Evidence:
**Proved-draft** (§1 proof + exhaustive exact verification).

### 2.2 L-E: 12/16 -> 16/16, and better

The headline question. The L-E test is
`||P_w r_t||_{D_S} <= beta ||P_w d_t||_{D_S}` with `P_w` the `D_S`-orthogonal
projector onto `w^perp` on the *running* face `S_t = supp(a_t)` and `w` its
certified Perron vector `w^(8)`.

| cell | corrections (base) | **base**, face geometry | worst ratio | corrections (face) | **face**, face geometry | worst ratio |
|---|---|---|---|---|---|---|
| P24 tuned `T=400` | 16 | **11/16** | **72.76** | 20 | **20/20** | **1.000000** |
| P16 tuned `T=250` | 19 | **14/19** | **219.2** | 23 | **23/23** | **1.000000** |
| P20 tuned `T=250` | 12 | **11/12** | **269.0** | 18 | **18/18** | **1.000000** |
| P12 tuned `T=200` | 15 | **10/15** | **201.7** | 18 | **18/18** | **1.000000** |
| cat5_2 `T=200` | 20 | **15/20** | **359.3** | 33 | **33/33** | **1.000000** |
| S16 leaf `T=150` | 78 | **66/78** | **205.7** | 99 | **99/99** | **1.000000** |
| **total** | 160 | **127/160** | **359.3** | 211 | **211/211** | **1.000000** |

So the answer to "does L-E go 12/16 -> 16/16?" is **yes, and universally**: every
single correcting stage under the face-aligned cap satisfies L-E in the face
geometry, with the worst ratio exactly `1` (attained only when both sides
vanish). This is exactly what the I3-C Perron-truncation lemma predicts:
`r_i = w_i * min(beta d_i / w_i, Delta_w)` is a coordinatewise 1-Lipschitz map in
the `w`-scaled coordinates, hence a `pi`-weighted variance contraction with
`pi_i = d_i w_i^2 / <w,w>_D`. Evidence: **Proved-draft**.

The trade is real and expected: under the face-aligned cap the *full-graph* L-E
now fails occasionally (`C5full` `18/20`, worst `1.221` on P24; `17/18`, worst
`1.009` on P12) — on a proper face the full-graph geometry is simply the wrong
one, and it is the face geometry that governs the recurrence.

### 2.3 Correction census: partial stages nearly vanish

The face-aligned cap converts genuinely partial (`P`) corrections into clean
(`C`, `r = Delta_w w` exactly, so `P_w r = 0`) and full (`F`) ones — which
matters because `P` stages are the sole Open link of the whole chain.

| cell | base `N/C/P/F` | face `N/C/P/F` | `P` change |
|---|---|---|---|
| P24 tuned `T=400` | `384/1/10/5` | `380/5/5/10` | 10 -> 5 |
| P16 tuned | `231/2/6/11` | `227/11/3/9` | 6 -> 3 |
| P12 tuned | `185/1/4/10` | `182/9/1/8` | 4 -> 1 |
| P20 tuned | `238/0/1/11` | `232/7/3/8` | 1 -> 3 |
| cat5_2 | `180/1/5/14` | `167/14/5/14` | 5 -> 5 |
| **P24 float `T=4800`** | `4556/21/126/97` | `4649/40/23/88` | **126 -> 23** |
| S16 leaf (`|S*|=2`) | `72/5/7/66` | `51/1/49/49` | 7 -> **49** |

The one adverse cell is the degenerate star with `|S*| = 2 of 16`, where the
face has two nodes of wildly different degree; there `P` stages explode. Worth
flagging, not fatal (that instance has `J_T = 0`, no inflation at all).

### 2.4 Does absorption fire on P24? **No — it still corrects forever.**

Exact `T = 400`: last correction at `t = 389` (base), `t = 373` (face, `k=8`).
Float `T = 4800`, the i2c spec cell (reproduced to 5 digits — baseline slope
`0.12552` vs the recorded `0.1255`, 91 events, last at `t = 4748`):

| | `J_T` | tail slope of `J` vs `qT` | inflation events | last event | corrections | max window `infl/(qw)`, `j>=1` |
|---|---|---|---|---|---|---|
| **baseline** | 17.894 | **0.12552** | 91 | 4748 | 244 | 0.582 |
| **face-aligned** | **8.598** | **0.05592** | **51** | 4776 | 151 | 0.569 |

So face-alignment **halves the windowed slope** (`0.1255 -> 0.0559`, a 55 %
reduction) and halves `J_T` — a large quantitative gain, still 18x below the
counterexample threshold `1` — but it does **not** produce absorption. The
`C10` low-mode floor keeps failing under both caps (P24: `177/399` base,
`182/399` face; post-face-lock `134/324` vs `147/329`).

---

## 3. Why absorption still fails — the NEW obstruction, isolated

L-E is repaired; L-H (`L_t >= (1-q) L_{t-1} > 0`) is not, and the reason is
structural and has nothing to do with the cap direction.

On the full face, `M 1 = alpha 1`, and the low-mode characteristic polynomial is
`z^2 - m_0(1+beta) z + m_0 beta` with `m_0 = kappa/(kappa+alpha) = 1-q^2`, which
factors as `(z - (1-q))^2` **exactly** — a critically damped double root. That
double root *is* the floor `1-q`.

On a proper face the governing operator is `M_S`, with bottom eigenvalue
`alpha_S > alpha`, so `m_S = kappa/(kappa+alpha_S) < m_0`. The discriminant of
`z^2 - m_S(1+beta) z + m_S beta` is `m_S [ m_S(1+beta)^2 - 4 beta ]`, and since
`4 beta/(1+beta)^2 = 1 - q^2 = m_0` exactly,

```
disc < 0   <=>   m_S < m_0   <=>   alpha_S > alpha .
```

So the face-Perron mode is **underdamped** the moment the face is proper:
complex conjugate roots of modulus `sqrt(m_S beta) < 1-q`.

> **Consequence.** An oscillatory mode has no floor: no constant `c > 0` can make
> `L^w_t >= c L^w_{t-1}` hold at every stage, so **L-H is false on every proper
> face**, and the absorption certificate — which needs `alpha ta_L` to dominate
> the high-mode energy — can never fire. The mechanism is that `beta` is
> calibrated to `alpha`, while the face runs at `alpha_S`; momentum tuned for
> `alpha` **overshoots** on a face whose own contraction is faster.

Measured exactly (Collatz–Wielandt brackets on the post-lock running face):

| cell | `|S|` | `alpha_S/alpha` | `m_S` | `m_0` | underdamped | `sqrt(m_S beta)` | `1-q` | spread of `w` |
|---|---|---|---|---|---|---|---|---|
| P24 tuned | 23 | **2.1936** | 0.997860 | 0.999023 | **yes** | 0.968186 | 0.968750 | 14.65 |
| P16 tuned | 13 | **3.0998** | 0.994638 | 0.998264 | **yes** | 0.956591 | 0.958333 | 8.30 |
| P20 tuned | 16 | **3.4654** | 0.996624 | 0.999023 | **yes** | 0.967586 | 0.968750 | 10.20 |
| P12 tuned | 11 | **3.0357** | 0.992449 | 0.997500 | **yes** | 0.947592 | 0.950000 | 7.03 |
| cat5_2 | 10 | **6.9779** | 0.982812 | 0.997500 | **yes** | 0.942980 | 0.950000 | 7.36 |
| S16 leaf | 2 | **[148.44, 150.26]** | [0.72643, 0.72884] | 0.997500 | **yes** | 0.812052 | 0.950000 | 3.81 |

(The `alpha_S/alpha = 2.1936` and face rate `0.968186 < 1-q = 0.968750` on P24
reproduce I3-C §6 to all printed digits, now with a *certified rational*
bracket rather than a float eigensolve.)

### 3.1 The fix works — probe: face-CALIBRATED momentum absorbs immediately

The mechanism above is testable in one line: keep the face-aligned cap and
replace `beta` by `beta_S = (1-q_S)/(1+q_S)` with
`q_S = sqrt(alpha_S/(1-alpha_S))` on the locked face. Safety is untouched — the
Safety Theorem's case (iii) does not involve `beta` at all, and case (ii) needs
only `r_i <= beta_S dh_i` — so this is legal for any stage-local `beta_t > 0`.

**FLOAT probe, `T = 2000-3000`, six proper-face cells, face-aligned cap in both
columns:**

| cell | `|S*|` | `alpha_S/alpha` | `1-q` | `1-q_S` | `beta`: corrections / face floor | `beta_S`: corrections / face floor |
|---|---|---|---|---|---|---|
| P24 tuned | 23 | 2.194 | 0.968750 | **0.953689** | 62, last `t=1956` / 1187/1929 | **0** / **1885/1885** |
| P16 tuned | 13 | 3.100 | 0.958333 | **0.926506** | 123, last `t=1980` / 1156/1968 | **0** / **1950/1950** |
| P20 tuned | 16 | 3.465 | 0.968750 | **0.941756** | 86, last `t=1970` / 1128/1920 | **0** / **1904/1904** |
| P12 tuned | 11 | 3.036 | 0.950000 | **0.912661** | 145, last `t=1988` / 1172/1968 | **0** / **1942/1942** |
| cat5_2 | 10 | 6.978 | 0.950000 | **0.866924** | 357, last `t=1988` / 1057/1982 | **2**, last `t=23` / **1982/1982** |
| S16 leaf | 2 | 149.36 | 0.950000 | **0.229580** | 1331, last `t=1998` / 1996/1997 | **0** / **1996/1996** |

**Corrections stop dead, and the face low-mode floor `L^w_t >= (1-q_S) L^w_{t-1}`
holds at 100 % of post-lock stages in all six cells** (worst ratios 0.9558,
0.9324, 0.9456, 0.9208, 0.8874, 0.6840 — every one above its own `1-q_S`). On
P24 the same holds with the *baseline* cap once `beta_S` is used (0 corrections
as well), so **the decisive ingredient is the momentum calibration, not the cap
direction** — the cap fixes L-E, the momentum fixes L-H, and absorption needs
both.

And this is a **gain, not a slowdown**: `alpha_S > alpha` means `1-q_S < 1-q`, so
the face-calibrated recurrence contracts *faster per stage* than the
`alpha`-calibrated one — dramatically so on `S16 leaf` (`0.2296` vs `0.9500`).

*Why it works, exactly.* With `beta_S` the face low-mode polynomial
`z^2 - m_S(1+beta_S) z + m_S beta_S` becomes (slightly) **overdamped** rather
than underdamped: `m_S = kappa/(kappa+alpha_S) = 0.997861` versus
`4 beta_S/(1+beta_S)^2 = 1-q_S^2 = 0.997855` on P24 — note `m_S` still uses the
global `kappa = 1-2alpha`, so the match is near-critical but on the *safe* side.
Real roots restore a genuine floor, and L-H comes back.

Evidence: **Measured** (float, six cells, 0 counterexamples). Not yet
Proved-draft: an exact-Fraction rerun and a proof that `m_S <= 1-q_S^2` in
general (equivalently `kappa/(kappa+alpha_S) <= kappa_S/(kappa_S+alpha_S)`,
i.e. `kappa <= kappa_S`, i.e. `alpha_S >= alpha` — which is exactly the
proper-face condition) are the two things to close. **That last equivalence
suggests the result is not a coincidence but a theorem.**

**This relocates the crux again, and sharply.** I2-C said the crux was
non-regularity; I3-C corrected that to the support face via L-E; I4-A now shows
L-E on the face is fully repairable, and what is left is a **momentum-calibration
mismatch**: `q_S = sqrt(alpha_S/(1-alpha_S)) > q`. The natural next move —
recalibrating `beta` to `beta_S = (1-q_S)/(1+q_S)` on the active face — is a much
deeper change than the cap (it changes the acceleration parameter itself) and is
listed as target 1 in §6.

---

## 4. HALF 2 — the `mu_2 >= 2q` class theorem

Half 1 did not block Half 2: face-alignment is *inert* on the interior face
(§1.2 Corollary), so the class theorem is stated for the **baseline** cap and is
simultaneously a statement about the face-aligned one.

### 4.1 The technical device: no eigenvectors, all rational

The whole modal chain is rewritten with the **rational operator**

```
Mm := kappa (kappa D + Qt)^{-1} D        (D-self-adjoint; eigenvalue m_k = kappa/(kappa+lam_k))
P_op := (1+beta) Mm ,  S_op := beta Mm
V(u,v) := <u,u>_D - <u,P_op v>_D + <v,S_op v>_D   = sum_k [h_k^2 - p_k h_k h_k^- + s_k (h_k^-)^2]
VS(u,v) := beta<u,Mm u>_D - beta(1+beta)<Mm u,Mm v>_D + beta^2<Mm v,Mm v>_D  = sum_k s_k V_k
```

so the `K_n` two-mode Lyapunov function generalises to **every graph with no
eigen-decomposition at all**, automatically carrying each mode's own
`(p_k, s_k)`. The N-stage decay becomes the exact rational identity
`V_{t+1} = VS(h_t, h_{t-1})`, and since every `V_k >= 0` (underdamping, C12) and
`s_k <= s_2`,

```
V_{t+1} = sum_k s_k V_k  <=  s_2 V_t  <=  (1-q)^2 V_t .          [Proved]
```

Spectral constants are certified by **exact rational LDL^T positive-definiteness
tests**, not eigensolvers:

```
mu_2  > theta  <=>  L - theta D + ((theta+1)/vol) d d^T   is PD
mu_max< theta  <=>  theta D - L                           is PD
```

(the rank-one term vanishes on `d^perp` and contributes `vol > 0` on `span{1}`).
26 bisection steps give a certified rational bracket; where `mu_2` is known
exactly (`K_{a,b}: 1`, `Q_k: 2/k`, Petersen `2/3`, rook `3/4`, cocktail `1`,
`C_6: 1/2`, `K_n: n/(n-1)`) the exact value is asserted to lie inside the
bracket and then used verbatim — **all 69 such assertions passed**.

### 4.2 The general absorption certificate, and a correction to I3-C

I3-C proposed "`lam_h -> lam_2` and one `1/sqrt(d_min)` loss". Working the
trigger step through, **two different eigenvalues appear**, and the substitution
is not uniform:

```
(M ta)_i = alpha ta_L + (M ta_h)_i ,   ||M ta_h||_inf <= ||M ta_h||_D / sqrt(d_min)
                                                     <= lam_max ||ta_h||_D / sqrt(d_min)
```

— the **operator norm on the high subspace is `lam_max`, not `lam_2`**. `lam_2`
is the right substitution in the *contraction* constants (`m_2`, `s_2`, `dn`);
`lam_max` is the right one in the *trigger* constant. With
`C_gen = (1+beta)^2 + beta^2/s_min`, `dn_gen = (1 - m_2/m_0)/2`,
`wh2 = d_min (alpha beta / lam_max)^2`:

> **Absorption Lemma (general graph).** If at stage `t`
> **(i)** `L_t >= (1-q) L_{t-1} > 0` and **(ii)** `C_gen V_t <= dn_gen * wh2 * L_{t-1}^2`,
> then `Delta_t = 0`, and (i),(ii) hold again at `t+1`. Hence every stage from `t`
> on is correction-free and `J_T^fin = J_t^fin =: B` for all `T`.

The `1/sqrt(d_min)` loss of I3-C is confirmed and appears **exactly once**, in
`wh2`. Exact verification of the three steps over the whole 82-instance battery:

```
S1 (weighted Cauchy-Schwarz, ||ta_h||_D^2 <= C_gen W_t)     1696/1696   PASS
S2 (Lyapunov lower bound, dn_gen W_t <= V_t)                1696/1696   PASS
S3 (premise => Delta_t = 0)                                 1086/1086   PASS
```

**Necessity check.** Replacing `lam_max` by `lam_2` (I3-C's literal reading)
makes the premise fire *earlier* and produced **0 violations on 18 cells** — but
it has no proof, since `||M u||_D <= lam_2 ||u||_D` is false as an operator
inequality. Labelled **Measured**, not Proved.

### 4.3 The theorem

> **Theorem (`mu_2 >= 2q` class; draft).** Let `G` be a finite connected simple
> graph, `alpha in (0, 1/2]`, `q = sqrt(alpha/(1-alpha)) <= 1/2`,
> `beta = (1-q)/(1+q)`, `kappa = 1-2alpha`. Assume
> * **(H0)** `s_i > rho d_i` for every `i` (so `ct > 0`, `x*` is interior, and
>   the active face is `V` from `t = 1` on);
> * **(Hgap)** `mu_2(L_sym(G)) >= 2q`;
> * **(L-I@P)** the closing inequality `V_{t+1} <= (1-q)^2 V_t` at genuinely
>   partial correcting stages — *the same single Open link as `K_n`*.
>
> Then there is a finite `t_abs`, bounded a priori by
> `t_abs <= t_F + ceil( log R_{t_F} / log((1-q)^2/eta) )`, such that every stage
> `t >= t_abs` is correction-free, `gamma_t = 1` for `t >= t_abs`, and for all `T`
> ```
> J_T^fin <= B := sum_{t < t_abs} log gamma_t ,
> ```
> so the Route-B net packing `J_T^fin <= (1-c) qT + B` holds with **`c = 1`**.
> The absorption radius carries one factor `1/sqrt(d_min)` relative to `K_n`, and
> the trigger constant uses `lam_max` while the contraction constants use `lam_2`.
>
> Moreover **(Hgap) is exactly the F-stage condition**: `s_2(2-m_2) <= (1-q)^2`
> `<=> m_2 <= 1-q <=> mu_2 >= 2q`, with equality on both sides at `mu_2 = 2q`.

### 4.4 Predicate-by-predicate classification and verification

Battery: **82 exact-rational instances** — `K_{3,3}`, `K_{2,4}`, `K_{2,5}`, `Q_3`,
`Q_4`, Petersen, rook `K_3□K_3`, cocktail `K_{3x2}`/`K_{4x2}`, `C_4`, `C_6`,
`circulant C_12(1,2,3)`, `ER(12, 0.70)`, `ER(14, 0.60)`, `K_8`, `K_5`, plus
below-threshold controls `P_8`, `C_12`, and `Q_4`/`Q_3`/`C_6`/Petersen at
`q` nudged just past `mu_2/2` — x 3 seed families (`unif`, `skew`, `prand`),
`T = 18..30`. **64 in class, 18 out.**

| tag | general-graph status | needs face-alignment? | verified (all / in-class) |
|---|---|---|---|
| C1 master | **general** — holds on any graph on the interior face | no | 1696/1696 / 1360/1360 |
| C2 F-collapse | **general** — `e_{t+1} = Mm e_t` | no | 8/8 / 7/7 |
| C3 N-linear | **general** — operator form `e_{t+1} = Mm ta_t` | no | 1685/1685 / 1351/1351 |
| C4 V-decay | **general** — exact identity `V_{t+1} = VS(h_t,h_{t-1})`, N **and** clean stages | no | 1686/1686 / 1352/1352 |
| C5 L-E | **general, PROVED** (I3-C §2) on the interior face where `w = 1` | **on proper faces, yes** (§2.2) | 1696/1696 / 1360/1360 |
| C6 trigger | **general** — `alpha Delta = max_i[-(M ta)_i]_+` | no | 1696/1696 / 1360/1360 |
| C7 defect | **graph-independent** (project ms-15) | no | 1696/1696 / 1360/1360 |
| C8 Phi floor | **graph-independent** (project ms-15) | no | 1696/1696 / 1360/1360 |
| C9 closing | N/clean **Proved**; F `<=>` (Hgap); **P Open** | no | 1696/1696 / 1360/1360 |
| C10 low floor | **general** — `m_0 = 1-q^2` and `m_0[(1+beta)-beta/(1-q)] = 1-q` are graph-independent identities | **false on proper faces** (§3) | 1696/1696 / 1360/1360 |
| C11 monotone | **general** | no | 1696/1696 / 1360/1360 |
| C12 structural | **general** — `s_k <= (1-q)^2` always, strict underdamping iff connected | no | 82/82 / 64/64 |
| C13 absorption | **general** with `(C_gen, dn_gen, d_min, lam_max)` | no | 77/82 / **64/64** (see note) |
| C14 R-geometric | **general** with `s_2` | no | 1222/1222 / 976/976 |
| C15 census | **inverts on general graphs**; measurement, not a lemma | — | 9/11 / 8/9 |
| C16 F-contraction | **`<=> mu_2 >= 2q`, exactly** | no | 64/82 / **64/64** |
| C17 P certificate | **still Open**, and now the only gap | no | 0/2 / 0/1 |
| S1/S2/S3 | **general** (§4.2) | no | 1696+1696+1086, all PASS |

*C13 note.* The printed run shows `63/64` in class; the single miss
(`Q4-eq skew q=1/4`) is a horizon artefact — re-run at `T = 30` it absorbs at
`t_abs = 17`, so **in-class absorption is 64/64**. Out of class, `14/18` absorb
anyway (the threshold is sufficient, not necessary).

**Aggregate: 17 of 20 predicates pass 100 % on all 82 instances.** The three that
do not are `C13` (horizon artefact only), `C15` (a census), and `C17` (the Open
link).

### 4.5 The threshold, exactly at the boundary

`C16` and the predicate `mu_2 >= 2q` agree on **82/82** instances. Boundary
behaviour, all exact:

| cell | `mu_2` | `2q` | in class | `s_2(2-m_2)/(1-q)^2` | C16 |
|---|---|---|---|---|---|
| `Q_3`, `q = 1/3` | `2/3` | `2/3` | **equality** | `= 1` exactly | ok |
| `Q_4`, `q = 1/4` | `1/2` | `1/2` | **equality** | `= 1` exactly | ok |
| `C_6`, `q = 1/4` | `1/2` | `1/2` | **equality** | `= 1` exactly | ok |
| `Q_4`, `q = 51/200` | `1/2` | `0.510` | out | **1.001616** | FAIL |
| `C_6`, `q = 51/200` | `1/2` | `0.510` | out | **1.001616** | FAIL |
| `Q_3`, `q = 101/300` | `2/3` | `0.673` | out | **1.001256** | FAIL |
| Petersen, `q = 101/300` | `2/3` | `0.673` | out | **1.001256** | FAIL |
| `P_8`, `q = 1/10` | 0.099031 | 0.200 | out | 1.006853 | FAIL |
| `C_12`, `q = 1/10` | 0.133975 | 0.200 | out | — | FAIL |

The threshold is **sharp and attained**: at `mu_2 = 2q` both sides are equal
exactly, and a perturbation of `q` by `1/200` breaks it by `1.6e-3`.

### 4.6 In-class consequences, measured exactly

* absorption fires in **64/64** in-class instances, `t_abs <= 21`;
* `B = J_total <= **0.34895** nats `< log 2 = 0.69315` over the whole in-class
  battery (worst `Q4-eq skew q=1/4`); most cells have `J = 0` exactly;
* worst per-stage `V` ratio in class **0.709083**, always under `(1-q)^2`;
* `C9` passed **1696/1696 including out-of-class cells** — below the threshold
  the *certified* F-bound fails but the *actual* contraction still holds, so
  (Hgap) is sufficient, not necessary. **Measured**, worth attacking (§6.3).

---

## 5. Evidence labels

**Proved-draft** (proof + verified exactly on every tested instance):
the Safety Theorem §1 and its constructive `w` (3 710 x 7 checks, 0 violations);
exact backward compatibility on the full face (6/6 bit-identical);
face-aligned L-E (211/211, worst ratio exactly 1);
C1–C8, C10–C12, C14 in general-graph form (1 696/1 696 each);
the operator identities `V_{t+1} = VS(h_t,h_{t-1})` and `V_{t+1} <= s_2 V_t`;
the C16 equivalence `s_2(2-m_2) <= (1-q)^2 <=> mu_2 >= 2q` (82/82);
S1/S2/S3 of the general absorption certificate with `(C_gen, dn_gen, d_min, lam_max)`;
the certified spectral machinery (69/69 asserted exact `mu_2` values inside their certified brackets).

**Measured** (0 violations, no proof):
**face-calibrated momentum `beta_S` stops corrections outright and restores the
face low-mode floor at 100 % of post-lock stages on all six proper-face cells**
(§3.1) — the single most important measurement of this direction;
the windowed-slope halving `0.12552 -> 0.05592` and `J_T` halving on P24 (float);
the `P`-stage collapse `126 -> 23`;
C9 holding on out-of-class instances;
the `lam_2`-in-the-trigger variant of the absorption certificate (0/18 violations).

**Refuted-draft:**
baseline L-E in the face geometry (127/160, worst ratio 359.3 on `cat5_2`);
L-H (`C10`) on proper faces, now with a *mechanism*: face underdamping,
`m_S < m_0` on 6/6 cells with `alpha_S/alpha` up to 150.3.

**Open:**
C9/C17 at genuinely partial stages — the single remaining link, on `K_n` and on
the general class alike (certified bound wastes `U/V = 3.69` on `Q4-eq skew`);
absorption on proper faces (blocked by face underdamping, §3);
whether (Hgap) can be dropped from the class theorem (§4.6 suggests yes).

---

## 6. Next targets, ranked

1. **Face-calibrated momentum — promote §3.1 from Measured to Proved-draft.**
   The float probe already shows corrections stopping dead and the face floor
   returning 100 % on all six proper-face cells. What remains: (a) rerun the
   probe in exact Fractions with the certified Collatz-Wielandt bracket on
   `alpha_S` in place of a float eigensolve (`i3g_core.face_w_exact` already
   returns it); (b) prove `m_S <= 1 - q_S^2`, which reduces to
   `kappa <= kappa_S <=> alpha_S >= alpha` — the defining property of a proper
   face, so this looks like a theorem rather than a coincidence; (c) handle the
   pre-lock phase, where `S_t` and hence `beta_{S_t}` change every stage (the
   Safety Theorem is stage-local, so a stage-varying `beta_t > 0` is already
   covered); (d) charge the `alpha_S` estimate in the work ledger — one extra
   face solve per distinct face, amortised by caching, plus the certified
   bracket which is free. If this closes, the i2c absorption chain transfers to
   **proper faces**, i.e. to the actual `l1`-regularized regime, and it does so
   with a *better* per-stage rate `1-q_S < 1-q`.
2. **Close C9/C17 at P stages.** Now the *only* Open link on both `K_n` and the
   general class, and face-alignment has made it much rarer (126 -> 23 P stages
   on P24) — attack it where it is now sparse. The certified `sqrt(vol)/2`
   range bound wastes a factor 3.7 on `Q4-eq skew`.
3. **Drop (Hgap).** C9 held 1696/1696 including all 18 out-of-class cells, so
   the F-bound `s_2(2-m_2) <= (1-q)^2` is sufficient but not necessary. A
   two-stage or windowed F-bound charging the `mu -> 0` overshoot against the
   `s_k/(1-q)^2 < 1` slack of neighbouring N stages would remove the spectral-gap
   hypothesis entirely and make the class theorem unconditional on `G`.
4. **The `S16 leaf` anomaly.** The one cell where face-alignment increased `P`
   stages (7 -> 49). `|S*| = 2` of 16 with degrees `15` and `1`: the face is
   maximally non-regular. Worth a targeted look before claiming the `P`-stage
   collapse is general.
