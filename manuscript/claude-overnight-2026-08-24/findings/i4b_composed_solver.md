# I4-B — ONE composed local PPR solver, fully charged on eleven coordinates

**Evidence: Measured** (84 cells × 7 methods, every certified run verified
against the exact solve, 372 verifications, 0 violations).
**Proved-draft** for the charging arithmetic in §9 only.
This is an empirical composition, not a theorem.

Code `i4b_composed/{ledger,composed,run,fit,hub,smoke}.py`; data
`i4b_composed/out/{i4b_main.json,hub.json,tables.txt}`; logs
`out/{main,hub}.log`. Sweep wall 1 015 s (14 families × 3 α × 2 ε × 7
methods); composed-solver-only wall 674 s.

---

## 0. VERDICT

**The composition works, is α-free, and is the only method in the campaign
that is never catastrophic — but it does not dominate the per-cell
hindsight-best baseline, and it loses badly to `push` on the high-treewidth
families at moderate α.**

1. **α-freedom, achieved uniformly.** Fitted exponent of `W/vol(S_eps)` in
   `α^{-q}`: **median q = 0.03, range −0.18 … +0.18** across all 14 families.
   Baselines: push 0.96, WY-style active set 1.17, forced-AMG 0.20,
   I3-A stand-alone AMG 0.18. **No family has q > 0.18.**
2. **Output-linearity with a usable constant on 10 of 14 families.**
   `W/vol(S_eps) = 14.5 … 159` (median 52) on the ten low-treewidth families
   — path, caterpillar, comb, spider, star, θ, prism, binary tree, random
   recursive tree, decoy-hub. On the four high-treewidth families (2-D and
   3-D grids, 3- and 4-regular expanders) it is **257 … 2 357** (median 648).
3. **The triage is cheap and decisive.** Cost of the test: **median 1.7 %,
   max 16.8 % of `W`.** Benefit: the ratio between the two forced routes is
   **1.2× … 3 170×** and the composed solver lands within **0.94–1.09× of the
   better forced route** in every cell. Question (a) is answered YES with a
   large margin.
4. **The decision does flip mid-run, exactly once, and it is cheap.**
   24/84 cells flip; **max flips per run = 1**, always ELIM→AMG, never back;
   the charged write-off of the discarded response state is **≤ 0.12 % of
   `W`**. Question (c)'s fear is real but small — *provided* the growth is
   batched (see 5).
5. **A naive composition really does lose to its own components.** With pure
   gate-violator admission and no geometric batching, `W` is **up to 13.4×
   larger** (path/decoy-hub 13.4×, caterpillar 11.9×, θ 9.8×, spider 9.0×) —
   worse than the stand-alone elimination baseline it contains. The
   refactorisation tax is the composition's dominant failure mode and the
   geometric batch rule is what removes it.
6. **The kinetic gate is free but, in this zoo, not decisive.** Push-gate vs
   pull-gate on identical trajectories: **push is cheaper in 42/42 cells but
   by only 0.0–6.7 % (median 0.14 %)**, including a purpose-built hub-path
   family with `vol(∂S)/|∂S|` up to 1 024. Honest reading in §6: the 266×
   of I3-B needs high-degree boundary vertices that stay *unadmitted*, which
   the ε-certified PPR stopping rule does not produce. The gate still
   **strictly dominates** (never worse) and it is what makes `R_adj ≡ 0`.

---

## 1. Architecture

```
  S = {v};  loop:
    (ii) TRIAGE(S)  on a 4x-volume ladder  ->  route in {ELIM, AMG}
         [flip => write off the discarded factor/hierarchy]
    interior solve on S:  ELIM = fill-reducing sparse LU (fill-free on a
         forest);  AMG = I3-A smoothed-aggregation V-cycles, stopped early
         by the gate when the boundary residual already exceeds the target
    (i)  KINETIC GATE: push P_j = sum_{i in S} Q_ji x_i along cross edges
         (never scan a boundary adjacency list); g_j = |b_j - P_j|/sqrt(d_j)
    (iii) if max(interior, boundary) |D^{-1/2}(Qx-b)| < alpha*eps  -> EMIT
         else admit every j with g_j > alpha*eps, then batch the closure by
         predicted gate value until vol(S) has grown 1.5x
```

