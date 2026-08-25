# I4-C — The companion class lower bound for signed one-hop relaxation

**VERDICT: PROVED-draft, and the separation is now class-vs-class.**
Every member of the signed-relaxation class `R±` pays
`W = Ω(1/(√α·ε_ppr))` on the centre-seeded star `K_{1,m}`, `m = ⌊1/(8ε)⌋`.
The bound is **two-sided** — an explicit member matches it to a factor 3.5–4.0
uniformly over `α ∈ [2⁻¹⁴, 2⁻⁶] × ε ∈ [2⁻⁹, 2⁻⁵]` — and it is **not** produced
by the energy budget the plan proposed, which gives nothing here.

Three secondary results, each of independent value:

* **The manuscript's long spider is not a valid lower-bound instance for any
  semantically-stopped class**: `S_ε = ∅` there for `α ≤ 2⁻⁸`. `z = 0` is a
  correct answer at `W = 0`, so the `Ω(1/(αε))` CF-Push obstruction on it is a
  statement about the certificate, not about the problem. (Measured, §6.1.)
* **The `log(1/α)` in I2-D T3 is a stopping-rule artefact.** With the semantic
  (oracle) stop that `R±` actually requires, SOR(ω⋆) on the star is `Θ(1/√α)`
  blocks, not `Θ(log(1/α)/√α)`. This *strengthens* I2-D Corollary 4.1: the
  M±-vs-R± separation ratio is `Θ(1/√α)`, with no log. (Measured, §6.3.)
* **The class bound is not an information barrier.** On the very same star,
  eliminating the centre returns the exact answer in `O(m) = O(1/ε)` work.
  So `Ω(1/(√α ε))` is a property of *one-hop relaxation*, and I4-D's
  `O~(1/ε)` target survives untouched. (§7.)

Code: `/home/claude/work/overnight/i4c/{core.py, calib.py, verify.py,
sched2d.py, general.py, sweep.py, stops.py}`; logs/data in `i4c/out/`.
Total rerun ≈ 9 min. Conventions as I2-D / I4-D (push scale
`H π = γ_α e_v`, `H = I − c_α A D⁻¹`, `c_α=(1−α)/(1+α)`, `γ_α=2α/(1+α)`).

---

## 1. The class `R±`

**Definition 1.1.** A member of `R±` maintains `(z, r)` with
`z⁽⁰⁾ = 0`, `r = γ_α e_v − H z` (so `r⁽⁰⁾ = γ_α e_v`; **signed**, no
nonnegativity constraint). Its only primitive is a **one-hop relaxation**

> `relax(u, ω)`: `δ ← ω r_u`; `z_u += δ`; `r_u −= δ`; `r_w += c_α δ/d_u` for
> `w ~ u`. Charged work `d_u`.

`ω ∈ (0,2)` is arbitrary and may be **fixed, per-vertex, adaptive (any function
of the observed state), or randomized**. The policy choosing `(u_t, ω_t)` is
arbitrary. The output is `z` and must satisfy the semantic guarantee
`max_u |π_u − z_u|/d_u ≤ ε`. Work `W = Σ_t d_{u_t}`.

`R±` ⊋ `M±` ⊋ `M₊` (I2-D Def. 0.2): dropping `r ≥ 0` is exactly what admits
`ω > 1`. It contains GS (`ω=1`), damped Jacobi-as-relaxation, SOR(ω⋆), FIFO
CF-Push Phase II, Gauss–Southwell, and every variable-ω / Chebyshev-SOR hybrid.

Two exact facts hold for every member, every `ω ∈ (0,2)`, every path:

* **(E1) energy identity.** With `e = π − z` and `Φ(e) = ½ eᵀD⁻¹He`
  (`D⁻¹H` symmetric PD),
  `Φ(e) − Φ(e⁺) = [ω(2−ω)/2]·r_u²/d_u ≥ 0`.
  *(Verified to `1e-44` relative at 60 dps over 200 random signed ops,
  `general.py` E4.b; the `1e-2` float deviations in `verify.py` are
  cancellation in `Φ ≈ 3e-5`, not a failure.)*
* **(E2) `Φ` is a state function.** A burst of consecutive relaxations at one
  `u` dissipates exactly what the single relaxation with
  `ω_eff = 1 − Π_j(1−ω_j) ∈ (0,2)` dissipates, and displaces `z_u` by exactly
  the same amount. So **WLOG no two consecutive ops share a vertex**, and
  repeating at one vertex can never displace `z_u` by more than `2r_u`.

