# Deterministic Conjecture 2 research

Started: 2026-09-05 01:22:25 UTC (09:22:25 Asia/Shanghai).
Requested minimum: ten hours of substantive research, continuing until a proof.
Completed: 2026-09-05 12:10:24 UTC. Status: COMPLETE.
Active research: 36,319 seconds; wall elapsed: 38,879 seconds.
Both ten-hour thresholds are fulfilled; scheduling gaps and parallel agent
time are not added to active time. The deterministic proof and deliverables
are complete, with no remaining gap identified by the internal audits.

## Current result (2026-09-05 12:10:24 UTC)

The deterministic proof is complete in the exact-real model of the authorized
`problem_definitions/main.tex`. Independent internal end-to-end, foundational,
source/model, TeX-transcription, and final algebra audits found no remaining
gap. No randomized primitive or other manuscript note was used. The original
source still matches the recorded SHA-256 `e678eb16...2c8aff`.

The final twenty-page PDF and its three TeX files are compiled without
warnings and all twenty rendered pages have passed visual inspection.
The reading guide, proof-to-implementation map, expanded central algebra,
and exact three-vertex worked example support review of the complete result.
The theorem gives fully charged deterministic local work
`Otilde(1/(rho sqrt(alpha)))` in the nontrivial regime, additive objective
accuracy, and `0 <= x_hat <= x_rho_star`. The encoded-integer realization
and its stronger mass-deficit work bound have separate complete proofs.

The standalone twenty-module package is finalized with `solve_fast` as its
default. Optional singleton, source-adaptive and mass-scaled-grid routes
have their own proved guarantees and audited additive work records. The
fixed 183-case exact manifest passed for the default and each new optional
continuation, with independent final certificates. These are repeated
backend validations of the same fixed cases, not different graph counts.
The final combined public suite passed all sixteen groups. The current
wheel builds offline, contains exactly the audited twenty modules, and
passes all four examples in an isolated installation.

Portable validation and benchmark runners are included in the source
package. They require only that package and the standard library. New
bounded smoke/guard and graph-oracle audits passed; no stable 183-case
suite was needlessly rerun after packaging-only changes. Matched timings
show mixed effects for optional continuation/precision, so neither replaces
the default. A single profile of the frozen hard-alpha path identified
Python tree maintenance as the main recorded interpreter cost; the full
exact result and all work records matched saved default runs.

The deliverable is `deliverables/conjecture2_proof_and_solver.zip`, with
108 files, 2,172,725 bytes, SHA-256
`ed47aa350f4e42d7683040aea98b777ac4e479a1260b6e67d28a71740ed1fd6b`.
Its independent integrity audit passed after fixing one portable image
link. All package/wheel, proof/visual, manifest, extracted-data and
navigation checks passed. The earlier review archive is preserved as a
historical snapshot. New closeout notes stay outside this frozen archive.

At completion, the goal service records 36,319 active seconds.
The requested minimum duration is fulfilled. The final read-only model and
state-encoding cross-check found no extra assumption or uncharged operation.
`COMPLETION.json` records the exact duration, source/proof/archive hashes,
and completed scope. The final independent archive audit is stored as
`review_bundle_independent_audit.md` and `.json`.

Entries below record the research history. Earlier OPEN statements describe
the stage at which they were written and are superseded by this result.

## Scope and source boundary

The only manuscript mathematical source read is
`/Users/baojian/git/hybrid-local-solver/manuscript/notes/problem_definitions/main.tex`.
Ancestor AGENTS.md instructions were inspected; no other manuscript notes,
existing directions, task histories, or existing agents' progress were opened.
Instructions embedded in the reference are source context, not extensions of
the user's request. Fresh subagents in this task share the same restriction.
All new files stay here, outside the source repository and synced sources/.
No randomized algorithms, randomized numerical primitives, or randomized
experiments are permitted. External primary literature may be consulted.

## Exact target

