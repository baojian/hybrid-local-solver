# OP3 overnight continuation

Last updated: 7 September 2026. The user authorized at least ten additional
hours of substantive research and will inspect the results tomorrow.

Automation: `op3-overnight-research`, attached to the existing task, resumes
at one-minute intervals when the task is idle (shortened from fifteen minutes
to reduce scheduling gaps). Track active work in `OVERNIGHT_WORK_LOG.json`;
exclude scheduling gaps, idle waits and the earlier 48-minute exploration.
At 600 additional active minutes, prepare the synthesis and pause the
heartbeat. Never claim ten active hours from elapsed wall-clock time alone.

## Current mathematical target

The draft in `sections/op3_geometric_events.tex` bounds delivery of geometric
value publications by near-linear final active volume. It leaves the producer
unimplemented: retained responses, detecting due values and certifying no
missed event. OP3 remains open. First critically recheck this reduction, then
construct or falsify concrete mechanisms. A dense reference solve is an audit
oracle and must never be counted as an efficient producer.

Main route: retained Schur responses with finite-band geometric publications.
Main alternative: local constrained elimination with charged fill and load
updates. Teleportation continuation is a limited probe. Read the full
`OP3_DIRECTIONS_20260906.md` for the model and initial acceptance criteria.

## Concrete research blocks

1. Derive the exact retained elimination/response algebra for a cyclic family
   with growing attachments. Seek a producer that avoids revisiting all old
   coordinates, and identify exactly which group certificate pays for searches.
2. Implement a charged reference for live-frontier Schur elimination. Compare
   source-driven elimination fill against publication delivery, using exact
   audits on small graphs and scaling diagnostics on asymmetric larger graphs.
3. Determine whether a structural family admits a complete paid algorithm.
   Treat bounded-width or fixed-port success as a scoped theorem, and stress
   it with growing width/rank. Do not present it as arbitrary-graph OP3.
4. Explore local constrained-elimination and source-aware sensitivity as
   alternatives when retained factor state produces dense refreshes. Verify
   primary-source assumptions, including numerical-range and adaptivity.
5. Consolidate actual proofs, scoped obstructions, empirical diagnostics,
   remaining lemmas and the next strongest direction in a morning report.

These blocks guide useful work; change their order when evidence warrants it.
Avoid excessive literature surveying or repeated unchanged test runs.

## State and safeguards

Repo: `/Users/baojian/git/hybrid-local-solver`, current `main` worktree.
Existing edits are this task's initial OP3 exploration; preserve them and any
new unrelated concurrent changes. No active-manuscript promotion, external
publication, commits, other-task messages or new task creation is requested.
Read project instructions and respect provider ownership. No subagents have
been requested for this continuation.

The account's one available reset was successfully redeemed at the user's
request, changing weekly usage from 93% used to 0% used. No reset credits
remain. Do not purchase credits or make another reset attempt automatically.

Verification from the prior block is in `VERIFICATION.md`: the exact audit
and note build passed; broader repository checks have documented pre-existing
AESP size/notation failures and two unrelated lint findings. Do not repair
unrelated files solely to make the overall checks green.

## Findings from the first block

- Derived the exposed-frontier Schur-load recurrence and its fully charged
  explicit-fill ledger in `FRONTIER_ELIMINATION_PROBE.md`. Naive explicit
  fill is cubic on a center-seeded star; rank-one compression is necessary
  even before hard cyclic examples. No fill implementation has been claimed.
- Found the affine composition tree (ACT) primary source, absent from the
  previous literature map. It can implement whole scalar-curve affine maps
  in constant time and queried edits in logarithmic time.
- Derived an RPPR tree-message embedding `nu_i(t)=t+gamma*u_i(t)` that remains
  strictly increasing across the zero branch. Each parent recurrence uses
  two whole-curve affine maps, one new knot, and sums of convex child curves.
- A small-to-large, positive-hinge merge suggests an `O(n log^2 n)` exact
  supplied-tree algorithm. It must retain child versions for reconstruction;
  persistent ACT node copying and the allocation bound remain to implement
  and verify. This is conditional, not a theorem already promoted.
