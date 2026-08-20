# Research Notes

## Hybrid Local Solver

Working hypotheses, proof ideas, and experimental observations should be recorded here.

Important topics:

- Catalyst acceleration;
- AESP;
- LocSOR;
- hybrid switching rules;
- complexity bounds.

## 2026-08-20: solver-family organization and response-preconditioned bridge

The project now records its solver classification in
`docs/solver-family-roadmap.md` and the machine-readable
`manuscript/notes/taxonomy.toml`. The classification uses three independent
axes: graph access, support evolution, and inverse realization. In particular,
nested active sets do not imply an SDD method, and adjacency access does not
imply a first-order restriction.

Two new standalone notes isolate the resulting research program:

- `manuscript/notes/response_preconditioned_hybrid/` proves the generic
  bordered-Schur correction, energy-to-boundary interval, and geometric rebuild
  lemmas, then states an exhaustively charged conditional composition theorem;
- `manuscript/notes/local_solver_oracle_hierarchy/` separates adjacency access,
  materialized restricted solves, local-linear-span recurrences, and persistent
  response, and formulates a same-instance recurrence-versus-response
  separation target.

The current judgment is deliberately narrower than universal optimality. A
mixed settled-response/frontier-repair architecture is the strongest
risk-adjusted project design because it interpolates between two unresolved
endpoints. A graph-uniform output-sensitive incremental SDD/Schur solver would
make iterative repair asymptotically unnecessary, while a graph-uniform
no-restart expanding-subspace theorem could attain the product scale without a
nontrivial response representation.

The immediate common target is certified finite-band boundary response on
nonequitable cyclic cores. The response layer must report every safe violation
and certify all unreported boundary coordinates outside the declared band;
spectral energy accuracy or single-coordinate query access alone is
insufficient. The complementary iterative target is acceleration over safely
expanding faces without restarting a complete solve after every support event.

Use `make note-audit`, `make note-report`, and `make note-graph` to validate and
inspect the inventory. These tools do not rewrite research sources.

### Dense response--frontier reference implementation

`src/hybrid_solver_codex/response_hybrid.py` now realizes the proposed
heavy/light controller exactly on small graphs. It maintains a dense inverse on
the settled anchor, warm-starts CG on the exact frontier Schur complement, and
absorbs the frontier after geometric degree-volume growth. Rebuild factors one,
two, and infinity expose the pure-response, mixed, and fixed-anchor iterative
endpoints behind the same support and verification controller.

The experiment `make response-hybrid` keeps adjacency scans, global boundary
reads, dense response-update arithmetic, Schur construction, frontier CG,
materialization, and output writes separate. At `alpha = 0.05`, note-scoped
`eps_ppr = 1e-6`, and random seed 7, factor two reduced the diagnostic response
update arithmetic relative to rebuilding every batch by approximately `77%`
on the path, `88%` on the binary tree, `68%` on the spider, and `66%` on the
random 4-regular graph. Relative to never rebuilding, it reduced frontier CG
iterations by approximately `53%`, `78%`, `54%`, and `34%`, respectively.

An immediate factor-two rebuild fails on the center-seeded star: its single
heavy batch would trigger the full dense response although the frontier solves
in one CG step. The implemented mixed arm therefore gives each new frontier
one converged iterative probe before permitting a volume-triggered rebuild.
This makes the star collapse to the fixed-anchor endpoint with one iteration
and no post-initial response update. These measurements establish a
reproducible tradeoff surface, not a combined work bound or universal hybrid
advantage. The implementation deliberately materializes the full matrix and
performs global boundary reads; replacing those two operations remains the
graph-local P0 obligation.

## 2026-08-20: repeated active-set SDD factor isolated

The new standalone note
`manuscript/notes/incremental_active_set_sdd/` audits the August 2026
Wei--Yang growing-active-set PageRank/RPPR result and resolves the first reuse
questions without overstating the arbitrary-graph case.

Closed statements:

- the source degree-form system is exactly the shared lazy RPPR system after
  the parameter change `alpha_bar = 2 * alpha / (1 + alpha)` and the variable
  change `x = D^(1/2) z`; `rho` is unchanged;
- successive exact restricted states have an explicit block-Schur correction,
  and the sum of their squared correction energies telescopes to at most
  `alpha_bar` along a source-valid trajectory;
- this energy identity is not a work amortization: on endpoint paths the
  active set can grow through every prefix, so any implementation that writes
  the full active vector or performs one full active-set matrix pass per round
  pays `Omega(|S*|^2) = Omega(|S*| vol(S*))`;
- the same endpoint paths admit an exact append-only tridiagonal `LDL^T`
  representation. Two scalars per admitted vertex determine the next boundary
  gate, and one terminal reverse pass materializes the answer. Total charged
  work is linear in the final active volume, with no polynomial dependence on
  `1 / alpha`;
- the exact path replacement inherits deterministic ACL approximation and
  RPPR support-containment/additive-objective guarantees from the source
  active-set proof.

The arbitrary-graph claim remains conditional. The needed primitive must
jointly maintain an implicit nested restricted solution and the complete set
of boundary violations. A conventional SDD warm start is insufficient because
the block correction can be dense and a changed old coordinate alters its
outside neighbors' residues. If a graph-uniform output-linear interface is
proved, Wei--Yang's outer argument would give `O_tilde(1 / rho)` RPPR work,
strictly stronger than the current `O_tilde(1 / (rho * sqrt(alpha)))` project
target. Existing product lower bounds do not rule this out because they use
narrower persistent-support or repeated-row access models.

## 2026-08-19: the orthogonal-locality proof program is closed

The remaining terminal-envelope question for `evolving_support_cg` has a
sharp negative answer. Fixing `alpha` and the note-scoped `eps_ppr`, a
four-vertex core can place one low-degree violating leaf beside a
nonviolating hub of arbitrary degree. Literal violation-only principal
expansion admits the leaf and terminates at degree volume `5`; factor-two
halo growth must also admit the hub to reach its doubling target, ending at
volume at least `M + 5` and performing at least `M` graph work.

The complementary positive statement is also proved: exact violation-only
expansion from a point seed has terminal degree volume at most
`d_source + (1 + alpha) / (2 * alpha * eps_ppr)`. Thus orthogonality itself
does not eliminate spatial locality, and geometric envelopes really do
amortize restart work, but nonviolating look-ahead cannot have a uniform
locality guarantee. The complete algorithmic conclusion is to use
frontier-sparse exact CG as the honest orthogonal baseline, retain
violation-only restricted CG as the support-safe reference, and allow
geometric halo growth only behind a hard degree-volume cap with a certifying
fallback.

The executable decoy sweep uses hub degrees `16, 64, 256, 1024, 4096` at
`alpha = 0.01` and `eps_ppr = 0.25`. Literal work stays `33`; factor-two work
is exactly `4M + 37`. All runs pass the verifier-owned residual certificate.

## 2026-08-18: geometric-envelope CG closes the restart ledger

The `evolving_support_cg` note and prototype now include factor-two envelope
growth after a failed restricted-CG solve.

Closed statements:

- exact line-minimizing CG preserves a nonpositive quadratic objective across
  warm starts and support expansion, so every restricted call retains the
  standard `O(1 / sqrt(alpha))` iteration scale;
- every nonexhausting failed envelope doubles in degree volume, giving at
  most logarithmically many restarts and total revisited envelope volume at
  most three times the terminal envelope volume;
