# Completed multipartite probe and its original proposal

Second-night update, 7 September 2026: the local discovery/event mechanism
and canonical-core/any-physical-seed extension are now implemented and
**Proved here** as drafts awaiting independent review. See
`LOCAL_MULTIPARTITE_PROBE.md`, `thm:op3-local-multipartite` and
`thm:op3-canonical-multipartite`. General OP3 remains **Open**. The supplied-
part audit below remains an algebraic reference; its saved source and output
retain their original historical scope.

The remainder records the first-night proposal, before this completion.

# Next bounded direction: multipartite core responses

Date: 7 September 2026. **Conditional / Open local extension.** The
following scalar reduction is now implemented as a supplied-part algebraic
reference and exactly audited; it is not an end-to-end local solver. The completed
clique theorem is `thm:op3-local-clique-pendants`; do not silently extend
its claim to this broader family.

## Why this is the next algebraic target

The clique solver succeeds because each original core row depends on one
aggregate S=sum(core values). A complete multipartite core seems to retain
that property after eliminating one aggregate per part. Unequal private
pendants add only one additional breakpoint to each coordinate response.
This route attacks a dense core with simple algebraic structure, separately
from reducing cycle rank or maintaining a generic approximate inverse.

Let the core have N vertices in parts C_g of sizes n_g, with at least two
nonempty parts. Core vertex i has t_i private leaves and original degree
d_i=N-n_g+t_i. The physical seed v is a core vertex. Let

`b_i=1_{i=v}-lambda*d_i`, `S=sum_i u_i`, `S_g=sum_{i in C_g}u_i`,
`T_g=gamma*(S-S_g)`.

Its exact core equation after pendant substitution is

`d_i*u_i-gamma*t_i*(gamma*u_i-lambda)_+ = b_i+T_g`.

Define the three-piece response psi_i(T): zero when b_i+T<=0;
(b_i+T)/d_i until that value reaches lambda/gamma; and

`(b_i+T-gamma*lambda*t_i)/(d_i-gamma^2*t_i)`

after the pendant birth. Both positive denominators are positive. The
breakpoints are T=-b_i and T=d_i*lambda/gamma-b_i; the second is irrelevant
when t_i=0. All slopes are nonnegative and nondecreasing.

## Eliminate the part aggregate exactly

Put F_g(T)=sum_{i in C_g}psi_i(T). The part equation is

`T/gamma+F_g(T)=S`.

The left side is strictly increasing onto the real line, so it has a
well-defined piecewise-affine inverse for every real S. Allow negative T
while constructing this algebraic inverse: at a trial S near zero, the
seed part can have S_g>S. At the final global fixed point, all part masses
are nonnegative and sum to S, so T_g=gamma*(S-S_g)>=0 automatically.
Discarding all negative T intervals at initialization would be incorrect.

On a piece F_g(T)=A*T+B, the resulting part response is

`G_g(S)=(gamma*A*S+B)/(1+gamma*A)`.

Transform a part breakpoint T_* to

`S_*=T_*/gamma+F_g(T_*)`.

Continuity makes this independent of the side used at a breakpoint, and
strict monotonicity preserves its order. Thus each original coordinate
contributes at most two events even after the part inversion. Sorting the
combined transformed events and maintaining aggregate affine coefficients
would solve

`S=sum_g G_g(S)`

in O(N log N) exact-word work on a **supplied** core description.

There is a uniform strict slope bound. Since
d_i-gamma^2*t_i>=N-n_g,

`A<=n_g/(N-n_g)`,
`G'_g<=gamma*n_g/(N-n_g+gamma*n_g)<n_g/N`.

Summing gives a slope strictly less than one, so the same exact breakpoint
root argument as in the clique solver applies. This is a finite sweep;
do not use the contraction factor as an iteration bound. A clique is the
special case of singleton parts, and the transformed formulas reduce to
the completed clique formulas, including the extra gamma on the diagonal.

## Local discovery: a concrete bipartite entry point

For a complete bipartite core with both parts of size at least two, every
core degree is greater than one. Core versus private-pendant labels can
therefore be distinguished by original degree, as in the clique case.
Suppose v belongs to part A.

1. Read the positive seed row and its neighbors' degrees. This identifies
   every core vertex of part B, but does not yet reveal all of A. It also
   identifies t_v, the seed's private-leaf count. No other original row
   has been read.
2. Solve the exact restricted seed star symbolically. If its initial seed
   value (1-lambda*d_v)/d_v gives gamma*u_v<=lambda, the seed leaves stay
   zero. Otherwise all t_v seed leaves are positive, and
   `u_v=(1-lambda*d_v-gamma*lambda*t_v)/(d_v-gamma^2*t_v)`.
   Their original degree-one equations are known from the seed incidences
   and degree queries, so this virtual face requires no separate leaf-row
   scan yet.
3. Check each exposed B vertex j by its true original gate
   `gamma*u_v-lambda*d_j`. If all are nonpositive, the restricted seed star
   is the exact obstacle solution: all other A vertices and their leaves
   see zero B values. Return it with paid final leaf output/scans.
