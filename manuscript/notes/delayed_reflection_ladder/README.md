# delayed_reflection_ladder

This standalone note develops the theoretical direction suggested by the
measured alternating exact-rung R-LSOR policy.  It proves the exact
optimal-SOR reflection identities, derives the alpha-scaled ladder bases
needed for asymptotic no-reactivation, gives a residual-splitting invariant
for delayed reflection debt, and audits the idea against the project's
long-spider obstruction.

The note now proves the exact-debt half of causal pair locality.  A single
restricted block correction annihilates all interior residual.  It is
computable in `O(vol(S))` work on a discovered forest and in
`O((w + 1)^2 vol(S))` work under a width-`w` elimination ordering, including
the boundary certificate.  Exact block cleanup erases all relaxation history
inside a fixed region, so acceleration can only come from discovering that
region sooner.  The note also proves that a supplied forest RPPR support
admits an exact terminal rung in `O(1 / rho)` work for a single seed.

The remaining conditional step for unrestricted graphs is no longer support
correctness.  Fixing the seed value produces one monotone piecewise-affine
active-set homotopy on every graph, and an exact boundary gate admits only
vertices in the true RPPR support.  Its actual work is
`O((w + 1)^2 (J + 1) vol(S*))`, where `J` is the realized number of nonempty
boundary batches.  The remaining cost issue is controlling `J`, or
maintaining the next event without refreshing the entire boundary, inside a
large cyclic core with no other thin structure.

The companion `propagate_settle_framework` note sharpens this ledger: fresh
settlement actually costs
`O((w + 1)^2 sum_j vol(U_j))`, so it is enough to bound cumulative settled
volume by `O_tilde(vol(S*) / sqrt(alpha))`. This revisit-volume target is
strictly weaker than bounding `J` and directly mirrors the adaptive frontier
solver's measured work-per-touched-support ratio.

That companion note also proves the log-free version false for the literal
gate: a width-two, radius-two tailed fan forces arbitrarily many singleton
activations in one distance shell and
`R_set = Omega_alpha(log(1 / rho))`.  Thus a surviving gate theorem must retain
a polylogarithmic dynamic-range factor, or replace fresh solves with retained
Schur state.

The gate now has a quantitative convergence theorem as well.  Each enlarged
restricted solve dominates one unit proximal-gradient step, so its objective
gap contracts by `1 - alpha`; if `delta_*` is the smallest positive optimum
coordinate, this gives an exact instance bound
`O(1 + alpha^(-1) log_+(1 / (d_o delta_*^2)))` on the number of batches.
This route cannot by itself yield acceleration: on the three-vertex endpoint
path the first-batch gap ratio tends to
`(1 - alpha)^2 / (1 + 6 alpha + alpha^2) = 1 - 8 alpha + O(alpha^2)` as
`rho -> 0`.  The note also gives the exact tied-batch Schur formula, showing
that simultaneous activations update all remaining slacks through one signed
Schur block-column.  Hence the open accelerated argument must exploit finite
support discovery or compressed event maintenance, not a generic
`1 - Theta(sqrt(alpha))` energy contraction.

For the RPPR continuation path
`rho[k + 1] = lambda(alpha)^s rho[k]`, the note proves a sharper supplied-
support ledger.  Since `vol(S*(rho[k])) <= 1 / rho[k]`, all exact bounded-width
rungs together cost `O((w + 1)^2 / (rho_final sqrt(alpha)))`, with no extra
dynamic-range logarithm.  An output-sensitive support-discovery lemma would
therefore close the matching forest bound directly.

The path and symmetric-spider discovery case is now closed more strongly.
Forward Schur messages stop exactly at the RPPR boundary KKT condition, and
one reverse pass returns the solution in output-linear work.  On the same
path-bundle spider used for the persistent-support lower bound, this costs
`Theta(1 / rho)`, versus the restricted oracle charge
`Omega(1 / (rho sqrt(alpha)))`.  Thus a general lower bound must account for
directed elimination messages; the spider is not hard for that richer local
model.