- explicitly charged boundary and breadth-first halo discovery preserves the
  output-sensitive bound
  `O_tilde(vol(U_final) / sqrt(alpha))`;
- certification remains verifier-owned, and all direction recurrences stay
  inside a fixed envelope between restarts.

Measured boundary at `alpha = 0.01` and note-scoped `eps_ppr = 1e-7`:

- factor-two envelopes reduce literal restart work from `278090` to `25676`
  on the 511-path and from `815040` to `89460` on the long spider;
- restarts fall from `76` to `7` and from `64` to `7`, respectively;
- the factor-two method remains `2.1` and `2.6` times more expensive than exact
  frontier-sparse CG and explores `192` rather than `153` path vertices.

The restart-amortization question is therefore closed in terms of the final
explored envelope. The 2026-08-19 decoy theorem resolves the remaining
locality question negatively for unconditional factor-two halo growth.

## 2026-08-16: direct theory of the literal two-rung policy

Recorded as the standalone note
`manuscript/notes/two_rung_direct_theory/`.

Closed statements:

- one relaxation-`omega` coordinate push decreases the unregularized
  quadratic by exactly
  `omega * (2 - omega) * r_u^2 / (1 + alpha)`;
- with charge `1 + d_u`, the empirical key
  `|r_u| * sqrt(d_u) / (1 + d_u)` is a graph-universal factor-two
  approximation to exact objective decrease per charge; the same factor
  holds for a top-`k` residual snapshot, without a band or sign assumption;
- the exact key is `|r_u| / sqrt(1 + d_u)`, giving a concrete ranking
  ablation;
- a fully refreshed score maximizer has a fixed-region charged-work
  contraction, while the literal top-fraction batching still needs a live
  staleness amortization;
- every literal two-rung run terminates under the note-scoped residual, with
  explicit nonaccelerated fallback bounds;
- on the single-edge graph, the complete ranked optimal-SOR trajectory is
  available in closed form and alternates signs with a critically damped
  linear transient;
- the asymptotic one-push settlement ratio is at most `0.3002831060...`
  uniformly over `alpha`; hence every fixed band factor below
  `3.3301906768...` has eventual one-push exact settlement;
- in particular, band factor `B = 2.5` needs at most one exact push after
  twenty spreading pushes on the one-edge model. This rigorously shows why
  neighbor cancellation can validate a band rejected by the
  self-reflection-only rule;
- on a sufficiently long endpoint-seeded path, the normalized optimal-SOR
  residual has an exact parity-wave event representation. Fully refreshed
  absolute-residual ranking executes exactly the events above the spreading
  gate and never charges a negative waiting packet: every such packet has a
  strictly larger enabled positive certificate on its northeast dependency
  chain;
- if `L` is the first depth with `lambda^L <= B * eps_ppr`, the spreading
  phase makes exactly `floor((L + 1)^2 / 4)` pushes and reaches an explicit
  two-level signed plateau. Its charged work is exactly three times that
  count minus `ceil(L / 2)`;
- for every `B < 3.3301906768...`, the path terminal phase pushes each
  high-parity coordinate at most once and possibly one outer coordinate.
  Hence its work is
  `O(V_exp * (1 + log(1 / (B * eps_ppr)) / sqrt(alpha)))`;
- strengthening the live batch guard with the condition `r_u > 0` extends
  the exact path theorem to snapshot batches of arbitrary size. It adds no
  charged coordinate work under the note's meter, though it can add service
  round trips;
- the sign guard is necessary for arbitrary batch sizes: with the original
  absolute live guard, full-frontier batching reaches a two-entry third
  snapshot, pushes a positive coordinate at distance two, and then charges a
  still-negative endpoint;
- for `alpha > 1/49`, including the measured values `0.025` and `0.04`, a
  partial-layer invariant proves that the actual unguarded top-`1/32`
  snapshots preserve the exact spreading and terminal path counts,
  independently of equal-rank tie breaking;
- static top-`1/32` parent closure is nevertheless false: an explicit
  dependency-closed 34-corner interface uniquely selects a distant positive
  event and then a still-negative endpoint. The smaller-`alpha` actual path
  trajectory therefore needs a stronger history invariant;
- on a symmetric `q`-arm spider, refreshed ranking has an exact center-only
  prefix. For fixed `q >= 3` and small `alpha`, it performs
  `Theta(1 / sqrt(alpha))` consecutive center pushes, about half on negative
  residual, with `Theta(q / sqrt(alpha))` charged work;
- this single-branch echo saturates but does not exceed the desired
  explored-volume acceleration budget. Persistent expansion can pay this
  echo, whereas the fixed `P_3` lower bound below shows that a reached leaf
  can turn it into a genuinely slower macrocycle;
- grouping every depth of a symmetric spider into a radial block reduces both
  the optimal-SOR and exact rungs identically to the endpoint-path recurrence
  scaled by `1 / q`. This proves the same accelerated explored-volume bound
  for the complete radial-block spider method;
- on every level-regular rooted tree, shell-energy coordinates
  `z_i = sqrt(n_i d_i) y_i` reduce both radial block rungs to an exact
  symmetric tridiagonal chain. Its edge impedance is
  `2 sqrt(phi_i / (d_i d_(i+1)))`, and its squared shell coordinate is the
  aggregate residual-energy numerator for one-step objective decrease;
- in a homogeneous `g`-ary bulk, a translation-invariant two-level parity
  wave exists only for `g = 1`. The exact uncancelled branch debt is
  `lambda^2 ((g - 1) / (g + 1))^2`, identifying the path as the unique
  homogeneous critical match;
- for every fixed `g >= 2`, refreshed radial ranking performs
  `Theta_g(1 / sqrt(alpha))` consecutive root pushes before selecting level
  one. Thus the common shell-visit factor cannot be constant;
- if a homogeneous expanding tree visits shell `i` at most
  `K (L - i + 1)` times, geometric shell volume absorbs the triangular
  revisits and total charged work is `O_g(K V_L)`;
- more strongly, every finite explored ball of the homogeneous `g`-ary tree,
  `g > 1`, has Dirichlet gap at least
  `(sqrt(g) - 1)^2 / (2(g + 1))`, independent of depth and `alpha`;
- applying refreshed block contraction retrospectively to the final explored
  ball pays all revisits without a per-shell estimate. Both the optimal-SOR
  spreading rung and exact terminal rung terminate with explicit work bounds,
  giving `O-tilde_g(V_exp / sqrt(alpha))` total radial work for every fixed
  band factor;
- a positive Jacobi supersolution with ratio `rho < 1` extends the same
  result to variable level-regular profiles. If every offspring count is at
  least `g > 1`, the homogeneous gap constant remains valid;
- a unary corridor of length `ell` has gap at most
  `alpha + pi^2 / (4 (ell + 1)^2)`, proving that the persistent-expansion
  condition cannot be removed inside the same spectral argument;
- the test vector `sqrt(d_u) g^(-depth(u)/2)` removes level symmetry:
  refreshed individual-coordinate two-rung SOR has
  `O-tilde_g(V_exp / sqrt(alpha))` work on every rooted tree with at least
  `g > 1` children per vertex;
- the unrestricted graph-uniform target is false. On the center-seeded
  three-vertex path, the literal top-`1/32` batches are singletons yet
  `W_spread >= alpha^(-3/2) / 1408` for `B = 2.5`, `eps_ppr = 0.01`, and
  `alpha <= 1e-4`, while `V_exp = 4`. The exact reflecting-leaf macrocycle
  combines `Theta(1 / sqrt(alpha))` center echoes with a
  `1 - Theta(alpha)` slow mode.