4. If a B gate is positive, j is support-safe. Read its row only after
   this gate is certified. Its degree-greater-than-one neighbors identify
   all of A. The two positive core rows now enumerate the complete core
   and identify its two parts. All core degrees and pendant counts follow
   from degree queries and opposite-part sizes.
5. Apply the supplied scalar part-response sweep, evaluate all core values
   once, and scan only positive core rows and positive pendant rows. Cache
   the two startup rows so they are not scanned again. Their degrees pay
   for all core identifiers, even when many other core vertices stay zero.

This is a concrete locality plan, not a proved implemented theorem yet.
The source-positive startup, seed-star gate, tie cases and complete final
original KKT certificate must be exact-audited. Treat the graph promise as
an assumption; verifying unseen multipartite edges would require additional
access. In the bipartite case, a part of size one leaves vertices in the
opposite part with only one core neighbor; an unadorned such vertex can
then be indistinguishable from a private leaf. The general criterion is
the minimum core degree below, not the presence of a singleton part by
itself (a clique has singleton parts and no classification problem).

For three or more unknown parts, two positive rows reveal the core labels
but do not immediately identify all remaining parts: vertices adjacent to
both startup vertices can belong to several different parts. Supplying
part labels would strengthen the access model. The following possible
continuation instead discovers parts only at positive original gates.

## A paid online part-discovery plan

Assume N-max_g(n_g)>=2, so every core vertex has degree at least two even
without private leaves. The preceding two-row startup identifies all core
labels and the seed's and newly admitted neighbor's parts: each part is
the core labels not adjacent to its representative, including itself.
The startup's two positive degrees pay for this initial O(N) enumeration.

Keep a set R of core vertices in as-yet unidentified parts, and a heap of
their original thresholds lambda*d_i/gamma. Build scalar response curves
only for discovered parts, with every other core coordinate set to zero.
The exact restricted solution then has one aggregate S. Every j in R is
adjacent to every currently positive core vertex, so its original gate is
exactly gamma*S-lambda*d_j. If S is at most the minimum unresolved threshold,
all undiscovered parts are quiet and the restricted solution is the
full obstacle optimum. Otherwise its minimum identifies a support-safe
representative j whose original row may be read.

Use that row's core-neighbor dictionary to classify the current R. The
nonneighbors (including j) are exactly j's entire part; remove them from R.
This scan of R is paid: each scanned outside-part vertex is an original
neighbor of j and is charged to d_j; each scanned inside-part vertex is
removed permanently and charged once to its identifier. Thus all such
part-discovery scans cost at most O(N+sum_representatives d_j), not q*N.
Every representative is positive in the final obstacle support. This is
an amortization argument to implement and test, not a free complement-set
oracle. Stale heap records must be removed or invalidated with paid work.

Once a part is identified, its size and all its original degrees determine
its pendant counts. Build that part's transformed scalar curve in
O(n_g log n_g) work. Insert its future S-breakpoints into the global heap;
initialize its current affine piece at the current exact S, counting every
skipped past event. The new part has a positive coordinate at the old S,
so the aggregate fixed point increases. All earlier part responses also
increase. Process crossed global breakpoints to get the new exact S.
Each discovered coordinate contributes at most two events, and monotone S
means each event is consumed at most once. This suggests O(N log N) total
curve/event work across all discovered parts, rather than solving a fresh
N-coordinate system at every part birth.

The precise implementation must not use a provisional affine root as a
true original boundary gate before all known-part breakpoints below it
have been processed. First solve the current discovered-part fixed point
exactly, then compare it with the unresolved-core heap. At equality the
unknown coordinate stays zero and no row is read.

This plan potentially extends the adjacency-only result beyond two parts.
The promised core classification, cached startup rows, complement-scan
accounting, monotone curve insertion, all pending heap events, and final
positive-only output must be verified together before stating a theorem.
It does not handle an arbitrary core lacking complete multipartite structure.

## Relation to existing notes

**Context/provenance, not a formal proof import:**
`delayed_reflection_ladder/sections/body/12_subsec_equitable_shells.tex`
already gives a scalar shell algorithm for root-distance-equitable graphs,
including pure cliques and complete bipartite graphs. Its
`14_subsec_equitable_tree_quotients.tex` develops exact tree quotients and
hidden-partition refinement with separately charged discovery.

Unequal pendant counts are not automatically covered by those conditions.
For a three-clique with t=(0,1,4) and seed0, the core degrees are 2,3,6.
The distance-one shell is not degree-equitable, and any degree-equitable
partition separates the three cores, leaving a triangle in the quotient.
The completed clique construction uses scalar algebra without equal core
values; it does not import the companion quotient theorem. The proposed
bipartite extension must likewise audit its access promise rather than
borrowing an unverified quotient-discovery assumption.

## Falsifiable next work

