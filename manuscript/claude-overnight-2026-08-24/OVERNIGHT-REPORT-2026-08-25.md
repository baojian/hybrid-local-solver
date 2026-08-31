# Overnight research campaign — consolidated report

**Project:** hybrid-local-solver (accelerated local PageRank).
**Ran:** 2026-08-24 20:40 → 2026-08-25 06:45 CST, autonomous, 3 iterations,
20 direction-agents, ~3.4M agent tokens.
**Method:** each iteration launched k parallel directions with a falsifiable
target and a kill criterion; results were merged into a scoreboard; each
direction was then continued, killed, merged, or spawned into new ones.

**Status of everything below.** This is campaign output, not repository-grade
work. Labels follow your vocabulary: **Proved-draft** = a proof written and
mechanically verified here, never independently audited; **Measured** =
numerics with a charged-work ledger; **Refuted-draft**; **Open**. Nothing was
written to `notes/`; no repository claim was promoted. Two findings *correct*
statements in my own assessment of yesterday afternoon, and one corrects a
diagnosis inside the campaign itself.

All code, per-direction findings (17 files, ~300KB), and raw JSON are in
`claude-overnight-2026-08-24/`.

---

## 1. What changed in the problem's landscape

Four results move the map. In descending order of how much they should change
what you do next:

### 1.1 The information question is closed — the open problem is purely computational

**W2 + I2-E, Proved-draft + Measured.** On the spider ensemble, the number of
adjacency probes any algorithm needs is **Θ(1/ε), α-free**, matched to a factor
of 80 — *not* `1/(√α·ε)`.

- *Lower*: a Yao-randomized ensemble forces `Ω(1/ε + log(√α/ε)/√α)` probes,
  with a **capacity ceiling of Θ(1/ε)** over the whole family — so no spider
  ensemble can ever witness the product scale. This is the extremal
  confirmation of why your killed-Green corridor attempts kept failing.
- *Upper*: an explicit interval-envelope algorithm with an O(1)-per-probe
  certificate achieves `T ≤ (1+o(1))/ε` on **every** spider, and extends to
  bounded-degree trees **with no degree bound needed** (105 cells, all
  ε-valid). The five-condition certificate collapses to one scalar inequality
  `y/(1−y²) ≤ β`.

**Consequence:** any `Ω(1/(√α·ε))` lower bound must charge *arithmetic*, not
information. Corridor-style routes are provably exhausted. This retires
direction D6 of yesterday's assessment as I stated it (I had it as a promising
information route; it is instead a proof that the route cannot work), and it
sharpens `conj:influence-packing`: the conjecture is either false at product
scale or needs a non-corridor mechanism.

### 1.2 α-free mechanisms exist on every family tested — and the map is indexed by ball treewidth

**I2-F + I3-A, Measured (69 cells, 0 verification failures).** See Figure 1.
Local multilevel response (a V-cycle built on the explored region, with
coarsening, transfers, RAP, and coarse solves all charged — setup is 26–93% of
the bill) has α-exponent **−0.16 … +0.34 on all twelve families**, against
push 0.82–1.39 and truncated Chebyshev 0.28–1.25. The V-cycle rate *saturates*
as α→0 (measured to α = 2⁻²⁰): the shift only helps, so cycle count is
Θ(log(1/ε)), α-free.

But the surprise is what wins: **local elimination on a growing ball, charged
identically, is 11–116× vol and α-free on 9 of 12 families**, beating AMG by
1.8×–51×. AMG wins outright only where the ball has high treewidth — 2-D grids
and 3-regular expanders at α ≤ 2⁻¹², exactly where elimination is catastrophic
(1.8·10⁴ and 1.6·10⁶ × vol).

**Consequence:** the campaign's map is **two-regime, indexed by the treewidth
of the explored ball**, not by "multilevel vs the rest". Push, polynomial
methods, and elimination all pay one pass per unit of *radius* (α^−1 or
α^−1/2); multilevel response is the first charged mechanism whose pass count is
set by log(1/ε). This whole mechanism family is absent from all 18 note
directions, and it sits squarely inside your response track.

*Honest limits:* AMG's constant tracks Galerkin operator complexity and is
destroyed by heavy-tailed degrees (random recursive tree: 9,000–22,000 units
per unit of output). On expanders `vol(S_ε) = Θ(n)`, so "local" is vacuous
there regardless of mechanism.

### 1.3 The boundary scan — the binding cost in the worst family — was an artifact

**I2-A + I3-B, Proved-draft + Measured.** See Figure 2. I2-A found that on a
marginal-hub ring, *even with a perfect admission gate and zero spurious
admissions*, **87% of a local solver's charged work was rescanning the boundary
for KKT violations**. I3-B then showed this is an artifact of *pulling*:
`grad_j` depends only on `N(j) ∩ S`, and the interior solver already scans
`N(i)` for every coordinate it touches. Pushing two accumulators
(`P_j = Σ Q_ji p_i`, `M_j = Σ Q_ji Mh_i`) gives `−grad_j` **exactly in O(1)**,
maintained inside work already paid for. Measured: **266× cheaper** than eager
rescan on the adversarial ring, flat in hub degree, 0 misses and 0 false
reports in 50 runs against exhaustive checking; at poll-every-step (your
frontier-1 requirement — report the crossing on the step it happens) the
advantage is 1,900–17,700×.

Three elementary facts carry it: `|∂S| ≤ vol(S)` always; maintenance is
`|N(i)\S| ≤ d_i` per interior step; and a newly admitted vertex's new boundary
has it as their only S-neighbour, so growth is `O(d_{j₀})`.

**And the structural question I2-A left open is closed.** Summing KKT gives an
exact leak identity yielding
`vol(shell_τ)/vol(S*) ≤ (1/τ)·[1/(ρ·vol(S*)) − 1]` — **α cancels identically**.
A hub-ladder construction attains it to within 1–2%. So a fat gate-relevant
boundary is a `ρ·vol(S*) ≪ 1` phenomenon, never an α phenomenon.

