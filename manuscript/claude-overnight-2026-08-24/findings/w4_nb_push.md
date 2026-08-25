# W4 — Nonbacktracking / directed-edge residual propagation as the accelerated tail (EES)

Code: `/home/claude/work/overnight/w4_nb_push/` (`ees.py`, `validate.py`, `run_spider.py`,
`run_spider2.py`, `run_cycles.py`, `run_crossover.py`; raw JSON: `spider_results.json`,
`spider_g_results.json`, `cycles_results.json`, `crossover_results.json`).
System/conventions: `H z = γ e_v`, `H = I − c A D^{-1}`, `c=(1−α)/(1+α)`, `γ=2α/(1+α)`,
z in π scale; certificate `max_u |r_u|/d_u < γ·eps` ⇔ `Model.cert_resid < α·eps` ⇒ semantic err ≤ eps.

## VERDICT

The nonbacktracking mechanism, made exact, **is** Gaussian elimination on the explored
region: the correct directed-edge forwarding weight is the impedance ratio
`(c/d_u)/D(u→v)`, computable only leaf-inward. Realized as EXPLORE–ELIMINATE–SUBSTITUTE
(EES), it (Measured) removes the spider obstruction: charged-work exponent **0.50 in
1/α** (one-shot variant EES-G; 0.71 for the robust doubling variant = 0.5 + log
artifact) versus **0.94 → 1 for FIFO-ω\* SOR**, with an absolute crossover at
α ≈ 2⁻¹⁴·⁵ and EES-G exactly linear in explored volume (≈ 9.0 charged units per
vol unit). Trees are solved exactly in one two-pass sweep (machine precision;
Proved-draft below). Cycles degrade through the **≤2-irreducible kernel** m of the
explored region (m ≤ 2β−2, β = first Betti number): work ≈ vol + Σ m³, measured
cubic (slope 3.06–3.33 in β) when the region is *closed* (min degree 3), yet m = 0 —
work ~ vol — on *open* high-β bands (ladders). Smallest failing family: closed
3-regular regions (prism / `double_cycle`), losing to SOR at **every** tested α
(ratio 7–866, growing ~α^{−1/2}); grids are catastrophic (ratio up to 1.2·10⁵).
Correctness (certificate + semantic error vs `Model.solve_exact`) held in **every**
run, including all failures.

## 1. Derivation (Proved-draft)

Row u of `H z = f`: `z_u − c Σ_{w~u} z_w/d_w = f_u` (entry for column w is `−c/d_w`).
Root a tree anywhere; eliminate leaf-to-root. For directed edge (u→p) define the
**impedance (pivot)** and **transfer**:

    D(u→p) = 1 − Σ_{x~u, x≠p} T(x→u),      T(x→u) = (c² / (d_x d_u)) / D(x→u),

with RHS message `φ(x→u) = (c/d_x)·Φ_x / D(x→u)`, `Φ_x = f_x + Σ_{y~x,y≠u} φ(y→x)`.
Back-substitution: `z_u = (Φ_u + (c/d_u)·... )` in reverse order — root-to-leaf wave.
Two passes, O(1) work per edge ⇒ **O(vol) exact tree solve** (Thomas generalization).

*Pivot positivity (induction):* leaf D = 1; if every child satisfies
`D(x→u) ≥ 1 − c²(1 − 1/d_x)` then `d_x·D(x→u) ≥ d_x(1−c²) + c² ≥ 1`, so each
`T(x→u) ≤ c²/d_u` and `D(u→p) ≥ 1 − c²(1 − 1/d_u) ≥ 1 − c² = 4α/(1+α)² > 0`.
Elimination is exact and stable; verified at machine precision (err ≤ 9·10⁻¹⁶ across
path/spider/binary-tree/caterpillar/star, both α = 0.25 and 2⁻⁸).

*Path fixed point = project kernel:* interior degree-2 chain gives
`D = 1 − (c²/4)/D` ⇒ `D∞ = (1+√α)²/(2(1+α))`, forwarded fraction
`(c/2)/D∞ = (1−√α)/(1+√α) = λ` — exactly the known kernel. The naive push weight
`c/d_v` backtracks; the correct nonbacktracking weight is the impedance ratio, which
depends on the whole subtree beyond the edge ⇒ not known a priori mid-graph ⇒
**two-phase design (a)** is the natural realization.

*Design (b), fixed-weight one-wave NB iteration (Open):* any fixed forward weight
(e.g. λ) is exact only on infinite degree-2 interiors; leaves/junctions change D by
O(1), and the upstream z-corrections are precisely the back-substitution wave. A
single-wave fixed-weight scheme cannot be exact on finite trees; the two-wave
asynchronous version *is* (a). Not run experimentally.

