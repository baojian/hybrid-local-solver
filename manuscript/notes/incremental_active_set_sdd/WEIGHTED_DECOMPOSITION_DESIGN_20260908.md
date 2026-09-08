# Weighted ownership and two-boundary refinement: implementation design

**Proved here and exactly audited; routed-load composition still open.**
`weighted_tree_ownership.py --full` passes 9,042 supplied-tree cases,
127,547 piece checks and 1,483,000 pairwise intersection checks. It records
10,486,152 charged construction units, including 6,562 actual Steiner
refinements. The saved audit matches source SHA-256
`e6c05c82ae246d09791311dc0f2833b491d43284fd03f2bf9a2b30f48028b4a9`.
No subsequent edits to that script have been made at this checkpoint.

This expands the next task in
`WEIGHTED_PIECE_CONSTRUCTOR_PROBE_20260908.md`. The rooted-piece spectral
comparison and literal component-stretch obstruction now have proofs in
`sec:op3-rooted-piece-comparison` and 19,854 exact weighted comparisons.
The decomposition proof is now in `sec:op3-weighted-tree-ownership`.
It still needs composition with the weighted path/corridor routing.
The full supplied constructor stays Conditional.

## Input and ownership

Input is a supplied positive-weight connected graph and a spanning tree T,
with vertices indexed once. Parallel original edges may first be aggregated
by a charged sort. Let `w_e=c_e*resistance(T[e])`, `W=sum_e w_e>0`, and
`a_v=sum_{e incident v} w_e`. Thus `sum_v a_v=2W`. The source low-stretch
tree import eventually gives W=O(m log n loglog n); the decomposition
should work for any positive weights without a ratio assumption.

Each vertex owns its load in exactly one piece containing it. Every
original edge is assigned to the one or two owner pieces of its endpoints.
The assigned edge load of a piece is at most its owned vertex load.
Shared boundary vertices may occur in many pieces but their load is paid
only by their owner, possibly a singleton heavy-vertex piece.

For j<64 use one tree piece and an arbitrary root. Its load is at most
2W and its actual local stretch at most W, so a sufficiently large
constant times W/j covers this branch. Handle n=1 separately. For j>=64
and j<=n, try `theta=64W/j`.

## DFS construction before refinement

Process T bottom-up. Each unfinished child bag is a connected subtree
containing the child, represented by an edge-list head/tail, an owner-list
head/tail, and owned mass strictly below theta.

At a light vertex (`a_v<theta`), start the pending bag with the single
owner record v. At a heavy vertex, immediately emit the singleton owner
piece `{v}` and start a zero-mass pending bag with connector v only.
For each child, attach the edge from v to that child's bag and splice
its edge and owner lists into the pending bag. If the mass reaches
theta, emit the pending connected piece and reset to connector v,
with empty edge/owner lists and zero mass. Vertex v is never owned twice.
Return the remaining bag to the parent. At the root, emit its final
remainder if it has an edge or an owner; omit an empty connector already
covered elsewhere.

Every emitted nontrivial flushed piece has owned mass in [theta,2theta),
since the previous pending and incoming child masses were both below
theta. The final piece has mass below theta. Heavy singleton pieces can
have arbitrarily large mass, but each has at least theta. Consequently
the initial piece count h0 is at most `2W/theta+1`.

Lists must be spliced in constant work rather than copied up the tree.
Each original tree edge has one list node, and each owned vertex has one.
Flushed piece headers and connector occurrences are charged. Materialize
memberships once from each piece's edge endpoints plus its connector,
using a reusable n-entry stamp array. Connected edge-disjoint subtrees
intersect in at most one vertex. Their piece/shared-vertex incidence
graph is a tree; total boundary incidences is at most `2(h0-1)`.

## Refining a piece with more than two boundaries

Build its local adjacency from its own edge list, never by repeatedly
scanning a high-degree boundary's complete original adjacency. A reusable
global-to-local index array is written only at this piece's vertices.
Total old memberships is O(n+h0), so these local arrays cost O(n+h0)
over the decomposition, not n times the piece count.

For a piece with b>2 old boundary vertices:

1. Peel nonboundary leaves to obtain the minimal Steiner tree spanning
   those b boundaries. Record each peeled vertex's parent. Its attachment
   to the remaining Steiner tree is recovered in reverse peel order.
2. Mark every old boundary and every Steiner branching vertex. There are
   at most `2b-2` marked vertices. Make one new piece for each maximal
   Steiner corridor between marked vertices; put hanging trees attached
   to an interior corridor vertex into that corridor piece.
3. For every marked vertex that has hanging edges, make one additional
   piece containing all of its hanging branches and that marked vertex.
   It has one boundary. No additional piece is made for an empty bundle.
4. Reassign each old owned vertex to one new piece containing it. An
   unmarked Steiner vertex has a unique corridor; a peeled vertex uses
   its attachment's corridor or hanging bundle. A marked vertex may
   choose a deterministic incident piece. No mass comes from another old
   piece, so each new nontrivial piece still has owned load below 2theta.

