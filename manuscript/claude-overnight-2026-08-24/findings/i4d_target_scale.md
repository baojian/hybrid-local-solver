# I4-D — Is the field's target scale set too low?  The output measure, the corrected target, and where the remaining `1/sqrt(alpha)` actually lives

**Direction:** a NEW direction raised by the campaign's own iteration-1..3 results
(I2-E's alpha-free `Theta(1/eps)` spiders, I3-A's alpha-free `W/vol(S_eps)`,
I2-B's output-linear HSEG-LDL, I2-F/W8's "vacuously loose" classic target).
The question: **can total charged work be `O~(1/eps)` with alpha-free constants
in general, rather than the conjectured `O~(1/(sqrt(alpha)*eps))`?**

Code: `/home/claude/work/overnight/i4d/{fam.py, run_out.py, fit_out.py,
run_work.py, run_ridge.py, adv.py, summarize.py}`.
Data/logs: `i4d/out/{out_measure.json, fit_out.json, run_out.log, run_work.log,
run_ridge.log}`.
Conventions as W1–W8 / I2-F / I3-A: `Q = (1+a)/2 I - (1-a)/2 D^{-1/2}AD^{-1/2}`,
`b = a D^{-1/2}e_v`, `pi = D^{1/2}x`, semantic err `= ||D^{-1/2}(x-x*)||_inf
= max_i |pi_hat_i - pi_i|/d_i`.  Meter as I3-A (scans charge `d_u`; every
coarse/factor/transfer/certificate op charged at its true count).
One surgical change to the shared arsenal: `amglib.VecMeter` gained a
`ring_scan(idx)` hook, **default-identical** to `scan_idx` (so every earlier
I3-A number is unchanged), used below by a `DQMeter` that charges the
boundary ring `O(1)` per vertex instead of `d_u` — see Lemma C.
**Every reported run was verified against the exact solve; the `!` marks in the
tables flag the (few) runs that did not certify and are excluded from all
"best mechanism" claims.**

---

## VERDICT (short)

1. **The task brief's premise is inverted, and this is the single most
   important thing in this report.**  It is **not** true that `vol(S_eps)`
   "can be much larger" than `1/eps`.  The correct statement is
   **`vol(S_eps) < 1/eps` unconditionally**, on every graph, every seed, every
   `alpha`, and the *degree volume* is the *larger* of the two candidate output
   measures (`|S_eps| <= vol(S_eps) < 1/eps`).  Measured: **545 clean cells, 14
   families, 0 violations, max `vol(S_eps)*eps = 0.60`.**
2. Hence **`O~(1/eps)` is type-correct as a target**, and since
   `1/(sqrt(alpha)*eps) >= 1/eps` for every `alpha <= 1`, the classic FY22
   target is **never tight against the output**: it leaves a factor
   `1/sqrt(alpha)` of unused headroom on *every* instance, not just on grids.
3. **Measured, the corrected target holds on every family tested.**  Along each
   family's *output-saturating ridge* (where `vol(S_eps) = Theta(1/eps)` and the
   target is hardest), the best mechanism's total charged work satisfies
   `W*eps ∈ [10.3, 82]` with log-log slopes **0.00 (star), 0.068 (2-D grid),
   0.21-and-falling (path)** — flat or sub-polynomial, i.e. `O~(1/eps)`.
4. **But no single mechanism achieves it, and the gap is now sharply located.**
   The mechanisms that are alpha-free (elimination, local AMG) select their
   region by BFS ball and are **not output-bounded** — the *ball trap* family
   drives their work to `1.5e5/eps` while the correct output is *empty*.  The
   mechanism that is output-bounded (push) is **not alpha-free**.  Nothing in
   the arsenal is both.
5. **Where the missing `1/sqrt(alpha)` actually lives (new, Measured).**  On the
   exact minimal region `S = S_eps` the repository's sufficient certificate
   **fails on the optimal output itself in 11 of 13 test cells** — it demands a
   residual `~alpha*eps` while the optimal output only achieves `0.06*eps`.  The
   true amplification is `A = err/theta ∈ [1.6, 17] = Theta(alpha^{-1/2})` on
   path / spider / caterpillar / grid2d / rrt, i.e. `4-330x` below the
   worst-case `Theta(alpha^{-1})` the rule assumes.  **But it is NOT universally
   so**: on `hidden_hub` (high-degree ring) `A = Theta(alpha^{-0.97})` and the
   rule is tight to 7 %.  So the `1/sqrt(alpha)` gap between self-certified and
   oracle-stopped work is a *stopping-rule* artifact on ordinary families and a
   *real* cost on high-degree boundaries — the fix is a computable
   instance-adaptive amplification bound, not a uniform relaxation (SP1, §8).
6. **Model precondition, now explicit and mandatory.**  `vol(dS_eps)` (the
   boundary RING volume) is **not** bounded by `1/eps` — measured up to
   `159 x (1/eps)` on the ordinary zoo and unboundedly on the *hidden hub*.  So
   `O~(1/eps)` is achievable **only in the model with an `O(1)` degree query**.
   In a pure scan-only model no bound in `1/eps` alone can exist.

Evidence grade: **Proved-draft** for §1–§3 (the output bound, the uphill lemma,
the boundary-sufficiency and certification lemmas — all short and checked
numerically); **Measured** for §4–§6; **Open** for the verdict's positive half.