Open boundary:

- extend the actual top-`1/32` endpoint-path invariant to
  `alpha <= 1/49`, or find an actual-run counterexample;
- design a boundary-aware correction that destroys the proved three-vertex
  reflecting slow mode, then splice that correction with the nonsymmetric
  expansion and exact corridor theorems;
- charge live stale operations inside larger measured batches on the
  resulting positive graph classes;
- do not compare the note-scoped unregularized `eps_ppr` bound with the
  persistent-support RPPR `rho` lower bound without an explicit accuracy and
  oracle mapping.

## 2026-08-16: propagate--settle absorption and revisit-volume framework

Recorded as the standalone note
`manuscript/notes/propagate_settle_framework/`. It extracts a common theory
from `two_rung_sor`, `rlsor_terminal_exact_rung`, and
`frontier_adaptive_ladder`.

Closed statements:

- exact Dirichlet settlement on a region is an affine idempotent map, and
  settlement maps on nested regions satisfy a two-sided absorption law;
- every propagation trajectory supported inside the next settled region is
  erased exactly, so two methods with the same nested discovered regions have
  identical exactly settled iterates and boundary residuals;
- the only possible benefit of over-relaxation in an exactly settled method is
  changing region discovery, discovery time, or discovery work; it cannot
  improve the terminal point of a fixed region;
- repeated unit-relaxation delivery has an exact defect certificate: if its
  remaining interior residual is `e_U`, its quadratic objective excess above
  exact settlement is `e_U^T Q_UU^(-1) e_U / 2`, at most
  `||e_U||_2^2 / (2 alpha)`;
- empirical charge volume `cvol(U) = sum_{u in U} (1 + d_u)` is within a
  factor two of degree volume, so the benchmark and theoretical work units
  can share one amortization;
- the trajectory-sensitive work quantity is the settled-volume revisit factor
  `R_set = sum_k cvol(U_k) / cvol(U_K)`, not the raw batch count;
- under constant scans and width-`w` settlement, work is
  `O((w + 1)^2 R_set cvol(U_K))`;
- condition-free exact RPPR boundary expansion admits only true-support
  vertices and has the sharper bound
  `O((w + 1)^2 sum_k vol(U_k)) = O((w + 1)^2 R_set / rho)`;
- hence the intended product scale needs only
  `R_set = O_tilde(1 / sqrt(alpha))`, a strictly weaker target than bounding
  the number of nonempty batches by the same order;
- a four-vertex tailed triangle refutes activation by root-distance layer: two
  vertices at distance one enter in consecutive exact-gate batches;
- a width-two tailed fan extends the obstruction to any prescribed number
  `L` of singleton batches among distance-one vertices and forces
  `R_set > (L + 1) / 5`, even though the graph has root radius two;
- quantifying the fan's limiting tridiagonal response gives
  `R_set = Omega_alpha(log(1 / rho))`; therefore a log-free revisit theorem is
  false for the literal fresh-refactor-and-rescan gate, while the
  polylogarithmic accelerated target remains viable;
- cumulative settled volume has an exact activation-age dual: every vertex is
  charged once for every fresh settlement after it enters, so the fan lower
  bound is caused by the long paid lifetime of its degree-`m` root;
- a lazy block-Schur update represents the correction to old coordinates and
  updates all remaining violation demands through one signed Schur
  block-column, without algebraically resettling the old region;
- on the same tailed fan, retaining the exact two-coordinate separator
  `{o, v_j}` reproduces the identical first `L` batches and restricted
  solution in `O(m + L) = O(cvol(U_L))` work, versus `Omega(m L)` for fresh
  settlement; hence the logarithmic fan lower bound is not an
  information-theoretic barrier to an output-linear exact local method;
- more generally, a charged online activation-aligned trace with live frontal
  size `zeta` and at most `nu` exact boundary-demand signatures reproduces
  every gate batch and the terminal solution in
  `O((1 + zeta^2 + nu zeta) cvol(S) + T_sep)` work, with the separator-update
  charge and exact metadata/access model now explicit;
- kinetic scalar threshold reporting removes the `nu` factor when distinct
  demands have stable one-dimensional crossings; rooted spiders admit an
  exact `O(cvol(S) log(2 + R))` online solver even if all `R` frontier
  responses differ;
- stable low-dimensional affine demands reduce exactly to dynamic
  extreme-point reporting; response-rank examples on sparse path cores show
  that bounded state dimension or bounded rekeying is a genuine hypothesis;
- certified low-rank response trees replace exact signature equality by
  rigorous KKT-sign intervals and charge only visited nodes, ambiguous exact
  leaves, factor maintenance, frontal algebra, and separator updates;
- constant-degree expanders with full RPPR support force
  `zeta, nu = Omega(n)` in every activation-aligned flat presentation, so the
  structural condition cannot be removed graph-uniformly within that
  framework; this is not a lower bound against all local solvers;
- the exact cutoff `zeta_0 = ceil(alpha^(-1/4))` caps pre-overflow dense Schur
  work at `O(cvol(S) / sqrt(alpha))`;
- an explicit RPPR tree refutes per-event shock-only continuation under
  explicit batch output, and a block argument separately proves that
  full-sweep accelerated-gradient, Chebyshev, and CG repair require one old-
  face pass even when the event shock tends to zero;
- aggregate numerical repair is nevertheless closed: with an exhaustively
  charged exact-response oracle, leave the iterate unchanged through an epoch
  and perform one final accelerated solve; telescoping charges its work by the
  total face shock and one scan ceiling;
- once an independent exact-response mechanism certifies the groups, heavy
  shocks require only a constant number of numerical repairs per epoch;
  `||q_B||_2^2 >= 2 theta E` is a sufficient repair-frequency condition, not
  an exact-sign certificate;
- lazy inverse-response recursion bypasses the literal gate and computes the
  exact support and solution on every rooted tree in
  `O_tilde((1 + cvol(S*)) / sqrt(alpha))` work; a conditional hierarchical
  route-charge lemma identifies the exact higher-rank interface;
- original-basis multifrontal or Cholesky response hierarchies require
  `Omega(n^2)` explicitly stored numerical entries on bounded-degree
  expanders, and eager exact-demand arrays require `Omega(n^2)` updates on a
  sparse cyclic Stieltjes light cascade; these are representation lower
  bounds, not lower bounds against compressed or matrix-free algorithms;
- relative to a stable exposed block--cut presentation, exact response
  recursion on blocks of size `b` has route work quadratic in `b`; for
  polylogarithmic `b` it reaches the product scale when the presentation can
  be maintained within the same budget, while online response recourse under
  cycle-closing block merges remains open;
- finite-resolution RPPR continuation needs no exact zero-sign decisions in
  an `alpha * tau` normalized KKT band: certified demand error
  `alpha * tau_gate / 4` gives support safety and terminal normalized error
  at most `tau_gate`, and one final accelerated solve yields total error
  `rho + tau_gate + tau_sol`;
- consequently, a graph-uniform finite-band response oracle would imply
  `O_tilde(1 / (epsilon * sqrt(alpha)))` work for degree-normalized PageRank
  error `epsilon`; this is strictly weaker than exact light-sign maintenance;