Three details matter and are all charged.

**(i) The gate.** After a Dirichlet solve on `S` the residual is *exactly*
zero on `S` (ELIM) and supported on `∂S`, so `max_{S ∪ ∂S}` is the true
global certificate: for `j ∉ S ∪ ∂S`, `x` has no neighbour in `S`, so
`r_j = 0`. The accumulators are updated by pushing along cross edges — cost
`crossdeg(S) = Σ_{i∈S}|N(i)\S| ≤ vol(S)` per solve (I3-B P1), *inside* the
interior's own row work; a newly exposed boundary vertex initialises in
`O(1)` because its only `S`-neighbour is the vertex that just exposed it
(I3-B P3). **No structure ever scans a boundary vertex's adjacency list**,
which is why `R_adj = 0` in every composed run (§2).

**(ii) The triage** is a two-step ball-treewidth test.
*Step 1 — Euler/forest test*, `O(|S| + m)` by union-find: the cyclomatic
number `cyc = m − n + c`. `cyc = 0` ⟺ the region is a forest ⟺ the
seed-rooted order is fill-free ⟹ ELIM immediately. (Also `|V(kernel after
degree-≤2 contraction)| ≤ 2·cyc` and `tw(S) ≤ cyc+1`, so small `cyc` is
already a width certificate — this is the "2-core peeling to the
≤2-irreducible kernel" the direction asked for, evaluated through its Euler
characteristic instead of by explicit peeling, which is strictly cheaper.)
*Step 2 — budgeted greedy min-degree symbolic elimination*, accumulating the
exact factor flop count `Σ_v deg(v)²` and **aborting the instant it exceeds
`budget = min(κ·vol(S), 3·10^5)`**, `κ = 8`. Completing within budget is a
constructive certificate that elimination is affordable (ELIM); aborting is a
one-sided witness of high fill (AMG). The charged cost is the work actually
done and is `≤ budget` **by construction**.

**(iii) Termination** is the repository's standard certificate,
`||D^{-1/2}(Qx̂−b)||_∞ < α·ε ⇒ max_i |π̂_i−π_i|/d_i < ε`, evaluated over
`S ∪ ∂S` only. Every method in the comparison uses the same rule except
`push`, which uses the ACL residual invariant `r_j ≤ ε d_j` (equivalent up
to the constant `γ_α = 2α/(1+α)`; both were verified against the exact solve
and neither ever violated ε).

*(A note I checked and discarded: because the ELIM route makes the residual
exactly non-negative, one is tempted to invoke the ACL symmetry/stochasticity
argument for a sharper certificate. Worked through, it gives
`||D^{-1}(π−π̂)||_∞ ≤ (1+α)/(2α)·||D^{-1}r_mass||_∞`, i.e. **exactly the same
`α·ε` threshold**. Non-negativity buys tightness of the bound, not a better
constant. Recorded so nobody re-derives it.)*

---

## 2. The eleven-coordinate ledger

`W = C_adj + R_adj + R_int + C_pre + C_ctl + C_rec + C_resp + C_mat + C_emit`.
`M_pers`/`M_tmp` are space (cells) and are **not** summed into `W`.
Full table: `out/tables.txt` TABLE 2. Two representative rows and the shape
of each regime:

| family | α | ε | C_adj | R_adj | **R_int** | C_pre | C_ctl | C_rec | C_resp | C_mat | C_emit | **W** | M_pers | M_tmp |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| comb (ELIM) | 2⁻¹² | 1e-6 | 4.9e3 | **0** | **0** | 0 | 2.19e4 | 2.67e4 | 8.74e4 | 2.67e4 | 2.45e3 | 1.70e5 | 1.47e4 | 9.8e3 |
| rrt (ELIM) | 2⁻⁸ | 1e-6 | 8.0e4 | **0** | **0** | 0 | 5.77e5 | 3.92e5 | 1.30e6 | 4.04e5 | 4.0e4 | 2.79e6 | 2.4e5 | 1.6e5 |
| grid2d (AMG) | 2⁻⁸ | 1e-6 | 1.87e5 | **0** | **1.65e7** | 0 | 1.30e6 | 5.78e6 | 1.28e7 | 2.16e6 | 4.7e4 | 3.88e7 | 3.8e5 | 3.2e5 |
| rand_reg3 (AMG) | 2⁻⁸ | 1e-6 | 6.0e4 | **0** | **5.18e6** | 0 | 4.00e5 | 1.54e6 | 2.15e7 | 8.4e5 | 2.0e4 | 2.95e7 | 1.4e5 | 1.8e5 |

