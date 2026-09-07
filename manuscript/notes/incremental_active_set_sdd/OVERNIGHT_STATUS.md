# OP3 overnight research

Last updated: 7 September 2026. Repository:
`/Users/baojian/git/hybrid-local-solver`, branch `main`.

## Current state

Completed **601.407 additional active research minutes** across fourteen
blocks, exceeding the requested ten-hour minimum. The work ledger is
`OVERNIGHT_WORK_LOG.json`. Idle and unverified gaps, including the recorded
94.352504-minute gap, and the earlier exploration are excluded.
The same-task heartbeat `op3-overnight-research` is **PAUSED**. Further
research awaits the user's choice. The user-authorized commit and push are
being finalized; Git history is the authority for their completion.

Read [OP3_MORNING_DECISIONS_20260907.md](OP3_MORNING_DECISIONS_20260907.md)
for the consolidated result and proposed decisions. General OP3 remains
**Open**. Positive results are **Proved here** as drafts awaiting independent
review, with source imports and reference substitutions identified. No
unreviewed theorem has been promoted into the active manuscript or shared
results ledger.

## Completed results and exact evidence

The local tree and unicyclic constructions give exact obstacle work
`O(1+cvol(U)*log^4(2+cvol(U)))`. Their application callbacks are implemented;
the published online top-tree balancing interface is an explicit **Source**
import. Earlier blocks and their witnesses remain in the completed-interval
ledger, `VERIFICATION.md`, and the individually named block/audit records.
The first block's direct artifacts are listed in the ledger.

Geometric lower-value publication removes repeated shared-candidate scans
and the revealed-rank factor. The subsequent certified sparse coarse
construction gives expected ACL work
`E[W]=O_tilde((1+E[r])/eps_appr)`, or `O_tilde((1+R)/eps_appr)` for a fixed
containing obstacle-support cycle-rank bound R. The fast supplied sparse
SDD solver is a second explicit **Source** import. This algorithm may stop
before the obstacle optimum and has no exact RPPR or OP2 conclusion.

A separate fully implemented scalar sweep solves a promised clique core
with arbitrary unequal private leaves and a core seed. Its exact-obstacle
work is `O(1+cvol(U)*log(2+cvol(U)))`, with linear storage. Choosing
`lambda=eps_appr/2` gives ACL accuracy; separately choosing `lambda=rho`
gives exact RPPR on that family. The graph promise is assumed, not verified
on unread rows. The arithmetic model is exact-real words, not bit complexity
or numerical stability. Original degrees and all graph accesses are charged.

Final-block evidence:

- `CERTIFIED_COARSE_PUBLICATION_AUDIT.json`: 67,856 complete original ACL
  checks, 223,514 independent faces and 3,228,290 error/due-row checks.
- `COARSE_RESIDUAL_EPOCH_AUDIT.json`: 4,866 complete ACL checks, 26 accepted
  reuse events, and six canonical clique-leaf forced-refresh families.
- `COARSE_GEOMETRIC_SUPERSOLUTION_AUDIT.json`: 16,446 independent Schur
  systems, including an exact triangle obstruction and the equality boundary.
- `LOCAL_CLIQUE_PENDANT_AUDIT.json`: 1,464 explicit exact obstacle comparisons
  and six implicit original-equation certificates. The largest ambient graph
  has `10^18+11` vertices; only six positive rows and 24 incidences are read.
- `MULTIPARTITE_SCALAR_AUDIT.json`: 261 original obstacle comparisons,
  704 supplied scalar fixed points and 182 positive part insertions.
  This is supplied-part algebra, not an end-to-end local solver.

## Refuted routes and next target

The absolute-budget residual-epoch policy can require a complete k-port
refresh at each of k^2 leaf admissions on a legal graph with quadratic
inverse-accuracy and support-volume scales. The resulting cubic writes
refute that specific shortcut. The scalar clique solver handles the same
family efficiently, so this is not an OP3 lower bound.

A true geometric coordinate envelope can fail the sufficient coarse
supersolution test; the exact triangle witness is in the proof and audit.
Adaptive or coupled certificates remain open.

The next bounded target is `MULTIPARTITE_CORE_PROBE.md`: implement local
positive-row startup, paid part discovery, and one incremental scalar-event
heap. Its algebra and monotonicity are audited, but the complete local
mechanism is **Conditional / Open**. The final probe also records explicitly
unaudited canonical-core and leaf-seed reductions. Establish the narrower
local theorem first. General OP3 still needs to avoid repeated whole-port
writes, all-component searches and cycle-triggered reconstruction.

## Verification and authorization

`OVERNIGHT_BLOCK14_AUDIT.json` and the final section of `VERIFICATION.md`
record source/backend hashes and checks. All 33 focused scripts pass lint
and formatting; registry tests give three passes. Ownership and whitespace
checks pass. The 74-page note builds without warnings, overfull boxes or
undefined references, and final proof pages were rendered and inspected.

Required `make reproduce` stops at the same three pre-existing test failures
with 231 passes; later pipeline stages are not claimed as run. Broad lint
retains two unrelated findings, and note inventory retains two unrelated
oversized AESP sources. All five baseline failure-file hashes are unchanged.

The user authorized committing and pushing all research updates; do not
force-push. Earlier completed commits include `a311768` and `381c0d5`.
Preserve unrelated changes and synced read-only project sources. No subagents,
other-task messages, new tasks or active-manuscript promotion were requested.
The account reset previously requested was redeemed successfully. No reset
credits remain; no further reset was attempted. Temporary keep-awake process
ownership is recorded in `OVERNIGHT_RUNTIME.json`; stop only matching owned
processes when finishing this continuation.