- accumulating backward packets into one net right-hand side makes a typed
  one-scan causal epoch output-linear on forests and width-sensitive on sparse
  cyclic regions, independent of how many causal paths contributed packets.

Open item:

- within the exact boundary-gate hybrid route, prove graph-uniform response
  maintenance for consecutive light-shock events on nonequitable cyclic
  cores. Numerical amortization is no longer open: one final accelerated
  repair suffices. The missing theorem must build an online response hierarchy
  whose event-route ranks and rekeys total
  `O_tilde(cvol(S*) / sqrt(alpha))`, including initialization, all old-face
  reads, exact sign queries, explicit output, and no future-support advice.
  Root radius, constant flat width, and one global low-rank factor are each
  insufficient on their own. For the approximate target it is enough to prove
  the strictly weaker finite-band certificate bound, charging only the
  transition-band refinements and finite-accuracy response maintenance.

## 2026-08-16: adaptive revisit control and safe policy portfolios

Recorded as the standalone note
`manuscript/notes/adaptive_revisit_control/`. The note isolates the
cross-instance revisit-memory idea from the measured frontier ladder and asks
what it can support without assuming that task difficulty transfers between
graphs or seeds.

Closed statements:

- the stored revisit ratio is exactly the charge-weighted mean number of paid
  visits to a touched coordinate, and its excess over one is the realized
  revisit work divided by touched-support charge;
- a four-way ledger indexed by the previous and current exact/spreading modes
  decomposes all revisit work exactly;
- every paid revisit after an exact push certifies intervening
  neighbor-generated backflow, because the exact push left zero residual on
  that coordinate;
- on a nested propagate--settle trace, the empirical ratio factors exactly as
  the settled-volume revisit factor times the settled-volume-weighted mean
  within-epoch multiplier;
- a causal revisit bank admits all first touches and only affordable repeated
  touches, enforcing `Work_t <= Gamma C(S_t)` at every prefix; applied to the
  propagate--settle ledger, this removes the assumed bounded-propagation
  multiplier and leaves the cross-epoch settled-volume factor as the
  structural obligation;
- every terminal support-safe RPPR trace has the a posteriori certificate
  `Work <= 2 rho_rev / rho`; a global bank with
  `Gamma = O_tilde(1 / sqrt(alpha))` therefore certifies the intended
  `O_tilde(1 / (rho sqrt(alpha)))` fast path without a structural graph
  condition, while a first overdraw caps the prefix before canonical fallback;
- the literal fixed-band two-rung continuation cannot make that bank
  graph-uniform: on one edge, an RPPR-certified support-safe handoff lies
  strictly below the spreading threshold and its exact-delivery tail takes
  `Omega(1 / alpha)` work at fixed `rho` and fixed `eps_ppr`;
- the scalar ratio does not order total work because its touched-support
  denominator is policy dependent, and one historical scalar cannot identify
  which of two future policies is better over unrestricted task sequences;
- immediate quadratic-objective decrease per charge is uniquely maximized by
  `omega = 1`, so any advantage of over-relaxation must arise over a
  multi-operation transport block rather than from a myopic descent score;
- every causal controller clamped to `omega in [1, 2 - delta]` terminates from
  the zero iterate when every paid operation satisfies the live note-scoped
  degree-normalized residual gate, with charged work at most
  `(1 + alpha) / (delta * (2 - delta) * alpha * eps_ppr^2)`;
- a budgeted adaptive prefix can switch irreversibly to exact Gauss--Seidel on
  the same state; its energy decrease is credited against the tail, giving
  `Work_total <= H_0 + (1 - delta * (2 - delta)) Work_prefix` and a hard
  near-baseline ceiling without branching or reset;
- a branchable weighted portfolio of finitely many certifying local policies
  has work `min_j Work_j / nu_j`, up to one scheduling chunk; uniform shares
  are therefore `K`-competitive with the best of `K` arms on every instance;
- a geometric restart portfolio uses one live policy state at a time and costs
  less than `4 K max(Work_best, B_0)`, so simultaneous branches are not needed
  when a clean instance reset is available;
- for single-seed RPPR, every exact restricted settlement is a canonical
  absorption checkpoint: a history-dependent controller may change policy and
  admit any nonempty subset of exact boundary violations while preserving true
  support containment, positivity, and finite termination; combining this gate
  with the revisit bank gives a genuine work-capped no-reset switch theorem;
- a finite simple unweighted single-seed RPPR tree, consisting of an
  independent length-`L` path and one heavy branch, has two legal exact
  boundary-batch orders with the same terminal canonical point and
  `R_set(early) / R_set(late) >= (L + 1) / 5`; hence checkpoint absorption,
  nested support, persistence, and even treewidth one cannot imply best-arm
  work competitiveness or policy-blind accelerated-bank success;
- if each policy has a work-valued countdown decreased by its own certified
  blocks and never increased by blocks of other policies, a fair scheduler
  committing every block to one shared state costs at most
  `min_j Phi_j / nu_j` plus scheduling discrepancy; `kappa`-tight countdowns
  make the uniform shared-state portfolio `K kappa`-competitive;
- irreversible common-state activation tokens give a general construction of
  such countdowns; on endpoint paths, one forward Schur-record token and one
  reverse-recovery token per true-support vertex give `kappa = 1`, exact
  declared work at most `2 C(S*) <= 4 / rho`, and a no-reset shared-state
  portfolio bound `4K / rho + Delta`;
- on a two-vertex RPPR breakpoint, a legal activation of fixed charge two has
  a vanishing state jump and energy drop; therefore no jointly continuous
  numerical-state countdown can pay activation uniformly, and the necessary
  energy multiplier diverges as the breakpoint is approached;
- the quadratic energy budget is an unconditional mergeable countdown for
  clamped live updates, but it has the nonaccelerated safety scale and does not
  distinguish the empirical arms;
- arbitrary revisit-based predicted shares remain distribution-free safe
  after adding an exploration floor, and the portfolio inherits any
  `O_tilde(V_loc / sqrt(alpha))` bound already held by one of its constant-many
  arms.

Boundary and open items:

- the safety bound is not accelerated and has quadratic tolerance dependence;
- the finite portfolio removes the need to know the best policy in advance,
  but the one-edge theorem refutes a graph-uniform accelerated work bound for
  the literal fixed-band two-rung continuation; adaptive SOR remains only a
  certified empirical arm unless separately analyzed;
- safe switching no longer requires branchable state, reset, or an assumed
  cross-policy state-transfer map at exact RPPR checkpoints; what remains is
  an order-independent activation-once transport representation for general
  branching and cyclic fronts, or a quantitatively forced-spreading arm; raw
  delayed-reflection and causal-backflow magnitudes are not themselves
  interference monotone;
- the endpoint-path activation-token theorem does not yet extend to arbitrary
  trees: the existing lazy tree-response iterator follows a sorted homotopy
  event order, while another legal boundary policy can admit a different
  positive branch first; a dynamic order-independent response-merge lemma is
  missing;
- a continuous relaxation family cannot be reduced safely to a finite grid
  without a regularity theorem for thresholded SOR work as a function of
  `omega`.

## 2026-08-16: finite-propagation CG and evolving principal systems

Recorded as the standalone note
`manuscript/notes/evolving_support_cg/`, with executable prototypes in
`src/hybrid_solver_codex/evolving_cg.py`.

Closed statements:

- exact ordinary CG from a seed-supported right-hand side has one-hop finite
  propagation; its cumulative direction envelope is a valid locally evolving
  set sequence, while each matrix product scans only the current direction;