Structural read-off, and it is the cleanest thing the eleven coordinates buy:

* **`R_adj = 0` in all 84 composed runs.** The solver never re-reads a
  non-active adjacency row. This is the gate's signature; the pull variant
  has `R_adj > 0` in every cell.
* **`R_int = 0` on the ELIM route.** The local matrix is assembled
  *incrementally* — admitting `j₀` writes its own row and the `d_{j₀}`
  reciprocal entries, so old active rows are never re-read. On the AMG route
  `R_int` is **42–77 % of `W`**: it is the level-0 smoother/residual passes,
  and it is the reason the high-treewidth regime is 10–40× more expensive per
  unit of output.
* `C_ctl` is 0.9–20 % of `W` and splits as triage (median 1.7 %), gate
  (0.5–20 %), certificate (0.2–7 %).
* `C_resp` (factor flops, hierarchy setup, coarse solves, switch write-offs)
  is 40–73 % of `W` in both regimes — the composition is response-dominated,
  as expected.
* `C_pre = 0` for every method: nothing is precomputed globally.

**Where the mapping is approximate — stated explicitly.**

1. **`R_adj` vs `R_int` is a role split of one physical operation.** Both are
   "re-read an adjacency row". We assign a re-read to `R_int` iff the vertex
   is in the active set at the time of the read, else to `R_adj`. A different
   repository convention (e.g. charging boundary re-reads to `R_int` when
   the boundary is treated as part of the region) would move mass between
   these two coordinates without changing `W`.
2. **`C_ctl` absorbs the gate's accumulator pushes.** Each pushed cross edge
   is *also* reported as `piggy` (0.1–3.4 % of `W`), because it happens
   inside an interior row scan already charged. The headline `W` therefore
   **double-counts** those edges — a deliberate over-charge.
3. **AMG hierarchy setup is charged to `C_resp`, not `C_pre`.** It is a
   preconditioner update, and it is seed-local and rebuilt per region, so it
   is not global preprocessing. `C_pre` is reserved for global work and is 0.
4. **`M_pers`/`M_tmp` are peak cell counts** (one float or one index = 1
   cell), sampled once per round; they are not integrated over time.
5. **The baselines are mapped from 6 counters, not measured on 11.** `push`
   (the C kernel) exposes only `C_adj`/`R_adj`; `amg`/`direct` from I3-A
   expose `C_adj,R_adj,C_rec,C_resp,C_mat`. For those rows `R_int`, `C_ctl`
   and `C_pre` are 0 by construction and `M_pers`/`M_tmp` are unmeasured
   (NaN). `W` is identical to the earlier `VecMeter.total()` in every case,
   so the comparison tables are consistent; only the *decomposition* of the
   baselines is coarser than the composed solver's.

---

## 3. Comparison (Measured) — `W / vol(S_eps)`

Abridged from TABLE 1 (`out/tables.txt` has all 84 cells). `nan` = the method
hit its wall cap or refused to certify.

