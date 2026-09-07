# OP3 exploration verification

Latest block: see **Overnight block 11** at the end for the local cycle-rank
theorem, selected Green queries and the next inverse-update transaction.

Date: 6 September 2026. Base commit:
`15446d8f946dd03ca42b7e035cd37517ad937a01` on `main`.
The worktree was clean at the start. Changes are uncommitted research notes
and a proof audit; solver implementations and the active manuscript were not
changed.

## Claim status

The new Section 9 is **Proved here**, meaning a proof draft awaiting
independent review. It establishes a conditional reduction with explicitly
unbounded response-production and event-location cost. **OP3 remains Open.**
Finite exact checks support the algebra; they do not prove a fast producer
or replace independent proof review.

`OP3_DIRECTIONS_20260906.md` gives the recommendation. The new source audit
also records the numerical-range assumption in Chen--Peng--Wang; the global
constrained solver is not imported as an unrestricted local theorem.

## Exact audit

Registered audit: `incremental_active_set_sdd.geometric_value_events`.

```text
uv run python experiments/proof_audits/incremental_active_set_sdd/geometric_value_events.py --max-n 6 --structured --output results/raw/op3_geometric_events_n6_structured.json
```

**Passed.** The final run took 37.316 seconds. The durable output is
[`EXPLORATION_AUDIT.json`](EXPLORATION_AUDIT.json), including parameters,
stopping rule, base commit, dirty-state flag and source SHA-256:
`7f41a53954399c3e0413e0607655c1a4d386597aa25e16dd6878c91e681ed065`.

- 19,416 atlas executions: 142 connected graph representatives of orders
  2 through 6, every seed, four teleportation values, three ACL accuracies,
  and batch/singleton admission policies.
- 24 structured executions: a 32-vertex path, a 24-vertex asymmetric ladder
  with extra chords, a 5-by-6 grid, and a barbell; parameters include
  `alpha=1/1000003`.
- 64,400 terminal clipping checks. These use all error-sign corners for
  graph order at most four and four adverse patterns on larger graphs.
- 484 scalar overlap-band checks, including threshold equality and
  asymmetric certified intervals.
- 1,618 teleportation-halving checks, plus the explicit three-vertex-path
  support-birth witness.

The invariant checks cover support safety, positive monotone exact responses,
conservation, lower-publication bands, exact incremental boundary keys,
boundary-signal sandwiches, safe admissions, stopping and ACL clipping.

The dense reference visited total face volume 200,515. Delivered publications
cost volume 150,441, of which 69,625 came from previously active coordinates.
The code charges dense face solves and full scans separately. It also counts
44 batch admissions having no neighbor in the immediately preceding batch.
These are diagnostics of necessary old-state propagation, not solver-runtime
comparisons. There is no random seed because these checks are deterministic
and use exact fractions. The audit is a mathematical reference computation,
not a graph-access implementation of the proposed producer.

## Build and repository checks

- Focused note `make`: **passed**, producing a 13-page PDF. The final LaTeX
  log has no undefined references/citations or overfull boxes. All pages
  were rendered for layout inspection; the new pages 10--13 and revised
  cover were inspected individually.
- Focused `ruff check` and formatting for the new audit: **passed**.
- `make agent-audit`: **passed**.
- `git diff --check`: **passed**.
- `make reproduce`: **stopped at the test stage**, with 231 tests passed
  and three pre-existing failures. It did not reach experiments, figures or
  the active paper build. The task's exact audit and focused note build were
  run explicitly as documented above.
- `make note-audit`: **fails on two pre-existing oversized AESP sections**.
  The modified OP3 note passes its status and size requirements.
- `make lint`: **fails on two pre-existing Python issues** listed below;
  the new audit passes its focused check.

The three failing tests are:

1. `test_known_semantic_aliases_do_not_regress`: an existing `r_rho`
   regularizer alias in
   `aesp_cd_l1_rppr/sections/body/02_eq_aesp_cd_target.tex`.
2. `test_note_inventory_audit_passes`: the AESP files below exceed the
   1,000-line review limit.
3. `test_note_sources_stay_within_reviewable_size_limits`: the same two
   files, at 1,237 and 4,361 lines:
   `aesp_cd_l1_rppr/sections/body/06b_prop_aesp_cd_dynamic_reporters.tex`
   and `aesp_cd_l1_rppr/sections/body/06d_cor_aesp_cd_obstacle_primitives.tex`.

The lint findings are an unused `pagerank_matrix` import in
`problem_definitions/verify_exact_batch_cholesky.py:14` and a lambda
assignment in `spectral_balance_threshold_batch/green_band_stress_exact.py:248`.
All five offending files were verified byte-for-byte identical to the starting
commit. Their hashes are in
[`BASELINE_CHECK_FAILURES.json`](BASELINE_CHECK_FAILURES.json).