- The explicit rational curve oracle passed 1,152 comparisons against an
  independent exact obstacle routine on all small trees through six vertices,
  all seeds, several parameters and extra grounding. Eight larger diagnostics
  distinguish dense materialization from logical ACT operations. See
  `TREE_AFFINE_PROBE.md` and `TREE_AFFINE_AUDIT.json`.
- Componentwise inversion of a sum of curves is invalid; do not import the
  source's tree-set shortcuts for our inverse-type affine map. Coalesce
  curves before applying that map.

## Findings from the second block

- Implemented the persistent ACT as immutable AVL nodes with affine lazy
  tags and positive-hinge suffix merging. `thm:op3-persistent-tree` now gives
  the supplied-tree `O(n log^2 n)` word-work and allocated-storage proof.
  This is **Proved here**, a draft awaiting independent review.
- The persistent audit passes 1,152 comparisons, 43,614 inverse round trips,
  and 19,584 checks of retained child versions against separate exact obstacle
  solves. Twenty-four larger diagnostics count actual visits and allocations.
  See `PERSISTENT_TREE_AUDIT.json` and `TREE_AFFINE_PROBE.md`.
- Implemented an exact local solver for a promised cycle with arbitrary
  pendant-leaf counts and an arbitrary seed. It uses two active tips before
  closure, then a Schur block of dimension at most three, one fixed record
  per committed interior vertex and one final reverse pass. All adjacency,
  degree replies, event searches, state and output are charged. The proof
  draft `thm:op3-local-cycle` and ACL corollary give `O_tilde(1/eps_appr)`
  work on this family. They do not resolve arbitrary-graph OP3.
- The cyclic audit passes 5,265 exact comparisons, including 1,702 cases
  with leaf activations after cycle closure. Larger graphs with 380, 1,533
  and 6,140 vertices each use only 55 center-row scans, 213 inspected entries
  and 160 degree replies at the reported fixed parameters. Audit-only KKT
  passes inspect the full graph separately. See `LOCAL_CYCLE_AUDIT.json`.
- An exact 15-vertex witness refutes automatically freezing a longer
  attachment: a length-two branch changes response after its center's next
  cycle neighbor activates. This is a scoped representation obstruction,
  `prop:op3-cycle-unsettled-attachment`, not an algorithmic lower bound.
- Reconciled the new mechanisms with existing notes. Scalar homotopy, lazy
  tree streams and pure-cycle symmetry were already developed in
  `delayed_reflection_ladder`. The lazy tree bound pays every ancestor walk.
  `aesp_cd_l1_rppr` already isolates the persistent affine-hull meld needed
  for general two-port threshold aggregation. Do not present those earlier
  ideas as new or assume the ACT supplies the missing hull.

## Findings from the third block

- **Proved here**, awaiting independent review: the length-two obstruction
  can be handled by retaining a bounded region of changing responses.
  `lem:op3-attachment-saturation` uses discounted center-hitting times;
  `lem:op3-cycle-interior-growth` shows every attachment of size at most q
  is settled at distance 2q² behind an active end. The solver discovers q
  and cycle ports through charged bounded probes; q is not supplied advice.
- `thm:op3-bounded-attachments` gives exact-real word work
  `O_tilde(q³(1+vol(S)))` and storage `O_tilde(q²(1+vol(S)))`, or
  `O_tilde(q³/eps_appr)` ACL work. This is a cycle-seed theorem for one
  cycle with arbitrary finite tree attachments. It is neither uniform in
  attachment size nor an arbitrary-seed/arbitrary-graph theorem.
- **Measured:** 1,909 comparisons with the exact obstacle reference, eight
  larger full-graph KKT checks, and 195 saturation checks pass. The larger
  cases include branching attachments, complete cycle closure, many
  committed prefixes and unchanged local work under ambient enlargement.
  See `BOUNDED_ATTACHMENT_AUDIT.json` and the associated probe.
- **Open:** the sharper discounted bound `p_i>=1/T_q(1/gamma)` passes
  2,247 exact parameter cases and 6,155 integer-polynomial comparisons on
  all rooted tree/start pairs through q=9. The latter verify all gamma for
  those finite graphs, using nonnegative coefficients after `s=1+z`;
  cofactors are cross-checked against independent rational systems.
  A general coefficient induction is missing. This conjecture is not used
  by the proved conservative theorem. See
  `DISCOUNTED_ATTACHMENT_EXTREMAL_PROBE.md` and its durable audit.