There are at most `(t-1)+t <= 4b-5` new pieces when b>2, where t is
the number of marked vertices. Pieces with b<=2 remain intact. A safe
global bound for h0>1 is `h1 <= 4*sum_i b_i <= 8(h0-1) <= j/4`.
All pieces are connected and edge-disjoint; intersections are only at
their marked boundaries, with at most two in each nontrivial piece.
Check the counting constants against the actual implementation before use.

## Roots, cuts and the common congestion offset

Let C be all shared vertices of the refined decomposition. If there is
only one piece and no shared vertex, choose one arbitrary root. In a
two-boundary piece, delete a corridor edge minimizing global tree-path
congestion `sum_{original e: f in T[e]} c_e`. Keep the one-boundary pieces.
The resulting rooted parts each have one root. Parts sharing that root
may join into a larger forest component, which is harmless for the new
rooted-piece theorem. Components with distinct roots cannot merge.

For a refined piece Wi with boundaries s,t, let D be its assigned original
edges whose tree path meets Wi. Any edge outside D that crosses an edge
of the s–t corridor traverses the entire corridor: its endpoints cannot
be interior to Wi, since those vertices are uniquely owned there.
Thus global corridor congestion equals D-congestion plus a common
nonnegative offset. A global minimizer is also a D-minimizer.

The corrected rerouting argument then bounds each rooted part's total
local stretch by at most twice the assigned original stretch load of Wi.
The minimum-congestion contribution obeys
`resistance(T[s,t])*conductance(D_cut) <= sum_{e in D} w_e`.
Ignoring the nonpositive subtraction in the source formula suffices for
the factor two. With assigned load below 2theta, kappa may be chosen
as `max(1,4theta)`, subject to full verification of all path cases.

Distances and global congestion use LCA path additions and a postorder
sum in O(m log n) work. Minimum corridor scans over the edge-disjoint
pieces cost O(n). Root labeling and core aggregation are already covered
by the new spectral comparison. None of these steps gives local graph
discovery; the whole graph here is supplied and its reads are charged.

## Audits required

- Exact owner coverage, edge partition, induced connectivity, pairwise
  intersections, global boundary counts and at-most-two-boundary property.
- Arbitrary positive loads, threshold ties, heavy singleton owners,
  high-degree stars, long paths, root-only remainders and empty bundles.
- Count all splices, list nodes, membership words, local adjacency records,
  queue operations, maps, copies, old temporary releases and output.
- Verify common corridor offsets, the corrected affected/unaffected route
  cases and local stretch bounds against independently enumerated paths.
- Compose the produced rooted pieces with the exact spectral validator.
- Keep the full supplied constructor Conditional until low-stretch source,
  sparsifier confidence and weighted numerical assumptions are reconciled.

## Next implementation: charged tree paths and forest assembly

Implement a supplied weighted-tree index with parent/depth/resistance
prefix sums and binary ancestors. Each original graph edge uses one LCA
query for its tree stretch and endpoint/LCA conductance differences.
A single reverse traversal computes every original tree-edge congestion.
Charge O((n+m) log n) words/work, including all ancestor tables; no path
table is supplied to the production constructor.

Run the audited ownership/refinement at `theta=64W/j` when j>=64.
For j<64, one whole-tree piece and an arbitrary root suffice. For every
two-boundary refined piece, enumerate its root-to-root tree corridor
using parent pointers and choose a minimum-congestion edge, with a fixed
edge-id tie rule. Corridors have disjoint tree edges, so their total
enumerated length is O(n); LCA overhead is O(number_of_pieces log n).

Build rooted parts within each individual refined piece after its cut,
using adjacency assembled from that piece's own edges. Do not identify
these parts with entire forest components. Label the resulting forest
from its roots; verify exactly one root per component and
`number_of_cuts+1=number_of_roots`. Original singleton owner pieces
contribute roots but no forest edges. A single-piece/rootless input
receives an explicit arbitrary root; a one-vertex input is a separate base.

Use original edge ownership to validate the common corridor-congestion
offset and the bound `local_stretch(part)<=2*assigned_stretch(piece)`.
No independent numerical path validator is part of the construction's
runtime. For n>=2, any spanning tree has W>=n-1. Therefore a uniform
safe choice is `kappa=256W/j>=1` for all 1<=j<=n: the small-j branch
has local stretch W, and the large-j branch has local stretch below
4theta. The proved rooted-piece comparison would then give quality
`5376W/j` before core sparsification, at most twice that after an
upward 2-sparsifier. These constants are proposed until the routing
composition has passed its own proof and audit.

The low-stretch-tree primary source's Theorem 1 is stated without an
expectation or failure qualifier, and its construction is deterministic
apart from an optional tie-breaking interpretation. Its use of
shortest-path distance in the denominator only strengthens the bound
on our resistance-edge denominator. Confirm this source contract and
the weighted fixed-accuracy core sparsifier's probability/work model
before declaring the supplied recurrence unconditional.