This is directly relevant to your frontier-1 interface ("report all boundary
KKT crossings without rescanning the full boundary after every light update"),
for which five cyclic gadget families were retired trying to build lower
bounds. The kinetic gate answers the *upper* side of that interface.

### 1.4 Route B's target looks true, and the K_n case is drafted

**W7 + I2-C + I3-C, Proved-draft (verified exactly) + Measured.**

- The reconstruction of your safeguarded AESP-CD recurrence was **validated
  5/5** against your published exact constants (γ₂ = 57072309867/51440146040,
  γ₃ = 192036347475007/168765931042095, P₄ J₅₀₀ = 1.023646 — all digits).
- Windowed inflation slopes are **≤ 0.145 on every known adversarial family and
  every perturbation searched** (target: < 1). The K₂ family that kills
  one-step banks has slope 0, and its killer bank *contracts* per-window
  (c_win ≈ 0.62). No counterexample direction emerged. **Evidence that the net
  exponent target is true and the obstacle is proof technique.**
- On complete graphs the result is stronger than windowed: **K_n absorbs** —
  corrections stop by stage ≤ 12, so `J_T ≤ B ≤ 0.369 < log 2` and packing
  holds with **c = 1**. 17/17 lemma predicates verified exactly on 140
  instances (n ∈ {2,4,8,16,32} × q ∈ {1/10,1/100,1/400} × 5 seeds × 2 ρ),
  7,130 stage-checks per universal predicate. The positive-part/spectral
  non-commutation obstacle is *resolved* on K_n: D = (n−1)I makes the projector
  mean-centering, and coordinatewise 1-Lipschitz maps contract variance, so
  corrections never pump low-frequency into high.
- **The general-graph crux was then misdiagnosed and re-diagnosed.** I3-C
  proved the needed inequality exactly — for any `v > 0`, `u ≥ 0`, `Δ > 0`,
  `‖P min(u, Δv)‖ ≤ ‖P u‖`, in both the Euclidean and Q-weighted norms, via the
  identity `‖Pu‖² = ‖v‖²·Var_π(u/v)` with `π_i = v_i²/‖v‖²` (for `v = D^{1/2}1`,
  π is the random-walk stationary distribution; the Q-form adds Dirichlet
  energy, and both terms contract). 1.5M random samples + 2,520 exact-rational
  instances: **0 violations**. Non-regularity therefore costs *nothing* — on
  full-support instances the relevant Perron vector is exactly `D^{1/2}1`.
  **The real obstruction is the support face**: on a proper face the face
  operator's Perron vector is misaligned (cos = 0.9099 on your P₂₄-type family,
  α_S/α = 2.19), and face-aligned contraction fails 12/16 there.
- A general-graph statement is now in reach: the K_n absorption theorem extends
  to **every connected graph with μ₂ ≥ 2q**, with one `1/√d_min` loss, modulo
  the same single Open link. An exact threshold was derived and verified 300/300:
  `s_k(2−m_k) ≤ (1−q)² ⟺ μ_k ≥ 2q`. Your P₂₄ family has μ₂ = 0.0093 ≪ 2q =
  0.0625 with three modes below threshold — which quantitatively explains why
  it is the hardest cell you have.

**Deliverable for your audit battery:** a new sharpest sustained stress family,
pinned to exact dyadic parameters — `P₂₄, q = 1/32, α = 1/1025, ρ = 65/4096`,
endpoint seed, |S*| = 23, breakpoint ρ* ≈ 0.0157290668; 91 inflation events to
t = 4748, slope 0.1255, max γ 1.4391, word bit-exact against the float mirror.
Note ρ = 1/64 (just below ρ*) is transient — the family is sharp.

---

## 2. Two manuscript-ready packages

### 2.1 Monotone-vs-signed separation (W1 + I2-D) — Proved-draft, a candidate section

Class **M**: state (p,r) with **r ≥ 0**, one-hop primitive charged `d_u`,
arbitrary adaptive/randomized/batched policy, output `p + Mr`.

- **Lower bound**: `W ≥ c/(α·ε)` on the center-seeded star, ordering-independent.
  The constant improved 3.7× over iteration 1 (to `W·αε ≥ 0.0433`, against a
  measured member frontier of 0.0867 — exactly 2×), and the new proof is
  **graph-free**, retiring three lemmas and the star-specific leaf-flow ledger.
- **The key object** is a single potential `Ψ(r) = pr(r)_c/π_c = (π_c − p_c)/π_c`.
  Any invariant-preserving update has `ΔΨ = −Δp_c/π_c`, so **Ψ moves only at
  seed-based operations, for either sign of the step** (verified to 3.6e-15 on
  10 graphs); `r ≥ 0` then forces `r_c ≤ Ψ`, giving a one-sided multiplicative
  bound. This closed the signed-step gap.
- **The separating axiom is `r ≥ 0`, not the sign of the step** — a cleaner and
  more quotable statement than the one I proposed yesterday.
- **Output maps**: the planned strengthening turned out **false**, and the truth
  is sharper. A Gale/Hall transport characterization shows radius-1 instances
  collapse to one scalar — the column mass `B` of the output map — with an exact
  threshold `B = 1 − ε·vol`, attained at `W = 0` and matched by `M = B·I` at
  `W = m`. `Ω(1/(αε))` holds for every `B < 1 − ε·vol`; at radius ≥ 2, `B = 1`
  costs `Ω(vol)` transport.
- **Upper half**: signed SOR at ω\* on the star is
  `O(m(log(1/ε) + log(1/α))/√α)`, measured at 0.53–0.57× the bound, from your
  own exact block recurrence `x_j = (j+1)λ^j`.
- **Separation**: same star, same primitive, same charge, same output —
  `Θ(1/(αε))` vs `Õ(1/(√α·ε))`, ratio measured 0.34 → 5.84 as α: 1/4 → 2⁻¹².

Two labelled Opens: no companion *class* lower bound for signed-residual
methods (so this is method-vs-class, not class-vs-class), and one constant in
the general-graph version is measured rather than proved.

### 2.2 The K_n absorption theorem (§1.4) — Proved-draft with a complete verification harness

---

## 3. Mechanisms measured, with honest failure modes

