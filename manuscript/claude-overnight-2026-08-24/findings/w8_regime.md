# W8 — Empirical regime map: push vs Wei-Yang-style active set vs the 1/(sqrt(alpha)*eps) target, with measured constants

**VERDICT (Measured).** Under honest degree-charged work, the textbook regime
picture — push `1/(alpha*eps)` vs WY `1/eps^2` crossing at `eps* = alpha`, with
an open wedge `eps < sqrt(alpha)` worth up to `1/sqrt(alpha)` — is **empirically
wrong in shape and wildly optimistic in prize** on support-sized families.
Measured WY is `~1/eps` (not `1/eps^2`) on every tree family, so the push/WY
boundary is a **horizontal line `alpha* ~ 2^-4..2^-6`** (eps-free), not a curve
`eps*(alpha)`; only the 2D grid shows a genuine in-eps crossover, and there it
follows the **alpha line** (`theta = 2.36 +- ~0.4` in
`eps* = kappa*sqrt(alpha)^theta`, kappa ~ 0.5), i.e. the constant-free algebra
line `eps* = alpha/2` — **not** `sqrt(alpha)`. The prize for the open
`O~(1/(sqrt(alpha)*eps))` target, measured against the best *oracle-stopped*
incumbent, **plateaus at ~2x on the W2-canonical spider, ~2.6x on
caterpillars, and peaks at 4.3x on grids** inside the entire sweep
(`alpha >= 2^-14, eps >= 2^-13`); against *self-certified* incumbents it
reaches 8–14x. **No cell reaches 10x (oracle bracket) and no cell reaches
100x (either bracket).** The open problem's asymptotic win is real only on
families with genuine 2D/fill-in structure, and becomes >=10x only beyond
`(alpha, eps) ~ (2^-13, 2^-15)` by ridge extrapolation.

Code: `w8_regime/{cpush.c, contenders.py, run_map.py, run_cert.py,
run_push_oracle.py, validate.py, fit.py}`. Data: `w8_regime/map.csv` (858 dense
cells, all columns per spec + extras), `cert.csv`, `push_oracle.csv`; digested
tables in `w8_regime/analysis.md`. Logs `logs/w8_map*.log`, `logs/w8_cert.log`.
Total compute ~ 2 min (C push kernel; 13 alphas x 11 eps dense grid).

## 0. Contenders, accounting, guarantees (all verified)

Shared Meter convention (as W1–W5): scans charge `d_u` (first exposure
`C_adj`, repeats `R_adj`).

* **PUSH** = literal `lib/model.py:appr_lazy` (FIFO lazy ACL), ported to C and
  validated **bit-identical** (45-cell suite: work counters exactly equal, `p`
  arrays equal to 0 ulp). Activation threshold = semantic `eps`.
  `W_push = C_adj + R_adj`.
* **WY-style active set**: grow `S` from the seed by boundary violations of the
  one-sided boundary certificate `cert_v = (a/d_v) * sum_{u in S~v}
  pihat_u/d_u`; per expansion solve `Q_SS x_S = b_S` exactly by sparse LU
  (`splu`, MMD_AT_PLUS_A). Charges: joins + per-round frontier scans
  (`C_adj/R_adj`), assembly `vol(S)` per round (`C_rec`), factor `nnz(L)+nnz(U)`
  and solves `2*(nnz(L)+nnz(U))` (`C_resp`). `W_WY` = sum of all four.
* **TARGET oracle**: `W_target = 1/(sqrt(alpha)*eps)` verbatim (positioning
  only).

Accuracy standards (the subtle part; both proved and measured):

1. Push at threshold `eps` satisfies the **one-sided ACL bound** `err <= eps`
   a priori (`pi - p = alpha*M^{-1} r`, `M^{-1} >= 0`, `M^{-1} d = d/alpha`),
   and simultaneously satisfies the two-sided certificate
   `||D^{-1/2}(Qx-b)||_inf < alpha*eps` (its system residual is `alpha*r`).
   Measured: certified-eps / true-err ∈ [1.4, 8.2] (median 1.4).