---

## 1. The output bound (Proved-draft; 545/545 cells confirm)

**Lemma A (output-volume bound).**  Let `G` have no isolated vertices, let
`s >= 0` with `1^T s = 1`, `alpha ∈ (0,1]`, and let `pi` be the source-aligned
PPR vector, `u = D^{-1} pi`.  For `eps > 0` put `S_eps = {v : u_v > eps}`.  Then

>  `eps * vol(S_eps) = eps * sum_{v ∈ S_eps} d_v  <  sum_{v ∈ S_eps} d_v u_v
>   <= sum_v pi_v = 1`,
>  hence   **`vol(S_eps) < 1/eps`**   and   **`|S_eps| <= vol(S_eps) < 1/eps`**.

*Proof.* `pi >= 0` and `1^T pi = 1` (from `pi = gamma s + c_a A D^{-1} pi` and
`1^T A D^{-1} = 1^T`: `1^T pi = gamma/(1-c_a) = 1`).  `d_v u_v = pi_v`, and on
`S_eps` each `pi_v > eps d_v`.  ∎

**Lemma B (minimality).**  Any `eps`-valid output must list every `v ∈ S_eps`
(a coordinate left at zero contributes error `u_v`).  So `S_eps` is *exactly*
the minimal support, and `vol(S_eps)` / `|S_eps|` are the two honest output
measures.

**Consequence — the correct target is type-correct.**  Both candidate output
measures are `< 1/eps` on every instance.  The brief's worry ("if the honest
output measure is degree volume the target may be unachievable for a trivial
reason") **does not arise**: degree volume is the larger measure and it is
still below `1/eps`.  The two measures do diverge — `|S_eps|` can be far below
`vol(S_eps)` on high-degree supports — but *both* stay under the bar.

**Measured (E1: 14 families x 9 alphas x 7 eps, exact solves, 545 clean cells):**

```
GLOBAL   violations of vol(S_eps) < 1/eps : 0 / 545 clean  (0 / 687 incl. clipped)
         max vol(S_eps)*eps               : 0.6000   (star, a=2^-2, eps=1e-5)
         max |S_eps|*eps                  : 0.1900
         max vol(dS_eps)*eps              : 159.20   <-- NOT bounded by 1/eps
         sum_v pi_v verified              : 1 +- 2.5e-12 in every cell
```

**Closed-form saturation constants (Proved-draft), and how tight the bound is.**
Writing `sigma(G) = sup_{alpha,eps} eps*vol(S_eps)`:

| family | `sigma` predicted | attained at | `sigma` measured |
|---|---|---|---|
| path / cycle / caterpillar (1-D) | `sup_t ln(t)/t = 1/e = 0.3679` | `sqrt(alpha) = e*eps` | **0.367–0.380** |
| 3-D lattice | `sup_t t^2 e^{-t}/3 = 4e^{-2}/3 = 0.1804` | `kappa_3 R = 2` | **0.1803** (a=1e-3, eps=1e-6) |
| 2-D lattice | `sup_t t^2 K_0(t)/2 = 0.2406` (continuum) | `kappa_2 R ≈ 1.55` | **0.347** (discrete near-field excess) |
| star `K_{1,m}` | `1 - alpha` | `m = (1-a)/(2 eps)` | **0.60** at `a = 2^-2` (coarse `m` grid) |
| `d`-regular expander / `K_n` at critical size | **`-> 1`** | `n ≈ 1/(d*eps)` | 0.138 (grid too coarse); ridge run reaches 0.899 on the star analogue |

So Lemma A is *tight*: the extremal instances are exactly those on which `u` is
nearly **constant** at level `eps` over volume `1/eps` — regular expanders (and
stars) at the critical size.  On those the whole graph *is* the output and
`Omega(1/eps)` work is forced; on everything else the output is strictly below
`1/eps` and an *output-linear* algorithm would beat `1/eps`.

**Parameter accounting per family** (fit `vol(S_eps) ~ C * alpha^{-p} * eps^{-q}`
over clean cells; `C`, `R^2` from `fit_out.py`):

| family | cells | `p` (alpha) | `q` (eps) | `R^2` | `max vol*eps` | `max vol(dS)/vol(S)` |
|---|---|---|---|---|---|---|
| path | 59 | +0.434 | +0.152 | 0.975 | 0.370 | 0.29 |
| cycle | 58 | +0.427 | +0.167 | 0.971 | 0.380 | 0.40 |
| caterpillar | 59 | +0.420 | +0.172 | 0.945 | 0.367 | 0.40 |
| decoy_hub | 56 | +0.431 | +0.166 | 0.930 | 0.370 | 0.29 |
| spider | 41 | +0.381 | +0.227 | 0.926 | 0.365 | 0.67 |
| comb | 54 | +0.395 | +0.289 | 0.860 | 0.325 | 0.64 |
| btree | 26 | −0.236 | +0.558 | 0.754 | 0.200 | 1.50 |
| rrt | 34 | +0.292 | +0.526 | 0.844 | 0.349 | **2.96** |
| pa_tree | 36 | +0.256 | +0.431 | 0.928 | 0.353 | **4.54** |
| grid2d | 41 | +0.558 | +0.412 | 0.887 | 0.347 | 1.60 |
| grid3d | 32 | +0.140 | +0.671 | 0.650 | 0.198 | 2.57 |
| exp3reg | 25 | −0.138 | +0.594 | 0.707 | 0.138 | 1.50 |
| star / complete | — | — | — | — | (all cells clipped: `S_eps` is the whole graph or empty) | up to **399** |

