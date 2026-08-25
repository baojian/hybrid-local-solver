# I2-D — Monotone-residual push vs. signed relaxation: a √α separation on the star

Candidate manuscript section. Status labels are per-statement:
**Proved-draft** (complete argument written here, unaudited),
**Measured** (numerics only), **Open**.

Code: `w9_i2d/{potential.py, sor_star.py, outmap_lp.py, threshold.py,
member_check.py}`, reusing `w1_monotone_lb/gpush.py` and `lib/zoo.py`.
Total rerun ≈ 4 min. Supersedes Lemmas 3–5 of `findings/w1_monotone_lb.md`.

**Headline.** The anti-acceleration axiom is **`r ≥ 0`**, not the sign of the
step. Signing the step amount (`η < 0`, "anti-pushes") does *not* help — the
Θ(1/(αε)) star bound survives verbatim, with a *better* constant than
iteration 1's. Signing the *residual* does help: SOR at ω⋆ finishes in
O(log(1/α)/(√α ε)). And the output map is governed by exactly one scalar —
its column mass `B` — with a threshold `B = 1 − ε·vol` that is sharp.

---

## 0. Setting

Lazy operator, mass scale. `a=(1−α)/2`, `c=(1+α)/2`, `c_a=(1−α)/(1+α)`,
`M_op = cI − a A D⁻¹`, `pr(h) = α M_op⁻¹ h`, `π = pr(e_v)`, `vol = Σ_u d_u`.

Facts (each one line): **F1** `1ᵀpr(h)=1ᵀh`; **F2** `h≥0 ⇒ pr(h)≥0`
(`M_op⁻¹ ≥ 0` entrywise, Neumann series); **F3** `pr(h) ≥ αh` for `h≥0`;
**F4** `max_u pr(h)_u/d_u ≤ max_u h_u/d_u` for `h≥0` (from `pr(d)=d`);
**F5** `|pr(h)| ≤ pr(|h|)` entrywise (F2 applied to `|h|±h`).

**Definition 0.1 (generalized push).** `gp(u,η)`: `r[u] −= (1+α)η/2`;
`r[w] += (1−α)η/(2d_u)` for `w ~ u`; `p[u] += αη`; charged work `d_u`.
It preserves `p + pr(r) = π` for every `η ∈ ℝ` (Lemma 1 of
`w1_monotone_lb.md`: (A1) one-hop + (A2) invariant-exact + (A4) `p` changes
only at the base **force** this form; the neighbour split is forced, the sign
of `η` is the only free boundary).

**Definition 0.2 (three classes).** State `(p,r)`, init `(0,e_v)`, arbitrary
adaptive/randomized/batched policy, work `d_u` per op.

| class | steps | residual | contains |
|---|---|---|---|
| **M₊** monotone push | `η > 0` | `r ≥ 0` always | ACL/APPR, non-lazy CF push, damped ω≤1, Jacobi, partial/below-threshold pushes |
| **M±** signed step | `η ∈ ℝ` | `r ≥ 0` always | M₊ + anti-pushes ("pumping") |
| **R±** signed relaxation | `η ∈ ℝ` | unrestricted | M± + GS-SOR with ω>1 |

Correctness: the output `out` must satisfy `err := max_u (π−out)_u/d_u ≤ ε`.

**Definition 0.3 (one-hop output class `O_B`).** `out = p + M r` with
`M ≥ 0`, `M_{uw}=0` unless `w ∈ N[u]`, and column mass bounded:
`1ᵀM ≤ B·1ᵀ`. Membership of the natural candidates:

| output map | `B` |
|---|---|
| `p` | 0 |
| `p + βr` | β |
| one Jacobi/Neumann smoothing step `M_J = α(1+a)I + aα AD⁻¹` | `α(2−α)` |
| `p + r` | 1 |

An entrywise-bounded family (`M_{uu} ≤ B`, `M_{uw} ≤ B/d_w`) sits inside
`O_{2B}`, so the column-mass parameter is the sharper one. *(Measured: at
α=1/4, 1/16, 1/64 the Jacobi step has B = 0.4375, 0.1211, 0.0310.)*

---

## 1. T1 — the output map: a sharp threshold at `B = 1 − ε·vol`

### 1.1 The mass-deficit lemma