| family | α | vol(S_ε) | **COMPOSED** | comp_E (forced elim) | comp_A (forced AMG) | WY-style | push | AMG (I3-A) | direct (I3-A) |
|---|---|---|---|---|---|---|---|---|---|
| star | 2⁻¹² | 200 000 | **14.5** | 14.5 | 26.0 | nan | nan | 20.5 | 11.5 |
| path | 2⁻⁴ | 49 | **52.6** | 51.8 | 61.1 | 759 | 94 | 111 | 50.4 |
| path | 2⁻¹² | 617 | **52.1** | 50.2 | 300 | nan | nan | 296 | 49.4 |
| caterpillar | 2⁻¹² | 843 | **66.6** | 64.2 | 631 | nan | nan | 480 | 47.8 |
| comb | 2⁻¹² | 1 975 | **86.1** | 84.0 | 899 | nan | nan | 565 | 58.0 |
| spider | 2⁻¹² | 3 018 | **106** | 104 | 703 | nan | nan | 399 | 60.4 |
| θ | 2⁻¹² | 1 641 | **67.5** | 65.1 | 530 | nan | nan | 372 | 55.5 |
| prism | 2⁻¹² | 2 526 | **68.4** | 64.6 | 414 | nan | nan | 327 | 78.0 |
| binary tree | 2⁻¹² | 131 068 | **28.9** | 28.4 | 966 | nan | nan | 1 003 | 25.5 |
| rrt | 2⁻¹² | 73 045 | **38.3** | 37.8 | nan | nan | nan | nan | nan |
| grid2d | 2⁻⁸ | 16 468 | **2 357** | 14 193 | 2 222 | 4 528 | **584** | **419** | 1 782 |
| grid2d | 2⁻¹² | 96 388 | **2 143** | 25 652 | 2 128 | nan | nan | **922** | 18 487 |
| rand_reg3 | 2⁻¹² | 60 000 | **504** | 602 602 | 524 | 13 710 | nan | nan | nan |
| rand_reg4 | 2⁻¹² | 80 000 | **591** | 1 684 846 | 581 | 11 784 | nan | nan | nan |
| grid3d | 2⁻¹² | 403 440 | **257** | 174 153 | 258 | nan | nan | nan | nan |

**Dominance (TABLE 7, median of `W_comp/W_baseline` per family, then over
all cells):**

| baseline | comp_E | comp_A | WY | push | AMG (I3-A) | direct (I3-A) | best-per-cell |
|---|---|---|---|---|---|---|---|
| median ratio | **1.02** | **0.32** | **0.07** | **0.54** | **0.27** | **1.13** | **1.20** |

Read this honestly:

* Against the **hindsight-best single mechanism chosen per cell**, the
  composed solver's median is **1.20×** and its worst family is grid2d at
  **5.78×** (grid3d 1.79×, prism 1.31×, comb/spider 1.29–1.51×). **It does
  not dominate.** Its claim is *uniformity*: it is the only method with a
  finite, α-free `W/vol` in all 84 cells.
* It is 2 % worse than forced elimination on the families where elimination
  is right (that 2 % is the triage), and 1 000–3 000× better where it is not.
* It beats WY-style by 14×, forced AMG by 3×, I3-A's stand-alone AMG by 3.7×.
* **`push` beats it by 5.9× (grid2d), 5.7× (rr3), 8.2× (rr4), 15.6× (grid3d)
  at the α values where push can still be run.** Push's exponent is 0.96, so
  the crossover moves with α: on grid2d push is 54 W/vol at α = 2⁻⁴, 584 at
  2⁻⁸, and infeasible at 2⁻¹². The composed solver's advantage on those
  families is entirely in the α-limit, not at α = 2⁻⁴.

**α-exponents (TABLE 3), median over families:**

| method | comp | comp_E | comp_A | WY | push | AMG (I3-A) | direct (I3-A) |
|---|---|---|---|---|---|---|---|
| q (median) | **0.03** | 0.04 | 0.20 | 1.17 | 0.96 | 0.18 | 0.03 |
| q (max over families) | **0.18** | 0.58 | 0.43 | 1.24 | 1.18 | 0.30 | 0.67 |

The composed solver is the only method whose *maximum* exponent over the zoo
stays below 0.2. `direct` matches its median but blows up on grid2d (0.67);
`comp_E` is `direct` inside this architecture and shows the same 0.58.

---

## 4. Question (a): does the triage cost less than the decision saves?

**YES, by 1–3 orders of magnitude.** (TABLE 4.)