2. **The boundary certificate at threshold eps does NOT guarantee semantic eps
   for restricted solves.** Exact facts (proved in `contenders.py` docstring,
   confirmed numerically): the zero-extended restricted solve obeys a maximum
   principle — `err = max_{v not in S} pi_v/d_v`, attained OUTSIDE `S` — and
   the cert-to-error gap is a structure constant of the outside region:
   `Theta(1)` on spiders/btrees but **`Theta(1/alpha)` on stars/caterpillars**
   (reflected mass that the killed chain loses; measured: the certificate
   threshold had to be tightened to `~alpha*eps` there, 8–12 halvings).
   Consequently we bracket WY:
   * `W_WY` (**LO**, in map.csv): tau-halving schedule stopped by an oracle
     check of the true error (a stand-in for Wei-Yang's whp estimation
     machinery, whose cost is NOT charged — so LO is a floor for any real WY).
   * `W_WYcert` (**HI**, cert.csv): fully self-certified deterministic
     variant, terminate at `cert < alpha*eps` (proved: `err <= cert/alpha`).
   * Symmetrically for push: `W_push_oracle` (push_oracle.csv) = cheapest
     threshold whose true error `<= eps` (bisection; median gain only 1.5x,
     but unbounded on near-equilibrated cells).
3. **Every one of the 854 feasible cells verified against the exact sparse
   solve** (all `n <= 131k`; no certificate-only cells were needed). Push:
   err/eps median 0.671, max 0.860, one-sidedness `p <= pi` exact. WY: median
   0.495, max 0.994. Zero assertion failures; 4 spider cells skipped at the
   200k-edge cap (recorded).

