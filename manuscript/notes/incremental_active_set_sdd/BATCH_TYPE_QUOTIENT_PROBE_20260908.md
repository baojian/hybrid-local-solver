# Batch discovery and exact twin quotients

**Open construction target after block 18.** General OP3 remains Open.
The existing grouped producer gives O(V*k^2*log(2+V)) on an unsupplied
global k-neighborhood-type promise. Try to replace repeated individual
pivots by complete currently eligible batches, without reading inactive rows.

Take every known member satisfying q_group>(lambda+kappa)*original_degree.
Their simultaneous face is strictly positive by the M-matrix inverse, so
lambda*(old_volume+batch_volume)<1 certifies all batch rows before reading.
After those paid rows are exposed, identify exact original twin classes
inside the batch using full open and closed adjacency keys, together with
old response-group identity and degree. Use sorted rows and deterministic
tries/AVL children; do not treat hashing, an ambient partition, or scanning
a giant unadmitted row as free. Equal induced-batch neighborhoods alone are
insufficient: they could merge vertices with different future couplings.

For batch classes a of size n_a, old group g_a, degree d_a and clique bit
c_a, form the quotient of the old Schur block. Its row-constant matrix is

    Hbar_aa = d_a-gamma*c_a*(n_a-1)-n_a*C[g_a,g_a],
    Hbar_ab = -n_b*(gamma*adj(a,b)+C[g_a,g_b]).

K=diag(n)*Hbar is symmetric positive definite. Factor it once, solve for
z=Hbar^-1*h and Y=Hbar^-1*W, where W[a,t] is the common coupling from a
batch member of class a to any future member of refined group t.
Then q_t increases by sum_a n_a*W[a,t]*z_a, and C[t,u] increases by
sum_a n_a*W[a,t]*Y[a,u]. Refine future groups only for original incidences
just read; unchanged heaps must not be traversed or copied.

Save class member lists, z, Y and group split/fresh records. One final
reverse replay uses x_a=z_a+sum_t Y[a,t]*future_group_value_sum[t],
undoes future splits and fresh discoveries, and adds n_a*x_a to the old
batch parent groups. No historical full-membership expansion is allowed.

Under the global promise each nonseed original type is known all at once,
stays unsplit and is admitted in one batch. Separate the physical seed
from its original type for accounting. Thus at most k+1 batches occur,
and the total number of consumed batch classes is at most k+1. If every
completed frontier has at most k groups, the quotient, reconstruction,
rebuild and group-refinement algebra should sum to O(k^3), while original
row lists, tries, heaps and stable label maps cost O(V*log(2+V)).
Target: O((1+V+(1+k)^3)*log(2+V)) total work/allocated words, with exact
obstacle and ACL variants. This is a proposed stronger structural bound,
not an arbitrary-graph improvement or a proved claim until implemented,
independently audited and reconciled with all group-history obligations.

## Completed block 19 result

The construction and reverse replay are now implemented and proved as
`thm:op3-batch-type-quotient`, awaiting independent review. The adaptive
bound on any graph is O((1+V+t*(t+f)^2)*log(2+V)), where t counts consumed
full-row classes and f is the maximum completed frontier-group count;
distinct nonzero columns give f<=2^t-1. Under a global k-type promise,
t<=k+1 and f<=k, proving the proposed O((1+V+(1+k)^3)*log(2+V)) work
and allocation bound. Live words are O(1+V+(1+k)^2).

The full audit checks 7,728 original ACL outputs and 7,298 exact obstacles,
88,759 final original residual rows, 40,641 prefixes, 37,149 reverse
coordinates and 27,098 historical group sums. Original row/degree queries,
merge sorts, trie AVL maps, heap moves, symmetric quotient LDL factors,
all future coupling solves, matrix rebuilds and output are charged.
The earlier default grouped implementation is unchanged.

A path of order five proves why induced-batch twins cannot replace full
original twins. A finite binary tree proves that this dense quotient factor
still has a cubic accuracy obstruction. Six executed binary-tree prefixes
are nonterminal, and are not counted among completed ACL outputs. At R=6
the last quotient has order 64 and uses 41,664 off-diagonal inner products.
This refutes only the representation's general near-linear cost.

A concrete next direction is to retain the quotient's graph structure rather
than eliminate it into a dense matrix: a tree of arbitrary twin classes
could combine local row discovery with the existing weighted tree response
machinery. A physical seed breaks symmetry within its class and needs an
explicit mean/contrast correction. Do not assume that a supplied quotient
or a generic tree callback already pays for that interface.
