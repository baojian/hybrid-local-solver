# Next probe: locally exposed cycle rank and a small coarse graph

Date: 7 September 2026. **Resolved in block 11:** the complete construction
is now **Proved here**, as a draft awaiting independent review, in
`thm:op3-local-cycle-rank`. The original proposal below is preserved, with
the refined proved ledger and measured resolution at the end. The fast
online hierarchy is an explicit published-source import; the audit rebuilds
reference hierarchies. General OP3 remains Open.

## Local parameter, rather than a supplied global decomposition

For connected active U, define r=|E(U)|-|U|+1 and let a_j be the number of
active parents of an inactive boundary vertex j. The graph consisting of U,
its boundary, and only edges incident to U has cycle rank

`q = r + sum_boundary_j (a_j-1)`.

This is locally computable from already scanned incidences. It is monotone
under admissions: admitting j transfers a_j-1 units from the boundary sum
to r; every newly scanned edge to an already discovered boundary vertex
adds one unit. It is at most the original graph's cycle rank, but a huge
unseen cyclic region need not contribute. In particular, at most q
exceptional candidates have a_j>=2, and the total number of their active
parents is at most 2q. Ordinary candidates have one parent and still use
one minimum heap row per active vertex. Maintain every exceptional original
gate by named-coordinate queries, charging all quiet checks too.

These counting identities follow from elementary cycle rank. A useful
algorithm still needs a paid representation after several active cycles.

## Candidate partition of the active spanning tree

Keep an insertion spanning tree T permanently rooted at the physical seed
v and r extra original edges. Mark v and every extra-edge endpoint; there
are at most 2r+1 marks. In T, form the minimal
subtree connecting the marks. Add its vertices of degree at least three
to the retained set P, so |P|=O(r). Its maximal paths between vertices of P
form an O(r)-edge coarse tree.

For each such path, make one connected tree component containing that
path and all unmarked branches attached to its interior. Assign any
unmarked branch at a vertex of P to one chosen incident path component.
Each component then has two retained boundary vertices, and distinct
components share only vertices of P. Their edge sets partition E(T).
All components use original full degrees and shifted fixed loads beta;
the existing two-port top-tree application and projective reporter apply.
For r=0, retain the existing one-port tree representation.

Including v among the marks makes adjacent coarse-path endpoints comparable
in the permanently rooted T. Choose the rootward endpoint as each component's
geometric anchor. This avoids changing vertex depths when the partition is
rebuilt. The uniform shift still permits the physical seed to be interior
in other representations, but no re-rooting is needed for this version.

Keep one permanent global home edge per active vertex: its insertion parent
edge, and the physical root's first admitted edge. A shared retained vertex's
ordinary heap minimum belongs to the component containing that home edge,
and appears there only. At a nonroot retained vertex this is its rootward
path component. The root's first edge may be in a side branch; assign that
branch to one chosen incident path component. Other active vertices have a
unique home component. Every reporter row is therefore counted once without
changing its global edge ownership. A named query uses the home component's
solved port values and current incident-edge locator. Updating the map from
home edge to component during a rebuild is still charged.

## Coarse assembly and original-edge restoration

Sum the component two-by-two Schur matrices and loads into a matrix on P.
If i belongs to m_i components, subtract (m_i-1)*d_i from its summed
diagonal and (m_i-1)*beta_i from its summed shifted load. This removes the
duplicated fixed vertex contribution. Then restore each extra edge by
subtracting gamma from its two off-diagonal positions and adding gamma*C
to both endpoint loads. The resulting matrix should be the exact Schur
complement of the full original active matrix, hence positive definite.

Solve the O(r)-dimensional system, query every component reporter at its
two resulting port values, and separately check all exceptional candidates.
An ordinary positive candidate is a leaf insertion into its parent's
component. If its parent is shared, use that parent's chosen home component.
Other components keep their numerical state; their next reporter queries
use the new coarse port values. Original degrees and beta are fixed, so
there is no degree-wide payload redistribution.