| Mechanism | Where it wins | Where it fails | Status |
|---|---|---|---|
| **Kinetic boundary gate** (I3-B) | everywhere; mechanism-independent | — (0 misses; ≤7% overhead on benign families) | Proved-draft + Measured |
| **Local elimination on a growing ball** (I3-A) | 9/12 families, α-free, 11–116×vol | high-treewidth balls: grids 1.8·10⁴×, expanders 1.6·10⁶× | Measured |
| **Local multigrid** (I2-F, I3-A) | grids, expanders — α-free everywhere | heavy-tailed degrees (RRT 9k–22k×vol); setup = operator complexity | Measured |
| **HSEG-LDL dynamic tree factorization** (I2-B) | all trees incl. the comb: q = 0.92–1.11, α-free, 149/149 certified | re-carve amortization Open; 6–57× above per-family best | Measured + Proved-draft |
| **Randomized APCG w/ carried momentum** (W3, I2-A) | α-exponent 0.45–0.51 vs 0.87–1.0 baselines; K₂/K₈ blockers do **not** bite (q^−1.0 in mean *and* max) | marginal-hub ring: spurious volume ω(vol(S*)) — 191.8× at hub degree 384; hysteresis tames but does not remove | Measured; damage bound Proved-draft |
| **Explore-eliminate-substitute** (W4) | spiders at product scale (s = 0.502 vs SOR 0.94) | grids (10⁵×); cost law vol + m³, m = ≤2-irreducible kernel | Measured |
| **Truncated Chebyshev** (W5) | star: beats push up to 43× | wherever ball volume is superlinear | Measured |
| **Two-stage push+SOR** (your CF-Push) | — | reproduced your Ω(1/(αε)) spider obstruction independently | Measured |

**Killed this campaign:** the product-scale information route (W2/I2-E — proved
impossible on corridors); the "second instance kills B=1" plan (I2-D — false);
uniform carry-mode APCG locality (I2-A — broken on volume); admission-order
append-only LDL and seed-rooted tree-DP as general tree backends (I2-B — the
comb defeats both, and defeats the inherited segment-tree design too).

---

## 4. What I got wrong yesterday, corrected

1. **D6 (spider information bound)** — I proposed proving `Ω(1/(√α·ε))`
   information-theoretically. That is *false*: information is Θ(1/ε), α-free.
   The correct use of the spider ensemble is the opposite — it proves the open
   problem is computational.
2. **The classic wedge `ε < √α` as the prize region** — W8 measured the
   practical prize at **<10× everywhere** in α ≥ 2⁻¹⁴, ε ≥ 2⁻¹³, and found the
   push/WY boundary is a *horizontal line in α*, not the `ε = √α` curve. On
   grids the target is not vacuous but *vacuously loose* (measured 22–91,491×
   above output size), because grid output is Θ(log²(1/ε)/α) — polylog in 1/ε
   while the target is linear. **The right target on high-treewidth families is
   output-linear with α-free constants**, not the product scale.
3. **D1's framing (warm-started incremental solvers)** — warm-starting buys a
   log factor and **never an order** (7,101 pooled rounds, correlation 0.862
   with the log-ratio prediction). The order comes from *incremental
   factorization*, which is a different mechanism. The `1/ε²` pessimism is also
   unreal at fixed α on every zoo family — it lives only on the diagonal α = ε.

---

## 5. Revised priorities

**Tier 1 — do these first**

1. **Adopt the kinetic gate everywhere** (§1.3). It is mechanism-independent,
   costs nothing on benign families, and removes what was 87% of the work in
   the worst measured case. It also gives your frontier-1 interface its upper
   side. *Cheap, immediate, affects every direction you run.*
2. **Open a multilevel-response direction.** Absent from all 18 notes; the only
   α-free mechanism on high-treewidth balls; every level is charged, so it fits
   your ledger discipline unmodified. Pair it with local elimination under a
   **ball-treewidth triage** — that pairing covers 12/12 families measured.
3. **Finish the monotone-vs-signed separation** (§2.1) and put it in the
   manuscript. It is the cleanest statement the campaign produced and it
   justifies the project's pivot to signed/response methods in one line.

**Tier 2**

4. **Route B on general graphs** (§1.4): the path is now concrete — prove the
   single Open link (V-contraction at genuinely partial corrections; 1
   occurrence in 140 instances, 2.1% margin), then push the μ₂ ≥ 2q class
   theorem. Add the P₂₄ family to the audit battery. Test face-aligned capping
   (a partial agent proved the safety theorem for **any** `w > 0` with
   `Q_S w > 0`, so rational approximations keep the algorithm exactly
   implementable — the code is in `w7_windowed/i3g_core.py`, unfinished).
5. **Randomized APCG**, with the honest caveat: the α-exponent survives every
   stress but the *constant* is broken by marginal-hub rings. Combine with the
   kinetic gate (which fixes the boundary half) and hysteresis, then re-measure.
6. **HSEG-LDL** on trees: close the re-carve amortization (or falsify it with a
   `thrash(k)` family designed to flip the heavy/light boundary Θ(log) times).

**Tier 3 — reframe the lower-bound program**

7. Given §1.1, a product-scale lower bound needs a model that charges
   arithmetic. Before investing, note that spiders provably cannot witness it,
   expanders are non-local, and grids have polylog output — so a witness needs
   support volume ~1/ε, diameter ~1/√α, *and* a reason arithmetic cannot
   shortcut. The campaign's α-free upper bounds on trees, and now on 12/12
   families, are weak evidence the product bound may simply be **false** in
   general. That possibility deserves an explicit direction rather than being
   the null hypothesis nobody tests.

---

## 6. Loose ends

- Three iteration-3 directions were cut off by a session limit and produced no
  findings: the signed-residual **class** lower bound (I3-D, nothing written),
  the **end-to-end composed solver** with a full eleven-coordinate ledger
  (I3-E), and **face-aligned capping** (I3-G — but its safety theorem survives
  in code comments and is worth recovering).
- The eleven-coordinate ledger mapping is approximate in campaign code: I used
  six counters (C_adj, R_adj, C_rec, C_resp, C_mat, C_emit). Anything promoted
  needs the full vector.
- Everything is exact-real / float; **no finite-precision claims** anywhere.
- One measurement subtlety worth carrying into your own harness: the boundary
  certificate at threshold ε mis-certifies restricted solves by Θ(1/α) on
  reflector families (caught as a genuine assertion failure, with a
  maximum-principle fix); and separately, the restricted-solve certificate is
  loose by exactly 1/(8α) on a lattice, which is a certificate-family property,
  not a mechanism property.