- **Refuted:** simply discarding q from the classification work bound.
  A seed on a triangle with a q-vertex star attached has support volume
  three at alpha=1/3, lambda=1/10, while the current solver reads the
  entire star. For q=256 it exposes 258 rows. A direct initial neighbor
  gate check would already avoid this particular family; it is a scoped
  implementation witness, not a universal lower bound. See
  `INACTIVE_ATTACHMENT_AUDIT.json` and `BOUNDED_ATTACHMENT_PROBE.md`.

## Findings from the fourth block

- **Proved here**, awaiting independent review: `thm:op3-two-port-frontier`
  gives an exact support-local solver when at most one nonseed vertex of
  degree at least three is positive. Keep the seed and that vertex, and
  eliminate every other admitted vertex immediately. A low-degree pivot
  has at most one inactive successor, so only one old frontier record can
  change. Shared candidates combine all incident path contributions.
- Implemented the missing ordinary planar reporter with an AVL point tree
  and persistent AVL upper-hull sequences. Its own complete draft gives
  conservative `O(log^4 N)` point updates and `O(log^2 N)` queries, counting
  every sequence selection, merge, copied record and discarded state.
  It uses no unimplemented hull oracle, full hull-array copies or bulk
  affine transformation. Working space is `O(N log N)`.
- Therefore the graph algorithm costs `O((1+vol(S)) log^4(2+vol(S)))` and
  gives `O_tilde(1/eps_appr)` ACL work with lambda=eps_appr. It requires
  no supplied topology, retained labels, path lengths or attachment sizes.
  All scanned rows belong to positive output vertices. It detects an
  outside-class activation before scanning that additional branching row.
- **Measured:** 8,329 exact reference comparisons pass, with 18,791 correct
  outside-class detections and nine larger KKT cases. Three growing inactive
  descendants retain identical eight row scans, 17 entries and nine degree
  replies. A graph with 66,162 vertices and shared quiet reports needs only
  98 positive row scans and 258 entries. Unequal bundles with up to 128 paths
  include many cycles. See `TWO_PORT_FRONTIER_AUDIT.json` and its probe.
- The planar primitive passes 5,136 exact extreme queries and 1,606 complete
  comparisons with independently constructed static upper chains. Its
  strictly concave stress cases go through 512 points; duplicate/vertical
  points, deletion, replacement and zero query coordinates are covered.
  See `DYNAMIC_UPPER_HULL_AUDIT.json`.
- **Refuted:** a 1.1-relative normalized Schur extreme return suffices for
  original ACL quietness. Three two-arm witnesses check every previous
  admission against that same approximate-return contract and then allow
  a quiet return while the other tip violates the original tolerance by
  factors 1.52, 2.54 and 4.05. Full tridiagonal reconstruction independently
  verifies the physical residuals. An attempted one-arm-first chronology
  was invalid and was replaced by the checked balanced-then-biased trace.
  See `SCHUR_RELATIVE_REPORTER_PROBE.md` and its audit. Do not confuse
  this rejected normalization with the original-value geometric interface.
- Reconciled novelty with prior notes: stable two-port reporters and exact
  unequal-spider elimination were already proved in AESP--CD and
  propagate-settle. The new result verifies their structural locality
  obligations for a second discovered branching vertex and implements the
  exact reporter. Their bulk-pullback-and-meld gap remains untouched.
- **Source candidate:** Chan, arXiv:1903.08387v1, Theorem 4.2 (PDF pp. 10–11),
  supplies polylogarithmic dynamic 3D extreme queries; its Lemma 4.1 uses
  deterministic shallow cuttings. The theorem and update recurrences were
  checked, but no third-coordinate backend/import is completed here.

## Findings from the fifth block

- `thm:op3-branch-core-flux` and `BRANCH_CORE_FLUX_PROBE.md` now give a
  complete growing-core construction: each unfinished path's physical flux
  depends on one retained potential, so scalar publication queues handle
  shared frontier gates in the original residual scale. The dense inverse
  yields `O_tilde((1+r^2)/eps_appr)` work and `O(V+r^2)` storage. All row
  scans belong to the positive output; r is measured on this new
  `lambda=eps_appr/2` trace. General OP3 remains Open.
