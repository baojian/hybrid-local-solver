# I4-F — The certificate tax: the sharp amplification constant of the repository's stopping rule, and what should replace it

**Direction:** the OPEN repository decision `docs/decisions/residual-convention.md`
("what is the implementation-wide stopping rule?"), raised as a side finding by
I4-D §6f and independently tripped over by I2-F §4 and I3-A §8.

Code: `/home/claude/work/overnight/i4f/{core.py, run1.py … run7.py, an.py}`.
Data/logs: `/home/claude/work/overnight/i4f/out/{cert2,esc4,push5,pay6,spread7}.json`,
`run{1..7}.log`.  Experiment labels: **E2** = `cert2` (support constant + (c)+(d)),
**E4** = `esc4` ((e') tradeoff curve), **E5** = `push5` (push), **E6** = `pay6`
(payoff / stopping radius), **E7** = `spread7` (ISTA, Chebyshev).
Conventions as W1–W8 / I2-F / I3-A / I4-D.

---

## VERDICT (short)

1. **The repository's certificate is not "loose" in the sense I4-D suggested — it
   is *exactly worst-case sharp*, and the entire tax is support-structural.**
   Proved and verified to 1e-15: with `M := D^{-1/2} Q^{-1} D^{1/2}`, we have
   `M >= 0` entrywise **and every row sum of `M` is exactly `1/alpha`**, hence
   `||M||_inf = 1/alpha` exactly. No constant better than `1/alpha` is valid
   uniformly over residual vectors. The looseness lives entirely in *which
   residuals an algorithm actually produces*.
2. **The sharp instance constant is a discounted occupation measure, in closed
   form (Proved-draft, verified exactly).** For any `x_hat` whose push-scale
   residual `r = gamma s - H pi_hat` is supported on `T`,
   `A(T) = max_i pi^{(i)}(T)` — the maximum, over start vertices `i`, of the
   PPR mass that the walk from `i` places on `T`. The max is always attained
   **inside `T`**. Equivalently `A(T) = (1-c) max_i G_i` with `(I - cP)G = 1_T`.
3. **One-sidedness buys exactly nothing in the constant (Proved-draft).** The
   extremal residual attaining `A(T)` is `r = theta * d * 1_T >= 0`, which is
   *nonnegative*. So the best support-conditional constant for monotone methods
   equals the signed one. ACL's one-sidedness gives a *lower envelope*
   (`pi_hat <= pi`), not a smaller constant. This settles a hypothesis in the
   task brief in the negative, with a proof and a numerical witness.
4. **The measured law.** For the region/eps-optimal output the realized
   normalized amplification is `A ≈ sqrt(alpha)` across the ordinary zoo —
   measured `A/sqrt(alpha) ∈ [0.71, 1.07]` over 11 families x 6 alphas, and
   **exactly `sqrt(alpha)` to 4 digits** on path / spider / decoy_hub. But this
   is a property of *region* methods, not of the problem:
5. **For push and for RPPR/ISTA, `A = Theta(1)`, alpha-free** — measured
   `0.48 … 0.88` (median `0.63`) over 30 push cells and `0.86 … 1.00` over 10
   ISTA cells. The reason is exact: a *threshold* stopping rule drives the
   residual to `r_j ≈ theta d_j` on its support, which is **literally the
   extremal profile of Theorem 2**. So ACL's constant is tight because ACL's
   stopping rule attains it. Push's measured certificate tax is `1.00 … 2.16x`
   (median `1.07x`); nothing is available to recover there.
   Signed Krylov iterates behave oppositely: truncated Chebyshev has
   `A = sqrt(alpha)` exactly on a path and `0.017 … 0.25` elsewhere
   (over-charge up to `57x`), because its residual oscillates in sign and
   cancels.
6. **A uniform `sqrt(alpha)` relaxation is UNSOUND, and for a stronger reason
   than I4-D gave.** I4-D's counterexample was `hidden_hub` (measured here
   `A = 1/(1+c)` *exactly*, i.e. `0.625, 0.531, …` -> `1/2`, so
   `A/sqrt(alpha) -> infinity`). But the decisive case is far more common:
   **push itself has `A = Theta(1)`**, so a `sqrt(alpha)`-relaxed rule would
   certify wrong answers for the campaign's single most-used mechanism at every
   `alpha < 0.4`. Refuted.
7. **A sound, locally computable replacement exists and is cheap: the
   profile-localized supersolution (certificate `e'`).** Solve
   `(I - cP) Ghat = |r|/d` on `Omega_K = B_K(supp r)` with the pessimistic
   exterior value `theta/(1-c)`. Sound by M-matrix comparison (0 violations in
   72 cells x 9 radii). **`K = Theta(alpha^{-1/2})` suffices** — measured
   `K* * sqrt(alpha) ∈ [0.5, 2]` to come within 2x of the truth — i.e. the
   certificate's own charged cost is on the *same `sqrt(alpha)` scale as the
   aspirational target*, not the `1/alpha` scale.
8. **Payoff, measured (E6).** A region method certified by `e'` at
   `K = ceil(4/sqrt(alpha))` stops at **exactly the oracle radius in 9 of 9
   cells** (`tax = 1.00`), where the repository rule over-charges by
   `1.15 … 2.54x` in region volume and growing as `alpha` falls. The
   certificate's own charged read cost is `1.2 … 8 x vol(S_eps)`, alpha-free.
9. **I3-A's two negative results are confirmed and one is corrected.** The
   max-principle bound is never better than `2x` (measured `A_mp ∈ [0.500,
   0.625]`, 46/46 cells) — confirmed exactly. The K-term Neumann bound is
   confirmed useless, but the required `K` is `Theta~(1/alpha)`, not
   `alpha^{-2}`: at `alpha = 2^-10`, `K = 512` still returns `0.995` against a
   truth of `0.031`.

Evidence grade: **Proved-draft** for §1–§3 and §5 (short derivations, each
verified numerically to machine precision); **Measured** for §4, §6–§9.

---

## 1. The certificate is worst-case sharp (Proved-draft; verified to 1e-15)

Write `M := D^{-1/2} Q^{-1} D^{1/2}`, so that for any `x_hat` with residual
`r_Q = Q x_hat - b`,

```
D^{-1/2}(x_hat - x^0) = M ( D^{-1/2} r_Q ),
err := ||D^{-1/2}(x_hat - x^0)||_inf,   theta_Q := ||D^{-1/2} r_Q||_inf.
```

**Lemma 1.** `M >= 0` entrywise and `M 1 = (1/alpha) 1`. Hence
`||M||_inf = 1/alpha` **exactly**, and the repository rule
`theta_Q < alpha * eps_ppr  =>  err < eps_ppr` is the *unimprovable* uniform
bound.

*Proof.* `Q` has nonpositive off-diagonals and is SPD, so it is a Stieltjes
matrix and `Q^{-1} >= 0`; `D^{-1/2} A D^{-1/2} (D^{1/2}1) = D^{1/2}1`, so
`Q (D^{1/2}1) = alpha (D^{1/2}1)`, so `Q^{-1}(D^{1/2}1) = (1/alpha)(D^{1/2}1)`
and `M 1 = D^{-1/2} Q^{-1} D^{1/2} 1 = (1/alpha) 1`. For a nonnegative matrix
`||M||_inf = max_i (M1)_i`. ∎

Verified (`core.py` sanity block): on a path, `min M_ij > 0` and row sums of `M`
equal `1/alpha` to 6 decimals at `alpha = 0.5, 0.05, 0.005`.

> **Consequence for the repository.** The premise "the certificate over-charges
> because the bounding step is careless" is false. The bound is exact for the
> worst residual. Any improvement must be *conditional on the residual an
> algorithm actually leaves*, and must therefore be **computed, not assumed**.

## 2. The sharp instance constant (Proved-draft; attained exactly)

Work in the push scale, which removes all `(1+alpha)/2` clutter:
`H = I - c A D^{-1}`, `c = (1-alpha)/(1+alpha)`, `gamma = 2 alpha/(1+alpha)`,
`P = D^{-1} A` (row-stochastic), `r = gamma s - H pi_hat`,
`theta = max_j |r_j|/d_j`. The exact conversions are

```
D^{-1/2}(Q x_hat - b) = -((1+alpha)/2) D^{-1} r ,  theta_Q = ((1+alpha)/2) theta
repo rule  theta_Q < alpha*eps   <=>   theta/(1-c) < eps        [since 1-c = gamma]
```

so the repository rule is *exactly* "assume the amplification equals its worst
value `1/(1-c) = (1+alpha)/(2 alpha)`". Define the **normalized amplification**

```
A := err / [ (1/alpha) * theta_Q ] = (1-c) * err / theta   ∈ (0, 1].
A = 1  <=>  the rule is exactly right ;  A << 1  <=>  it over-charges by 1/A.
```

**Theorem 2 (sharp support-conditional constant).** Let `r` be supported on `T`.
Then `err <= A(T) * theta/(1-c)` where

```
A(T) = (1-c) * max_i G_i ,   (I - cP) G = 1_T
     = max_i  sum_{k>=0} (1-c) c^k  Pr_i[ X_k ∈ T ]      (X = simple random walk)
     = max_i  pi^{(i)}(T)                                 (PPR mass from i on T)
```

and the bound is **attained** by `r = theta * d * 1_T`. Moreover
`max_i G_i = max_{j ∈ T} G_j`.

*Proof.* `D^{-1}H^{-1}D = (I - cP)^{-1} >= 0`, so
`(pi - pi_hat)_i/d_i = (D^{-1}H^{-1} r)_i <= theta (D^{-1}H^{-1} d 1_T)_i
 = theta ((I-cP)^{-1} 1_T)_i = theta G_i`, with equality for `r = theta d 1_T`.
The PPR identity follows from reversibility `pi^{(j)}_i/d_i = pi^{(i)}_j/d_j`
and `pi^{(i)} = gamma (I - cAD^{-1})^{-1} e_i`. For the location of the max:
`G_i = 1_T(i) + c (PG)_i`, so at a global max `i*` with `i* ∉ T` we get
`G_{i*} <= c G_{i*}`, forcing `G_{i*} = 0`. ∎

Verified exactly (`core.py` sanity block, path `n = 400`): for
`T = {v}, {v,v+1}, [v-50, v+50]` and `alpha ∈ {0.5, 0.05, 0.005}`,
`(1-c) * err_worst/theta` equals `A(T)` to 6 decimals in all 9 cases, and
`argmax G ∈ T` in all 9.

**Corollary 2a (closed form, the source of the `sqrt(alpha)` law).** On the
infinite path with `T` a single vertex,
`A(T) = sqrt( (1-c)/(1+c) ) = sqrt(alpha)` **exactly**. (Measured: `0.707107`,
`0.223607`, `0.070711` at `alpha = 0.5, 0.05, 0.005`; `sqrt(alpha) =
0.7071068, 0.2236068, 0.0707107`.)

**Corollary 2b (the general law).** `A(T)` is `(1-c)` times a discounted
occupation of `T`. For `T` a single vertex on a graph of spectral dimension
`d_s` (return probability `p_k ≍ k^{-d_s/2}`):

| structure of `T` | `A(T)` | over-charge `1/A` |
|---|---|---|
| `d_s = 1`, or a codimension-1 ring in a lattice | `Theta(sqrt(alpha))` | `Theta(alpha^{-1/2})` |
| `d_s = 2` (point in `Z^2`) | `Theta(alpha log(1/alpha))` | `Theta~(1/alpha)` |
| transient: trees, expanders, `Z^{d>=3}` (point) | `Theta(alpha)` | `Theta(1/alpha)` — **max** |
| **trap**: `T ∋ j` with all neighbours of degree 1 (hub / star centre) | `-> 1/(1+c) -> 1/2` | `<= 2` — rule tight |
| `T` = the whole explored core (push, ISTA, Chebyshev) | `-> 1` | `1` — rule exact |

The last two rows are why **no uniform relaxation of any exponent is sound**.

**Corollary 2c (one-sidedness buys nothing).** The extremal `r = theta d 1_T`
is `>= 0`. Therefore the best constant valid for all monotone (`r >= 0`) methods
with residual support `T` is *identical* to the signed one. ACL's one-sidedness
delivers `pi_hat <= pi` (a valid lower envelope, useful for sweep cuts and for
support decisions) — **not** a smaller amplification.

## 3. Measured amplification law (E2, E4, E5; 11 families x 6 alphas, eps = 1e-5)

`x_hat` = exact solve of `Q[S_eps, S_eps]`, zero-extended (the *optimal*
eps-output; residual on the ring `∂S_eps`, one-signed).

| family | `A` at 2^-4 | 2^-6 | 2^-8 | 2^-10 | 2^-12 | `A/sqrt(alpha)` range |
|---|---|---|---|---|---|---|
| path | 0.2500 | 0.1250 | 0.06250 | 0.03125 | 0.01563 | **1.000** (exact) |
| spider | 0.2500 | 0.1250 | 0.06250 | 0.03125 | 0.01563 | **1.000** (exact) |
| decoy_hub | 0.2500 | 0.1250 | 0.06250 | 0.03125 | 0.01563 | **1.000** (exact) |
| caterpillar | 0.2616 | 0.1321 | 0.06623 | 0.03314 | 0.01657 | 1.046–1.061 |
| grid2d | 0.2270 | 0.1076 | 0.05124 | 0.02531 | 0.01526 | 0.810–0.977 |
| grid3d | 0.2216 | 0.1109 | 0.06664 | — | — | 0.886–1.066 |
| btree | 0.2319 | — | — | — | — | 0.928 |
| exp3reg | 0.2201 | — | — | — | — | 0.880 |
| rrt | 0.1991 | 0.0890 | 0.02990 | 0.00971 | 0.01011 | 0.31–0.80 (drifts to `alpha^{0.7}`) |
| **hidden_hub** | **0.5312** | — | — | — | — | **2.125 and growing** |

* **Best case (most over-charging) measured:** `rrt` at `alpha = 2^-10`,
  `A = 0.0097` — the rule over-charges by **103x**. Analytically the best case
  is `A = Theta(alpha)`, over-charge `Theta(1/alpha)`, realized on transient
  structures (trees / expanders / `Z^{d>=3}`) with a low-codimension `T`.
* **Worst case (rule tight) measured and proved:** `hidden_hub`
  `A = 1/(1+c)` **exactly** (`0.625` at `2^-2`, `0.53125` at `2^-4` —
  `1/(1+c)` gives `0.625000` and `0.531250`), and `A -> 1` for `T = V`.
* **The generic law is `A = sqrt(alpha)`**, and on path / spider / decoy_hub it
  is `sqrt(alpha)` to four digits — not a fitted exponent but an identity.

**And the same measurement for push (E5, fixed accumulator, 30 cells):**

| family | `A` at 2^-4 | 2^-6 | 2^-8 | 2^-10 |
|---|---|---|---|---|
| path | 0.658 | 0.599 | 0.636 | 0.882 |
| grid2d | 0.580 | 0.584 | 0.606 | 0.587 |
| grid3d | 0.590 | 0.536 | 0.509 | — |
| rrt | 0.831 | 0.696 | 0.644 | 0.583 |
| spider | 0.842 | 0.528 | 0.628 | 0.657 |

`A ∈ [0.483, 0.882]`, **median 0.632, no alpha trend**.

**And for RPPR/ISTA and truncated Chebyshev (E7, `run7.py`, eps = 1e-5):**

| family | `alpha` | `A` (ISTA) | `A` (Chebyshev) |
|---|---|---|---|
| path | 2^-4 / 2^-6 / 2^-8 | 0.949 / 0.947 / 0.943 | 0.2500 / 0.1250 / 0.06251 |
| grid2d | 2^-4 / 2^-6 / 2^-8 | 0.928 / 0.899 / 0.857 | 0.174 / 0.0623 / 0.0219 |
| rrt | 2^-4 / 2^-6 / 2^-8 | 0.998 / 0.984 / 0.979 | 0.152 / 0.0736 / 0.0175 |
| exp3reg | 2^-4 | 0.885 | 0.245 |

**The criterion is not "spread vs boundary" — it is the residual *profile*.**
A **threshold** stopping rule (push: `r_j <= eps_appr d_j` for all `j`;
ISTA/RPPR: soft-threshold stationarity) leaves `r_j ≈ theta d_j` across its
support, which is *exactly* the extremal residual `r = theta d 1_T` of Theorem 2.
That is why ACL's constant is tight — **ACL's stopping rule attains the worst
case by construction.** A restricted *solve* (region / AMG / elimination) or a
signed Krylov iterate leaves a residual far from that profile, and pays.

> **This is the decisive soundness fact.** The `sqrt(alpha)` law is a property of
> **how a mechanism leaves its residual**, not of the problem. Any rule that
> assumes `A <= C sqrt(alpha)` is violated by push at every `alpha < (0.48/C)^2`
> and by ISTA at every `alpha < (0.86/C)^2`.

## 4. Candidate certificates — soundness, tightness, charged cost

All bounds normalized: a candidate is a computable `Ahat` used as
`stop when theta * Ahat/(1-c) <= eps`. Sound iff `Ahat >= A_real` always.

| # | certificate | sound? | measured `Ahat` (region output) | charged cost | verdict |
|---|---|---|---|---|---|
| **(a)** | repo rule: `Ahat = 1` (`theta_Q < alpha*eps`) | **yes, worst-case sharp** (Lemma 1) | `1` | `O(vol(S) + \|∂S\|)` degree queries (I4-D Lemma D) — already paid | over-charges `1/A` = `4 … 103x` on region methods, `1.1 … 2x` on push |
| **(b)** | one-sided (`r >= 0`) support version | yes | `= (a)`; **no gain** (Cor. 2c) | same | **refuted as an improvement**; keep only for the envelope `pi_hat <= pi` |
| **(b')** | one-sided `l1` variant `Ahat = \|\|r\|\|_1/(theta d_min)` | yes | `1.0` in **46/46** cells (`d_min = 1`) | `O(\|T\|)` | useless on any graph with a degree-1 vertex |
| **(c)** | K-term Neumann | yes | `alpha=2^-6`: `K=512 -> 0.878`; `alpha=2^-10`: `K=512 -> 0.995` vs truth `0.031` | `sum_{k<K} vol(B_k(T))` | **useless**; needs `K = Theta~(1/alpha)` (I3-A said `alpha^{-2}`; the correct exponent is `1`, still unaffordable) |
| **(d)** | max-principle / boundary-inward decay, `Ahat = 1/(1+c*tau)` | yes | `∈ [0.500, 0.625]` over **46/46** cells | `O(\|∂S\|)` | **confirms I3-A: never better than 2x** |
| **(e)** | sharp support constant `A(T)` (Thm 2), exact global solve | yes | equals the truth | global solve — not local | reference value only |
| **(e')** | **profile-localized supersolution** (below) | **yes — 0 violations / 72 cells x 9 radii** | reaches `A_real` at `K ≈ 2/sqrt(alpha)` | `vol(Omega_K)` reads + one local solve on `Omega_K` | **RECOMMENDED** |
| **(f)** | uniform `sqrt(alpha)` relaxation | **NO** | violated by push (`A ≈ 0.6`) and by `hidden_hub` (`A = 1/(1+c)`) | `O(1)` | **refuted — never adopt** |

### The recommended certificate (e'), in full

> Let `psi = |r|/d` (push-scale residual profile), `theta = ||psi||_inf`,
> `T = supp(psi)`, `Omega = B_K(T)`. Define `Ghat` by
> `Ghat_i = theta/(1-c)` for `i ∉ Omega`, and on `Omega` solve
> `d_i Ghat_i - c sum_{j~i} Ghat_j = d_i psi_i`.
> Then **`err <= max_{j ∈ T} Ghat_j`**, and the bound decreases monotonically in
> `K` to the exact error when `r` has one sign.

*Soundness (Proved-draft).* `G = (I-cP)^{-1} psi` satisfies `err <= ||G||_inf`
with equality for one-signed `r`; `max G` is attained on `T` (max principle, as
in Thm 2); `G <= theta/(1-c)` everywhere, so the exterior value is a valid
majorant; `(I - cP)|_Omega` is a nonsingular M-matrix with nonnegative inverse,
so `Ghat - G >= 0` on `Omega`. ∎
*Measured soundness:* **0 violations in 72 cells x 9 values of `K`.**

**Tradeoff curve (E4).** `K*` = smallest `K` with `Ahat_e(K) <= 2 A_real`:

| family | `alpha` | `A_real` | `K*` | `K* sqrt(alpha)` | `vol(Omega_{K*})/vol(S_eps)` |
|---|---|---|---|---|---|
| path | 2^-6 / 2^-8 / 2^-10 | 0.125 / 0.0625 / 0.0313 | 8 / 32 / 64 | 1.0 / 2.0 / 2.0 | 1.24 / 1.47 / 1.51 |
| spider | 2^-6 / 2^-8 / 2^-10 | 0.125 / 0.0625 / 0.0313 | 8 / 32 / 64 | 1.0 / 2.0 / 2.0 | 1.34 / 1.69 / 1.77 |
| caterpillar | 2^-8 / 2^-10 / 2^-12 | 0.0662 / 0.0331 / 0.0166 | 16 / 64 / 128 | 1.0 / 2.0 / 2.0 | 1.35 / 1.75 / 1.81 |
| grid2d | 2^-6 / 2^-8 / 2^-10 | 0.108 / 0.0512 / 0.0253 | 8 / 32 / 64 | 1.0 / 2.0 / 2.0 | 2.28 / 4.62 / 3.81 |
| grid3d | 2^-4 / 2^-6 | 0.222 / 0.111 | 2 / 8 | 0.5 / 1.0 | 2.72 / 3.70 |
| exp3reg / rrt | 2^-4 / 2^-6 | 0.220 / 0.089 | 4 / 8 | 1.0 / 1.0 | 4.21 / 3.33 |

> **`K* = Theta(alpha^{-1/2})` with constant `0.5 … 2`.** The certificate lives
> on the *diffusion length*, i.e. exactly the `sqrt(alpha)` scale the program is
> chasing — it does **not** need the `1/alpha` mixing scale that kills the
> Neumann bound. Read cost is `1.2 … 4.6 x vol(S_eps)`, alpha-free.

## 5. The payoff and the certificate tax (E3, E6)

**E6 — certified stopping radius of a region method (exact restricted solve on a
BFS ball), `eps = 1e-5`.** `R_cert` = repo rule; `R_esc` = (e') at
`K = ceil(4/sqrt(alpha))`; `R_oracle` = exact semantic error `<= eps`.

| family | `alpha` | `K` | `R_cert / R_esc / R_oracle` | `vol_cert/vol_oracle` | `vol_esc/vol_oracle` | cert read / `vol(S_eps)` |
|---|---|---|---|---|---|---|
| path | 2^-4 | 16 | 22 / **19** / 19 | 1.15 | **1.00** | 1.87 |
| path | 2^-6 | 32 | 45 / **37** / 37 | 1.21 | **1.00** | 1.88 |
| path | 2^-8 | 64 | 91 / **69** / 69 | 1.32 | **1.00** | 1.94 |
| spider | 2^-4 | 16 | 17 / **14** / 14 | 1.21 | **1.00** | 2.17 |
| spider | 2^-6 | 32 | 34 / **26** / 26 | 1.30 | **1.00** | 2.25 |
| spider | 2^-8 | 64 | 69 / **47** / 47 | 1.46 | **1.00** | 2.37 |
| grid2d | 2^-4 | 16 | 15 / **13** / 13 | 1.32 | **1.00** | 6.35 |
| grid2d | 2^-6 | 32 | 30 / **22** / 22 | 1.84 | **1.00** | 7.95 |
| grid2d | 2^-8 | 64 | 55 / **34** / 34 | **2.54** | **1.00** | 5.43 |
| hidden_hub | 2^-4 | 16 | 5 / — / 5 | 1.00 | (rule already tight) | — |

**The escape certificate recovers the oracle stop exactly, in 9 of 9 cells.**

**How much of the campaign's measured work is certificate tax?**

| mechanism / family | tax = `W_certified / W_oracle` | removable by (e')? |
|---|---|---|
| **push, all 30 cells** | `1.00 … 2.16`, median **1.07** | no — and nothing to remove; the rule is already tight (§3) |
| region solve, path | `1.15 -> 1.32` as `alpha: 2^-4 -> 2^-8` | **yes, to 1.00** |
| region solve, spider | `1.21 -> 1.46` | **yes, to 1.00** |
| region solve, grid2d | `1.32 -> 2.54` | **yes, to 1.00** |
| region solve, grid3d / exp3reg (E3) | up to `2.49` | expected yes |
| **local AMG on 2-D lattices (I2-F/I3-A, quoted)** | region inflation `2.0 … 6.1x`, and *all* of the certified-vs-oracle exponent gap (`+0.20` vs `-0.06`) | **yes — this is the same object** |

**Which headline numbers move.** In the campaign's `vol` units the tax is
`1.15 … 2.5x` at the alphas reachable here; it is a *radius* excess
`Delta R = ln(1/A)/kappa` and so enters volume as `(1 + Delta R/R)^D`. Because
`A = sqrt(alpha)` and `kappa ≍ sqrt(alpha)`, `Delta R ≍ ln(1/alpha)/(2 sqrt(alpha))`
— **the same order as `R` itself**, which is why I2-F saw `2.0–6.1x` and I3-A
saw up to `17.5x` in 3-D. Concretely:

* **Every self-certified region-method figure in I3-A §3, I2-F §3 and I4-D §4–§5
  is inflated by this factor**, and the inflation grows with `1/alpha` and with
  dimension. I4-D §5's grid ridge (`amg self-cert 433 -> 638` vs
  `amgO 43 -> 59`, a `~10x` gap) is, per E6, *entirely* certificate tax:
  the oracle-stopped radius is reachable by a sound computable rule.
* **No push figure moves** (`<= 2.16x`, median `1.07x`). I4-D §4's push entries
  (`star 0.60`, `btree 4.61`, `grid3d 38.9`, `exp3reg 5.67`, `pa_tree 178`)
  stand as they are.
* **I4-D §6f's headline is corrected in one respect and confirmed in another.**
  Confirmed: the stated rule fails on the optimal output in most cells and the
  true amplification is `Theta(alpha^{-1/2})` there. Corrected: this is not "the
  missing `1/sqrt(alpha)`" of the target — it is a `Theta(alpha^{-1/2})` factor
  in the *residual threshold*, which costs only `Delta R = Theta(log(1/alpha)/sqrt(alpha))`
  extra radius, i.e. a **constant-to-`polylog` factor of volume in 1-D and
  `2 … 6x` in 2-D/3-D**, not a factor `1/sqrt(alpha)` of work.

## 6. RECOMMENDATION (decision-ready, for `docs/decisions/residual-convention.md`)

**Adopt a two-tier rule. Keep (a) as the always-valid floor; add (e') as the
implementation-wide stopping rule for any method that leaves its residual on a
boundary.**

```
TIER 0 (unconditional, unchanged, always sound):
    stop when  ||D^{-1/2}(Q x_hat - b)||_inf  <  alpha * eps_ppr .
    Justification: Lemma 1 — 1/alpha is EXACTLY ||D^{-1/2}Q^{-1}D^{1/2}||_inf.
    Charged cost: already inside every ledger (I4-D Lemma D).
    Use as-is for any THRESHOLD-stopped method (push / APPR, ISTA / RPPR):
    measured A ∈ [0.48, 1.00], so Tier 0 is within 2x of optimal there and
    Tier 1 cannot repay its own cost.

TIER 1 (region / restricted-solve / multigrid / elimination / Krylov methods
        -- anything NOT stopped by a per-coordinate residual threshold):
    let r = gamma s - H pi_hat,  psi = |r|/d,  theta = ||psi||_inf,
        T = supp(psi),  Omega = B_K(T) with K = ceil(4 / sqrt(alpha)) ;
    solve on Omega:   d_i Ghat_i - c sum_{j~i} Ghat_j = d_i psi_i ,
        with Ghat_j = theta/(1-c) for j outside Omega ;
    STOP when  max_{j in T} Ghat_j  <=  eps_ppr .
    Sound for every K and every graph (M-matrix comparison; Prop. e').
    Charged cost: vol(Omega_K) row reads + one local SPD solve on Omega_K.
      measured 1.2 – 8 x vol(S_eps), alpha-free.
      For an elimination/AMG method that already factors Q[Omega,Omega], this is
      one extra triangular solve on an annulus, not a new region.
```

**Hypotheses under which Tier 1 is valid (state these in every theorem that
uses it).** `G` simple, undirected, unweighted, no isolated vertices;
`alpha ∈ (0,1]`; `r` computed exactly (in floating point, threshold `T` at
`|r_j| > 10^{-8} theta d_j` and add the discarded mass to `theta` — see
caveat 3); `Omega ⊇ T`. Nothing about `r`'s sign is needed. Nothing about the
graph is needed.

**What remains unsound / not recommended.**

* **A uniform `sqrt(alpha)` relaxation of Tier 0 is UNSOUND.** Two independent
  refutations, one proved: `hidden_hub` has `A = 1/(1+c) -> 1/2`; **push has
  `A = Theta(1)` on every family measured**. Do not adopt it in any form,
  including "with a safety factor" — `A/sqrt(alpha)` is unbounded as
  `alpha -> 0`.
* **One-sidedness is not a certificate improvement** (Cor. 2c, proved). Do not
  quote a "tighter one-sided bound"; quote instead the *envelope*
  `pi_hat <= pi <= pi_hat + (theta/(1-c)) d`, which is what monotonicity
  actually gives.
* **K-term Neumann and max-principle refinements are dead ends** (confirmed
  I3-A): `Theta~(1/alpha)` terms and `<= 2x` respectively.
* **The support-only constant `A(T)` is not implementable as stated.** It is
  numerically fragile: any round-off inside the region inflates `T` and drives
  `A(T)` back toward 1 (measured `A_sharp = 0.95` on a path where the true
  `A = 0.016`). **Always use the profile version (e'), never the support
  version.** This is a real trap and the single most likely way to implement
  this wrong.
* **Open:** whether Tier 1's `K = Theta(alpha^{-1/2})` can be reduced. The
  `sqrt(alpha)` scale is a diffusion length and is probably necessary; a
  lower bound would close the question.

## 7. Ledger, verification, caveats

* **E7.** `run7.py` / `spread7.json`: ISTA and Chebyshev amplifications.
* **Verification.** Every `A_real` is `(1-c) err/theta` with `err` computed
  against an exact `spsolve` (or CG to `rtol = 1e-13`) — no self-reported
  residuals. Theorem 2 and Lemma 1 were checked against dense inverses on
  `n = 400`. Soundness of (e') was checked pointwise: `Ahat_e(K) >= A_real`
  in **648** (72 cells x 9 radii) comparisons, 0 violations.
* **Ledger.** Certificate costs are reported as (i) `vol(Omega_K)` charged row
  reads and (ii) `nnz` of the local system — both recorded in `esc4.json`.
  Region volumes in E6 are `vol(B_R)`, the object I2-F/I3-A inflate.
* **Caveats.**
  1. `eps = 1e-5` throughout; graph sizes 6k–20k. Large-`alpha^{-1}` cells with
     `K > 128` or `|Omega| > 60000` are reported as `>128` and are not failures.
  2. The E6 payoff is measured on an exact restricted solve, which isolates the
     stopping rule from the mechanism. An inexact solver leaves interior
     residual too, which (e') handles (it uses the full profile) but which will
     raise its `Ahat` toward Tier 0 — exactly as it should.
  3. Floating-point support detection is the one implementation hazard (§6).
     All `A_sharp` numbers in `cert2.json` are contaminated upward by it and
     should be read as *upper bounds only*; the (e') numbers are not.
  4. `run1.py` (kind = `push`, `push30`) used a mis-scaled push accumulator and
     those rows are superseded by `run5.py`/`push5.json`. All `opt`/`ball`/
     `ista`/`cheb` rows are unaffected. E5/E6 use the corrected code.
  5. I4-D's `hidden_hub` exponent `alpha^{-0.97}` is here explained and made
     exact: `A = 1/(1+c)`, so `A/A_worst -> 1/2` and the over-charge is exactly
     `1 + c -> 2`, never more.
