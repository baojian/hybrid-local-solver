# I2-A — Attacking carry-mode growing-support APCG

**VERDICT: MIXED.** Carry mode **survives on the α-exponent** (the thing iteration 1
claimed): vol-normalized exponents **0.44–0.51** on every path-like, two-scale and
K8-embedded family, versus 0.64–0.67 for restart. It is **BROKEN on spurious volume**:
a marginal-hub ring drives `spur_vol / vol(S*)` to **Θ(hub_deg)** — measured 7.5×, 15×,
28×, 50×, 99×, 192× as `hub_deg` runs 12→384 — i.e. **ω(vol(S*))**, which is the stated
kill criterion. Gate hysteresis at 4× does *not* remove the ω (ratio still linear in
hub_deg: 0.79→6.39); 8× does empirically, but no fixed multiplier is provably safe.

A third, **carry-independent** break surfaced: on the ring, even with **zero** spurious
admissions (gate 8×), **87% of all charged work is the boundary gate scan**, because
`vol(∂S*) = 16·vol(S*)`. The safe-gate framework itself — not momentum — costs
`Θ(vol(∂S*)·α^{-1/2})`.

The positive half is strengthened: a **one-insertion damage bound**
`√Λ⁺ ≤ √Λ⁻ + √(2 D_t)` (Proved-draft, graph-uniform) that telescopes to an **additive
`log(1+T)`** inside the logarithm — explaining why carry keeps the exponent and restart
does not.

Code: `w3_apcg/{fam_attack,grow2,run_attack,run_ring}.py`; data
`w3_apcg/results_{attack,ring,mitig2}.json`; logs `w3_apcg/{attack_bcd,ring_ab,ring_mitig}.log`.
Compute ≈ 50 s solver time (≈ 35 min wall incl. analysis).

---

## 0. Two bugs found in the inherited harness (both fixed)

1. `grow2.apcg_grow2`, hysteresis path: `adm = sorted(pending)` unconditionally
   overwrote the strict-sweep admission list with the (empty) pending set, so any run
   with `gate_mult > 1` **looped forever** admitting nothing. Fixed by merging the sweep
   result into `pending`. This branch had never been executed before.
2. `solvers.exact_support_solver`: the interior-residual assertion
   `resid_in < 1e-6·α·ρ` has no absolute floor and fires on true-zero residuals
   (1.4e-18) once ρ ≲ 1e-8, which the ρ-bisection reaches. Floored with `+1e-15`.
   No effect on any iteration-1 result (all used ρ ≥ 2.5e-4).

New in `grow2.py`: `Restricted2.confirm` (deferred re-confirmation of a candidate at the
current iterate, charged `d_j`) and the `recheck` admission mode.

---

## 1. Family definitions

All in `w3_apcg/fam_attack.py`. α ∈ {2⁻⁶, 2⁻⁸, 2⁻¹⁰, 2⁻¹²}, 5 seeds for carry and the
fixed-support reference, 3 for restart; medians reported, spurious/missed as the max over
seeds. Stop rule and charging model unchanged from W3 (`h ≤ 0.1·αρ`, `d_i` per sampled
coordinate, `d_j` per boundary gate test, `vol(S)+n` per periodic check).

* **(a) `ring_star(m, hub_deg)` — marginal-hub ring.** Star core: seed = center 0
  (degree *m*), core leaves 1..*m* (degree 2), each carrying a pendant **hub** of degree
  `hub_deg` with `hub_deg−1` dead leaves. By symmetry every hub has the *same* KKT ratio
  `rel_j = −grad_j(x*)/λ_j`, and exactly `rel_j ∝ 1/d_j`, so one ρ tunes the entire ring
  to the activation breakpoint at once. ρ is bisected per α to put every hub just
  **below** activation (`rel = 0.983`, and a `ring_edge` variant at `rel = 0.9995`).
  `S* = {center} ∪ leaves`, constant in α ⇒ raw exponent = vol-normalized exponent.
  vol(S*) = 3m = 180; if all hubs leak, spurious volume = m·hub_deg.
