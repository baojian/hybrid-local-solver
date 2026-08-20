# response_preconditioned_hybrid

This standalone note defines a common active-set interface for the project's
iterative and persistent-response solver lines. It does not claim that a mixed
method is universally optimal. Instead, it proves the generic block-response,
dual-local orthogonal-correction, boundary-interval, uniform-leverage,
response-energy-packing, monotone boundary-variation, geometric-rebuild, and
probe-before-rebuild lemmas and states a conditional
composition theorem whose two endpoints are the local iterative product scale
and an output-sensitive incremental SDD/Schur solver.

The proposed method stores a response representation for a settled anchor,
uses a frontier buffer for newly admitted vertices, performs aggregate
preconditioned repair, and materializes the old-face correction only at final
output. The unresolved graph-uniform ingredient is certified finite-band
boundary reporting on nonequitable cyclic cores; no uncharged boundary scan or
future-support oracle is hidden in the interface.

The no-restart numerical half is now closed conditionally on charged response
application. For every support expansion, the whole lifted Schur-frontier
space is energy-orthogonal to all earlier lifted frontier spaces. Consequently
arbitrary certified frontier-solve errors add exactly in quadrature, and the
settled face never needs to be optimized again. This does not hide the dense
lift: all applications of the old-face response remain in the explicit
`U_lift` charge.

Successive exact corrections on nested faces are `Q`-orthogonal. Their primal
vectors can be dense, but applying `Q` annihilates the whole old face and
leaves a dual signature only on the new batch and current boundary. This is
the precise surviving locality of an orthogonal evolving-set method. The
missing implementation must produce or query that dual signature from an
implicit response without materializing the dense primal correction.

Eliminating the settled face gives an exact positive dual-transfer operator
from the current batch demand to all exterior demand increases. This rewrites
support discovery as monotone threshold reporting for implicit nonnegative
Schur transfers; it is a narrower target than maintaining every primal
coordinate after every expansion. Schur associativity additionally proves
that any consecutive interval of light transfers may be replaced by one exact
aggregate transfer without changing its endpoint, exterior demands, or the
operator seen by future events. The remaining cost is representation and
crossing discovery, not trajectory correctness.

The boundary-variation ledger proves that every still-inactive normalized
demand is monotone and that all such motion has total degree-weighted mass at
most `(1-alpha)/2`. Thus exact keys cross a fixed threshold only once. The
remaining difficulty is to route an implicit dense Schur increment to all
crossing keys; publishing additive `alpha*tau` scalar updates merely recovers
the classical `1/(alpha*tau)` accounting.

A source-aware leverage theorem now exploits the fact that a nested correction
is generated on the newly admitted batch `B`. The squared exterior leverages
sum to at most `|B|`, yielding an a priori degree-volume bound on ambiguous
finite-band intervals without materializing the dense correction. A matched
edge construction shows why the older source-oblivious energy interval is not
enough: it can mark every boundary row ambiguous after a one-row change and
force quadratic refresh. A rank-sensitive locator lemma proves that a
bounded-arity hierarchy with constant-factor aggregate leverage-mass queries
finds all potentially ambiguous rows with probe count controlled by `|B|`,
the correction energy, and hierarchy depth---not by boundary size. The
remaining data-structural target is a local squared-response range-add that
implements those group traces on nonequitable cyclic cores.

The source-aware mass has now been identified exactly with a simpler object.
For a batch elimination `A -> A union B`, the squared leverage at an exterior
vertex is the decrease of that vertex's diagonal in the terminal Schur
complement. These diagonal losses telescope to at most `(1-alpha)/2` for each
still-exterior label, independently of the number of earlier batches. Group
masses are therefore weighted aggregate Schur-diagonal losses. The hierarchy
needs only a certified one-sided estimate with additive error proportional to
its current pruning threshold; multiplicative accuracy on tiny groups is not
required.