- **Completed as a supplied-part reference:** construct each part's complete
  affine curve, including negative input intervals, transform all breakpoints
  into the common S coordinate, and compare against full original obstacle
  solves on unequal complete-bipartite and multi-part examples.
- **Open:** implement the two-positive-row startup and test early exact
  termination before any second core row is read.
- **Open:** replace supplied part labels by paid positive-gate discovery and
  maintain the global breakpoint heap across part insertions without rebuilding.
- **Open:** include huge inactive parts/attachments, core and pendant birth ties,
  very small alpha, and arbitrary core seeds.
- **Open:** charge all transformed-event records, sorting, root candidates, degree
  queries, cached rows and final output. Separate any supplied-label variant
  from the adjacency-only bipartite result.

Only after these checks should this become a new structural theorem. The
general OP3 route still needs a mechanism for arbitrary core topology and
all-original-coordinate publication certificates.

## Completed supplied-part algebra audit

`MULTIPARTITE_SCALAR_AUDIT.json` passes 261 full original obstacle comparisons
on six part-size patterns, unequal pendant counts, every core seed and three
alpha/lambda pairs. It checks 704 supplied scalar fixed points, 3,602
transformed breakpoints (including 878 negative transformed events), 1,298
global event crossings and 182 positive-gate part insertions. The complement
scan counting identity passes at every such insertion.

This reference is given the partition and rebuilds curves during its part
insertion checks. It validates the algebra and monotonicity only. It does
not implement adjacency-only startup, paid online partition discovery or
persistent insertion into the global breakpoint heap. Those remain the
next bounded implementation/proof target. The graph-uniform conjecture is
unchanged.

## Final review: potentially remove two access restrictions

**Open extension, not covered by the completed supplied-part audit.** The
minimum-core-degree assumption and core-seed assumption may be removable
without a generic multidimensional reporter. The following reductions are
algebraic/combinatorial observations; they still need a complete local
algorithm and independent checks before any broader theorem is stated.

First consider canonical core membership. In a complete multipartite core,
an original core vertex can have graph degree one only when its core degree
is one and it has no private leaves. Core degree one forces the other
parts together to have size one, so the core is a star. Such an unadorned
peripheral core vertex can be relabelled as a private leaf of the center.
After all such relabellings, the vertices of original degree greater than
one form another complete multipartite core, possibly a single center or
an edge. The underlying graph has not changed. For a nontrivial star the
center has original degree greater than one; the two-vertex graph is a
separate constant-size case. Thus degree classification may work with this
canonical representation even when the initially supplied representation
has minimum core degree one. This observation alone does not reveal the
canonical core size or its parts locally.

Second, consider a physical seed v of original degree one with neighbor j.
For `lambda<1`, its exact value is always positive and satisfies

`u_v=1-lambda+gamma*u_j`.

The one-coordinate seed face has value `1-lambda`. If
`gamma*(1-lambda)-lambda*d_j<=0`, that face already satisfies the full
original obstacle conditions, so the exact solution is seed-only. Otherwise
j is a certified positive admission and its row may be read. Eliminating
the already positive seed changes only j's core data:

`d_j -> d_j-gamma^2`,
`b_j -> gamma*(1-lambda)-lambda*d_j`.

Original degrees in penalties, residuals and charged work stay unchanged;
the displayed diagonal is only a reduced coefficient. Treat the seed as
one distinguished forced-positive leaf, excluding it from the ordinary
private-leaf count. If that ordinary count is t_j and the canonical core
degree is c_j, the post-pendant positive-piece denominator is

`d_j-gamma^2*(t_j+1)=c_j+(1-gamma^2)*(t_j+1)>=c_j`.

For other core vertices the earlier denominator bound is unchanged. Thus
the part-response slope argument appears to survive, and the effective
positive source remains at the known core neighbor. Recover the physical
seed once at output, charging its row and value. The one-core case can be
solved directly as a star; the two-vertex graph has a constant-size solve.

The next implementation should first establish the narrower promised
core-seed/minimum-degree result already specified. Then test these reductions
on stars, double stars, singleton-part cores, leaf seeds, and exact zero
gates. It must retain the physical seed v in the original certificate;
renaming the effective reduced source to v would obscure the normalization.
No claim above verifies the complete online partition or event work.

## A longer-term algebraic question after the multipartite case

**Open, unaudited direction:** replace the single multipartite layer by a
core built recursively from disjoint unions and complete joins. A module
whose external neighbors connect uniformly to it receives one external
scalar field. Disjoint union adds child aggregate responses. At a complete
join, child g receives the common field plus gamma times the total response
of the other children, suggesting the same part-response inversion as above.
Unequal private leaves can remain in the base response functions.

The missing work argument is substantial: composing these curves through
an unbalanced hierarchy may repeatedly copy every old breakpoint. A useful
target would require a persistent curve representation and paid local
module discovery, not a supplied global decomposition. Establishing only a
small response-curve size would not establish fast maintenance. This is a
question to investigate after the concrete multipartite local mechanism;
neither an algorithm, a new theorem nor a novelty claim is asserted here.