* **(a′) `ring_graded(m, dmin, dmax)`.** Same core, hub degrees geometrically spaced
  8→512, so `rel_j` is graded over a 64× range inside a single graph. Reading off the
  smallest `rel_j` that still gets admitted measures the **momentum overshoot
  threshold τ(α)** directly.
* **(b) staircase** — `zoo.path(3000)`, endpoint seed, ρ = 1/12000. Admissions occur one
  at a time (measured 31/58/106/192 events at the four α), the Θ(|S*|)-admissions case.
* **(c) lollipop** — `K₁₆` head + 360-node path tail, seed *inside* the clique (node 1,
  not the junction), ρ = 1/4000. Dense head, long sparse tail.
* **(d) k8emb** — the Round-026 **K₈ pulse** seed distribution
  (`s₀ = 363437/651088`, `sᵢ = 41093/651088`) on `K₈` with a 260-node path tail attached
  at node 0, ρ = 1/2000. *Caveat:* attaching the tail raises `d₀` from 7 to 8, so this is
  the pulse construction perturbed, not bit-exact; the w7 exact harmful mode is not
  reproduced verbatim.

---

## 2. Results: the three benign families survive (Measured)

Vol-normalized exponents `p` in `W/vol(S*) ~ α^{-p}`, 4 points; `spur` = max over seeds
of `spur_vol / vol(S*)`; missed nodes and final semantic error `‖D^{-1/2}(x−x*)‖_∞`
(target `≤ 0.1ρ`).

| family | vol(S*) @2⁻⁶→2⁻¹² | **carry p** | restart p | fixed-ref p | carry spur | missed | err ok |
|---|---|---|---|---|---|---|---|
| staircase | 63 → 379 | **0.508** | 0.656 | 0.489 | 0.07 | 0 | ✓ |
| lollipop | 267 → 449 | **0.510** | 0.672 | 0.531 | 0.01 | 0 (1 restart run) | ✓ |
| k8emb | 89 → 279 | **0.451** | 0.636 | 0.488 | 0.02 | 0 | ✓ |
| ring (D=48) | 180 (const) | 0.236 | 0.180 | 0.181 | **31.67** | 0 | ✓ |
| ring_edge | 180 (const) | 0.239 | 0.110 | 0.181 | **31.67** | 0 | ✓ |
| ring_graded | 120 (const) | −0.084 | — | — | 1.18 | 0 | ✓ |

Carry work ratios vs the fixed-support reference are ≤ 1.0 on staircase (0.70–0.77),
≈ 1.0 on lollipop, 0.73–0.91 on k8emb — carry is *cheaper* than knowing S* offline,
because early segments run on a small S. Restart is 1.4–3.0× the reference and rising
with α⁻¹, reproducing iteration 1.

**The K8 pulse does not reappear.** k8emb carry is 0.451 with ≤ 2 spurious nodes at every
α; the deterministic harmful mode stays invisible to the randomized method even when the
support has to grow *through* the K₈ head. (Evidence: Measured. Caveat above on `d₀`.)

**Staircase does not drift toward exponent 1.** 192 carried-momentum admissions at 2⁻¹²
give p = 0.508, indistinguishable from the fixed-support 0.489. Θ(|S*|) insertions are
free at the exponent level.

**Honest negative on the stop rule (both variants):** two runs (lollipop 2⁻¹², restart and
gate-4 carry) ended with `missed = 1` — a true-support node of negligible mass never
admitted because `h ≤ 0.1αρ` fired first. Semantic error was still 2–4e-6 ≪ 0.1ρ = 2.5e-5,
so this is a stop-rule artifact, not a correctness failure, but "missed = 0 always" is
**false** as stated in iteration 1.

---

## 3. The ring breaks it (Measured)

### 3.1 Spurious volume is ω(vol(S*))

α = 2⁻¹⁰, m = 60, vol(S*) = 180, gate multiplier 1 (the safe gate):