**Lemma 1.1 (Proved-draft).** Let `r ≥ 0` and `out = p + Mr` with `M ∈ O_B`
satisfy `err ≤ ε`. Then `(1−B)·‖r‖₁ ≤ ε·vol`.

*Proof.* Sum `(π − p − Mr)_u ≤ ε d_u` over `u`. By F1 and `r ≥ 0`,
`Σ_u (π−p)_u = 1ᵀpr(r) = 1ᵀr = ‖r‖₁`. And
`1ᵀMr = Σ_w r_w (1ᵀM)_w ≤ B‖r‖₁`. Hence `‖r‖₁ − B‖r‖₁ ≤ ε·vol`. ∎

Note the lemma is informative — i.e. it forces `‖r‖₁ < 1`, which is what the
work bound consumes — **exactly when `B < 1 − ε·vol`**. §1.3 shows that
threshold is not an artifact.

### 1.2 Exactly which output maps escape (new)

**Lemma 1.2 (transport characterization; Proved-draft).** Fix a state `(p,r)`,
`r ≥ 0`. There exists `M ∈ O_B` with `err(p+Mr) ≤ ε` **iff** for every
`S ⊆ V`

  `Σ_{u∈S} [ pr(r)_u − ε d_u ]₊  ≤  B · r(N[S])`,  where `N[S] = ⋃_{u∈S} N[u]`.

*Proof.* Put `N_{uw} := M_{uw} r_w` for `w ∈ N[u]` with `r_w > 0` (columns with
`r_w=0` contribute nothing to `Mr`, so they may be ignored). The guarantee is
`Σ_w N_{uw} ≥ (π−p)_u − ε d_u = pr(r)_u − ε d_u` (row demands); `M ∈ O_B` is
`Σ_u N_{uw} ≤ B r_w` (column capacities); `N ≥ 0`. This is a bipartite
transportation feasibility problem on the "closed-neighbourhood" bipartite
graph, and Gale–Hoffman/Hall gives the stated cut condition. ∎

This answers gap G1's question "*which* output maps are forbidden?" exactly:
a one-hop map escapes iff residual mass can cover the outstanding PPR demand
**within one hop**. Two consequences:

* Taking `S = V` recovers Lemma 1.1 (`N[V]=V`), so the `S=V` cut is the only
  one that can produce an α-dependence; every other cut is a *transport*
  (locality) obstruction.
* On a graph of radius 1 around the seed — the star — `r(N[S]) = ‖r‖₁` for
  every non-empty `S`, so `S = V` is the *only* binding cut. **On the star,
  the whole output-map question collapses to the single scalar `B`.**

*(Verified by LP: `outmap_lp.py` solves the primal feasibility LP directly;
`threshold.py` prints the cut values. At α=1/64, ε=2⁻⁸, m=32, W=m: the cuts
`{c}`, all-leaves, half-leaves, one leaf need `B ≥ 0.373, 0.373, 0.249,
0.023`, and `S=V` needs `B ≥ 0.746` — binding, as predicted.)*

### 1.3 Sharpness — and why a second instance cannot rescue `B = 1`

**Proposition 1.3 (Proved-draft + Measured).** Centre-seeded star `K_{1,m}`,
`m = ⌊1/(8ε)⌋`, so `ε·vol = 2εm ≤ 1/4`. Then:

1. (*zero-work escape*) For every `B ≥ 1 − ε·vol` there is `M ∈ O_B` with
   `err(M e_c) ≤ ε` at **`W = 0`**. *Proof.* `π_c = c = (1+α)/2` and
   `π_l = a/m` (solve `M_op π = α e_c`), so `π_u > ε d_u` for all `u` when
   `εm < a`, i.e. for `α < 3/4`; then the only Hall cut is `S=V`, with demand
   `Σ_u(π_u − εd_u) = 1 − ε·vol` and capacity `B·r(N[V]) = B`. ∎
2. (*one-push escape*) After one full lazy centre push (`W = m`, `η=1`) the
   residual is exactly degree-stationary, `r = (a/m)·d`, so `pr(r) = r` and
   `M = B·I` works iff `(1−B)a/m ≤ ε`, i.e. `B ≥ 1 − ε·vol/(1−α)`.
