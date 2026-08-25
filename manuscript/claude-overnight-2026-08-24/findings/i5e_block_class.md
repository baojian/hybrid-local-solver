# I5-E — The block relaxation class `R_B`: the bridge from one-hop signed methods to elimination

**VERDICT.** The block generalization of I4-C is now closed-form. The per-op
seed cap generalizes from `2√(α(1+α))` to

> `|Δz_v| ≤ 2·√(γ_α π_v · τ_v(U))`,  `τ_v(U) := ((H_UU)^{-1})_vv`,

a single locally computable quantity (`τ` = the block's *compliance at the
seed*), with the exact global identity `τ_v(V) = π_v/γ_α`. Three consequences:

1. **Star interpolation (exact, two-sided).** On centre-seeded `K_{1,m}`,
   `W(B) = Θ((1/ε)·√(x(B)/α))`, `x(B) = 1 − c_α²(B−1)/m`. The conjectured
   `√(α + j/m)` cap is **refuted**: blocks buy only `1/√x`, which is `O(1)`
   until coverage `→ 1`.
2. **Block lower bound: PROVED-draft, stronger than conjectured.** Every member
   of `R_B` with `B ≤ m/2 + 1` pays `W ≥ 0.0083/(√α·ε)` on the star,
   `m = ⌊1/(8ε)⌋`. `g(B) = Θ(1)` — *no* polynomial-in-B discount. The
   candidates `g = √B`, `g = B` are dead. Escape requires **output-scale
   coverage** `B = (1 − O(α))·m = Θ(1/ε)`, at which point `W = Θ(1/ε)` (sharp
   phase transition, both endpoints measured).
3. **What forces block methods is VOLUME, not propagation.** On the path,
   blocks of size `b` advance the frontier `b` hops per op (linear, not `√b`)
   and `B ≳ 0.28/√α` collapses `W` to `1.3–2.8 × vol(S_ε)` — the path forces
   nothing beyond volume. On the star/double-star/spider, `τ` is an exact
   *coverage-fraction* functional of the reflecting boundary, and only
   near-total coverage escapes.

Code `/home/claude/work/overnight/i5e/{core.py, exact_checks.py, star_law.py,
battery.py}`; logs/data `i5e/out/`. Exact checks: **42/42** Fraction
identities; float battery: **0 cap violations** over every policy run
(max utilization 1.0000, attained, never exceeded), plus 1 316 *inexact*
monotone block updates (max 0.23). Conventions as I4-C (`H = I − c_α A D^{-1}`,
`H π = γ_α e_v`, semantic stop `max_u |π_u − z_u|/d_u ≤ ε`). Runtime ≈ 14 min.

---

## 1. The class `R_B` (decision recorded)

A member maintains `(z, r)`, `z⁰ = 0`, `r = γ_α e_v − H z` (signed). Primitive
= **ω-relaxed exact block relaxation** on any `U`, `|U| ≤ B`, `ω ∈ (0, 2]`:

> `δ = H_UU^{-1} r_U`; `z_U += ω δ`; `r −= ω H[:,U] δ`.

`ω = 1` is block Gauss–Seidel: `z_U ←` exact solve of the restricted system
given current boundary values. **`R_B` includes `ω ≠ 1`** (decided here), so
`R_1 = R±` exactly, and `R_n ∋` the one-shot full solve. Adaptive, randomized,
per-op-varying `(U_t, ω_t)` all allowed.

**Charging (both reported).** `W_vol = Σ vol(U_t)` (adjacency exposure — the
I4-C-comparable scale); `W_S1 = Σ vol(U_t) + (|U_t| + intE(U_t))` (structured
solve — honest for tree/banded blocks, which is every optimal block below:
star arrowheads, path windows, spider sub-trees); `W_S3 = Σ vol + |U|³` (dense
worst case). All lower bounds below use `W_vol` only, so they hold under any
charging. In the tables `W_S1 ≈ 2·W_vol`; dense `W_S3` would matter only for
unstructured blocks (`B³ ≫ vol`), where the solve economy becomes exactly
I3-A's elimination/AMG question — see §6.

## 2. The generalized cap lemma

