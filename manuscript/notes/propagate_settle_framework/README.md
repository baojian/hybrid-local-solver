# propagate_settle_framework

This standalone note extracts a common theoretical framework from the
measured `two_rung_sor`, `rlsor_terminal_exact_rung`, and
`frontier_adaptive_ladder` methods.

The central proved fact is an absorption law for exact settlement.  Once the
outside coordinates and the settled region are fixed, an exact restricted
solve erases every over-relaxation, ordering, and signed-packet decision made
inside the region.  For nested regions, smaller settlements are absorbed by
the larger one.  Thus the settled trajectory is determined only by the
sequence of discovered regions; over-relaxation can help only through region
discovery or its work cost.

The note also proves an exact defect identity for an inexact delivery phase
and a trajectory-sensitive work theorem.  The relevant structural quantity is
the settled-volume revisit factor

`R_set = sum_k cvol(U_k) / cvol(U_K)`,

not the raw number of batches.  Exact RPPR boundary expansion therefore costs
`O((w + 1)^2 R_set / rho)` under supplied width-`w` orderings.  The desired
product scale follows from the strictly weaker target
`R_set = O_tilde(1 / sqrt(alpha))`, even when the number of small early
batches is larger.  This quantity is the theoretical analogue of the adaptive
frontier solver's measured work-per-touched-support ratio.

The note now proves that a log-free graph-uniform revisit bound is false for
the literal exact boundary gate.  A four-vertex tailed triangle has two
activation batches in the same root-distance shell.  A width-two tailed fan
extends this to any prescribed number `L` of singleton batches, all among
distance-one vertices, and forces `R_set > (L + 1) / 5`.  With a quantitative
choice of the fan size, this gives the intrinsic lower bound
`R_set = Omega_alpha(log(1 / rho))`.  Thus constant elimination width and
constant support radius do not remove the dynamic-range logarithm.

The polylogarithmic revisit target remains open in thick, large biconnected
cores and is consistent with the fan obstruction.  The alternative is to
retain incremental Schur state, as the path, tree, cycle, and bounded-block
algorithms in `delayed_reflection_ladder` already do.

The note now makes that alternative exact.  Cumulative settled volume equals
a charge-weighted activation age: each vertex is charged once for every fresh
settlement after it enters.  A lazy block-Schur update stores the correction
to old coordinates and updates remaining violation demands through one signed
Schur block-column.  On the same tailed fan that forces a logarithmic fresh
revisit, a two-coordinate separator reproduces the identical first $L$
batches and exact restricted solution in $O(m+L)$ work, versus
$\Omega(mL)$ for fresh settlement.  Thus the lower bound isolates a
state-maintenance cost rather than an information-theoretic discovery
barrier.

This fan mechanism now has several rigorous structural generalizations.

- A charged online activation-aligned presentation with live frontal size
  `zeta` and at most `nu` exact signatures reproduces every gate batch in
  `O((1 + zeta^2 + nu zeta) cvol(S) + T_sep)` work.  The note explicitly
  charges separator discovery and states the exact metadata/access model.
- A kinetic threshold theorem removes the `nu` term when distinct demands
  cross zero in a stable scalar order.  It gives an exact
  `O(cvol(S) log(2 + R))` online solver on rooted spiders even if all `R`
  frontier responses differ.
- A certified low-rank response tree replaces exact row equality by interval
  certificates and refines only clusters whose KKT sign is ambiguous.

The flat structural condition cannot be removed graph-uniformly.  A proved
constant-degree expander family has full RPPR support but forces
`zeta, nu = Omega(n)` in every activation-aligned presentation.  This is a
framework obstruction, not a lower bound against all algorithms.

Two representation-specific cyclic obstructions sharpen that conclusion.
Original-basis multifrontal or Cholesky hierarchies that explicitly store
their exact fronts require `Omega(n^2)` entries on bounded-degree expanders.
On sparse cyclic Stieltjes systems, arbitrarily light singleton cascades make
every remaining boundary demand change, so an eager exact-demand array also
requires `Omega(n^2)` updates.  Neither result rules out compressed, lazy, or
matrix-free state.  Positively, a stable exposed block--cut presentation with
block size `b` supports an exact response-generated solver whose route cost is
quadratic in `b`; polylogarithmic blocks reach the product scale when the
presentation itself can be maintained within that budget.  The companion
`delayed_reflection_ladder` note now removes this metadata assumption for
bounded blocks.  Activating zero-valued vertices preserves all consumed
response prefixes, so online block mergers rebuild only future iterator state
and retain the same product scale under ordinary adjacency access.

The universal hybrid proof is now reduced to one precise response step.
Exact Schur algebra is used until `zeta = ceil(alpha^(-1/4))`, which costs at
most `O(cvol(S) / sqrt(alpha))`.  A per-event shock-only repair bound is
proved false: a tiny singleton shock can require a linear next-batch output,
and full-sweep AG/Chebyshev/CG still need one old-face pass as the shock tends
to zero.  However, the note now proves that all numerical repairs in an epoch
can be deferred to one final accelerated solve.  With an independently
maintained exact response certificate, heavy shocks bound the number of such
repairs.  Arbitrary rooted trees meet the intended product bound through a
different exact response-generated trace, without claiming that trace equals
the literal boundary gate.  Within the exact-gate hybrid route, the remaining
universal claim is light-shock response maintenance on nonequitable cyclic
cores, with every old-face read and response query explicitly charged.

For approximate output, the note proves a strictly weaker reduction.  If
every exact boundary demand is certified to additive normalized error
`alpha * tau_gate / 4`, admitting only estimates above the corresponding
finite threshold remains support-safe and terminates with degree-normalized
solution error at most `tau_gate`.  One final accelerated solve adds
`tau_sol`, while RPPR regularization contributes `rho`.  Thus a certified
finite-band response oracle would give
`O_tilde(1 / (epsilon * sqrt(alpha)))` work by taking all three errors as
`epsilon / 3`.  Establishing that band-response oracle on general cyclic
cores is now the weakest sufficient unresolved theorem; exact zero-sign
maintenance is no longer necessary for this approximate target.

The response certificate is now weakened further.  Uniform point estimates
are unnecessary: certified lower endpoints suffice for admission, certified
upper endpoints suffice for termination, and only intervals intersecting the
transition band must be refined.  For any nested exact-face expansion, the
full exterior demand change has squared Euclidean norm at most twice the
objective shock.  Therefore boundary degree volume moving by normalized
margin `theta` is at most `2 * shock / theta^2`, with telescoping shock over
disjoint epochs.  The remaining cyclic problem is an output-sensitive
heavy-change reporter for these energy-packed crossings, not a full boundary
refresh.

Build from this directory with:

```bash
make
```