---

## 2. What the energy budget gives — and why it is not the proof

The plan's route was `#ops ≥ (energy to dissipate)/(max dissipation per op)`.
**On the star this route is vacuous, for two independent reasons.**

1. *Nothing must be dissipated.* `Φ_0 = γ_α π_c/(2d_c) = α/(2m)`, while the
   guarantee only forces `Φ_end ≤ (1+c_α)·ε²·vol/2 ≈ 1/(32m)`. For `α < 1/16`
   the permitted terminal energy **exceeds** `Φ_0`: an `R±` member may finish
   without dissipating anything at all.
2. *One op can dissipate everything.* The first relaxation at `v` dissipates
   `ω(2−ω)γ_α²/(2d_v)`, which is `ω(2−ω)·(γ_α/π_v)·Φ_0` — a constant fraction
   of `Φ_0` at `ω=1`. There is no "many small bites" structure.

And `ω(2−ω) ≤ 1` with equality at `ω=1`, so the damping factor cannot supply
`√α` by itself, exactly as the brief anticipated.

**The refined Cauchy–Schwarz version also fails.** Writing
`disp_j = ω_j r_v^{(j)}` and `η_j := ω_j/(2−ω_j)`, (E1) gives
`disp_j² = 2 d_v·diss_j·η_j`, so
`Σ_j|disp_j| ≤ √(Σ diss_j)·√(2d_v Σ η_j) ≤ √(γ_α π_v Σ_j η_j)`, hence

> `Σ_j η_j ≥ π_v/(4γ_α) = Θ(1/α)`  on the star.

At `ω_j = 1` (`η=1`) this reproduces the monotone `Θ(1/α)`; at `ω_j = ω⋆`
(`η ≈ 1/(2√α)`) it gives `Θ(1/√α)`. But `η` is **unbounded as `ω → 2`**, so
this bound alone permits `O(1)` seed ops. And `ω → 2` is not a strawman: it is
empirically the *best* schedule we found (§6.2). The proof therefore has to cap
the per-op displacement itself, not its energy price.

---

## 3. The proof: a fast-mode cap on the per-op displacement

Work in `y := D^{-1/2}e`, `H_sym := I − c_α D^{-1/2}AD^{-1/2}`, so
`Φ = ½ yᵀH_sym y` and a relaxation is the coordinate step
`y ← y − ω (H_sym y)_u ê_u`, `(H_sym y)_u = r_u/√d_u`. `H_sym` is PD with
spectrum in `[1−c_α, 1+c_α] = [2α/(1+α), 2/(1+α)]`.

**Lemma 3.1 (mode cap; Proved-draft).** Let `φ` be a unit eigenvector of
`H_sym` with eigenvalue `μ > 0` and `ŷ_φ := ⟨y, φ⟩`. Then at every time `t`
`½μ ŷ_φ² ≤ Φ_t ≤ Φ_0`, i.e. `|ŷ_φ| ≤ √(2Φ_0/μ)`.
*Proof.* `Φ = ½Σ_k μ_k ŷ_k²` with every `μ_k > 0`, and `Φ` is non-increasing
by (E1). ∎

**Lemma 3.2 (per-op displacement cap; Proved-draft).** A relaxation at `u`
changes `ŷ_φ` by `−ω(r_u/√d_u)φ(u)`. By Lemma 3.1 applied before and after,
`|Δŷ_φ| ≤ 2√(2Φ_0/μ)`, hence

> **`|Δz_u| = ω|r_u| ≤ (2/|φ(u)|)·√(2 d_u Φ_0/μ)`.**

Since `Φ_0 = γ_α π_v/(2 d_v)` exactly (from `e⁽⁰⁾ = π`, `r⁽⁰⁾ = γ_α e_v`),
this is a **closed-form, schedule-independent, pathwise** cap. ∎

**The star.** `K_{1,m}`, centre `c`, seed `c`. `H_sym`'s spectrum is
`{1−c_α, 1, …, 1, 1+c_α}` with `φ_∓ = (√m, ∓1, …, ∓1)/√(2m)`; the `m−1`
leaf-difference modes vanish at `c`. Take `φ = φ_-`, `μ = 1+c_α = 2/(1+α)`,
`φ_-(c) = 1/√2`, `d_c = m`, `π_c = (1+α)/2`, `Φ_0 = α/(2m)`:

> **`|Δz_c| ≤ 2√(α(1+α))` at every centre relaxation, for every `ω ∈ (0,2)`.**

Note what this says: the *fast* mode is the one that is nearly saturated at
`t=0` (`|ŷ_-⁽⁰⁾| = π_c(1−c_α)/√(2m)` is within `O(α)` of its cap), the centre
moves `ŷ_+` and `ŷ_-` by **equal magnitudes**, and so the slow mode — the one
carrying the answer — can only advance as fast as the fast mode is allowed to
oscillate. That is where `√α` comes from: the cap is `Θ(√α)`, while the
required travel is `Θ(1)`.

**Theorem 3.3 (class lower bound; Proved-draft).** Centre-seeded `K_{1,m}` with
`m = ⌊1/(8ε)⌋` (so `εm ≤ 1/8`). Every member of `R±` that stops with
`max_u |π_u − z_u|/d_u ≤ ε` performs

> `N_c ≥ (π_c − εm)/(2√(α(1+α))) ≥ 3/(16√(α(1+α)))`

relaxations at the centre, and since each is charged `d_c = m`,

> **`W ≥ m·N_c ≥ 3/(128·ε·√(α(1+α))) = Ω(1/(√α ε))`,  explicitly `W·√α·ε ≥ 3/128 = 0.0234`.**

*Proof.* `z_c⁽⁰⁾ = 0` and `z_c` changes only at centre relaxations, so
`Σ_{centre ops}|Δz_c| ≥ |z_c^{final}| ≥ π_c − ε d_c = π_c − εm ≥ 3/8`.
Divide by the Lemma-3.2 cap. ∎

The statement is **pathwise**, so randomized policies obey it with probability
1 (no success-probability caveat), and adaptivity, per-vertex `ω`, and
`ω`-bursts are all covered — bursts by (E2), which only *reduces* the op count.

**Proposition 3.4 (general graphs; Proved-draft).** For any connected `G` and
seed `v`, let `P_{≥μ₀}` be the spectral projector of `H_sym` onto eigenvalues
`≥ μ₀` and `κ_v := max_{μ₀} ‖P_{≥μ₀}ê_v‖·√μ₀`. Then

> `|Δz_v| ≤ 2√(γ_α π_v)/κ_v`,  `N_v ≥ (π_v − ε d_v)κ_v/(2√(γ_α π_v))`,
> `W ≥ d_v N_v`; and if `ε d_v ≤ π_v/2`, `N_v ≥ (κ_v/4)·√(π_v/γ_α)`.

So the instance parameter that decides the exponent is **`π_v/γ_α`**, the
seed's self-return amplification. Measured (`general.py` E4.a, 11 graphs):
`π_v/γ_α = (1+α)²/(4α) = Θ(1/α)` on the star (16.50 at `α=2⁻⁶`, 256.50 at
`α=2⁻¹⁰`) but only `Θ(1/√α)` on path / spider / caterpillar / tree / grid /
random-regular (4.06→16.26 on `path(40)`; `1/√α` = 8→32). **The star is the
extremal family precisely because its seed reflects mass back in one step.**
On 1-D-like families Prop 3.4 degrades to `Ω(α^{-1/4})` seed ops, which is
honest: those families do not force `1/√α` (§6.1, §7).

---

## 4. Matching upper bound: the bound is tight

**Theorem 4.1 (Measured, exact 2-dim reduction).** On the same instance, the
member "alternate a centre block with an all-leaves block, `ω → 2`" satisfies
`W ≤ 0.094/(√α ε)`, and SOR(ω⋆) satisfies `W ≤ 0.375/(√α ε)`, both with the
semantic stop. Hence on the centre-seeded star

> **`W_{R±} = Θ(1/(√α·ε))`, pinned from both sides, ratio 3.5–4.0.**

`sweep.py` E5, 15 cells, `α ∈ {2⁻⁶,2⁻⁸,2⁻¹⁰,2⁻¹²,2⁻¹⁴}`, `ε ∈ {2⁻⁵,2⁻⁷,2⁻⁹}`,
`m = ⌊1/(8ε)⌋`:

| α | `LB·√α·ε` | `W(ω⋆)·√α·ε` | `W(ω→2)·√α·ε` | UB/LB |
|---|---|---|---|---|
| 2⁻⁶ | 0.02374 | 0.1719 | 0.09375 | 3.95 |
| 2⁻⁸ | 0.02351 | 0.1719 | 0.08594 | 3.65 |
| 2⁻¹⁰ | 0.02346 | 0.1719 | 0.08594 | 3.66 |
| 2⁻¹² | 0.02344 | 0.1699 | 0.08398 | 3.58 |
| 2⁻¹⁴ | 0.02344 | 0.1689 | 0.08301 | 3.54 |