The initial status edit also triggered a required-field check. It was fixed;
the final test run above has no failure caused by the OP3 edits.

## Coverage and handoff

[`EXPLORATION_COVERAGE.json`](EXPLORATION_COVERAGE.json) distinguishes the
status-card survey from targeted mathematical reads and primary-source
inspection. This was a focused exploration within the authorized two-hour
window, not a line-by-line audit of the entire notes directory. Its timestamps
record actual elapsed work, including verification.

Next target: a paid producer for the geometric-publication interface on an
asymmetric cyclic family with growing attachments. Keep response production,
change location, publication delivery, and terminal completion in separate
work counters. Do not interpret successful delivery accounting as a bound on
the first two costs. The main alternative is local constrained elimination;
teleportation continuation is a limited secondary probe.


## Overnight block 1

The tree affine-response oracle passed 1,152 exact obstacle comparisons and
produced eight larger path/star diagnostics. Its source hash and parameters
are recorded in `TREE_AFFINE_AUDIT.json`; the script and registration are
under `experiments/proof_audits/incremental_active_set_sdd/`.
Focused lint/format, ownership and diff checks passed. The subsequent
repository test run had 231 passes and the same three pre-existing failures
listed above. No LaTeX source changed in this block; new derivations remain
scoped Markdown probes. The persistent ACT implementation, local discovery
and cyclic-graph extension remain open.

## Overnight block 2

Two implementations and proof drafts were added to this standalone note:

- `persistent_affine_tree.py`: 1,152 exact comparisons, 43,614 value/inverse
  round trips and 19,584 retained-version checks; 24 path/star/binary/comb
  diagnostics through 512 vertices. The final audit is
  `PERSISTENT_TREE_AUDIT.json`, source SHA-256
  `fd9847de989f8c6bc58464a641fca3acff9fa5ff1340b90f7bb278a31c93de20`.
  `thm:op3-persistent-tree` is the supplied-tree work/storage proof draft.
- `local_sun_solver.py`: 5,265 exact obstacle comparisons and full KKT
  checks, covering cycle and leaf seeds; 2,212 closures, including 1,702
  cases with later block-leaf activations. Six larger asymmetric diagnostics
  distinguish the charged local solver from full-graph audit work. A separate
  15-vertex conditional-response witness refutes freezing length-two
  attachments too early. The final audit is `LOCAL_CYCLE_AUDIT.json`, hash
  `8d69c10953d31c9f259be3dc167eecac78152e0f2074efd73fb031a9b2b5235a`.
  `thm:op3-local-cycle` and `cor:op3-local-cycle-acl` are proof drafts for
  the promised cyclic family, not arbitrary-graph OP3.

The full audit commands are registered in `experiments/proof_audits/registry.toml`.
The new files pass focused lint and formatting. Ownership and diff checks
pass. The repository tests again have 231 passes and the same three
pre-existing failures listed above. Broad lint again reports only the same
two unrelated findings, and the note inventory only the two existing
oversized AESP files. The unrelated failing files remain untouched.

The expanded note builds successfully; its log has no unresolved references,
citations or overfull boxes. New proof pages and the revised cover/contents
were rendered and visually inspected. These checks are our own audits, not
an independent mathematical review. No claim was promoted to the active
manuscript or shared theorem ledger.

## Overnight block three

`bounded_attachment_cycle.py` passes 1,909 comparisons against the separate
exact obstacle solver and eight larger KKT-only cases, plus 195 exact
saturation checks. Its SHA-256 is
`609289cc8ed0c2e05449344aad8b7dfcf1937b9293fddb712e5482b062b48f9b`.
`BOUNDED_ATTACHMENT_AUDIT.json` preserves the parameters, stopping rules,
charged operations and larger diagnostics. The work proof is
`thm:op3-bounded-attachments`, a cycle-seed result with polynomial dependence
on actual attachment size q. It is not a general OP3 claim.

`discounted_attachment_extremal.py` passes 2,247 rooted-tree/parameter cases,
18,465 individual rational inequalities and 6,155 exact integer-polynomial
coefficient checks through q=9. The cofactor formulas agree with the separate
rational solves. An early polynomial audit exposed a vertex-order indexing
bug in its own degree array; using a label-indexed degree dictionary fixed
it before this final complete run. The general extremal conjecture remains
Open. `DISCOUNTED_ATTACHMENT_AUDIT.json` has the final source hash.

`inactive_attachment_probe.py` verifies four exact seed-only instances with
attachment sizes 4, 16, 64 and 256. The current full classifier reads all of
the inactive attachment despite constant positive support volume. The
closed-form optimum and full-graph KKT are checked independently of the
charged solver. This is a specific implementation obstruction, avoidable
on this family by an initial gate check. `INACTIVE_ATTACHMENT_AUDIT.json`
records both audit and solver hashes.

