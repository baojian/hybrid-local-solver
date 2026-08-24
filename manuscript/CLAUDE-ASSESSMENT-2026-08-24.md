# Assessment of the problem definition, current progress, and candidate working directions

**Date:** 2026-08-24.
**Prepared from:** the active manuscript (`main.tex` and all section files), the
shared problem definition and ledgers under `notes/_shared/`, all eighteen
direction `STATUS.md` cards, coordination rounds 023–027, `registry.toml`, and
the project literature notes (ACL06, FRS+19, FY22, MWP23, Che+23, ZSB+24,
HLX+25, FM26, WY26).
**Status of this document:** external review and planning aid. Nothing here is
proof authority; every mathematical claim below that is not attributed to a
repository proof or a source paper is marked as a *suggestion* or *heuristic*
and must be verified before use.

---

## 1. What the project is, in one paragraph

The repository pursues the Fountoulakis–Yang open problem in a sharpened,
fully-charged form: given adjacency-list access, a sparse seed, `alpha`, and a
degree-normalized solution accuracy `eps_ppr`, return a sparse PPR
approximation with every unit of work charged (discovery, repeated reads,
numerical operations, response updates, certificate queries, output), at the
aspirational graph-uniform scale `O_tilde(1/(sqrt(alpha) * eps_ppr))` — or
show that a precisely defined computational restriction forbids it. The active
manuscript currently proves *tightness and obstruction* results (APPR is
`Theta(1/(alpha*eps_appr))` even on a star for every legal ordering; batch and
coordinate RPPR ISTA are exactly characterized; the CF-Push/SOR hybrid is
blocked at `Omega(1/(alpha*eps_ppr))` by a long spider). The notes program
(18 directions, 27 reviewed rounds) has built a large body of scoped positive
machinery, exact counterexamples, and a disciplined refuted-routes ledger, but
no graph-uniform accelerated end-to-end theorem yet — consistent with the
project's own promotion gates.

---

## 2. Assessment of the problem definition

### 2.1 What the definition gets right

**The semantic target is the correct invariant.** Fixing the output notion as
`max_i |pi_hat_i - pi_i| / d_i <= eps_ppr` — rather than any algorithm's
internal threshold — is what makes cross-algorithm comparison meaningful. Most
of the historical confusion in this literature (push thresholds vs objective
gaps vs KKT residuals vs proximal fixed-point residuals) is dissolved by the
repository's namespace discipline (`eps_appr`, `eps_obj`, `eps_pg`,
`eps_kkt`, `rho`, `delta` all kept distinct). This is genuinely unusual rigor
and should be preserved verbatim in any publication.

**The fully charged ledger is the substantive contribution of the framing.**
The eleven-coordinate resource vector
`(C_adj, R_adj, R_int, C_pre, C_ctl, C_rec, C_resp, M_pers, M_tmp, C_mat,
C_emit)` and the theorem-acceptance checklist close exactly the loopholes that
make "accelerated local" claims slippery: uncharged burn-in, free response
state, oracle-supplied supports, and repeated-prefix work hidden in iteration
counts. The audits of ASPR (repeated restricted solves) and of the literal
AESP inner loop show the ledger has real discriminating power. In my view the
charged-work model is publishable in its own right (see D16).

**Source-aligned parameterization.** Pinning the lazy `alpha` convention with
an explicit conversion obligation (the dictionary in the open-problem note,
Section 11) prevents silent `alpha <-> 2*alpha/(1+alpha)` drift between
ZSB+24 / HLX+25 / WY26 conventions. Good.

**The RPPR surrogate is used honestly.** `rho` is never silently identified
with `eps_ppr`; the Round-022 contract fixes an explicit conversion
(`rho = tau = eps_ppr/2` through the safe-lower-point bridge). Good.

### 2.2 Gaps and tensions worth resolving

**(a) The live parameter regime should be stated explicitly.** With WY26's
`O_tilde(1/eps^2)` (whp, ACL namespace, polylog in `1/alpha`) alongside
APPR's `O(1/(alpha*eps))`, the known upper envelope is
`O_tilde(min{1/eps^2, 1/(alpha*eps)})`. Comparing with the target
`1/(sqrt(alpha)*eps)`:

- against APPR, the target is smaller for every `alpha <= 1`;
- against WY26, the target is smaller exactly when `eps < sqrt(alpha)`.