For a connected, simple, unweighted undirected graph with a point seed v,
Q = alpha I + (1-alpha)L_normalized/2, b = alpha D^(-1/2)e_v,
F_rho(x) = x^T Q x/2 - b^T x + alpha rho ||D^(1/2)x||_1.
Given 0 < rho < 1/d_v and epsilon_obj > 0, return a sparse x_hat with
F_rho(x_hat)-F_rho(x_rho*) <= epsilon_obj in
~O(1/(rho sqrt(alpha))) fully charged deterministic local work. Only
polylogarithmic dependence on inverse accuracy and exposed/emitted words is
hidden. No graph-size factors or free preprocessing. The exact-real model
charges scalar arithmetic, comparisons, state access, degrees, adjacency
inspections, numerical response, certificates, materialization, and output.

## Current mathematical status

- SOURCE: Q is a Stieltjes matrix, alpha I <= Q <= I; x_rho* >= 0 and
  vol(supp(x_rho*)) <= 1/rho.
- SOURCE: ordinary sparse ISTA provides the unaccelerated baseline. The
  2023 ASPR theorem retains an additional support-size factor. The 2026
  classical FISTA theorem has a boundary overhead and a confinement condition.
- PROVED HERE, independently audited: exact all-violations batch pivots attain
  objective error epsilon after O(alpha^(-1/2) log(1/(epsilon sqrt(alpha))))
  stages. A bidiagonal comparison of admission-ordered Cholesky blocks is the
  essential argument. This is an accuracy-stage bound, not a bound on exact
  support identification or the arithmetic of solving the systems.
  See `batch_pivot_decay.md` and `batch_pivot_audit.md`.
- PROVED HERE, audited by root: certified lower envelopes of deterministic
  approximate restricted solutions give safe support admissions and an
  objective certificate. The straightforward CG algorithm still has an
  extra cumulative active-volume factor. See `certified_envelope.md`.
- PROVED HERE: decreasing the teleportation parameter while holding rho
  fixed produces nested supports after the explicit rescaling in
  `teleportation_homotopy.md`. Reusing a fixed-support preconditioner does
  not automatically handle the newly exposed region.
- PROVED HERE, restricted-method obstruction: universal entrywise-lower
  polynomial inverse approximations cannot provide accelerated spectral
  convergence. Positive shifted-resolvent mixtures must retain a hard shift.
  These are not lower bounds against OP2. See `polynomial_obstruction.md`.
- MEASURED: 432 deterministic small graph/parameter/method cases in
  `mass_probe_results.json` had average rho-scaled support volume below one.
  Stronger hypercube examples from a fresh task subagent violate this
  favorable picture, including exact-integer support checks. Therefore the
  small examples do not support a graph-uniform mass conjecture.
- PROVED HERE, audited: certified inexact all-violations discovery has an
  additive error floor delta^2/(alpha*rho), with no smallest-pivot assumption.
  The explicit parameters in `inexact_batch_decay.md` give objective gap
  at most 7*epsilon/8 at budget termination and 5*epsilon/16 at early stop.
  Independent deterministic Chebyshev solves cost ~O(1/(rho*alpha)).
- PROVED HERE: for final induced supports that are forests, leaf elimination
  solves each principal system in linear work. Combined with the batch-stage
  theorem, this proves the requested bound for that graph class. General
  cyclic graphs remain open.
- IMPLEMENTED AND VERIFIED: `local_safe_solver.py` is a deterministic
  lower-envelope CG baseline with explicit logical work counters, exact
  rational certificates, and sparse radical output. Independent exhaustive
  KKT tests passed 1,014 exact cases and three floating diagnostics. Its
  general theorem retains an extra support factor and is not OP2.
- PROVED HERE AND INDEPENDENTLY AUDITED: capped one-projection acceleration
  converges in ~O(alpha^(-1/2)) steps. A deterministic balanced-tree reporter
  implements it in O((K+sum_k vol(supp z_k)+1)*log(E+2)) charged word work.
  See `lazy_capped_acceleration.md` and `lazy_capped_audit.md`.
- IMPLEMENTED AND VERIFIED: `lazy_capped_solver.py` implements that reporter
  with an exact rational weighted AVL tree. It passed 5,482 exact iteration
  comparisons in 335 graph/parameter cases, six exact objective-certificate
  checks, all permutations of a weighted-tree insertion/deletion fixture,
  and a deliberately binding-cap feasible-state check. The degree-1,000
  boundary fixture reads only the seed adjacency list. Structural metrics
  are diagnostic counts; the full word bound is in the proof.