All new audits are registered. Focused lint/format, ownership and whitespace
checks pass. The latest repository test run is 231 passed and the same three
pre-existing failures; broad lint still has the same two unrelated findings.
The note inventory still reports only the two oversized AESP files recorded
in `BASELINE_CHECK_FAILURES.json`. The required reproduction pipeline is
blocked by those existing checks as previously documented; the focused exact
audits and note build ran explicitly. No unrelated failing files were edited.

The 23-page note builds without unresolved references, citations or overfull
boxes. Pages 19–23 and the revised cover/contents were rendered and visually
inspected. No claim was promoted to the active manuscript or shared results
ledger. Mathematical self-audits and finite exact checks do not constitute
independent proof review.

## Overnight block four

`two_port_frontier.py` passes 8,329 exact reference comparisons on connected
atlas graphs through seven vertices, every seed and four parameter pairs.
It correctly detects 18,791 cases outside the promised support class and
passes nine larger KKT-only checks. The class allows at most one nonseed
positive vertex of degree at least three. The implemented bound is
`O((1+vol(S)) log^4(2+vol(S)))`, with no inactive adjacency scans.
`TWO_PORT_FRONTIER_AUDIT.json` records all parameters, graph access counts,
actual reporter operations, final source hash and hull-backend hash.

`dynamic_upper_hull.py` passes 5,136 exact extreme comparisons and 1,606
independent static-chain comparisons, including strictly concave chains
through 512 points. It handles replacements, deletes, coincident coordinates,
vertical points and nonnegative directions with zero entries. Visits to
both AVL structures, sequence selections, merges and allocations are counted.
Its complete conservative proof is `lem:op3-avl-upper-hull`, not an import of
an unimplemented optimal hull algorithm. See `DYNAMIC_UPPER_HULL_AUDIT.json`.

`schur_relative_reporter_probe.py` verifies three source-valid finite path
witnesses: 909 strict admissions also satisfy the 1.1 approximate-extreme
contract, yet the final allowed quiet return misses an original residual
violation. An independent ordered tridiagonal solve reconstructs 912
positive active coordinates and verifies both tip residuals. The final
violation factors are approximately 1.52, 2.54 and 4.05. An initial
one-arm-first chronology failed its gate test and was discarded; the final
balanced-then-biased trace is checked at every step. This is a scoped oracle
contract refutation, not a lower bound or a failure of original-value
geometric publications. See `SCHUR_RELATIVE_REPORTER_AUDIT.json`.

The ten audit scripts pass focused lint and format checks, and the registry
has three passing tests. Ownership and whitespace checks pass. The latest
broad repository tests have 231 passes and the same three pre-existing
failures; broad lint and note inventory retain only their documented two
unrelated findings each. The previously blocked reproduction pipeline is
unchanged; the new exact audits and note build were run explicitly.

The 27-page note builds with no unresolved references/citations or overfull
boxes. Revised opening pages and pages 22–27 were rendered and visually
inspected, including the final matrix notation and source citation changes.
The two-port theorem, hull proof and all earlier results remain drafts
awaiting independent review. No active-manuscript or shared-ledger promotion
was made. Jacob–Brodal's primary theorem and computational model were
checked for provenance, while Chan's 3D theorem is recorded only as a bounded
next import to audit, not as an implemented extension.


## Overnight block 5

`branch_core_flux.py` implements a growing retained branching core and
scalar physical-flux publication queues. `thm:op3-branch-core-flux` gives
`O(|U|r^2 + rV + VL log(2+V))` exact-real word work, with
`L=1+log_+(1/(bar_alpha eps_appr))`, and `O(V+r^2)` storage. This includes
all failed queue searches and dense inverse changes. It returns the ACL
witness at `lambda=eps_appr/2` and scans precisely positive output rows.
It is a proof draft awaiting independent review; arbitrary-graph OP3 is Open.

- `BRANCH_CORE_FLUX_AUDIT.json`: **27,120** exact returned-face comparisons,
  full-obstacle domination checks and original ACL residual checks through
  seven vertices, every seed and four parameter pairs. Intermediate checks
  through five vertices cover 2,112 faces, 9,717 inverse entries, 4,345
  physical fluxes and 3,253 shared boundary sums. Seventeen additional
  cases cover cyclic subdivisions, shared high-degree inactive reports,
  equality, stars through 4,097 vertices, and all three prior cancellation
  graphs. The final run took 133.946 seconds including reference work.
  Source SHA-256:
  `9b88c8159f6df5694de0250e36fe5cc58a43684a83eb0a3a2bb5871509f1ed2b`.
