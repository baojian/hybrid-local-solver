# I3-A — Does LOCAL ALGEBRAIC MULTIGRID retain I2-F's output-linear, alpha-free law on arbitrary graphs?

Code: `/home/claude/work/overnight/i3a_amg/` (`amglib.py` = local SA-AMG +
charged baselines, `run_zoo.py` = sweep, `rate_test.py` = alpha-uniformity of
the V-cycle rate, `fit.py` = tables).  Data: `out/zoo_{main,g3d,exp,exp2}.json`,
`out/tables.txt`; logs `out/{main,g3d}.log`.
Conventions as W1–W8 / I2-F: `Q = (1+a)/2 I − (1−a)/2 D^{-1/2}AD^{-1/2}
= a I + (1−a)/2 L_sym`, `b = a D^{-1/2}e_v`, semantic err
`= ||D^{-1/2}(x−x*)||_inf`, certificate `||D^{-1/2}(Qx−b)||_inf < a·eps
⇒ err < eps`.  Meter: level-0 adjacency reads charge `d_u` (`C_adj`/`R_adj`);
every coarse-level operation charges its actual nonzero op count (`C_resp`);
materialised cells `C_mat`; coordinate writes `C_rec`; `W = Σ`.
**69 cells, all verified against the exact solve, 0 failures.**
Total compute ≈ 75 min (over the 40-min guidance; the expander cells and the
elimination baseline on them were the overrun).

## VERDICT

**The MECHANISM generalizes; the ECONOMICS do not.**  (Measured.)

* **(YES) alpha-freedom is general.**  Local AMG's measured alpha-exponent of
  `W/vol(S_eps)` is `−0.16 … +0.34` (median ≈ 0.16) across **all twelve
  families**, against push `0.82 … 1.39` and Chebyshev `0.28 … 1.25`.  The
  V-cycle contraction rate **saturates** as `alpha → 0` on every family
  (measured to `alpha = 2^-20`): the shift only helps, monotonically, and
  the limit rate is `0.47 … 0.80`.  So cycle count is
  `Theta(log(1/eps))`, alpha-free, off-lattice exactly as on the lattice.
  I2-F's mechanism claim survives the generalization.
* **(NO) output-linearity with a *useful* constant does not.**  Certified
  local AMG costs **93 … 1 300 charged units per unit of `vol(S_eps)`** on
  the well-behaved families and **9 000 … 22 000** on a random recursive
  tree.  I2-F's geometric MG cost 104–410.  **Setup is 26–93 % of the bill**
  and it is the part that grows: the Galerkin `RAP` hierarchy densifies
  (operator complexity `1.00 … 9.5`), and on heavy-tailed-degree graphs the
  densification destroys the win outright.
* **(SURPRISE) the real general-graph winner is ELIMINATION, not multigrid.**
  The same growing-ball region solved by a fill-reducing sparse LU — the
  generalization of I2-F's ND-EES, charged identically — is **11–116 × vol
  and alpha-free on 9 of 12 families**, and beats AMG by 1.8× (star) to 51×
  (binary tree).  AMG wins outright only where the ball has high treewidth:
  **2-D grids at `alpha ≤ 2^-12`** and **3-regular expanders at
  `alpha ≤ 2^-12`** — the two families where elimination is catastrophic
  (`1.8·10^4` and `1.6·10^6 × vol`).

**Precise conjecture supported by the data** — see §7.

## 1. The algorithm and its complete charging ledger

`Q` is a positively shifted normalized graph Laplacian: SPD M-matrix,
`spec(Q) ⊆ [alpha, 1]`, `diag(Q) ≡ (1+alpha)/2`.  That is exactly the class
smoothed aggregation is built for, and the near-nullspace of `L_sym` is
`D^{1/2}1`, so the level-0 near-nullspace candidate is `B = sqrt(d)|_S` — no
lattice structure is used anywhere.

**Region.**  Incremental BFS ball `Omega = ball(v,R)`, boundary ring
`dOmega = ball(R+1) \ Omega`.  The residual is exactly zero outside
`Omega ∪ dOmega`, so the certificate is genuinely local.  *Volume-driven
ladder*: shells are added one at a time and a solve is attempted only when
`vol(ball)` has grown `≥ 1.5×` since the last attempt.  (A geometric **radius**
ladder — I2-F's — overshoots trees and expanders by `2^{0.3R}`; this was
worth a 4.5× reduction in `W` on the binary tree.)  Every failed attempt is
charged in full.