Work in `y = D^{-1/2}(π − z)`, `H_sym = D^{-1/2} H D^{1/2}`,
`Φ = ½ yᵀH_sym y`, `Φ₀ = γ_α π_v/(2 d_v)`.

**Definition (block compliance).**
`τ_v(U) := ((H_sym)_UU^{-1})_vv = ((H_UU)^{-1})_vv` (diagonal similarity
preserves inverse diagonals; so `τ` is computable from adjacency reads of `U`
plus one solve on `U`). Variationally

> `τ_v(U) = max { x_v² / (xᵀ H_sym x) : supp(x) ⊆ U }`,

i.e. the block's capacity to support a low-Rayleigh (slow-mode-aligned) vector
with mass at `v` — this is I4-C's "spectral alignment with the slow mode" made
precise. `τ` is monotone in `U`, `τ_v({v}) = 1`, and **`τ_v(V) = π_v/γ_α`
exactly** (from `π = γ_α H^{-1} e_v`; verified in exact rationals, E2). So the
seed-amplification parameter of I4-C Prop 3.4 *is* the full-graph compliance.

**Lemma B1 (Proved-draft; exact-op form).** Every `R_B` op with `v ∈ U` obeys

> `|Δz_v| ≤ ω·√(2 Φ_t d_v τ_v(U)) ≤ ω·√(γ_α π_v τ_v(U))`.

*Proof.* `Δy_v = −ω (G^{-1} SᵀH_sym y)_v = −ω ⟨H_sym w, y⟩` with
`G = (H_sym)_UU`, `w = S G^{-1} ê_v`. Cauchy–Schwarz in the `H_sym` inner
product: `|⟨H_sym w, y⟩| ≤ √(wᵀH_sym w)·√(2Φ)`, and
`wᵀH_sym w = (G^{-1} G G^{-1})_vv = τ_v(U)`. `Φ_t ≤ Φ₀` because each op
dissipates `ΔΦ = −[ω(2−ω)/2]·r_Uᵀ (H_UU D_U)^{-1} r_U ≤ 0` (block energy
identity, verified in exact rationals, E3). ∎

**Lemma B2 (Proved-draft; monotone form — covers inexact solves).** In any run
where `Φ` never increases, **any** update supported on `U` obeys
`|Δz_v| ≤ 2√(γ_α π_v τ_v(U))`.
*Proof.* Let `u* = argmin{uᵀH_sym^{-1}u : u|_U = ê_v|_U}`. Then
`⟨u*, Δy⟩ = Δy_v` (supports), `|⟨u*, y⟩| ≤ √(2Φ₀ · u*ᵀH_sym^{-1}u*)` before and
after, and the Schur identity `min = ê_vᵀ((H_sym^{-1})_UU)^{-1}ê_v… = τ_v(U)`
gives the claim. ∎

B2 is the reach of the lemma: it covers damped-Jacobi-on-`U`, aggregated /
multilevel coarse corrections, any Φ-monotone V-cycle — i.e. local AMG's
correction step *is* a B2 update with `U = Ω` (Galerkin coarsening + convergent
smoothing is a `Q`-norm contraction). Corollary, since `τ ≤ π_v/γ_α`:
`|Δz_v| ≤ 2π_v` always — the cap saturates exactly when the block is fully
aligned, and one saturated op can finish.

**Lower-bound template (alignment price).** `z_v` moves only at ops with
`v ∈ U`, so any member reaching `z_v ≥ π_v − ε d_v` pays

> `W ≥ (π_v − ε d_v) / (2√(γ_α π_v)) · min_{U ∈ 𝒰, U ∋ v} vol(U)/√(τ_v(U))`.

The whole design problem of the campaign is minimizing **`vol(U)/√(τ_v(U))`**.

**Verification status.** E1–E4: 42/42 exact-rational checks (star `τ` closed
form; `τ_v(V) = π_v/γ`; block energy identity for 4 blocks incl. `ω = 19/10`;
9-op adversarial exact run, max `(Δz_c/cap)² = 0.727`). Float battery
(star / path / spider / double-star × coordinate sweeps, windows, greedy
top-B, hub-blocks, `ω` up to `2−10⁻⁶`): **0 violations**; utilization reaches
**1.0000 exactly** on one-shot escape ops (first op from `z = 0` has
`|Δz_v|/cap = √(τ_v(U)/τ_v(V))` — the lemma is sharp). B2 on 1 316 inexact
monotone updates: max 0.23, 0 violations.

