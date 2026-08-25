# W3 — Randomized accelerated proximal CD (APCG) as a locality-compatible acceleration mechanism

**VERDICT: POSITIVE (Measured).** Uniform-sampled APCG restricted to a support set achieves
expected charged work `~ vol(S)/sqrt(alpha)` on every graph tested (fitted vol-normalized
exponents 0.45–0.52 vs 0.87–1.00 for all baselines), and the K2/K8 per-trajectory
adversarial families that block the deterministic safeguarded accelerated-CD analysis do
**not** bite the randomized method — not in expectation, not in median, not even in the
max over 40 seeds (iteration count ~ 1/q, vs 1/q^2 for plain CD).

Code: `w3_apcg/{solvers,verify,exp_scaling,exp_k2k8,exp_grow,exp_extra}.py`; raw data in
`w3_apcg/results_*.json`; logs in `w3_apcg/scaling.log`. Total compute ≈ 8 min.

## 0. Implementation and verification (Measured)

APCG (Lin–Lu–Xiao 2014), strongly-convex constant-parameter variant, uniform sampling
(valid: all `L_i = Q_ii = (1+alpha)/2` equal). `sigma = 2*alpha/(1+alpha)` (strong
convexity w.r.t. `||.||_L`; a priori, no eigensolve), `a = sqrt(sigma)/n`, `n = |S|`.
Per-step map in `(x, z)` diagonalizes as `p = (x+z)/2` (stored plainly) and
`m = (x−z)/2 = phi * Mh` (scalar decay accumulator `phi <- phi*(1−a)/(1+a)`), so one
iteration touches only the sampled coordinate and its neighbors: true cost `O(d_i)`,
charged as `meter.scan(i)` **including zero-prox steps**; periodic stop checks
(every `n` iterations) charged `vol(S)+n` via `meter.rec`; state flush when
`phi < 1e-120` charged `n`.

* Lazy form ≡ full-vector reference with the paper's **unsimplified** step 4 to 5.6e-17
  (300–997 iters) and 3.7e-14 after 20k iters at `alpha=2^-10` — the algebraic
  simplification `x_{k+1} = y_k + n·a·Δ·e_i` and the two-accumulator coupling are exact.
  No instability of the lazy coupling observed anywhere.
* Ground truth by active-set exact solver (monotone growth + sparse solves), cross-checked
  vs `Model.rppr_exact` to 6e-14.
* `E[F(x_k)] − F*` decays linearly at 1.5–2.6× the guaranteed rate `(1 − sqrt(sigma)/n)`
  per iteration (fitted slopes: star `2^-12`: 1.35e-4/iter vs theory 8.8e-5; path `2^-12`:
  3.76e-4 vs 1.43e-4).

Stop rule (all methods): one-sided KKT excess `h(x) = max_i(−grad_i/√d_i − αρ)_+ ≤ 0.1·αρ`.
Sanity: full-KKT (`sym`) crossing occurred within ≤1.15× of the h-crossing work in every
cell — **momentum did not cause spurious early h-stops**; final semantic error
`||D^{-1/2}(x−x*)||_inf ≤ 0.1·rho` in all 80 runs, statuses all `ok`, no caps hit.

## 1. Fixed-support scaling, S = supp(x*(rho)) offline (Measured)

Median charged work W over 5 seeds (uniform CD: 5/3/2 seeds at α ≥ 2^-8 / 2^-10 / 2^-12;
GS and ISTA deterministic). star: m=250=1/(8ρ), ρ=1/2000; path(1200), spider(6,150),
caterpillar(500,1): ρ=1/4000. Support grows as alpha shrinks on path-like graphs
(diffusion-limited), so the **vol-normalized exponent is the primary metric**.