---

## Figures

- `figures/fig1_alpha_exponents.png` — fitted α-exponents of W/vol(S_ε) for
  four mechanisms across twelve families.
- `figures/fig2_boundary_gate.png` — charged gate work on the marginal-hub
  ring: rescan vs pushed accumulators vs kinetic event queue.

## Contents of the delivery

```
claude-overnight-2026-08-24/
├── OVERNIGHT-REPORT-2026-08-25.md   (this file)
├── SCOREBOARD.md                    (per-iteration verdicts and decisions)
├── LOG.md                           (chronological campaign log)
├── figures/                         (2 figures + generator)
├── findings/                        (17 per-direction findings documents)
└── <direction dirs>/                (all code, checkers, raw JSON results)
```

---

# ITERATION 4 (2026-08-25 morning, 6 directions)

A fourth round was run after the report above. It changes the organizing target
of the whole program, produces the missing companion lower bound, and turns up
one finding about your **active manuscript** that should be checked before
submission.

## 4.1 The output bound, and what it does and does not say (I4-D) — CORRECTED

`ε·vol(S_ε) ≤ Σ_{v∈S_ε} d_v·u_v = Σ_{v∈S_ε} π_v ≤ Σ_v π_v = 1`, hence

> **vol(S_ε) < 1/ε unconditionally** — every graph, every seed, every α.

Measured across 687 cells and 14 families: 0 violations, max `ε·vol = 0.60`
(independently re-verified here: max 0.90 over 63 further cells). The bound is
tight, approached by regular expanders and stars at critical size. Degree volume
is the larger of the two candidate output measures (`|S_ε| ≤ vol(S_ε) < 1/ε`),
which settles the measure question.

**Attribution correction.** This inequality is *not new*. It is the classical
Markov-type volume bound, the same fact as FRS19 Thm 2
(`vol(supp(x*(ρ))) ≤ 1/ρ`) and ACL's `vol(supp(p)) ≤ 2/((1−α)ε)`. The agent
reported it as a discovery and the first version of this report repeated that
framing. What is genuinely useful here is the *systematic measurement* of how
far below the bound real instances sit, and the ridge experiment below.

**Framing correction — the earlier claim that FY22 is "refuted as a tight
target" was overstated.** Output size does not produce work lower bounds. The
correct statement is narrower:

> Output size alone can never justify the `1/(√α·ε)` scale, since the output is
> always below `1/ε`. Any justification — or refutation — of that target must
> come from a *work* argument.

And in the same iteration, I4-C supplied exactly such an argument in the
positive direction: the signed-residual class R± provably needs
`Ω(1/(√α·ε))` on the center-seeded star, where the output is only `~1/ε`. The
two results are consistent and together say something sharper than either:

| | star, output `~1/ε` |
|---|---|
| monotone / signed-step one-hop | `Θ(1/(αε))` — proved |
| signed-residual one-hop (R±) | `Θ(1/(√α·ε))` — proved |
| elimination | `Θ(1/ε)` — achieved |

So FY22 is **not refuted as an achievable target**; it is *tight for a natural
algorithm class* and *beatable by a stronger primitive on the same instance*.
The open question is unchanged in substance but better posed: for which
primitive classes is output-linear work achievable?

**The boundary is a different object, and it is genuinely unbounded.**
`vol(∂S_ε)` admits **no** bound of the form `f(ε, α)`. Construction (verified):
a seed with `k` hub neighbours of degree `D` — since `Σπ ≤ 1` forces
`u_hub ≤ 1/d_hub`, growing `D` pushes the hubs *below* threshold, so `S_ε`
collapses to `{seed}` while `vol(∂S_ε) = kD` diverges:

| hub degree D | vol(S_ε) | vol(∂S_ε) | ratio |
|---|---|---|---|
| 200 | 6 | 1,200 | 200 |
| 1,000 | 6 | 6,000 | 1,000 |
| 4,000 | 6 | 24,000 | 4,000 |