- `BRANCH_CORE_COST_AUDIT.json`: four full-support balanced trees through
  127 vertices verify cubic explicit inverse writes. The formal statement
  is `prop:op3-dense-core-binary-tree`; the construction does not lower-bound
  other local solvers. Source SHA-256:
  `3d3aeed4f96f26d0b50edcb99314f81cd8390c31a91ba328e616dd150c617fb0`.
  Its imported backend hash matches the preceding solver.
- `LIVE_CORE_PEELING_PROBE.md`: **Open**, candidate current-degree removal
  and grouped physical-flux algebra for the next block. No implementation
  or graph-uniform work bound is claimed.

Focused lint and formatting pass for all twelve audit scripts; the registry
has three passing tests. Ownership and whitespace checks pass. The full
repository tests still have **231 passes and the same three pre-existing
failures** documented above. Note inventory still reports only the same two
oversized AESP sections. The two unrelated broad-lint findings were unchanged
from block 4 and were not re-run without a relevant change.

The final 31-page note builds without overfull boxes or unresolved references.
Opening pages and pages 27–31 were rendered and inspected; the abstract was
shortened to keep the cover clear of the footer. The new proof includes the
separate cost of scanning retained queues: near-linear publication count
is not claimed to make all queue visits near-linear. Source hashes were
checked against the executed audit files. Chan 2019's three-dimensional
source contract is reconciled in the literature topic note; its backend is
not implemented. No active-manuscript promotion or shared-result promotion
was made. The heartbeat remains active until the ten additional active hours
are actually completed; see `OVERNIGHT_WORK_LOG.json`.


## Overnight block 6

`live_core_peeling.py` now removes eligible nonseed vertices according to
current reduced degree, preserves grouped physical-flux publications, and
uses stable original labels for inverse rows and recovery equations.
`thm:op3-live-core-peeling` gives the fully charged bound in maximum live
core q: `O((|U|q^2+qV+VL) log(2+V))` work and `O(V+q^2)` storage.
The algorithm returns the original ACL certificate and scans only positive
output rows. The proof is a draft awaiting independent review.

- `LIVE_CORE_PEELING_AUDIT.json`: **54,240** exact comparisons through
  seven vertices, every seed, four parameter pairs, and FIFO/LIFO policies;
  **50** structured cases cover cyclic subdivisions, grouped parallel paths,
  previous cancellation witnesses, balanced trees and asymmetric combs.
  Audit-only trace checks cover 4,268 faces, 15,476 inverse entries, 6,872
  reduced core equations, 8,497 physical groups and 6,728 shared sums.
  Those membership lists and dense reference solves are excluded from the
  charged algorithm. The final run took 298.323 seconds including reference
  work. Source SHA-256:
  `f041e65baaae76ea7fc345a58cf238b6060076bfbd5c98f27c6573cd52279c52`.
- `prop:op3-live-core-binary-order`: both policies are proved to realize
  their usual search orders at the stated parameters. Completed balanced
  trees have logarithmic maximum core under LIFO but linear core and cubic
  inverse writes under FIFO. Four sizes through 127 vertices verify the
  exact write counts and peak cores; these rows are in the preceding audit.
- `LIVE_CORE_WIDTH_AUDIT.json`: **ten** canonical implicit binary-tree
  cases verify the interior-support obstruction for both policies, through
  2,097,151 ambient vertices. An independent exact radial obstacle reference
  checks every output coordinate; all exposed original residuals are checked.
  No original leaf is reached and no core vertex is removed. Mandatory and
  actual dense inverse writes agree. The proof is
  `prop:op3-live-core-interior-tree`, an implementation-specific obstruction,
  not an OP3 lower bound. The audit took 11.446 seconds. Source SHA-256:
  `706a8ab17d24c8252525f865add1089184bbd03ca4f425ce74cce4b5777c12a4`.
  Its backend hash matches the preceding solver.
- `ROOT_THRESHOLD_ORDER_PROBE.md`: next **Open** exact search, with clear
  separation from the existing rho-homotopy reordering and backbone-first
  caterpillar reporter. No new threshold-order claim is made yet.

Focused lint and formatting pass for all fourteen scripts. Ownership,
registry and whitespace checks pass. Full repository tests retain **231
passes and the same three pre-existing failures**; note inventory reports
only the same two oversized AESP files. The two unrelated broad-lint findings
remain unchanged, and the already blocked reproduction pipeline has not been
represented as passing. Exact audits and the note build ran explicitly.

The final 35-page note builds without overfull boxes or unresolved references.
The revised cover, contents, and pages 30–35 were rendered and visually
inspected. A redundant conclusion paragraph was removed to keep the last
reference from occupying a separate page. Source and backend hashes match
the executed audits. No result was promoted to the active manuscript or
shared ledger. The heartbeat remains ACTIVE until the user-requested ten
additional active hours are actually completed.


## Overnight block 7

