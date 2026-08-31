# Handoff: structured-response-composition

- Agent family: codex
- Role: direction-agent
- Branch: `agent/codex/structured-response-composition`
- Base commit: `e72d3de654f67a2939931c03536ab2d323310079`
- Assignment state: ready_for_review
- Write scope: the `volume_gated_acceleration` note, its note/shared result
  ledgers, one exact audit and registry entry, note dependencies, coordination
  assignment, and this handoff.

## Outcome

- Requested result: determine whether an already-proved structured response
  backend reduces the exact-optimum comparator's dense `O(q^-3)` response to
  the `O_tilde(q^-2)` product scale without hiding per-face solution,
  boundary, scan, write, validation, or output work.
- Implemented result:
  - Proved the general charged composition ledger.  The comparator visits at
    most `5/q+1` faces and every face has volume at most `5/q`, so
    `sum_U vol(U) <= 30/q^2`, at most six times
    `1/(rho sqrt(alpha))=5/q^2`.  Any exact backend whose actual per-face
    solve/materialization/complete-gate work is charged by that sum composes
    to product-scale work.  This clause is explicitly conditional and does
    not declare an arbitrary-graph backend.
  - Proved an unconditional literal-comparator implementation on every tree.
    Each active face is a connected induced subtree.  Fresh leaf elimination
    toward the seed, reverse solution materialization, coordinate conversion,
    and the complete boundary scan cost `O(vol(U))` per face and hence
    `O(q^-2)` total, with `O(q^-1)` peak storage/output.
  - Proved the bounded-block extension.  If every ambient biconnected block
    has at most `b` vertices, a fresh charged block--cut decomposition and
    dense leaf-block elimination on every face cost `O(b^3 q^-2)` arithmetic
    and `O(b^2 q^-1)` peak response storage.  It is product-scale up to
    polylogarithms for `b=polylog(1/q)` and assumes no supplied block IDs.
  - Specialized the note's append-only path `LDL^T` records to the comparator:
    every face is a prefix, only the immediate successor can violate, and
    batches are singleton.  A full reverse materialization and literal
    complete scan on every face cost `O(q^-2)` with every repeated write
    retained.
  - Formally imported the activation-once path theorem from
    `incremental_active_set_sdd`.  The exact map
    `D^(1/2) kappa_rho(D^(1/2)z)=alpha(rho d-r(z))` makes the shared strict
    gate identical to the source gate with `lambda=rho,kappa=tau`.  The
    imported forward records therefore realize the same prefix trace, while
    one terminal reverse pass gives output-linear `O(q^-1)` charged work.
  - Formally imported the `delayed_reflection_ladder` lazy tree and causal
    bounded-block results only as separate terminal-task solvers.  They reach
    `O_tilde(q^-2)` on their graph classes but generate their own response
    traces and are not claimed to reproduce the comparator's batches.
- Exact scope:
  - All new comparator results are exact-real and use the changed policy that
    gates directly on exact restricted optima.  They do not remove the
    logarithmic face hold for the named fixed-step candidate-envelope
    recurrence.
  - No arbitrary-core complete-violation response, finite-precision,
    stability, or bit-complexity theorem is claimed.

## Concurrent HSEG-LDL-FW assessment

- The untrusted Claude finding's combinatorial re-carve potential appears
  internally plausible: insertion raises its light-edge potential by
  `O(log n)`, and a hysteresis-2 swap releases more than the number of path
  vertices moved, giving `O(n log^2 n)` segment-tree structure work.
- It does not directly compose with this RPPR comparator as stated.  The code
  stores only the point-source load and appends every nonseed row with zero
  right-hand side; RPPR restricted systems have the distributed signed load
  `-alpha rho sqrt(d_i)` on every admitted nonseed row.  Its algebraic
  exactness is only float-verified in the finding, and its shipped pipeline
  queries frontier values and materializes only the final vector, not the
  full restricted optimum on every comparator face.
- Even if that interface were repaired, the fresh tree elimination theorem
  above already gives the required literal-comparator `O(q^-2)` bound without
  relying on the concurrent files.

## Evidence

- Added `volume_gated_acceleration.structured_response_composition`, an exact
  rational regression audit.  It checks 408 strict gate-map/product cells and
  36 distributed signed-right-hand-side leaf-elimination cells against dense
  rational solves.
- All 15 full-tier `volume_gated_acceleration.*` audits pass in 40.7 seconds,
  including both optional finite graph enumerations and the projection
  screen.
- The 84-page note builds successfully with no undefined reference or
  citation in the final log.
- Note inventory, coordination audit, audit-registry listing, focused Ruff
  lint/format, and `git diff --check` pass.
- All 210 repository tests pass.  Pytest reports only the 15 known
  temporary-directory cleanup warnings.

## Review notes

- Provider-owned paths changed: none.
- Formal note dependencies added: `incremental_active_set_sdd` and
  `delayed_reflection_ladder`; the existing `aesp_cd_l1_rppr` dependency is
  retained.  The dependency graph remains acyclic.
- Next target: either remove the per-face logarithm for the named recurrence,
  or construct a fully charged arbitrary-core response that reports the
  complete changing-face violation set.  Dynamic solves or energy telescopes
  that omit complete violation maintenance do not compose.