What *is* bounded is the **cardinality**: `|∂S_ε| ≤ vol(S_ε) < 1/ε` (each
boundary vertex consumes a distinct edge already counted in `vol(S_ε)`; the
table's `|∂S_ε| ≡ 6` is this). **This is precisely why the model needs an O(1)
degree query**: with it, a boundary vertex costs O(1) to adjudicate and the
total is `O(|∂S_ε|) ⊆ O(1/ε)`; without it, merely discovering that a hub does
*not* belong costs `d_hub`. Note this is a different object from I3-B's shell
lemma, which bounds the *gate-relevant* shell (slack within a constant factor
of threshold), not the full boundary.

**The ridge measurement stands** and is the substantive part of I4-D: following
the curve where `vol(S_ε) = Θ(1/ε)`, the log-log slope of `W·ε` against `1/ε`
is **0.000** on the star (2.5 decades, `W = 10.34/ε` exactly), 0.068 on the 2-D
grid, 0.215-and-falling on the path. No family shows a power-law excess for its
best mechanism. Against FY22 the portfolio wins on 8 of 11 families (ratios
0.034–0.71), losing only on grid2d (9.2×). Honest scope: `O~(1/ε)` is
consistent with every measurement but holds only at *portfolio* level — no
single mechanism was both output-bounded and α-free, which is what I4-E then
attacked.

## 4.2 Value-guided admission: the first mechanism with proved output-boundedness (I4-E)

Every region method in the campaign admitted by **adjacency**; push admits by
**value** and is therefore output-bounded, but is not α-free. VGF admits a
boundary vertex only when its certified value lower bound clears `γ·ε`.

- **Output-boundedness is proved** (Lemma V2: `S ⊆ {v : u_v ≥ θγε}`, no
  adjacency or distance term).
- On the **ball trap** (a clique hung off the support path, where the correct
  output is *empty*): `W·ε` slope **−0.05, flat in clique size M**, against
  **+2.94** for ball-elimination and **+1.92** for ball-AMG. On hidden-hub:
  flat vs exactly linear. The prediction was confirmed exactly.
- Region inflation exponent **+0.033 — α-free**; mechanism +0.064. The entire
  residual α-dependence (+0.256 end-to-end) is the **round count**, not the
  region and not the solver.
- 45/45 certified, 0 misses.

**What breaks it:** a *fan trap* — boundary vertices parked in the band
`[γε, ε]` — costs 516× in region and 938× against oracle. That, and the round
count, are the two named open items.

## 4.3 The companion class lower bound, and three corrections (I4-C)

**Proved-draft.** The signed-residual class **R±** (state `(z,r)` with `r`
signed, one-hop relaxation at any `ω ∈ (0,2)`, adaptive/per-vertex/randomized,
charged `d_u`) pays `W ≥ 3/(128·ε·√(α(1+α)))` on the center-seeded star. This
completes the separation into **class-vs-class**, which I2-D had listed as its
main Open.

The energy-budget route everyone would try **is vacuous** here (terminal energy
can exceed Φ₀; `ω→2` is empirically optimal and `ω/(2−ω)` is unbounded). What
works: energy monotonicity caps the fast spectral mode, and a center relaxation
moves both modes by *equal magnitude*, so `|Δz_c| ≤ 2√(α(1+α))` per operation
while `z_c` must travel ≥ 3/8 — pathwise, so randomization gets no exemption.
Numerically, direct L-BFGS optimization over ω-schedules gives `N_opt·√α` flat
at 0.66–0.75, with 0/104 violations over 13 schedule families.

**This yields a clean ladder on one instance, each row dropping one axiom and
buying one √α:**

| class | axiom dropped | work on the star |
|---|---|---|
| monotone `M₊`, signed-step `M±` | — | `Θ(1/(αε))` |
| signed residual `R±` | `r ≥ 0` | `Θ(1/(√α·ε))` |
| elimination | one-hop locality | `Θ(1/ε)` |

**Three corrections came with it, and they matter more than the theorem:**

1. **About your manuscript.** The long spider used in `thm:cf-spider-lower` has
   `S_ε = ∅` for α ≤ 2⁻⁸ — the all-zero vector is a valid output at `W = 0`.
   If that holds up, the theorem lower-bounds the cost of satisfying the
   *certificate*, not the cost of solving the problem. **Worth verifying before
   the paper goes out.**
2. **I2-D's `log(1/α)` is a stopping-rule artifact**: under a semantic stop
   `N·√α` is flat (1.375→1.348); under the certificate stop it grows
   (2.625→4.574).
3. Eliminating the star's center solves it exactly in `O(1/ε)`, beating every
   R± member by `1/√α`. So R± is a *class* theorem, not a barrier — I4-D's
   `O~(1/ε)` target is untouched by it.

## 4.4 The certificate, characterized exactly — decision-ready (I4-F)

This bears directly on your open `docs/decisions/residual-convention.md`.

**The rule is not carelessly loose.** `M := D^{-1/2}Q^{-1}D^{1/2} ≥ 0` with
every row sum exactly `1/α`, so `‖M‖_∞ = 1/α` **exactly**: the `1/α` factor is
worst-case sharp and all slack is *residual-structural*.

**The sharp constant.** For a residual supported on `T`, the true amplification
is `A(T) = max_i π^(i)(T)` — the PPR mass a walk from `i` places on `T`. On the
infinite path with `|T| = 1` this equals **exactly √α**, which is the observed
law across families (`A/√α ∈ [0.71, 1.07]`).

**One-sidedness buys nothing** — refuted with a witness: the extremal residual
`r = θ·d·1_T` is itself nonnegative, so the monotone constant equals the signed
one. One-sidedness gives an envelope `π̂ ≤ π`, not a better constant. This also
explains why ACL is tight: a *threshold* stop leaves exactly that extremal
profile.

**How much of the program is certificate tax:**

| method class | tax (certified ÷ oracle) |
|---|---|
| push / APPR, ISTA / RPPR (threshold stops) | **1.00–2.16×** — nothing to recover |
| region / restricted-solve / AMG / elimination / Krylov | 1.15 → **2.54×**, growing as α falls |

I2-F's 2.0–6.1× lattice inflation, I3-A's up to 17.5× in 3-D, and the whole
certified-vs-oracle exponent gap are **this one object**. No push headline moves.

**Recommendation (two-tier).** Keep the current rule as Tier 0 for
threshold-stopped methods, where it is within 2× of optimal. Adopt as Tier 1,
for region and restricted-solve methods, a **profile-localized supersolution**
certificate: solve `(I − cP)Ĝ = |r|/d` on `B_K(supp r)` with a pessimistic
exterior — sound by M-matrix comparison, 0 violations in 648 adversarial
checks, α-free cost of 1.2–8× `vol(S_ε)`, and it hits the oracle radius exactly
in 9/9 cells at `K = ⌈4/√α⌉`. Implementation trap: use the *profile* version,
never the support version — round-off inflates `supp r` and drives the bound
back to 1. **A uniform √α relaxation is UNSOUND** (refuted by a high-degree ring,
and by push itself). Candidates (c) K-term Neumann and (d) max-principle were
both tested: Neumann needs `K = Θ~(1/α)` and is dead; max-principle gives ≤2×,
confirming I3-A.

## 4.5 Route B: face alignment helps, momentum calibration may close it (I4-A)

The recovered safety theorem is **correct and constructive**: for any `y > 0`,
`w := Q_S^{-1}y` automatically satisfies the positivity hypothesis, so exact
rational inverse iteration with a free Collatz–Wielandt bracket suffices — no
eigensolver, no error analysis. Safety verified over 23,100 exact flag checks,
0 violations. A corollary settles the regression for free: `Q·1 = α·d` means
face-aligned ≡ baseline **bit-exactly whenever S = V**, so the K_n theorem
survives by construction (17/17 re-verified).

Face-aligned capping takes the face contraction from **127/160 to 211/211**
(worst ratio 359 → 1.000000) and **halves** P24's inflation (`J_T` 17.89→8.60,
slope 0.1255→**0.0559**, P-stages 126→23). But **absorption still does not
fire**, and the cause is now isolated: on a proper face `α_S > α`, which makes
the face mode underdamped — momentum is calibrated to `α` while the face runs
at `α_S` (measured ratio 2.19–150.3).

