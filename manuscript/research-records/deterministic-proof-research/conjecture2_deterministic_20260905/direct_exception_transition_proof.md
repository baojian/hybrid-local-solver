# Direct replacement of full exception records

This optional representation optimization preserves the integer corrector's
actual rounded trajectory. It does not alter projection, caps, numerical
updates, rebase arithmetic, schedule, or repair. Stable implementations and
the package are unchanged.

At each reporter query boundary a vertex belongs to exactly one tree.
Base keys are `b_i/d_i` with global positive scale `S`; exception keys store
the **full** numerical numerator `n_i=S*b_i+H*e_i`. The vertex registry
records the old kind, numerator, and degree. Removing a record uses this
stored key, not a value reconstructed from the new scale.

Between two queries the tree may contain a mixture of old and new full
exception numerators. It remains a valid ordered tree of those numerical
keys, but it is not yet queried as the new raw vector. The transition is
completed before the next projection or any checkpoint can run.

Let `E_old` and `E_new` denote the old/new source-kinetic exception sets,
and `T` the touched base-response indices. In a non-rebase step:

1. Vertices in `E_old \ E_new` are moved to their current base keys.
2. Touched vertices outside both sets have their base key updated.
3. Every vertex in `E_new` receives its full new exception numerator
   directly, replacing its registered old record if one exists.

The first two cases cover all base vertices whose key or classification
changed. The third covers every final exception. An untouched base vertex
outside these sets still has its unchanged valid base key. Newly exposed
records start with a zero base key; if affected by a primal scatter they
are touched, and if affected only by the new kinetic neighbor sum they
belong to `E_new`. Thus no new exposure is omitted.

A scalar rebase retains the original paid full base-key rebuild followed
by exception installation. Hence at every query boundary both trees and
their disjoint registry represent exactly the same keys as the stable
implementation. Projection uniqueness and the identical integer numerical
updates prove exact trajectory equivalence by induction. Tree shapes and
operation counters may differ.

All membership passes visit old/current kinetic-source supports and touched
neighbors, with their existing deterministic AVL logarithmic cost. Their
sum is still bounded by `O(W+K/r)` logical point operations for a stage,
where `W` is cumulative kinetic volume. The full rebase cost is unchanged.
Old temporary sets are reclaimed within the same support charge. No graph
call or reporter root query is introduced during a transition.

The optimization can avoid an exception-to-base-to-exception round trip
for persistent exceptions. This is a possible constant-factor improvement;
it is not presumed faster until measured. Independent tests and audit are
pending.
