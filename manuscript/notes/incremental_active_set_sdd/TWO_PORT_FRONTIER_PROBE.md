# Local discovery with two retained vertices

Date: 7 September 2026. **Proved here:** complete implementation and proof
draft awaiting independent review. General OP3 remains **Open**.

This block supplies a second way around the large inactive-attachment
problem. Keep the seed and the first admitted nonseed branching vertex;
eliminate admitted degree-one and degree-two vertices immediately. Every
pending boundary condition then depends on only two retained potentials.
Crucially, an update changes an individual boundary record, without changing
the coordinate system of all old records.

The exact support condition is

\[
 \#\{i\in S\setminus\{v\}:d_i\geq3\}\leq1,
\]

where S is the positive obstacle support at the requested parameters.
Neither the graph topology nor those retained labels need be supplied.
The ambient graph outside the support can be arbitrarily large and complex.
If another nonseed branching vertex must activate, the algorithm detects
that the condition fails before reading its row.

## Why the old keys really stay stable

Write the Schur matrix and load on the retained set C as H and f. Each
inactive exposed vertex j has a diagonal delta_j, negative load h_j, and
nonnegative two-vector a_j. Its exact gate is

\[
 g_j=h_j+\boldsymbol a_j^T\boldsymbol u_C,
 \qquad \boldsymbol u_C=\boldsymbol H^{-1}\boldsymbol f.
\]

A positive degree-at-most-two candidate has at least one original active
neighbor, so it has at most one inactive successor. Its elimination changes
the two-by-two matrix and at most that successor's record. Different active
paths that reach the same inactive vertex update the same record; no
independent-copy gate is used. No fill edge is created between two inactive
vertices. Original inactive–inactive edges are revealed only when one
endpoint activates. The saved equations recover all eliminated values in
one final reverse pass.

Normalize `p_j=a_j/(-h_j)`. One planar extreme query in direction u_C
finds a legal gate if `max_j p_j·u_C>1`; otherwise it certifies all exposed
gates quiet. Unexposed vertices have no active neighbor and need no query.
The second retained coordinate is reserved as zero from the beginning;
discovering its vertex changes only records along its scanned row.

## Implemented reporter and charged bound

`dynamic_upper_hull.py` uses an AVL tree on labeled planar points. Each
node stores its upper hull as a persistent AVL sequence. Horizontally
separated hulls are merged by two nested binary searches for their common
upper tangent, then by sequence splits and concatenation. Full hull arrays
are never copied. Vertical coincidences and duplicate points are supported.

Including every indexed sequence access gives a conservative
`O(log^4(2+N))` point-update bound and `O(log^2(2+N))` extreme-query bound.
Working storage is `O(N log(2+N))`; allocated and discarded recursion
records are charged to updates. The solver makes only `O(1+vol(S))`
updates, queries, graph accesses and reverse records. Its bound is therefore

\[
 O\bigl((1+\operatorname{vol}(S))\log^4(2+\operatorname{vol}(S))\bigr).
\]

The formal statements are `lem:op3-two-port-stability`,
`lem:op3-avl-upper-hull`, and `thm:op3-two-port-frontier` in
`sections/op3_two_port_frontier.tex`. With lambda=eps_appr, the obstacle
residual gives the ACL witness and `vol(S)<=1/eps_appr`. This attains OP3's
soft-O work scale on the stated class. It uses exact-real word arithmetic;
coefficient-bit complexity and floating-point stability are outside the claim.

## What was already known

**Context/provenance**, not formal proof imports:

- `aesp_cd_l1_rppr/sections/body/06b_prop_aesp_cd_dynamic_reporters.tex`,
  `cor:aesp-cd-stable-port-reporter`, already reduces stable two-port keys
  to ordinary dynamic planar extreme queries. The same file's
  `prop:aesp-cd-sp-meld-hull-reduction` explicitly requires a stronger bulk
  transformation and meld operation for changing series-parallel parses.
- `propagate_settle_framework/sections/body/10_sec_kinetic_thresholds.tex`,
  `thm:rooted-spider-kinetic`, already gives exact arrowhead elimination and
  kinetic scalar gates on unequal rooted spiders. The two-port construction
  extends that mechanism to a locally discovered second branching vertex,
  shared inactive candidates and multiple cycles.