- the resulting graph work through iteration `K` is bounded by the sum of
  the degree volumes of the visited seed balls, without changing the CG
  recurrence or its `1 / sqrt(alpha)` spectral iteration scale;
- the note-scoped degree-infinity residual certificate implies the matching
  degree-scaled solution-error guarantee;
- masking or thresholding a live direction destroys conjugacy on a
  three-coordinate path, whereas full reorthogonalization remains spatially
  confined but becomes dense in the accumulated support;
- exact principal-subsystem solutions are nonnegative, grow coordinatewise
  under support expansion, and expose nonnegative residual only on the
  boundary, giving a correct restarted evolving-set scaffold.

Measured boundary:

- frontier-sparse exact CG certified all five synthetic graph families;
- restart-after-every-boundary-expansion cost `1.6` to `23.4` times more
  graph work, so that literal policy is refuted as the primary solver;
- fast-growth graphs still make exact CG global quickly. Geometric growth
  amortizes restarts in terms of the terminal envelope, but the 2026-08-19
  high-degree decoy refutes any `alpha`/`eps_ppr`-only bound on that envelope.

## 2026-08-15: alpha-scaled exact rungs and delayed reflection debt

Recorded as the standalone note
`manuscript/notes/delayed_reflection_ladder/`.  The note turns the measured
alternating exact-rung R-LSOR mechanism into a proof program and audits it
against the active long-spider obstruction.

Closed statements:

- with `lambda = (1 - sqrt(alpha)) / (1 + sqrt(alpha))`, optimal SOR has
  `omega_star = 1 + lambda^2` and leaves signed self-reflection
  `-lambda^2 * r_u`;
- an immediate over-relaxed push followed by an exact push is exactly one
  unit-relaxation push, so delay is mathematically load-bearing;
- current-rung no-self-reactivation requires
  `b <= lambda^(-2)`, and missing the next rung requires
  `b <= lambda^(-1)`;
- both admissible bases are `1 + Theta(sqrt(alpha))`, giving
  `Theta(log(R) / sqrt(alpha))` rungs over dynamic range `R`;
- every fixed base `b > 1`, including two and three, eventually violates the
  optimal-SOR no-self-reactivation window as `alpha -> 0`;
- exact unit-relaxation cleanup contracts degree-weighted absolute residual
  mass from arbitrary signed states;
- a fresh/debt residual split preserves `r = b - Qx` exactly while allowing
  self-reflection to be delayed;
- on a spider arm, the neighbor-generated backward packet has magnitude
  `lambda * |r_u|`, larger than the self-debt `lambda^2 * |r_u|`, so delaying
  self-reflection alone cannot remove the triangular traversal.

Conditional target:

- if a causal spreading/exact-cleanup pair costs `O(V_loc)` work and reduces
  the live threshold by an admissible alpha-scaled factor, the total is
  `O(V_loc * log(R) / sqrt(alpha))`; this yields the intended accelerated
  scale under an `O(1 / eps_ppr)` PPR volume bound or the proved safe RPPR
  `O(1 / rho)` support bound.

Open item:

- the exact-debt half of causal pair locality is now closed: a restricted
  block correction zeros all residual in a discovered region; leaf
  elimination computes the correction and boundary residual in `O(vol(S))`
  work on forests, while a width-`w` elimination order costs
  `O((w + 1)^2 vol(S))`;
- exact block cleanup erases all SOR relaxation and scheduling history within
  a fixed region, returning the unique restricted Dirichlet point; therefore
  the only possible accelerated role of the ladder is online region discovery;
- given the exact RPPR support, a shifted Dirichlet solve plus boundary KKT
  check returns the RPPR optimum and an unregularized residual certificate;
  on a forest support with a single seed its cost is `O(1 / rho)`;
- RPPR support components must contain seed coordinates, so single-seed
  support is connected and boundary expansion is complete;
- on an endpoint path, a forward Schur recurrence discovers the exact RPPR
  boundary at the first nonpositive transformed demand; one reverse pass
  solves the support in `O(1 + vol(S*))` work;
- arm symmetry reduces the lower-bound path-bundle spider to the same radial
  recurrence, giving `Theta(1 / rho)` actual scan work on that instance;
- therefore the existing `Omega(1 / (rho sqrt(alpha)))` persistent-support
  product is oracle-specific rather than universal: it charges all resident
  volume at every exposure round, whereas directed Schur messages scan only
  the frontier and then back-substitute once;
- on a rooted tree, every child subtree response as a function of its parent
  value is continuous, monotone, and piecewise affine with nested supports;
  it is zero exactly below the one-edge threshold
  `alpha * rho * sqrt(d_child) / (-Q_parent,child)` and has at most one new
  affine piece per activated subtree vertex;
- the exact tree recursion sums child responses into a strictly increasing
  inverse map `H_u`; its slope is the local Schur complement divided by the
  parent coupling and is at least `alpha / (-Q_parent,child)`, so child
  breakpoints are merged and monotonically transformed without combinatorial
  proliferation;
- explicit bottom-up materialization of these response lists gives an exact
  `O(n^2 log(1 + max_degree))` solver on every finite tree, with no exponential
  active-set enumeration;
- lazy response iterators request only realized activation events, scan an
  active vertex's adjacency once, and never inspect descendants of an inactive
  boundary vertex;
- Chebyshev approximation of `Q^(-1)` gives exponential graph-distance decay
  with ratio `(1 - sqrt(alpha)) / (1 + sqrt(alpha))`; on every graph, the
  exact support radius is
  `O(1 + log(1 / (alpha rho)) / sqrt(alpha))`;
- charging each realized activation through its active ancestors proves an
  exact, support-oracle-free
  `O~(1 / (rho sqrt(alpha)))` degree-work solver on every finite tree, with
  `O(vol(S*))` storage;
- fixing the root value on an arbitrary graph gives one scalar
  piecewise-affine obstacle homotopy with nested supports and at most one
  activation event per nonseed vertex; cyclicity therefore does not obstruct
  exact support discovery;
- an exact block-inverse identity shows that one activation updates every
  remaining slack by one nonpositive Schur-complement column times the new
  coordinate; the unresolved event data structure is therefore a kinetic
  minimum under successive signed low-rank updates, not a correctness issue;
- for block-incidence graphs with biconnected blocks of size at most `q`, lazy
  block responses give an exact, condition-free
  `O~(q^3 / (rho sqrt(alpha)))` solver;
- on a single-seed cycle, reflection symmetry reduces the whole biconnected
  core to a radial tridiagonal Stieltjes system; one forward Schur recurrence
  and one reverse solve discover and return the exact solution in
  `O(1 + vol(S*))` work;
- this output-linear result extends from cycles to every
  root-distance-equitable graph.  Orthogonal shell averaging commutes with the
  RPPR matrix, so the full nonnegative obstacle problem reduces exactly to a
  tridiagonal quotient.  Scanning a certified active shell reveals the next
  shell's size, backward incidence, and degree before that next shell is
  scanned; its Schur demand therefore supplies a lazy KKT stopping test.  The
  resulting exact solver costs `O(1 + vol(S*))` without support, radius, or
  confinement advice, even with arbitrarily thick shells.  Examples include
  cliques, complete bipartite graphs, hypercubes, Hamming and Johnson graphs,
  and all distance-regular graphs;