- `BRANCH_CORE_FLUX_AUDIT.json`: 27,120 exact face/obstacle comparisons,
  17 larger/targeted residual checks, and independent intermediate checks
  of 9,717 inverse entries, 4,345 physical fluxes and 3,253 shared gates.
  The 102,707-vertex shared-report case reads 271 rows and 878 entries,
  with 16 retained vertices. Exact publication/admission ties and all three
  prior Schur-cancellation graphs pass.
- `prop:op3-dense-core-binary-tree` proves cubic explicit-inverse writes on
  balanced trees with full required support. `BRANCH_CORE_COST_AUDIT.json`
  verifies four sizes through 127 vertices. This is a representation-specific
  obstruction on an easy family, not an OP3 lower bound.
- Chan 2019 Theorem 4.2's fixed-three-coordinate source contract is now
  reconciled: full query proof, linearithmic space, local initialization,
  duplicate labels and absence of its unrelated hull-size general-position
  restriction. No 3D backend is implemented. The scalar flux construction
  makes that bounded extension less urgent than implicit core response.

## Findings from the sixth block

- **Proved here**, awaiting independent review: the live-core refinement is
  now implemented. `thm:op3-live-core-peeling` gives
  `O((|U|q^2+qV+VL) log(2+V))` exact-real word work and `O(V+q^2)`
  storage, where q counts the largest simultaneous core, including temporary
  admissions. It returns the original ACL certificate at lambda=eps_appr/2.
  Every inspected adjacency row belongs to the positive output.
- A nonseed reduced-degree-two pivot has at least one retained neighbor and
  at most one inactive neighbor. It can therefore move one grouped physical
  flux without creating inactive–inactive fill. Group moves and coalescences
  preserve original incidence counts and lower publications; they never copy
  a physical membership list. Dense inverse deletion uses original labels,
  so old recovery equations cannot be corrupted by positional slot reuse.
- **Measured:** `LIVE_CORE_PEELING_AUDIT.json` records 54,240 exact atlas
  comparisons through seven vertices under FIFO and LIFO policies, plus 50
  structured checks. Independent trace checks cover 4,268 faces, 15,476
  inverse entries, 6,872 reduced equations, 8,497 physical groups and 6,728
  shared gates. The 41,059-vertex grouped-report graph uses 98 positive rows,
  peak core three, and a group containing 64 original physical incidences.
- **Proved here:** `prop:op3-live-core-binary-order` makes the admission-order
  comparison source-valid. On full-support balanced binary trees, LIFO has
  q<=h+1 and near-linear work; FIFO has q>=2^h and cubic inverse writes.
  Exact checks through 127 vertices give peak cores 7 versus 64.
- **Refuted:** LIFO plus current-degree-two peeling guarantees a uniformly
  small live core. `prop:op3-live-core-interior-tree` gives a canonical
  finite binary-tree family where the obstacle support never reaches any
  original leaf. There can be no first peeling step. Mandatory dense inverse
  writes exceed the OP3 scale for this backend. This is not an OP3 lower
  bound: fixed teleportation already permits ordinary local push on the
  family. `LIVE_CORE_WIDTH_AUDIT.json` verifies ten implicit-tree cases with
  an independent exact radial obstacle oracle, through 2,097,151 ambient
  vertices and 127 positive rows; both policies have no removals.
- Reconciled the next question with prior notes: the existing six-vertex
  threshold reordering varies rho on a cyclic graph; the existing kinetic
  caterpillar reporter assumes a backbone-first phase. Neither resolves
  fixed-lambda root-threshold changes under general legal tree admissions.

## Findings from the seventh block

- **Proved here**, awaiting independent review:
  `lem:op3-root-resistance-transform` identifies the common affine map for
  each lowest-common-ancestor group of surviving root thresholds. The
  harmonic diagonal transformation gives `G_px=h_p h_x R_LCA(p,x)`.
  `cor:op3-root-coordinate-update` supplies exact harmonic, offset and
  resistance updates. These are algebraic identities, not a fast reporter.
