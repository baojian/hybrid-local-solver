# OP3 third campaign: ten additional active hours

The user asked to check whether existing lower bounds support the tightness
of Conjecture 3 and, if so, to continue for ten more hours. The active-time
minimum is **600 NEW minutes**, excluding both completed campaigns and any
idle, scheduling or unverified gaps. Use `OVERNIGHT_20260908_WORK_LOG.json`.

## Initial verdict and current work

**Source:** Wei, Wen and Yang, ICDT 2024, arXiv:2401.01019v1, PDF pp.2–3,
fix the nonlazy teleportation probability and record a degree-normalized
sparse-output lower-bound scale. Their hidden constant-alpha convention
must not be imported as an alpha-uniform upper bound. The star output
argument in the problem-definition note supports Omega(1/eps_appr) for
our stronger original ACL certificate. Recheck its exact constants and
representation before recording a note-local theorem.

**Open:** General OP3 and removal of polynomial inverse-alpha dependence.
A matching accuracy lower bound shows optimality if the conjectured upper
bound is achieved; it does not establish that upper bound.

Read next: `LOWER_BOUND_LITERATURE_AUDIT_20260908.md` (completed initial
audit) and `WEIGHTED_PIECE_CONSTRUCTOR_PROBE_20260908.md` (next proof target).
The exact lower-bound audit passes; it also refutes an instancewise
mass-over-error interpretation while preserving existential worst-case
optimality. New propositions are in `sec:op3-lower-bound-quantifiers`.
Primary PDFs in /tmp: op3-lower-wwy24 (ICDT degree-normalized error),
op3-lower-bj26 (undirected thresholded relative estimation),
op3-lower-jllx26 (PODS 2026 v5, formerly Tighter Lower Bounds), and
op3-lower-wwwy24 (STOC 2024 contributor/centrality queries).

Work directly on main under the continuing commit/push authorization.
No subagents, new tasks or further usage resets. Preserve existing proved
drafts and expensive audit results. Own note and audit scripts remain in
incremental_active_set_sdd; literature metadata and registry may be updated
as needed. Formal note dependencies now include `problem_definitions`
for the explicitly imported star formula/output argument in Proposition 5
of its proof-attempt supplement. Do not promote results into the active
manuscript.

At 600 actual active minutes, save a candid synthesis, commit and push,
pause the same-task heartbeat, and stop only the matching owned process in
`OVERNIGHT_20260908_RUNTIME.json`. Do not pad time with sleeps or repeated
unchanged tests. Existing repository-wide baseline failures remain recorded
in `BASELINE_CHECK_FAILURES.json`.
