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
vertices in the true RPPR support.  The remaining cost issue is maintaining
the next event inside a large biconnected cyclic core without refreshing its
entire boundary after every activation.

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
slope at least `alpha`.  For a block-incidence graph whose biconnected blocks
have size at most `q`, lazy scalar block responses yield the exact,
condition-free bound
`O~(q^3 / (rho sqrt(alpha)))`.  Thus trees with bounded-size cyclic gadgets
glued at articulation vertices are closed at the product scale.  A large
biconnected core remains open; treewidth alone is insufficient for this
argument because an arbitrarily long cycle has width two but unbounded block
size.

The supplied-support condition has also been removed on arbitrary graphs for
correctness and locality.  An exact boundary-violation gate admits only
vertices in the true RPPR support and terminates at the exact optimum.  It costs
`O(|S*| vol(S*)) = O(1 / rho^2)` with fresh tree elimination.  This already
matches `O(1 / (rho sqrt(alpha)))` when `rho >= sqrt(alpha)` and supplies a
separate monotone correctness proof; supplied width-`w` intermediate
orderings give `O((w + 1)^2 / rho^2)`.  Lazy tree and bounded-block responses
give the sharper product bound in the fine-regularization regime.

Build from this directory with:

```bash
make
```