`sections/op3_root_threshold_groups.tex` contains the fixed-lambda tree
threshold identities and scoped shortcut counterexamples. The harmonic
change of coordinates gives an exact weighted-tree Green formula, a common
positive affine threshold map for each ancestor group, and exact harmonic,
offset and resistance updates. This is **Proved here**, as a draft awaiting
independent review. It does not supply a dynamic reporter or local work bound.

- `ROOT_THRESHOLD_ORDER_AUDIT.json`: **22,440** actual traces on every
  nonisomorphic tree through nine vertices, every seed, six parameter pairs
  and five policies. It verifies 110,542 strict admissions, 115,237 Schur
  rows, 46,912 same-ancestor factors and 406,131 Green/resistance coordinate
  checks. All final ACL certificates pass; all 13,464 exact-stop outputs
  equal the independent obstacle reference. The reference uses dense solves
  and full frontier scans; all of this is excluded from any algorithmic
  claim. Final execution took 75.798 seconds. Source SHA-256:
  `fd8d1faf461243ef7486af6dadd5c60b1c98b3c78570dc1be5e245e3e11ba51a`.
- `MINIMUM_ROOT_THRESHOLD_AUDIT.json`: **13,179** complete symbolic
  minimum-policy sequences through eleven vertices, every seed and three
  alpha choices, with 122,388 symbolic admissions. Exact parameter intervals
  give 33 strict quiet-order reversals and 39 missed-positive intervals.
  The first witnesses are reconstructed with independent dense face solves,
  including every earlier minimum choice. The simple exact-stop witness
  uses alpha=1/7 and lambda=1/31. No ACL failure was found in this finite
  minimum-policy family; no general robustness claim follows. Final execution
  took 29.649 seconds. Source SHA-256:
  `b371ce25f826416848bee03316386ad6bc9c0408499407226ff1c6de5514c92e`.
- `ROOT_THRESHOLD_WITNESSES_AUDIT.json`: the fifteen-vertex canonical
  tree gives a legal selected prefix with an original ACL miss of ratio
  `194118268149174442122/182466278813571685633 > 1`. It is a different
  policy from the minimum-threshold policy. Each earlier positive gate and
  all current affine coefficients are recorded. Four implicit backbone
  cases through length 32 verify distinct group maps, exact path solutions,
  quiet high-degree reports and all coordinate formulas. Twenty independent
  dense face comparisons cross-check the tridiagonal oracle. The explicit
  map count is quadratic in backbone length, but this family has exponentially
  small epsilon and does not refute an accuracy-logarithmic amortization or
  OP3. Execution took 0.329 seconds. Source SHA-256:
  `a6e4ba8fe6e67ee96c7f507757f20d7a7b755fa6ca7ddcaa9c4eebb7aa551145`.

Both imported reference hashes match the executed files. The initial small
threshold audit exposed its own mismatch between graph iteration order and
label-indexed arrays; explicit label-indexed matrix/load construction fixed
it before the successful final sweep. An auxiliary exact interval search
helped locate the same nine-vertex family; it was not used as a complexity
measurement. Two unused assignments were removed from the symbolic audit,
then its entire final enumeration was rerun. No solver/backend was silently
substituted for the charged algorithms from earlier blocks.

All seventeen scripts pass focused lint and format checks. Registry tests
have three passes, and ownership/whitespace checks pass. Full repository
checks retain **231 passed and the same three pre-existing failures**;
broad lint has the same two unrelated findings, and note inventory has the
same two oversized AESP files. All five affected failing-file hashes remain
byte-identical to the recorded baseline. The previously blocked reproduction
pipeline remains blocked; the new exact audits and note build ran explicitly.

The final **40-page** note builds without overfull boxes or unresolved
references. Contents pages 2–3 and changed pages 34–40 were rendered and
visually inspected. A missing status macro and an overlong theorem-opening
line were corrected before the final successful build. The cover is unchanged.
No claim was promoted to the active manuscript or shared results ledger.

The next **Open** constructive target is fully specified in
`ORDERED_PATH_CLUSTER_PROBE.md`: verify adjacent-path slope separation and
implement a charged persistent projective convex-chain primitive, before
importing any online tree-hierarchy guarantee. General OP3 and local tree
response maintenance remain Open. The heartbeat remains ACTIVE until ten
additional actual active research hours have been completed.


## Overnight block 8

`sections/op3_ordered_path_clusters.tex` proves the finite homogeneous
chart, complete positive projective pullback and adjacent-path interval
separation. The immutable AVL primitive charges whole maps, failed bridge
searches, structural copies, queries and retained versions. Edge, compress,
one/two-port rake, forget and recovery operations use the original diagonal
and load, subtracting one duplicated shared-port copy. These are **Proved
here** drafts awaiting independent review. The online local-tree theorem is
**Conditional**; arbitrary-graph OP3 remains **Open**.