Every column is flat in `α` **and** in `ε` (all three `ε` values give identical
constants), which is the two-sided `Θ(1/(√α ε))` law.

---

## 5. The adversarial schedule search (no refutation found)

**5.1 Direct optimization over `ω`-schedules** (`sched2d.py` E2). The star's
symmetric dynamics reduce *exactly* to the 2-dim error map
`C(ω) = [[1−ω, ωc_α],[0,1]]`, `L(ω) = [[1,0],[ω c_α, 1−ω]]` on `(e_c, E_L)`
from `e⁽⁰⁾ = π_c(1, c_α)`, target `‖·‖_∞ ≤ εm = 1/8`. We minimized the block
count over `ω ∈ (0,2)^N` by warm-started L-BFGS (Chebyshev-SOR and `ω⋆` starts
plus 6 random restarts per `N`), bisecting on `N`, for `α = 2⁻⁶ … 2⁻¹⁴`:

| α | `1/√α` | `N_SOR(ω⋆)` | `N_ChebSOR` | **`N_opt`** | `N_opt·√α` | `N_SOR·√α` | LB (blocks) |
|---|---|---|---|---|---|---|---|
| 2⁻⁶ | 8.0 | 11 | 13 | 6 | 0.750 | 1.375 | 1.52 |
| 2⁻⁸ | 16.0 | 22 | 27 | 11 | 0.688 | 1.375 | 3.01 |
| 2⁻¹⁰ | 32.0 | 44 | 53 | 22 | 0.688 | 1.375 | 6.00 |
| 2⁻¹² | 64.0 | 87 | 105 | 43 | 0.672 | 1.359 | 12.00 |
| 2⁻¹⁴ | 128.0 | 173 | 209 | 85 | 0.664 | 1.352 | 24.00 |

`N_opt·√α` is **flat at 0.66–0.75** over four octaves: the optimum is
`Θ(1/√α)`, matching Theorem 3.3 to `3.5×` in blocks and `1.8×` in centre ops.
The optimizer drives `max ω → 2.000000` in every cell — it discovers the
`ω→2` member on its own. Golub–Varga cyclic-Chebyshev SOR is *worse* than
fixed `ω⋆` here (1.63 vs 1.36 in `N·√α`), because the target is a constant
factor, not an asymptotic rate.

**5.2 Battery on the full star, no symmetry assumed** (`verify.py` E3; 13
schedule families × 8 cells, `α = 2⁻⁶…2⁻¹²`): `sor_alt`, `gs_alt`, fixed
`ω ∈ {0.5, 1.5, 1.9}`, `ω = 2−10⁻⁶`, `ω = 2−α`, Chebyshev-like oscillating `ω`,
i.i.d. random `ω`, centre-bursts, leaf-heavy (4 leaf blocks per centre op),
**asymmetric partial-leaf blocks**, and Gauss–Southwell greedy.

* max `|ŷ_-|/B_-` (Lemma 3.1) = **0.9989** — never exceeded, nearly attained;
* max `|ω r_c|/cap` (Lemma 3.2) = **0.9786** — never exceeded, nearly attained;
* violations of `N_c ≥ LB`: **0 / 104**.
* Tightest members are `ω = 2−10⁻⁶` and `ω = 2−α` at `N_c/LB = 1.83–1.99`;
  `sor_alt` sits at `3.65–3.67`; `gs_alt` at `15–118` (the monotone rate);
  `leaf_heavy` at `12–477` (buying cheap leaf work does not substitute for
  centre ops, exactly as Theorem 3.3 says).

**5.3 Zoo sweep** (`general.py` E4.a): 11 graphs × `α ∈ {2⁻⁶, 2⁻¹⁰}` × 5
schedules (sweeps at `ω⋆`, 1, 1.99, `2−10⁻⁸`, and uniformly random `(u, ω)`),
`ε = π_v/(4 d_v)`: **0 violations** of the Prop-3.4 cap or of `N_v ≥ LB`.
Cap utilization is 0.94–0.98 on stars and 0.22–0.67 elsewhere — again, the star
is where the mechanism is tight.

**No schedule beat the bound.** We report this as evidence *for* the theorem,
not as proof; the theorem is what carries the claim.