For a general rooted tree, the note now proves that each child subtree sends a
continuous monotone piecewise-affine response to its parent.  The response is
zero below the explicit local activation threshold
`alpha * rho * sqrt(d_child) / (-Q_parent,child)`, allowing a whole inactive
branch to be pruned at its first edge.  The key general-tree problem is to
charge the child-breakpoint stream without copying inactive descendants.
The exact recursion is explicit: sum the child responses, form a strictly
increasing piecewise-affine map whose slope is a local Schur complement, and
invert it.  Its slope is bounded below by `alpha / (-Q_parent,child)`, so the
issue is representation and amortized merging rather than mathematical
stability.
Explicitly materializing all subtree response lists already gives an exact
`O(n^2 log(1 + max_degree))` solver on every finite tree.  The desired local
solver does avoid irrelevant copies: it requests response breakpoints lazily,
never enters a descendant of an inactive boundary vertex, and stops when the
root equation is solved.  A Chebyshev inverse-decay lemma bounds the exact
support radius by
`1 + O(log(1 / (alpha rho)) / sqrt(alpha))`.  Charging each realized
activation through its active ancestors therefore gives an exact,
condition-free
`O~(1 / (rho sqrt(alpha)))` degree-work bound on every finite tree, using
`O(vol(S*))` storage.  This closes the nonsymmetric branching-tree case.

The Chebyshev radius proof is actually graph-universal.  Cycles also preserve
a scalar ordered homotopy: conditioned on the root value, coordinates activate
monotonically and at most once, and the root equation has Schur-complement
slope at least `alpha`.  One activation changes every remaining affine slack
through one signed Schur-complement column, identifying the open maintenance
problem as a kinetic minimum under low-rank updates.  For a block-incidence
graph whose biconnected blocks
have size at most `q`, lazy scalar block responses yield the exact,
condition-free bound
`O~(q^3 / (rho sqrt(alpha)))`.  Thus trees with bounded-size cyclic gadgets
glued at articulation vertices are closed at the product scale.  The block
identifiers and rooted block-cut tree no longer need to be supplied.  With
ordinary adjacency access, a newly activated zero coordinate can merge
current blocks without changing any consumed response prefix; only the
affected future iterators are rebuilt.  Charging those rebuilds to the
activating incidences preserves the same `O~(q^3 / (rho sqrt(alpha)))`
bound.  Unbounded blocks are not automatically hard: reflection symmetry
reduces a whole cycle to a radial tridiagonal recurrence and gives an
output-linear exact solver.
More generally, every root-distance-equitable graph has an exact symmetric
tridiagonal shell quotient.  A lazy shell scan tests the next Schur demand
before scanning that shell, so it discovers, solves, and certifies the optimum
in `O(1 + vol(S*))` work without a support or radius oracle.  This permits
arbitrarily thick shells and includes cliques, complete bipartite graphs,
hypercubes, Hamming and Johnson graphs, and all distance-regular graphs.
The fast path is now certifying on an arbitrary graph: active-shell scans
audit the quotient identities, coordinatewise boundary violations either
prove termination or provide the exact safe gate batch, and any failed audit
falls back to the general boundary gate without risking correctness.

The one-cell-per-shell restriction is also removed.  If an equitable cell
partition has a tree quotient, the same orthogonal reduction
turns the graph obstacle problem into a tree Stieltjes problem.  Lazy cell
responses discover only active cells, scanning every active original
adjacency list once and paying one quotient-ancestor walk per cell event.
This gives the exact bound `O~(1 / (rho sqrt(alpha)))` with no support, radius,
or confinement oracle.  Several inequivalent thick cells may occupy one
distance shell, and the original graph may have unbounded treewidth and
arbitrarily large biconnected cores.  Cell identifiers no longer need to be
supplied.  Online rooted color refinement groups exposed labels by degree and
their incidences with scanned classes.  Indistinguishable cells have the same
next slack zero, activate as one tied bundle, and split only after the bundle
is safely scanned.  Smaller-half refinement plus persistent response forks
preserves the same product-scale work bound using ordinary adjacency access.
More generally, if at most `chi_*` exact-support vertices occur in any
root-distance shell, the condition-free gate costs
`O~((w + 1)^2 chi_* / (rho sqrt(alpha)))`.  This closes arbitrarily long
cycles and fixed-width cyclic strips.