- `PROJECTIVE_HULL_ROPE_AUDIT.json`: 516 independent static-chain checks,
  43,906 retained-point comparisons, 360 extreme queries, 360 one-port
  queries, 96 separated compressions and 130 retained versions. Every tested
  whole map copies exactly one root. Final run 45.204 seconds. Source hash:
  `9efde237937cd5e37f46061d3d2ebeaa474f336e1131c81bc5bb5932a3e91d03`.
- `PATH_CLUSTER_REPORTER_AUDIT.json`: 423 source instances on all trees
  through seven vertices, every seed, three parameter pairs; 1,512 positive
  faces, 18,819 independent full Schur comparisons, 29,278 boundary rows,
  31,590 two-port queries, 8,289 one-port checks, 74,400 recovered coordinates,
  5,265 retained regroupings and 1,040 one-port/one-port rakes. Five implicit
  private-star path cases through 128 positive vertices keep every boundary
  row on the chain and prohibit inactive adjacency scans. Final run 27.484
  seconds. Source hash:
  `37411b1b5bcdd77db21e200522d0636a0ca369691a2d0e936429f234f0a19ab4`.
  Its imported hull hash matches the executed primitive.
- Both audits use exact fractions; their materialized hulls, full-graph
  metadata and dense solves are independent reference work, excluded from
  the proposed backend complexity. The cluster driver rebuilds supplied
  hierarchies and is not an online balancing implementation.
- The top-tree primary source arXiv:cs/0310065v2 was read at Sections 2 and
  6.1–6.2, including Theorem 1 and Figure 1. PDF pages 4, 6 and 25 were
  rendered and visually inspected. Publication metadata were checked against
  the University of Copenhagen author record. The source and application
  obligations are recorded together in the literature index/topic note.
  Link resets external boundaries; source exposure cannot be silently
  assumed throughout a link. The callback reconciliation is the next probe.

All nineteen scripts pass focused lint and formatting. Registry tests have
three passes; ownership and whitespace checks pass. The initial broad test
caught a new reserved seed symbol in this draft, which was corrected before
rerunning the suite. Final tests have **231 passes and the same three
pre-existing failures**. Broad lint has the same two unrelated findings;
note inventory has the same two oversized AESP files. All five failing-file
hashes are unchanged from the recorded baseline. The previously blocked
reproduction pipeline remains blocked; these new exact audits and the note
build ran explicitly.

The final **43-page** note builds without warnings, overfull boxes or
unresolved references. Contents pages 2–3 and pages 38–43 were rendered and
visually inspected. A shorter contents title removes a collision with its
page number; the revised contents page was rendered and checked again.
The cover remains unchanged. No result was promoted to the active manuscript
or shared ledger, and no commit was created. The heartbeat remains ACTIVE;
the ten-hour minimum has not yet been fulfilled.


## Overnight block 9

`sections/op3_local_top_trees.tex` discharges the tree hierarchy condition.
The exact local tree theorem `thm:op3-local-top-tree` is **Proved here** as a
draft awaiting independent review. It imports the published height-bounded
top-tree algorithm, proves the full application callback contract, and
charges graph discovery, local heaps, home-edge payloads, every failed query,
all persistent copies, optional active-capacity doubling and final recovery.
Its O(cvol(U) log^4(2+cvol(U))) exact-real word work gives
O_tilde(1/eps_appr) ACL work and exact O_tilde(1/rho) RPPR work on trees.
It does not establish finite-precision stability or arbitrary-graph OP3.

- `TOP_TREE_CALLBACK_AUDIT.json`: 650 canonical positive tree faces, every
  core tree through eight vertices, every seed and two alpha choices.
  All 167,384 legal binary joins are checked under exposed and unexposed
  seed boundaries, covering all five source join shapes. The audit has
  26,130 independent Schur oracles, 168,294 valid summary comparisons,
  104,794 owned rows, 270,792 two-port queries, 78,030 one-port checks,
  833,718 recovered coordinates, 650 exposure transitions and 1,296
  intermediate payload refreshes. Old roots are rechecked after changes.
  Execution took 240.431 seconds. Source SHA-256:
  `9aa5fb5e7ecc557d5147248db0d53c5cbaf05bedc350f6fc366ddcbae0d750e8`.
- `sections/op3_shifted_tree_clusters.tex` proves that C=1/bar_alpha and
  w=u-C make every cluster load negative, using fixed base vertex loads
  plus gamma*C per edge endpoint. The geometric anchor may differ from the
  physical seed. Arbitrary reporter intercepts remain correct; normalized
  hulls are simply translated vertically. It proves the exact shifted
  two-port correction for one extra edge, including the required load term.