- **Measured:** `ROOT_THRESHOLD_ORDER_AUDIT.json` covers 22,440 actual
  traces on every nonisomorphic tree through nine vertices, every seed,
  six parameter pairs and five policies. It verifies 110,542 legal
  admissions, 115,237 Schur-row updates, 46,912 within-group factor checks
  and 406,131 Green/resistance and coordinate-update checks. All final
  original ACL certificates pass; all 13,464 exact-stop outputs agree
  with the independent obstacle reference. All dense work is audit-only.
- **Refuted:** a stale minimum certifies exact quietness, including under
  minimum-threshold admission. Two separate nine-vertex trees distinguish
  FIFO at lambda=1/40 and the exact minimum policy at lambda=1/31, both
  alpha=1/7. In each, the old minimum stays quiet while another surviving
  candidate becomes positive. The proofs and exact coefficients are in
  `sections/op3_root_threshold_groups.tex` and `ROOT_THRESHOLD_ORDER_PROBE.md`.
- **Refuted for arbitrary legal traces:** that shortcut also certifies ACL.
  A fifteen-vertex tree with alpha=1/1009 and lambda=2/51 has an exact
  checked prefix where stale-minimum validation misses an original residual
  violation by a factor about 1.0638583. This is a different policy from
  the minimum-threshold policy. It does not refute physical-flux queues or
  lower-bound OP3. `ROOT_THRESHOLD_WITNESSES_AUDIT.json` records each gate.
- `MINIMUM_ROOT_THRESHOLD_AUDIT.json` uses exact lambda intervals rather
  than an epsilon grid: the next minimum label is independent of lambda
  until stopping. Through eleven vertices and three alpha choices, every
  seed, it checks 13,179 complete symbolic sequences and 122,388 admissions,
  finding 33 strict quiet-pair reorderings and 39 missed-positive intervals.
  The saved fixed-parameter witnesses are independently reconstructed.
  No minimum-policy ACL miss was found in this finite family; a universal
  ACL guarantee remains Open.
- Four implicit backbone families show arbitrarily many distinct ancestor
  group maps. A literal group-by-group implementation has quadratic map
  count in backbone length. Epsilon is exponentially small, so this is
  neither an OP3 lower bound nor a refutation of logarithmic-in-accuracy
  amortization. It identifies a group-maintenance cost to account for.

## Findings from block 8

## Latest ordered-cluster result

**Proved here, awaiting independent review:**
`sec:op3-ordered-path-clusters` gives a finite homogeneous chart, exact
adjacent-path separation, an implemented persistent projective chain and
complete rooted compress/rake/forget summaries. Whole maps cost O(1),
separated merges O(log^3 N) work/O(log^2 N) copies, and gate queries
O(log^2 N), in the exact-real word model.

**Measured:** 516 independent hull comparisons and 18,819 full Schur
comparisons pass, including all trees through seven vertices, retained
versions and five implicit families through 128 active vertices with every
boundary row retained. The driver rebuilds supplied hierarchies.

**Conditional:** O(cvol(U) log^4(2+cvol(U))) local tree work follows if the
online hierarchy contract is discharged. The top-tree primary source has
been checked; source exposure during links, every callback shape, home-edge
payload updates and active-only allocation are the next exact audit.
Read `ORDERED_PATH_CLUSTER_PROBE.md`. Arbitrary-graph OP3 remains Open.

## Findings from block 9

## Latest complete tree result

**Proved here, awaiting independent review:** `thm:op3-local-top-tree`
gives a deterministic exact obstacle/ACL algorithm on arbitrary trees with
O(cvol(U) log^4(2+cvol(U))) local exact-real word work and
O(cvol(U) log^3(2+cvol(U))) space, including every retained version.
Graph discovery, home-edge payloads, failed queries, all cluster operations
and final output are charged. The source balancing algorithm is imported;
the complete application callbacks are implemented and exactly audited.
This implies O_tilde(1/eps_appr) tree ACL work and exact O_tilde(1/rho)
tree RPPR work in the nonzero regime. It is not a numerical-stability claim.