For approximate output, the note now weakens the response requirement again.
A margin-adaptive gate needs only certified one-sided intervals: it admits a
label whose lower endpoint is safely positive, terminates when every upper
endpoint is below the allowed band, and refines only ambiguous intervals.
Nested exact-face corrections satisfy an exterior response contraction:
the squared change of all boundary demands is no larger than the primal
energy shock.  Hence boundary degree volume moving by normalized margin
`theta` is at most `2 * shock / theta^2`, and every scalar response leverage
is at most one. Source-aware leverage has now been reduced to an exact scalar
state: its square is the decrease of a terminal Schur diagonal across the
batch elimination. These losses telescope to at most `(1-alpha)/2` per
still-exterior label. A bounded-arity locator needs only a certified one-sided
aggregate estimate with additive error at the current pruning scale. A
Chebyshev inverse-square-root sketch constructs every exposed boundary loss at
a fixed face in `O_tilde(vol(S) / sqrt(alpha))` work; geometrically spaced
full checkpoints have the same final-volume product bound. What remains open
between checkpoints is narrower still: Chebyshev whitening of any
constant-factor spectral frontier prepares all Gaussian source probes in
`O_tilde(T_mv / sqrt(alpha))` work, without an exact frontier square root.
The same inverse square root also has a positive geometric ladder of shifted
exact rungs. Its total shifted work mass and monotone Schur-coordinate
settlement count are `O(1 / sqrt(alpha))`. Every rung is a sparse shifted face
system, and an unfinished solve is represented exactly by nonnegative anchor
debt whose later cleanup produces the shifted Schur residual. This turns the
source construction into a rigorous delayed-push mechanism rather than a
signed polynomial recurrence.
The companion response note now proves that arbitrarily many fixed-face debt
fragments may be summed before propagation and flushed by signed Chebyshev
semi-iteration in `O_tilde(cvol(T) / sqrt(alpha))` graph work. A computable
energy certificate restores simultaneous one-sided exterior intervals, so
signed variables remain strictly internal. This removes the one-edge
`Omega(1 / alpha)` factor for fixed-face realization and preserves the product
bound when there is one flush per geometrically growing face.
The same companion note proves that the literal exact gate cannot rely on
that schedule: a single-seed path can force singleton prefix admissions while
successive charged-volume ratios tend to one. Paths remain easy by scalar
response, so this is a scheduling obstruction rather than a work lower bound.
The companion `response_preconditioned_hybrid` note proves that small
normalized cut rank closes the target harmonic bank, and also gives the
linear-volume comb with full cut rank and rank-deficient energy error bounded
below independently of the comb length for fixed `alpha < 1`.
On a high-rank large core with neither bounded articulation blocks, an
equitable tree quotient, nor thin radial support, the remaining problem is now
an output-sensitive partial flush, or a different proved support-safe trace,
without rescanning the full boundary after every light update. Pure geometric
sleep for the literal gate is already refuted.

The supplied-support condition has also been removed on arbitrary graphs for
correctness. An exact boundary-violation gate admits only vertices in the true
RPPR support and terminates at the exact optimum. If every intermediate
induced graph is a forest, fresh tree elimination costs
`O(|S*| vol(S*)) = O(1 / rho^2)`; more generally, supplied width-`w`
intermediate orderings give `O((w + 1)^2 / rho^2)`. The forest bound already
matches `O(1 / (rho sqrt(alpha)))` when `rho >= sqrt(alpha)`, while the
arbitrary-graph theorem by itself is a monotone correctness result. Retaining
the realized batch count gives the sharper trajectory-dependent bound above,
so thin radial support also reaches the fine-regularization product scale.
Lazy tree and bounded-block responses cover branching structures whose shells
need not be thin.

Build from this directory with:

```bash
make
```