- the shell method no longer requires a trusted global promise.  On an
  arbitrary graph, each active scan audits the degree and three shell-incidence
  counts.  The last active scan also gives every coordinatewise boundary
  violation before those boundary lists are scanned.  An empty positive set
  is a full KKT certificate; a partial set or failed uniformity check is a
  concrete witness and is handed unchanged to the safe exact boundary gate;
- one cell per distance shell is not necessary.  For an equitable partition
  whose distinct-cell interaction graph is a tree,
  orthogonal cell averaging gives an exact tree-sparse Stieltjes quotient.
  Lazy cell responses reveal the first child event before scanning that cell,
  and the full solver costs
  `O(vol(S*) + log(1 + Delta_P) sum_active_cells quotient_depth)` =
  `O~(1 / (rho sqrt(alpha)))`.  This permits several inequivalent thick cells
  in one shell and original graphs with unbounded treewidth and arbitrarily
  large biconnected cores;
- the partition representation is no longer an oracle condition.  Starting
  from root and degree colors, online equitable refinement uses only counts
  from already scanned adjacency lists.  Every visible class is a union of
  hidden true cells, and indistinguishable boundary cells have one common
  affine slack, so they activate as an exact tied bundle.  Once scanned, a
  bundle may split and fork only its future response.  Smaller-half refinement
  costs `O(vol(S*) log(1 + vol(S*)))`; all response forks retain the
  `O~(vol(S*) R_*)` ancestor charge.  Hence the exact
  `O~(1 / (rho sqrt(alpha)))` bound needs no supplied cell identifiers and
  remains a certifying fast path on arbitrary graphs;
- the supplied-support assumption is removable on arbitrary graphs: exact
  boundary-violation batches admit only true RPPR-support vertices, terminate
  at the exact optimum in at most `|S*|` batches, cost
  `O(1 / rho^2)` with fresh forest elimination, and cost
  `O((w + 1)^2 / rho^2)` with supplied width-`w` intermediate orderings;
- retaining the realized nonempty-batch count `J` sharpens the latter bound to
  `O((w + 1)^2 (J + 1) vol(S*))`; if at most `chi_*` support vertices occupy
  each root-distance shell, then `J + 1 <= chi_* (R_* + 1)` and the
  graph-universal radius lemma gives
  `O~((w + 1)^2 chi_* / (rho sqrt(alpha)))`;
- this radial-width result closes arbitrarily long cycles and fixed-width
  cyclic strips without assuming bounded biconnected blocks; the direct cycle
  recurrence is stronger and output-linear;
- a tied activation batch has an exact block-Schur update: the new block is
  solved with its principal Schur complement, the old active solution receives
  one inverse-positive correction, and every remaining KKT slack changes by
  one nonpositive Schur block-column;
- every exact-gate expansion dominates one unit proximal-gradient step, so the
  RPPR objective gap contracts by `1 - alpha`; if `delta_*` is the smallest
  positive optimum coordinate, the gate terminates within
  `O(1 + alpha^(-1) log_+(1 / (d_o delta_*^2)))` batches, in addition to the
  finite-support bound;
- a three-vertex endpoint path proves that this energy route cannot become a
  graph-uniform accelerated contraction: as `rho -> 0`, its first-batch gap
  ratio is
  `(1 - alpha)^2 / (1 + 6 alpha + alpha^2) = 1 - 8 alpha + O(alpha^2)`;
  this refutes a `1 - Theta(sqrt(alpha))` per-batch gap argument but does not
  refute an accelerated combinatorial batch-count theorem, since that path
  terminates in two batches;
- this condition-free bound already meets `O(1 / (rho sqrt(alpha)))` for
  `rho >= sqrt(alpha)`; the lazy-response theorem closes the fine regime on
  trees as well;
- on the alpha-scaled path `rho[k + 1] = lambda^s rho[k]`, the supplied-
  support exact-rung volume ledger is geometric and costs
  `O((w + 1)^2 / (rho_final sqrt(alpha)))`, without an extra dynamic-range
  logarithm;
- the remaining open structural item is compressed event maintenance, or a
  universal batch-count argument, inside a large biconnected core with
  neither bounded articulation blocks, an equitable tree quotient, nor thin
  radial support.  Exact support discovery, cycles, thick
  equitable cells, fixed-width strips, and bounded-size cyclic blocks are
  closed.

## 2026-08-14: active lower-bound ledger and first tight local hybrid

The active manuscript now separates six algorithm-specific statements under
their native accuracy conventions.

Closed statements:

- the classical APPR proof was rechecked against Andersen, Chung, and Lang
  (2007), Definition 3.3, Lemma 3.4, Algorithm 1, and Theorem 3.2. The lazy
  update, column-vector invariant, mass identity, ordering-independent star
  lower bound, and RPPR bridge are correct;
- a new numerical regression test solves the PageRank and RPPR systems
  directly and verifies `p + pr(r) = pi` for every implemented active ordering;
- full-batch RPPR ISTA retains its previously proved tight general-seed work
  `Theta((1 + log(1 / (delta * rho))) / (alpha * rho))`;
- residual-thresholded coordinate ISTA has a new ordering-independent star
  lower bound `Omega(1 / (alpha * rho))`. Together with its existing potential
  upper bound, this proves exact worst-case work
  `Theta_delta(1 / (alpha * rho))` for every fixed relative accuracy `delta`;
- the coordinate-to-batch coarse-to-fine hybrid inherits the same lower bound
  from its first phase and therefore has the same exact fixed-accuracy
  worst-case order. This is the first active-manuscript hybrid with matching
  upper and lower work bounds;
- the coarse forward-push star proof was strengthened from a scheduled-cycle
  argument to an ordering-independent flow proof, giving an explicit matching
  lower bound for Phase I;
- the full fixed-relaxation FIFO CF-Push hybrid still has only the spider lower
  bound `Omega(1 / (alpha * eps_ppr))` and the weaker energy upper bound. Its
  exact worst-case order remains open.

Scope boundary:

- these statements do not identify `eps_appr`, `rho`, `delta`, and `eps_ppr`;
- tightness is for the stated algorithms and work models, not for every local
  graph oracle;
- the graph-uniform accelerated `O_tilde(1 / (rho * sqrt(alpha)))` target
  remains open and the AESP--LOCSOR publication gate is unchanged.

## 2026-08-12: ASPR 2023 correctness and path tightness audit

Recorded as a standalone note in `manuscript/notes/aspr23_bound_audit/`.
The note reconstructs the intended exact-arithmetic ASPR theorem after
repairing the source's quadratic normalization, RPPR linear term, and the
APGD-output distance display.

Closed statements:

- the support-safety and objective-gap argument is valid for the corrected
  Stieltjes quadratic contract;
- on an endpoint-seeded RPPR path with full optimal support, every proper
  active prefix exposes exactly its next vertex;
- for sufficiently small objective-gap tolerance, literal ASPR makes exactly
  `|S*|` APGD calls and has restricted-solve work
  `Omega(|S*|^2 / sqrt(alpha))`;
- literal fresh-gradient discovery separately costs `Omega(|S*|^2)` on the
  same family;
- these bounds match the two structural products in the published ASPR upper
  bound up to logarithms;
- the quantitative scaling `alpha = |S*|^{-2}`, `rho = alpha / 100`, and
  `eps_obj = 10^{-4} alpha^2` gives
  `Omega(|S*|^3 log |S*|)` ASPR work versus
  `O(|S*|^2 log |S*|)` FISTA work at the same tolerance, while the 2026
  leaf-star lower bound gives the opposite separation when FISTA activates a
  high-degree center;
