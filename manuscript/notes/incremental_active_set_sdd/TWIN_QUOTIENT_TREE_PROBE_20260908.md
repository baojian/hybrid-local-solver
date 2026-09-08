# Preserving a locally discovered tree of original twin classes

**Next bounded target after block 19; Open construction.** General OP3
remains Open. The exact batch quotient is proved and audited, but its dense
factor has a cubic binary-tree obstruction. Explore a graph whose canonical
original true/false-twin quotient is a tree (including one quotient vertex).
The type count is unbounded and no partition or quotient is supplied.
Do not import the unweighted tree theorem as a ready-made weighted updater.

## Exact mean and source contrast

For an active original type C, let n_C be its admitted multiplicity, D_C
its original degree, and c_C its internal clique bit. Every nonseed type
is admitted completely in a whole eligible-type batch; only the physical
seed's type R can have a first singleton and a later remainder. Let y_C
be the mean physical potential. The symmetric mean system is

    K_CC = n_C*(D_C-gamma*c_C*(n_C-1)),
    K_CH = -gamma*n_C*n_H for adjacent quotient classes,
    b_C  = 1_{C=R}-lambda*n_C*D_C.

It is SDD with nonnegative grounding because D_C retains all inactive
original neighbors, not just admitted quotient edges. Every nonseed
individual has u_i=y_C. Within the seed class,

    u_i = y_R + (1_{i=v}-1/n_R)/(D_R+gamma*c_R).

This follows from subtracting two original within-class equations.
The scalar source contrast must not be discarded. When n_R=1 its lift
is zero irrespective of the temporarily unknown clique bit. After the
remainder is admitted, its clique bit is visible in the paid rows.

## Local type discovery and sparse descriptor changes

The block-19 producer exposes complete positive batches. Reuse its full
sorted original rows, but maintain additional global open/closed-row tries
without its old-group prefix. A new batch class can match a previously
admitted global type only in the seed's type, since every other type was
consumed as a whole. A representative's full open and closed keys suffice;
all such key lengths sum to O(V). Stable physical-to-class labels and a
paid quotient pair map construct only edges exposed by those positive rows.
A new ordinary type is a leaf of the active quotient tree. The seed type
can grow once, without introducing a new quotient vertex.

When the seed multiplicity grows, refresh its diagonal/load and every
incident quotient weight. Its old quotient degree is at most the physical
seed degree D_R, and the newly read seed-class members pay at least D_R
in original volume. All other class diagonals stay fixed. Distinct new
quotient edges are paid by original row incidences. This suggests a total
O(V log(2+V)) bound for type maps and sparse descriptors, not yet the
numerical solver or global threshold reporter.

A single-parent choice is useful for the prospective fast implementation:
ask a tree reporter for one eligible parent heap, recover that parent's
value, and remove every currently eligible member of that heap at the fixed
old face. This still consumes whole nonseed original types. Then identify
full original twins from the paid batch rows and add the new quotient
leaves, possibly together with the one seed-class enlargement. Merely
scanning every frontier heap in every round is not a fast general tree
reporter; the dense BatchFrontier remains a reference producer for this test.

## One-parent gates and the special seed-type gate

In a connected active quotient subtree, an unadmitted vertex from a new
global type has exactly one active quotient parent P. Its original residual
is gamma*n_P*y_P, so a degree heap uses threshold
(lambda+kappa)*D_i/(gamma*n_P). Heap order remains original-degree order
when n_P changes, allowing one scalar minimum refresh instead of moving
all keys. Handle gamma=0 directly.

The only possible unadmitted vertices with two or more distinct active
quotient parents are the missing members of the seed type. Otherwise their
new quotient vertex and the connected active subtree would form a cycle.
Before they are admitted n_R=1, and for such a member j,

    r_j = (D_R+gamma*c_R)*u_v - 1 + lambda*D_R.

Its strict gate is equivalent to

    u_v > (1+kappa*D_R)/(D_R+gamma*c_R).

The bit c_R is already known from whether j is adjacent to the original
seed. Classify such candidates from a second distinct active-class row,
and move them from their old heap to a special seed heap; every move has
a paid original incidence. Candidates with only one active parent can
stay in the ordinary heap even if they will later prove to be seed twins.
Their complete original rows identify the root merge when they are admitted.

## Weighted callbacks and the multiple-payload obligation