The 1-D families sit at `p ≈ 0.43 ≈ 1/2` — this is the analytic
`vol(S_eps) = ln(sqrt(a)/eps)/sqrt(alpha)`, i.e. **the output itself carries a
`1/sqrt(alpha)`** on path-likes.  Grids sit near I2-F's exact-kernel law
`Theta(log^2(1/eps)/alpha)` (the fitted `p = 0.558` is depressed because many
cells sit near the trivialisation boundary where the `log^2` factor is `O(1)`).
`btree`/`exp3reg` have **negative** `p`: the output *shrinks* as `alpha` falls,
because the ball volume grows faster than `1/sqrt(alpha)` and mass thins out.
**In every case the product with `eps` is capped by Lemma A.**

---

## 2. Two structural lemmas that make `O(1/eps)` certification possible

**Lemma C (uphill / connectivity).**  For `v ∉ supp(s)`,
`u_v = (c_a / d_v) * sum_{w~v} u_w <= c_a * max_{w~v} u_w` with
`c_a = (1-alpha)/(1+alpha) < 1`.  So every `v ∈ S_eps` has a neighbour `w` with
`u_w > u_v`; iterating gives a strictly increasing `u`-path inside `S_eps` to a
seed vertex.  **`S_eps ∪ supp(s)` is a union of connected components each
containing a seed.**

**Corollary C1 (outer-boundary sufficiency).**  If `S ∋ supp(s)` and
`u_w <= eps` for every `w ∈ dS` (the outer ring), then `u_w <= eps` for *every*
`w ∉ S`.  A local certificate never has to look past one ring.

**Lemma D (certification costs `O(vol(S))`, with a degree oracle).**  For
`x_hat` supported on `S`, the residual row at a ring vertex `h` is
`(D^{-1/2}(Q x_hat - b))_h = -((1-a)/2) * (sum_{w ∈ S, w~h} u_w) / d_h`.
The edge set `S -> h` and the values `u_w` are already known from having
scanned `S`; **`d_h` is the only new datum**.  Hence the full certificate over
`S ∪ dS` costs `vol(S)` (rows in `S`) `+ |dS|` degree queries `+ O(|dS|)`
arithmetic, and `|dS| <= vol(S)`.  **Never `vol(dS)`.**

**Lemma E (the model precondition is real).**  In a *scan-only* model (no `O(1)`
degree query) no bound of the form `f(1/eps)` exists.  Adversary: `hidden_hub` —
a 6-path from the seed ending at a hub `h` of degree `M`.  `u_h = pi_h/M`, so
`h ∉ S_eps` for `M` large, `vol(S_eps) = 11` and `1/eps = 1000` are *fixed*, but
distinguishing `deg(h) = M` from `deg(h) = 3` (which would put `h` and its
neighbours in `S_eps`) requires `Omega(M)` scan work.  Measured (`adv.py`):

```
hidden_hub M=1e3 : vol(S)=11  volS*eps=0.011  vol(dS)*eps=1     | push 1.25  direct 6.3   amg 6.5
hidden_hub M=1e4 : vol(S)=11  volS*eps=0.011  vol(dS)*eps=10    | push 1.25  direct 60.3  amg 60.6
hidden_hub M=1e5 : vol(S)=11  volS*eps=0.011  vol(dS)*eps=100   | push 1.25  direct 600.3 amg 600.5
                                                                  (all figures are W*eps)
```

`W*eps` for the ball-based mechanisms is **exactly proportional to `M`** while
the output is constant.  Push (value-guided) is flat at `1.25`.
The `DQMeter` does **not** rescue elimination/AMG here (6.332 vs 6.338): their
volume-driven ladder *admits* the hub into the region rather than merely
ring-testing it.  That is a mechanism defect, not an information barrier —
Lemma D says the certifying region `S = S_eps` needs `vol = 11` plus **one**
degree query.

---

## 3. STATE THE CORRECT TARGET

The classic FY22 target and the corrected one, in the project's conventions:

```
FY22 (classic):     W  =  O~( 1 / (sqrt(alpha) * eps) )
I4-D (corrected):   W  =  O~( nnz(s) + vol(S_eps) )   ⊆   O~( nnz(s) + 1/eps )
                    S_eps = { v : pi_v / d_v > eps },   vol(S_eps) < 1/eps  (Lemma A)
                    model: adjacency-list scan (cost d_u) + O(1) degree query
```

Two remarks that decide the "which measure" question the brief asked for.

* **Use `vol(S_eps)`, not `|S_eps|`, as the primary output measure** — it is the
  larger one, it is what an algorithm must actually read (Lemma D charges
  `vol(S)`), and it is *still* under `1/eps`.  `|S_eps|` is the right measure
  only for the emission term `C_emit`.
* **The output-linear form is the real target; `1/eps` is its universal
  corollary.**  A solver that always spends `Theta(1/eps)` is not local: on 2-D
  grids the output is `Theta(log^2(1/eps)/alpha)`, which is `10^-4 * (1/eps)`
  at `(alpha, eps) = (2^-12, 10^-10)`.  Quoting only `O~(1/eps)` would license
  that waste.  Quoting `O~(vol(S_eps))` does not.

