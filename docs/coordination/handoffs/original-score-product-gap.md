# Handoff: original-score-product-gap

- Agent family: codex
- Role: direction
- Branch: `agent/codex/original-score-product-gap`
- Base commit: `50a9a1c8aab264900987bb5a7f621662039814a9`
- Assignment state: ready_for_review
- Write scope: the `volume_gated_acceleration` note, two exact scalar audits
  and their registry entries, the note registry, coordination assignment, and
  this handoff.

## Outcome

- Requested result: investigate whether the per-face logarithm or dense
  exact-response factor in the complete-gate fallback can be removed under
  the same exact-real point-seed model, retaining all response, scan, write,
  and output charges.
- Implemented result:
  - Sharpened the named fixed-step gate threshold from order `q^12` to
    `E_gate=4q^10/(25(1+q^2)(1+3q^2)^2)`.  If
    `Rmax=max_i |r_i(z)|`, then `Rmax^2 <= (1+q^2)E`.  For
    `w=z-[z-delta*1]_+`, Stieltjes signs give
    `(Hw)_i <= ((1+q^2)/2) delta`; hence every active envelope row is safe at
    the displayed threshold.  The hold bound becomes
    `ceil(log(25(1+q^2)(1+3q^2)^2/(4q^8))/-log(1-q))`.  Its asymptotic order
    remains `O(q^-1 log(1/q))` per face.
  - Proved an exact-optimum active-set comparator.  If the exact restricted
    optimum already materialized by dense transport is allowed to be the gate
    candidate, its safe correction is zero, so the same complete gate runs
    immediately on every face.  This removes the hold logarithm under that
    changed control policy: cumulative scans are `O(q^-2)`, dense factor and
    solve work is `O(q^-3)`, storage is `O(q^-2)`, and row/output charges are
    `O(q^-1)`.
  - Proved a representation-specific dense-response STOP.  For any fixed-gap
    family of connected 3-regular `n`-vertex spectral expanders, set `q=1/(2n)` and
    `rho=tau=q/5`.  The exact PPR resolvent gives
    `||pi-1/n||_2 <= 2q^2/gamma`, so every normalized RPPR coordinate exceeds
    `tau` for large `n`.  Terminal certification therefore forces the named
    execution, and the exact-optimum comparator, to reach the full face.
    Linear treewidth and strict Stieltjes fill force every original-basis
    explicit ordinary scalar Cholesky/LDL response to store `Omega(n^2)`
    scalars and execute `Omega(n^3)=Omega(q^-3)` scalar pivot updates, even
    with the final support and best offline ordering supplied.
- Deliberately unchanged:
  - The logarithm remains open for the named post-step candidate-envelope
    recurrence.  The exact-optimum comparator removes it only by changing the
    control policy.
  - The expander result is not a recurrence, information-theoretic, or
    all-linear-algebra lower bound.  It excludes compressed, matrix-free,
    iterative, approximate, fast-matrix-multiplication, and other
    non-Cholesky responses.
  - The result is exact-real.  Finite precision, bit complexity, numerical
    stability, implicit boundary response, and product-scale non-Cholesky
    work remain open.
  - The companion `propagate_settle_framework` expander result and
    `incremental_active_set_sdd` exact-active-set framework are recorded only
    as context/provenance; both new proofs are self-contained and add no
    formal registry dependency.

## Evidence

- Added `volume_gated_acceleration.explicit_cholesky_expander_stop`, an exact
  rational regression audit for the PPR resolvent normalization, spectral
  multiplier, RPPR margin, product-scale conversion, filled-clique storage,
  and scalar Schur-update sum.  It passes 20 cells.
- Updated `volume_gated_acceleration.original_score_quartic` to check the
  sharpened residual threshold and exact diagonal-envelope constant.  It
  still passes 4,860 integer-degree and eight horizon cells.
- All 14 full-tier `volume_gated_acceleration` audits pass in 47.8 seconds,
  including both optional finite graph enumerations and the projection screen.
- The 80-page note builds successfully with no undefined reference or
  citation in the final log.  The note inventory, coordination audit, focused
  Ruff lint/format, and `git diff --check` pass.
- All 210 repository tests pass with 15 known temporary-directory cleanup
  warnings.
- Repository-wide `make lint` reproduces the 1,345 pre-existing findings
  under `manuscript/claude-overnight-2026-08-24/`; focused lint on both changed
  Python files passes.

## Review notes

- Provider-owned paths changed: none.
- Shared paths changed: the proof-audit registry, note registry, and
  coordination metadata listed in the assignment.
- Open decisions or follow-up: either prove/remove the logarithm for the named
  candidate-envelope recurrence, or construct a fully charged compressed,
  matrix-free, iterative, approximate, or otherwise non-Cholesky response
  with `O_tilde(q^-2)` total work.  Do not attempt another sparse-ordering
  optimization of the explicit scalar factor on arbitrary graphs.