The diagonal-loss ledger and the orthogonal correction-energy ledger combine
multiplicatively. Over any epoch in which an exterior label remains asleep,
its normalized response uncertainty is at most the square root of the
accumulated diagonal loss times the accumulated correction energy. Summing
over disjoint wake-up epochs gives a second Cauchy--Schwarz telescope. For a
unit seed, the total correction energy is at most `alpha`; since the total
diagonal loss of label `v` is at most `(1-alpha)/(2*d_v)`, wake-ups at margin
`Theta(alpha*tau)` occur at most
`O(1/(tau*sqrt(alpha*d_v)))` times per label. This is a proved response-side
`1/sqrt(alpha)` mechanism, not a global running-time theorem: summing over all
live labels can still be too expensive, and maintaining the diagonal-loss
ledger is precisely the unresolved operation.

There is also an exact route from that operation to spectral graph machinery.
After scaling by `D^(1/2)`, the PageRank matrix becomes the grounded Laplacian
`((1-alpha)/2)*(D-A) + alpha*D`: original graph edges have conductance
`(1-alpha)/2`, and every vertex has a ground edge of conductance `alpha*d_v`.
Schur complements, diagonal losses, and normalized exterior responses respect
this congruence. The dynamic spectral-vertex-sparsifier and electrical-flow
locator of van den Brand et al. therefore supplies a concrete construction
blueprint. Its published preprocessing, update, and query costs are global in
the ambient graph and do not prove the desired local bound; the new target is
to make its terminal/locator epochs exposure-charged and schedule them by the
two-ledger product rule.

At the information level, the ambient graph is no longer an obstacle. For a
current face, its response rows and diagonal losses depend only on the face's
internal edges, the cut incidences exposed by scanning its rows, and one degree
query per distinct boundary label. Edges wholly in the exterior do not enter
the formulas. The complete static locator record therefore has size linear in
charged exposed volume, and geometric anchor rebuilding makes all such static
builds near-linear in final volume, modulo the locator's parameter factor.
What remains open is the update/query cost between rebuilds, not acquisition
of the unexposed graph.

A fixed-anchor sketch identity further connects the two solver arms. For any
linear measurement matrix on normalized exterior dual demands, precompute its
transposed harmonic extensions through the anchor. An exact frontier solution
then updates the complete exterior sketch from frontier-incidence scans and
the touched rows of those stored extensions. Its known frontier source is
subtracted explicitly. No dense old-face correction or boundary scan appears.
This makes CountSketch, sparse-recovery, and hierarchy measurements concrete
backend candidates, while leaving the number of measurements, anchor solves,
stored-row reads, and within-epoch updates fully charged.

The complementary energy-packing ledger proves that the squared exterior
demand change across any nested exact-face expansion is at most the primal
energy shock. Boundary degree volume moving by normalized margin `theta` is
therefore at most `2 * shock / theta^2`, telescoping over disjoint epochs.
Every scalar response leverage is also at most `sqrt((1-alpha)/2)`, so
energy-certified repairs yield normalized queried intervals without
coordinate-specific leverage estimation. The open primitive is now precisely
an output-sensitive heavy-change reporter for these monotone, energy-packed
crossings.

The group-trace oracle has also been reduced to a concrete randomized object.
A logarithmic batch of source-normalized Gaussian response sketches estimates
all fixed hierarchy-node leverage masses simultaneously; branch and bound may
then use those estimates adaptively. The static lemma alone suggests retaining
signed sketches, but the adaptive theorem below replaces that unsafe reuse by
fresh per-batch randomness and nonnegative mass accumulation.

Across an adaptive support trace, fresh sketches are drawn only after the
current batch is fixed and their nonnegative squared masses are accumulated.
Conditional concentration and a summable failure budget make every prefix
valid. Energy-normalized frontier bases are mutually orthogonal, and a newly
exposed boundary vertex has zero response to every earlier basis, so neither
old probes nor old faces are replayed. The remaining primitive is a local
squared-response range-add on the live hierarchy. Equivalently, it can be a
dynamic additive aggregate Schur-diagonal-loss oracle, which removes the
random source dimension entirely. The sketch route is a Monte Carlo
reduction; deterministic or Las Vegas certification of discarded groups
remains an additional obligation.

The exact diagnostic backend is
`src/hybrid_solver_codex/response_hybrid.py`, with the reproducible comparison
driver `experiments/explore_response_hybrid.py`. It separates adjacency scans,
global boundary reads, dense response arithmetic, Schur construction,
frontier iterations, materialization, and output writes. It is a correctness
and switching oracle, not an output-sensitive implementation.

Build from this directory with:

```bash
make
```