| graph | alpha | \|S*\| | vol(S*) | W_apcg | W_unif | W_gs | W_ista | GS/APCG |
|---|---|---|---|---|---|---|---|---|
| star | 2^-4 | 251 | 500 | 3.15e4 | 4.56e4 | 1.63e4 | 2.70e4 | 0.5x |
| star | 2^-6 | 251 | 500 | 5.78e4 | 1.49e5 | 6.54e4 | 1.08e5 | 1.1x |
| star | 2^-8 | 251 | 500 | 1.28e5 | 5.85e5 | 2.63e5 | 4.35e5 | 2.0x |
| star | 2^-10 | 251 | 500 | 2.43e5 | 2.15e6 | 1.05e6 | 1.74e6 | 4.3x |
| star | 2^-12 | 251 | 500 | 5.07e5 | 8.43e6 | 4.20e6 | 6.97e6 | 8.3x |
| path | 2^-4 | 15 | 29 | 2.05e3 | 4.37e3 | 1.24e3 | 3.48e3 | 0.6x |
| path | 2^-6 | 28 | 55 | 8.14e3 | 2.78e4 | 8.29e3 | 2.44e4 | 1.0x |
| path | 2^-8 | 50 | 99 | 2.78e4 | 1.84e5 | 5.34e4 | 1.59e5 | 1.9x |
| path | 2^-10 | 88 | 175 | 9.33e4 | 1.17e6 | 3.30e5 | 1.01e6 | 3.5x |
| path | 2^-12 | 154 | 307 | 2.97e5 | 7.38e6 | 2.00e6 | 6.24e6 | 6.7x |
| spider | 2^-4 | 61 | 126 | 8.76e3 | 1.49e4 | 4.35e3 | 1.17e4 | 0.5x |
| spider | 2^-6 | 115 | 234 | 3.15e4 | 9.46e4 | 2.77e4 | 7.84e4 | 0.9x |
| spider | 2^-8 | 205 | 414 | 1.02e5 | 5.80e5 | 1.66e5 | 4.83e5 | 1.6x |
| spider | 2^-10 | 355 | 714 | 3.35e5 | 3.46e6 | 9.45e5 | 2.81e6 | 2.8x |
| spider | 2^-12 | 577 | 1158 | 1.00e6 | 1.91e7 | 4.94e6 | 1.47e7 | 4.9x |
| caterpillar | 2^-4 | 20 | 39 | 2.68e3 | 5.45e3 | 1.68e3 | 4.48e3 | 0.6x |
| caterpillar | 2^-6 | 37 | 74 | 9.57e3 | 3.55e4 | 1.10e4 | 3.13e4 | 1.2x |
| caterpillar | 2^-8 | 66 | 131 | 3.63e4 | 2.32e5 | 6.98e4 | 2.00e5 | 1.9x |
| caterpillar | 2^-10 | 117 | 234 | 1.17e5 | 1.50e6 | 4.32e5 | 1.27e6 | 3.7x |
| caterpillar | 2^-12 | 202 | 403 | 3.82e5 | 9.19e6 | 2.59e6 | 7.63e6 | 6.8x |

Fitted exponents `p` in `W ~ alpha^{-p}` (raw / vol-normalized, 5 points, max log2-dev ≤ 0.11):

| graph | APCG | CD-uniform | CD-GS | ISTA (on S) |
|---|---|---|---|---|
| star | 0.505 / **0.505** | 0.946 / 0.946 | 1.001 / 1.001 | 1.001 / 1.001 |
| path | 0.894 / **0.470** | 1.342 / 0.918 | 1.331 / 0.907 | 1.350 / 0.926 |
| spider | 0.855 / **0.454** | 1.292 / 0.892 | 1.270 / 0.869 | 1.287 / 0.887 |
| caterpillar | 0.896 / **0.476** | 1.342 / 0.922 | 1.323 / 0.903 | 1.340 / 0.920 |

The star (support constant in alpha) is the cleanest cell: p = 0.505 raw. Constants are
strikingly stable: `W_apcg/(vol·alpha^-1/2)` lies in [13.5, 18.5] across all 20 cells —
a 1.37x band over 4 graph families and 256x in alpha, i.e.
`W ≈ 15·vol(S)/sqrt(alpha)` at delta=0.1.
Tighter accuracy `delta = 0.01` leaves the exponent unchanged (star 0.520, path 0.477 —
`results_extra.json`), only shifting the constant.

## 2. Adversarial families K2 / K8 (Measured)

`alpha = q^2/(1+q^2)`; K2: uniform seed, ρ=1/16; K8: uniform seed, ρ=1/112; support = all
nodes (checked); n constant so work = iteration count. Median (IQR) over 25 seeds:

| family | q | APCG iters | IQR | CD-uniform iters |
|---|---|---|---|---|
| K2 | 1/30 | 282 | [242, 298] | 4.43e3 |
| K2 | 1/100 | 992 | [916, 1028] | 4.93e4 |
| K2 | 1/300 | 3024 | [2916, 3106] | 4.45e5 |
| K2 | 1/1000 | 10024 | [9892, 10216] | 4.94e6 |
| K8 | 1/30 | 848 | [800, 920] | 1.06e4 |
| K8 | 1/100 | 2768 | [2632, 2872] | 1.11e5 |
| K8 | 1/300 | 7984 | [7888, 8336] | 9.66e5 |
| K8 | 1/1000 | 26064 | [25480, 26824] | 1.05e7 |

Fits: APCG `iters ~ q^-1.018` (K2), `q^-0.976` (K8); CD `q^-2.001` / `q^-1.967`.
With 40 seeds on K2, **mean** ~ `q^-1.018` and **max** ~ `q^-0.976` (max/median ≤ 1.10).
The persistent-low-mode / pulse phenomenon that defeats the deterministic safeguarded
accelerated-CD per trajectory does not slow the randomized method even in its worst
sampled trajectory; concentration is tight, so this is not a fragile in-expectation-only
effect.

## 3. Growing support with the safe gate (Measured, exploratory)

Start `S_0` = violating seeds; every `|S|` iterations test boundary `j`: admit iff
`grad_j f(x) < −αρ·√d_j` (charged `d_j` per test). Variants: **restart** (z ← x, momentum
reset per admission event) and **carry** (keep the two-accumulator state, append zeros;
not covered by the estimate-sequence analysis — Open). 3 seeds, medians; "spur" = admitted
nodes outside supp(x*) (max over seeds); missed nodes: always 0; final error fine in all runs.

| graph | alpha | W_fixed | W_restart | W_carry | admit events | spur (restart/carry) |
|---|---|---|---|---|---|---|
| star | 2^-6 | 5.35e4 | 5.50e4 (1.03x) | 5.38e4 (1.00x) | 1 | 0 / 0 |
| star | 2^-10 | 2.22e5 | 2.24e5 (1.01x) | 2.24e5 (1.01x) | 1 | 0 / 0 |
| star | 2^-12 | 4.44e5 | 4.46e5 (1.00x) | 4.46e5 (1.00x) | 1 | 0 / 0 |
| path | 2^-6 | 7.31e3 | 9.78e3 (1.34x) | 5.61e3 (0.77x) | 27 | 0 / 0 |
| path | 2^-10 | 9.16e4 | 1.96e5 (2.14x) | 7.73e4 (0.84x) | 87 | 0 / 4 |
| path | 2^-12 | 2.87e5 | 8.35e5 (2.91x) | 2.52e5 (0.88x) | 153 | 0 / 6 |
| spider | 2^-6 | 3.39e4 | 4.91e4 (1.45x) | 2.60e4 (0.77x) | 46 | 0 / 5 |
| spider | 2^-10 | 3.00e5 | 9.82e5 (3.28x) | 2.52e5 (0.84x) | 219 | 0 / 9 |
| spider | 2^-12 | 9.55e5 | 3.85e6 (4.03x) | 8.57e5 (0.90x) | 399 | 0 / 29 |
| caterpillar | 2^-6 | 9.65e3 | 1.51e4 (1.57x) | 8.95e3 (0.93x) | 26 | 0 / 1 |
| caterpillar | 2^-10 | 1.21e5 | 2.84e5 (2.34x) | 8.76e4 (0.72x) | 97 | 0 / 3 |
| caterpillar | 2^-12 | 4.11e5 | 1.21e6 (2.93x) | 3.14e5 (0.76x) | 175 | 0 / 2 |

