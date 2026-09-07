# Completed supplied-module probe and remaining local question

Second-night block 2 update, 8 September 2026: the candidate algebra and
edge accounting below are implemented and **Proved here** as drafts
awaiting independent review. `thm:op3-supplied-modules` gives the explicit
O((N+m_core)*log(2+N)) construction. The stronger implemented
`thm:op3-persistent-modules` uses immutable affine curves and non-largest
physical child merging for O(N*log^2(2+N)) work and allocated words, with
all recovery versions retained. Neither supplies local module discovery.

Proof authority: `sections/op3_recursive_modules.tex`. Exact audits:
`RECURSIVE_MODULE_RESPONSE_AUDIT.json` and
`PERSISTENT_MODULE_RESPONSE_AUDIT.json`. The former verifies 50,250 full
original affine intervals on 1,716 cases/53 cores; the latter checks the
same original problems, 22,530 retained curve versions and 100,500
coordinate recoveries, plus 18 larger supplied cores through 512 vertices.
The persistent 512-core comb has 65,536 edges and 38,598 immutable node
allocations. Explicit matrices and the full-graph decomposition recognizer
are validation only. Its recursive recognizer was replaced by an explicit
stack after the first 512-core validation reached Python's depth limit;
all final audits passed on the corrected source. Solver traversals already
use postorder/stack processing and bounded-height AVL paths.

The relevant mathematical correction is stronger than the initial edge
charge: whole join transforms are affine shears of curve points, so they
need only a persistent root copy. Stream the knots of non-largest physical
child modules, adding their nonnegative hinges through suffix updates.
Each vertex incurs such a merge only logarithmically many times. A zero
left ray is permitted because this algorithm makes only horizontal queries;
no inverse query requiring a positive left slope is imported.

**Next:** `MODULE_REPORTER_AND_UPDATE_PROBE.md` isolates fixed-module
reporting from changing-graph recognition and response replacement. The
source screen in `docs/literature/lcp-solvers.md` is scoped, not a claim of
an exhaustive literature review. General OP3 remains **Open**.

The original block-1 proposal follows as development history.

# Recursive union/join response: next bounded algebraic probe

Date: 7 September 2026, second night, block 1.
Status: **Conditional / Open implementation and local work**. The algebra
below is a derived proof candidate to audit independently before promotion.
General OP3 remains **Open**. No novelty claim or external algorithm import
is attached to these elementary response identities.

## Exact target and assumptions

Start with a supplied decomposition of a core into singleton leaves and
recursive disjoint-union or complete-join nodes. At a union there are no
cross-child core edges; at a join all cross-child pairs are edges. Each core
vertex has arbitrary private degree-one leaves. Use original full degrees,
physical point seed, M=D-gamma*A and b=e_v-lambda*d. Initially keep the seed
in the core; the proved forced-positive leaf elimination may be imported
only with its original-degree and distinguished-seed recovery conditions.

For a module H, keep every exterior coordinate zero and add a common
physical field h to each of its core equations. Let F_H(h) be the sum of
its core obstacle values, including the exact effect of its private leaves.
The supplied decomposition, all original degrees and all leaf counts are
reference inputs here. They are **not** free local oracles.

## Candidate exact composition

A singleton has the same three-piece kernel as the multipartite solver.
Every coordinate has one zero-to-positive birth and at most one ordinary
private-leaf birth. Retain negative input intervals as well as positive ones.
All responses start at zero as h tends to minus infinity.

At a union node, F_H(h)=sum_j F_j(h). Merge sorted child breakpoints and
sum the current affine coefficients; tied events must be applied together
or treated through continuity.

At a join node put S=F_H(h), z=h+gamma*S and S_j=F_j(z-gamma*S_j).
Define the increasing inverse transform

    z=t+gamma*F_j(t),  G_j(z)=F_j(t).

If F_j(t)=a*t+b on a piece, then

    G_j(z)=(a*z+b)/(1+gamma*a),
    z_* = t_*+gamma*F_j(t_*).

Merge these transformed child event streams to obtain G(z)=sum_j G_j(z).
The parent is obtained through h=z-gamma*G(z), F_H(h)=G(z). On a combined
piece G(z)=A*z+B, the candidate formulas are

    F_H(h)=(A*h+B)/(1-gamma*A),
    h_* = z_*-gamma*G(z_*).