- `SHIFTED_TREE_CLUSTER_AUDIT.json`: 564 positive core faces through seven
  vertices, every physical seed, two anchors and two alpha choices; 33,550
  conditional shift identities, 9,496 independent Schur oracles, 28,606
  valid summary comparisons, 1,972 clusters with physical seed interior,
  14,012 positive-intercept rows and 564 exposure transitions. The triangle
  and off-cycle-source witnesses match independent full solves. The triangle
  has a negative uncorrected spanning-tree coordinate despite a legal
  positive full-cycle admission; using a tree obstacle solution would be
  incorrect. Final execution took 27.212 seconds. Source SHA-256:
  `82a0e2d37499a2455479bab1327e1654f860c5980d68db77361300a138702cad`.
  All imported backend hashes match the executed files.

These are exact algebra and callback audits. Their exhaustive hierarchy
construction, cluster metadata and dense reference solves are paid reference
work, not the source's online balancing implementation. Payload-only changes
are marked as intermediate algebraic tests rather than graph admissions.
The asymptotic theorem depends on the checked published source algorithm;
it is not inferred from finite runtimes. Temporary query matrices are charged
to work and are not counted as permanently retained hull nodes.

The published journal PDF of Alstrup et al. was checked in addition to the
older arXiv version: Theorem 2.1, journal p. 247; definitions and application
pointers pp. 245–248; exposure and arbitrary degrees pp. 259–260. Pages 247
and 260 were rendered and visually inspected. The journal removes the old
zero-argument expose option; this application uses one or two vertices only.
The final proof imports the published height guarantee, not the unbounded-
height amortized variant. The literature index and topic were updated together.

All twenty-one scripts pass focused lint and formatting. Registry tests
have three passes and ownership/whitespace checks pass. Full tests retain
**231 passed and the same three pre-existing failures**; broad lint has the
same two unrelated findings and note inventory the same two oversized files.
All five failing-file hashes match the baseline. The previously blocked
reproduction pipeline remains blocked; new exact audits and builds ran
explicitly.

The final **49-page** note builds without warnings, overfull boxes or
unresolved references. The revised cover, contents and pages 42–49 were
rendered and visually inspected. Short contents titles avoid page-number
collisions; capacity and published-source changes were re-rendered. No
active-manuscript or shared-ledger promotion and no commit were made.
The next **Open** target, including the point-query contract and signed
spanning-tree pitfall, is `UNICYCLE_TOP_TREE_PROBE.md`. The heartbeat remains
ACTIVE until the ten-hour minimum is actually reached.

## Overnight block 10: complete local unicyclic construction

**Proved here, awaiting independent review:** `lem:op3-cluster-point-query`,
`lem:op3-unicyclic-exception` and `thm:op3-local-unicyclic` in
`sections/op3_local_unicyclic.tex`. The result charges original graph access,
all heap/payload work, unsuccessful exceptional checks, one cycle re-rooting,
source callbacks, retained application versions and final output. It imports
the published height-bounded online top-tree algorithm explicitly. The audit
rebuilds reference hierarchies; it is not an implementation of that online
balancing algorithm. General OP3 remains Open.

- `cluster_point_queries.py --max-n 6`: **passed**, 13.370 seconds;
  256 canonical faces, 58,816 named-coordinate comparisons and 168,468 affine
  pullbacks. Tests include arbitrary port assignments, one-port base edges,
  compress/rake/forget helpers, old roots and intermediate payload versions.
  `CLUSTER_POINT_QUERY_AUDIT.json` records source SHA-256
  `e18411100027224ad2de26ad98d7c1fac425f1f4d3e045a74283c06a47d806fc`.
- `local_unicyclic_clusters.py --max-n 7 --structured`: **passed**, 22.605
  seconds; 3,888 executions on all 78 connected tree/unicyclic atlas graphs
  through seven vertices, every seed, four parameter pairs and two policies;
  sixteen larger explicit attachment executions and four implicit private
  star examples. Independent references check 16,371 faces and 26,043
  original gates, including 319 negative uncorrected spanning-tree faces.
  `LOCAL_UNICYCLIC_CLUSTER_AUDIT.json` records source SHA-256
  `ec488382ed145eeecd4dd39e900fb5eb3fb48f3c697598fd36b63afe904080ad`.
- Atlas state-machine counts: 1,502 cycle closures, 1,674 subsequent leaf
  admissions, 2,078 exceptional checks (136 quiet), and 4,156 named queries.
  The full driver records all graph operations and separates rebuilt
  hierarchy work, dense validation and retained-root checks.
- Four finite private-star graphs have active core sizes 9/17/15/16, using
  only 27/51/45/48 original adjacency entries and 18/34/30/32 degree replies.
  No inactive hub row is scanned. Their full finite ambient sizes and exact
  parameters are recorded; they are not materialized for algorithm access.