- the post-COLT official Julia repository generally plots default ASPR faster
  than its FISTA and ISTA baselines, with CASPR fastest, so those plots are not
  evidence that default ASPR is empirically slow;
- in official commit `3a169eb`, the periodic boundary-gradient option deletes
  the active-to-boundary cross block before evaluation. Its early-discovery
  flag is therefore inert on RPPR and the periodic variants only add work;
- the same implementation's in-place retraction fails to clip entries in
  `(0, delta)`, and the baseline support filter performs an `O(n)` complement
  allocation outside the stated local work model;
- a corrected early-discovery method still needs one successful event per path
  layer and `Omega(|S*|^2)` work under fresh-prefix scans, although the current
  proof does not retain the per-stage `1 / sqrt(alpha)` inner lower bound for
  that variant.

Scope boundary:

- the lower bound is for literal ASPR, not every accelerated local solver;
- the sufficiently small accuracy is an objective-gap target and is not
  identified with APPR, PPR infinity error, or the experimental proximal
  fixed-point residual;
- an algorithm-independent local-oracle lower bound remains open.

## 2026-08-13: composite AESP-CD inner oracle proved

The standalone note `manuscript/notes/aesp_cd_l1_rppr/` uses the shared RPPR
objective and analyzes a local proximal-coordinate inner method with
degree-weighted update cost.

Closed statements:

- the minimum-magnitude composite KKT map is one-Lipschitz in each untouched
  coordinate's smooth gradient;
- every exact proximal coordinate update decreases weighted KKT mass by the
  factor `2 * (alpha + kappa_A) / (1 + alpha + 2 * kappa_A)` times the updated
  violation, including zero hits and sign crossings;
- the degree-normalized KKT diagnostic divided by the shifted strong-convexity
  constant certifies degree-normalized solution error;
- both results extend to any separable `l1`-regularized Stieltjes quadratic
  `H` that admits a positive supersolution `H v >= mu v`, with coordinate
  contraction factor `(H v)_i / (H_ii v_i)`;
- thresholded sequential updates have work at most
  `C_t(z_0) / (tau_cd * eps_in)` and give an explicit objective-gap inner
  oracle; for `kappa_A = 1 - 2 * alpha`, `tau_cd = 2/3`;
- consequently, composite AESP can use this oracle from its signed
  extrapolated centers, with cumulative inner work at most
  `3 / (4 * (1 - alpha)) * sum_t C_t(y_(t-1))^2 / phi_t`;
- the raw absolute-gap functional cannot be controlled pointwise by outer
  objective error: minimum KKT mass is discontinuous when a nonzero coordinate
  approaches an `l1` kink;
- the standard composite Catalyst proximal warm start smooths this
  discontinuity, and greedy normalized-KKT coordinate selection contracts
  mass exponentially in degree work on a fixed envelope of volume `V`;
- with Catalyst's relative criterion C2, every inner stage costs
  `O_tilde(V)`, so a certified envelope gives total
  `O_tilde(V / sqrt(alpha))`; an optimal-support oracle specializes this to
  `O_tilde(1 / (rho * sqrt(alpha)))`;
- the actual full-graph heap implementation needs no support oracle and has
  trajectory-dependent work
  `O_tilde(V_exp_max / sqrt(alpha))`, where `V_exp_max` is the largest degree
  volume explored by one stage; every newly nonzero KKT key is locally exposed
  by a touched coordinate or one of its neighbors;
- if a proximal center is a certified lower solution, Stieltjes comparison
  traps its exact shifted minimizer, proximal warm start, and every greedy
  coordinate iterate below the RPPR optimum; no KKT key outside the optimal
  support activates, so that entire safe-centered call costs
  `O_tilde(1 / rho)` without a support oracle;
- any signed finite-support trial point can be converted locally into a lower
  certificate by subtracting its maximum normalized negative one-sided
  residual and clipping at zero; this makes the safe-center result directly
  applicable to accelerated trial points, but does not itself prove that
  repeated retraction preserves acceleration;
- zero-start coordinate descent for unshifted RPPR recovers the standard
  `O(1 / (alpha * eps_kkt))` degree-work scale.

Scope boundary:

- the diagnostic remains note-scoped and is not identified with the source
  proximal fixed-point residual or a repository stopping rule;
- the result closes the composite inner-locality conjecture but not the
  oracle-free graph-uniform accelerated theorem: start-mass interaction is now
  closed both on a fixed certified envelope and in terms of realized explored
  volume; safe lower centers also enforce `V_exp_max <= 1 / rho` for each
  inner call. What remains open is an accelerated outer continuation whose
  centers retain this order safety, or an amortized safeguard that corrects
  unsafe extrapolated centers without repeated acceleration restarts.

## 2026-08-12: volume-gated RPPR acceleration and expanding-subspace lemma

Recorded as a standalone note in
`manuscript/notes/volume_gated_acceleration/`. The note reconstructs the
active-volume flattening discussion and separates the spider's spectral
behavior from support-growth and repeated-scan work.

Closed statements:

- every principal restricted PageRank system has condition number at most
  `1 / alpha`; on a depth-`L` spider prefix the exact scale is
  `Theta(1 / (alpha + L^(-2)))`, so the spider obstruction is geometric
  rather than a local condition number of order `1 / alpha^2`;
- exact PPR has a degree-volume-`1 / tau` superlevel core whose Dirichlet
  restriction is `tau`-accurate in degree-normalized infinity norm;
- fixed RPPR regularization gives support volume at most `1 / rho` and PPR
  error at most `rho`;
- an arbitrary signed restricted candidate can be corrected to a safe lower
  envelope; one-sided KKT violations then admit only true-support vertices,
  and the absence of such violations certifies normalized infinity error;
- choosing `rho = tau = epsilon / 2` proves peak working volume at most
  `2 / epsilon` and final PPR error at most `epsilon`;
- an endpoint-source path forces
  `Omega(log(sqrt(alpha) / rho) / sqrt(alpha))` one-vertex expansions,
  refuting the claim that support changes can always be grouped into only
  `O(log(1 / epsilon))` ordinary restarts;
- the exact expansion gain is a Schur-complement quadratic. Its elementary
  bound is a lower bound, not the upper perturbation bound required for
  accelerated stability;
- continuous restricted re-solving costs telescope to
  `O(log(1 / epsilon) / sqrt(alpha)) + N_exp` full iterations.

Open item:

- the graph-uniform `O_tilde(1 / (rho * sqrt(alpha)))` work theorem requires
  a one-sided projected continuation lemma over safely expanding subspaces, or
  the weaker ability to charge expansion overhead only to newly admitted
  degree volume. The note does not close the separate AESP--LOCSOR promotion
  gate and does not promote the universal bound into the active manuscript.

## 2026-08-12: rigorous AESP--LocGD center-star lower bound

Recorded as a standalone note in
`manuscript/notes/aesp_locgd_star_lower_bound/`. The note reconstructs the
complete proof development for the literal AESP-PPR outer loop with the
batched LocGD inner solver and uses the AESP paper's cumulative active-volume
work measure.

Closed statements:

- on the center-seeded star `K_{1,B}`, every nonempty batched LocGD call costs
  at least `B`, and every `epsilon`-accurate output requires
  `Omega(B / sqrt(alpha))` work whenever `B * epsilon <= 1/4`;