- **Source:** [Jacob–Brodal, *Dynamic Planar Convex Hull*](https://arxiv.org/pdf/1902.11169),
  Theorem 1, PDF p. 2, and computational model §2.2, PDF pp. 5–6, provide
  faster standard individual updates and extreme queries. The conservative
  AVL implementation here is separately proved and tested. We do not claim
  a new optimal hull theorem or the missing bulk-transform-and-meld oracle.

## Exact evidence

`TWO_PORT_FRONTIER_AUDIT.json` records 8,329 exact reference comparisons
through seven vertices, every seed and four parameter pairs. Another 18,791
cases correctly detect a second nonseed branching activation and stop as
outside the class. Nine larger cases pass separate full-graph KKT audits.
In every successful case, the set of scanned rows equals the positive output
support. The algorithm has no ambient iteration or inactive row scan.

| Family | Ambient vertices | Positive vertices | Scanned entries | Degree replies |
|---|---:|---:|---:|---:|
| Partly active attachment; q=64 | 73 | 8 | 17 | 9 |
| Same attachment; q=256 | 265 | 8 | 17 | 9 |
| Same attachment; q=1024 | 1,033 | 8 | 17 | 9 |
| Shared quiet reports, 4 reports | 1,048 | 14 | 34 | 18 |
| Shared quiet reports, 16 reports | 16,570 | 50 | 130 | 66 |
| Shared quiet reports, 32 reports | 66,162 | 98 | 258 | 130 |
| Unequal bundle, 128 paths | 884 | 884 | 2,020 | 884 |

The shared reports have unequal path lengths from both retained vertices
and large inactive leaf populations. Both parent contributions enter each
shared gate. This exercises stable mixed-coordinate boundary constraints,
not merely a set of independent scalar arms. Full-graph KKT and dense
reference work are audit-only and excluded from the reported solver counts.

`DYNAMIC_UPPER_HULL_AUDIT.json` records 5,136 exact extreme comparisons,
1,606 comparisons with independent static upper-chain construction, and
strictly concave hull diagnostics through 512 points. It includes deletes,
replacements, duplicate coordinates, vertical coincidences and zero query
coordinates. Counts cover actual tree visits and allocations. These finite
checks support the construction but do not replace independent proof review.

## Remaining research choices

**Update from the following block:** `BRANCH_CORE_FLUX_PROBE.md` supplies
a growing-core construction using scalar physical-flux publications and
an explicit `O_tilde((1+r^2)/eps_appr)` dense-core cost. It resolves the
need for a higher-dimensional reporter on that trace, while leaving the
polynomial response-update cost open. The earlier research targets below
explain the transition to that construction.

The most useful next extension is a growing active branching core. Retaining
more vertices increases both solve size and reporter dimension. Eliminating
them behind a hierarchy instead changes the coordinates of old boundary
records, recreating the bulk-update obligation. Neither extension follows
from the successful two-port theorem.

An approximate reporter also needs a careful error conversion: a relative
error after dividing by `-h_j` permits an absolute gate error proportional
to the accumulated Schur load, which can exceed the original `lambda*d_j`
scale. The geometric publication proof controls original neighbor flux;
it does not automatically justify relative rounding of these transformed
keys. The source-valid failure is now recorded in
`SCHUR_RELATIVE_REPORTER_PROBE.md`: every approximate return in its trace
meets a 1.1 factor, yet the final original residual can exceed the requested
degree tolerance by more than four. This rejects that oracle contract.

A bounded source alternative is Chan's three-dimensional extreme-query structure,
Theorem 4.2 of arXiv:1903.08387v1, PDF pp. 10–11. Its individual updates
have polylogarithmic amortized bounds, with linearithmic initialization;
Lemma 4.1 uses deterministic shallow-cutting
construction. The same low-degree elimination algebra suggests a third
retained coordinate, but that backend is not implemented here. The following
block reconciled its query, degeneracy, initialization and space contract;
see `docs/literature/lcp-solvers.md`. A bounded three-coordinate import
would still leave the cost of an unbounded retained core open.