**Why the classic target is not merely loose but structurally so.**  Since
`vol(S_eps) < 1/eps <= 1/(sqrt(alpha)*eps)`, the FY22 bar sits a factor
`1/sqrt(alpha)` *above the maximum possible output* on **every** instance.
I2-F showed this makes the target vacuous on grids; Lemma A upgrades that from a
grid fact to a **theorem about every graph**.

---

## 4. Measured total work at each family's output-saturating cell (E2)

For each family we took the `(alpha, eps)` cell maximising `vol(S_eps)*eps`
subject to `1500 <= vol(S_eps) <= 90000` and un-clipped support — i.e. the cell
where the output is as close to `Theta(1/eps)` as that family gets, which is
where `O~(1/eps)` is hardest.  `W*eps = 1` means "total charged work is exactly
`1/eps`".  `push` = literal lazy ACL (C kernel); `cheb` = W5 truncated
Chebyshev; `direct` = growing-ball exact sparse LU (the ND-EES / elimination
line); `amg` = I3-A local smoothed-aggregation multigrid; the `DQ` suffix is the
same run with Lemma D's degree-query ring.

| cell (`alpha`, `eps`) | `vol*eps` | push | cheb | direct/DQ | amg/DQ | **best `W*eps`** | best / (FY22 `1/sqrt(a)`) |
|---|---|---|---|---|---|---|---|
| path `2^-20, 1e-4` | 0.233 | — | 2.07e4 | **35** | 231 | **35** (direct) | 0.034 |
| star `2^-2, 1e-5` | 0.600 | **0.6** | 1.2 | 13.8 | 24.6 | **0.60** (push) | 0.30 |
| spider `2^-12, 1e-4` | 0.365 | 658 | 1840 | **84.9** | 1250 | **84.9** (directDQ) | 1.33 |
| caterpillar `2^-20, 1e-4` | 0.280 | — | 8.4e4! | **46.6** | 485 | **46.6** (directDQ) | 0.046 |
| comb `2^-16, 1e-4` | 0.325 | — | 2.0e4 | **78.5** | 659 | **78.5** (directDQ) | 0.31 |
| btree `2^-6, 1e-5` | 0.061 | **4.61** | 34.3 | 9.01 | 102 | **4.61** (push) | 0.58 |
| rrt `2^-14, 1e-5` | 0.349 | — | 2380 | **37.7** | 1.25e4 | **37.7** (directDQ) | 0.30 |
| pa_tree `2^-10, 1e-4` | 0.287 | **178** | 1690 | 336 | 6.7e5! | **178** (push) | 5.6 |
| grid2d `2^-12, 1e-5` | 0.232 | — | 2280 | 8270 | **587** | **587** (amgDQ) | 9.2 |
| grid3d `2^-8, 1e-5` | 0.178 | **38.9** | 172 | 3.5e5 | 499 | **38.9** (push) | 2.4 |
| exp3reg `2^-6, 1e-5` | 0.088 | **5.67** | 58.3 | 2.9e6 | 634 | **5.67** (push) | 0.71 |

**Reading of the table.**

* **Total charged work is `O(1/eps)` with a modest constant on every family**:
  best `W*eps ∈ [0.60, 587]`, and the excess over the output is
  `W/vol(S_eps) ∈ [1, 2.5e3]`.
* **The excess is NOT coming from output size** — `vol*eps` is `0.06 … 0.60`
  everywhere, so the output never accounts for more than `0.6/eps`.  It is
  coming from the mechanism and the stopping rule (§5, §6).
* **Against the classic target the portfolio already wins on 8 of 11 families**
  (ratios `0.034 … 0.71`), ties on spider (1.33) and loses only on `pa_tree`
  (5.6), `grid3d` (2.4) and `grid2d` (9.2) — and on those three the loss is a
  constant, not a growing exponent (§5).
* **The DQ ring saves 0–15 %** on these families (`btree` 10.3 → 9.01 is the
  largest) because their ring volumes are ordinary.  Its value is on the
  adversaries (§6), where it is the difference between bounded and unbounded.
* **The champion changes with the family**: elimination on trees/path-likes and
  heavy-tailed trees, AMG on 2-D grids, push on high-degree/expanding/3-D cells.
  No mechanism is best twice in a row.  *This is the whole remaining problem.*

---

## 5. The DECISIVE measurement: the output-saturating ridge (E5)

A single cell cannot separate `C/eps` from `C/eps^{1.3}`.  So for three families
we followed the **ridge** — the `(alpha, eps)` curve on which `vol(S_eps)*eps`
is pinned at its maximum, so the output is `Theta(1/eps)` at every point — over
1.5–2.5 decades of `1/eps`, and fitted `log(W*eps)` against `log(1/eps)`.
A slope of `0` is *exactly* `O(1/eps)`; a positive slope `beta` means
`Theta(eps^{-(1+beta)})`.  `amgO` = local AMG stopped by the **oracle**
(semantic error, not the certificate) — it isolates mechanism cost from
stopping-rule cost.

**Path ridge, `alpha = 7.4 eps^2`** (the regime where FY22 reads `1/(2.72 eps^2)`):