## 3. The star interpolation, exact

`U = {c} ∪ (j leaves)`: `τ_c(U) = 1/(1 − c_α² j/m)` **exactly** (E1), so with
`γ_α π_c = α` exactly:

> `cap(j) = 2√(α / x)`, `x = 1 − c_α² j/m ≈ (1 − j/m) + 4α j/m`.

The hypothesized `√(α + j/m)` growth is wrong: alignment improves like
`1/√(1 − coverage)`, i.e. **not at all** until the block covers nearly every
leaf, then diverges to the saturated cap `1 + α` at `j = m`.

**Measured two-sided law** (`star_law.py`, reduced 3-dim dynamics — proven
exact against the full simulator to `8.9e-16` — member: `{c}+j` block
alternating with outside-leaf pass, `ω` optimized per cell; `m = 64`,
`ε = 1/(8m)`, 45 cells: `α ∈ {2⁻⁶…2⁻¹⁴} × j ∈ {0…64}`):

| quantity | range over all 45 cells |
|---|---|
| `N_c / N_c^LB` (centre ops vs Lemma B1 bound) | **1.77 – 3.10** |
| `W_vol / W^LB` | **1.81 – 3.92** |
| `W_vol·√α·ε / √x` | **0.083 – 0.144** (flat in `α` and in `j`) |

> **`W(B) = Θ((1/ε)·√(x(B)/α))`, `x(B) = 1 − c_α²(B−1)/m`,** pinned two-sided
> within ≈ 3.9× uniformly, including both endpoints: `B = 1` gives I4-C's
> `Θ(1/(√α ε))`; `B = m+1` gives one op, `W_vol = 2m = 1/(4ε)`, `err = 0`.
> Best schedules: `ω_b → 2` while many ops are needed, `ω_b = 1` at the
> one-shot end — exactly the cap's `ω`-dependence. The optimal
> `B(α, ε)` is degenerate: nothing between `Θ(1)` and `Θ(1/ε)` is ever optimal
> (`W` decreases in `B` only through `√x`, while every centre op costs
> `≥ m` regardless), so a designer should use `B = 1` or `B ≥ |S_ε|`, never in
> between. Greedy top-B (residual-driven) never beat the structured member
> (10–20× worse at `B = 33`) and never violated the cap.

## 4. The block class lower bound (Q3): PROVED-draft on the star

**Theorem B3.** Centre-seeded `K_{1,m}`, `m = ⌊1/(8ε)⌋`, `ε ≤ 1/16`. Every
member of `R_B` with `B ≤ m/2 + 1` that reaches the semantic guarantee
performs `N_c ≥ 3/(16√2·√α)` centre-block ops (each with `vol(U) ≥ d_c = m`),
hence

> `W_vol ≥ 3m/(16√2·√α) ≥ (3/(256√2))·1/(√α·ε) ≈ 0.0083/(√α·ε)`,
> and always `W_vol ≥ m ≥ 1/(16ε)`.

*Proof.* `z_c` moves only at ops with `c ∈ U`; those have `j = |U|−1 ≤ m/2`,
so `τ_c(U) ≤ 1/(1 − c_α²/2) ≤ 2` and `cap ≤ 2√(2α)` (Lemma B1, `ω ≤ 2`).
Pathwise `Σ|Δz_c| ≥ π_c − εm ≥ 3/8`. ∎ (Pathwise ⇒ randomized members obey it
with probability 1; adaptivity free; same-`U` bursts compose as in I4-C E2.)

**So `g(B) = Θ(1)`: bounded blocks buy *nothing* on the star** — the
`Ω(1/(√α ε))` of I4-C survives every `R_B` with `B` up to half the output
support, and then collapses (not degrades) to `Θ(1/ε)` at `B ≈ |S_ε|`. Both
conjectured forms `g = √B` and `g = B` are refuted. Under the dense charging
`W_S3` the bound only strengthens; the `Θ(1/ε)` upper endpoint survives because
the star block is an arrowhead (structured solve `O(m)`).

