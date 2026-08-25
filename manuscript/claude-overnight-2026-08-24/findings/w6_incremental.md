# W6 — Warm-started / incremental active-set solving: the amortization landscape

**VERDICT: MIXED, SHARP (Measured).** (1) At **fixed alpha** the Wei–Yang `(#expansions) x (per-solve)`
pessimism is unreal on every zoo family: fitted W-exponents in `1/eps` are 0.2–1.3 (trees) — nowhere
near 2 — because at fixed alpha either `E ~ log(1/eps)` (geometric decay) or batches double
(`E ~ log vol`). The `1/eps^2` shape appears **only on the diagonal `alpha = eps`** (path: CG-COLD
q=1.97, ORACLE-SDD q=1.46 vs vol-exponent 0.68), and there a real incremental solver already
removes it: **INC-LDL is exactly output-linear, W = 10.5·vol(S*) on paths, alpha-free and
eps-free per volume** — the note's Thm `path-linear` reproduced by a *generic* mechanism (up-looking
LDL^T in admission order), which also stays output-linear on caterpillar (17·vol), **theta (20.5·vol,
a 2-connected cyclic graph!)** and spider (64.5·vol). (2) The same mechanism **fails quadratically on
branching trees** (btree: nnz(L)=|S|^2/4; hub: 300^2 leaf clique): admission order = root-first
elimination = maximal fill. The complementary seed-rooted tree-DP backend (TREE-INC) fixes btree/hub
but pays a measured `alpha^{-0.51}` truncation radius on path-like trees. **No single implemented
structure is output-linear on all trees — that gap is precisely conj:aggregate.** (3) Warm-starting
CG is a **log-factor, not an order**: `iters_warm/iters_cold ≈ ln(r0_warm/tol)/ln(r0_cold/tol)`
(corr 0.86 over 6595 pooled rounds); it saves 39x when the increment is <1e-4 relative and exactly
1.0x once rel-increment ≥ 1e-2 (all big-batch rounds). It does not remove the `1/sqrt(alpha)`
(path it_cold ~ a^-0.49, it_warm ~ a^-0.38) and does not change the diagonal exponent (1.78 vs 1.97).
(4) Prize size for conj:aggregate on real traces: ORACLE-SDD/ORACLE-INC = **0.9x (btree, no prize) to
133x (path a=1e-4), ~E/2 / polylog in general**; on the diagonal at eps=2^-12 the realized (not
idealized) gap COLD-LU/INC-LDL is 35x and ORACLE-SDD/INC-LDL is 187x.

Code: `w6_incremental/{core,run_all,analyze}.py`; raw: `results_{main,alpha,diag}.json`;
log `run_all.log`. 126 configs, total compute ~65 s. **Every config asserted
`||D^{-1/2}(Qx−b)||_inf < alpha·eps` and semantic error ≤ eps vs `Model.solve_exact` — zero
failures, for every backend's own final vector.**

## 0. Setup (Measured; charges per meter.py)

Outer loop (unregularized ACL target): S0=supp(s); solve `Q_SS x_S = b_S`; boundary residual
`r_w = beta·Σ_{u∈S~w} x_u/(sqd_u sqd_w)`; admit ALL w with `r_w/sqd_w ≥ 0.5·alpha·eps`; inner
solves to scaled-inf residual ≤ `0.1·alpha·eps` (CG final round auto-tightened if the cert needs
it; never triggered >1 retry). Termination certifies err < eps. One exact trace per config
(per-round splu); every backend replays the identical trace with its own meter. Common outer
ledger: admission scan d_v once (C_adj), per-round frontier rescan (R_adj) + C_rec per boundary
edge. Backends: **COLD-LU** charge nnz(L)+nnz(U) per round (stated proxy) + |S| materialize;
**CG-COLD/WARM** charge (nnz(Q_SS)+6|S|)/iter, Jacobi precond = identity since diag(Q) const;
**INC-LDL** incremental up-looking LDL^T in admission order, charge touched factor entries on
append (sparse-triangular reach), append-only forward solve, gate = partial backward solve on the
reverse closure D(frontier), charged; **TREE-INC** (trees) seed-rooted elimination DP: pivots
delta_u from children, admission = O(d_v) + upward delta-path truncated at relative change 1e-8,
one batched downward x-refresh pruned at 1e-8, gate on touched frontier, exact finalize;
**ORACLE-SDD** Σ_t cvol(S_t)·plog + per-round boundary rescan; **ORACLE-INC** (conj:aggregate
ideal) plog(cvolS*)·(cvol(S*) + cvol(∂-ever) + E), plog=log2(2+x). Graphs: path(6000, end-seed),
caterpillar(3000,1), spider(8,400), btree(depth 12), decoy_hub(50,300), theta(60,60,60),
grid(70x70).