**The closing probe is the most promising algorithmic lead in this round:**
face-calibrated momentum `β_S = (1−q_S)/(1+q_S)` — legal, since safety is
stage-local in β — gives **0 corrections on 5 of 6 cells** (2 on the sixth, both
at t ≤ 23), a **100% face floor on all six**, and is *faster* than baseline.
Measured, float.

The **`μ₂ ≥ 2q` class theorem** is verified on 82 exact instances (bipartite,
Q₃/Q₄, Petersen, rook, cocktail, cycles, circulant, ER, K_n): 17 of 20
predicates at 100% (1696/1696 each), absorption 64/64 in class, `B ≤ 0.34895`,
and the C16 ↔ `μ₂ ≥ 2q` equivalence holds 82/82 with sharp equality at the
threshold. One correction to I3-C: `λ₂` is right in the contraction constants,
but the *trigger* needs `λ_max`.

## 4.6 The composed solver: works, does not dominate (I4-B)

α-free (median exponent 0.03 vs push 0.96, WY 1.17), 372/372 certified, and the
only method never catastrophic on any family — but median **1.20×** (worst
5.78×) against the per-cell hindsight best, and push beats it 5.7–15.6× on
high-treewidth families wherever `1/(αε)` is small enough to run. Triage costs
1.7% of work and buys 1.2×–3170×; route flips happen in 24/84 cells, always
ELIM→AMG and never back, with ≤0.12% write-off. Full eleven-coordinate ledger
reported — `R_adj ≡ 0` in every composed run is the kinetic gate's signature.

**Honest negative:** the gate wins only 0.0–6.7% in this setting. I3-B's 266×
needs hubs that stay *unadmitted*, which ε-certified PPR does not produce — so
the gate's dramatic win is real but narrower than it first appeared.

---

# REVISED PRIORITIES (superseding §5)

**Tier 1**

1. **Verify the spider claim in `thm:cf-spider-lower`** (§4.3). It is a
   half-hour check and it affects a theorem in the active manuscript.
2. **Adopt the two-tier certificate** (§4.4). It closes your open
   residual-convention decision with a sound, α-free, decision-ready
   recommendation, and it retroactively removes a tax from every region-method
   bound in the program.
3. **Restate the program's target** as `O~(nnz(s) + vol(S_ε))` with α-free
   constants (§4.1) — *as a second target alongside FY22, not as a replacement*.
   FY22 remains tight for the R± class (§4.3); what §4.1 establishes is that
   output size can never justify it, so the interesting question is for which
   primitive classes output-linear work is reachable.
4. **Push VGF to SP3** (§4.2): frontier Schur / incremental factorization to
   kill the round-count exponent, plus the fan-trap band problem. If both fall,
   a single mechanism is output-bounded *and* α-free end-to-end — which would be
   the campaign's strongest possible outcome.

**Tier 2**

5. **Face-calibrated momentum** (§4.5) — the cheapest remaining shot at
   absorption on proper faces, and it is *faster* than baseline, not a tradeoff.
   Then prove `m_S ≤ 1−q_S²`.
6. **Publish the ladder** (§4.3): `M± = Θ(1/(αε))` → `R± = Θ(1/(√α·ε))` →
   elimination `Θ(1/ε)`, three classes on one instance, each row dropping one
   axiom. With I2-D this is now class-vs-class and is a complete short paper.
7. **Block one-hop relaxation** — the star's center-plus-leaves block escapes
   I4-C's coordinate lemma in `O(m)`, and the escape condition is local and
   computable. That is the formal bridge from the push/SOR world to local AMG.

**Tier 3**

8. The kinetic gate remains right, but adopt it for correctness and simplicity
   rather than for the 266× (§4.6).
9. Composed-solver polish (HSEG-LDL into the ELIM route; push as a third
   triage route) is worth ~3× and is not urgent.

---

# ITERATION 5 (2026-08-25, 6 directions)

Run at the user's request after the §4.1 corrections. Two questions closed, one
breakthrough, one manuscript answer, two deliverable packages.

## 5.1 The manuscript spider question — answered fairly (I5-A)

Exact threshold: `u_max = (√α/k)·(1+λ^{2L})/(1−λ^{2L})`, so `S_ε = ∅` iff
`√α·(1+ζ)/(1−ζ) < θ_sp`. In the theorem's regime every admissible dyadic α
gives an empty output set (θ=1/8: all α ≤ 2⁻⁷). **I4-C's diagnosis is also
corrected**: the Ω(1/(αε)) is *not* "about the certificate" — the certificate
is satisfiable at support radius 3 (vol 7k), and the manuscript's own ω=1 push
at τ=ε meets it with `W·αε → 0`. The bound isolates **the fixed-ω\* signed
FIFO dynamics specifically** — which is exactly what the theorem is used for
in the paper's argument, so the theorem's role survives. The wave lemma
verifies push-exactly (2.8e-15). A **pendant-seed repair** (degree-1 pendant
on the center, ε = γ_α, k = Θ(θ/α)) makes the zero output invalid, keeps the
triangular wave (constants perturbed ≤ 12%), and preserves `W·αε = 0.070–0.086`
flat. Recommended edit: one remark stating the closed form and the scoping;
optionally the pendant variant (which would need an inequality-form re-proof of
the wave lemma to adopt formally). Author-facing note:
`findings/i5a_manuscript_spider.md`.

## 5.2 Route B: the safeguard can be made to never fire (I5-C)

With BOTH fixes — the face-aligned cap (I4-A) and face-calibrated momentum
`β_t = (1−q_r)/(1+q_r)` calibrated to the **upper** Collatz–Wielandt end —
run in exact rational arithmetic: **0 corrections and 0 retractions in
2,550/2,550 exact stages across 9 proper-face cells**, including all pre-lock
face changes. On P24, `J_T = 0.000 exactly` (the float slope goes
0.12552 → 0.00000). Supporting lemmas: `α_S ≥ α` (Cauchy interlacing);
I4-A's claimed inequality was **sign-backwards** — the truth is
`m_S ≥ 1−q_S² ⟺ α_S ≥ α` (proved via an exact identity, 200/200), which is
the *overdamping* direction and dictates upper-end calibration. The face chain
is monotone (≤ |S\*| changes, proved), and re-tuning at face changes *releases*
potential (jump < 1 at all 85 downward re-tunes) — it telescopes. One honest
negative: "faster" is refuted — face-calibrated momentum is 25–60% slower to
fixed accuracy (weak early momentum delays lock); it wins only asymptotically.
K_n regression bit-identical.