| hub_deg | spur nodes | spur_vol | **spur_vol/vol(S*)** | W/W_fixed |
|---|---|---|---|---|
| 12 | 687 | 1347 | 7.48 | 7.6× |
| 24 | 1325 | 2705 | 15.03 | 12.8× |
| 48 | 2175 | 4995 | 27.75 | 25.6× |
| 96 | 3385 | 9085 | 50.47 | 64.1× |
| 192 | 6363 | 17823 | 99.02 | 125.6× |
| 384 | 11550 | 34530 | **191.83** | 231.2× |

Ratio ≈ `0.52·hub_deg`, unbounded in the family parameter, and the charged work tracks it.
At α ∈ {2⁻⁸, 2⁻¹⁰, 2⁻¹²} with hub_deg = 48 the run admits **all 60 hubs and all 2820 of
their dead leaves** (spur = 2880 nodes, 5700 volume = 31.67× vol(S*)). Every run still
finishes with `missed = 0` and correct semantic error — S ⊇ S* keeps the restricted
solution equal to x* — so this is a pure **work / locality** failure, not a correctness one.

Restart is hurt too, contradicting iteration 1's "restart admitted zero spurious nodes":
30–107 spurious nodes, 8–16× vol(S*). The ring defeats the safe gate for *both* variants;
carry is 2–4× worse.

### 3.2 Mechanism: momentum inflates the gate by a constant, not by a function of α

The graded ring reads off the smallest true KKT ratio that still gets admitted:

| α | τ = min admitted `rel` | spur/vol |
|---|---|---|
| 2⁻⁶ | 0.417 | 0.48 |
| 2⁻⁸ | 0.344 | 0.78 |
| 2⁻¹⁰ | 0.344 | 1.01 |
| 2⁻¹² | 0.344 | 1.18 |

τ is **α-independent**: the carried iterate transiently overshoots `x*_S` by a factor
`O ≈ 1/τ ≈ 2.9`, so the *effective* admission threshold is `τ·λ_j`, not `λ_j`. This is
exactly why the exponent survives and the constant does not:

* spurious volume = vol of the **τ-marginal shell** `{j ∉ S* : −grad_j(x*) ≥ τ·λ_j}`,
  which is a *geometric* property of the instance and is O(vol(S*)) on paths/trees
  (where `rel` decays only ~2% per hop, so the shell is a few nodes) but **Θ(m·hub_deg)**
  on the ring;
* it does **not** grow as α → 0, so `W ~ C(graph)·vol(S*)·α^{-1/2}` with a broken
  constant, not a broken exponent.

Measured overshoot is family-dependent: τ ≈ 0.34 on the star-core ring (large early
ramp transient after a burst admission of the whole leaf layer), τ ≈ 0.86 on paths
(admissions happen deep in the linear regime, where overshoot is ~16%).

### 3.3 A carry-independent break: the gate's own cost

Ring, hub_deg = 48, α = 2⁻¹⁰, `vol(S*) = 180`, `vol(∂S*) = 2880 = 16·vol(S*)`:

| gate mult | W | W_boundary | boundary share | spur_vol |
|---|---|---|---|---|
| 1 | 7.05e5 | 4.98e4 | 7% | 4995 |
| 4 | 2.39e5 | 1.96e5 | 82% | 95 |
| 8 | 1.62e5 | 1.41e5 | **87%** | **0** |

With the gate perfectly tuned and **zero** spurious admissions, 87% of the work is
re-scanning the boundary: the gate is evaluated every `n` iterations at cost `vol(∂S)`,
so the framework pays `Θ(vol(∂S*)·α^{-1/2}·log)` no matter what the optimizer does.
`vol(∂S*) = O(vol(S*))` is **not** a graph-uniform hypothesis — the ring makes it
`Θ(hub_deg)`. Any end-to-end `Õ(vol(S*)/√α)` claim needs this separately.

---

## 4. Mitigations (Measured)

Ring, m = 60, hub_deg = 48, 5 seeds, all four α. "batch" = deferred confirmation: a
candidate is parked, the run continues with it excluded for `⌈α^{-1/2}⌉` iterations, and
it is admitted only if it **still** violates the gate at re-test (`Restricted2.confirm`,
charged `d_j`). A final strict (multiplier-1) sweep at convergence guarantees no misses.

