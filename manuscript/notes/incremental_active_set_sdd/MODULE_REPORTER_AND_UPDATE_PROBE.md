# Next local-module probe: weighted-depth reporting and changing curves

## Block 3 update

The fixed-response reporter and known convex summand removal are now
**Proved here**, drafts awaiting independent review, and implemented.
Authoritative proofs: `sections/op3_module_reporter.tex` and
`sections/op3_module_curve_removal.tex`. Their exact records are
`MODULE_VALUE_REPORTER_AUDIT.json` and `MODULE_CURVE_REMOVAL_AUDIT.json`.
The reporter supports arbitrary fields and positive target increases or
decreases; it uses dense indexed heaps and preserves all curve versions.
Removal deletes zero slope jumps and uses the common transformed field.

Resume `MODULE_ADMISSION_COST_PROBE.md` for the remaining changed-curve
work and a possible original-residual charge. The original proposal and
reachable module-split witness below are preserved as historical context.

## Historical proposal

Date: 8 September 2026, second night, block 2. **Conditional / Open** until
independent proof and exact audit. Do not confuse a supplied decomposition
with a locally constructed one. General OP3 remains **Open**.

The supplied recursive response theorem and persistent version now identify
a useful algebraic primitive. Before attempting a full local graph solver,
separate reporting on a fixed module, module recognition under admissions,
and replacement of old response curves. These are three different costs.

## Degree pays for depth in a reduced decomposition

For any core vertex i in a reduced alternating union/join tree, each join
ancestor has a sibling containing at least one neighbor of i. Those sibling
sets are disjoint along the ancestor path. Therefore the number of join
ancestors is at most the core degree of i, and the number of union ancestors
is at most one more. Thus

    depth(i) <= 2*deg_core(i)+1 <= 2*d_i+1.

This can pay for a root-to-leaf traversal whenever it is charged to an
actual original row publication at i. Height alone is not the right
obstruction: a deep leaf in such a core already has many incident edges.
Verify the precise constant with singleton/root-union cases and retain
original degrees throughout. The claim does not pay for arbitrary walks
made without a charged coordinate event.

## Exact next-event threshold on fixed supplied module responses

Fix the original matrix and all module curves, allow the root's common
external physical field h to increase, and assign each tracked core
coordinate a target T_i>0. Let tau_H be the first field of module H at
which any tracked descendant reaches its target. At a singleton,

    tau_i = d_i*T_i - gamma*t_i*(gamma*T_i-lambda)_+ - b_i.

At a union, tau_H=min_j tau_j. At a join, for each child define

    z_j = tau_j + gamma*F_j(tau_j),  z_min=min_j z_j,
    tau_H = z_min - gamma*G_H(z_min),

where G_H is the sum of the transformed child responses. It can be obtained
from the retained parent response by the positive shear (x,y)->(x+gamma*y,y),
so evaluating it does not require summing every child at query time.

Store each child's key in an indexed comparison heap and keep the winning
original descendant label. Updating a single target changes only its
ancestor path. Each step costs O(log N) for response evaluation and the
heap update, hence O((1+d_i)*log N) by the depth bound. At the root,
h>tau_root is the strict due test; equality is not a strict violation.
The returned winning leaf should be checked against an independently
recovered original coordinate. Its value can be obtained by a top-down
path query using stored module responses, with the same weighted-depth
charge. Keep negative tau values; they can be needed even with T_i>0.

Private-leaf events can be represented by a parent target
(T_leaf+lambda)/gamma, with a heap for multiple distinct leaf targets, but
this extension should be separately charged and tested. Start with core
coordinates only. No source or terminal ACL claim follows from an unchecked
threshold reporter.

Falsification suite: every core seed, unequal pendants, target ties,
negative module thresholds, exact root equality, monotone root-field
changes, repeated target increases and mixed union/join trees. Compare
all reported and quiet states to independent original matrix solutions.
Count initial construction separately, all heap/index updates, old-version
queries, path visits, final coordinate recovery and copied state. A saved
curve version must remain unchanged after any target update.

## What changes at an actual graph admission

A newly admitted positive core vertex may cease to be uniformly adjacent
to an old module. For example, a triangle on {a,b,c} extended by a vertex
j adjacent only to a is still a union/join core, but the old triangle is
not a module of the larger graph. Its new decomposition joins a with the
union of edge {b,c} and singleton j. Adding a private leaf to j can make
its original degree greater than one without changing this core example.
This is a reachable original-gate trace. Take labels a=0, b=1, c=2,
j=3 and private leaf 4, edges {01,02,12,03,34}, physical seed 2,
alpha=1/3 (gamma=1/2), lambda=1/100 and original degrees (3,2,2,2,1).
The original restricted responses and next positive gates are:

| Current face | Its positive values in the listed order | Next vertex | Original excess |
| --- | --- | --- | --- |
| {2} | 49/100 | 0 | 43/200 |
| {0,2} | 43/575, 117/230 | 1 | 25/92 |
| {0,1,2} | 87/800, 5/32, 89/160 | 3 | 11/320 |

The full original obstacle response is
(171/1525, 48/305, 34/61, 11/610, 0). These fractions were checked by
the independent exact original-matrix obstacle routine; direct substitution
also verifies all equalities and inactive inequalities. The old triangle
is a module of the **induced active core**, not of the full ambient graph.
Admission of 3 changes the induced active decomposition while all scanned
core vertices remain positive. This refutes only an interface that keeps
every old active module intact under arbitrary legal admissions.

A graph-recognition update alone does not update an obstacle response.
Even if recognition changes O(d_j) tree records, replacing a large child
response by another can cost its full curve size under the present
small-child merge routine. Subtracting an old known child from a sum may
be possible through signed hinge removal, but this requires exact knot
multiplicity/deletion and convexity invariants. It must also be done in the
correct transformed coordinate. Independently transforming summands by an
inverse map does not transform their sum.

A fixed module's external field is scalar only while its entire boundary
has the required uniform adjacency. Do not carry that hypothesis across
a split without proof. The candidate route is to audit paid incremental
module recognition, exact curve split/merge operations and sparse change
propagation together. A repeated complete root-curve reconstruction or an
unpaid ancestor walk is a stop criterion for that particular mechanism,
not a universal OP3 lower bound.

## Recommended order

1. Exact-audit the weighted-depth lemma and fixed-module target reporter.
2. Extend the explicit triangle witness above to audit the actual proposed
   module-recognition and response-update interface, not just its graph shape.
3. Investigate signed removal and a paid cotree-update interface, with all
   old response versions and original gate certificates explicit.
4. Reassess the generic coarse-system route after this bounded target.
   Dynamic min-cost-flow sources screened in docs/literature/lcp-solvers.md
   have different certificates and explicit subpolynomial overhead; they
   are context, not direct OP3 imports. Constrained elimination remains
   another route, subject to its source parameter and locality obligations.

Formal proof imports, if promoted, are within this note: module response
transforms, persistent affine primitives and original obstacle comparison.
No new cross-note dependency or active-manuscript promotion is implied.