The denominator must be proved positive on **every** interval, including
negative trial fields, before using this as an exact curve construction.
For a child of size n_j inside a join of size n, its active Jacobian has
row sums at least n-n_j: these are original cross-child degrees, retained
in its diagonal while its siblings are fixed to zero. Its inactive core
neighbors only increase that margin; eliminating active private leaves
leaves the nonnegative contribution (1-gamma^2)*t_i. Inverse positivity
therefore suggests F'_j <= n_j/(n-n_j). Hence

    gamma*G'_j <= gamma*n_j/(n-n_j+gamma*n_j) < n_j/n,

so gamma*A<1 after summing children. This is the same strict contraction
used by the completed multipartite part transform. Any original neighbors
outside the parent module improve the bound. The final parent transform
then preserves event order and is onto the real line.

## What the algebra would and would not pay for

If the transformations are correct, each parent has no more breakpoints
than its children together, hence at most twice its number of core vertices.
An independent route to the same count is monotonicity of the original
obstacle response under increasing uniform h: each core and each private
leaf group becomes positive at most once. The sum response is continuous
and piecewise affine between these events. Verify the count by exact
original-matrix comparisons, not by counting only emitted heap entries.

A naive supplied-tree construction has work proportional to the sum of
all module sizes (plus merge/search costs). Its record count can be
quadratic in the number of core vertices on an unbalanced tree, but this
is **not yet an excessive-work witness**: the core may already have
quadratically many edges. The following edge charge is a more useful
candidate than treating depth alone as the blocker.

First flatten adjacent nodes of the same operation and contract unary
nodes, yielding a reduced alternating decomposition. At a join node of
size n with child sizes n_j, its cross-child edge set has size
C=sum_{j<k}n_j*n_k >= n-1 >= n/2. Every core edge belongs to exactly one
such set, its endpoints' lowest common join ancestor. Thus

    sum_{join nodes H} |H| <= 2*m_core.

Every non-root union node has a join parent; the total sizes of those union
children are at most the parent's size. A union root costs at most n.
Consequently

    sum_{all internal nodes H} |H| <= n+4*m_core.

This would pay for all retained child curves and their copying in a
supplied reduced decomposition, with O((n+m_core)*log(2+n)) word work and
O(n+m_core) words even on an alternating comb. Check flattening,
construction, sorting and reconstruction costs explicitly. The charge
uses **all core edges**, so it does not establish a support-volume local
bound when many core vertices remain inactive and their rows are unread.

Even a fast supplied-tree construction would leave local discovery open.
The multipartite proof can enumerate all core identifiers with two positive
rows because every core vertex sees one of two adjacent representatives.
A general recursive core has no such two-row cover. One must not read an
entire supplied module or a zero vertex row to recognize its decomposition.
Any local theorem must pay for module membership, adjacency classifications,
original degree queries, negative certificates, event transformations,
history/copies, updates and final coordinate recovery.

## Falsifiable next steps

1. Implement the supplied recursive response algebra with exact fractions.
   Test union/join trees, mixed depths, negative fields, all event ties and
   original core/private-leaf equations; compare entire affine intervals
   against independently solved original obstacle instances.
2. Count final and intermediate records on alternating combs and balanced
   trees, and audit the distinct-edge charge above. A quadratic count in
   core vertices can be linear in input edges; do not call it a lower-bound
   obstruction without comparing the right charged quantity.
3. Separate a supplied-decomposition O(m_core log n) theorem from a local
   O(cvol(U) log cvol(U)) theorem. Seek paid incremental module recognition
   and skip response construction for provably inactive regions. Arbitrary
   tree balancing can change graph semantics; exact same-operation
   flattening is available, arbitrary rotations are not assumed.
4. Reassess the arbitrary-graph bottleneck after this audit. Generic sparse
   coarse SDD solves still write all port coordinates at each call; the
   known expected O_tilde((1+E[r])/eps_appr) theorem does not amortize that
   aggregate away. Uniform module fields address a structured rank-one
   coupling, not generic coarse residual updates. Check recent primary
   sources on monotone SDD obstacle/min-cost convex-flow methods before
   investing the whole night in increasingly narrow graph families.

Formal imports within this direction: coordinate kernels and original
obstacle comparison from the local multipartite proof. Context/provenance:
MULTIPARTITE_CORE_PROBE.md and the earlier clique response. No new formal
cross-note registry edge is introduced by this unpromoted probe.
