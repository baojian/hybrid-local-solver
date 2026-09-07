# Next probe: local unicyclic continuation with two retained cycle ports

Date: 7 September 2026. **Resolved in block 10:** the complete unicyclic
algorithm and charged work are now **Proved here**, as a draft awaiting
independent review, in `thm:op3-local-unicyclic`. The original plan below is
preserved for traceability. The named-coordinate queries and local state
machine are implemented and exactly audited; fast online balancing is still
an explicit published-source import. Arbitrary-graph OP3 remains Open.

## Completed ingredients

`thm:op3-local-top-tree` gives the complete local tree existence theorem,
using the checked height-bounded top-tree source algorithm and implemented
application callbacks. The source balancing algorithm itself has not been
implemented in this project. `TOP_TREE_CALLBACK_AUDIT.json` covers every
legal join shape, source exposure, payload paths and retained versions.

`lem:op3-uniform-negative-shift` sets C=1/bar_alpha and w=u-C. For any
edge-induced cluster B, its load is

`b'_B(i) = 1[i=physical_seed] - lambda*d_i - C*(d_i-gamma*degree_B(i)) < 0`.

Store the fixed base load `beta_i=1[i=physical_seed]-lambda*d_i-C*d_i` and
add gamma*C at both endpoints of each represented edge. Joins subtract one
duplicated beta_i. This works with the physical seed inside the cluster and
does not require updating every edge incident to a growing active vertex.
The geometric anchor can therefore differ from the physical seed.

A local boundary heap key becomes `lambda*d_j/gamma-C`. Arbitrary reporter
intercepts, including positive ones, are valid: the compact chain only
needs W>0 and nonnegative port coefficients. Every normalized point is
vertically translated by +C, so chain membership is unchanged. One-port
thresholds shift by -C. The existing negative-offset pullback contract is
preserved by the negative cluster loads. Final recovery adds C once per
emitted coordinate. This is exact-real algebra, not a numerical-stability
claim.

If the active graph is a spanning tree plus extra edge {c,t}, retain those
two ports and correct its shifted root state by

`[H - gamma*[[0,1],[1,0]]] * w_ports = h' + gamma*C*[1,1]`.

The right-hand correction is essential. Interior response records remain
valid. `SHIFTED_TREE_CLUSTER_AUDIT.json` includes both a triangle and a
triangle-with-source-leaf example, with independent full-matrix solutions.

A crucial source-valid witness: triangle, seed 0, alpha=1/3, lambda=1/20,
eps_appr=1/10. Legal prefix [0,1] has values [7/15,1/15]. Candidate 2's
full two-parent gate is 1/6, but the gate through parent 1 alone is -1/15.
The full triangle solution is [1/2,1/10,1/10]; the spanning path obtained by
removing edge {0,2} has unconstrained solution [13/28,2/35,-1/28]. Thus the
spanning tree is a signed affine response object. Never replace it by its
obstacle solution or assume its uncorrected response is positive. Only the
corrected full active graph must be on a positive face.

## Candidate online algorithm to implement and falsify

Assume the original graph is a tree or unicyclic; do not require its cycle,
cycle length, seed-to-cycle distance, attachment sizes or final support as
input. Start from the physical seed using the tree solver's local discovery.

Before the active graph closes a cycle, U is a connected tree. Every ordinary
inactive boundary candidate has one active parent. At most one candidate
can have two active parents: each such candidate plus the connecting path
inside U would form a distinct cycle. Detect this exceptional candidate
from cached incidence records when a newly admitted row reveals its second
parent; exclude its row from both ordinary local heaps.

The regular root reporter covers all other candidates. Check the exceptional
gate `gamma*(u_p+u_q)-lambda*d_j` separately. Obtain each current active
coordinate by descending the current cluster hierarchy to an incident edge,
using saved affine recovery records, in O(log |U|) word work if the height-
bounded source hierarchy is used. This point-query implementation must be
written and charged; a whole-face recovery per exceptional query is not
acceptable. Charge quiet exceptional checks after every admission too.