| mitigation | max spur/vol(S*) | W/W_fixed range | carry p | missed |
|---|---|---|---|---|
| none | 31.67 | 22–30× | 0.236 | 0 |
| hysteresis 2× | 23.57 | 8.0–15.2× | 0.324 | 0 |
| **hysteresis 4×** | **0.79** | 5.9–7.8× | 0.123 | 0 |
| hysteresis 8× | 0.53 | 6.5× | — | 0 |
| batching (α^{-1/2}) | 25.92 | 17.8–25.5× | 0.237 | 0 |
| hysteresis 2× + batching | 6.38 | 7.3–10.1× | 0.250 | 0 |

* **Batching alone fails.** The overshoot persists for far longer than `α^{-1/2}`
  iterations, so the candidate re-confirms. It is also *expensive* on benign families
  (14× on `path(400)`, because each deferral forces a full convergence on the smaller
  support before the candidate can be admitted).
* **Hysteresis 4× works at fixed hub_deg but does not remove the ω.** Re-running the
  hub-degree sweep under gate 4× gives spur/vol = 0.79, 1.59, 3.19, **6.39** for
  hub_deg = 48, 96, 192, 384 — still exactly linear. One or two hubs always leak (the
  overshoot factor has a tail over the ~`K/n` gate evaluations), and *one* leaked hub
  already costs `hub_deg/(3m)·vol(S*)`. Gate 8× gives 0, 0.53, 0, 0 — bounded here,
  but this is a race between a fixed multiplier and the max of the overshoot over all
  checks, so it is not a guarantee.
* **Hysteresis 4× is free on the benign families**: carry p = 0.450 (staircase), 0.455
  (lollipop), 0.442 (k8emb), spur ≤ 0.05, missed 0 (one lollipop stop-rule miss as in §2).
  So 4× hysteresis is a strictly good default — it just does not repair the ring.

**Kill criterion assessment.** No family forced exponent ≥ 0.75 (max vol-normalized
carry exponent observed: 0.510). The ring **does** force spurious volume ω(vol(S*)) and
**survives both mitigations** in the ω sense. Direction I2-A is therefore *not* killed on
its acceleration claim but *is* killed on the unconditional locality claim.

---

## 5. Theory

### 5.1 Estimate sequence on a fixed support (Proved-draft)

`F_S = f_S + Ψ_S`, `f_S(x) = ½xᵀQ_SS x − b_Sᵀx`, `Ψ_S(x) = Σ_{i∈S} λ_i|x_i|`,
`λ_i = αρ√d_i`. All coordinate Lipschitz constants are equal, `L_i = Q_ii = c = (1+α)/2`,
so uniform sampling is the optimal APCG sampling and `‖·‖_L = √c ‖·‖₂`. Since
`Q ⪰ αI` and `Q_SS` is a principal submatrix, `f_S` is `σ`-strongly convex in `‖·‖_L`
with `σ = α/c = 2α/(1+α)` — **a priori, graph-uniform, no eigensolve**.

