# W1 — Class lower bound: monotone one-hop local push methods on the star

Status: **Proved-draft** (theorem below, unaudited), **Measured** (all tables;
630 member runs, 0 assertion failures), plus two sharply-located **Open** gaps.
Code: `w1_monotone_lb/{gpush.py, run_verify.py, anti_push_search.py,
pump_exploit.py}`. Full console log: scratchpad `w1_out.txt`; rerun is ~10 s.

Setting (manuscript conventions): lazy operator, mass scale. `a=(1-α)/2`,
`c=(1+α)/2`, `c_a=(1-α)/(1+α)`. `M_op = cI - a A D^{-1}`,
`pr(h) = α M_op^{-1} h` (the lazy PPR of seed measure h), `π = pr(e_v)`.
Facts used (all one-line): F1 `1ᵀpr(h)=1ᵀh` (mass conservation);
F2 `h≥0 ⇒ pr(h)≥0`; F3 `pr(h) ≥ αh` for `h≥0` (lazy recursion
`pr(h)=αh+a(I+AD^{-1})pr(h)`); F4 max principle `max_u pr(h)_u/d_u ≤
max_u h_u/d_u` for `h≥0`, from `pr(d)=d` (the degree vector is a fixed
point — this fact also powers the output-map loophole in §5.2).

---

## 1. The class M

**Operational definition (3 lines).** State `(p,r)`, init `(0, e_v)`, with
`r ≥ 0` maintained at all times. One primitive, the *generalized push*
`gp(u,η)`, `η ∈ (0, 2r_u/(1+α)]`:
`r[u] -= (1+α)η/2;  r[w] += (1-α)η/(2d_u) ∀w~u;  p[u] += αη`, charged `d_u`.
Policy (choice of `u`, `η`, order, batching, stopping) is arbitrary, adaptive,
randomized; output is `p` (Cor. 7: `p+βr`, `0≤β≤α` also covered); correctness:
the output must satisfy `err = max_u (π_u - out_u)/d_u ≤ ε` on every input.

**Axiomatic definition.** (A1) *one-hop, directed*: each operation removes
residual only at its base vertex `u` and changes `r` only on `{u}∪N(u)`;
(A2) *sound*: `p + pr(r) = π` preserved exactly; (A3) *monotone*: `r ≥ 0`
always; (A4) `p` changes only at the base; (A5) work `d_u` per operation;
(A6) output `p`, guarantee `err ≤ ε`.

**Lemma 1 (characterization; Proved-draft).** (A1)+(A2)+(A4) force every
operation to be `gp(u,η)` for some `η>0`, and (A3) is equivalent to
`η ≤ 2r_u/(1+α)`.
*Proof.* `pr` is invertible with `pr^{-1} = (1/α)M_op`. Write
`Δp = t e_u`, `Δr = -ξe_u + Σ_w c_w e_w` (w ranges over `{u}∪N(u)`).
(A2) gives `t e_u = pr(-Δr)`, i.e. `-Δr = (t/α)M_op e_u =
(t/α)[(1+α)/2 e_u - (1-α)/(2d_u) Σ_{w~u} e_w]`. Matching neighbor
coordinates: `c_w = (t/α)(1-α)/(2d_u)`; removal-at-base-only (A1) forces
`c_w ≥ 0` hence `t ≥ 0`; set `η = t/α`. Net removal at `u` is `(1+α)η/2`,
so (A3) ⟺ the cap. ∎

Consequences: **lazy ACL push** (amount ξ≤r_u) is `gp(u, ξ)`; **non-lazy /
CF push** (removal ξ, nothing retained) is `gp(u, 2ξ/(1+α))`; **damped ω**
is `gp(u, ωr_u)`; partial, adaptive, below-threshold pushes are just choices
of η. **GS-SOR with ω>1** is `gp(u, ω·2r_u/(1+α))` — the *same primitive with
the cap violated* (`r_u` goes negative): it satisfies (A1),(A2),(A4),(A5) and
fails exactly (A3). Measured (T6): the invariant holds to 1e-16 for a signed
overshoot `η = 1.7·cap`, while any non-proportional neighbor split with the
same totals breaks it (err 2.6e-2) — the split is forced, the sign is the
only free boundary.