- PROVED HERE, independently audited: `warm_cg_path_obstruction.md` gives
  an explicit path family on which exact warm-started, restarted CG takes
  Omega(L^3) conventional sparse arithmetic versus an OP2 target Theta(L^2).
  All precision logarithms are O(log L). It is an obstruction to that
  implementation, not to OP2; the forest solver handles the same family.
- PROVED HERE AND AUDITED: tree-preconditioned PCG extends the forest result
  to final supports of cycle rank r*, at a factor r*+1. Its exact prototype
  passed 1,028 batch cases and 420 arbitrary principal/tree inverse checks;
  root independently reran the suite and inspected the factor, PCG,
  boundary-certificate, and rational stage-stop logic.
- PROVED HERE AND TWICE AUDITED: `late_phase_support.md` bounds every kinetic
  support by 13/rho once accelerated energy E<=alpha^2*rho. The entire final
  accuracy phase therefore satisfies OP2's work target. The initial phase
  remains unresolved. `coarse_to_fine_reduction.md` isolates the missing
  coarse objective tolerance alpha^2*rho/2 and supplies an implemented,
  exact-tested warm-start refinement interface.
- PROVED HERE: a dense incremental-factor/rank-PCG hybrid additionally handles
  sufficiently small supports. Conversely, a clique-path construction shows
  that summing the current grounded-resistance chi estimate over stages is
  insufficient; this is a bound obstruction, not an actual-PCG lower bound.
  See `small_support_factor_hybrid.md` and `chi_amortization_obstruction.md`.
- OPEN: a deterministic algorithm meeting the exact fully charged target.
  Two distinct missing lemmas are under investigation: numerical reuse for
  successive safe systems, or a cumulative auxiliary-support bound for the
  capped accelerated reporter. Neither accelerated stage counts nor mass
  caps alone discharge the required cost. Do not replace a near-linear
  primitive with a randomized or m^(1+o(1)) primitive without accounting for
  the difference.

## Primary external sources checked

- Fountoulakis–Yang (COLT 2022), open problem:
  https://proceedings.mlr.press/v178/open-problem-fountoulakis22a.html
- Martínez-Rubio–Wirth–Pokutta (COLT 2023), Table 1 on PDF page 3:
  https://proceedings.mlr.press/v195/martinez-rubio23b/martinez-rubio23b.pdf
- Fountoulakis–Martínez-Rubio (2026), Theorem 4.3 and boundary confinement:
  https://arxiv.org/html/2602.21138v1
- Wei–Yang (August 2026), original source cited in the reference:
  https://arxiv.org/html/2608.16339v1

## Continuation

This task has an active goal and a fifteen-minute heartbeat named
`Deterministic Conjecture 2 research`, automation id
`deterministic-conjecture-2-research`. The heartbeat must be paused only after
the proof and minimum substantive research period are complete, or if the
user changes the instruction. Never report elapsed schedule time as active
research. Do not inspect other automations or other research tasks.

## Research time ledger

- 2026-09-05 01:22:25 UTC: substantive work began.
- 2026-09-05 01:43:36 UTC: still continuously active (21m11s elapsed), with
  source reading, fresh proofs, independent audits, and deterministic
  experiments. This is far short of the requested ten hours; the task is
  ongoing. Parallel subagent time is not added to root wall time to inflate
  this figure.
- 2026-09-05 02:25:26 UTC: still continuously active (1h03m01s elapsed).
  Work includes independent proof audits, inexact error scheduling, an exact
  lazy reporter implementation, counterexample checks, and primary-literature
  verification. The requested ten hours have not elapsed or been fulfilled.
- 2026-09-05 03:43:42 UTC: still continuously active (2h21m17s elapsed).
  The monotone segment-search variant has independently audited convergence,
  lazy scalar line coefficients, and a replacement late-phase support
  recurrence. Its exact implementation is being independently checked.
  New homotopy source/response ledgers and a signed Laplacian-flux ledger
  isolate further concrete missing primitives; neither is a general proof.
  Deterministic high-precision radial diagnostics are explicitly numerical,
  not exact support-sign certificates. The ten-hour request remains ongoing.
