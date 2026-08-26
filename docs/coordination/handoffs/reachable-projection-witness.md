# Handoff: reachable-projection-witness

- Agent family: codex
- Role: direction
- Branch: `agent/codex/reachable-projection-witness`
- Base commit: `7b822627493787941295d697f5ed4ed402f56afc`
- Assignment state: ready_for_review
- Write scope: the coordination record and this handoff, the proof-audit
  registry and new reachable-projection audit, and the listed
  `volume_gated_acceleration` note files.

## Outcome

- Requested result: search literal zero-start complete-gate traces for a
  reachable clipped row with positive post residual and actual original-score
  ledger debt; test whether the normal-anchor effect yields a scalable
  superquartic obstruction.
- Implemented result:
  - Added an exact 30-vertex, point-seed trace at `q=12/625`.  The complete
    gate admits through the exact action word
    `A^3 A^3 H^7 A^9 H^2 A H^11 A^9 H A^2 A A H^2 C` and certifies at
    stage 32.
  - At vertex 23 in stage 12 the projected candidate is exactly zero, its
    projection normal is positive, and its post-step residual is positive and
    is the literal all-coordinate residual maximum.  Thus relevant clipping
    is reachable, not merely an algebraic off-trajectory possibility.
  - Exact rational arithmetic proves `553/100 < n_23/b_23 < 55301/10000`,
    strict positive debt `Xi_12-D_12`, and required reserve coefficient
    `433/5000 < lambda_12 < 867/10000`.  Equivalently,
    `1178/10^11 < q^4 lambda_12 < 1179/10^11`.
  - Added an exact rational screen on the same rooted graph for
    `q=187/10000,...,195/10000`.  Relevant clipping appears only on a short
    finite window; positive debt appears at `q=0.0192,0.0193,0.0194`.
    This finite screen supplies no asymptotic family.
  - Updated scope, ledger, README, and STATUS language to record exactly what
    the witness refutes: the shortcut that every reachable clipped row has
    nonpositive post residual.
- Deliberately unchanged:
  - No `Omega(q^-5)` coefficient, convergence failure, solver-class lower
    bound, or work lower bound is claimed.  The witness is finite and its
    coefficient is below `0.087`, so it does not widen the existing sharp
    `Theta(q^-4)` reachable lower order.
  - Floating high-degree motif screens were not promoted.  Some finite
    resonances had `q n/b` near `0.1`, but no persistent small-`q` family was
    found.
  - No provider-owned file, dirty main worktree, or file outside the registered
    scope was changed.

## Evidence

- Added the exact rational audit
  `volume_gated_acceleration.reachable_projection_witness`.  It checks the
  graph, full chronology, strict gate margins, interior restricted optima,
  active projection, residual maximum, normal-anchor ratio, positive debt,
  and coefficient intervals.  Its full mode runs the nine-point rational
  `q` screen.
- Commands and results:
  - The new audit passes in primary and full-screen modes.
  - All 12 full-tier `volume_gated_acceleration` audits pass.
  - The note builds successfully; `make note-audit` and `make agent-audit`
    pass.
  - All 210 tests pass, with only temporary-directory cleanup warnings.
  - The new verifier passes focused Ruff lint and format checks, and
    `git diff --check` passes.
  - Repository-wide `make lint` remains blocked by 1,345 pre-existing Ruff
    errors in tracked overnight research scripts present at the base commit;
    none is in the new audit.

## Review notes

- Provider-owned paths changed: none.
- Remaining mathematical target: either prove a graph-uniform restriction on
  first relevant clipping/normal-anchor debt or construct an exact scalable
  family whose required reserve coefficient is superquartic.  The present
  finite witness settles neither alternative.