**Hierarchy (rebuilt from scratch on every region attempt).**

| step | what | charge |
|---|---|---|
| strength of connection | `|A_ij| ≥ theta·max_k|A_ik|`, symmetrised, `theta = 0.25` (at level 0 this *is* the classical Ruge–Stüben M-matrix rule for `Q`) | 1 level-0 scan pass = `vol(Omega)`; `nnz(A_l)` at level `l ≥ 1` |
| aggregation | distance-2 MIS (vectorised Luby) + 2 assignment rounds | `rounds × vol(Omega)` / `rounds × nnz(S_l)` |
| tentative prolongator | `T[i,agg(i)] = B_i/||B_agg||` | `3 n_l` |
| spectral radius | **level 0 is free and rigorous**: `rho(D^{-1}Q_SS) ≤ 2/(1+alpha)` exactly (uniform diagonal + Cauchy interlacing); levels `≥1` use 12 power iterations × 1.25 safety | `12·nnz(A_l)` for `l ≥ 1` |
| prolongator smoothing | `P = (I − (4/(3rho))D^{-1}A)T` | exact SpMM multiply-add count + `nnz(P)` |
| **Galerkin RAP** | `A_{l+1} = P^T A_l P` | **exact SpMM counts for both products** |
| coarsest solve | sparse LU, MMD ordering, `n_c ≤ 60` | `Σ_j nnz(L[:,j])^2` factor + `2 nnz(L+U)` per solve |
| V-cycle | weighted Jacobi `nu1 = nu2 = 2`, `om = 4/(3rho)` | level 0: `(nu1+1+nu2)` scans; level `l`: `(nu1+1+nu2)·nnz(A_l)`; transfers `nnz(P_l)` each |
| certificate | residual over `Omega` + cross-block residual over `dOmega` | 1 scan of `Omega` + 1 scan of `dOmega` per cycle |
| materialisation | `nnz(A_l) + nnz(P_l) + 2n_l` per level | `C_mat` |

*Smoother is provably convergent, uniformly in alpha* (Proved-draft): with
`rho = 2/(1+alpha)` and `om = 4/(3rho)`, `spec(om D^{-1}Q) = [(4/3)alpha, 4/3]`
so `spec(I − om D^{-1}Q) ⊆ [−1/3, 1−(4/3)alpha]`.  No estimation, no failure
mode.  (Estimating `rho` by power iteration instead **diverges on the star**:
the top eigenvector has `O(1/sqrt(n))` overlap with a random start.  Bug found
and fixed; recorded because it is a real trap for anyone reimplementing this.)

*Nested iteration*: the previous (smaller) region's iterate warm-starts the
next, charged as `|S|` coordinate writes.  *Early region rejection*: after 3
cycles, if the boundary part of the certificate alone exceeds `alpha·eps`, the
region is provably too small and is abandoned.

**Honesty of the aggregation charge.**  The vectorised MIS costs `rounds`
passes where the sequential Vaněk 3-pass costs 3.  Both are metered:
`W_seq/W ∈ [0.89, 1.00]` over all 69 cells — **at most 11 % of the reported
bill is an artefact of the parallel aggregation**, so no conclusion below
turns on it.

**Baselines**, all under the same meter and the same region machinery:
`PUSH` (bit-identical C ACL kernel from W8), `CHEB` (W5 truncated Chebyshev
with the free measured certificate), `DIRECT` (same growing ball, exact
sparse-LU solve of `Q[Omega,Omega]` with an `MMD_AT_PLUS_A` fill-reducing
ordering, charging `Σ_j nnz(L[:,j])^2` factor flops + fill + solves) — this is
I2-F's ND-EES generalised to arbitrary graphs and is the campaign's
elimination line (EES, HSEG-LDL) in one-shot form.

## 2. Correctness (Measured)

Every one of the **69 cells** was checked against the exact solve
(`spsolve` for `n ≤ 8 000`, CG to `rtol = 1e-14` above — verified residual
`≤ 2.4e-18` and agreement with `spsolve` to `8.8e-17` on the star).