3-point vol-normalized exponents: restart 0.50 (star) but **0.64–0.67** (path/spider/
caterpillar, where admissions ≈ |S*|) vs fixed-ref 0.41–0.51; carry 0.44–0.51 ≈ fixed.
So restart-per-admission **partially degrades** the scaling (≈ +0.15–0.25 in the exponent
over this alpha range; consistent with paying a fresh momentum ramp per admitted layer),
while carrying momentum across admissions preserves both the exponent and the absolute
constant (even beating fixed-support, since early segments run on small S with cheap
checks). Momentum does drive the iterate out of the monotone cone occasionally: the carry
variant admits 0–5% spurious nodes (worst: spider 2^-12, 29/577 ≈ 5% of |S*|, extra vol
bounded and harmless to correctness since S ⊇ S* keeps the restricted solution = x*);
the restart variant admitted **zero** spurious nodes in all runs.

**Decoy-hub probe (Measured).** `decoy_hub(200, hub_deg∈{100,400})`, ρ=1/4000,
α∈{2^-10, 2^-12}: the high-degree hub adjacent to the support was **never** spuriously
admitted (0/24 grow runs, both variants), nor were its leaves; spurious admissions remain
a handful of low-degree path nodes just past the true boundary. At `hub_deg=400, α=2^-12`
the hub legitimately truncates S* (|S*|=116 vs 222 at hub_deg=100 where the hub enters S*),
and carry's overhead ticks up to 1.23x fixed — worst carry ratio observed, still ≪ restart's
3.07x. So the momentum-breaks-the-safe-gate worry did not materialize on the decoy family.

## 4. Honest negatives / caveats

* **Constants, not scaling, at moderate alpha:** GS-CD beats APCG by ~2x at `alpha=2^-4`
  on every graph; crossover is at `alpha ≈ 2^-6`. APCG's constant is ≈ 4x GS's.
* **Restart-per-admission is not free** (above): exponent ~0.65 on many-admission graphs.
  The carry variant fixes it empirically but has no theory (Open) and a small spurious rate.
* **Baseline exponents ran 0.87–0.95, not 1.00**, on the growing-support graphs (mild
  bending consistent with log-factors and support-boundary effects); GS/ISTA on the star
  hit 1.001 exactly. This does not affect the 2:1 exponent contrast.
* GS coordinate selection (argmax) and per-iteration h availability were not charged
  (bookkeeping outside the degree-charge model; a heap makes it `O(log n)`); this favors
  the *baseline*, so the APCG comparison is conservative.
* No graph was found where APCG's expected work reverts to `1/alpha` (tested: star, path,
  spider, caterpillar, K2, K8). Lazy-coupling drift: none measured (≤ 3.7e-14 over 20k
  iters at `2^-10`; flush guard never triggered in production runs).
* `sigma = 2·alpha/(1+alpha)` was used a priori; on these supports
  `lambda_min(Q_SS) ≈ alpha` so no hidden conditioning gift.

## 5. Conjecture and next falsifiable target

**Conjecture (supported by all data above).** For RPPR on any fixed support `S ⊇ supp(x*(ρ))`,
uniform-sampled APCG with `sigma = 2α/(1+α)`, charged `d_i` per sampled coordinate,
reaches KKT excess `h ≤ δ·αρ` in expected charged work
`W = O(vol(S)/sqrt(alpha) · log(h(0)/(δαρ)))` — measured constant ≈ 15 at δ=0.1 — and
concentrates (IQR/median ≤ 1.1). The in-expectation estimate-sequence analysis is
per-trajectory-adversary-free: no analog of the K2/K8 deterministic blocker exists for it.

**Next falsifiable target (W3.next).** End-to-end `O~(1/(ρ·sqrt(alpha)))` without offline
support knowledge: prove/refute that growing-support APCG with the safe gate and
**carried momentum** (or restart batched into `O(log |S*|)` epochs, e.g. admit-on-doubling)
has expected charged work `O~(vol(S*)/sqrt(alpha))`. Two concrete attack points:
(a) a bound on spurious admissions under momentum — measured ≤ 5% of |S*|, and the
decoy_hub probe (hub_deg up to 400) never admitted the hub; is spurious extra volume
`O(vol(∂S*))`-bounded adversarially, or does some family (e.g. many marginal hubs ringing
S*) blow up vol(S)? (b) an estimate-sequence argument tolerant of
coordinate insertion at value 0 (the carry variant), or a restart schedule with
`O(log)` restarts. Refute by exhibiting a graph where carry-mode expected work is
`omega(vol(S*)/sqrt(alpha))`.