**The path kills nothing — and blocks kill the path.** On the path, `τ_v` of a
`b`-prefix grows ≈ linearly and saturates at `π_v/γ_α = Θ(1/√α)` at
`b* ≈ 0.28/√α` (measured: `b*·√α = 0.375, 0.312, 0.281, 0.281, 0.281` for
`α = 2⁻⁶…2⁻¹⁴`). The template then yields at most `Θ(α^{-1/4})` seed ops even
at `B = 1` (I4-C Prop 3.4's honest degradation), and `vol(S_ε) =
Θ(log(1/ε)/√α)` dominates: the path never forces `1/(√α ε)`. Measured minimum
work (`n = 1600`, `ε = 2⁻⁹`, best of coordinate-`ω` sweeps / windows / greedy):

| `α` | `vol(S_ε)` | `W/vol`, B=1 | B=4 | B=16 | B=64 | B=256 |
|---|---|---|---|---|---|---|
| 2⁻⁶ | 33 | 23.4 | 25.8 | **1.9** | 2.8 | 2.8 |
| 2⁻¹⁰ | 89 | 28.9 | 25.4 | 32.2 | **1.4** | 1.7 |
| 2⁻¹⁴ | 177 | 59.1 | 44.4 | 11.6 | 12.8 | **1.3** |

The collapse point tracks `b* = Θ(1/√α)`, and a window advances the frontier
`b` hops per op — **linear in `b`, not `√b`** (ops fall ≈ ×14 for `b`×4 in the
pre-saturation regime). Propagation is cheap for blocks; it cannot carry a
block lower bound.

**Spider = the product instance (both axes at once).** `k = 8` arms, hub seed:
measured **exactly** (deviation ≤ 6e-14, all 75 cells)

> `τ_hub(t arms × depth p) = 1 / (1 − (t/k)·σ(p))`,

arm-additive by Schur complement, with `σ(p)` saturating at `1 − Θ(√α)` at
`p ≈ b*`. Escape needs **all `k` arms** (volume axis) **and** depth `Θ(1/√α)`
(propagation axis): `B* = Θ(k/√α) = Θ(vol(S_ε))` again. Measured
(`ε = 2⁻¹¹`; at `ε = 2⁻⁹`, `S_ε = ∅` for `α = 2⁻¹⁴` — I4-C §6.1's phenomenon
recurs): sub-escape blocks grind (`B = 129` at `α = 2⁻¹⁴`: `τ/τ_V = 0.26`,
unconverged at `W = 76·vol`), support-scale blocks one-shot
(`B = 449`: 1 op, `W = 1.22·vol`, utilization 0.84). Double-star (`m₁ = m₂ =
40`, `α = 2⁻¹²`): `τ(c₁+own leaves) = 39.5`, adding the bridge hub `c₂` gives
only `40.4`, full graph `528.6` — **crossing the bridge is worthless without
the far reflector's volume**: it is coverage of reflecting volume, not reach,
that `τ` prices.

## 5. What `S_ε`-scale blocks cost is the only remaining question

Theorem B3 + the template reduce every class in the campaign to one ratio:
`min_U vol(U)/√(τ_v(U))` subject to what the primitive may build, times the
price of actually *applying* a `τ`-saturated update. For `U ⊇ S_ε`-scale
regions the update is a linear solve on `U`, and its honest price is exactly
I3-A's two-regime map: `O(vol)` by elimination on bounded-treewidth balls,
`O(vol·polylog)` by AMG on bounded-`opcx` balls, open on hub-rich
heavy-tailed balls.

## 6. THE LADDER (the campaign's mechanism map as one statement)

> Every local method the campaign has studied is a Φ-monotone sequence of
> supported updates, and its `α`-scaling is decided by one quantity: the
> compliance `τ_v(U) = ((H_UU)^{-1})_vv ≤ π_v/γ_α` of the supports it can
> afford, through the pathwise cap `|Δz_v| ≤ 2√(γ_α π_v τ_v(U))`.
> **Coordinates** (`τ = 1`, I4-C): the cap is `2√(γ_α π_v)` and reflecting
> seeds pay `Θ(1/(√α ε))` — proved two-sided. **Bounded blocks** (`τ ≤
> 1/(1−coverage)`, this direction): the cap moves only through boundary
> coverage, so `B` below the output scale buys `Θ(1)` and the same
> `Ω(1/(√α ε))` holds — proved on the star, `g(B) = Θ(1)` for `B ≤ |S_ε|/2`.
> **Output-scale blocks** (`τ = Θ(π_v/γ_α)`): the cap saturates at `2π_v`,
> one aligned update can finish, and *all* `α`-dependence migrates into the
> price of the block solve — `Θ(1/ε)` by closed form on the star, `O(vol)`
> by elimination on bounded-treewidth regions, `O(vol·polylog)` by multilevel
> solves on bounded-`opcx` regions (I3-A, measured `α`-free everywhere it is
> affordable). Local AMG is exactly a B2 update with `U = Ω` and an
> approximate solve; its measured `α`-freeness is the statement
> `τ_v(Ω)/τ_v(V) → 1` once `Ω` covers the seed's reflecting volume. The
> ladder rungs — `Θ(1/(αε))` monotone, `Θ(1/(√α ε))` signed one-hop,
> `Θ(1/ε)` elimination — are not three phenomena: they are the single cap
> evaluated at `τ = 1` with `r ≥ 0`, `τ = 1` signed, and `τ = π_v/γ_α`.
> What separates `1/√α` from `α`-free is therefore **not** iteration count,
> momentum, or step size — it is whether the primitive can afford supports
> whose compliance at the seed is a constant fraction of `π_v/γ_α`.

## 7. Status table

| # | statement | status |
|---|---|---|
| B1 | exact-op block cap `|Δz_v| ≤ ω√(γπ_v τ_v(U))` | **Proved-draft**; 42/42 exact checks; 0 float violations, utilization attains 1.0000 |
| B2 | monotone-update cap (factor 2), covers inexact/AMG updates | **Proved-draft**; 1 316-op inexact battery, 0 violations |
| B3 | `R_B` pays `Ω(1/(√α ε))` on the star for `B ≤ m/2+1`; `g(B) = Θ(1)` | **Proved-draft** (pathwise); tight to 1.8–3.9× |
| B4 | star law `W(B) = Θ((1/ε)√(x(B)/α))`, `x = 1−c_α²(B−1)/m` | **Measured two-sided** (45 cells, const 0.083–0.144 flat) + LB proved |
| B5 | `τ_v(V) = π_v/γ_α`; star/spider/double-star `τ` closed forms | **Proved-draft + exact-rational** (spider arm-additivity: measured exact, 6e-14) |
| B6 | path: blocks advance `b` hops/op; `b* ≈ 0.28/√α`; no path LB above `vol` | **Measured** |
| B7 | hypothesis `cap ~ √(α + j/m)` | **Refuted** (truth: `2√(α/(1−c_α² j/m))`) |

**Gaps.** (i) B3's UB/LB constant gap (1.8–3.9×) unclosed, as in I4-C.
(ii) B3 covers `R_B` (exact block relaxations); extending the *theorem* to all
B2-monotone bounded-support methods needs only replacing `ω ≤ 2` by the
factor-2 cap — done in the proof, but an adversary with non-monotone updates
(e.g. deliberately Φ-increasing detours) is outside every class here; nothing
in the campaign uses one. (iii) The `1/ε` additive floor is star-specific
volume; a family forcing `Ω(1/(√α ε))` against *output-scale* structured
blocks would have to defeat elimination too — I3-A's heavy-tailed-`opcx`
family (rrt) is the natural candidate and is **the** next target.

**Next target.** The ladder says the open problem is now exactly: *is there a
family where every affordable support with `τ_v(U) = Ω(π_v/γ_α)` has
elimination/AMG cost `ω(vol·polylog)`?* Concretely: hub-rich balls (rrt-like)
where I3-A measured `opcx = 9.5` and no `α`-free solver is known. Prove either
(a) a `vol(U)/√τ_v(U)` + solve-price lower bound there for all Φ-monotone
bounded-fill methods — which would be the first *computational-restriction*
result matching the project's central question — or (b) a degree-aware
multilevel scheme (I3-A target (i)) that caps `opcx`, which would collapse the
last rung and argue the aspirational `O~(1/(√α ε_ppr))` is beatable to
`O~(vol(S_ε))` on all families the campaign owns.