3. Both thresholds are **attained**: LP bisection over `B` returns
   `B* = 0.7500 = 1−ε·vol` at `W=0` and `B* = 1−ε·vol/(1−α)` at `W=m`
   (0.6667, 0.7333, 0.7460, 0.7490 for α = 1/4, 1/16, 1/64, 2⁻⁸) — matching
   the closed forms to 4 decimals on all 8 grid cells.

**Consequence (honest, and it contradicts the plan for this iteration).** The
requested strengthening — *a second instance on which `p + Mr` fails for every
admissible `M` unless Ω(1/(αε)) work was done* — **is false for `B = 1`, on
the star and on every radius-1 instance**, by Lemma 1.2. Two checks:

* *Two-seed family with a shared `M`* (`outmap_lp.py` T1.c): the same star,
  runs seeded at the centre and at a leaf, one `M` shared. The LP is feasible
  at `B = 0.9` and `B = 1` with `W_centre = m` and `W_leaf = 1`. The
  "leaf-seeded residual is not degree-stationary" intuition is correct but
  irrelevant: `B=1` maps do not need stationarity, only one-hop coverage.
  (And even for `M = I` alone the leaf-seeded star is escapable in `m+1`
  work: a tuned partial centre push `η = c_a` lands exactly on `r ∝ d`.)
* *Larger radius does bite, but only as transport* (`outmap_lp.py` T1.d,
  α=1/64, ε=2⁻⁷, greedy non-lazy): minimum work for a feasible `M ∈ O_1` is
  `192 = 6.4·vol` on `path(16)`, `254 = 6.7·vol` on `caterpillar(10)`,
  `64 = 1.3·vol` on `spider(6,4)`, `30 = 0.5·vol` on `binary_tree(4)`. These
  are Ω(vol) locality bounds, **not** Ω(1/(αε)): the α-price lives only in
  the `S=V` cut, which `B=1` neutralizes by construction.

So the theorem *must* scope the output map, and the right scope is the column
mass. That scoping is tight, not a modelling convenience.

---

## 2. T2 — the settling potential: the bound is sign-of-η agnostic

This closes gap G2 (signed `η` with `r ≥ 0`) and retires Lemmas 3–5 of
iteration 1.

**Definition 2.1.** For the seed `c`, put `Ψ(r) := pr(r)_c / π_c = ⟨φ, r⟩`
with `φ_u := pr(e_u)_c / π_c`. Equivalently `Ψ = (π_c − p_c)/π_c`: the
**fraction of the target's own value at the seed that is still unsettled**.
`φ ≥ 0` (F2), `φ_c = 1`, `Ψ(0) = 1`, `Ψ ≥ 0` whenever `r ≥ 0`.
On the star, `π_c = (1+α)/2` and `φ_l = a/π_c·(1/1) = c_a`, so
`Ψ = r_c + c_a Σ_{l∈L} r_l`.

**Lemma 2.2 (exact, axiom-free; Proved-draft).** Any state change preserving
`p + pr(r) = π` has `ΔΨ = −Δp_c/π_c`. In particular
`gp(u,η)` gives `ΔΨ = −(α/π_c)·η·[u = c]`: **`Ψ` is invariant under every
operation not based at the seed, for either sign of `η`.**
*Proof.* `Δp = pr(−Δr) = −αM_op⁻¹Δr`, so
`ΔΨ = e_cᵀM_op⁻¹Δr·(α/π_c) = −Δp_c/π_c`. ∎
*(Verified to 3.6e-15 absolute over 300-op random signed sequences on 10 zoo
graphs × 3 values of α — `potential.py` P1. `φ ≥ 0` and `‖φ‖_∞ = φ_c` held on
every cell.)*