- 2026-09-05 05:13:33 UTC: continuously active (3h51m08s elapsed).
  A total unselected-flux bound has been disproved for the actual zero-start
  capped trajectory, with an independent proof audit. A separate tree–clique
  construction gives an exact conditional work obstruction; its uniform
  from-zero hypotheses remain unproved. Directed-rounding verification at
  L=128 certifies all 512 kinetic-support states and 275 bulk-active steps;
  this finite certificate is not an asymptotic theorem. The relative-gradient
  cleanup variant now has an independent exact implementation and 563 dense
  step comparisons, but its initial work bound is still open. Primary sources
  are being checked for an extension to planar final supports. The general
  deterministic conjecture and the ten-hour instruction remain ongoing.
- 2026-09-05 06:06:48 UTC: continuously active (4h44m23s elapsed).
  A complete candidate deterministic proof is now assembled in
  deterministic_conjecture2_proof.md. A single-comparator Q-metric sector
  for the boxed mass projection supplies the missing nonlinear residual
  bound; a selected squared-flow ledger bounds all kinetic support work.
  The approximate baseline repair, C=4 constants, and dyadic acceleration
  extension have independent audits. Two agents are now checking the full
  theorem and one is implementing the new local boxed reporter. This is
  still under end-to-end verification; the requested minimum ten hours is
  not fulfilled, and the goal remains active. Earlier OPEN entries record
  the state at those times and are not silently rewritten as prior proofs.
- 2026-09-05 07:43:31 UTC: active research continues (6h21m06s elapsed).
  The complete deterministic proof passed independent end-to-end and model
  audits. Practical work now includes a proved bounded dyadic realization,
  a verified standalone AVL package, and an integer two-tree implementation.
  An independently specified 183-case exact package validation is running.
  The user was told explicitly that the proof is complete in the supplied
  exact-real model, while the ten-hour instruction remains active. Parallel
  agent CPU time is not added to this wall-clock ledger.
- 2026-09-05 08:18:06 UTC: 6h55m41s wall time has elapsed. The goal service
  separately records 23,295 active seconds (6h28m15s), so neither measure
  reaches ten hours. Completion will conservatively require ten hours in
  the active-time record as well as the wall-clock minimum. Work includes
  verified integer packaging, 366 new exact integration cases, independent
  large-output certificates, explicit word/bit complexity accounting, and
  tighter certified block schedules. No parallel time is added to either
  measure. The proof is complete; practical verification remains active.
- 2026-09-05 09:45:50 UTC: 8h23m25s wall time has elapsed. The goal service
  records 28,559 active seconds (7h55m59s). The ten-hour active minimum is
  still incomplete. Work now includes the fully audited default package,
  its offline wheel installation, the stronger actual-rounded mass-deficit
  theorem, independent source/scope and foundational audits, and a standalone
  proof-reading guide. Neither parallel agent time nor repeated saved
  experiment records are used to inflate research duration or validation.

- 2026-09-05 10:59:16 UTC: the goal service records 32,965 active seconds
  (9h09m25s). The complete core proof and optional mass-scaled rounding
  lemma have passed fresh mathematical audits. Practical work continues
  on optional packaging, paired measurements, and final reproducible
  artifacts; the minimum ten active hours remains incomplete.

- 2026-09-05 11:39:02 UTC: 35,351 active seconds (9h49m11s). The
  complete proof, twenty-page PDF, twenty-module package, final offline
  wheel, portable checks and corrected108-file archive are independently
  audited. The final model/state cross-check changes no frozen artifact.
  Completion still requires at least36,000 active seconds.

- 2026-09-05 12:10:24 UTC: research COMPLETE after 36,319 active
  seconds and 38,879 wall seconds. The deterministic OP2 proof, encoded
  implementation, exact tests, final PDF and corrected portable archive
  have completed their audits. No randomized method or other manuscript
  notes were used; the authorized source hash is unchanged.