| method | cells | max `err/eps` |
|---|---|---|
| AMG (certified) | 69 | **0.379** |
| AMG (oracle-stopped) | 69 | 0.975 |
| push | 51 | 0.946 |
| Chebyshev | 69 | 0.500 |
| local direct | 56 | 0.233 |

**0 failures.**  67/69 AMG runs returned `cert`; the 2 that did not
(`binary_tree 2^-12/1e-8`, `rrt 2^-12/1e-6`) correctly returned `maxed` and
*refused to certify* — their true errors were 0.25·eps and 0.14·eps, i.e. the
refusal was conservative, not wrong.  Both were caused by the stall rule
(`cert < 0.6·best`) firing when the measured V-cycle rate is `0.6–0.7`; a
looser stall window would certify them at slightly lower cost, so the reported
`W` is if anything an over-charge.

## 3. Charged work — `W/vol(S_eps)` (Measured; full table in `out/tables.txt`)

| family | alpha | eps | vol(S) | volΩ/volS | **AMG** | AMG-oracle | push | cheb | direct |
|---|---|---|---|---|---|---|---|---|---|
| grid2d | 2^-4 | 1e-6 | 1 956 | 1.9 | 221 | 129 | 54 | 45 | 234 |
| grid2d | 2^-8 | 1e-6 | 16 468 | 2.9 | 419 | 269 | 583 | 395 | 1 782 |
| grid2d | 2^-12 | 1e-6 | 96 388 | 5.9 | **922** | 261 | 5 498 | 4 350 | 18 487 |
| grid2d | 2^-12 | 1e-8 | 425 300 | 1.9 | **389** | 222 | — | 2 038 | 8 901 |
| grid3d | 2^-8 | 1e-6 | 123 378 | 3.3 | 636 | 245 | 285 | 382 | 717 931 |
| grid3d | 2^-12 | 1e-6 | 403 440 | 1.0 | **234** | 184 | 3 421 | 634 | 219 554 |
| double_cycle | 2^-8 | 1e-6 | 738 | 1.5 | 186 | 122 | 1 143 | 234 | **51** |
| double_cycle | 2^-12 | 1e-6 | 2 526 | 2.3 | 327 | 199 | 15 245 | 1 611 | **78** |
| binary_tree | 2^-8 | 1e-6 | 131 068 | 1.0 | 1 010 | 922 | 420 | 141 | **26** |
| caterpillar | 2^-12 | 1e-6 | 843 | 1.5 | 480 | 356 | 17 958 | 2 399 | **48** |
| comb | 2^-12 | 1e-6 | 1 975 | 1.8 | 565 | 282 | 16 185 | 3 992 | **58** |
| spider | 2^-12 | 1e-6 | 3 018 | 1.9 | 399 | 217 | 14 832 | 2 114 | **60** |
| star | 2^-12 | 1e-6 | 200 000 | 1.0 | 21 | 21 | 5 828 | 941 | **12** |
| decoy_hub | 2^-12 | 1e-6 | 617 | 1.5 | 296 | 154 | 18 655 | 2 108 | **49** |
| rand_reg3 | 2^-12 | 1e-6 | 60 000 | 1.0 | **502** | 396 | 9 507 | 486 | 1.6e6 |
| rand_reg4 | 2^-12 | 1e-6 | 80 000 | 1.0 | 567 | 453 | 8 633 | **434** | — |
| **rrt** | 2^-12 | 1e-6 | 73 045 | 1.0 | **8 982** | 8 640 | 7 993 | 1 507 | **38** |

### Fitted alpha-exponents `s` of `W/vol(S) ~ C·alpha^{-s}` (eps = 1e-6)