**Lemma 2.3 (one-sided multiplicative step; Proved-draft).** Let `r ≥ 0` and
let `κ := 2α/((1+α)π_c) ∈ (0,1)`. Then every operation satisfies `ΔΨ ≥ −κΨ`,
and `ΔΨ < 0` only at seed-based operations with `η > 0`.
*Proof.* Non-seed ops and `η<0` seed ops: `ΔΨ ≥ 0` by Lemma 2.2. For a seed
op with `η>0`, feasibility (`r_c ≥ 0` after the op) gives `η ≤ 2r_c/(1+α)`,
and monotonicity of `pr` with `r ≥ r_c e_c ≥ 0` gives
`pr(r)_c ≥ r_c pr(e_c)_c = r_c π_c`, i.e. `r_c ≤ Ψ`. Hence
`−ΔΨ = αη/π_c ≤ 2αr_c/((1+α)π_c) ≤ κΨ`. ∎
On the star `κ = κ₊ := 4α/(1+α)²`, and `κ₊<1` for all `α∈(0,1)`.
*(Measured: `max` observed `−ΔΨ/Ψ` over random signed runs is 0.585/0.640,
0.202/0.221, 0.0554/0.0606 of the bound on `star(8)` at α=1/4,1/16,1/64, and
never exceeds it on any of 6 graphs × 3 α — `potential.py` P3.)*

**Theorem 2.4 (class lower bound for M± ⊇ M₊; Proved-draft).** Centre-seeded
star `K_{1,m}`, `m = ⌊1/(8ε)⌋`, `ε ≤ 1/16`, `α ∈ (0,1)`. Let a member of
**M±** stop with output `p + Mr`, `M ∈ O_B`, `B < 1 − ε·vol`. Let `N_c⁺` be
its number of seed-based operations with `η > 0`. Then

> `N_c⁺ ≥ ln( (1−B)/(ε·vol) ) / ( −ln(1 − κ₊) )`,  `κ₊ = 4α/(1+α)²`,
> and `W ≥ m·N_c⁺`.

*Proof.* `Ψ(0)=1`. By Lemma 2.3, `Ψ(t+1) ≥ (1−κ₊)Ψ(t)` at every op and
`Ψ` is non-decreasing except at the `N_c⁺` positive seed ops, so
`Ψ(T) ≥ (1−κ₊)^{N_c⁺}`. At stopping, `Ψ(T) = Σ_u φ_u r_u ≤ ‖φ‖_∞‖r‖₁ =
‖r‖₁` (on the star `‖φ‖_∞ = φ_c = 1`, since `φ_l = c_a < 1`), and Lemma 1.1
gives `‖r‖₁ ≤ ε·vol/(1−B)`. Combine and take logs. Each seed op is charged
`d_c = m`. ∎

**Corollary 2.5 (explicit constants).** With `B = 0` (output `p`), `ε·vol ≤
1/4`:
`N_c⁺ ≥ ln4/(−ln(1−κ₊)) ≥ ln(4)(1−κ₊)(1+α)²/(4α)` and
`W ≥ m·ln4/(−ln(1−κ₊))`. Writing `c := W·α·ε` and taking `1/(8ε)` integral
(so `mε = 1/8` exactly, as on the whole dyadic test grid), this is
`c ≥ 0.0424` (α=1/4), `0.0433` (α ≤ 1/16), against iteration 1's proved
`3/256 = 0.0117` — a **3.7× stronger constant**, and exactly 2× below the
measured member frontier `0.0867`. For general `ε ≤ 1/16` the floor costs a
factor 2 (`m ≥ 1/(16ε)`), giving the closed form
`W ≥ ln(4)(1+α)²(1−κ₊)/(64·αε) ≥ 0.0216/(αε)` for `α ≤ 1/16`.

**What this buys.** (i) Gap G2 is closed: the direction of the step is not
load-bearing; anti-pushes buy nothing, because `Ψ` simply *rises* under them
and every unit of rise must be paid back by seed pushes at the same
multiplicative rate. (ii) The proof no longer uses the leaf-flow ledger, the
`‖r‖₁ ≤ 1` cap, or the `η ≤ 2/(1+α)` per-op cap — the three star-specific,
monotone-specific steps of iteration 1. (iii) Lemma 2.2 holds for *any*
invariant-preserving update, so multi-base and batched operations are covered
without a characterization lemma.

**Verification (Measured).**
* `member_check.py`: 600 runs, 14 member policies × 2 stopping rules ×
  {α=1/4,1/16,1/64} × {ε=2⁻⁵..2⁻⁹} × 3 seeds. **0 assertion failures** of
  `W ≥ m·N_c⁺(LB)` and `N_c⁺ ≥ LB`. Tightest members (`nonlazy`,
  `greedy_nonlazy`, `cheap_first`, `jacobi_nonlazy`) sit at
  **`N_c⁺/LB = 1.015–1.022`** and `W/LB = 2.000` — the centre-op count bound
  is tight to 1.5 %, and the residual 2× is the `⌊1/(8ε)⌋` vs `1/(8ε)` slack
  plus leaf work.