- Both source hashes and every backend dependency hash: **matched**.
- Focused Python lint and formatting: **all 23 scripts passed**.
- Proof audit registry: **3 passed**. Ownership and whitespace: **passed**.
- Repository tests: **231 passed, same three pre-existing failures**.
  Broad lint has the same two unrelated findings, and note inventory has
  the same two oversized AESP files. All five baseline hashes are unchanged.
- Note build: **52 pages**, no warnings, overfull boxes or unresolved
  references. Revised cover, contents and pages 47–52 rendered and inspected.
  PDF SHA-256:
  `5f990bbc8f60e83c108a570627201a46d761ca72d5116a215a1ad648bb419231`.

`BOUNDED_CYCLE_RANK_PROBE.md` is the next Open construction: a permanently
rooted active spanning tree, O(q) two-port components, a coupled coarse solve,
and fully charged repartitioning. No bounded-cycle-rank algorithm or theorem
has yet been asserted. Usage reads 7% consumed / 93% remaining; the same-task
heartbeat remains active, and no further reset was attempted.

## Overnight block 11: local cycle-rank theorem and selected Green queries

**Proved here, awaiting independent review:** `thm:op3-local-cycle-rank`
gives work O(1+V*((1+r)*L^4+(1+r)^3+q*L^2)), separating active cycle rank r
from revealed cycle rank q. It explicitly charges piece partitioning,
shared-port duplication, original graph accesses, every exceptional gate,
coarse matrices and solves, source callbacks, histories and final output.
The online balancing algorithm is imported, while per-checkpoint hierarchy
reconstruction and dense reference validation are labelled audit work.
General OP3 remains Open. The final text distinguishes OP3's ACL 1/eps_appr
scale from the separate OP2 accelerated RPPR product scale.

- `local_cycle_rank_clusters.py --max-n 7 --structured`: **passed**,
  353.838 seconds including references.
  It covers 54,240 executions on all 995 connected atlas graphs through seven
  vertices, every seed, four parameter pairs and two policies, plus twenty
  larger explicit cases and five finite implicit private-star cases.
- Independent checks: 217,410 positive faces, 168,368 complete coarse Schur
  matrices and shifted loads, 483,413 original gates, 729,558 unique edge/row
  home checks and 198,001 retained component root rechecks.
- Atlas traces include 33,074 multi-cycle births, up to six active parents
  in an admission, up to five simultaneous exceptional candidates, and
  166,405 exceptional gate queries (3,441 quiet). Every graph row is scanned
  exactly once after positive admission. The five implicit cases inspect
  58/51/48/62/70 original entries, with no inactive hub row scan.
- Rank audit source SHA-256: `0a2b5745bbaee48d9fa027e84760da7d39889e3cc1be65e91dc639f98fb39297`.

**Proved here / Measured:** `lem:op3-cluster-conditional-green` and
`lem:op3-green-promotion-border` give selected conditional Green queries,
port-promotion identities and a positive original-vertex border pivot.
The full maintained inverse algorithm and its proposed r^2 bound remain
**Open**, with a precise transaction in `COARSE_INVERSE_UPDATE_PROBE.md`.

- `cluster_green_queries.py --max-n 6`: **passed**, final run
  22.361 seconds. There are 256 canonical
  faces, 2,664 independent conditional inverse matrices, 29,408 affine and
  variance comparisons, and 123,844 covariance pairs.
- The compact variance path stores no trace; covariance queries explicitly
  require retained traces. Both modes are checked. Old payload versions,
  shifted source-interior clusters and every helper shape are included.
- Green audit source SHA-256: `54d77cf4a72adf08be9e13eee84c5b03991c08e433c0a0be55f0fac01e61d20d`.
- Both source hashes and all backend dependency hashes: **matched**.
- Focused lint/format: **25 scripts passed**; the final trace-contract change
  also passed its full exact audit and focused checks. Registry: **3 passed**.
- Ownership and whitespace: **passed**. Broad tests: **231 passed**, the same
  three pre-existing failures. Broad lint and note inventory retain the same
  unrelated findings. All five baseline failure-file hashes remain unchanged.
- Note: **58 pages**, no warnings, overfull boxes or unresolved references.
  Revised cover/contents and pages51–58 rendered and inspected, including
  re-rendered namespace wording and temporary-port refinement.
  Final PDF SHA-256: `24651194362bd2dcc29e5ceb704fa23ca8c0978da70ebe1fe844c4a580400778`.

The active-time ledger conservatively excludes 94.352504 minutes from
23:16:43.813547 UTC to00:51:04.963783 UTC, a long unverified gap spanning
resumed verification outputs. Even brief checks within that span are not
counted. Only substantive intervals outside it count toward the 600-minute
minimum. Temporary idle-sleep prevention was extended for the remaining
research, and the existing same-task heartbeat stays ACTIVE. Usage is
8% consumed / 92% remaining; no additional reset was attempted.