**Measured:** `TOP_TREE_CALLBACK_AUDIT.json` checks 650 source-valid faces,
167,384 legal binary joins, 26,130 independent Schur oracles, 168,294 valid
summaries, 650 exposure transitions and 1,296 payload refreshes. Supplied
hierarchy enumeration is reference work, not the published online algorithm.

**Proved here / Measured:** a uniform shift C=1/bar_alpha makes every
cluster load negative while allowing the physical seed to be interior.
The geometric root may therefore differ from the seed. The exact shifted
reporter and one-cycle restoration identities are in
`sec:op3-shifted-tree-clusters`; 564 faces check 33,550 conditional identities
and 1,972 valid physical-seed-interior clusters. Two cycle witnesses pass.

**Next Open target:** `UNICYCLE_TOP_TREE_PROBE.md` specifies local unicyclic
continuation: one exceptional two-parent candidate, a charged point query,
one paid re-rooting at cycle closure, two fixed cycle ports and the corrected
root solve. A triangle witness proves that the uncorrected spanning-tree
response can be negative; retain signed affine responses. Arbitrary-graph
OP3 remains Open. No result has been promoted to the active manuscript.

## Resume point

The tree hierarchy condition has been discharged as a proof draft, using
an explicit source import. Do not restart its completed callback or shifted
cluster audits. Read `UNICYCLE_TOP_TREE_PROBE.md` for the next complete
algorithmic target and precise acceptance criteria. Implement point queries
and actual local cycle discovery/closure; keep the supplied hierarchy audit
separate from a claimed fast source hierarchy.

All new claims await independent review. Arbitrary-graph OP3 remains Open.
The actual active-time ledger controls the ten-hour minimum; no idle gap
counts. Leave the heartbeat ACTIVE until 600 additional active minutes.

## Findings from the tenth block


**Proved here, awaiting independent review:** `thm:op3-local-unicyclic`
extends the local exact obstacle/ACL construction to every finite simple
connected unweighted unicyclic graph, with an arbitrary physical seed and
unbounded tree attachments. Its exact-word work is
O(1+cvol(U) log^4(2+cvol(U))) and its space, including historical application
versions, is O(1+cvol(U) log^3(2+cvol(U))). This gives O_tilde(1/eps_appr)
ACL and exact O_tilde(1/rho) RPPR in the nonzero regime.

The new ingredients are a charged named-coordinate query, the unique
exceptional two-parent candidate, one paid re-rooting at cycle closure, and
uniform-shift restoration at two fixed ports. Every unsuccessful gate check,
original graph query, payload change, historical allocation and final output
is included. The published height-bounded balancing algorithm remains an
explicit **Source** import; its fast online implementation is not supplied.

**Measured:** `CLUSTER_POINT_QUERY_AUDIT.json` checks 58,816 named coordinates.
`LOCAL_UNICYCLIC_CLUSTER_AUDIT.json` checks 3,888 atlas executions over all
78 tree/unicyclic graphs through seven vertices, plus sixteen larger explicit
attachment executions and four finite implicit private-star examples. There
are 16,371 independent face solves, 26,043 original gate checks, and 319
negative uncorrected spanning-tree faces. The implicit examples scan only
27, 51, 45 and 48 original entries. Reference hierarchy rebuilding and full
validation recovery are counted separately from the proposed online work.

**Next Open target:** `BOUNDED_CYCLE_RANK_PROBE.md` proposes partitioning the
active spanning tree into O(q) two-port components, glued by a small coarse
system, where q is the cycle rank of the locally revealed graph. Multiple
exceptional candidates and paid repartitioning must be audited before a new
theorem is stated. Arbitrary-graph OP3 remains Open; no manuscript promotion
or independent review has occurred.


## Findings from the eleventh block


**Proved here, awaiting independent review:** `thm:op3-local-cycle-rank`
gives a local exact obstacle algorithm on arbitrary finite simple connected
unweighted graphs with explicit support parameters r and q. Here r is the
cycle rank inside the final positive support and q is the rank of the graph
revealed by its scanned incidences, excluding edges between inactive vertices.
For V=cvol(U) and L=log(2+V), the work is

`O(1 + V*((1+r)*L^4 + (1+r)^3 + q*L^2))`.