| quantity | value |
|---|---|
| triage cost as % of `W` | min 0.0, **median 1.7**, max 16.8 (prism, α = 2⁻⁴) |
| `W(wrong route)/W(right route)` | **1.18× … 3 170×** |
| `W(best forced route)/W(composed)` | **0.94 … 1.09** (median 0.98) |

The last row is the sharp statement: the composed solver recovers **94–109 %**
of the benefit of knowing the right mechanism in advance. On `rand_reg3` and
`rand_reg4` it is *better* than forced AMG (ratio 1.04–1.09) because the first
7–11 rounds run on a ball that genuinely is a tree, where elimination is free.

Where the triage is expensive: the prism/`double_cycle` (16.8 % at α = 2⁻⁴)
and `comb` (5.3 %). Both are cells where the min-degree simulation *completes*,
and a completed symbolic min-degree costs about what the numeric factorisation
it predicts costs. The 4×-volume ladder (§9 A2) is what keeps this at a
constant multiple of the output rather than a per-round tax; at the 1.5×
ladder used in the first build the same cells cost 32 % of `W`.

---

## 5. Question (c): the ball's structure changes — how often does the route
flip, and what does the switch cost?

| statistic | value |
|---|---|
| cells that flip at all | **24 / 84** |
| maximum flips in any run | **1** |
| direction | **always ELIM → AMG, never back** |
| charged write-off of discarded response state | 920 … 1.82·10⁴ units = **≤ 0.12 % of `W`** |
| where | grid2d (after 7 rounds), grid3d (6), rand_reg3 (11), rand_reg4 (7) |

Route strings are stable and readable, e.g. `rand_reg3`
`EEEEEEEEEEEAAAA` and `grid2d` `EEEEEEEAAAAAAAAAAAAAAAAAA` at every
(α, ε). The mechanism: a small ball in a 3-regular expander or a grid **is**
a tree or near-tree, so the Euler fast path fires; once the ball closes
enough cycles the min-degree budget blows and the route switches for good.

Monotonicity is half-provable: `cyc(S) = m−n+c` is non-decreasing under
vertex addition, so the *forest* fast path can only ever stop firing, never
resume. The min-degree budget test is **not** formally monotone (relative
fill can fall as a region grows), so "at most one flip" is **Measured
(84/84)**, not proved.

**The refactorisation tax — the real composition overhead.** Turning off
geometric batching (`comp_nb`: admit exactly the gate violators, re-solve
every round) multiplies `W` by:

| path / decoy_hub | caterpillar | θ | spider | rrt | prism | comb | rr3 | rr4 | grid2d | star | binary tree |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **13.4×** | 11.9× | 9.8× | 9.0× | 7.0× | 6.9× | 3.9× | 1.79× | 1.38× | 1.20× | 0.97× | **0.85×** |

Un-batched, the path costs 702 `W/vol` — worse than the elimination
component it contains (50). **A naive composition does lose to its own
components**, exactly as the direction anticipated, and the fix is the
geometric batch, not the mechanisms. On the two families where the region is
the whole graph in one step (star, binary tree) batching is a 3–15 % *loss*.

---

## 6. The kinetic gate inside the composition — an honest negative

Push-gate vs pull-gate on **identical trajectories** (the only difference is
whether boundary residuals are read from accumulators or recomputed by
scanning `N(j)`), 42 comparable cells:

| statistic | value |
|---|---|
| cells where push ≤ pull | **42 / 42** |
| `W_pull / W_push` | min 1.0000, **median 1.0014**, max **1.0667** |

And on a purpose-built adversary (`hub.py`, `hubpath(400, D)`: a path with a
degree-`D` hub pendant on every vertex, so `vol(∂S)/|∂S|` can reach `D`):

| D | 4 | 32 | 256 | 1024 |
|---|---|---|---|---|
| `W_pull/W_push` | 1.01 | 1.00–1.01 | 1.01 | 1.01 |