| `1/eps` | `vol*eps` | direct | amg | **amgO** |
|---|---|---|---|---|
| 333 | 0.369 | 91.3 | 393 | **30.6** |
| 1 000 | 0.367 | 103 | 509 | **48.4** |
| 3 333 | 0.368 | 105 | 655 | **63.1** |
| 10 000 | 0.368 | 118 | 1180 | **78.8** |
| 33 333 | 0.363 | 119 | 810 | **82.2** |

log-log slope: **direct 0.058**, **amgO 0.215 over the first 1.5 decades but
0.035 over the last half-decade** — flattening, consistent with `amgO*eps ≈
0.95 * ln^2(1/eps)` (predicted 32.1 / 45.3 / 62.5 / 80.6 vs measured 30.6 /
48.4 / 63.1 / 78.8, mean error 5 %).  Both are `O~(1/eps)`.
**FY22 at the last point is `1/(sqrt(a)*eps) = 12 255/eps`; measured is
`119/eps` — the classic target overestimates the true cost by `103x` at
`1/eps = 33 333`, and since FY22`*eps = 1/sqrt(alpha) = 1/(2.72*eps)` grows
linearly in `1/eps` along this ridge while the measurement is flat, the gap
grows without bound.**

**Star ridge, `m = 0.9/(2 eps)`, `alpha = 2^-10`** (`vol*eps = 0.899`, i.e. the
output is `0.9/eps` — as close to Lemma A's bar as any family gets):

| `1/eps` | `vol*eps` | push | **direct** | amg |
|---|---|---|---|---|
| 1 000 | 0.898 | 273 | **10.34** | 18.4 |
| 10 000 | 0.899 | 272 | **10.34** | 18.4 |
| 100 000 | 0.899 | 272 | **10.34** | 18.4 |
| 333 333 | 0.899 | — | **10.34** | 18.4 |

**Slope 0.000 over 2.5 decades.**  `W = 10.34/eps` exactly, alpha-free,
at an output of `0.9/eps`: **11.5 charged units per unit of output.**

**2-D grid ridge, `alpha = 15.3 eps`** (the family that costs the most in §4):

| `1/eps` | `vol*eps` | amg (self-cert) | **amgO** | direct |
|---|---|---|---|---|
| 10 000 | 0.237 | 433 | **42.9** | 1.6e3 |
| 33 333 | 0.241 | 481 | **53.0** | 3.8e3 |
| 100 000 | 0.240 | 554 | **43.9** | 8.4e3 |
| 333 333 | 0.241 | 638 | **49.2** | 1.9e4 |
| 1 000 000 | 0.260 | 253 | **58.7** | 6.4e3 (wall-capped) |

**amgO slope 0.068 over two decades, non-monotone** — flat within noise.
`W = ~50/eps` on the hardest family in the zoo, at an output of `0.24/eps`:
**about 210 charged units per unit of output, alpha-free.**
Self-certified AMG's slope is `+0.13` — the certificate, not the mechanism.
Elimination's slope is `+0.54`, i.e. `Theta(eps^{-1.54})`: nested dissection's
`vol^{1.5}` — **the one clean super-`1/eps` law measured anywhere in this
report**, and it is a property of *that* mechanism only.

> **Summary of §5.**  On all three ridges the best mechanism's total charged
> work is `O~(1/eps)`, with constants `10 – 60` (oracle-stopped) and
> `100 – 640` (self-certified).  There is no measured family on which the best
> mechanism's `W*eps` grows like a power of `1/eps`.

---

## 6. The adversarial half — what actually breaks

### 6a. High-degree supports where `vol(S_eps) >> 1/eps` — **do not exist** (Lemma A)
Refuted analytically and in 545/545 cells.  What *does* exist is high-degree
supports where `|S_eps| << vol(S_eps)`: `K_{1,m}` at critical width has
`|S_eps|*eps ≈ 0.5` but `vol(S_eps)*eps ≈ 0.9`.  Both are `< 1`.  The measure
choice changes the constant, not the exponent.

### 6b. Grids at small alpha — output is `Theta(log^2(1/eps)/alpha)` — **not an obstruction**
Along the grid ridge `eps*vol(S_eps)` is pinned at `0.24`, i.e. the output is
`Theta(1/eps)` there, and `amgO` still delivers `~50/eps`, flat.  Away from the
ridge (`eps << alpha`) the output *collapses* far below `1/eps`, which makes
`O~(1/eps)` easier, not harder.  Elimination is the casualty (`eps^{-1.54}`),
AMG is not.

### 6c. Expanders (`vol(S_eps) = Theta(n)`) — **the extremal case, and it is easy**
An expander at the critical size `n ≈ 1/(d*eps)` is *exactly* the instance that
makes Lemma A tight (`u` constant at level `eps`, `eps*vol -> 1`).  There the
whole graph must be read, so `Omega(1/eps)` is forced — and matched: push gives
`W*eps = 5.67` at `a = 2^-6`, `cheb` 58.3, `amgDQ` 634; elimination is
catastrophic (`2.9e6`, fill-in).  So expanders **prove the `Omega(1/eps)` side of
the corrected target** rather than refuting the `O` side.

### 6d. Heavy-tailed-degree trees — **AMG dies, elimination does not**
`rrt` at its saturating cell: `directDQ 37.7`, `amgDQ 1.25e4` (332x worse).
`pa_tree`: `push 178`, `directDQ 336`, `amg 6.7e5` and **uncertified**.
This reproduces I3-A's finding (Galerkin `RAP` densification on heavy tails) and
localises it: it is an AMG-setup pathology, and the alternative mechanism in the
arsenal covers the family at `W*eps < 340`.

### 6e. **BALL TRAP — small support, unbounded work.  This one bites.**
`ball_trap(L=400, M, at=60)`: a path from the seed with a clique `K_M` hung by a
single edge at depth 60.  Clique vertices have `u = Theta(mass/M^2)`, so they are
never in `S_eps`; here the parameters (`alpha = 7.4e-6`, `eps = 1e-3`) even make
`S_eps` **empty**, so the *correct output is the zero vector* and the ideal work
is `O(1)`.

```
ball_trap M=100 : vol(S_eps)=0 | push 1245   directDQ 8.0e2   amgDQ 8.9e2
ball_trap M=300 : vol(S_eps)=0 | push 1241   directDQ 1.9e4   amgDQ 8.2e3
ball_trap M=600 : vol(S_eps)=0 | push 1243   directDQ 1.5e5   amgDQ 2.4e4 (uncertified)
                                                        (all figures are W*eps)
```

**Push is flat in `M` (1245 / 1241 / 1243); both ball-based mechanisms grow like
`M^2`.**  Lemma D's degree-query ring does not save them, because the failure is
not in the ring test — it is that a **BFS-ball region rule must swallow the
clique's interior** on its way outward.  This is the cleanest statement of the
remaining gap:

> the two alpha-free mechanisms in the arsenal (elimination, local AMG) select
> their region **geometrically** and are therefore **not output-bounded**; the
> one output-bounded mechanism (push) selects **by value** and is therefore
> **not alpha-free**.  `O~(1/eps)` in general needs a mechanism that is both.

### 6f. The stopping rule is the other half of the gap (new, Measured)
On the **exact minimal region** `S = S_eps` we computed the push-scale residual
`theta = max_v |r_v|/d_v` (`r = gamma s - M pi_hat`, `M = I - c_a A D^{-1}`),
the true error `err`, and the amplification `A = err/theta`.  The repository's
sufficient certificate is exactly `theta < 2*alpha*eps/(1+alpha)`, i.e. it
assumes the worst case `A = (1+alpha)/(2 alpha)`.

| family | `alpha` | `err/eps` | `theta/eps` | **`A = err/theta`** | worst-case `A` | stated cert on `S_eps` |
|---|---|---|---|---|---|---|
| path | 2^-4 | 0.705 | 0.332 | **2.13** | 8.5 | FAIL |
| path | 2^-10 | 0.993 | 0.062 | **16.0** | 512 | FAIL |
| spider | 2^-4 / 2^-10 | 0.945 / 0.971 | 0.445 / 0.061 | **2.13 / 16.1** | 8.5 / 512 | FAIL |
| caterpillar | 2^-4 / 2^-10 | 0.643 / 0.985 | 0.289 / 0.058 | **2.22 / 17.0** | 8.5 / 512 | FAIL |
| grid2d | 2^-4 / 2^-10 | 0.877 / 0.987 | 0.464 / 0.075 | **1.89 / 13.2** | 8.5 / 512 | FAIL |
| rrt | 2^-4 / 2^-10 | 0.998 / 1.000 | 0.617 / 0.185 | **1.62 / 5.39** | 8.5 / 512 | FAIL |
| exp3reg | 2^-4 | 0.999 | 0.549 | **1.82** | 8.5 | FAIL |
| hidden_hub | 2^-4 / 2^-10 | 0.050 / 0.467 | 0.011 / 0.0018 | **4.52 / 256** | 8.5 / 512 | PASS |

Two things follow.

1. **The stated certificate fails on the optimal output itself** in 11 of 13
   cells.  A solver that uses it *must* enlarge its region strictly beyond
   `S_eps`.  Every "`W/vol(S_eps) = 150 … 2500`" number in §4 is partly this.
   The `err/eps` column of §4 measures the same thing from the other side:
   certified elimination/AMG runs land at `err/eps = 2.4e-13 … 0.15`, i.e. they
   **over-solve by `7x` to `4e12`** (median ≈ `3e3`).
2. **On ordinary families the true amplification scales like `alpha^{-1/2}`,
   not `alpha^{-1}` — but a uniform relaxation is REFUTED by the same table.**
   On path / spider / caterpillar / grid2d / rrt, `A` grows by `7.0-7.7x`
   (median `7.5x`, rrt `3.3x`) when `alpha` falls by `64x`: fitted exponent
   **0.48**, i.e. `A = Theta(alpha^{-1/2})`, and `A/A_worst = 0.003 … 0.25`
   (over-charged by `4x` to `330x`).  It is tempting to conclude that the sharp
   rule is `||D^{-1/2}(Q x_hat - b)||_inf < c*sqrt(alpha)*eps`, a factor
   `1/sqrt(alpha)` weaker — *numerically the same `1/sqrt(alpha)` that separates
   the classic target from `1/eps`*.
   **That conclusion is wrong, and `hidden_hub` is the counterexample.**  There
   `A` grows `56.6x` for the same `64x` drop in `alpha` (exponent **0.97**) and
   reaches `A/A_worst = 0.50` — the worst case is attained within a factor 2 —
   and correspondingly it is the *only* family where the repository's stated
   certificate **passes on the minimal region** (theta/eps `= 1.82e-3` against a
   threshold `2*alpha/(1+alpha) = 1.95e-3`: tight to 7 %).
   **So the certificate is tight exactly on high-degree-boundary instances and
   loose by `4-330x` on everything else.**  A universal `sqrt(alpha)` rule is
   therefore **unsound**; what is needed is an *instance-adaptive, locally
   computable* amplification bound `A_hat(S) >= A(S)`.  That reframes SP1
   (§8) from "relax the constant" to "compute the constant", which is a
   strictly better-posed question.

---

## 7. VERDICT

Of the brief's three options:

* **(i) "`O~(1/eps)` achievable in general — the target is set too low."**
  *The negative half of (i) is established; the positive half is supported but
  not proved.*
  **Established (Proved-draft):** the classic target is **not tight on any
  instance** — `vol(S_eps) < 1/eps <= 1/(sqrt(alpha) eps)` always, so FY22
  leaves a `1/sqrt(alpha)` factor of headroom above the maximum possible output
  everywhere, and `O~(1/eps)` is type-correct with degree volume as the output
  measure.  **Supported (Measured):** on 11/11 families at their
  output-saturating cells and on 3/3 ridges over 1.5–2.5 decades, the best
  mechanism achieves `W*eps ∈ [0.6, 587]` with log-log slope `0.00 … 0.22` and
  falling.  **Not established:** no *single* algorithm does this; the portfolio
  is selected per instance using knowledge the algorithm does not have.
* **(ii) "achievable on a characterized class but provably not in general."**
  *No obstruction family was found, so the "provably not" half is unsupported.*
  Every candidate obstruction dissolved: high-degree supports (Lemma A),
  small-alpha grids (ridge is flat), expanders (they *force* `Omega(1/eps)` and
  are matched), heavy-tailed trees (elimination covers them at `W*eps < 340`).
  The one family that genuinely breaks things — the **ball trap** — breaks
  *mechanisms*, not the target: its correct output is empty, so an
  output-bounded algorithm would spend `O(1)`, and push (value-guided) is
  already flat in `M` there.
* **(iii) "the evidence is insufficient."**  *This is the honest label for the
  positive half of (i)*, and I name the two measurements that would decide it in
  §8.

**Formally: the supported verdict is (i)-negative + (iii)-positive.**  The
classic target is refuted as a *tight* target (Proved-draft).  The corrected
target `O~(nnz(s) + vol(S_eps)) ⊆ O~(nnz(s) + 1/eps)` is *consistent with every
measurement in this campaign* and is achieved cell-by-cell by the arsenal's best
member, but it is **Open** whether one algorithm achieves it, and the campaign
has **no lower-bound machinery capable of refuting it** — absence of a single
fast algorithm in the arsenal is not a proof, and I do not claim one.

---

## 8. The corrected open problem (candidate replacement for the FY22 target)

> **Open Problem (I4-D: output-linear local PPR).**
> Let `G = (V,E)` be simple, undirected, unweighted, with no isolated vertices,
> accessed by adjacency-list scans (scanning `i` costs `d_i`; repeats charged)
> together with an `O(1)` degree query `deg(i)`.  Let `s >= 0`, `1^T s = 1`, be
> given as `nnz(s)` sparse entries, `alpha ∈ (0,1]`, `eps_ppr ∈ (0,1]`.  Let
> `pi = D^{1/2} Q^{-1} b` be the source-aligned PPR vector and
> `S_eps = { v : pi_v/d_v > eps_ppr }`.
>
> Is there an algorithm which outputs a finite-support `x_hat` with
> `max_i |pi_hat_i - pi_i| / d_i <= eps_ppr`, under the full charged ledger
> (seed reading, discovery and degree queries, repeated row reads, coordinate /
> factor / response / sketch updates, boundary tests, certificate verification,
> materialisation and output writes), with total charged work
>
> ```
> W  =  O~( nnz(s) + vol(S_eps) )        [output-linear form]
> ```
>
> uniformly in `alpha` and in `G`?  By Lemma A this implies the weaker
> **graph-uniform form** `W = O~(nnz(s) + 1/eps_ppr)`, which is already strictly
> stronger than the classic `O~(1/(sqrt(alpha)*eps_ppr))` by a factor
> `1/sqrt(alpha)` on every instance.

**Attached facts.**
* `vol(S_eps) < 1/eps_ppr` always (Lemma A); `|S_eps| <= vol(S_eps)`; the bound
  is tight, approached by `d`-regular expanders and stars at the critical size
  `vol ≈ 1/eps_ppr`.
* `S_eps ∪ supp(s)` is connected through seeds (Lemma C); certification needs
  only the outer ring (C1) and costs `O(vol(S))` charged units with `|dS|`
  degree queries (Lemma D).
* The `O(1)` degree query is **necessary**: without it, `hidden_hub` forces
  `Omega(d_max)` for a fixed `O(1)`-volume output (Lemma E, measured 6.3 → 600
  in `W*eps` as `M` goes `10^3 → 10^5`).
* `Omega(vol(S_eps))` is forced on expanders at the critical size, and
  `Omega(1/eps)` probes are forced on spiders (I2-E / W2, matched to a factor
  80), so the target is **tight** where it binds.
* **Sub-problem SP1 (compute the certificate constant, do not relax it).**
  The repository's rule `||D^{-1/2}(Q x_hat - b)||_inf < alpha*eps_ppr` is the
  worst-case instantiation `A = (1+alpha)/(2 alpha)` of the exact identity
  `err = ||M^{-1} r||_{D^{-1},inf}`, `M = I - c_a A D^{-1}`.  Measured on the
  exact minimal region, the true `A` is `Theta(alpha^{-1/2})` on path / spider /
  caterpillar / grid2d / rrt (over-charging by `4-330x`, and the stated rule
  **fails on the optimal output in 11/13 cells**) but `Theta(alpha^{-1})` —
  within `2x` of worst case — on `hidden_hub`.  **A uniform relaxation is
  therefore unsound.**  SP1: give a locally computable `A_hat(S) >= A(S)`,
  charged inside the ledger, that is `O(alpha^{-1/2})` whenever the true
  amplification is.  Solving SP1 removes the `1/sqrt(alpha)` gap between
  self-certified and oracle-stopped work measured in §5 (`~10x` on grids,
  `~8x` on paths) on exactly the families where it is safe to.
* **Sub-problem SP2 (value-guided + alpha-free).**  Exhibit one mechanism that
  is simultaneously *output-bounded* (does not read volume outside
  `S_eps ∪ dS_eps` — push is, ball-based elimination/AMG are not: ball trap) and
  *alpha-free* (cycle count `O(log(1/eps))` — AMG/elimination are, push is not:
  `1/(alpha*eps)`).  The natural candidate is **value-guided region growth +
  incremental factorisation** (I2-B's HSEG-LDL admission on trees, I3-A's local
  AMG hierarchy on high-treewidth regions), which no run in this campaign has
  yet combined.

**What would decide it (the measurements I did not have time for).**
1. **SP1 directly:** sweep `A = err/theta` on the exact `S_eps` over
   `alpha ∈ {2^-2 … 2^-20}` x all 14 families, and correlate `A/A_worst` with
   a *candidate computable statistic* of the ring (the obvious one, given
   `hidden_hub`: `max_{h ∈ dS} d_h / vol(S)`).  A statistic that separates the
   `alpha^{-1/2}` families from `hidden_hub` is the certificate.
   (`i4d/run_amp.py` is written and ready; it did not fit the compute cap.)
2. **SP2 directly:** implement value-guided admission (rank ring vertices by
   scaled residual, admit only violators, never a whole shell) on top of
   `direct_local`, and re-run the **ball trap** and **hidden hub**.  Predicted:
   `W*eps` flat in `M` on both, which is the missing existence proof for an
   output-bounded alpha-free mechanism.
3. **Ridge extension:** push the star and 2-D grid ridges two further decades
   (`1/eps` to `10^8`) to confirm the slopes stay at `0.00` / `0.07`.

---

## 9. Ledger, verification and caveats

* **Verification.**  Every run in §4–§6 was checked against `spsolve`/CG:
  `err = max_i |pi_hat_i - pi_i|/d_i` computed exactly and compared with `eps`.
  Runs that failed (`err > eps`) or did not certify are marked `!` in the tables
  and are **excluded from every "best mechanism" figure**.  Exactly three such
  runs occur (caterpillar/cheb, pa_tree/amg, ball_trap M=600/amgDQ), all of them
  wall-cap timeouts on mechanisms that were losing anyway.
  E1's 545 cells are exact solves; `sum_v pi_v = 1 ± 2.5e-12` in every one.
* **Ledger.**  As I3-A: level-0 adjacency reads charge `d_u` (`C_adj` first,
  `R_adj` repeats), every coarse-level / factor / transfer / RAP / coarse-solve
  operation charges its true nonzero count (`C_resp`), materialised cells
  `C_mat`, coordinate writes `C_rec`; `W = sum`.  The only new ledger item is
  the **degree query**, charged 1 unit each (`C_resp`) in `DQMeter`, used only
  for the outer ring, and justified by Lemma D.  A ring vertex later admitted to
  the region is charged its full degree at that point.
* **Caveats, stated plainly.**
  1. The `O~(1/eps)` claim is **portfolio-level**: the champion is chosen per
     family after the fact.  Turning this into an algorithm requires SP2.
  2. Ridge slopes rest on 4–5 points over 1.5–2.5 decades; `amgO`'s path slope
     (0.215) is not distinguishable from `ln^2` at this range.
  3. `amgO` is **oracle-stopped**; it lower-bounds mechanism cost, it is not an
     algorithm.  The gap to the self-certified figure (`~10x` on grids) is
     exactly SP1.
  4. The `alpha^{-1/2}` amplification law rests on two `alpha` values, and is
     **already known not to be universal** (`hidden_hub` gives `alpha^{-0.97}`);
     see SP1.
  5. The 2-D measured saturation constant (0.347) exceeds the continuum
     prediction (0.241) by 44 %; the discrete near-field Green's function is
     larger than `K_0` near the origin.  This does not affect Lemma A, which is
     exact and graph-independent.
  6. `amglib.py` was modified (the `ring_scan` hook).  The default path is
     byte-for-byte the old behaviour, so no I3-A number changes; the `DQMeter`
     subclass lives in `i4d/`.