**Lemma 1' (star closure; Proved-draft, star-specific).** On `K_{1,m}`
(`m≥2`), even dropping (A4) — allowing `Δp` and `Δr` supported anywhere on
`{u}∪N(u)` — every sound one-hop operation decomposes as a nonneg
combination of simultaneous `gp`'s based inside `{u}∪N(u)`: a center-based
op = `gp(c,t_c) + Σ_w gp(w,t_w)`; a leaf-based op = `gp(l,t_l)` only.
*Proof sketch:* `Δp = Σ t_x e_x` with `-Δr = (1/α)M_op Δp`; `M_op e_c` has
support `{c}∪L` (all leaves), so a leaf-based op (support `{l,c}`) forces
`t_c = 0`; center-based ops may carry leaf components `t_w`, whose ledger
contributions are identical to separate leaf pushes. The work bound below
only counts *center-based* operations, so batching leaf-settles into a
center op (charged `m` once) changes nothing. ∎ (This also kills the
"systolic batch" cheat: a batch is a multiset of feasible gp's; all ledgers
below are linear and order-free.)

---

## 2. The lower bound (Proved-draft)

Instance: star `K_{1,m}`, center `c` seeded, leaves `L`, `m = ⌊1/(8ε)⌋`,
`ε ≤ 1/16` (so `m ≥ 1/(16ε) ≥ 2`), `vol = 2m`, `ε·vol ≤ 1/4`.
Let `Z_c, Z_L` = total η at center / at leaves, `Z = Z_c + Z_L`,
`N_c` = number of center-based operations, `W` = charged work.

**Lemma 2 (guarantee ⇒ ℓ1 mass).** If the output `p` of a member satisfies
`err ≤ ε`, then `‖r‖₁ ≤ ε·vol` at stopping.
*Proof.* `π - p = pr(r) ≥ 0` (F2), so
`‖r‖₁ = 1ᵀr = 1ᵀpr(r) = Σ_u d_u·(pr(r)_u/d_u) ≤ vol·err ≤ ε·vol` (F1). ∎
(The coordinatewise stopping rule `r_u < εd_u` implies the same directly,
and implies `err ≤ ε` by F4 — both standard stopping semantics land here.
Monotonicity is what converts a *sup* guarantee into *ℓ1* mass: signed
methods cancel inside `pr(r)` and escape precisely this lemma.)

**Lemma 3 (mass ledger).** After any legal sequence, `Σp = αZ` and
`Σr = 1 - αZ` exactly; with `r ≥ 0`, `‖r‖₁ = 1-αZ ≤ 1` and is
non-increasing. At stopping, Lemma 2 gives `αZ = 1 - ‖r‖₁ ≥ 3/4`, so
**`Z ≥ 3/(4α)`**.
*Proof.* Per op, `Δ(Σp) = αη` and `Δ(Σr) = -(1+α)η/2 + (1-α)η/2 = -αη`. ∎

**Lemma 4 (leaf ledger / flow).** At every time,
`Σ_{w∈L} r_w = (1-α)/2·Z_c - (1+α)/2·Z_L`, hence (`r≥0`)
`Z_L ≤ c_a Z_c` and **`Z_c ≥ Z/(1+c_a) = (1+α)Z/2 ≥ 3(1+α)/(8α)`**.
*Proof.* Identity by induction: a center op adds `(1-α)η/2` to the leaf set
in aggregate (every neighbor of `c` is a leaf, `d_c = m` cancels); a leaf
op nets `-(1+α)η/2` on the leaf set (its only neighbor is `c`); leaves
start at 0 (seed at center). Nonnegativity of the left side from `r ≥ 0`. ∎

**Lemma 5 (per-op cap at the center).** Every center op has
`η ≤ 2r_c/(1+α) ≤ 2‖r‖₁/(1+α) ≤ 2/(1+α)`, so
**`N_c ≥ (1+α)Z_c/2 ≥ 3(1+α)²/(16α) ≥ 3/(16α)`**.
*Proof.* Feasibility cap of Lemma 1 + `‖r‖₁ ≤ 1` from Lemma 3. ∎