* `potential.py` P4: the crafted signed-η pump adversary (pump `‖r‖₁` to
  `K ∈ {1,4,16}` by leaf-antis + centre-anti, then solve) at
  α ∈ {1/4,1/16,1/64,2⁻⁸}, ε ∈ {2⁻⁷,2⁻⁹}: guarantee met, `r ≥ 0` throughout,
  and `N_c⁺ ≥ LB` on all 24 cells. Pumping to `K=16` *raises* `N_c⁺` from 134
  to 312 and `W` from 4272 to 15664 (α=2⁻⁸, ε=2⁻⁷) — 3.7× worse, as measured
  in iteration 1, now with a proof of why it cannot help.

**Proposition 2.6 (general graphs; Proved-draft, instance-dependent
constants).** Nothing above used the star except the two numbers `π_c` and
`‖φ‖_∞`. For any connected `G`, seed `c`:

> `N_c⁺ ≥ ln( (1−B) / (Φ·ε·vol) ) / (−ln(1−κ))`,  `W ≥ d_c·N_c⁺`,
> `κ = 2α/((1+α)π_c)`, `Φ = max_u pr(e_u)_c/π_c = max_u d_uπ_u/(d_cπ_c)`.

Asymptotically `W = Ω( d_c·π_c·ln(1/(Φ ε vol)) / α )`. The star is the
extremal case `d_c = m`, `π_c = (1+α)/2`, `Φ = 1`. *(Measured: `Φ = 1` — i.e.
`‖φ‖_∞ = φ_c` — on all 10 zoo graphs × 3 α tested. Whether `Φ = 1` holds
whenever the seed maximizes `d_uπ_u` is **Open**; it can fail in principle
when a high-degree non-seed vertex dominates.)* This retires the
star-specific Lemma 4 of iteration 1; what remains star-specific is only the
star-closure Lemma 1′ (multi-base ops when axiom (A4) is dropped).

---

## 3. T3 — the signed-relaxation upper bound on the star