**Route B now has a single named obstacle**: the *never-triggering lemma* —
prove the trial point stays a subsolution under face damping, making P-stages
vacuous. The face-C16 transplant provably does not work (fails on all six
cells), so this is the route.

## 5.3 The τ functional: one cap explains the whole mechanism map (I5-E)

Generalized cap (Proved-draft; 42/42 exact + 1,316 inexact-update checks, 0
violations): for any Φ-monotone update supported on a block U,

> `|Δz_v| ≤ 2·√(γ_α·π_v·τ_v(U))`,  `τ_v(U) = ((H_UU)^{-1})_vv`,

locally computable, with the exact identity `τ_v(V) = π_v/γ_α`. Consequences,
all verified: on the star, `W(B) = Θ((1/ε)·√(x(B)/α))` with
`x(B) = 1 − c²(B−1)/m` — **bounded blocks buy nothing** (any B ≤ m/2 still
pays `0.0083/(√α·ε)`); escape is a sharp phase transition at `B ≈ |S_ε|`. On
the path, blocks advance linearly and saturate at `b* ≈ 0.28/√α` — no block
bound exists there. **What forces block methods is volume (coverage of the
seed's reflecting boundary), not propagation distance.** The three-class
ladder becomes one statement with three τ regimes: coordinates (τ = 1),
bounded blocks (τ = Θ(1)), output-scale blocks (τ = π_v/γ_α, and the
α-dependence migrates into the block-solve price — which is exactly where
local AMG/elimination live, and why they are α-free per unit output).

## 5.4 The certificate radius law — closed both ways (I5-F)

- **Lower** (theorem, verified to 1e-13): the cycle `C_{2K+4}` is
  indistinguishable from the infinite path on `B_K(supp r)` plus degree
  queries, forcing `K ≥ artanh(1/C)/(2·artanh√α) − 2` for any sound C-tight
  local certification. Measured `K_min(C=2) = 0.25–0.27/√α`.
- **Upper**: a new *exact self-consistent exterior* (two solves + a scalar
  fixed point, sound) certifies factor 2 at `K = 0.25–0.30/√α` —
  minimax-optimal within ~20%. The earlier log(1/α) schedules are obsolete.

**Θ(1/√α) is necessary and sufficient.** Production implementation in
`lib/cert.py` (1,472 exact soundness checks, 0 violations). Tax-free
re-measurement: bound tightness improves from median 8.0× over-charge to 1.01;
the *work* gap closes off-lattice (1.6–1.8× → 1.2–1.3×) but on lattices a
generic certifier re-introduces the exponent because the certificate system is
itself 1/α-conditioned — the certifier must reuse the mechanism's own α-free
solver. The two-tier recommendation for `docs/decisions/residual-convention.md`
is finalized and paste-ready in `findings/i5f_cert_integration.md`.

## 5.5 VGF after SP3 (I5-B) — the honest state

The SP3 prediction was refuted in its stated form: incrementality does not kill
the round count (on path-likes, one admission's influence region is Θ(vol(S))
up to logs, so "stalled round = O(vol(new))" is impossible for exact-residual
methods). What works is certification: (e')-based early stopping collapses
endgame rounds and breaks the fan trap (region ×516 → ×9.9; work 103 → 5.6).
Median mechanism exponent: 0.256 → 0.156 (oracle 0.104). Next: (e')-first VGF
using I5-F's self-consistent certifier. Still no single mechanism with both
proved output-boundedness and end-to-end α-freeness — the gap is now entirely
in round count + certification scheduling.

## 5.6 The ladder package (I5-D) — ready for audit

745 lines, all three class theorems restated in the manuscript's z-scale with
a single verification script (45 cells × 13 checks, 0 failures). Consolidation
strengthened the results: a graph-free Theorem A′ (the Φ constant eliminated),
a new pathwise `‖r‖₁ ≤ 2√(α/(1+α))` cap extending Theorem B to output maps,
and two constant slips in earlier iterations found and fixed. Two Opens are
crisply stated (the general-graph O_B corollary; whether bounded-seed-degree
families can force the R± bound). `findings/i5d_ladder_paper.md`.

## Iteration-5 state of the campaign

Closed so far: information complexity (Θ(1/ε), it. 1–2); the boundary-scan
artifact + shell law (it. 3); the output-volume bound's role (it. 4,
corrected); the certificate sharp constant (it. 4) and radius law (it. 5);
K_n absorption (it. 2) and now empirically-exact never-firing on proper faces
(it. 5). Live: the never-triggering lemma (Route B's last obstacle), (e')-first
VGF, the heavy-tailed-ball solve-cost question (the last rung of the τ
ladder), and the R± bound's instance scope. Corrections cascade audit-style:
I4-C corrected by I5-A, I4-A's sign by I5-C, constant slips by I5-D — each
recorded in place.

---

# ITERATIONS 6–7: THE PROOF PUSH (2026-08-26)

Run at the user's request: "try your best to finish the proof." Eight agents
across two iterations, everything aimed at closing open proof links. Outcome:
**four theorems completed, one refutation that reshapes the target, and one
promotion-audit-ready document.**

## 6.1 The K_n absorption theorem is COMPLETE (I6-B)

The single open link (C9, V-contraction at genuinely partial correction
stages) is closed — and the investigation revealed the old certificate was
structurally broken (it fails 47 of 53 partial stages once you can generate
them; the published pulse's 0.979 margin was the *luckiest* case, not the
typical one). The repair: an exact clip identity plus a truncation-covariance
lemma `Var(ψ(v)) ≤ Cov(ψ(v), v)` closes C9 on K_n for all n, all q ≤ 1/2, any
cap value, **with no new hypothesis**. Final battery: 140 instances, 18/18
predicates, 0 failures. **The Route-B packing target holds on K_n for the
ORIGINAL recurrence with c = 1 and B ≤ 0.36918 < log 2, no open links.**

## 6.2 The never-triggering theorem: refuted as stated, completed as modified (I6-A1, I6-A2, I7-A)

Two independent iteration-6 routes each reached proved-except-one-step with
complementary machinery and a cleanly stated interface. The iteration-7
composition then did the honest thing: it **refuted the unmodified lemma** —
an exact counterexample (rt22b, a random tree on 22 vertices) fires at t = 13,
three stages after a face lock. The two "absorbable transients" iteration 6
had noticed were luck, not a pattern.

The completion is the modified algorithm **fm-w**: after every face change,
run J_S pure-proximal (β = 0) stages — each unconditionally fire-proof by the
new LCP comparison lemma P-A — and enable momentum only after an
exact-rational inertia gate passes (the (H-sep) condition, now *checked*
online rather than assumed). The warmup contraction identity
`μ⁺ = s₂/(1−q_r)²` shows warmup contracts the entrance certificate at twice
momentum's own log-rate, giving an explicit J_S. Result, verified exactly:

> **On fm-w, Δ_t = 0 at every stage of every run** — 3,840/3,840 stages over
> 19 cells including five adversarial short-segment cells; the previously
> firing K8 control is cured; rt22b's own lock face runs 228 momentum stages
> fire-free. No α restriction. Hence **J_T^fin = 0 exactly, and the Route-B
> packing target holds trivially with c = 1** — with the modification proved
> *necessary*, not merely convenient.

The honest cost (from iteration 5, unchanged): fm-variants are 25–60% slower
to fixed accuracy than the baseline, winning only asymptotically; and J_S is
large on near-critical faces (those run prox-only — safe but unaccelerated).
Never-triggering controls *inflation*, not total work — the end-to-end work
theorem still needs the outer iteration count assembled (sketched in the
theorem document).

## 6.3 The class theorem, closed via a new master form (I7-B)

The planned invariant TK ≥ 0 turned out to be the *wrong* one — proved
equivalent (over the reachable clip cone) to the (H-K) entrywise condition,
with exact negative witnesses on C6/Q4/Petersen, so no transport argument
could ever work. The replacement is cleaner: a **master form**
`V_{t+1} − (1−q)²·V_t = Ψ(y, h)`, making C9 equivalent to the stage-free
variational statement `sup Ψ ≤ 0` (**PSI**). Status: exact rational proofs on
C6, C8, Q3, and Petersen — the boundary cases q = μ₂/2 are *sharp*
(sup Ψ = 0, mixed-pattern extremals identified); Q4 decided completely by full
automorphism-orbit enumeration of all 3¹⁶ sign assignments; a 20-family
adversarial sweep finds (H-K) failing on 14 families and (PSI) holding on
every one, zero violations. **Theorem B''**: for connected G, q ≤ 1/2, (H0),
(Hgap), (PSI): C9 holds at every stage, absorption fires, J_T^fin ≤ B, c = 1.
What remains is analytic (PSI) in general — now a clean, isolated variational
problem with its extremal structure known.

## 6.4 The ladder is closed; the HSEG tree theorem is complete (I6-C, I6-D)

- **Φ = 1 proved** by a five-line maximum principle (max_u π_u/d_u is attained
  at the seed — an off-seed maximum would force max u ≤ c_α·max u). The
  general-graph monotone corollary is now constant-free, and the proof pass
  found and recorded an erratum in an earlier display (ratio, not product).
- **The scope theorem** replaces the second Open: the R± lower envelope is
  `max(vol(S_ε), T_seed, T_bulk)`, and on every bounded-degree family it is
  o(1/(√α·ε)) — **the √α-coupling is a d_v·√π_v = Ω(1/ε) phenomenon**
  (high-degree-with-mass seeds), which is sharper than "self-return". One
  narrower successor question remains (a √(1/ε) member-vs-envelope window on
  bounded-degree cycles). Extended verifier: 630 cell-checks, 0 failures.
- **HSEG-LDL amortization proved** with the potential
  Φ = Σ_light max(0, 2·sz(c) − sz(h)); hysteresis factor 2 is exactly the
  self-amortizing constant; total re-carve O(n·log²n), α-free. The thrash
  adversary validates rather than falsifies (and shows per-op Θ(n) is real, so
  amortization is genuinely needed). A real bookkeeping hole in the shipped
  code was found and repaired along the way. **Complete tree theorem**: on any
  tree, any admission order, total charged work O((nnz(s)+vol(S))·log²·) with
  α-free constants, certified — and trees escape the Θ(1/√α) certification
  radius at tightness C ≥ 2, so the theorem is α-free end-to-end.

## 6.5 The assembled document (I7-C)

`findings/i7c_routeB_theorem.md` is the promotion-candidate write-up: the
executive statement in the repository's own vocabulary (everything labeled
Proved-draft = unaudited; enters the ladder as Conditional), fm-w pseudocode
with every certified quantity, the fifteen-theorem chain T0–T15 with
hypotheses, statuses, verification counts, and file pointers, the
program-impact section (which of the repository's open items this addresses:
the Route-B queue, the windowed spectral split, the K₂/K₈ STOP families — all
explained or absorbed), and a single driver `i7c/verify_routeB.py` that
re-verifies the composed chain end-to-end in 109.5 s: **all gated exact checks
pass**. One subtle consistency point was reconciled machine-verifiably: the
apparent I5-C/I7-A contradiction about re-tune direction is two names for the
same monotone event (q_r nonincreasing ⟺ β nondecreasing).

Audit anchors, in order: the rt22b counterexample; Petersen at q = 1/3 and C6
at q = 1/4 (the sharp (PSI) boundaries); the S16 inertia-gate rejection; the
K8 pulse.

## Where this leaves the campaign

Fully closed (campaign standard — Proved-draft, exactly verified, no open
links): K_n absorption; fm-w never-triggering (with necessity); the HSEG tree
theorem; the three-class ladder including both former Opens; the
monotone/signed separation; the certificate sharp constant and radius law;
spider information complexity. Open and cleanly isolated: analytic (PSI);
sharp entrance propagation (J_S → O(1)); inexact inner solves; finite
precision; the end-to-end work-ledger assembly; the bounded-degree window;
non-tree incremental factorization.