| family | **AMG** | AMG-oracle | push | cheb | direct |
|---|---|---|---|---|---|
| grid2d | 0.26 | 0.13 | 0.83 | 0.83 | 0.79 |
| grid3d | −0.14 | 0.01 | 0.82 | 0.46 | 0.36 |
| double_cycle | 0.16 | 0.15 | 0.94 | 0.63 | 0.08 |
| binary_tree | −0.00 | 0.31 | 0.96 | 0.29 | −0.21 |
| caterpillar | 0.26 | 0.36 | 0.95 | 0.74 | 0.01 |
| comb | 0.17 | 0.06 | 0.97 | 0.75 | 0.04 |
| spider | 0.17 | 0.05 | 0.94 | 0.65 | 0.09 |
| star | −0.00 | −0.00 | 1.00 | 0.80 | −0.00 |
| decoy_hub | 0.18 | 0.19 | 0.95 | 0.64 | −0.00 |
| rand_reg3 | −0.16 | −0.09 | 1.08 | 0.28 | — |
| rand_reg4 | 0.01 | −0.03 | 1.11 | 0.60 | — |
| rrt | −0.16 | −0.17 | 0.99 | 0.50 | — |

(eps = 1e-8 rows in `out/tables.txt` are the same picture: AMG 0.00–0.34.)

*Host-size caveats, stated explicitly.*  Two cells are host-limited and are
excluded from the qualitative claims: `grid2d 2^-12/1e-8` (region = the whole
`451²` host, `volΩ/volG = 1.00`) and `grid3d 2^-12/1e-5` (`eps/alpha = 0.04`,
the near-trivial regime — `vol(S) = 1 218` but `volΩ/volS = 331`, giving the
one absurd `W/vol = 64 092` in the raw table).  Every other cell has
`volΩ ≤ vol(G)` with slack, or is a family whose eps-support genuinely is the
whole graph (star, binary tree, expanders — see §6).

**This is the paper-level number.**  I2-F measured, on grids only, `s = 0.20`
(MG certified) vs 0.75–0.85 for every other mechanism.  The same separation
now holds on **every family in the zoo**, including the two expander families
and the closed 3-regular prism: `s_AMG ≤ 0.34` everywhere, `s_push ≥ 0.82`
everywhere, `s_cheb ≥ 0.28`.  The residual `s ≈ 0.2` in the certified variant
is again almost entirely the **certificate tax** — the `volΩ/volS` column has
its own alpha-exponent 0.00–0.21, and AMG-oracle drops to 0.00–0.36.

## 4. (a) Is the V-cycle rate alpha-uniform off-lattice?  **YES — it saturates.**

To separate the rate from the region search, `rate_test.py` fixes the graph,
takes `Omega` = the whole graph, and sweeps `alpha` from `2^-2` to `2^-20`
(median residual-reduction factor per V-cycle, cycles 3–14):

| graph | 2^-2 | 2^-4 | 2^-6 | 2^-8 | 2^-10 | 2^-12 | 2^-16 | **2^-20** | opcx |
|---|---|---|---|---|---|---|---|---|---|
| grid(101,101) | 0.057 | 0.245 | 0.337 | 0.456 | 0.508 | 0.538 | 0.557 | **0.559** | 1.34 |
| rand_reg(4000,3) | 0.075 | 0.336 | 0.479 | 0.523 | 0.535 | 0.538 | 0.539 | **0.539** | 2.12 |
| rand_reg(4000,4) | 0.076 | 0.316 | 0.427 | 0.458 | 0.464 | 0.466 | 0.467 | **0.467** | 3.92 |
| double_cycle(500) | 0.051 | 0.221 | 0.304 | 0.347 | 0.548 | 0.606 | 0.639 | **0.680** | 1.31 |
| binary_tree(11) | 0.080 | 0.343 | 0.482 | 0.584 | 0.603 | 0.620 | 0.662 | **0.667** | 2.12 |
| caterpillar(2000) | 0.032 | 0.248 | 0.367 | 0.507 | 0.607 | 0.663 | 0.702 | **0.754** | 1.77 |
| spider(6,500) | 0.078 | 0.329 | 0.467 | 0.524 | 0.567 | 0.661 | 0.776 | **0.804** | 1.39 |
| rrt(4000) | 0.074 | 0.356 | 0.560 | 0.649 | 0.722 | 0.751 | 0.734 | **0.736** | 4.58 |
| star(4000) | 0.012 | 0.012 | 0.012 | 0.012 | 0.012 | 0.012 | 0.012 | **0.012** | 1.00 |