## 1. E(eps): is the 1/eps^2 pessimism real? (Measured)

`E` = admission rounds; batch = all violators. eps = 2^-4..2^-10, saturated points (S stopped
growing) excluded from fits.

| graph | alpha | E over eps grid | E/\|S*\| | E ~ eps^-x | vol ~ eps^-x | meanT |
|---|---|---|---|---|---|---|
| path | 1e-2 / 1e-4 | 17..37 / 173..381 | **0.97 / 1.00** | 0.19 | 0.18/0.19 | 1.0 |
| caterpillar | 1e-2 / 1e-4 | 13..28 / 132..279 | 0.54 / 0.55 | 0.18 | 0.20 | 1.8 |
| spider | 1e-2 / 1e-4 | 6..27 / 65..277 | 0.12 | 0.33 | 0.33 | 8.0 |
| btree | 1e-2 / 1e-4 | 3..8 / 3..9 | **0.01–0.02** | 0.22/0.26 | 0.82/**1.02** | up to 114 |
| decoy_hub | 1e-4 | 37..49 | 0.14 | 0.08 | 0.83 | 1→7 (hub batch=300) |
| theta | 1e-2 | 11..32 | 0.33 | 0.25 | 0.24 | 3.0 |
| grid | 1e-4 | 15..154 | 0.03 | 0.68 | 1.34 | 4→36 |

- Path/decoy admit **one vertex per round** (E=|S*|): Wei–Yang's `E ≤ |S*|` is *tight* — the honest
  negative — but at fixed alpha |S*| ~ (1/sqrt(a))·log(1/eps), so E's eps-exponent is only ~0.2.
- The two ways E stays small: geometric value decay (E~log(1/eps), trees at fixed alpha) or doubling
  batches (E~log vol, btree/grid). **E ~ vol AND vol ~ 1/eps simultaneously requires alpha ↓ with
  eps** (diagonal regime, §3). `Σ_t vol(S_t) ≈ 0.5·E·vol(S*)` on one-at-a-time families
  (0.22–0.25 on btree) — the naive product is the right shape whenever E is large.

## 2. Fitted eps-exponents q (W ~ eps^-q), fixed alpha (Measured)

| graph, alpha | COLD-LU | CG-COLD | CG-WARM | INC-LDL | TREE-INC | OR-SDD | OR-INC |
|---|---|---|---|---|---|---|---|
| path 1e-4 | 0.37 | 0.56 | 0.58 | **0.19** | 0.36 | 0.40 | 0.22 |
| caterpillar 1e-4 | 0.36 | 0.56 | 0.60 | **0.21** | 0.38 | 0.40 | 0.23 |
| spider 1e-4 | 0.65 | 0.99 | 0.98 | **0.33** | 0.65 | 0.70 | 0.37 |
| btree 1e-4 | 1.03 | 1.25 | 1.25 | 2.72 (fill!) | **1.14** | 1.21 | 1.17 |
| theta 1e-2 | 0.45 | 0.70 | 0.61 | **0.25** | — | 0.52 | 0.28 |
| grid 1e-4 | 2.42 | 2.76 | 2.46 | 2.39 | — | 2.20 | **1.44** |

On trees, q(INC-LDL) ≈ q(vol) exactly (output-linear); q(COLD) ≈ q(E)+q(vol); nothing at fixed
alpha reaches q=2 except grid a=1e-4 (2D: vol~eps^-1.34 by mass, E~eps^-0.68 ⇒ product ~2).

## 3. Diagonal alpha = eps — where 1/eps^2 lives and dies (Measured)

Path (caterpillar analogous): E ~ eps^-0.69 ≈ vol ~ eps^-0.68 (both ~ log(1/eps)/sqrt(eps)).

| W ~ eps^-q | COLD-LU | CG-COLD | CG-WARM | INC-LDL | TREE-INC | OR-SDD | OR-INC |
|---|---|---|---|---|---|---|---|
| path | 1.28 | **1.97** | 1.78 | **0.68 = q(vol)** | 1.23 | 1.46 | 0.80 |
| caterpillar | 1.20 | 1.86 | 1.69 | **0.68 ≈ q(vol)** | 1.17 | 1.38 | 0.77 |

At eps=2^-12: INC-LDL 6059 (=10.5·vol, same constant as everywhere), COLD-LU 35x more, ORACLE-SDD
187x more, CG-WARM 3556x more. **The repeated factor is real exactly here, and the note's
append-only construction removes all of it — including the boundary-query cost (gate = 0.5·vol
total, D(F)=1 per round).**

## 4. Warm-start value law (Measured, 7101 pooled rounds)

| rel increment ||x_t − x_{t−1}||/||x_t|| | n | med it_warm | med it_cold | ratio |
|---|---|---|---|---|
| < 1e-4 | 258 | 8 | 319 | **39x** |
| 1e-4–1e-3 | 1114 | 20 | 225 | 9.6x |
| 1e-3–1e-2 | 2269 | 45 | 122 | 2.7x |
| ≥ 1e-2 (all big batches) | 3460 | ≤33 | ≤41 | **1.0x** |

`it_warm/it_cold ≈ ln(r0_warm/tol)/ln(r0_cold/tol)` — corr 0.862, slope 1.52: warm-starting buys the
**log of the residual-head-start, a constant factor**, exactly as the note's "energy is not work"
argument predicts. It never changes an exponent (diagonal q 1.78 vs 1.97; alpha exponent 0.38 vs
0.49). Batches that break it: btree — CG needs exactly `depth+1` iters warm or cold at every alpha
down to 2^-14 (per-round iters = 1,2,3,…,10 identically): the radial Krylov dimension is the binding
constraint, and the warm iterate lives in the same radial subspace. Alpha-free CG on btree is a
spectral accident (shell count < sqrt(kappa)), not warm-start value.

## 5. Alpha dependence at eps=2^-8 (Measured)

path: `it_cold ~ alpha^-0.49`, `it_warm ~ alpha^-0.38`, TREE-INC truncation radius
`up_mean ~ alpha^-0.51` (clean 1/sqrt(alpha)); grid: 0.37 / 0.20. btree: everything alpha-frozen
below 2^-8 (active set and iters alpha-independent — mass-split-limited).
**INC-LDL total = 10.5·vol at every alpha 2^-4..2^-14 on path: the exact incremental factorization
is alpha-free like Wei–Yang's SDD oracle, but with zero repeated factor.** The SDD-oracle emulation
confirms: repeated nearly-linear solves give W_orsdd ≈ (E/2)·cvol·plog regardless of solver
technology; only amortization (not solver speed) removes E.

## 6. INC-LDL structure: Expand vs Violations cost split (Measured, finest eps)

| graph (a=1e-4) | append/vol | gate/vol | max reverse-closure D | verdict |
|---|---|---|---|---|
| path | 3.5 | **0.5** | 1 | output-linear (= note Thm 7) |
| caterpillar | 8.6 | 0.8 | 3 | output-linear |
| spider | 48.8 (const/admission ≈ 98, |S|-indep) | 2.2 | 8 | output-linear |
| theta (cycle!) | 11.3 | 1.0 | 3 | output-linear |
| btree | **22195** (nnzL=|S|^2/4) | 57 | 512 | fill catastrophe |
| decoy_hub | **6776** (300^2 leaf clique) | 65 | 300 | fill catastrophe |
| grid | 1027 | 19.8 | 151 | ≈ COLD-LU, no gain |

**The Violations interface is cheap everywhere measured** (reverse-closure partial backsolve;
lazy variant ≈ eager, 0 misses on trees): on these traces the open bottleneck is *Expand*
(maintaining a fill-free factorization under append), not boundary queries — refining the note's
open-problem diagnosis. Caveat: batch admission empties the frontier quickly here; a
just-below-threshold pendant kept forever could still blow up D(F).

TREE-INC complement: btree 23.8·vol, decoy 69k vs INC-LDL 4.87M; but path/cat/spider pay
E·alpha^-0.5 (spider descent touches all 8 arms/round, touched≈|S|/2). Full passes = 2 always;
frontier verification error ≤ 2.6e-5.

## 7. Prize size for conj:aggregate (Measured, idealized ledgers on real traces)

ORACLE-SDD / ORACLE-INC at finest non-saturated eps:

| | path | cat | spider | btree | decoy | theta | grid |
|---|---|---|---|---|---|---|---|
| a=1e-2 | 13.0 | 12.3 | 12.3 | **0.9** | 3.3 | 13.5 | 10.1 |
| a=1e-4 | **133** | 120 | 126 | **1.0** | 21 | 26 | **76** |
| diag 2^-12 | 101 | 90 | | | | | |

Prize ≈ E/(2·plog): large exactly where admissions are increment-like (E large), zero where batches
double. Realized-vs-ideal gap: on path/cat/spider/theta INC-LDL already sits within ~2–10x of
ORACLE-INC; on grid the best real backend is 55x above ORACLE-INC (unclaimed); on btree COLD-LU
already beats both oracles' ledgers (E=9).

## 8. Honest negatives

1. E=|S*| exactly on endpoint path and decoy (one-at-a-time admission) — Θ(vol) expansions, as the
   note's Thm `path-materialization` family predicts.
2. Admission-order append-only LDL^T (the natural generalization of the note's path recurrence) is
   **quadratic on any branching growth** (btree, hub) — the elimination order that makes appends
   O(1) on paths is root-first and hence maximal-fill on trees. Order and appendability conflict.
3. Warm-started CG saves exactly nothing (ratio 1.0) on every round with relative increment ≥ 1e-2,
   i.e., all doubling batches.
4. Grid: no implemented incremental structure beats fresh COLAMD splu (fill of any fixed
   admission-compatible order ≈ refactor cost); only the oracle ledger shows a 76x headroom.
5. theta a=1e-4 and grid a=1e-4 eps≤2^-9 saturate the graph (marked, excluded from fits).
6. No certificate failures anywhere (126/126 pass), including CG backends' own final vectors.

## 9. Sharpest next falsifiable target for conj:aggregate

The data isolate the missing object precisely: a **dynamic-order incremental LDL^T on trees** —
append vertices at the frontier *while re-rooting the elimination order away from branch points* —
with amortized O(polylog) reorder work per admission. Falsifiable prediction: such a structure
achieves W ≤ C·cvol(S*)·polylog, alpha-free, simultaneously on path, caterpillar, spider, btree,
decoy_hub (each currently served by one of two mutually-incompatible orderings; min over my two
backends already achieves it per-family, max instance gap = btree-vs-path). Adversarial instance to
test first: **comb with teeth of length ~1/sqrt(alpha)** (backbone + long pendant paths, seed at
backbone end) — growth alternates between backbone and ~sqrt(vol) interleaved teeth; predicted
quadratic-ish for BOTH admission-order LDL (interleaved chain fill) and seed-rooted DP (update
paths), while conj:aggregate demands ~cvol/sqrt(alpha). If the comb kills both, the cyclic case is
moot until trees are solved; if a top-tree/multifrontal variant survives the comb, extend to theta
(already output-linear for INC-LDL: cyclic per se is NOT the obstacle — width is: grid). The
boundary-violation dictionary is empirically NOT the bottleneck (gate ≤ 2.2·vol on all trees) and
can be deprioritized.