Families (support ~ `1/eps` per spec): star `m = 1/(4eps)` center-seeded;
spider `k = 1/(4eps), L = 2/sqrt(alpha)`; caterpillar `m = 1/(4eps)` + pendant
leaves, end-seeded; binary tree `n ~ 1/eps` root-seeded; grid
`side = sqrt(1/(2eps))` corner-seeded; **plus spider2** `k =
sqrt(alpha)/(4eps), L = 2/sqrt(alpha)` — the W2-canonical hard spider (see
Anomaly A3: the task's spider sizing trivializes at small alpha).

## 1. The regime geometry (winner map)

Full winner tables: `w8_regime/analysis.md`. Per-alpha row profiles over
non-trivial cells (P = push row, W = WY row, M = mixed = in-eps crossover):

| family | LO bracket (oracle-stopped) | HI bracket (self-certified) |
|---|---|---|
| star | P for alpha >= 2^-3, **M at 2^-4**, W below — eps-free | same boundary at ~2^-4 |
| spider2 | P >= 2^-3, M in 2^-4..2^-7, W <= 2^-8 | P down to 2^-10, M 2^-12, W 2^-14 |
| caterpillar | P >= 2^-4, M 2^-5..2^-7, W <= 2^-8 | P >= 2^-4, M 2^-6..2^-8, W <= 2^-10 |
| btree | M 2^-2..2^-4, W <= 2^-5 | **P everywhere** |
| grid | M 2^-3..2^-10 (real crossover curve), W <= 2^-11 | **P everywhere** |

Reading: under self-certified rules push wins most of the plane (it IS its own
certificate; certified WY must cover the `alpha*eps` superlevel set). Under
oracle rules WY wins everything below `alpha ~ 2^-5±2` because measured
`W_WY ~ 1/eps`, e.g. star at `eps = 2^-9`: `W_push/W_WY` = 0.28 (alpha=2^-2),
1.04 (2^-4), 12.4 (2^-8), 565 (2^-14) — `W_WY ≈ (4.5..10.7)/eps` with only a
`log(1/alpha)` drift from the tightening schedule.

## 2. Crossover law eps*(alpha)

* **Trees (star, spider, spider2, caterpillar, btree): no eps*(alpha) curve
  exists** — at fixed alpha the winner is constant in eps (0–2 stray crossings
  over 13 alphas). The boundary is `alpha* ~ 2^-4` (star, btree), `~2^-5.5`
  (caterpillar), `~2^-5..-7` (spider2). The theoretical comparison line
  `eps = sqrt(alpha)` is not just quantitatively off — it is the wrong shape,
  because WY is not `1/eps^2` there.
* **Grid (the only genuine curve): `theta = 2.36`, `kappa = 0.51`**
  (rms 0.74 in log2, 8 alphas) — statistically the **alpha line**
  `eps* ≈ alpha/2` (theta=2), clearly excluding the sqrt(alpha) line
  (theta=1). So where the naive algebra applies at all, its exponent is right
  and its constant is ~1/2.
* Empirical wedge boundary (target beats best incumbent, map.csv LO):
  spider2 `eps† = 0.18*sqrt(alpha)^0.91` (parallel to the sqrt line, 5.5x
  lower); grid `eps† = 0.30*sqrt(alpha)^1.69`. The theoretical wedge
  `eps < sqrt(alpha)` overstates the region substantially.

## 3. Constants (the point of the exercise)

`W_push * alpha * eps` (non-trivial cells, eps <= 2^-5):

| family | median | range |
|---|---|---|
| star | **0.367** | [0.312, 0.368] |
| spider | 0.156 | [0.125, 0.250] |
| spider2 | 0.207 | [0.066, 0.244] |
| caterpillar | 0.162 | [0.009, 0.254] |
| btree | 0.062 | [0.001, 0.211] |
| grid | 0.135 | [0.021, 0.215] |

Star sits inside the manuscript's proven `[3/128, 1] = [0.023, 1]` and agrees
with W1's literal-APPR measurement (c ≈ 0.30–0.31); the family saturates the
`1/(alpha*eps)` law with constant ~ 1/3.

`W_WY * eps^2` is **not an invariant** (WY is not `1/eps^2`): median values
1e-5..0.05 and still falling with eps on trees. The honest summary is the
fitted exponents `log2 W = c + pe*log2(1/eps) + pa*log2(1/alpha)`:

| family | push pe, pa | WY(LO) pe, pa | comment |
|---|---|---|---|
| star | 1.00, 1.01 | 0.99, **0.10** | WY ~ 1/eps, alpha-free |
| spider | 1.00, 0.50 | 0.97, −0.00 | push ~ 1/(sqrt(alpha)*eps)! |
| spider2 | 1.07, 0.95 | 1.18, 0.45 | hard family: both pay alpha |
| caterpillar | 0.67, 1.16 | 0.62, 0.72 | equilibration-shaved |
| btree | 0.91, 0.48 | 0.96, −0.56 | deeper alpha helps WY |
| grid | 0.97, 0.95 | **1.45**, 0.17 | only ~eps^-1.5 family (fill-in) |

Self-certified WY constant `W_WYcert * eps^2`: median 0.009 (star) to 0.17
(grid), max 14.2 (spider2 deep) — the certified variant does reach the
`1/eps^2`-and-worse regime.

## 4. Expansion counts vs the "1/eps expansions" pessimism

Measured E (rounds incl. tightenings) at `eps = 2^-13`: star **2–14**
(log(1/alpha) tightenings only), spider 1, btree 1–10, grid 7–137
(≈ 2*side ~ eps^-0.5, fitted slope 0.99 at alpha=2^-10 across eps),
caterpillar **7–409 with E ≈ |S|** — the one-hop-per-round creep is real on
path-like graphs (and for certified WY: E_cert = 422 ≈ ecc). So the `~1/eps`
expansion pessimism is: wildly pessimistic on stars/spiders, essentially TIGHT
on caterpillars (E ≈ |S| ≈ 1/eps at the deep end). A doubling growth rule
would provably cut E to log — see Next targets.

## 5. Prize map (the deliverable)

Speedup = best-incumbent / `W_target`, LO = oracle-stopped incumbents
(min of oracle-push, oracle-WY), HI = self-certified incumbents.

* **>= 10x: LO — nowhere in the sweep. HI — one cell: spider2
  (2^-14, 2^-9) at 14x** (certified-WY creep + push paying
  0.2/(alpha*eps)).
* **>= 100x: nowhere, either bracket.**
* Family maxima (LO | HI): star 1.5x | 1.4x; spider 0.2x | 0.5x; spider2
  2.1x | 14.1x; caterpillar 2.6x | 8.3x; btree 0.4x | 0.7x; grid 4.3x | 9.0x.
* Structure of the LO ridge (max over eps per alpha): spider2 **plateaus at
  1.9–2.2x** for alpha <= 2^-8 (empirical corroboration of W2's Theta(1/eps)
  ceiling: on the family built to witness the target, incumbents already sit
  ~2x from the target line, forever). Caterpillar plateaus at ~2.5x. **Only
  the grid ridge grows** (0.34 → 4.34x at (2^-11, 2^-13)), at ×~1.3 per
  alpha-halving, and it is truncated by the sweep edge (best eps pegged at
  2^-13 from alpha = 2^-9 on) and then by family equilibration (alpha <=
  2*eps makes the support-sized grid trivial). Extrapolating the un-truncated
  ridge slope: **10x at ~(2^-13, 2^-15), 100x only near (2^-21, 2^-23)** on
  support-sized grids; the HI bracket reaches those thresholds ~4–6 octaves
  earlier.

**Interpretation for research priority:** the open `1/(sqrt(alpha)*eps)`
target is worth < 3x over oracle incumbents everywhere practical on 1D/tree
families — the wedge there is a constants game, not an exponents game. The
real payoff region is 2D/fill-in-like structure at deep accuracy
(`eps <~ alpha/2`), where the measured gap grows without visible bound but
starts from 4x at the edge of this sweep.

## 6. Anomalies

* **A1 (certificate-scale gap).** The natural boundary certificate at
  threshold eps mis-certifies restricted solves by Theta(1/alpha) on
  reflector families (star, caterpillar) — first observed as a hard
  assertion failure (err = 1.5*eps on a 3-node star), then isolated to the
  killed-chain mass loss; exact maximum-principle characterization
  `err = max_{v not in S} pi_v/d_v` proved and used. Any WY-style
  implementation needs whp outside-mass estimation or a geometric
  tightening schedule (ours: cost only log(1/alpha) extra rounds).
* **A2 (oracle-WY can cost more than certified WY).** Star deep cells:
  tau-halving probe rounds (8.6e4) exceed the direct certified run (3.7e4)
  — a schedule artifact, folded into the brackets.
* **A3 (spider sizing).** The task's `k = 1/(4eps)` spider goes trivial
  (`max pi/d <= eps`, x = 0 valid) for alpha <= 2^-6 — mass equilibrates
  over vol ~ 1/(eps*sqrt(alpha)). Kept in the map (flagged `triv`), and the
  W2-canonical `k = sqrt(alpha)/(4eps)` added as spider2. More generally
  **every support-sized family self-trivializes at alpha <~ 2*eps** (grid,
  btree rows show it); the non-degenerate wedge is a band, not the full
  `eps < sqrt(alpha)` region.
* **A4.** Push's two-sided `alpha*eps` certificate is nearly tight on these
  families (over-certifies by median 1.4x) — the one-sided bound and the
  certificate agree here, unlike for restricted solves (A1).

## 7. Next targets

1. **Grid ridge extension** (cheap, ~min): eps to 2^-16, n to 32k on grids to
   watch the LO ridge cross (or fail to cross) 10x; this is now the single
   decisive family for the open problem's value.
2. **Kill the caterpillar creep**: doubling/geometric growth in the active-set
   solver should cut E from ~|S| to ~log|S|, making measured WY `~1/eps
   polylog` on ALL tree families — likely provable (tree factorizations are
   linear); would formally reduce the open problem's tree-case prize to O(1).
3. **Theory target suggested by the data**: active-set with exact solves costs
   `O~((1/eps)*(fill(S) + creep))` — the `1/eps^2` in Wei-Yang is creep, not
   fill. Reframe the open problem as: beat `fill`-driven costs on non-tree
   structure at `eps < alpha` — i.e. the wedge that matters is
   `eps < ~alpha/2` (measured), not `eps < sqrt(alpha)`.