---

## 6. Calibration against I4-D — and a correction to the manuscript's spider

### 6.1 The long spider has an empty answer

I4-D proved `vol(S_ε) < 1/ε` unconditionally. The brief asked whether the
candidate family is even consistent with that. It is not, and dramatically so.
For the manuscript's `k = θ/ε` arms of length `L ≈ 1/√α` (`θ = 1/8`), the
seed's own degree-normalized value is `π_v/d_v ≈ √α/k`, so
`π_v/(d_v ε) ≈ √α/θ < 1` for `α < θ²`. Measured (`calib.py` E1.a):

| α | `π_v/(d_v ε)` | `vol(S_ε)` | `|S_ε|` |
|---|---|---|---|
| 2⁻⁶ | 1.0365 | 8 | 1 |
| 2⁻⁸ | 0.5186 | **0** | **0** |
| 2⁻¹⁰ | 0.2593 | **0** | **0** |
| 2⁻¹² | 0.1297 | **0** | **0** |

So for `α ≤ 2⁻⁸` the long spider's correct `ε`-output is the **zero vector**,
`W = 0` suffices, and *no* class lower bound above `0` can be proved on it.
`thm:cf-spider-lower`'s `Ω(1/(αε))` is therefore a sharp statement about the
`γ_α ε d`-activation certificate — precisely I4-D §5's "the rule demands
`α·ε` where the optimum only needs `0.06·ε`" — and **not** about the semantic
problem. Any future graph-uniform claim must re-instantiate it with
`k ≲ √α/ε`; but at that `k` the whole spider has volume `Θ(1/ε)`, so the family
cannot force `1/(√α ε)` either. **This is why the star, not the spider, is the
right hard instance for `R±`.**

### 6.2 Where the `√α` really lives, seen twice

The same obstruction shows up on a path. A forward sweep at `ω⋆` reproduces the
interior geometric decay `π_{j+1}/π_j = λ` *exactly* (`c_α ω⋆ = 2λ`), and even
the endpoint ratio `π_1/π_0 = 2λ` — but the seed's own value is short by the
factor `1−λ² = Θ(√α)`, because `z_0 = ω⋆γ_α` while `π_0 = ω⋆γ_α/(1−λ²)`.
Measured (`calib.py` E1.b): one forward sweep leaves in-prefix error
`7.6e-2 → 1.5e-2` for `α = 2⁻⁶ … 2⁻¹²`, not `1e-15`. The seed amplification
`π_v/γ_α` is the whole story, and Lemma 3.2 caps the rate at which any `R±`
member can climb it.

### 6.3 The `log(1/α)` in I2-D T3 is a stopping-rule artefact

`stops.py` E6, star, `εm = 1/8`, SOR(ω⋆), blocks to stop:

| α | `N_err` (semantic) | `N_res` (certificate) | `N_err·√α` | `N_res·√α` |
|---|---|---|---|---|
| 2⁻⁶ | 11 | 21 | 1.375 | 2.625 |
| 2⁻¹⁰ | 44 | 109 | 1.375 | 3.406 |
| 2⁻¹⁴ | 173 | 536 | 1.352 | 4.188 |
| 2⁻¹⁶ | 345 | 1171 | 1.348 | 4.574 |

`N_err·√α` flat, `N_res·√α` growing like `log(1/α)`. Since `R±` is defined by
the semantic guarantee, its correct star upper bound is `Θ(m/√α)` with **no
log**, and I2-D Corollary 4.1's separation ratio improves from
`Ω(1/(√α log(1/α)))` to `Θ(1/√α)`. (I2-D Theorem 3.3 is not wrong — it bounds
the residual-stopped run — but its `log(1/α)` should be attributed to the
certificate, per I4-D §5.)

---

## 7. Is the class bound consistent with I4-D? Yes — and it is not a barrier

On the star, `vol(S_ε) = 2m = 1/(4ε)`, so `ε·vol(S_ε) = 0.25 < 1` ✓ (I4-D
Lemma A). Theorem 3.3 says `R±` work exceeds this output by `Θ(1/√α)`. There is
no contradiction: I4-D bounds the *output*, and a class may pay more than it
prints.

But the converse matters and must be said plainly. **On the same star, a
non-`R±` mechanism finishes in `O(1/ε)`**: eliminating the centre from
`H π = γ_α e_v` gives `π_c = γ_α/(1−c_α²)` and `π_l = c_α π_c/m` in closed
form, i.e. `O(m) = O(1/ε)` charged work (one degree scan plus `m` output
writes) — matching I4-D's `O~(1/ε)` corrected target and beating **every**
member of `R±` by `Θ(1/√α)`. So:

> Theorem 3.3 is a **class** theorem, not a complexity barrier. It says
> one-hop relaxation with `ω ∈ (0,2)` is `1/√α` away from the output scale on
> reflecting seeds, and it locates the reason (Lemma 3.2's fast-mode cap). It
> gives **no support** to the field's `1/(√α ε)` target as a *necessary* cost.

Combining the campaign's three class results on one instance
(centre-seeded `K_{1,m}`, `m = ⌊1/(8ε)⌋`):

| class | axiom dropped | star work |
|---|---|---|
| `M₊` monotone push | — | `Θ(1/(αε))` (I2-D T2) |
| `M±` signed step | step sign | `Θ(1/(αε))` (I2-D T2) |
| **`R±` signed residual** | `r ≥ 0` | **`Θ(1/(√α ε))`** (here) |
| elimination / Schur | one-hop locality | `Θ(1/ε)` |

Each row drops exactly one axiom and buys exactly one factor of `√α`. That is
the cleanest statement the campaign has produced.

---

## 8. Status, gaps, next target

| # | statement | status |
|---|---|---|
| L1 | Lemma 3.1 mode cap; Lemma 3.2 displacement cap | **Proved-draft**, 104-run battery, 0 violations, ≤0.98 utilization |
| L2 | Theorem 3.3 `W ≥ 3/(128 ε√(α(1+α)))` for all of `R±` on the star | **Proved-draft**, 0 violations, tight to 1.8× in `N_c` |
| L3 | Theorem 4.1 two-sided `Θ(1/(√α ε))` | **Measured** (15 cells, both constants flat in `α` and `ε`) |
| L4 | Prop 3.4 general graphs, `N_v ≥ (κ_v/4)√(π_v/γ_α)` | **Proved-draft**; `Ω(1/√α)` only when `π_v/γ_α = Θ(1/α)` (Measured: star yes, 1-D families no) |
| L5 | long spider has `S_ε = ∅` for `α ≤ 2⁻⁸` | **Measured** (exact solves) |
| L6 | I2-D T3's `log(1/α)` is a stopping-rule artefact | **Measured** |
| L7 | elimination beats all of `R±` on the star by `Θ(1/√α)` | **Proved-draft** (closed form) |

**Gaps.**
1. **Only the seed's ops are counted.** Theorem 3.3 ignores leaf work entirely;
   adding the trivial `W ≥ vol(S_ε)` gives `W ≥ max(3/(128 ε√α), 1/(4ε))`,
   which is not an improvement for `α < 1`. Closing the remaining `3.5×` to the
   member frontier needs a ledger over all coordinates, not just `v`.
2. **Batched / block primitives are outside the class.** Lemma 3.2 is a
   *coordinate* statement; a block relaxation over `S` changes many `ŷ_φ` at
   once and evades it. Whether `Ω(1/(√α ε))` survives block one-hop relaxation
   is **Open** — and this is the first place a positive result should be
   hunted, since local AMG (I3-A) is exactly such a method.
3. **No graph-uniform version.** Prop 3.4 yields `Ω(α^{-1/4})` seed ops on
   1-D-like families. Whether some family forces `Ω(1/√α)` *and* has
   `vol(S_ε) = Θ(1/ε)` at a low-degree seed is Open; §6.1 argues the spider
   route is closed.
4. `ε` two-sided vs one-sided: Theorem 3.3 uses only `z_c ≥ π_c − ε d_c`, so it
   holds verbatim for the one-sided requirement too.

**Next target.** Gap 2. Define `B±(k)`: one-hop *block* relaxation on sets of
diameter ≤ 1, charged `vol(S)`. The star's centre-plus-all-leaves block solves
it in `O(m)`, so `B±(k)` breaks Theorem 3.3 immediately — meaning the right
question is not "does the bound survive blocks" but **"what is the cheapest
primitive that escapes the fast-mode cap, and is it implementable locally?"**
Lemma 3.2 says the escape condition is `‖P_{≥μ₀} (block direction)‖` small at
the seed — i.e. the block must be *spectrally aligned with the slow mode*.
That is a computable, local, and previously unnamed design criterion, and it is
the natural bridge to I3-A's local AMG and I2-B's HSEG-LDL.