**Setup.** `t := √α`, `λ := (1−t)/(1+t)`, `ω⋆ := 1+λ²`. Identities (direct
computation, matching the manuscript's `eq:cf-opt-sor-identities`):
`c_a ω⋆ = 2λ`, `1 − ω⋆ = −λ²`, and `ω⋆ = 2/(1+√(1−c_a²))` (the SOR optimum).
On `K_{1,m}` seeded at the centre, symmetry keeps all leaves equal; write the
state `(R, S) = (r_c, per-leaf residual)`. SOR steps are `gp(u, ω⋆·2r_u/(1+α))`:

* **centre block** (1 op, work `m`): `R ← −λ²R`; `S += 2λR/m`.
* **leaf block** (`m` ops, work `m`): `S ← −λ²S`; `R += 2λ·(mS)`.

**Lemma 3.1 (exact block recurrence; Proved-draft).** Let `x_j` be the
aggregate residual processed in block `j` (`x_j = R` for a centre block,
`x_j = mS` for a leaf block), `x_0 = 1`. Then
`x_1 = 2λx_0`, `x_{j+1} = 2λx_j − λ²x_{j−1}`, and hence — the characteristic
polynomial being `(z−λ)²` —

> `x_j = (j+1)λ^j`.

*Proof.* Both block types have the same two-line action; after block `j` the
just-processed layer holds `−λ²x_j` and the other layer holds
`−λ²x_{j−1} + 2λx_j`, which is `x_{j+1}` by definition. ∎
*(Verified: max relative deviation from `(j+1)λ^j` over 40 blocks is
1.4e-13…2.7e-15 for α ∈ {1/4, 1/16, 1/64, 2⁻⁸, 2⁻¹²} and m ∈ {8, 64, 512};
the recurrence is m-free. Symmetric reduction reproduces the full
n-dimensional simulator to 2.1e-14 — `sor_star.py` T3.a, T3.c.)*

**Lemma 3.2 (stopping test).** At the boundary of block `j` the
degree-normalized residual is `max_u |r_u|/d_u = x_j/m`: the centre carries
`x_j` with `d_c=m`, the leaves carry `λ²x_{j−1}` spread over `m` leaves with
`d_l=1`, and `λ²x_{j−1} = jλ^{j+1} < (j+1)λ^j = x_j`. By F5 + F4,
`err(p) = max_u pr(r)_u/d_u ≤ max_u |r_u|/d_u`, so the guarantee holds once
`x_j ≤ ε m`. ∎

**Theorem 3.3 (star upper bound for SOR(ω⋆); Proved-draft).** For `εm < 1`,

> `W_SOR ≤ m · ⌈ (1/√α)·ln( 2 / (√α·ε·m) ) ⌉
>        = O( m·( log(1/(εm)) + log(1/α) ) / √α )`.

*Proof.* `−lnλ = 2·arctanh(t) ≥ 2t`, so `λ^j ≤ e^{−2tj}`; and
`j+1 ≤ (2/t)e^{tj/2}` (since `e^x ≥ 1+x` gives `(2/t)e^{tj/2} ≥ 2/t + j`).
Hence `x_j ≤ (2/t)e^{−3tj/2} ≤ (2/t)e^{−tj}`, which is `≤ εm` as soon as
`j ≥ (1/t)·ln(2/(t·ε·m))`. Each block costs `m` (Lemma 3.2). ∎

With `m = ⌊1/(8ε)⌋` this reads **`W_SOR = O( log(1/α)/(√α·ε) )`**, matching
the manuscript's Θ(log(1/α)/(√α ε_ppr)) star *lower* bound for this method
(`subsec:cf-star-lower`) — so the star cost of SOR(ω⋆) is now pinned from
both sides.

**Verification (Measured, `sor_star.py` T3.b).** 18 cells,
α ∈ {1/4,1/16,1/64,2⁻⁸,2⁻¹⁰,2⁻¹²} × ε ∈ {2⁻⁷,2⁻⁹,2⁻¹¹}, `m = ⌊1/(8ε)⌋`:
`W_actual / W_bound = 0.529–0.571` on every cell (bound valid everywhere,
loose by ≤ 1.9×). Constants: `W·√α·ε / (log(1/α)+log(1/(εm)))` = 0.0721,
0.0580, 0.0526, 0.0492, 0.0473, 0.0457 as α decreases — flat in ε, drifting
slowly in α, consistent with the Θ law. The stronger oracle stop
(`err(p) ≤ ε` directly, rather than via the residual) costs 0.36–0.75× of
`W_actual`.

---

## 4. T4 — the separation

**Corollary 4.1 (Proved-draft).** Fix `ε ≤ 1/16`, `α ∈ (0,1)`, and take the
centre-seeded star `K_{1,m}` with `m = ⌊1/(8ε)⌋` (so `ε·vol ≤ 1/4`). Then on
this single instance:

* **(lower)** every method in **M±** — hence every method in **M₊** — whose
  output lies in `O_B` with `B ≤ 1/2` satisfies
  `W ≥ m·ln(2)/(−ln(1−4α/(1+α)²)) = Ω(1/(αε))`,
  with explicit constant `W·αε ≥ 0.0217` when `1/(8ε)` is integral
  (`≥ 0.0106` for general `ε ≤ 1/16`), and 2× those for `B = 0`;
* **(upper)** the method SOR(ω⋆) ∈ **R±**, output `p` (i.e. `B = 0`),
  satisfies `W ≤ m·⌈(1/√α)ln(2/(√α εm))⌉ = O(log(1/α)/(√α ε))`.

The ratio is `Ω( 1/(√α·log(1/α)) )`. Both classes use the identical
primitive `gp(u,η)`, the identical work charge `d_u`, the identical output
map `p`, and the identical instance; **the only difference between them is
the axiom `r ≥ 0`.**

**Measured (`sor_star.py` T3.d), ε = 2⁻⁹, m = 64:**

| α | LB (M±, W) | UB (SOR(ω⋆), W) | ratio | `1/(√α ln(1/α))` |
|---|---|---|---|---|
| 1/4 | 86.8 | 256 | 0.34 | 1.44 |
| 1/16 | 354.4 | 576 | 0.62 | 1.44 |
| 1/64 | 1419.4 | 1344 | 1.06 | 1.92 |
| 2⁻⁸ | 5678.2 | 3072 | 1.85 | 2.89 |
| 2⁻¹⁰ | 22713.0 | 6976 | 3.26 | 4.62 |
| 2⁻¹² | 90852.2 | 15552 | 5.84 | 7.69 |

The crossover is at α ≈ 1/64 and the gap tracks `1/(√α log(1/α))` from there
down. What SOR spends to buy it, measured on the same runs: `min_t min_u r_u
= −1.11` (α=1/64) and `−2.57` (α=2⁻⁸), `max_t ‖r‖₁ = 2.98` and `5.90`. Both
are exactly the two quantities Theorem 2.4 forbids: `Ψ ≥ 0` fails the moment
`r` does, and with it the multiplicative-decrease argument.

**Corollary 4.2 (the axiom is exactly located).** Combining §2 and §3, on the
centre-seeded star:
`M₊ = Θ(1/(αε))`, `M± = Θ(1/(αε))`, `R± = Õ(1/(√α ε))`.
Iteration 1's conjecture that "monotonicity is the anti-acceleration axiom"
is confirmed and sharpened: it is **residual** nonnegativity, not step
positivity. Signed step amounts are a red herring.

---

## 5. Status summary

| # | statement | status |
|---|---|---|
| T1 | Lemma 1.1 mass-deficit; Lemma 1.2 transport characterization; Prop 1.3 sharp threshold `B = 1−ε·vol` | **Proved-draft**, LP-confirmed to 4 decimals |
| T1′ | *second instance defeats `B=1`* (the planned strengthening) | **False as posed** — disproved for every radius-1 instance (Lemma 1.2 + LP) |
| T2 | Lemmas 2.2/2.3, Theorem 2.4: M± obeys `W = Ω(1/(αε))` | **Proved-draft**, 600 runs + pump adversary, 0 failures |
| T2′ | Prop 2.6 general-graph version | **Proved-draft** modulo the instance constant `Φ` (`Φ=1` Measured on 10 graphs, **Open** in general) |
| T3 | Lemma 3.1 exact recurrence; Theorem 3.3 `O(m(log(1/ε)+log(1/α))/√α)` | **Proved-draft**, verified on 18 cells (≤1.9× loose) |
| T4 | Corollary 4.1 separation `Ω(1/(√α log(1/α)))` on one instance | **Proved-draft**, both sides measured |

## 6. Remaining gaps

1. **`Φ = 1` in Prop 2.6** is verified, not proved; a high-degree non-seed
   vertex could in principle make `‖φ‖_∞ > φ_c`, weakening the general bound
   by a `log Φ` additive term. Cheap to fix or to bound crudely.
2. **Multi-base / batched ops on general graphs when axiom (A4) is dropped**:
   Lemma 2.2 covers any invariant-preserving update, but "one-hop" then needs
   a definition on graphs of girth > 4 — the star-closure Lemma 1′ of
   iteration 1 is still the only classification. Unchanged from G3.
3. **`R±` has no matching class lower bound.** Theorem 3.3 is an upper bound
   for one method. Whether *every* signed-residual one-hop method needs
   Ω(1/(√α ε)) — the natural companion theorem, and what would make the
   separation two-sided — is **Open**. (The manuscript's long-spider result
   shows the *fixed*-ω⋆ FIFO method is not graph-uniformly `Õ(1/(√α ε))`.)
4. **Constants**: Theorem 2.4 is tight to 1.5 % in `N_c⁺` but 2× in `W`
   (leaf work is not counted at all); Theorem 3.3 is 1.9× loose.
5. `err` is one-sided (`π − out ≤ εd`). SOR's `p` can overshoot; under a
   two-sided `|π − out| ≤ εd` requirement the T3 constant changes (the
   residual-based stop already certifies the two-sided version via F5, so
   the bound stands, but this was not swept).

## 7. Next target

The companion lower bound for `R±` (gap 3): show that any one-hop
invariant-exact method with *signed* residual needs `Ω(vol_ε/√α)` on the
star, e.g. by replacing `Ψ ≥ 0` with a quadratic energy
`Φ(e) = ½eᵀD⁻¹He` (the manuscript's `eq:cf-energy`) and pricing one-hop
coordinate updates against its `ω(2−ω) = Θ(√α)` damping. That would convert
Corollary 4.1 from *one method beats the class* into *class beats class*.