**Why the 266× of I3-B does not appear here.** In I3-B the hubs were tuned
(by bisecting `ρ`) to sit *just below* the RPPR activation threshold, so they
stayed on the boundary and were rescanned forever. Under the ε-certified PPR
rule the same hubs are either **admitted** on the first round they matter (and
then their `d_j` is a one-off `C_adj`, identical for both gates) or they are
so far below threshold that they are pendant leaves of degree 1. In every
family in the zoo the *unadmitted* boundary turned out to satisfy
`vol(∂S) ≈ |∂S|`.

Conclusion, stated carefully: **the kinetic gate is the right default — it is
never worse, it costs 0.5–20 % of `W`, it is what makes `R_adj ≡ 0`, and it
removes an unbounded worst-case term — but on this zoo under this stopping
rule it buys ≤ 6.7 %.** Its measured 266× lives in the RPPR/`ρ`-threshold
regime (I2-A's marginal-hub ring), not in generic ε-certified PPR.

---

## 7. Correctness

* **372 certified runs** verified against the exact solve
  (`spsolve` for `n ≤ 8 000`, CG to `rtol = 1e-14` above).
* **0 violations** of `max_i |π̂_i − π_i|/d_i ≤ ε`.
* Max `err/ε`: composed **0.233**, comp_E 0.233, comp_A 0.233, comp_pull
  0.233, comp_nb 0.154, WY 0.500, push 0.924.
* Certificate used: `||D^{-1/2}(Qx̂−b)||_∞ < α·ε` evaluated over `S ∪ ∂S`,
  which is exact because the residual vanishes identically outside
  `S ∪ ∂S`. **No cell required a proxy certificate**; every cell in this
  sweep was small enough for an exact reference solve.
* The `decoy_hub` family is *locally identical to `path`* at every (α, ε)
  measured — the decoy hub sits at distance 10 000 from the seed and is
  never inside the ε-level set — so its rows duplicate `path` exactly. This
  is a property of the I3-A zoo configuration, inherited, and it means
  **the zoo contains no cell in which a high-degree vertex is a live
  boundary decision**. Fixing that is a prerequisite for any future claim
  about the gate (see §10).

---

## 8. Regimes covered, and where it still fails

**Fully charged, output-linear (`W/vol(S_ε)` = 14.5–159), α-free
(`q ≤ 0.13`), certified — for all α ∈ {2⁻⁴, 2⁻⁸, 2⁻¹²} and both ε:**
path, caterpillar, comb, spider, star, θ, prism/double-cycle, binary tree,
random recursive tree, decoy-hub. That is **60 of 84 cells**, i.e. every
family whose seed-local ball has bounded treewidth or is a forest. On these
the composed solver is within **1.02× (median; 1.20× worst) of forced
elimination** and beats
push by 1.9–26× and WY by 14–450×.

**Charged and α-free but NOT output-linear at a usable constant
(`W/vol(S_ε)` = 257–2 357):** 2-D grid, 3-D grid, 3-regular and 4-regular
random graphs — 24 cells. Here the interior is AMG and `R_int` (level-0
smoother passes) is 42–77 % of `W`. The exponent is fine (`q ≤ 0.18`); the
constant is 10–40× the low-width regime. **`push` is 5.7–15.6× cheaper on
these families wherever `1/(αε)` is small enough to run it**, so at α = 2⁻⁴
the composed solver is simply the wrong tool; it only wins in the α-limit.

**Still failing outright:**
* **The high-treewidth constant.** 2 357 `W/vol` on grid2d at α = 2⁻⁸ is
  5.6× worse than I3-A's stand-alone local AMG (419) on the same cell. The
  composition *costs* us there: gate-driven active sets on a grid need
  23–26 hierarchy rebuilds against amg_local's BFS-ball ladder, and the
  region overshoot `vol(Ω)/vol(S_ε)` reaches **11.4×** (vs 2.9× for
  amg_local). **This is the clearest place the composition overhead eats the
  gains.**
* **Region overshoot in general.** `vol(Ω)/vol(S_ε)` is 1.0–4.6 on the
  low-width families but 8.4–11.4 on grid2d at α ≤ 2⁻⁸ — partly the α·ε vs ε
  level-set gap that every residual-certified method pays, partly the 1.5×
  batch.
* **No `1/√α` claim is supported.** Nothing here demonstrates the
  `Õ(1/(√α ε))` target. What is demonstrated is `α^{±0.2}` *for
  `W/vol(S_ε)`*, i.e. the α-dependence has been pushed entirely into the
  size of the output support, not eliminated from the problem.
* **Scale.** Everything is ≤ 4·10⁵ `vol`; the exact reference solve is the
  binding constraint on going bigger.

---

## 9. Charging arithmetic (Proved-draft)

**A1 (gate).** Per solve, gate work is `crossdeg(S) = Σ_{i∈S}|N(i)\S| ≤
vol(S)`, with no `vol(∂S)` term, because every cross edge is counted once in
`vol(S)`. The pull alternative costs `vol(∂S)`, which is unbounded relative
to `vol(S)`. Newly exposed boundary vertices initialise in `O(1)`
(I3-B P3). ∎

**A2 (triage).** One triage costs `≤ min(κ·vol(S), C_abs)` by the abort rule.
With the `g_tri = 4` volume ladder the ladder volumes satisfy
`V_k ≤ V_final/4^{K−k}`, so the total triage bill is
`Σ_k κ V_k ≤ κ V_final Σ_{j≥0} 4^{−j} = (4/3)κ·vol(S_final)`.
**Triage is `O(vol(S_final))` — a constant multiple of the output, never
asymptotically dominant.** Measured: median 1.7 % of `W`. ∎

**A3 (number of solves).** The batch rule admits until `vol(S) ≥ 1.5·vol` at
the last solve or the closure budget `(1.5−1)·vol` is spent, so each round
either grows the volume by 1.5× or exhausts a budget proportional to the
current volume. Hence `#solves ≤ log_{1.5} vol(S_final) + O(1)`. Measured:
2–26 rounds, matching `log_{1.5}` of the final volume to within a factor 1.3.
∎ (The closure-budget branch is where the bound is loose; that is the residual
gap between this and a true incremental factorisation.)

**A4 (switch).** A flip charges the full cell count of the discarded factor
or hierarchy as `C_resp`, plus the new mechanism's setup at full price.
Measured ≤ 0.12 % of `W`. ∎

**Not proved:** that the refactorisation total `Σ_rounds fill(S_r)` is
`O(fill(S_final))`. With a 1.5× volume ladder it is a geometric sum *only if*
`fill` is superlinear in `vol`, which is exactly the case the triage routes
away. Empirically `Σ_rounds fill / fill(S_final) ≈ 3`. A genuinely
incremental elimination — I2-B's **HSEG-LDL**, `q = 0.92–1.11` on every tree
family — would remove this factor on the ELIM route; it is not wired in here
and that is the single largest identified saving left on the table (§10).

---

## 10. Next targets, in priority order

1. **Wire HSEG-LDL (I2-B) into the ELIM route.** The measured
   refactorisation total is ≈ 3× the final factorisation. An incremental
   factorisation carried across rounds should take the low-width families
   from `W/vol ≈ 52` to `≈ 20–25`, i.e. below `direct` and at I2-B's
   `q ≈ 1` exponent, and would let the batch factor drop to 1.0 (pure
   gate-driven growth) without the 13.4× tax.
2. **Fix the high-treewidth constant.** Either (a) reuse the AMG hierarchy
   across rounds by building it on a ball that is a *superset* of the
   predicted final region, or (b) let the triage return a third route
   (`push`) when `1/(αε) < c·vol(S)`, since push beats the composition by
   5.7–15.6× on exactly those families at moderate α. (b) is cheap and
   would remove the only regime where the composition is beaten by an order
   of magnitude.
3. **Build a zoo cell where a high-degree vertex is a live boundary
   decision** (hub at distance 3–5 from the seed, tuned so `π_h/d_h ≈ ε`).
   Without it, no claim about the kinetic gate's magnitude in ε-certified
   PPR is testable, and §6's negative stands only for the current zoo.
4. **Re-run the I3-A baselines on the eleven-coordinate ledger** so the
   comparison is not partly 6-counter. Only the decomposition is affected,
   not `W`, but the promotion standard asks for the full vector.