So the target scale is *already achieved or beaten* (randomized, ACL
namespace, modulo the repository's own charging audit of WY26) whenever
`eps_ppr >= sqrt(alpha)`, and the genuinely open wedge is the deep-accuracy
regime `eps_ppr < sqrt(alpha)`. This wedge has a nice geometric meaning: the
diffusion length `1/sqrt(alpha)` is then *smaller* than the support scale
`1/eps_ppr`, i.e. the output region is many decay-lengths wide — precisely the
regime the spider construction lives in. I recommend adding a small
`(alpha, eps)` regime map to the shared problem definition and restating the
open target as regime-scoped. This also disciplines lower-bound work: WY26
already rules out uniform `Omega(1/(sqrt(alpha)*eps))` statements, so any
lower bound must be posed inside the wedge or against a restricted class.

**(b) Certified vs semantic output should be two named tasks.** The
definition demands the semantic error but the Round-022 contract additionally
demands one terminal certificate, and the sufficient certificate
`||D^(-1/2)(Q x_hat - b)||_inf < alpha*eps_ppr` is *sufficient, not
necessary*. The oracle-hierarchy counteralgorithms (five-site degree-four
polynomial; singleton-basis synthesis) exploit exactly this gap: the
certificate task can be strictly easier than the literal Galerkin trace, and
the semantic task can in principle be easier than any certificate-driven
stopping rule. Since the lower-bound program already distinguishes these,
naming them (`PPR-cert` vs `PPR-sem`) in the shared definition would prevent
future scope accidents.

**(c) The randomness policy is stated but not exercised.** The problem
definition admits randomized algorithms with stated success probability and
charged rebuilds, yet the frozen Round-022 acceptance contract is
deterministic exact-real, and essentially the entire notes program is
deterministic. Meanwhile the strongest recent external progress (WY26) is
randomized, and the most plausible fast routes (incremental SDD, sketching,
sampled cleanup, randomized coordinate acceleration) are inherently
randomized. I recommend a two-tier target: Tier A deterministic exact-real
(current contract), Tier B randomized-whp with all randomness-dependent
rebuilds charged. Progress on Tier B should be a first-class outcome, not a
consolation prize.

**(d) Precision debt is scoped out but will return.** Exact-real/algebraic
cells are the right setting for the current counterexample work, but two of
the three live frontiers (response maintenance; SDD-based solves) are exactly
the places where finite precision bites hardest. A short standing note in the
problem definition — "which claimed results would survive fixed-point / floating
error, and which are known to be exact-cell only" — would prevent a future
unpleasant surprise at paper time. (Several STATUS cards already carry this
flag; it is not yet centralized.)

**(e) Small nits.** Parameter-range patchwork across notes (`alpha < 1/4`,
`< 1/2`, `<= 1`, `eps <= 1/16`, …) is handled correctly but a single table in
the shared definition would help. The `nnz(s)` input term is handled well.
The output lower bound `Omega(1/eps_ppr)` listed coordinates is proved and
should be quoted next to the aspirational scale so the target reads as
"output size × per-unit revisit cost `1/sqrt(alpha)`".

**Verdict.** The problem definition is sound, unusually careful, and — with
the regime map, the two-task split, and the two-tier randomness policy —
would be fully airtight. None of the gaps above invalidates existing work.

---

## 3. Assessment of current progress

### 3.1 The active manuscript

The manuscript proves a coherent, self-contained set of results:

1. **APPR tightness** (`Theta(1/(alpha*eps_appr))`, ordering-independent,
   center-seeded star), with the two mechanisms cleanly separated
   (`Omega(1/alpha)` processed mass; constant fraction through a
   `Theta(1/eps)`-degree center), plus the exact lazy path kernel showing why
   stars, not paths, are the clean witness.
2. **RPPR ISTA characterization**: removal of `log(1/alpha)` from the
   published batch bound; `Theta((1/(alpha*rho))(1 + log(1/(delta*rho))))`
   for general seeds via the direct-sum instance; star-tight
   `Theta((1/(alpha*rho))(1 + log(1/delta)))` for single seeds; a
   residual-thresholded coordinate method and a coordinate-to-batch hybrid
   with exact `Theta(1/(alpha*rho))` at fixed relative accuracy — the
   project's "first fully matched local hybrid result".
3. **CF-Push two-stage analysis**: Phase-I coarse push is
   ordering-independently tight at `Theta(1/(alpha*tau))` (as
   `alpha -> 0`), `tau = eps/sqrt(alpha)` is the unique balancing power-law
   exponent, the handoff certificate is exact, Phase-II
   converges unconditionally — and the long spider forces
   `Omega(1/(alpha*eps_ppr))` for the fixed-relaxation FIFO tail, killing the
   hoped-for uniform square-root bound *for that implementation* and
   correctly identifying what must change (tail mechanism, not handoff
   scale).

This is honest, tight, and well-scoped work. Two observations. First, the
paper as it stands is a *tightness-and-obstructions* paper: every headline
result is a matched bound or a negative result; there is no accelerated
positive theorem. That is a perfectly publishable shape (and the spider
mechanism is genuinely instructive), but the framing should own it. Second,
the experiments section covers only the APPR star validation; the RPPR and
CF-Push claims have no reported runs yet, and the conclusion's design
alternatives (nonbacktracking state, elimination on explored regions, varying
relaxation) are currently prose, not measurements. See D14 and D18.

### 3.2 The notes program

The scale is unusual: 18 registered directions across five tracks, 27
controller-reviewed rounds with independent audits and exact rational
checkers, a shared results ledger, and a refuted-routes table. My reading of
the assets, grouped by kind:

**Proved positive machinery (reusable):**
- Safe-support gates and the `1/rho` peak-volume invariant
  (`volume_gated_acceleration`); safe lower retraction, fixed-envelope
  locality, terminal gate and RPPR→PPR bridge, cached-row mechanics, and the
  unconditional `alpha >= 1/4` fallback (`aesp_cd_l1_rppr`).
- The Round-024 **high-Dirichlet promised-class theorem**: if the optimal
  face satisfies `theta_A >= c0*q`, direct resolvent contraction delivers the
  gate and the full charged vector — the blocker is genuinely confined to
  low-Dirichlet faces. This is a real structural narrowing, not bookkeeping.
- Persistent-row L1/square-energy banks, truncation-energy bounds, and the
  lagged Euclidean reserve (Rounds 026–027) — exact, actual-finite, and
  correctly scoped as *not yet* an accelerated rate.
- Structured response solvers with complete charged ledgers: paths, trees,
  cycles, bounded blocks, equitable quotients (`delayed_reflection_ladder`);
  three-arm spider and double-Y token countdowns, caterpillar
  `O(m log m)` delta reporters (`adaptive_revisit_control`); fixed-attachment
  cycle reporter `FACR(p)` (`two_rung_direct_theory`); settlement calculus and
  trace-legality machinery (`propagate_settle_framework`); block-Schur
  correction and path `LDL^T` gates (`incremental_active_set_sdd`).
- Trajectory-dependent AESP–LOCSOR handoff theorem with the explicitly
  conditional `Lambda_J` promotion gate (`hybrid_aesp_locsor`).

**Proved lower bounds and obstructions (scoped):**
- Literal AESP+batched-LocGD is `Omega(1/(sqrt(alpha)*eps_ppr))` on a
  center-seeded star — i.e. the flagship accelerated framework is already
  *at* product scale on the simplest instance, so any improvement must come
  from transient-volume separations, not star geometry
  (`aesp_locgd_star_lower_bound`).
- Literal ASPR pays `Omega(|S*|^2/sqrt(alpha))` restricted-solve work — the
  repeated-prefix factor is real (`aspr23_bound_audit`).
- The literal measured two-rung policy fails graph-uniform acceleration on a
  three-vertex path (`two_rung_direct_theory`); the FIFO SOR spider bound in
  the manuscript; the output lower bound `Omega(1/eps)`; the exact-CG
  endpoint-path calibration (`Theta(n^2)` literal ledger).
- The oracle-hierarchy counteralgorithm pair (constant-work five-site
  certificate; linear-work singleton-basis synthesis) showing that natural
  "recurrence" classes are defeated by slack spreading and delayed synthesis
  — a hard-won negative meta-result about lower-bound model design.
- The refuted-routes ledger (30+ closed shortcuts). This is institutional
  memory most projects never build; it is worth its weight in avoided
  re-derivation.

**Conditional frames awaiting one named lemma each:**
- `Lambda_J = O(1/eps)` early-locality gate (AESP–LOCSOR end-to-end).
- The actual-finite net exponent `J_T^fin <= (1-c)qT + B` on low-Dirichlet
  faces (Route B; after Rounds 026–027 restricted to windowed / spectrally
  split / nonlinear-transfer Lyapunovs).
- All-history causal solvency for volume-gated acceleration.
- The expanding-face estimate-sequence lemma (ASPR successor).
- Width-`w` ordering assumptions for the general resolution theorem.

**Measured artifacts:** the 24-cell SOR campaign family (`B = 2.5` two-rung
best tested at 60.7M charged ops), preserved with correct provenance and
without promotion.

### 3.3 Honest meta-assessment

**Strengths.** Claim discipline is exemplary; the controller/audit loop
catches real errors (Round 027's two hard index repairs); nothing in the
shared ledger looks over-claimed to me. The problem has been decomposed into
three sharply named frontier interfaces, each with an explicit falsifiable
next target. The negative knowledge is dense enough that a newcomer can be
productive without stepping on a mine.

**Concerns.**

1. **Narrowing risk.** The AESP-CD Lyapunov line (Rounds 022–027) is now
   optimizing against specific exact families (`K_2` low mode, `K_8`
   high-band pulse) with rational constants like `14641/32256`. Each round
   closes one proof template at significant cost, and the surviving template
   space ("windowed spectrally split nonlinear-transfer differently
   normalized …") is shrinking toward the empty set *for this proof style*.
   That pattern usually means either the statement is false for the literal
   recurrence (and a real counterexample family exists), or the right proof
   lives at a different granularity (windowed/amortized over `Theta(1/q)`
   stages, or in expectation over randomized steps) where per-step adversarial
   families lose their force. I recommend a cap-and-review: fix a budget of
   1–2 more rounds for the current template class, then force a granularity
   switch (see D8, D2).

2. **Portfolio imbalance.** Nearly all effort is deterministic, worst-case,
   per-trajectory. Missing or barely touched mechanism families:
   randomization (sampled cleanup, sketching, randomized coordinate
   acceleration), nonbacktracking/directed-edge state (named in the
   manuscript's own conclusion but owned by no note), `alpha`- or
   `rho`-continuation/homotopy, bidirectional (forward+reverse) estimators,
   and the dynamic-Laplacian/incremental-solver literature as a source of
   response primitives. Several of these are exactly shaped for the three
   frontier interfaces (see Tier 1 below).

3. **The upper-bound center of gravity may be in the response track.** WY26's
   own remark — warm-starting the nested SDD solves could plausibly reach
   `O_tilde(1/eps)` — points at `incremental_active_set_sdd`, currently one of
   the *thinnest* directions (11 files, no incoming dependency edges).
   Note that `O_tilde(1/eps * polylog(1/alpha))`, if achievable, is *stronger
   than the project's target everywhere* (since `1/eps <= 1/(sqrt(alpha)*eps)`),
   and would resolve the FY22 question in its strongest form. Even a
   conditional or structured-graph version of that statement would leapfrog
   the current Route-B battle. The project's response machinery (Schur
   banks, transfer trees, FACR, settlement) is exactly the deterministic
   substrate for this; what is missing is engagement with randomized
   incremental sparsified-Cholesky/Schur techniques.

4. **Synthesis lag.** `hybrid_local_solver_synthesis` and several STATUS
   cards predate Rounds 025–027; the manuscript's conclusion does not yet
   cite the AESP-LocGD star lower bound or the WY26 boundary, both of which
   materially reframe "what would count as progress". A synthesis refresh
   pass is cheap and overdue.

5. **Publication risk.** The tightness results (star APPR bound, ISTA
   log-removal, coordinate `Theta(1/(alpha*rho))`, spider obstruction) are
   individually findable by others — the area is moving fast (WY26 appeared
   2026-08-17). Sitting on a finished obstructions paper while the notes
   program hunts the big theorem has real priority risk.

---

## 4. Candidate working directions

Directions are grouped in four tiers. Each entry gives the question, why now,
a concrete first step, and a kill criterion, in the repository's own idiom.
Tags: [UB] upper bound, [LB] lower bound, [S] structural/conditional,
[E] empirical, [P] publication/infrastructure. Confidence marks:
(checked) = consistent with repository proofs/ledgers as read;
(heuristic) = my suggestion, verify before relying on it.

### Tier 1 — high-leverage, concrete, under-explored

**D1. Warm-started incremental active-set solver: attack `O_tilde(1/eps^2) -> O_tilde(1/(sqrt(alpha)*eps))`, stretch `O_tilde(1/eps)`.** [UB]
*Question.* Can the WY26 active-set loop reuse solver state across its
`<= 2/eps` expansions so that total charged work is near the *final* volume
rather than (number of expansions) × (per-solve volume)?
*Why now.* This is the strongest known upper-bound frontier; WY26 explicitly
flag it; `incremental_active_set_sdd` already owns the deterministic
path-case and the conditional interface (`thm:conditional-interface`), and
`response_preconditioned_hybrid` owns the Schur/refresh machinery. The
missing ingredient is randomized incremental solver technology
(sparsified Cholesky / approximate Schur maintenance under vertex
insertions), which the repository has not yet imported. (checked, except the
external-literature fit, which is heuristic)
*First step.* Literature intake note on incremental/dynamic SDD solving and
approximate Schur sparsifiers; then a Tier-B (randomized, fully charged)
interface spec for `Violations/Expand/Finalize` with amortized
`polylog` per admitted volume unit; test first on trees (where exact transfer
trees already give it deterministically) and then on the caterpillar and
double-cycle families already in the repo.
*Kill criterion.* An OMv-style conditional hardness result for the
incremental boundary-reporting task (see D12), or a proof that any
`o(1/eps)`-amortized refresh forces uncharged replay on a named family.

**D2. Randomized accelerated proximal coordinate descent on the certified support.** [UB]
*Question.* Does accelerated *randomized* proximal coordinate descent
(APCG/NUACDM-style), run inside the safe-support gates the project already
proved, achieve expected charged work `O_tilde(vol(S*)/sqrt(alpha))` between
support expansions?
*Why now.* For `Q` with `Q_ii ~ (1+alpha)/2`, standard accelerated coordinate
complexity `O_tilde(sum_i sqrt(L_i)/sqrt(mu))` coordinate updates translates
(heuristic — verify the composite/proximal variant and the lazy
representation of the dense momentum coupling) to
`O_tilde(vol(S)/sqrt(alpha))` expected work on a fixed support `S`. The
adversarial per-step families blocking the deterministic AESP-CD Lyapunov
(`K_2` persistent low mode, `K_8` pulse) are realized-trajectory
constructions; an expectation-based estimate sequence is a *different proof
granularity* that those STOPs do not obviously reach. Support safety can come
from the existing safe lower-retraction gate; expansions restart the estimate
sequence, so the remaining research content is exactly the reset-amortization
question (D9) — but now with only an *expected* ledger to control.
*First step.* One note: state the composite APCG variant on a fixed certified
envelope with every sampled coordinate's `d_i` charged (including zero
updates), prove the fixed-support expected-work bound, and run it exactly on
the star, `P_4`, `K_8`, and caterpillar families to see whether the
deterministic STOP families even apply in expectation.
*Kill criterion.* A reachable family where expected spurious/collateral work
per stage is `Omega(1/q)` despite the gate — i.e. the randomized analogue of
the Round-026 STOP.

**D3. Nonbacktracking / directed-edge push as the Phase-II tail.** [UB]
*Question.* Does residual propagation with one-hop *directed-edge* state
(nonbacktracking split, or equivalently forward elimination on the explored
tree with back-substitution) give an unconditional
`O_tilde(1/(sqrt(alpha)*eps_ppr))` tail on trees and tree-like regions, and
what exactly breaks on cycles?
*Why now.* The manuscript's own conclusion names "nonbacktracking state" and
"elimination on an explored tree" as the productive alternatives, and the
spider lower bound is *exactly* the instance where FIFO vertex-push pays
`Theta(L^2)` per arm while elimination pays `Theta(L)`. No note owns this
mechanism. On trees, nonbacktracking push *is* Thomas-algorithm elimination,
so the structured-response notes already contain the ingredients; the open
design question is the general-graph correction (girth/tangle terms — the
spectral folklore connecting nonbacktracking operators to square-root
spectral behavior is suggestive but must not be over-read). (heuristic)
*First step.* Define NB-push precisely in the shared normalization; prove the
spider cost `O(kL)`; then characterize the smallest cyclic family (theta
graph, double cycle — both already in the repo's zoo) where NB state alone
fails, which hands the baton to the cyclic-core response interface (frontier
1).
*Kill criterion.* A bounded-degree cyclic family where any one-hop
directed-edge state provably re-pays `Omega(L^2)`-type revisit despite NB
memory.

**D4. Certified truncated Chebyshev (make LocCH unconditional on a class).** [UB]
*Question.* Chebyshev iteration reaches `1/sqrt(alpha)` iterations globally;
truncation keeps iterates local but injects errors into a three-term
recurrence. On which classes is the truncation-error amplification factor
`O(polylog)` so that thresholded Chebyshev with a *certified* truncation rule
achieves the product scale?
*Why now.* This is the cleanest formalization of the ZSB+24 conditional
bound, the repo already has Chebyshev checkpointing machinery
(`delayed_reflection_ladder`, aggregate debt flush), and trees are likely
provable exactly. It also directly targets the manuscript's "varying
relaxation" alternative: Chebyshev *is* the varying-`omega` schedule that
removes the critically damped double root behind the star logarithm.
(checked for the star-log mechanism; amplification analysis heuristic)
*First step.* Exact amplification analysis of truncated three-term recurrences
on paths/spiders (the `lambda = (1-sqrt(alpha))/(1+sqrt(alpha))` kernel is
already in the manuscript); then a certified drop rule charging every
threshold test.
*Kill criterion.* Instability is intrinsic: a path family where any
truncation at threshold `tau` amplifies to `Omega(tau/ (alpha^c))` residual
error, forcing re-runs.

**D5. Monotone-class lower bound: "acceleration requires signed state" as a theorem.** [LB]
*Question.* Extend the manuscript's ordering-independent star bound from
literal APPR to the *class* of monotone one-hop push methods: nonnegative
residual state, arbitrary damped step sizes `omega in (0,1]`, arbitrary
scheduling, each push scanning its adjacency list. Conjecture:
`Omega(1/(alpha*eps_appr))` on the center-seeded star for the whole class.
*Why now.* The manuscript's proof mechanisms (mass identity + leaf-flow
identity) use only nonnegativity, one-hop structure, and the settle fraction;
they do not use the specific APPR step size (heuristic but high-confidence —
the three steps of `thm:appr-star-lower-bound` appear to survive partial
pushes verbatim). This upgrades an algorithm-specific theorem into the clean
conceptual statement the introduction already gestures at, and it formally
justifies the project's pivot to signed/momentum/response methods. Low cost,
publishable immediately inside the active manuscript.
*First step.* Write the class definition (state, invariant, admissible
updates), re-run the three-step proof, and check the boundary cases
(pushes smaller than the active threshold; lazy vs non-lazy settle fraction).
*Kill criterion.* A monotone one-hop counteralgorithm that beats
`1/(alpha*eps)` on the star — which would itself be a striking result.

**D6. Information-theoretic optimality of the product scale on spiders.** [LB]
*Question.* Prove that any (even randomized) algorithm needs
`Omega_tilde(1/(sqrt(alpha)*eps_ppr))` adjacency probes on a spider ensemble:
`~1/eps` arms whose independent shapes within depth `~log(1/eps)/sqrt(alpha)`
each shift some degree-normalized coordinate by more than `eps`.
*Why now.* It would pin the target as the *information* optimum — locating
the open problem entirely on the computational side — and it forces any
super-product lower bound to be model-restricted, matching what the
oracle-hierarchy work has been discovering the hard way. The killed-Green
influence-packing conjecture (`conj:influence-packing`) is the general form;
the spider case looks like the tractable first instance: each arm's
contribution to the seed-side values is an impedance determined to constant
relative precision only by `Omega(1/sqrt(alpha))` depth, and `1/eps` arms
must be resolved independently. (heuristic; the per-arm sensitivity
calculation must be done carefully in the degree-normalized error metric)
*First step.* Two-arm-shape distinguishing lemma with exact kernel
calculations (the manuscript's path kernel does most of it), then a direct
sum/packing argument; state in the word-RAM output model already used for the
`Omega(1/eps)` output bound.
*Kill criterion.* A sub-product estimator on the ensemble (e.g. sampled
impedance sketching beating the per-arm cost) — which would itself redraw the
map.

### Tier 2 — structural and conditional positives (extend the proved core)

**D7. Graph-class product theorems.** [S]
Prove `O_tilde(1/(sqrt(alpha)*eps))` (or `O_tilde(1/(rho*sqrt(alpha))))`
end-to-end on explicit classes, using machinery already in the notes:
(a) *bounded treewidth / supplied width-`w` ordering* — the conditional
`thm:width-resolution` plus transfer-tree responses look close to
unconditional here; (b) *trees* outright (should be fully closable now);
(c) *expanders* — heuristic: FM26-style confinement/no-percolation conditions
may hold a priori when the local graph mixes fast, making over-regularized
FISTA or AESP unconditionally local; (d) *bounded degree + large girth* via
D3. Each class theorem is a publishable positive result and a regression
target for the general question.
*Kill criterion per class:* an in-class family violating the required
confinement/locality condition.

**D8. Route B (windowed/spectral low-Dirichlet Lyapunov) — continue, but capped.** [UB]
This is the controller's current live queue and it is genuinely the last gap
in an otherwise complete acceptance contract (terminal bridge, gates, cached
rows, fallback all proved). Two recommendations. (i) Enforce the granularity
switch the Round-027 evidence suggests: the next attempt should be a
*windowed* estimate over `Theta(1/q)` stages (where the `K_2` per-step loss
`O(q^2)` sums to `O(q)` — potentially acceptable) rather than another
one-step bank. (ii) Time-box: if two more rounds of exact-family narrowing
pass without a windowed GO, switch the direction's effort to D2 (randomized
granularity) and demand from the adversarial track an actual *counterexample
family* for the deterministic net exponent rather than more template STOPs.
(checked as far as the ledger state; the recommendation is judgment)

**D9. The expansion/reset amortization lemma as a single named target.** [UB/S]
The same missing lemma appears under four names:
`Lambda_J` early locality (`hybrid_aesp_locsor`), all-history causal solvency
(`volume_gated_acceleration`), the expanding-face estimate-sequence lemma
(`aspr23_bound_audit` successor), and restart amortization
(`hybrid_local_solver_complete_note`). They are not identical, but they share
the shape "accelerated state survives a certified support admission with cost
charged to newly admitted volume". Consolidating them into one shared problem
statement with one adversarial family zoo (three-arm spider, double-Y,
caterpillar, T-tree — all already built) would concentrate effort and make a
STOP in one note transfer automatically. The two-admission and
next-admission-stop results (Rounds 019–021) delimit it from below; the
`SettledAuxAppend` shock result delimits it from above. This consolidation is
cheap (a controller round) and high-value.

**D10. Frontier 1 (cyclic-core finite-band reporter) — change the gadget generator.** [S]
Five cyclic families are retired; the obstructions were all *legality*
failures (the prescribed witness chronology cannot occur), not reporter lower
bounds. Two suggestions: (i) invert the search — instead of hand-designing
couplings and then checking legality, enumerate small bounded-degree cyclic
gadgets computationally (the repo has exact trace checkers) and filter for
legal report-free later-petal chronologies before any human proof effort;
(ii) connect to D12 — if incremental boundary reporting on cyclic cores is
OMv-hard, the reporter target should be weakened to output-sensitive amortized
reporting, and that would be a *finding*, not a failure. (heuristic)

### Tier 3 — the lower-bound program

**D11. Galerkin-restricted product lower bound.** [LB]
The five-site and singleton-basis counteralgorithms defeat broad polynomial
classes by *leaving* the Krylov/Galerkin trajectory. The natural repaired
class — iterates confined to the Krylov space of exposed rows with charged
per-step supported work (covering CG, Chebyshev, heavy-ball, and every method
in the manuscript) — is precisely the "independently justified
trajectory/materialization restriction" the STATUS card calls for. The
surviving-regime cyclicity theorem (`n - r - 1` degree bound at
`alpha = n^(-2)`) is most of the algebra; what is missing is the argued-for
justification that the restriction is natural rather than gerrymandered.
*First step:* write the class definition and check it against every
algorithm the project has ever run (they should all be members).
*Kill criterion:* a natural member algorithm that escapes the degree bound.

**D12. Conditional hardness from OMv (or similar) for incremental
maintenance.** [LB]
The recurring wall — repeated boundary refresh under dense implicit Schur
corrections (`conj:aggregate`, frontier 1, frontier 3's Gram-refresh
blocker) — has the flavor of Online Matrix-Vector / dynamic-problem hardness.
A reduction from OMv to "maintain KKT boundary violations under `T` vertex
admissions on a cyclic core with charged queries" would (a) explain five
retired gadget families, (b) justify weakening the reporter target, and
(c) bound what D1 can hope for. Even a partial reduction (for a restricted
reporter interface) would reshape the program. (heuristic; the reduction is
nontrivial because the repo's matrices are Stieltjes and local)

**D13. Influence packing (the information route).** [LB]
`conj:influence-packing` remains the only route to an
algorithm-independent statement. D6 is its tractable special case; after D6,
the bounded-overlap corridor version on general graphs is the natural next
rung, and it dovetails with the regime map (only the `eps < sqrt(alpha)`
wedge matters).

### Tier 4 — publication, scope, and infrastructure

**D14. Ship the tightness-and-obstructions paper.** [P]
The active manuscript is close to submission-ready: results are proved,
audited, and internally consistent. Missing: RPPR/CF-Push experiment runs,
a related-work pass that positions against WY26 (currently absent from the
manuscript bibliography as far as the sections show), and a decision on
whether the monotone-class upgrade (D5) goes in. I would submit this rather
than holding it hostage to the accelerated theorem; it defines the
benchmark, the charged model, and the obstruction landscape the eventual
positive paper will stand on — and the area is moving (WY26 is seven days
old).

**D15. Two follow-on papers are already latent in the notes.** [P]
(a) *Structured persistent-response local solvers*: transfer trees, token
countdowns, caterpillar reporters, FACR, settlement calculus — a coherent
"data structures for local solvers" paper with complete charged ledgers.
(b) *Lower bounds for accelerated local methods*: AESP-LocGD star bound +
ASPR audit + literal two-rung P3 bound + (D5, D6 if they land). Both can be
assembled mostly from existing proved material with scope statements the
STATUS cards already contain.

**D16. Publish the charged-work model itself.** [P]
The eleven-coordinate ledger, the accuracy-namespace atlas, and the
theorem-acceptance checklist would make a strong short methods/position
paper (or a manuscript section) — and would let future theorem statements
cite a fixed model instead of re-deriving the charging discipline each time.

**D17. Update the shared definition per Section 2.** [P]
Regime map (`eps` vs `sqrt(alpha)` wedge, WY26 envelope), `PPR-cert` /
`PPR-sem` split, Tier A/Tier B randomness policy, precision-debt register,
and a WY26 charging audit (does `O_tilde(1/eps^2)` survive the eleven-vector?
`incremental_active_set_sdd` is the natural owner).

**D18. Systematic falsification harness + measured-track expansion.** [E]
Extend the exact checker infrastructure into a standing adversarial zoo
(star, spider, `P_4`/`P_7`, `K_2`/`K_8` families, caterpillar, double-Y,
double-cycle, decoy-hub) with the charged ledger as the universal meter, and
run every new candidate mechanism (D1–D4) against it *before* proof effort.
Symmetrically, run the manuscript's missing RPPR/CF-Push experiments. The
measured track currently covers only SOR schedules; D1–D4 all have cheap
empirical pilots. Given the project's agent-driven workflow, a
search-over-schedules with the ledger as fitness (as `frontier_adaptive_ladder`
accidentally was) is a legitimate discovery instrument — provided results
stay in the measured namespace.

**D19. Scope extensions as separable projects.** [P]
Weighted graphs (most machinery is Stieltjes-generic), directed graphs
(Che+23 do this empirically; theory is open), dynamic seeds/graphs
(incremental PPR maintenance — connects to D1/D12), multi-seed `nnz(s)`
regimes, and single-coordinate/point-query variants (where bidirectional
sampling methods achieve square-root phenomena of a different kind — worth a
literature note to make sure no transferable mechanism is missed).

---

## 5. Suggested prioritization

If I had to allocate the next quarter:

1. **Now (cheap, decisive):** D5 and D6 (two theorem-sized additions that
   round out the manuscript), D14 (submit), D17 (definition update), D9
   (consolidation round). D18's zoo formalization.
2. **Main new bets (parallel direction agents):** D1 (incremental active-set,
   Tier-B randomized) and D2 (randomized accelerated CD) — these attack the
   two most plausible winning mechanisms; D3 as a third seat if capacity
   allows (it feeds frontier 1 with a principled gadget question).
3. **Continue, capped:** D8 (Route B, windowed granularity, two-round cap),
   D10 with the inverted gadget search.
4. **Background:** D11–D13 lower-bound seats; D15/D16 assembly when the
   first-tier items stabilize.

The portfolio logic: the project currently has one deep deterministic
worst-case bet (Route B) plus a broad obstruction program. Adding one
randomized-analysis bet (D2), one solver-technology bet (D1), and one
mechanism bet (D3), each with an existing note to land in, converts the
program from "one door" to "four doors", while D5/D6/D14 bank guaranteed
value immediately.

---

## 6. Direct answers to the two questions asked

**Is the problem definition sound?** Yes — with three amendments worth
making: scope the open target to the `eps_ppr < sqrt(alpha)` wedge (WY26
closes the rest at Tier B), split certified from semantic output, and
formalize the deterministic/randomized two-tier acceptance policy. The
charged-work ledger and namespace discipline are the definition's real
assets and should be published as such.

**Where does progress actually stand?** The tightness floor is done and
publishable (manuscript). The accelerated target is genuinely open in both
directions; the notes program has (a) reduced the upper-bound question to
three named interfaces — low-Dirichlet windowed Lyapunov, expansion/reset
amortization, cyclic-core response maintenance — with everything around them
proved, and (b) demonstrated that naive lower-bound classes are defeated by
counteralgorithms, leaving Galerkin-restricted, information-packing, and
fine-grained-conditional routes. The single most under-weighted fact in
current planning is external: WY26's `O_tilde(1/eps^2)` with
`polylog(1/alpha)` moves the frontier to *warm-started incremental solvers*,
where the project's response-track machinery is strong but its randomized
tooling is absent.