If the exceptional gate is positive and j is admitted, the active graph
becomes unicyclic. Take one of its two new edges as the single extra edge
{c,j}, and retain the other in the spanning tree. Rebuild/re-root the current
active spanning tree once, at geometric anchor c, with original degrees,
shifted loads and newly homed boundary minima. This one-time O(V polylog V)
rebuild is paid by final V; arbitrary repeated re-rooting would not be.
Expose c and j as the two external ports and use the corrected two-by-two
root solve. The physical seed may now be interior to a cluster.

Thereafter, a unicyclic original graph cannot have another inactive candidate
with two active parents, since that would create a second cycle. New
admissions are leaf insertions into the stored spanning tree. Maintain two
fixed external cycle ports after every link, refresh the one old parent
payload and the new vertex payload, query the complete two-port root hull,
and stop only after an exact all-quiet certificate. Final recovery uses the
corrected two-port values and adds C before outputting bar_alpha*D*u.

A stop before active cycle closure is also valid if both the ordinary
reporter and the exceptional candidate are quiet. This should allow a huge
unseen cycle or attachment to remain unscanned. All original degree replies,
cache reads/writes, heap work, exceptional checks, failed queries, callbacks,
re-rooting, historical copies and final output must enter the ledger.

## Required next audits

1. Implement a charged original-coordinate point query on existing cluster
   records. Compare it against full recovery, including helper forget nodes,
   repeated shared ports, old versions, and two-port roots.
2. Implement a locally discovering state machine with zero or one exceptional
   candidate. If using a supplied or rebuilt hierarchy as a correctness
   oracle, count and label that construction separately; the asymptotic
   theorem must explicitly import the source's online hierarchy algorithm.
3. Test all small connected unicyclic graphs, every seed, multiple alpha and
   lambda values, and actual strict source-driven admissions. Compare every
   original gate, every full face solve, both sides of cycle closure and
   final obstacle/ACL output with independent exact references.
4. Include the negative-spanning-tree triangle witness, off-cycle seeds,
   multiple attachment branches, long attachments that keep changing after
   cycle closure, large quiet inactive stars, and stops before seeing a cycle.
5. Prove the at-most-one exceptional candidate invariant, single re-rooting
   charge, active-only initialization and all source callback assumptions
   for two exposed cycle ports. Only then state a unicyclic local theorem.

If this succeeds, it would remove both the cycle-seed restriction and the
polynomial attachment-size factor from the earlier bounded-attachment result.
It would still be a structural result and would not resolve OP3 on arbitrary
nonequitable cyclic graphs.

## Point-query implementation refinement

The published source's Section 2.4 already stores C(i), the lowest cluster
where active vertex i is interior (or the root if i is external). Prefer
this locator, or an incident-edge leaf locator, to any fresh subtree search.
A query can maintain an affine row for w_i in the current cluster's at-most-
two ports and pull it upward through O(log |U|) parent callbacks, then
evaluate it at the solved root ports. Each callback introduces at most two
helper records, so its child-to-parent affine map is computed in O(1)
word work. This formulation uses constant-size affine state plus the source
parent pointers and avoids a full recovery vector. Verify the helper maps
for compress, rake, rake-then-forget and one-port base edges, including the
physical seed inside a shifted cluster. Named-coordinate queries alone are
not a general event locator; they suffice here only for the one exceptional
candidate, whose every failed check is charged.

## Resolution and next probe

All five original acceptance obligations have a proof draft and exact audit
in `sections/op3_local_unicyclic.tex`, `CLUSTER_POINT_QUERY_AUDIT.json` and
`LOCAL_UNICYCLIC_CLUSTER_AUDIT.json`. The query pulls a constant-size affine
row upward from a stored incident edge, with O(log n) work on the imported
height-bounded hierarchy. The reference driver reconstructs parent indices
and hierarchies; those full traversals are separately charged audit work.

The atlas sweep has 3,888 executions on all 78 eligible graphs through seven
vertices, every seed, four parameter pairs and two policies, plus sixteen
larger explicit attachment cases. It checks 16,371 exact positive faces and
26,043 original gates, including 319 negative uncorrected spanning-tree
faces. Four enormous finite private-star constructions scan no inactive hub
rows. Their core sizes 9/17/15/16 need only 27/51/45/48 original entries.

The next Open question is `BOUNDED_CYCLE_RANK_PROBE.md`. Do not reuse the
one-exception or two-fixed-port claims on graphs with multiple exposed
cycles without the new coarse-system and repartitioning argument.
