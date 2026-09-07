# Live-core peeling: a complete construction and its limit

Date: 7 September 2026. **Proved here:** implemented construction and
proof drafts awaiting independent review. **General OP3 remains Open.**
The initial candidate in this file has now been implemented and audited.

The retained core can shrink when side branches settle. Admit each positive
candidate temporarily, then eliminate any nonseed retained vertex with at
most two distinct neighbors in the current reduced graph. A removed vertex
is saved once for final recovery. The seed is always retained.

The resulting bound is

\[
 O\left((|U|q^2+qV+VL)\log(2+V)\right),\qquad
 V=\operatorname{vol}(U),\quad
 L=1+\log_+\frac1{\bar\alpha\varepsilon_{\rm appr}},
\]

with `O(V+q^2)` working storage. Here q is the maximum simultaneous core
size, including a temporary admission before peeling. Since
`V<=2/eps_appr`, the work is `O_tilde((1+q^2)/eps_appr)`. The algorithm
scans only positive-output rows and may query degrees of their inactive
neighbors. It receives no topology, final support, elimination order or q.
All arithmetic is exact-real word arithmetic; coefficient-bit complexity
and finite-precision certification remain outside this statement.

The formal result is `thm:op3-live-core-peeling` in
`sections/op3_live_core_peeling.tex`. The implemented parameter is the
maximum live core, rather than the permanent original-branching count of
`BRANCH_CORE_FLUX_PROBE.md`. Both use `lambda=eps_appr/2`; their permitted
admission schedules can return different valid ACL supports.

## Why removing a vertex does not require a global rekey

The current active graph is connected to the seed. Every nonseed retained
vertex therefore has a retained neighbor. An eligible vertex with at most
two reduced neighbors can touch at most one inactive vertex. Eliminating it
changes at most two neighbors and moves at most one physical-flux group;
it never creates fill between two inactive vertices.

A group `(c,j)` represents a disjoint set of k original boundary edges
ending at inactive j. Its physical sum is

\[
 F_{cj}=a_{cj}u_c+b_{cj},\qquad a_{cj}>0,\quad b_{cj}\leq0.
\]

The stored publication satisfies

\[
 \ell_{cj}\leq F_{cj}\leq\tfrac54\ell_{cj}
                      +k\varepsilon_{\rm appr}/16.
\]

For an eligible core i with retained neighbor c and inactive neighbor j,
its equation is `delta_i*u_i=b_i+w_ic*u_c+a_ij*u_j`. Moving its group to c
replaces its slope and intercept by

\[
 a'_{cj}=a_{ij}w_{ic}/\delta_i,\qquad
 b'_{cj}=b_{ij}+a_{ij}b_i/\delta_i.
\]

Its original incidence count and lower publication stay unchanged. If a
same-pair group exists, add both slopes, intercepts, counts and publications.
This preserves the shared lower gate at j and its original-degree error
allowance. No group operation copies the physical edge list.

There are only `O(V)` group lifetimes: each original edge starts at most
one direct group, each original vertex is eliminated at most once, and
each elimination moves at most one group. Every fixed lifetime has
`O(L)` publications because `F<=k*gamma/bar_alpha` and the additive floor
also scales with k. Failed queue searches, all visits to retained queues,
retired entries, reduced-edge changes and recovery are charged separately.

The inverse after eliminating a retained vertex is the principal submatrix
of the previous inverse on the remaining retained labels. The implementation
uses original labels as dictionary indices. It deletes one row and column
without reindexing old records. Saved reverse equations also name original
vertices; every positive coordinate is recovered exactly once. The solver
uses no reusable positional slots, avoiding the slot-reuse hazard identified
in the initial design.

## Exact evidence

`LIVE_CORE_PEELING_AUDIT.json` records **54,240 exact comparisons** through
seven vertices, every seed, four parameter pairs and both FIFO and LIFO
ready policies. Each output is checked against an independent exact solve
on its returned face, the full obstacle optimum, and the original ACL
residual inequalities. Its scanned rows equal its positive output support.

Intermediate audits, including the smaller grouped-report cases, check
4,268 full faces, 15,476 retained-inverse entries, 6,872 reduced core
equations, 8,497 physical groups and 6,728 shared gates. The independent
auditor explicitly partitions original boundary edges into disjoint groups;
its 1,998 membership copies are audit-only. Those sets never exist in the
local solver.