If an admitted candidate has a>=2 active parents, keep one new edge in T,
add a-1 extra edges, recompute the marked partition, and rebuild all current
components from cached active edges. There are at most final r such
repartitioning events. This is a paid rebuild, never an online-free claim.
Each component has separate structural copies of shared ports; these are
application records glued by the coarse equation, not new PageRank vertices.
Count their multiplicity, locator changes, original-label dictionaries and
all re-homing work explicitly.

## Tentative ledger to prove or reject

Writing V=cvol(U_final) and q for the final exposed cycle rank, a conservative
candidate bound is

`O((1+V)*((1+q)*log^4(2+V) + (1+q)^3))` exact-word work.

The proposed charges are: O(V) original row/degree and incidence work;
O(V log^4 V) individual payload changes and leaf updates; at most q complete
rebuilds, each O(V log^4 V); O((1+q)^3) coarse solve per admission;
O((1+q) log^2 V) ordinary reporter queries and exceptional point queries per
checkpoint; one final O(V polylog V) recovery. Current coarse matrices and
their copies cost O(q^2), and must not be hidden behind a solver call.
Historical application state may cost O((1+q)*V log^3 V); retaining every
temporary coarse solve is unnecessary and must not be claimed free.

For fixed q this would again imply exact O_tilde(1/rho) RPPR and
O_tilde(1/eps_appr) ACL. It would handle arbitrary ambient graphs with a
locally small revealed cycle rank. For growing q this bound does not settle
OP3 and may be worse than existing methods. No universal lower bound follows.

## Required falsifiable checks

1. Construct and independently verify the edge partition, retained vertices,
   shared-port duplication corrections and unique row homes on all small
   connected graphs, including intersecting and disjoint cycles.
2. Compare every coarse solve and component reporter with an independent
   full active-face solve along strict source-driven admission traces.
3. Include a candidate with three or more active parents, simultaneous
   exceptional candidates, and admissions that create several cycles at once.
4. Include shared retained vertices with many component copies, physical
   seeds interior to a component, and extra edges whose endpoints coincide
   with previous marks or junctions. Verify all affine-load signs.
5. Track actual local q and its monotonicity; charge scans, all exceptional
   quiet checks, changed-home paths, component copies and repartition work.
6. Distinguish a rebuilt reference driver from the imported online hierarchy
   and prove that each non-closure leaf update preserves the fixed partition.

If this closes, the next difficult target is a representation avoiding the
polynomial dependence on exposed cycle rank, or a genuinely local graph
family with large cycle rank but separately compressible cycle blocks.

## Possible improvement after the conservative construction works

The marked set only grows, and permanent global home edges and depths need
not change. Thus a new cycle might refine a few existing components through
paid splits and links instead of rebuilding the entire active tree. Do not
assume this is free: splitting a high-degree retained vertex into shared
component copies can otherwise move many incidences, and the published
top-tree API exposes at most two external vertices per component. A valid
refinement interface would have to account for that structural duplication
and every affected reporter map. The conservative q full-rebuild charge
above remains the default until such an interface is proved.

## Resolution: active rank and boundary excess have different costs

`sections/op3_local_cycle_rank.tex` proves the construction with the sharper
bound `O(1+V*((1+r)*L^4+(1+r)^3+q*L^2))`, where r is active cycle rank and
q is final revealed cycle rank. Only r controls partition rebuilds and the
coarse dimension; exceptional parent incidences number at most 2(q-r).
The previous q^3 conservative proposal is therefore unnecessary. Space is
O(1+(1+r)*V*L^3+(1+r)^2), retaining historical cluster state and using
current temporary dense coarse matrices.

The exact audit covers 54,240 atlas executions, twenty larger explicit
examples and five finite implicit private-star examples. It independently
checks 217,410 positive faces, 168,368 coarse Schur systems and 483,413
original gates. All original edge ownership and minimum-row homes are
unique, shared-port duplication is corrected, multiple cycle births and
simultaneous exceptional candidates occur, and inactive hub rows are never
scanned. See `LOCAL_CYCLE_RANK_CLUSTER_AUDIT.json` for full provenance.

The next improvement is `COARSE_INVERSE_UPDATE_PROBE.md`. Selected
conditional Green queries now pass 123,844 covariance comparisons, but a
complete inverse-update transaction and its improved r^2 work theorem are
still Open. Do not replace the established cubic term before that audit.