## 2. Algorithm EES (implemented, `ees.py`)

Maintain global invariant `r = γ e_v − H z` (sparse). Round: (EXPLORE) multi-source
BFS from violating vertices `|r_u| ≥ γ·eps·d_u`, gated by optimistic path-worst-case
decay ρ → λρ, admission `ρ ≥ γ·eps·d_w`; depth capped by a per-round doubling `R_cap`
(robust variant) or uncapped (**EES-G**, one-shot). (ELIMINATE) Gaussian elimination
of `H[S,S]δ = r[S]` with degree-≤2-first greedy ordering: peels pendant forest
(Thomas) *and* contracts degree-2 chains of the 2-core into effective edges
(self-loops fold into diagonals — pure cycles and thetas eliminate completely);
the ≤2-irreducible junction kernel (min degree ≥ 3, size m ≤ 2β−2) is solved densely.
(SUBSTITUTE) reverse-order back-substitution; `z += δ`, `r[S] = 0`, boundary pushback
`r_w += c δ_u/d_u`. Under-exploration is *safe*: termination is certificate-driven.

**Charging (honest, as implemented):** scan(u)=d_u per vertex of S per round
(repeats → R_adj: the re-elimination cost of doubling); resp ≈ 3–7 per eliminated
vertex + **resp(m³)** and mat(m²) per dense kernel solve; rec per coefficient
write / backsub op / BFS test / pushback. SOR baseline: scan(u) per push.

**Correctness (Measured):** 14 zoo graphs × {α=0.2, 2⁻⁶} × {eps=1e-3, 1e-6}:
0 failures for both EES and SOR (cert < α·eps and semantic err ≤ eps everywhere;
EES err typically ≤ 10⁻¹⁶ once S covers the support).

## 3. Spider (k = 1/(4·eps) arms, L = round(2/√α)) — Measured

eps = 2⁻⁷ (k = 32); charged totals (meter.total):

| α | L | n | EES (doubling) | EES-G | FIFO-SOR ω* | k·L | 1/(αε) |
|---|---|---|---|---|---|---|---|
| 2⁻⁴ | 8 | 257 | 2 147 | 4 419 | 192 | 256 | 2 048 |
| 2⁻⁶ | 16 | 513 | 4 742 | 9 027 | 672 | 512 | 8 192 |
| 2⁻⁸ | 32 | 1 025 | 12 585 | 18 243 | 2 496 | 1 024 | 32 768 |
| 2⁻¹⁰ | 64 | 2 049 | 42 495 | 36 675 | 8 832 | 2 048 | 131 072 |
| 2⁻¹² | 128 | 4 097 | 94 455 | 73 539 | 33 120 | 4 096 | 524 288 |
| 2⁻¹⁴ | 256 | 8 193 | — | 147 267 | 128 160 | 8 192 | 2.1e6 |
| 2⁻¹⁶ | 512 | 16 385 | — | 294 723 | 509 792 | 16 384 | 8.4e6 |
| 2⁻¹⁸ | 1024 | 32 769 | — | 589 635 | 2 022 080 | 32 768 | 3.4e7 |

(eps = 2⁻⁵, k=8 sweep gives identical exponents; see JSON.)