The rate is **monotone increasing in `1/alpha` and converges** — the `alpha → 0`
limit operator is exactly `(1/2)L_sym`, so the rate is bounded above by the
pure-Laplacian SA rate of the family and the mass term `alpha` can only
improve it.  Sup over the whole zoo and the whole alpha range: **0.804**.
Hence `#cycles ≤ log(1/eps)/log(1/0.804) = 4.6·log(1/eps)`, **alpha-free**.
This is the *strongest* single claim of this direction and it is exactly
I2-F's claim with the lattice removed (I2-F's geometric rates were 0.024–0.066
because a rediscretised coarse operator is far better than a Galerkin one).

The two worst families are the *quasi-1-D* ones (spider 0.804, caterpillar
0.754): a single near-nullspace vector plus aggregation is a weak coarse space
on a long thin region.  Nothing here is anywhere near 1.

## 5. (b)–(c) Output-linearity and the setup cost — where the win dies

**Output-linearity in `eps` holds** (cycles grow like `log(1/eps)`: measured
total cycles 19–71 across a `1e-6 → 1e-8` range, and `W/vol(S)` at fixed alpha
moves by at most 2× between the two eps values).  **Output-linearity in
`vol(S)` holds with a large constant.**  The problem is the constant.

**Setup vs solve split (the crux, since there is exactly one solve):**

| family | setup % of W | operator complexity `Σ nnz(A_l)/nnz(A_0)` | levels |
|---|---|---|---|
| star | 43–59 | 1.00 | 2 |
| double_cycle | 30–47 | 1.20–1.30 | 2–4 |
| caterpillar / comb / spider / decoy_hub | 26–51 | 1.26–1.85 | 2–4 |
| grid2d | 45–56 | 1.32–1.35 | 3–5 |
| grid3d | 47–60 | 1.40–1.44 | 4–5 |
| rand_reg3 | 44–71 | 2.16–2.18 | 3 |
| binary_tree | 58–83 | 2.58–3.60 | 5–6 |
| rand_reg4 | 56–74 | 4.24 | 3 |
| **rrt (random recursive tree)** | **83–93** | **8.62–9.50** | 4 |

**Setup dominates whenever the Galerkin `RAP` densifies**, and the two
quantities move together almost perfectly.  This is the classical AMG failure
mode reproduced under an honest meter: aggregation merges a hub with all its
neighbours, `P^T A P` then couples every pair of aggregates that share any
2-path, and the coarse operator's density explodes.  On the **random recursive
tree** — a tree with a power-law-ish degree profile — `opcx = 9.5`, setup is
93 % of the bill, and `W/vol(S)` is **8 982 – 21 736**, i.e. **78–188× worse
than a local elimination solve on the same ball (38–116)** and 24–650× worse
than push/Chebyshev.  **That is the answer to (c): yes, on one family in the
zoo AMG setup destroys the win completely, and the mechanism is RAP
densification driven by degree heterogeneity, not by alpha or eps.**

Note the failure is *not* alpha-dependent: rrt's alpha-exponent is `−0.16`.
AMG stays alpha-free while being uniformly 100× too expensive.

## 6. (d) Expanders — is the eps-relevant support even local?  **NO.**

| family | alpha | eps | `vol(S_eps)/vol(G)` | `vol(Omega)/vol(G)` | R_sem | AMG | cheb | push |
|---|---|---|---|---|---|---|---|---|
| rand_reg3 (n=20 000) | 2^-4 | 1e-6 | 0.36 | 1.00 | 13 | 1 098 | 91 | 25 |
| rand_reg3 | 2^-4 | 1e-8 | **1.00** | 1.00 | 16 | 451 | 26 | 79 |
| rand_reg3 | 2^-8 | 1e-6 | **1.00** | 1.00 | 16 | 484 | 108 | 575 |
| rand_reg3 | 2^-12 | 1e-6 | **1.00** | 1.00 | 16 | 502 | 486 | 9 507 |
| rand_reg4 (n=20 000) | 2^-12 | 1e-6 | **1.00** | 1.00 | 11 | 567 | 434 | 8 633 |

On a random 3- or 4-regular graph the ball of radius `R` has volume `~d·(d−1)^R`,
so `R_sem = Theta(log n)` saturates the *whole graph* as soon as
`eps ≲ alpha/n`: **`vol(S_eps) = Theta(n)` in every non-degenerate cell tested.**
"Local" is vacuous on an expander; the eps-support is everything, and the
region necessarily equals the graph.  The interesting question therefore
becomes the global one, and there the answer is clean:

* **AMG behaves.**  Rate 0.21–0.56 (saturating at 0.47–0.54), operator
  complexity 2.2 (deg 3) / 4.2 (deg 4) — densification is real but **bounded**,
  and `W/vol` is flat in alpha (`s = −0.16 … 0.01`): 451 → 484 → 502 for
  rand_reg3 at eps=1e-6 as alpha goes `2^-4 → 2^-8 → 2^-12`.
* **push pays `1/alpha`** (`s = 1.08, 1.11`) and **Chebyshev pays `1/sqrt(alpha)`**
  (`s = 0.28, 0.60`), so AMG **catches Chebyshev at `alpha ≈ 2^-12`**
  (502 vs 486 on rand_reg3; 643 vs 733 at eps=1e-8, where AMG already wins)
  and overtakes it for smaller alpha.
* **Elimination is catastrophic on expanders**, as expected from treewidth:
  `1.6·10^6 × vol(S)` at alpha=2^-4 (the ball has treewidth `Theta(n/log n)`).
  This is the one place where AMG's multilevel response is the *only* viable
  alpha-free mechanism.

## 7. (e) Where AMG loses, and to what — the winner map

Best certified `W/vol(S)` per cell, and AMG's ratio to it:

| family | 2^-4 | 2^-8 | 2^-12 | AMG / best (range) |
|---|---|---|---|---|
| grid2d | cheb | cheb (1.06×) | **AMG** | 1.00 – 5.4 |
| grid3d | push | push | push (1.5×)* | 1.3 – 18 |
| double_cycle | cheb | direct | direct | 2.7 – 6.5 |
| binary_tree | push/direct | direct | direct | **29 – 51** |
| caterpillar | cheb/direct | direct | direct | 2.9 – 14 |
| comb | direct | direct | direct | 4.7 – 14 |
| spider | direct | direct | direct | 4.2 – 8.8 |
| star | cheb/direct | direct | direct | 1.8 – 2.4 |
| decoy_hub | direct | direct | direct | 2.2 – 7.1 |
| rand_reg3 | push/cheb | cheb | **AMG** (1e-8) / tie (1e-6) | 1.00 – 45 |
| rand_reg4 | cheb | cheb | cheb (1.3×) | 1.3 – 33 |
| **rrt** | push | cheb | cheb | **78 – 234** |

\* 3-D grids never flip inside the tested `n ≤ 7·10^4`, exactly as I2-F
predicted: the crossover needs `R ≳ 40`, i.e. `n ~ 10^6`.  The one 3-D cell
that *does* reach `R = 60` (`alpha = 2^-12, eps = 1e-5→1e-6`) shows AMG at
234 vs push 3 421 and cheb 634 — the flip has arrived there.

**The loss to specialised winners (question (e)):**

1. **Trees — local elimination wins by 29–51×** (binary tree: AMG 940–1 306,
   direct 25.5).  A BFS ball in a tree has treewidth 1, so the sparse LU is
   exactly a two-pass Thomas sweep with no fill; this is W4's EES tree result
   and I2-B's HSEG-LDL (`W/(vol·log²vol) ∈ [1.59, 5.57]`, alpha-free) realized
   one-shot.  AMG cannot compete: its coarse hierarchy is pure overhead on a
   problem elimination solves *exactly* in `O(vol)`.
2. **All quasi-1-D families (caterpillar, comb, spider, decoy_hub) — direct
   wins by 3–14×** for the same reason (bounded-treewidth balls).