- choosing `B = floor(1 / (4 * epsilon))` gives the unconditional lower bound
  `Omega(1 / (sqrt(alpha) * epsilon))` for this literal algorithm;
- under an edge budget `m`, the construction gives
  `Omega(min(m, 1 / epsilon) / sqrt(alpha))`;
- if unit outer-loop overhead is counted in addition to active volume, the
  first nonempty call contributes a separate
  `Omega(log(B / alpha^2) / sqrt(alpha))` delay in the small-`alpha` regime.

Proof correction and scope:

- leaf symmetry rigorously forces a full center or leaf-block scan, but it does
  not imply the proposed signed residual cone;
- the unconditional proof instead uses the first nonempty activation to bound
  every later subproblem's slow-mode error, followed by a positive
  Green-function calculation for the critically damped outer recurrence;
- the theorem does not apply to arbitrary AESP inner maps, sequential
  LocAPPR, RPPR, or every hybrid local method, and therefore does not by itself
  close the AESP--LOCSOR publication gate above;
- no polynomially larger AESP-LocGD lower bound is currently proved. A
  multiscale spider, star-of-stars, or clustered lollipop would have to force
  transient explored volume beyond the `O(1 / epsilon)` significant-output
  scale.

## 2026-08-12: black-box tradeoff and composite RPPR extension

The standalone note in `manuscript/notes/hybrid_aesp_locsor/` now includes the
latest parts of the project discussion rather than treating the 2026 RPPR paper
only as structural evidence.

New closed statements:

- for every finite handoff, total work is bounded by Phase-I work plus the
  smaller of the objective-gap and weighted-gradient-mass LOCSOR tails;
- using the direct AESP inner amortization and optimizing the objective handoff
  gives an instance-wise
  `O(R / (alpha^(3/4) * epsilon))` inner-plus-tail bound;
- this Path-I result is unconditional with respect to graph structure,
  confinement, and residual signs, but remains parameterized by the realized
  AESP ratio `R` and excludes uncharged outer initialization work;
- the RPPR unit-step proximal map is a `(1 - alpha)` contraction in
  degree-weighted infinity and one norms;
- its fixed-point residual divided by `alpha` certifies solution error;
- a finite composite Catalyst burn-in followed by full ISTA is therefore
  unconditionally convergent from every handoff.

The three proof paths are now separated explicitly:

1. black-box AESP/SOR balancing: closed and `R`-parameterized;
2. early locality/support confinement: conditionally gives
   `O_tilde(1 / (sqrt(alpha) * epsilon))`;
3. KKT-slack cumulative boundary charging: the abstract charge is proved, but
   a shifted-subproblem margin and a localized inner path-length lemma are
   still missing for AESP.

For RPPR, correctness is no longer the open point. The open point is the
`O_tilde(1 / (rho * sqrt(alpha)))` degree-work theorem from an arbitrary
accelerated warm start. Zero-start support monotonicity cannot be silently
reused after Catalyst overshoot.

## 2026-08-12: rigorous AESP--LOCSOR synthesis

Recorded as a standalone note in
`manuscript/notes/hybrid_aesp_locsor/`. The note reconstructs the project
conversation in a common PageRank normalization and separates source results,
new proofs, conditional statements, empirical observations, corrections, and
open claims.

Closed statements:

- after any finite valid AESP handoff, local SOR with fixed
  `0 < omega < 2` terminates under the final degree-normalized gradient
  certificate;
- with the proof-safe tail `omega = 1`, an objective-gap handoff
  `f(x_J)-f* <= alpha^(3/2) * eps / (1+alpha)` gives tail work
  `O(1/(sqrt(alpha) * eps))`;
- the weighted-gradient-mass handoff
  `||D^(1/2) grad f(x_J)||_1 = O(alpha^(3/2))` gives the same tail order and
  bounds every tail active-set volume;
- the complete hybrid has a trajectory-dependent bound
  `O~(Lambda_J/sqrt(alpha)) + O(1/(sqrt(alpha) * eps))`.

Corrections and open item:

- the universal signed weighted-`l1` monotone SOR range is
  `0 < omega < 1+alpha`, not all of `(0,2)`; objective descent still holds on
  `(0,2)`;
- the graph-uniform target total work follows if the early AESP locality
  factor satisfies `Lambda_J = O(1/eps)`;
- that early-locality statement is not proved for every graph. The note gives
  a support-envelope lemma and an explicit no-percolation condition under
  which it does hold, and explains why the 2026 RPPR/FISTA support results do
  not transfer automatically to unregularized AESP.

The note is intentionally not input by the active manuscript while the
repository-wide residual convention remains open.

### Publication gate

Keep `manuscript/notes/hybrid_aesp_locsor/` as a rigorous standalone research
note; do not promote its graph-uniform end-to-end complexity claim into the
active paper until one of the following is established:

1. the central early-AESP locality lemma
   \[
   \Lambda_J
   := \max_{1\leq t\leq J}
      \frac{\overline{\operatorname{vol}}(S_t)}{\gamma_t}
   = O(1/\epsilon),
   \]
   with a graph-independent hidden constant; or
2. a correct weaker structural condition or alternative burn-in work argument
   that is sufficient for the paper's stated theorem.

Until this gate is closed, paper-facing statements may use the proved
trajectory-dependent theorem and explicitly conditional confinement
corollaries, but must continue to label the universal
`O~(1/(sqrt(alpha) * epsilon))` work bound as open.

## 2026-08-02: APPR worst-case work is `Theta(1/(alpha * eps))`

Recorded in `manuscript/sections/appr_lower_bound.tex`. The classical ACL
upper bound `O(1/(alpha * eps))` is worst-case tight, witnessed by the
center-seeded star `K_{1,m}` with `m = floor(1/(8 * eps_appr))`, for every
legal active-vertex ordering. This fixes the baseline that the hybrid solver
must beat and identifies the two obstructions to attack:

1. the `1/alpha` factor, from settling only an `alpha`-fraction of pushed
   residual per push;
2. the `1/eps_appr` factor, from repeatedly rescanning a
   `Theta(1/eps_appr)`-degree vertex.

Any hybrid or accelerated method claiming a better worst-case bound must break
at least one of these; a `sqrt(alpha)`-type acceleration attacks (1) only.

Implementation status and open items:

- `src/baselines/appr.py` now provides a controlled reference implementation
  with exact degree-weighted work accounting and four legal active-vertex
  orderings. `tests/test_appr_lower_bound.py` makes the star a regression test
  and cross-checks FIFO output against the Numba kernel after repairing its
  missing self-reactivation queue step. The reproducible diagnostic entry
  point is `uv run python -m experiments.check_appr_lower_bound`; it records
  graph, `alpha`, `eps_appr`, source, random seed, stopping rule, ordering, and
  code version. Its path and long-spider rows are explicitly not theorem
  checks.
- Whether a path or long spider is tight in the coupled regime
  `L = Theta(1/eps)` with `alpha * L^2 = O(1)` is left open; the star needs no
  such coupling.
- The lower-bound checker enforces the theorem regime
  `0 < eps_appr <= 1/16`; out-of-regime values are rejected rather than
  reported as theorem checks. The figure generator validates the complete
  `(alpha, eps_appr, ordering)` grid before plotting actual or scaled work.
- The relation between `eps_appr` and the RPPR sparsity parameter `rho` is
  deliberately not asserted. Both bound support volume, and settling it is a
  prerequisite for a fair APPR-versus-RPPR work comparison.
