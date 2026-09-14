# Deterministic Conjecture 2 research

Started: 2026-09-05 01:41:57 UTC (09:41:57 Asia/Shanghai).
Minimum requested research window ends: 2026-09-05 11:41:57 UTC.
Status: **A deterministic OP2 proof has passed this task's independent
mathematical and local-work audit. At least ten hours of accumulated work
and the requested wall-clock minimum have been completed.** The report is
`deliverables/deterministic_op2_audit.tex`; the portable implementation is
in `deliverables/deterministic-op2-solver/`.

The core continuation proof was developed by the parallel project task
**Prove conjecture 2 deterministically**. This task independently reviewed
that proof and added degree pruning, a boundary-forest component solver,
full-problem projected-gradient checkpoints, a bounded region pilot, an
integer component transcription, and ordinary rational output. Those
refinements remain private to this task. This is not a machine-checked
formal verification or a claim of external peer review.

The user requests at least ten hours of work and continued investigation until
Conjecture 2 is proved, with no randomized algorithms and with practical,
efficient implementation in view. Elapsed time is recorded separately from
active reasoning and computations; neither waiting nor a scheduled run is
reported as completed research time.

The authoritative target is OP2 in
`/Users/baojian/git/hybrid-local-solver/manuscript/notes/problem_definitions/main.tex`:
on a finite simple connected unit graph, one source vertex, and
`0 < rho < 1/d_v`, produce an RPPR objective gap at most `eps_obj` in fully
charged `O_tilde(1/(rho sqrt(alpha)))` work. Polylogarithmic factors are allowed;
a general `M^o(1)` factor is not a polylogarithm. The exact-real algebraic word
model does not itself impose a coefficient-bit theorem.

This working directory is separate from the shared repository and synced
project references. The repository is read-only during this investigation.
No other agent receives our current directions or intermediate results.

Initial repository snapshot: `e83d996e7e61534ba5f3724ea3df3e25778a7ba9`.

## Initial verified boundary

- The threshold-batch block-Cholesky argument is deterministic. Its full
  argument in `active_edge_lcp/sections/body/note_part1.tex` was read and checked
  for sign, inverse ordering, block-bandwidth, and threshold-forcing accounting.
- The fast end-to-end implementation in `note_part2.tex` uses randomized
  nearly-linear supplied-face SDD solves. Residual certification makes an
  accepted output safe; it does not make the algorithm deterministic.
- The large `spectral_balance_threshold_batch` notebook has already investigated
  fresh CG, shifted solves, support-safe NAG, scalar retraction, exact/approximate
  safe boxes, tree/cycle-rank response, and deterministic sparsifier interfaces.
  Its 2026-09-04 halo integration audit supersedes older optimistic summaries.
- Fresh CG pays a second square-root condition factor in general. Existing
  almost-linear deterministic SDD substitution retains a subpolynomial graph
  factor. Neither meets the exact target as stated.

## Earlier directions, preserved with their actual status

1. An explicit map of proof authorities, special cases, and recurrence
   obstructions is recorded in `notes/prior-obstructions-vs-complete-proof.md`.
2. The cyclic-dual-averaging exact-support route is refuted by an outward-
   rounded interval witness on a canonical 255-vertex binary tree. Its
   dimension-free smoothness bound remains valid. See
   `notes/cyclic-dual-averaging.md` and the saved exact witness.
3. The earlier mass-constrained positive linear coupling, and a distinct
   averaged variant with sparse score corrections and an ordered threshold
   reporter. Both have proved accelerated potentials; neither yet has the
   required whole-run local volume theorem. The supplied-matrix and local
   implementations of the first variant agreed in 1,233 deterministic cases.
4. A mass-preserving score-repair variant has proved fully charged
   `O_tilde(T/rho)` work, a unique correct fixed point, an exact energy-debit
   formula, and a conditional root-rate bound on fixed auxiliary supports.
   Its general accelerated convergence remains open. See
   `notes/mass-preserving-score-repair.md` and STATUS.md. Extreme-cell dense
   score statistics from the first simulations are flagged for cancellation
   error; corrected replays maintain the prethreshold score directly.
5. None of these earlier open recurrence questions is retroactively resolved
   by the distinct continuation proof. Their stopped experiments and exact
   obstructions are retained for traceability.

All graph families, enumeration orders, numerical routines and checks were
deterministic. Numerical observations are not proofs.

## Research record

- `notes/`: mathematical arguments and source audit.
- `experiments/`: independent proof-falsification programs.
- `results/`: reproducible outputs and timestamps.

The task remains active until a valid deterministic proof, its complete work
ledger, and the requested minimum research duration have all been addressed.
