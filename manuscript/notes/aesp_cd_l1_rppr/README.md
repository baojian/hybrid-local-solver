# AESP-CD RPPR note

This standalone note develops a composite AESP outer loop with local proximal
coordinate descent for the shared regularized PageRank model. The proof source
is `main.tex` and its included sections; [`STATUS.md`](STATUS.md) is the
current claim ledger and handoff.

The oracle-free end-to-end contract is the canonical point-source problem
`s=e_v`.  The shared definitions remain general.  Linearity extends a proved
point-source PPR solver to a sparse distribution with work
`nnz(s)+O_tilde((sum_v sqrt(s_v))^2/(sqrt(alpha)*eps_ppr))`; it does not give
the formerly requested additive `nnz(s)` bound.  RPPR obstacle solutions do
not superpose.  Point-source lower publications are, however, automatically
rooted and connected, so no multi-source component-merge reporter is needed.

The note proves the local KKT-mass and relative-oracle interfaces, safe lower
centers and retraction, fixed-envelope locality, finite residual identities,
several exact trajectory calibrations, and an unconditional accelerated result
on the a-posteriori high-Dirichlet class. It also records sharp failures of
raw correction counting, Euclidean-only collateral packing, black-box
shadowing, and the simplest unsplit lagged energy bank.
The finite-inner comparison is now sharp at the root-potential level:
`sqrt(Phi_(t+1)) <= sqrt((1-q) gamma_t Phi_t) + sqrt(kappa_A) xi_t`.
This removes the artificial `xi_t <= 1` restriction and improves the
conditional absolute polish from a `theta` scale to a `sqrt(theta)` scale;
it does not prove the missing net packing inequality.
On the exact settled optimal face, a new cross-normalized error/velocity bank
contracts by `1-q` on every correction-free stage and by a constant after a
`Theta(1/q)` post-full window. It passes the previous K2 low-mode STOP; its
unpaid term is now the explicit correction forcing in a `Q_A^(-1)` norm. A
reachable complete-graph family proves that no graph-uniform constant can pay
that forcing from net high-band decrease alone: the required ratio is
`>(N-1)/23`. The surviving exact fixed-face interface is instead a
contract-or-spend window: after `Theta(1/q)` stages the bank contracts by a
constant unless it spends a telescoping low Euclidean endpoint drop.
A fully rational-interval `P24` trajectory additionally proves that paying
the low forcing by net high-band drop plus `6/5` times the starting low bank
still fails; its certified required coefficient is greater than
`1.206959416`. This narrows the viable interface to the unsplit endpoint
spend or an adaptive event allowance.
An alternative Moreau-Hessian bank has a correction-event forcing metric with
condition number below `4(1+q^2)`.  For an explicit nested-face epoch protocol
that expands only at boundaries and restarts momentum at the unchanged primal
point, it gives a geometric root-potential ledger: face-optimum gains and
correction masses are injected once and earlier events are automatically
discounted.  This is not yet an event-packing theorem for the automatic
per-stage admission trajectory.
Keeping the correction cross term gives a sharper signed increment `Xi_t`.
Only `[Xi_t]_+` enters the refined epoch ledger, and its fixed-face sum has a
telescoping Stieltjes payment without the former geometric `1/q` loss. A
reachable `P3` event proves that `Xi_t` can nevertheless be positive and can
increase the bank, while the reachable `K8` family makes the telescoping
payment asymptotically tight.  An exact settled `S5` trajectory has adjacent
positive partial/full events and grows the bank across the pair, so even a
mandatory one-step quiet gap is false.  On the positive side, every graph
family with a proved clipped-master inequality has a mean-free Moreau bank
that contracts by a factor at most `3/8` in `ceil(log(2)/q)` exact fixed-face stages,
independently of event density.  The remaining pulse obstruction is therefore
concentrated in the constant low mode.  This high-bank estimate now has a
finite-inner root perturbation with a discounted residual budget.  For the
low mode there is an exact dichotomy: mean overshoot contracts its Moreau bank
by `1-q` in one step, while every non-overshoot correction is forced by the
infinity norm of the mean-free trial residual.  Combining the master high
root with the exact forced mean recurrence gives a two-scale epoch potential:
a quiet `ceil(2/q)` same-point-restart epoch contracts it below `0.407`, and
an epoch whose observable weighted mean deficit is at most one quarter still
contracts by `3/4`.  A sharper arbitrary-history low-root gate halves the
two-scale potential on every accepted `ceil(2/q)` window, and it retains an
explicit finite-inner residual allowance.  Independently, an observable
pure-prox alignment warmup reduces the high/mean residual ratio by
`(1+q)^(-J)`; once its computable threshold is crossed, the entire exact
global-momentum tail is permanently correction-free.  This gives a genuine
fixed-full-face accelerated route with `O(1/q)` warmup up to logarithms,
without lower eigendata.  A reachable `K_N` family proves that high-to-low
transfer cannot be paid by a graph-uniform high-bank coefficient: even after
a `1/q` rescaling the required coefficient is greater than `(N-1)/15`.
Thus a local, infinity-norm, or volume-sensitive payment for the weighted
mean deficit is still needed.
On a fixed certified face, the inner-work obstruction is now removed:
Chebyshev semi-iteration may use signed scratch vectors, after which a
Stieltjes retraction and coordinatewise maximum with the old safe checkpoint
publish a monotone lower certificate. A small shift therefore costs
`O_tilde(vol(A)/sqrt(lambda_lower))`, and a certified final RPPR face can be
solved directly in `O_tilde(1/(rho*sqrt(alpha)))` work. Requiring every
scratch residual to remain nonnegative provably loses this acceleration, and
fixed-rank low-mode deflation is blocked by arbitrarily high multiplicity
near-ground clusters. The remaining end-to-end issue is face discovery,
certification, and replay rather than the terminal linear solve.
That boundary is now sharper. Full-graph Chebyshev scratch can carry constant
`l2` mass on an exponentially large regular-tree frontier at degree
`Theta(1/sqrt(alpha))`, so unrestricted signed scratch is not automatically
local even when the final obstacle support is one vertex. Conversely, if
every restricted face exposes a margin-certified boundary batch of volume at
least `gamma*vol(A)`, safe restricted solves and scans geometrically sum to
`O_tilde(vol(S*)/(gamma*sqrt(alpha)))`. Endpoint paths give the matching
structural STOP: a boundary-only protocol may expose one vertex per batch and
pay quadratic cumulative face volume. Across an explicit same-point face
replay, the sharp graph-uniform Moreau root-shock coefficient is `2` (energy
coefficient `4`), so the existing root convolution has optimal scale.
The singleton path STOP is not informational.  An append-only scalar
`LDL^T` message evaluates each new boundary key in constant time and performs
only one terminal back substitution, giving output-linear discovery work.
The block Schur identity shows what must replace this message on a general
graph: an implicit dynamic response applying the old inverse to every new
coupling block and refreshing affected boundary queries.  Fixed-rank Krylov
recycling does not suffice for arbitrary new coupling directions.
On forests this interface can be realized by top-tree Schur summaries:
each link, active/pinned toggle, or named KKT query changes only logarithmically
many two-port quadratic messages.  A supplied width-`w` junction tree gives
the analogous `O((w+1)^3 log B)` update.  This is not yet an end-to-end
frontier oracle: the number `Q` of named pinned-coordinate queries remains an
explicit charge and can be quadratic under repeated full-frontier rescans.
For a stable fixed separator of dimension one or two, a kinetic threshold
heap or planar extreme-point reporter closes this query term in near-linear
work; the general fixed-dimensional statement is an explicit dynamic
extreme-point interface. Balanced forest messages also have a certified
finite-precision implementation under a nonzero KKT gap. Exact rational
messages do not have polylogarithmic bit size in general: a constant-condition
tridiagonal family already produces endpoint fractions with linearly many
bits.
For one positive root load on a promised tree, the query interface closes
completely: scalar child responses propagate the next exact activation
threshold to the root, so every emitted singleton has a currently positive
boundary key and the first failed root comparison is the global obstacle KKT
certificate.  The same exact-real argument extends to single-source
unicyclic graphs by paying for explicit scans of the unique cycle, whose
length is bounded by the support radius.  The total literal-admission work is
`O_tilde((1+vol(S*))/sqrt(alpha))`, hence
`O_tilde(1/(rho*sqrt(alpha)))` for RPPR.  Independent rational audits cover
negative internal intercepts, competing branches, threshold ties, and exact
zero.  Persistent transfer products and static dormant-run hulls further
close cactus traces having only polylogarithmically many productive descendant
sites per cycle, even when arbitrarily many immutable live thresholds remain.
Epoch rebuilding removes that hypothesis with the unconditional
instance-sensitive block charge
`O_tilde(L_B + J_B*min{p_B+1,sqrt(L_B)})`, strictly improving a full block scan but not
yet reaching the radius--volume target on every cactus; it does reach that
target whenever every root route has
`sum_B min{p_B+1,sqrt(L_B)}=O_tilde(R*)`.  The
bounded-productive result includes chains of arbitrarily long cycles.  The smallest still-open
structural reporter is a cactus trace with unbounded productive sites in
unbounded ancestor cycles, and more
generally a variable-port series--parallel graph.  A three-vertex two-source
example shows why running
independent single-root copies does not handle component mergers.
A small-`rho` connected-prefix realization lemma makes the square-root
separation reachable by a legal RPPR singleton trace; it stops the literal
flat rebuild-and-scan interface, not multilevel reporting or another legal
batch order.  A matching static-cluster interface proposition makes this
boundary explicit: without bulk affine pullback or hull meld, an adversarial
`Theta(sqrt(L))`-event phase costs `Omega(L)` even though this is not an
algorithmic lower bound.
Even the exact Schur objective decrease cannot pay a fixed amount per
admission: an exact two-vertex RPPR family has a strict admission whose gain
tends quadratically to zero.  Thus gain-only charging needs an explicit
relative margin or a different potential.  With a declared batch-density
gate, the repair is exact: `||g_W||^2 >= 2 eta L work(W)` makes the Schur gain
at least `eta work(W)`, so accepted batch costs telescope.
If the final closed block tree, its weighted heavy--light decomposition, and
balanced series--parallel parses are supplied offline, whole heavy paths can
instead be rebuilt as chain-cactus superblocks and the full post-closure
cactus reporter meets the radius--volume product.  Making those decompositions
online is already possible for an immutable core revealed as one contiguous
prefix by binary-counter SP merges.  Interleaved closure and response updates,
and dynamic heavy-path changes, still require the unresolved persistent
cut/concatenate and bulk pullback/meld interface.
A separate quantitative result reduces uniformly separated RPPR boundary
keys to monotone coordinate-level events.  This is soft-linear only when the
level-event source is itself charged; ordinary point-query Schur messages do
not reveal those crossings automatically.  An exact RPPR P4 witness rules
out fixed factor-two bins.
For the remaining series--parallel interface, fixed-mark Schur updates and
named cycle responses are logarithmic.  A conditional reduction isolates the
missing object as a persistent affine hull supporting bulk pullback and meld.
The pullback alone is structured: nonnegative two-port Schur maps act on
normalized row slopes by an order-preserving/reversing Möbius map, so one
child hull can keep a lazy projective view.  These views compose as fixed
$3\times3$ homogeneous matrices, so an entire series chain remains
constant-size.  The unresolved operation is the
meld and strict argmax across differently transformed, arbitrarily
interleaving child hulls.
If every sibling pair instead has disjoint pulled-back slope intervals, one
bridge tangent gives a logarithmic persistent meld; this is a clean
structural GO, but not a general reporter.
The condition is observable from the two lazy endpoint images at every
changed meld, so the fast branch can be guarded online and abandoned safely
when the intervals overlap.
Separately, exact all-positive batching cannot be charged just to support
radius.  An explicit point-source fan family has every graph vertex at radius
one but needs at least $m/2-1$ nonempty simultaneous batches on $m$ path
vertices; an eight-vertex exact instance additionally realizes five strict
singleton batches.  Thus the point-source restriction removes component
mergers, not serial boundary activation around one root.
Nor can the nonlinear obstacle be replaced by one ordinary-PPR sweep: an
exact point-source path has an active RPPR coordinate where the corresponding
unconstrained shifted PPR coordinate is strictly negative.
Parametric point-source homotopy gives a sharper algebraic interface: after
one admission, every surviving critical threshold is a nonnegative weighted
average of its old value and the admitted maximum.  The thresholds therefore
move monotonically, but a six-vertex exact trace reverses two candidates'
priority order.  A plain lazy heap is insufficient; the remaining reporter
must support nonuniform rank-one mixtures.
Keeping the complete exterior Schur complement turns that identity into an
exact ratio-pivot homotopy algorithm: every support coordinate enters once,
and the target support is certified when the largest remaining ratio falls
below $\rho$.  Its discovery work is
$\widetilde O(\vol(S^\star)+\sum_w(1+\delta_w)^2)$, where $\delta_w$ is the
actual Schur-fill degree at pivot $w$.  Bounded homotopy width therefore gives
a genuine product-scale point-source solver after the final-face Chebyshev
step.  Explicit fill can still be quadratic (already at a high-degree root),
so this is a new structural GO rather than the universal theorem.
Linear pivot-path length for K-matrix LCPs is classical
([Foniok--Fukuda--G\"artner--L\"uthi](https://arxiv.org/abs/0807.1249)); the
new role here is the point-source $\rho$-ratio parameterization, sparse-fill
ledger, and finite-error contract, not the number of exact pivots alone.
At a single requested $\rho$, this simplifies further: maintain only the
scalar restricted residual $g_v=A_v-\rho B_v$, pivot any certified-positive
row, and stop when all certified upper residuals meet the normalized KKT
tolerance.  Point-source locality makes this row discovery complete because
every nonroot row not yet adjacent to the support still has strictly negative
load.  Thus the weakest missing universal interface is now a dynamic
one-sided residual reporter; separate ratio vectors are needed only for the
full $\rho$-homotopy.
The same homotopy has a margin-free approximate stopping rule:
$\alpha d_v\leq B_v\leq(1+\alpha)d_v/2$, so an additive upper error
$\eta$ on the largest remaining critical ratio costs at most
$(1+\alpha)\eta/2$ in the normalized KKT diagnostic.  Exact support and
exact breakpoint separation are therefore unnecessary at the requested
finite accuracy.
A certified interval version makes the remaining approximation contract
explicit: rowwise pair radii of order $\alpha\eta d_v$ suffice for additive
ratio accuracy $\eta$, and the reporter may safely pivot, stop, or refine a
gray row.  A two-by-two exact witness shows why a generic two-sided spectral
Schur approximation is not already such a certificate: an
$\varepsilon$-spectral perturbation can replace a positive updated breakpoint
by zero.  Approximate elimination therefore still needs a rowwise one-sided
error conversion; this is the present general-graph bridge.
This distinction matters when importing near-linear
[approximate Gaussian elimination](https://arxiv.org/abs/1605.02353),
[spectral vertex sparsifiers](https://arxiv.org/abs/1506.08204), or their
[dynamic variants](https://arxiv.org/abs/1906.10530): those papers certify
spectral/energy behavior, while the ratio-pivot stop needs simultaneous
one-sided row intervals.  Whether those tools can be augmented to supply the
intervals at local cost is now the precise open interface.
An exact RPPR theta core proves that one direction-free scalar threshold is
insufficient, while a weighted fan has a quadratic-size explicit obstacle
response table; neither statement is an algorithmic lower bound.
The closest dynamic-data-structure results do not currently supply that
combined interface.  [Top trees](https://arxiv.org/abs/cs/0310065) give
logarithmic structural updates once a composable cluster summary is provided,
and [dynamic treewidth](https://arxiv.org/abs/2504.02790) maintains a bounded-
width decomposition and declared dynamic-programming state.  The
[dynamic planar convex hull](https://arxiv.org/abs/1902.11169) supports
insert/delete and extreme-point queries in one global coordinate frame, while
[dynamic hulls for simple paths](https://doi.org/10.4230/LIPIcs.SoCG.2024.24)
add restricted deque/concatenate structure.  Their stated operation sets do
not yield arbitrary hierarchical affine pullback together with persistent
hull meld/split and strict labeled argmax.  Thus these papers validate the
neighboring ingredients, but using them here still requires a new reduction
or a stronger reporter theorem.
[Kinetic/dynamic hulls](https://doi.org/10.1016/j.comgeo.2006.01.002) also
allow points with declared bounded-complexity trajectories and individual
flight-plan changes.  A Schur update, however, changes the pulled-back
trajectory of an entire dormant cluster at once; treating it as one flight-
plan update per row reproduces the very materialization charge at issue.
Speculative coordinate-envelope doubling gives a second conditional route:
its solves geometrically sum to
`O_tilde(vol(U_final)/sqrt(lambda_floor))`, but `U_final` includes inactive
halo and need not be controlled by `vol(S*)`.  A margin-free clip-or-pay
retraction now converts feasible accelerated projected-gradient scratch into
an order-safe obstacle subsolution in the required
`O_tilde(vol(U)/sqrt(alpha))` work.  It charges each unsafe coordinate either
to its small primal value or to its residual, so strict complementarity is no
longer needed for this fixed-envelope primitive.  Strict margins remain useful
only when the exact active face itself must be identified.  High-degree
inactive decoys and dynamic boundary reporting still remain.
The RPPR support cap nevertheless gives a universal retained-volume result:
by keeping at most `1/rho` inactive halo volume in addition to the true active
support, an exact dynamic obstacle protocol never retains more than `2/rho`
volume. This is a partial affirmative answer, not an accelerated solver: all
serial updates and frontier reports remain charged to the explicit quantity
`W_DS(2/rho)`. A subcubic exact audit shows that naive factor-two speculation
can already explore `26/9` times the final support volume. Once discovery has
certified the final positive face, carrying no momentum through admissions
and restarting only once gives the q-free bridge
`C_rst <= 4(F(z)-F(x*))`.  On a general proper final face this composes
directly with the safe Chebyshev terminal solve.  The master/mean accepted
windows and alignment tail require their additional constant-mode, spectral,
and face-stability certificates; the bridge does not manufacture them.
The common-cap truncation ledger is also joint: correction and surviving
momentum `Q`-energies share one copy of the telescoping energy drop.

The live target is to batch and certify face discovery, pack failed
proper-face windows, and charge changing-face replays.
No graph-uniform exact accelerated solver or unconditional
`O_tilde(1/(rho*sqrt(alpha)))` end-to-end theorem is claimed. In particular:

- the abstract ledger witness is not an RPPR instance or an exact-proximal
  trajectory;
- the finite P4/P7 traces prove no infinite periodicity and no finite-inner
  work theorem;
- the fixed-P4 theorem refutes a horizon-uniform inflation bound while its
  primal error still converges geometrically, so it is not a net-exponent
  counterexample;
- the retraction discontinuity is a STOP for black-box shadowing, not a
  counterexample to direct finite-sequence packing or a graph-uniform solver
  theorem;
- entry-dominated stages and persistent-row energy now have explicit charges,
  but converting the event-level low-progress spend into a changing-face
  accelerated net exponent remains open.

An exact settled `P96` trajectory also shows why the new gate cannot be
replaced by a raw half-contraction assertion: its total Moreau bank retains
more than `0.54` after exactly `1/q` transitions, with the low component
retaining more than `2/3`.

Build the note from the repository root with:

```bash
make -C manuscript/notes/aesp_cd_l1_rppr
```

Run all twenty-four exact audits with:

```bash
uv run python -m experiments.proof_audits.runner \
  --tier full --note aesp_cd_l1_rppr
```

Their durable IDs are:

- `aesp_cd_l1_rppr.safeguarded_outer_ledger` (Round 022 provenance);
- `aesp_cd_l1_rppr.fixed_operator_p4_tail` (Round 023);
- `aesp_cd_l1_rppr.retraction_and_fixed_face` (Round 024);
- `aesp_cd_l1_rppr.boundary_shielding_filter` (Round 025);
- `aesp_cd_l1_rppr.persistent_q_energy` (Round 026);
- `aesp_cd_l1_rppr.weighted_reserve_boundary` (Round 027);
- `aesp_cd_l1_rppr.windowed_cross_normalized` (Round 028);
- `aesp_cd_l1_rppr.p24_low_start_stop` (Round 029);
- `aesp_cd_l1_rppr.signed_event_stop` (Round 030);
- `aesp_cd_l1_rppr.adjacent_signed_event_stop` (Round 031).
- `aesp_cd_l1_rppr.p96_full_face_window_stop` (Round 032).
- `aesp_cd_l1_rppr.safe_chebyshev_face` (Round 034).
- `aesp_cd_l1_rppr.singleton_face_batches_stop` (Round 035).
- `aesp_cd_l1_rppr.s5_face_shock_sharp` (Round 036).
- `aesp_cd_l1_rppr.rppr_speculative_decoy` (Round 037).
- `aesp_cd_l1_rppr.dynamic_schur_forest` (Round 038).
- `aesp_cd_l1_rppr.bounded_degree_speculative_stop` (Round 039).
- `aesp_cd_l1_rppr.tree_singleton_threshold` (Round 040).
- `aesp_cd_l1_rppr.separated_level_reporter` (Round 041).
- `aesp_cd_l1_rppr.variable_two_port_stops` (Round 042).
- `aesp_cd_l1_rppr.radius_batch_stop` (Round 043).
- `aesp_cd_l1_rppr.obstacle_clip_retraction` (Round 044).
- `aesp_cd_l1_rppr.accelerated_support_spill` (Round 045).
- `aesp_cd_l1_rppr.point_source_scope` (Round 046).

The full tier includes the optional P7 corroborating trace. These audits check
the scoped exact identities and source guardrails; they do not promote the
open graph-uniform theorem.