Constant-parameter APCG (LLX 2014): `n = |S|`, `a = √σ/n`, `y = (x+az)/(1+a)`,
`ẑ = (z+ax)/(1+a)`, `z⁺ = ẑ + Δ e_i` with `Δ` from the coordinate prox at `y`, and
`x⁺ = y + naΔ e_i` (the simplification of the paper's step 4, verified exact in W3).
Lyapunov / estimate-sequence value

> `Λ_S(x,z) = [F_S(x) − F*_S] + (σc/2)·‖z − x*_S‖₂² = [F_S(x) − F*_S] + (α/2)‖z − x*_S‖₂²`

(the `σc/2` collapses to `α/2` for this `σ`, `c`). The estimate-sequence argument gives the
**one-step, history-free** contraction

> **(H3)**  `E_i[ Λ_S(x⁺,z⁺) ] ≤ (1 − a)·Λ_S(x,z)` for **every** state `(x,z) ∈ R^S×R^S`.

Iterating from `x₀=z₀=0` and charging `E[d_i] = vol(S)/n` per iteration reproduces the W3
measurement `W = O(vol(S)·α^{-1/2}·log(Λ₀/ε))`, constant ≈ 15 at δ = 0.1.

**(H3) verified numerically** (`grow2.onestep_expectation`, exact expectation over the
uniform sample, paper-form unsimplified step, exact restricted optimum): path(120),
star(40), caterpillar(60,1), ring_star(8,6) × α ∈ {2⁻⁴,2⁻⁸,2⁻¹²} × 7 state types
including `x = z = 0`, **post-insertion states** (one coordinate zeroed), large-momentum
states (`z = x* − 5(x − x*)`), and infeasible negative-`x` states. The contraction held in
every case with **strictly positive slack**; worst observed slack `(1−a) − E[Λ⁺]/Λ =
+5.1e-5`. This is the crucial point: **(H3) references no invariant of the trajectory**,
so a carried state that arrives from a *different* support is still a legal starting state.

### 5.2 What actually breaks on insertion

At an admission `S → S⁺ = S ∪ {j}` the algorithm appends `x_j = z_j = 0` and keeps
`(p, M, φ)`. Three things move underneath the estimate function:

1. `n → n+1`, so `a = √σ/n` shrinks. Harmless and monotone: the final `n = |S_fin|`
   already appears in the bound.
2. **The reference value drops**: `F*_S → F*_{S⁺}`, so the gap term of `Λ` jumps *up* by
   `D_t := F*_{S_t} − F*_{S_t⁺} ≥ 0` with the iterate unchanged.
3. **The center moves**: `x*_S ⊕ 0 → x*_{S⁺}`, so the quadratic term is measured from a
   different point. Write `w_t := x*_{S⁺} − (x*_S ⊕ 0)` and `u := (z⊕0) − (x*_S⊕0)`.

Neither (2) nor (3) is covered by any fixed-support estimate sequence — this is exactly
the gap iteration 1 flagged as Open.

### 5.3 One-insertion damage bound (Proved-draft, graph-uniform)

`Λ⁺ − Λ⁻ = D_t + (α/2)(‖u − w_t‖² − ‖u‖²) = D_t + (α/2)‖w_t‖² − α⟨u, w_t⟩`.

*Step 1 (the moved center is paid for by the released value).* `x*_S ⊕ 0` is feasible for
the `S⁺` problem with `F_{S⁺}(x*_S⊕0) = F*_S`, and `F_{S⁺}` is `α`-strongly convex with
minimizer `x*_{S⁺}`, so

> `D_t = F_{S⁺}(x*_S⊕0) − F_{S⁺}(x*_{S⁺}) ≥ (α/2)‖w_t‖²`.

*Step 2 (cross term by Cauchy–Schwarz against the two halves of `Λ`).* Using
`(α/2)‖u‖² ≤ Λ⁻` and Step 1,
`α|⟨u,w_t⟩| ≤ 2·√((α/2)‖u‖²)·√((α/2)‖w_t‖²) ≤ 2√(D_t·Λ⁻)`.

Hence `Λ⁺ ≤ Λ⁻ + 2D_t + 2√(D_t Λ⁻) ≤ (√Λ⁻ + √(2D_t))²`, i.e.

> ### `√(Λ⁺_t) ≤ √(Λ⁻_t) + √(2 D_t)`
>
> **Carrying momentum through one insertion costs an additive `√(2D_t)` in the `√Λ`
> metric**, where `D_t` is the drop in the restricted optimal value. No graph structure,
> no monotone cone, no sign condition on `w_t` is used — only `Q ⪰ αI`.

Note what the bound is *not* stated in: the admission slack at the iterate. The gate slack
governs *which* `j` is admitted (§3.2); once `j` is in, the damage is controlled by `D_t`
alone. A spurious admission has `D_t ≈ 0` and therefore does **negligible estimate-sequence
damage** — which is why the ring's failure shows up as volume, not as lost convergence.

**Measured check** (`grow2` diag mode, staircase, α = 2⁻¹⁰, 105 admissions, exact
restricted optima at every event): `Σ_t (Λ⁺−Λ⁻) = 8.17e-6` versus `Σ_t D_t = 1.42e-5`,
ratio **0.575 ≤ 2** as the bound requires; per-event `(Λ⁺−Λ⁻)/D_t ∈ [−0.40, 1.29]`;
104/105 jumps positive.

### 5.4 Summing over admissions (Proved-draft)

`Σ_t D_t = F*_{S₀} − F*_{S_fin}` telescopes, so with `G₀ := F(0) − F*_{S_fin}` we get
`Σ_t D_t ≤ G₀` and `Λ₀ ≤ 2G₀` (strong convexity at `x=z=0`). Discarding *all* contraction
between admissions (the adversary's best case: every admission adjacent) and applying
Cauchy–Schwarz over `T` events,

`√Λ_max ≤ √Λ₀ + Σ_t √(2D_t) ≤ √(2G₀) + √(2T·Σ_t D_t) ≤ √(2G₀)(1 + √T)`,

so `Λ_max ≤ 4G₀(1+T)`. Feeding that into (H3):

> ### Conditional Theorem (Proved-draft, modulo (H3))
> Growing-support APCG with the safe gate and **carried accumulators**, admitting `T`
> times and ending on support `S_fin ⊇ S*` with `n = |S_fin|`, reaches `E[Λ] ≤ ε` in
> expected charged work
>
> `W ≤ C · vol(S_fin) · α^{-1/2} · ( log(G₀/ε) + log(1+T) ) + N_chk · vol(∂S_fin)`,
>
> where `N_chk` is the number of gate sweeps (`= K/n` for the standard schedule).
> Since `T ≤ |S_fin|`, **carried-momentum insertion costs only an additive
> `log(1+|S_fin|)` inside the logarithm** — never a factor per admission.

This is the cleanest statement the algebra supports, and it predicts the measured
carry/restart split: restart replaces `z ← x`, which can *multiply* `Λ` by a constant at
each admission rather than adding `√(2D_t)` to `√Λ`, giving `Θ(T)` inside the log instead
of `log T`. Measured exponent gap 0.51 vs 0.65 is consistent in sign and rough size, but
the restart side is **Open** — I did not derive its lower bound.

### 5.5 Which hypotheses are graph-uniform

| ingredient | status | graph-uniform? |
|---|---|---|
| `σ = 2α/(1+α) ≤ λ_min(Q_SS)/c` | Proved (`Q ⪰ αI`, principal submatrix) | **yes** |
| `(α/2)‖w_t‖² ≤ D_t` (Step 1) | Proved | **yes** |
| damage bound `√Λ⁺ ≤ √Λ⁻ + √(2D_t)` | Proved-draft | **yes** |
| `Σ_t D_t ≤ G₀` (telescoping) | Proved | **yes** |
| **(H3)** one-step contraction from arbitrary `(x,z)` | Measured (12 cells × 7 state types, slack > 0); standard for constant-parameter APCG | **yes** if true — it is a property of the map, not the instance |
| **(G1)** `vol(S_fin) = O(vol(S*))` (bounded spurious volume) | **Refuted** — ring gives `Θ(hub_deg)` | **NO** |
| **(G2)** `vol(∂S*) = O(vol(S*))` (bounded boundary) | **Refuted** — ring gives `16×` at m=60, D=48, unbounded | **NO** |

So the obstruction to end-to-end `Õ(vol(S*)/α^{1/2})` is **not** momentum and **not** the
estimate sequence. It is the geometry of `S*`: both the τ-marginal shell (G1) and the
boundary volume (G2) can be arbitrarily fatter than `S*` itself, and (G2) binds even for an
oracle-perfect gate.

---

## 6. Honest gaps

* **(H3) is verified, not proved here.** I checked the expectation exactly on 12
  problem cells and 7 state families; I did not write out the LLX per-step inequality.
  Everything in §5.4 rests on it.
* **τ is measured, not bounded.** I have no bound on the overshoot factor `1/τ`, nor a
  proof that it is α-uniform (only four α, one graph family for the graded read-off).
  Without a bound on τ, no hysteresis multiplier is provably safe.
* **k8emb is a perturbed pulse** (`d₀ = 8` not 7); the bit-exact w7 harmful mode is not
  reproduced. The negative result "K8 mode does not reappear" is therefore about the
  perturbed construction.
* **The ring's exponent cell is uninformative** (`p ≈ 0.18–0.24` even for fixed support,
  because a 61-node star-like support has `λ_min(Q_SS) ≫ α` and converges far faster than
  the a-priori rate). The ring proves a volume statement, not an exponent statement; no
  family combining a fat boundary *with* an α-growing support was built. **Open.**
* `missed = 0` is **not** universal (§2): the `h ≤ 0.1αρ` stop rule can drop one
  negligible-mass true-support node. Semantic error was fine in all runs.
* Restart's exponent degradation has no matching lower-bound argument.
* Seeds: 5 (carry/fixed), 3 (restart, degree sweeps). Medians for work, max for
  spurious/missed. Concentration was not re-measured for the ring.

## 7. Attempted exponent kill — and why it failed (Measured, negative)

The natural follow-up is a family with **both** a fat τ-marginal shell **and** an α-growing
support: a path core with a hub at every other position, each hub's degree tuned so all of
them sit at the same `rel ≈ 0.94–0.97`. Since `rel_j ∝ 1/d_j` exactly, and the maximum
shell-admissible degree scales as `x*_k/(αρ) ∝ α^{-1}`, the shell volume would be
`Θ(α^{-1}) · Θ(α^{-1/2})` against `vol(S*) = Θ(α^{-1/2})`, predicting an exponent well
above 0.75. I built it twice (`w3_apcg/fam_grow_ring.py`) and **it does not exist in this
geometry**:

* Naive per-position rescaling oscillates: the tuned degrees are bimodal, 8–44 hubs land
  *inside* `S*` and the remainder collapse to `rel ≈ 0`.
* With damping (0.55) and an in-support push-out (×1.6) over 12 passes, the outcome is
  stable but degenerate: **≤ 4 hubs** in the shell at every α, median `rel` of the
  non-support hubs `≈ 0.00`, and shell/vol(S*) = 0.22–0.70 — flat in α.

The obstruction is structural and worth stating: on a path core a marginal hub sits exactly
at the threshold of absorbing enough mass to *enter* `S*`, and once it does it truncates the
diffusion downstream (measured: one entering hub pushed `|S*|` from ~130 to ~917 and drove
every later hub to `rel ≈ 0`). Path-like cores therefore self-limit the τ-shell to `O(1)`
hubs. The star core of §1(a) evades this only because its symmetry makes all hubs enter or
leave *together* — which is exactly why it produces a large but **α-independent** shell.

**Open:** is `vol(shell_τ(S*))/vol(S*)` growing in `α^{-1}` achievable at all, or is there a
theorem forcing it to be O(1)-in-α on every graph? A positive answer to the latter would
upgrade §5.4 to an unconditional `Õ(C(graph)·vol(S*)/√α)` with a graph constant, i.e. carry
mode would be exponent-safe *always* and only constant-unsafe. That is now the sharpest
question in this direction.

## 8. Next target

Two, in priority order:

1. **Settle the τ-shell scaling question above.** Either construct a fat shell on a
   non-path core (expander/grid cores do not have the truncation feedback that killed the
   path construction), or prove the shell is α-uniform. This decides whether I2-A's verdict
   is "exponent-safe, constant-broken" (current evidence) or "dead".
2. **Fix the boundary-scan cost (G2), which binds regardless.** The gate re-scans `∂S`
   every `n` iterations at cost `vol(∂S)` — 87% of the ring's work with a *perfect* gate.
   A lazy/priority-queue gate that maintains `−grad_j` incrementally for boundary nodes
   (updating only when a neighbour moves) would charge `d_j` per *change* rather than per
   *sweep*, and is the obvious way to make the framework's cost `Õ(vol(S*)/√α +
   vol(∂S*))` instead of `Õ((vol(S*) + vol(∂S*))/√α)`. This is a strictly separate and
   probably easier win than anything about momentum.