**Theorem 6 (class lower bound).** For every member of M, every policy and
every stopping rule whose output satisfies `err ≤ ε` on the center-seeded
star with `m = ⌊1/(8ε)⌋`, `ε ≤ 1/16`, `α ∈ (0,1)`:
`W ≥ m·N_c ≥ 3(1+α)²/(256·αε) ≥ 3/(256·αε)`.
*Proof.* Each center op is charged `d_c = m ≥ 1/(8ε) - 1 ≥ 1/(16ε)`;
multiply Lemma 5. ∎

**Corollary 7 (residual add-back).** If the output is `p + βr` with
`0 ≤ β ≤ α ≤ 1/2`, then `π - (p+βr) = pr(r) - βr ≥ (α-β)r ≥ 0` (F3), Lemma
2 gives `‖r‖₁ ≤ ε·vol/(1-β) ≤ 1/(4(1-α)) ≤ 1/2`, and the chain yields
`W ≥ (1+α)²/(128·αε) ≥ 1/(128·αε)`. (β > α is *not* safe — §5.2.)

Where structure is used: **undirectedness** enters through reversibility
(`pr(d)=d` for F4, and the symmetric roles of the two directions of an edge
in Lemma 1's split); **star structure** enters only in Lemma 4 (bipartite
flow: all center outflow lands on leaves, all leaf outflow returns to the
center, leaves start empty) and in `d_c = m` (Theorem 6). Everything else is
graph-free.

## 3. Axiom audit — weakest conditions per step

- **Lemma 2+3 (Step 1)** need: per-op settle `= αη` with per-op ℓ1-drain
  `= αη` (any common rate works), `r ≥ 0`, output `p` (or `p+βr, β≤α`), and
  the semantic guarantee. *Not needed:* the exact lazy split, full pushes,
  any ordering/threshold discipline.
- **Lemma 4 (Step 2)** needs: one-hop locality, seed at center, `r ≥ 0` *at
  leaves only*, and a bounded outflow/drain ratio — in axiomatic form: leaf
  inflow per center op `≤ f⁺η` and net leaf drain per leaf op `≥ g⁻η` with
  `f⁺/g⁻ ≤ c` gives `Z_c ≥ Z/(1+c)`. The invariant supplies
  `f⁺/g⁻ = c_a < 1` exactly; any "leaky" update family with a uniform ratio
  bound would do.
- **Lemma 5 (Step 3)** needs: `r ≥ 0` *globally* (`‖r‖₁ ≤ 1` and
  `r_c ≤ ‖r‖₁`) plus the removal-feasibility cap, plus *directedness* (see
  §5.3). This is the load-bearing monotone step.
- Variants: (i) non-lazy — member, `η = 2ξ/(1+α)`; (ii) partial `ξ<r_u` —
  member; (iii) pushes at inactive vertices — allowed, proof is
  policy-free; (iv) adaptive step sizes — allowed; (v) simultaneous /
  batched pushes — ledgers are linear and order-free, and Lemma 1' covers
  single-charge center batches. All five verified numerically.

## 4. Mechanical verification (Measured)

Grid: `α ∈ {1/4, 1/16, 1/64}`, `ε ∈ {2^-5..2^-9}` (`m ∈ {4..64}`), 15
member policies × 2 stopping rules (`coord`: all `r_u < εd_u`; `l1`:
earliest `Σr ≤ ε·vol` — the weakest legal stop), randomized policies with 3
seeds → **630 runs, 0 failures** of: mass identities ≤ 1e-12·(ops/5e4)
(drift consistent with ulp/op), `min_t min_u r ≥ -1e-12`, invariant
`‖p+pr(r)-π‖∞ ≤ 1e-9` at stop, `Σr ≤ ε·vol` at stop, center-η ≤ 2/(1+α),
`W ≥ 3/(256αε)`, `m·N_c ≥ 3/(256αε)`, `N_c ≥ 3/(16α)`. Lib cross-check:
simulator reproduces `lib/model.appr_lazy` exactly (same W, same p).
Lemma 4's identity holds to 2e-15 on instrumented runs, with measured
`Z_L/Z_c = 0.849–0.853 ≤ c_a = 0.882` at α=1/16.