Fifty additional diagnostics cover cyclic subdivisions, many shared inactive
reports, the three earlier cancellation examples, balanced trees, unequal
combs and cycles, and coalesced groups with up to 64 original incidences.
The 64-path report graph has 41,059 ambient vertices and only 98 positive
rows; its peak core is three and a single group eventually contains all
64 boundary incidences. Exact evidence supports the proof but does not
replace independent review.

## Admission order can change the live core substantially

`prop:op3-live-core-binary-order` proves a separation on the complete
binary tree of height h with `alpha=1/1009` and
`eps_appr=alpha/(10*6^h)`. Every exposed frontier is ready after its queues
settle. FIFO therefore explores by levels; LIFO explores a subtree before
returning to its siblings. Under LIFO, completed subtrees are peeled and
all retained vertices lie on the current root path, so `q<=h+1` and the
work is `O_tilde(n)`. Under FIFO, all internal vertices remain retained
before the first leaf, forcing cubic inverse writes.

| Vertices | FIFO peak core | LIFO peak core | FIFO inverse-entry updates | LIFO inverse-entry updates |
|---:|---:|---:|---:|---:|
| 15 | 8 | 4 | 247 | 48 |
| 31 | 16 | 5 | 2,319 | 160 |
| 63 | 32 | 6 | 20,127 | 480 |
| 127 | 64 | 7 | 167,743 | 1,344 |

On a 128-center asymmetric cycle with length-two/three attached paths,
LIFO's maximum core is four; its final positive support has 335 vertices.
This is a measured example, not a general small-core theorem.

## A source-valid limit: peeling may never start

**Refuted:** LIFO plus current-degree-two peeling guarantees a uniformly
polylogarithmic live core. `prop:op3-live-core-interior-tree` gives an exact
family: a complete binary tree of height `H=3h+5`, with

\[
 \alpha=1/3,\qquad \varepsilon_{\rm appr}=1/(12\cdot6^h).
\]

A single-walk PPR lower bound forces every ACL output to include all
vertices through depth h. A geometric-series upper bound shows that no
original leaf at depth H can be positive in the obstacle at
`lambda=eps_appr/2`. Every admitted nonseed vertex therefore keeps three
original reduced neighbors. There is no first eligible peeling step,
under either ready order or any other legal ready policy in this algorithm.
Thus `q=|U|>=2^(h+1)-1`, and explicit inverse writes are
`Omega(8^h)=Omega((1/eps_appr)^(log_6 8))`, exceeding the OP3 scale for
this backend.

`LIVE_CORE_WIDTH_AUDIT.json` checks both policies using an implicit finite
binary-tree degree/row oracle and a separate exact radial obstacle solve:

| Ambient vertices | Positive rows, either policy | Positive depth | Core removals | Inverse-entry updates |
|---:|---:|---:|---:|---:|
| 511 | 7 | 2 | 0 | 91 |
| 4,095 | 15 | 3 | 0 | 1,015 |
| 32,767 | 31 | 4 | 0 | 9,455 |
| 262,143 | 63 | 5 | 0 | 81,375 |
| 2,097,151 | 127 | 6 | 0 | 674,751 |

The large ambient trees are never materialized. Independent residual
validation covers all positive vertices and their exposed neighbors;
unexposed vertices have no positive neighbor. The radial reference is
audit-only. This is an explicit-response obstruction on a canonical trace,
not an OP3 lower bound. Fixed teleportation already makes ordinary local
push efficient on this family.

## What to investigate next

The successful ingredients are now concrete: scalar physical-flux bands,
shared candidate sums, degree-two core removal, stable-label inverse
restriction and one-pass reconstruction. The missing general mechanism must
handle a large unfinished branching core, rather than rely only on completed
subtrees disappearing. Possible next targets are a higher-degree grouped
response, a hierarchy that pays for common threshold transformations, or
an implicit core response paired with aggregate event certificates.

The earlier rooted-tree threshold iterator already pays ancestor-route
work; the cactus hysteretic-HLD result is still radius-paid. Reimplementing
either at the same cost would not establish OP3. A useful next falsification
is whether actual source-driven branch activations change the order of
surviving root-coordinate thresholds, and which groups share a paid affine
change. Keep that source-valid requirement, the original residual bands,
and all failed-query costs explicit.