**Fitted exponents, work ~ (1/α)^s at fixed eps:**
- FIFO-SOR: s = 0.937 (all) / 0.942 (tail) → 1; normalized SOR·α·eps ∈ [0.06, 0.09]
  ⇒ **Θ(1/(α·eps)) reproduced** (the project's triangular-blowup obstruction).
- EES doubling: s = 0.693/0.711 — i.e. 0.5 plus the measured log(diam) re-elimination
  factor (rounds 1→6; R_adj ≈ 3×C_adj at α=2⁻¹²).
- **EES-G: s = 0.509 (all) / 0.504 (tail); work/vol(S) = 8.97–9.0 constant, one
  round** ⇒ clean product scale **O(vol(S)) = O(1/(√α·eps))**.
- Locality: at eps=2⁻⁵, |S| = 705 of n=1025 (support-truncated, arms cut at the
  decay radius).
- **Absolute crossover** (eps=2⁻⁷): SOR/EES-G = 0.45, 0.87, 1.73, 3.43 at
  α = 2⁻¹², 2⁻¹⁴, 2⁻¹⁶, 2⁻¹⁸ — crossover at **α ≈ 2⁻¹⁴·⁵**, ratio then doubling per
  two octaves (the √(1/α) separation). Below that, SOR's tiny per-push constant wins.

## 4. Cycles — degradation law (Measured)

α-sweeps at eps=1e-3 (sizes ∝ 1/√α; EES = doubling variant; ratio = EES/SOR):

| family | α=2⁻⁴ | 2⁻⁶ | 2⁻⁸ | 2⁻¹⁰ | 2⁻¹² |
|---|---|---|---|---|---|
| theta(≈1.5/√α) ratio | 2.66 | 1.99 | **0.75** | **0.44** | **0.24** |
| cycle(≈3/√α) ratio | 2.26 | 0.97 | **0.63** | **0.37** | **0.20** |
| double_cycle(≈1.5/√α+2) ratio | 178.7 | 148.6 | 241.6 | 443.4 | 866.4 |
| grid(16,16) ratio | 700 | 6 592 | 4 023 | 558 | 201 |

- **theta, cycle:** chain contraction reduces the whole 2-core (kernel m = 0; hubs
  fold via parallel effective edges, cycles via self-loops). Work ~ vol; EES beats
  SOR for α ≤ 2⁻⁸ and the advantage grows like the spider's.
- **Closed prisms** (whole 3-regular graph explored, no degree-≤2 entry): kernel
  m = |S| = 2β−2 exactly. At α=2⁻⁸: work vs β over t ∈ {6,10,16,26}
  (β = 13,21,33,53): log-log slope **3.08**; work/core³ = 0.93–0.99 ⇒ work ≈ m³ ≈ 8β³.
- **Open bands — β is not the governing parameter:** double_cycle(40), α=2⁻⁸: the
  support is an open 148-vertex ladder band with β(S) = 72, yet the ≤2-peel sweeps
  it entirely (bandwidth-2 elimination): kernel m = 0, EES total 6 576, ratio 1.43.
  The honest law is **work ≈ C·vol·rounds + Σ m³ with m = ≤2-irreducible kernel**,
  m ≤ 2β−2 but often ≪ (closedness/treewidth, not β, decides).
- **Grids:** kernel ≈ β^0.94, work slope 3.33 in β; worst measured ratio 1.2·10⁵
  (grid(24,24), α=2⁻⁸, EES 9.2·10⁸ vs SOR 7 695). rand_reg(2000,3): kernel = n ⇒
  charged 8.0·10⁹. Certificates still hold in every failing run.

**Smallest failure:** closed 3-regular region — `double_cycle` — loses to SOR at
*every* tested α (min ratio 7.25 at n=24), ratio growing ~α^{−1/2}; the smallest
failing single config in absolute charge is grid(16,16) at α=2⁻⁴, eps=1e-3
(|S|=56, β=39, kernel 46 ⇒ 2.6·10⁵ vs SOR 372).

## 5. Charging caveats

1. Dense kernel charged m³ (what is implemented/executed). A treewidth-aware core
   solver would charge O(m) on prism bands (bandwidth 4) and O(m^{3/2}) (nested
   dissection) on grids — prisms are plausibly rescuable to product scale; grids
   improve to ~r³ ~ α^{−3/2} at fixed eps, still ω(vol): grids likely fail any
   elimination-style product-scale claim (Open).
2. The doubling variant's log factor is real re-elimination (R_adj); EES-G removes
   it, but its λ-gate is path-tuned: on graphs whose support is a strict sub-ball
   with faster-than-λ decay it can over-explore (audit on binary_tree(12) and
   rand_reg showed no overshoot only because supports were global at tested eps —
   worst-case overshoot on branching graphs is unbounded in principle; Open).
3. Per-vol constants: EES-G ≈ 9 charged units/vol vs SOR ≈ 1/push — ~4× intrinsic
   gap from two-pass messages + certificates; crossover α ≈ 2⁻¹⁴·⁵ could move to
   ≈ 2⁻¹²–2⁻¹³ with incremental factor reuse, not further without changing the meter.
4. One round of EES re-solves all of S; incremental (frontier-appended) elimination
   with truncated back-substitution is the obvious next engineering step (Open).

## 6. Next falsifiable target

**"EES with a treewidth-aware kernel solver achieves the product scale
O~(vol(S) + 1/(√α·eps)) on every explored region whose ≤2-irreducible kernel has
bandwidth O(polylog); the closed-prism family is rescued (banded core ⇒ work ~ vol),
while grid(w,w) with w ≥ 3/√α remains ω(vol + 1/(√α·eps)) under any elimination
ordering (separator lower bound ~r³ flops ~ α^{−3/2} at fixed eps)."**
Secondary: quantify EES-G's λ-gate overshoot on deep branching trees with
sub-support eps (binary_tree(depth ≥ 20), eps near γ·λ^{depth/2}).