Work constants `c = W·αε` (min over grid):

| policy (stop=l1) | min c | | policy | min c |
|---|---|---|---|---|
| cheap_first / nonlazy / greedy_nonlazy / jacobi_nonlazy | **0.0867** | | appr_fifo | 0.219 |
| damped_0.9 | 0.281 | | greedy / rand_v | 0.230–0.250 |
| appr_lifo | 0.3125 | | rand_xi / rand_mix | 0.297–0.436 |
| damped_0.5 | 0.594 | | damped_0.1 | 3.26 |
| jacobi (lazy) | 0.271 | | tiny_leaf (adversary) | 2.54 |

- **Empirical frontier `c0 ≈ 0.0867`** (flat in ε and α, as the theorem
  predicts a pure `1/(αε)` law), achieved by full non-lazy pushes,
  leaf-first, earliest-ℓ1 stop. Center-work-only constant as low as 0.0449.
  **No member policy ever came below the proved 3/256 = 0.0117**; gap
  proved→best-member ≈ 7.4x (slack: Lemma 5's cap 2/(1+α) vs typical η,
  and Lemma 3's 3/4 vs the ~1 actually settled).
- Literal manuscript APPR (FIFO, coord): `c ≈ 0.30–0.31`, consistent with
  the manuscript's Θ(1/(αε)) with the constant sandwiched in [3/128, 1].
- `tiny_leaf` adversary (leaf pushes of size ε/10, up to 2.4e5 ops): wastes
  39x the frontier work, never dents the bound — tiny/lazy spinning at
  leaves adds work but cannot substitute for center ops (Lemma 4 forces
  `Z_c`; Lemma 5 prices it).

## 5. The class boundary is meaningful (three witnesses)

**5.1 Signed over-relaxation (violates A3).** GS-SOR sweeps, oracle stop at
`err ≤ ε` (most favorable for SOR):

| α | ω=1.5: c=W·αε | ω_opt(α): c | min r | max‖r‖₁ | max η_c (cap 2/(1+α)) |
|---|---|---|---|---|---|
| 1/4 | 0.1875 | 0.1250 | -0.50 | 1.0 | 2.4 / 1.78 |
| 1/16 | 0.0469 | 0.0469 | -0.63 | 1.9 | 3.5 |
| 1/64 | 0.0312 | 0.0234 | -1.11 | 3.0 | 5.8 |
| 2^-8 | 0.0293 | **0.0107** | -2.6 | 5.9 | 11.7 |
| 2^-10 | 0.0291 | **0.0054** | -5.5 | 11.8 | 23.5 |

- **ω = 1.5 does NOT beat the conjectured bound on the star**: its constant
  freezes at ≈ 0.029–0.031 for small α (ε-independent) — a fixed ω only
  buys a ~3x constant over the best member (0.087), staying ~2.5x above
  the proved 0.0117. Fixed over-relaxation does not change the Θ(1/(αε))
  scaling.
- **ω_opt(α) = 2/(1+√(1-c_a²)) breaks the class scaling**: measured
  `c ∝ √α` (halves per 4x drop in α), crossing the proved member constant
  at α ≈ 2^-8 and the member frontier already at α = 1/16. Mechanism as
  diagnosed by the proof: `r < 0` (Lemma 2 dies by cancellation), transient
  `‖r‖₁ ≫ 1` and per-op center η up to 12x the member cap (Lemma 5 dies).
  So the theorem's value: monotonicity is exactly what forbids
  √α-acceleration; the boundary is real and sits at `r ≥ 0`.

**5.2 Output post-processing (violates A6).** After ONE full lazy center
push (`W = m`, all ops in M), `r = a·e_c + (a/m)Σe_l` is *exactly* the
degree-stationary measure: `pr(r) = r` (F4's fixed point), so `p + r = π`
**exactly** (measured err(p+r) = 2e-17 at W=64 vs LB=384). An "algorithm"
whose ops are all in M but which outputs `p+r` computes π exactly with
`W = m ≈ 1/(8ε)`, no 1/α at all. The output map is therefore part of the
class definition, not a formality: `β ≤ α` add-back is safe (Cor. 7;
measured: oracle-stop at `err(p+αr) ≤ ε` costs W=13248 ≥ LB=384), `β = 1`
is fatal. (This is the FORA/residual-correction phenomenon: hybrid
estimators that consume `r` escape push lower bounds.)

**5.3 Reverse moves (violates A1's direction).** If `η < 0` is allowed
(anti-pushes: one-hop moves *into* the base, still `r ≥ 0`, invariant
exact), randomized adversarial rollouts **pump** `r_c` to 14.4 and `‖r‖₁`
to 28 (α=1/4, m=4) by driving `Σp` negative (un-settling) — so Lemma 5's
cap `η ≤ 2/(1+α)` genuinely fails for the signed-η class; directedness is
load-bearing. However a crafted pump-then-solve exploit never wins:
W(pump to K)/W(no pump) = 1.7x, 2.4x, 3.7x for K = 2, 4, 16 (α=1/64,
ε=2^-9; same pattern on the whole grid) — borrowed mass must be re-settled
at the same α-rate. Whether Theorem 6 (with a worse constant) extends to
the signed-η, `r ≥ 0` class is **Open**; the exploit evidence says yes.

## 6. Edge cases

- Overshoot `ξ > r_u` keeping other coordinates ≥ 0: excluded by `r_u ≥ 0`
  at the base; this *is* SOR (§5.1).
- Tiny pushes / lazy self-retention spinning at leaves: cost 1 per op, only
  add work; center work is forced independently (`m·N_c ≥ 3/(256αε)`
  asserted on every run incl. the tiny-leaf adversary).
- Below-threshold pushes, adaptive η, batches: covered (§3), verified.
- Numerical caveat: identities drift ~1 ulp/op; all claims use ops-scaled
  tolerances.

## 7. Honest gaps (in decreasing severity)

1. **Output maps.** Only `out = p + βr`, `β ≤ α` is covered. §5.2 shows
   *some* local post-processing (β=1) destroys the bound entirely, so the
   theorem cannot be strengthened much here — but a principled boundary
   ("which output maps are forbidden?") is missing. Any final theorem must
   say "algorithms that output their settled mass," and that is a real
   modeling restriction, weaker than one would like.
2. **Signed-η / reverse-move class** (§5.3): Lemma 5 fails as stated;
   bound conjectured to survive via a re-settlement-cost potential
   (`Ψ = r_c + c_a Σ_L r` decreases only via center ops; pumping measured
   unprofitable), unproved.
3. **Lemma 1' beyond the star / multi-base batches on general graphs**: the
   characterization with p-gain off-base is proved only on `K_{1,m}`; on
   general graphs an op settling on `{u}∪N(u)` can require two-hop residual
   support and is not classified. Also `α ≤ 1/2` is assumed in Cor. 7.
4. Cor. 7's constants and the main 3/256 are certainly loose (measured
   frontier 0.087); no attempt to optimize.
5. Randomized-policy coverage is 3 seeds/policy on a 15-policy zoo —
   adversarially *optimal* member policies were probed only via
   `cheap_first`/frontier reasoning, not exhaustively.

## 8. Next falsifiable targets

- **T1 (signed class).** Prove or refute: one-hop, invariant-exact,
  `r ≥ 0`, *signed*-η methods obey `W = Ω(1/(αε))` on the star. Candidate
  tool: potential `Φ_θ = Σp + θ(r_c + c_a Σ_L r)`; falsifier: a pump
  schedule with work `o(m/α)` reaching `err ≤ ε` (search harness exists,
  `pump_exploit.py`).
- **T2 (separation, upper side).** Prove the measured SOR(ω_opt) upper
  bound `W = O(m·log(1/ε)/√α)` on the star for the signed one-hop class —
  together with Theorem 6 this gives a clean monotone-vs-signed
  `√α`-separation on one instance, i.e. the theorem's value statement.
- **T3 (beyond the star).** Conjecture: for every graph and seed,
  members of M satisfy `W ≥ c·(1/α)·vol(S_ε)` for a suitable ε-support
  volume `vol(S_ε)`; the star is the extremal case `vol(S_ε) ≈ 1/ε`.
  Falsifier candidates: spider/caterpillar from `lib/zoo.py`.