The existing Backend in path_cluster_reporter.py uses the common gamma
only in its base-edge matrix. Its compress/rake/forget operations read
positive coupling weights from matrix entries. A separate WeightedBackend
can supply per-edge weights gamma*n_C*n_H while retaining the fixed
current node diagonal/load. Nonseed loads remain negative; keep the seed
class as the geometric root so its load is never eliminated in a valid
summary. Audit all weighted Schur, reporter and recovery identities against
independent original physical systems, not just the compressed matrix.

Existing Lemma op3-top-tree-payload updates one home payload. Changing
n_R changes the numerical data on every incident base edge, because base
summaries duplicate endpoint diagonals and loads. Refreshing them one at
a time against mixed old/new shared-node data is unsafe. A proposed paid
transaction marks the union of their current hierarchy ancestor paths,
changes the sparse descriptors, and rebuilds all marked summaries once in
postorder. Each old summary containing that root owns an incident root edge,
so it must be marked; an unmarked child cannot contain stale root data.
There are O(deg_Q(R)*log V) marked records, with no graph-wide membership
scan. Retain immutable old versions but never reactivate them as current.
This needs its own proof and exact callback audit before source composition.

At the matrix level, set the final root diagonal/load before increasing
its incident weights: the final root diagonal dominates the final incident
sum, and all other original diagonals do too. Intermediate matrices remain
SDD. No gate query is issued during the transaction. Structural leaf links
and reporter refreshes must also be completed before the next original gate.

## Completion discipline

First implement and audit the paid full-row class map, exact mean/contrast
identity and frontier gate classification on actual positive prefixes of
mixed clique/independent tree blow-ups, all seeds, both exact and ACL gates,
small/tiny alpha and source-type merger regimes. The block-19 dense producer
and supplied graph partitions may be validators, not hidden fast operations.
Then audit weighted callback closure and the simultaneous payload refresh.
Only claim an end-to-end source-backed fast local solver once graph discovery,
all degree heaps, special-root gates, online balancing, callback updates and
final physical/canonical output have complete charged contracts. Otherwise
record the proved reduction and the precise remaining interface as Conditional.


## Completion after blocks 20–21

The paid descriptor and weighted/bulk update obligations are now proved
in `sec:op3-twin-quotient-tree`. The full single-parent-heap state machine
and source-backed numerical composition are proved, as drafts awaiting
independent review, in `thm:op3-local-twin-quotient-tree`. The three scripts
`twin_quotient_tree.py`, `weighted_tree_payloads.py` and
`local_twin_tree_stream.py` have separate full exact audits. In particular,
the final audit covers 1,298 transactions that grow the source class and
add new ordinary leaves; source refresh precedes links, and every
intermediate weighted matrix is positive and SDD in the audit.

This closes the restricted quotient-tree construction at the proof level.
The published online balancing algorithm is still imported, and the
stream audit's dense numeric reporter remains a deliberately slow
reference. A bounded-cycle quotient extension is a new target; do not
silently apply the original unweighted cycle-rank theorem to weighted
quotient loads, changing source multiplicity or source-class contrast.
General OP3 remains Open.

## Bounded-cycle continuation sharpened at the final checkpoint

`lem:op3-quotient-cycle-frontier-budget` now proves that, with quotient
rank r and active rank r_S, new types spend at most r-r_S excess parents.
At most r-r_S+1 multi-parent response groups remain, including possible
missing source twins. The five-cycle witness in
`prop:op3-five-cycle-source-type-ambiguity` rules out using the tree's
two-parent source classification on a one-cycle quotient.

For a one-cycle promise, first implement paid parent-set refinement with
at most two small exceptional groups, and classify large-parent candidates
as source twins only after the rank quota proves it. Every candidate's
original degree stays in a heap; group keys are current active type parents,
not a supplied global type partition. Avoid copying a long source parent
set once per new incidence. Use its certified source formula when the
parent quota applies. The finite quota audit is global reference work,
not this missing local maintenance code.

The numerical prototype can allow one rebuild at quotient-cycle closure
and one at source-class enlargement, using only cached positive rows and
current heap minima. Each event happens at most once; two rebuilds costing
O((1+V)*log^4(2+V)) fit the desired total scale. This is a budget observation,
not a completed cyclic algorithm. It avoids requiring an unproved fully
dynamic weighted correction interface at the first prototype stage.
The remaining proof must still supply the weighted cycle solve, shifted
reporters if the geometric root moves, original seed contrast, exact gate
recovery, and all local group updates before any stopping query.