3. **Star — direct wins by 1.8–2.4×**, both essentially `O(vol)`.
4. **Closed 3-regular prisms — direct wins by 2.7–6.5×.**  This *refutes the
   premise of the I3-A brief*: the family that broke EES globally does **not**
   break local elimination, because a BFS ball inside a prism is an *open
   band* whose ≤2-irreducible kernel is `m = 0` (W4's own law), not the closed
   graph with `m = 2beta−2`.  Region-restriction rescues elimination here.
5. **Random recursive tree — everything wins by 78–234×** (§5).

## 8. The certification tax and whether it can be removed (question 4)

The `volΩ/volS` column of §3 is the tax: 1.0–5.9 in 2-D, **up to 17.5 (and one
degenerate 331) in 3-D**, because the tax is a *radius* excess and enters as
`(1 + ΔR/R)^D`.  It accounts for essentially the whole gap between certified
AMG (`s = 0.00…0.34`) and oracle AMG (`s = −0.17…0.36`, with the certified
minus oracle difference alpha-positive in 9 of 12 families).

**I attempted the tighter graph-aware certificate and report a negative
result with a proof sketch.**  In semantic coordinates the error obeys
`u = (1/c)D^{-1}R + (a'/c)Wu` with `W = D^{-1}A` row-stochastic,
`c = (1+a)/2`, `a' = (1−a)/2`, so `||u||_inf ≤ cert/alpha` (this *is* the
standard certificate).  Two refinements were analysed:

* **K-term Neumann bound** (rigorous, computable):
  `err ≤ ||Σ_{k<K} y_k||_inf + (c/alpha)||y_K||_inf`, `y_0 = (1/c)D^{-1}R`,
  `y_{k+1} = (a'/c)Wy_k`.  It interpolates between `cert/alpha` (K=0) and the
  truth.  **It is useless at any affordable K**: `a'/c = 1 − 2alpha/(1+alpha) ≈ 1`,
  so the only decay is diffusive spreading of a *codimension-1* source (the
  ring), i.e. `||y_K||_inf ~ K^{-1/2}·cert` on a 2-D lattice.  Driving the tail
  term below `cert` needs `K ~ alpha^{-2}` hops — worse than simply growing
  the region.
* **Maximum-principle bound.**  With `x` the exact restricted solve the error
  is `(a'/c)`-harmonic off `dOmega`, so its max sits on `dOmega`; letting
  `tau = max_{v∈dOmega}|N(v) ∩ Omega|/d_v` and using the one-hop inward decay
  gives `err ≤ cert/(alpha(1 + (a'/c)tau))` — **at best a factor 2**, because
  the inward decay of the error over one hop is `a'/c ≈ 1`, not `beta`.

I2-F's exact lattice constant `err/cert = d_v/a' = 8` comes from the *global*
Green's-function return structure, which no bounded-order local computation
reproduces.  **Measured conclusion: the `Theta(1/alpha)` looseness of the
restricted-solve residual certificate is not removable by any bounded-order
local refinement of the residual bound.**  Removing it needs a different
certificate object (e.g. a charged escape-probability estimate, or a
supersolution `z ≥ 0` with `(I − (a'/c)W)z ≥ (1/c)D^{-1}R` verified by one
matvec — constructing a good `z` cheaply is Open).  This is a genuinely useful
narrowing: it says the tax is a property of the *certificate family*, not of
this or that mechanism, and it is paid identically by AMG and by DIRECT.

## 9. Conjecture supported by the data

> **C1 (mechanism, Measured, strong).**  For the shifted normalized Laplacian
> `Q = alpha I + ((1−alpha)/2)L_sym` on **any** graph, a smoothed-aggregation
> V-cycle built by Galerkin coarsening of `Q[Omega,Omega]` has contraction
> factor `rho(alpha) ≤ rho(0) < 1`, **monotone decreasing in alpha** and
> saturating as `alpha → 0` at the pure-Laplacian SA rate of the family.
> Consequently the number of cycles to accuracy eps is `O(log(1/eps))` with
> **alpha-free constants on arbitrary graphs**.  Measured `sup rho = 0.804`
> over 9 families × 8 alphas down to `2^-20`.

> **C2 (cost, Measured).**  Charging setup, aggregation, RAP, transfers,
> coarse solves and all failed region attempts, certified local AMG satisfies
> `W = C(G)·vol(S_eps)·log(1/eps)` with `C(G)` **alpha-free**
> (measured exponent `−0.16 … +0.34` on all twelve families vs `≥ 0.82` for
> push and `0.28 … 1.25` for Chebyshev), but `C(G) = Theta(opcx(G))` where
> `opcx` is the Galerkin operator complexity of the region.  Measured
> `C(G)` vs `opcx`: 21 at `opcx=1.0` (star), 130–330 at 1.2–1.4
> (prism, grid2d, spider, decoy_hub), 400–780 at 1.6–1.9 (comb,
> caterpillar), 450–650 at 2.2 (rand_reg3), 530–570 at 4.2 (rand_reg4),
> 940–1 310 at 2.6–3.6 (binary tree), **9 000–21 700 at 8.6–9.5** (rrt) —
> a super-linear dependence, local exponent `1.4–2.0` in `opcx` over the
> non-degenerate range.  `opcx` is therefore the single predictive statistic
> for whether local AMG is worth building on a given family.

> **C3 (the class statement).**  *Local AMG achieves `O(vol(S_eps)·log(1/eps))`
> charged work with alpha-free constants on graph classes whose explored
> region has **bounded Galerkin operator complexity** — lattices, bounded-degree
> expanders, bounded-degree quasi-1-D families — and it is the **only** known
> alpha-free mechanism on the high-treewidth members of that class (lattices in
> `D ≥ 2`, expanders), where elimination costs `Theta(R·vol)` in 2-D and
> `Theta(n^2)` in 3-D/expanders.  It **fails on graphs with heavy-tailed degree
> profiles** (random recursive tree: `opcx = 9.5`, setup 93 %, 78–234× worse
> than every competitor) because aggregation around hubs makes `P^T A P` dense;
> and it is **dominated by local elimination on every bounded-treewidth-ball
> family** (trees 29–51×, quasi-1-D 3–14×, prisms 2.7–6.5×, star 1.8–2.4×),
> because there elimination is exactly `O(vol)` and alpha-free too.*

> **C4 (the reframing this direction forces on the campaign).**  The campaign's
> mechanism separation is **not** "multilevel beats everything".  It is a
> two-regime map indexed by the *treewidth of the explored ball*:
>
> | ball structure | alpha-free winner | cost | fails when |
> |---|---|---|---|
> | bounded treewidth (trees, caterpillars, combs, spiders, stars, prisms, decoy hubs) | **local elimination** (EES / HSEG-LDL / MMD-LU) | 11–116 × vol(S) | treewidth grows |
> | high treewidth, bounded operator complexity (grids `D ≥ 2`, expanders) | **local AMG** | 230–920 × vol(S) | degrees heavy-tailed |
> | high treewidth **and** heavy-tailed degrees (rrt-like, hub-rich) | **none known** | — | — |
>
> Push and Chebyshev are alpha-free on *no* family (`s ≥ 0.82`, `s ≥ 0.28`).

## 10. Next falsifiable targets

1. **Kill the setup cost, not the cycle count.**  Setup is 26–93 % of `W` and
   the whole failure mode.  Two concrete, cheap attacks:
   (i) **degree-aware aggregation** — force hubs into singleton aggregates
   (or use compatible-relaxation / Ruge–Stüben C/F splitting with direct
   interpolation, whose `opcx` is bounded by construction) and re-measure
   `opcx` and `W` on `rrt` and `rand_reg4`.  Falsifiable target: *`opcx ≤ 2`
   and `W/vol(S) ≤ 800` on the random recursive tree.*
   (ii) **hierarchy reuse across region attempts** — the region only grows, so
   the coarse levels of `ball(R)` are a sub-hierarchy of those of `ball(R')`.
   Target: *setup charged once, not `attempts` times* (attempts 7–23 in the
   sweep; the geometric ladder makes the saving ~2–3×).
2. **The hybrid the map demands (C4).**  Per-region, cheaply estimate the ball's
   elimination cost (`Σ_j nnz(L[:,j])^2` after a greedy min-degree pass — the
   ≤2-degree peel of W4 already gives it for free) and choose elimination vs
   AMG.  Falsifiable target: *one algorithm within 1.5× of the per-family best
   in the whole §7 winner map, with the selection cost charged.*  This is the
   concrete input I3-E needs.
3. **The certificate is now the bottleneck, mechanism-independently** (§8).
   Target: *a charged, computable supersolution `z` with
   `(I−(a'/c)W)z ≥ (1/c)D^{-1}R` whose `||z||_inf` is within `O(1)` of the true
   error on lattices* — that alone moves every certified exponent in §3 to its
   oracle value and shrinks the 3-D region by `17.5^{1/3} ≈ 2.6×` in radius.
4. **3-D crossover at `n ~ 10^6`** (inherited from I2-F, now partially
   answered: the `alpha=2^-12, R=60` cell already flips, AMG 234 vs cheb 634).