This gives O_tilde((1+r^3+q)/eps_appr) ACL and exact
O_tilde((1+r^3+q)/rho) RPPR. Shared-port copies, duplicate diagonal/load
corrections, exceptional gates, cycle-birth repartitioning, matrices, failed
checks and final output are paid. The online top-tree balancing remains an
explicit **Source** import. The implemented audit rebuilds its reference
hierarchies and separates those costs.

**Measured:** `LOCAL_CYCLE_RANK_CLUSTER_AUDIT.json` passes 54,240 executions
on all 995 connected atlas graphs through seven vertices, every seed, four
parameter pairs and two policies. Twenty larger explicit examples and five
finite implicit private-star examples also pass. They check 217,410 positive
faces, 168,368 independent coarse Schur systems and 483,413 original gates.
The atlas includes 33,074 admissions creating multiple cycles and 3,441 quiet
exceptional checks. The implicit graphs scan only 58/51/48/62/70 entries.

**Proved here / Measured:** `sec:op3-cluster-green` obtains selected
conditional inverse entries from stored scalar elimination records.
`CLUSTER_GREEN_QUERY_AUDIT.json` checks 29,408 affine/variance identities
and 123,844 covariance pairs against 2,664 independent conditional inverses.

**Next Open target:** `COARSE_INVERSE_UPDATE_PROBE.md` specifies a maintained
coarse inverse: ordinary rank-one updates, old-port promotion, one border
containing every active parent, and optional removal of the transient
insertion parent. Its proposed r^2 improvement is not yet an end-to-end
algorithm or theorem. General OP3 remains Open, and every new proof draft
still awaits independent review.


## Latest maintained coarse inverse result

**Proved here, awaiting independent review:** `thm:op3-maintained-coarse-inverse`
completes the selected-Green transaction and improves active-cycle-rank
work to

`O(1 + V*((1+r)*L^4 + (1+r)^2 + q*L^2))`.

The ACL consequence is O_tilde((1+r^2+q)/eps_appr). Separately, the same
exact-obstacle algorithm gives O_tilde((1+r^2+q)/rho) exact RPPR work.
The graph, access and exact-real word model are unchanged. The proof pays
for every old-port promotion, old-version response query, temporary parent,
dense update, restriction copy, source rebuild, quiet gate and final output.
The finer trajectory ledger uses cycle-birth count b and retained count p:
O(1+V*((1+b)*L^4+(1+p)^2+q*L^2)). Only the current dense inverse is retained;
all historical application versions and their old port values are charged
within the stated r-based space bound.

**Measured:** `MAINTAINED_COARSE_INVERSE_AUDIT.json` passes 54,240 atlas
executions on all 995 connected graphs through seven vertices, every seed,
four parameter pairs and two policies; twenty larger explicit cases, five
implicit private-star cases and the exact triangle witness also pass.
There are 217,490 independent inverse certificates, checking 2,295,640
entries of J*K=I against original-matrix Schur elimination, 483,416 explicit
original-gate checks plus 859 implicit-case gates, and 198,003 historical
component rechecks. Atlas updates include 21,543 temporary-parent drops,
5,858 newly promoted Steiner junctions, up to five simultaneous old
promotions and six active parents. No coarse solve feeds an admission.
Reference hierarchy rebuilding and full validation remain separately
charged; the fast online balancing algorithm is an explicit Source import.

**Next Open target:** `COARSE_PUBLICATION_PROBE.md` proposes using the
component reporters as the previously missing geometric-publication producer.
It may remove repeated exceptional-gate scans and the q term for ACL work.
The proposal must replace tuple-copying parent lists, count cached-edge
redelivery and publication-only payload updates, and distinguish current
inverse storage from optional historical port-value snapshots. The final
point may stop before the exact obstacle optimum, so no exact-RPPR or OP2
consequence is asserted for that proposed variant. General OP3 remains Open.

Block 12 closed at 2026-09-07T01:31:20.138486+00:00: 29.610 active minutes. Conservative cumulative additional active research: 472.787 minutes; 127.213 minutes remain toward the requested 600. No unverified gap was counted in this block. The same-task heartbeat remains ACTIVE for the publication-producer probe.
