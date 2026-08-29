# Handoff: active-edge-lcp

- Agent family: codex
- Role: direction
- Branch: `agent/codex/active-edge-lcp`
- Base commit: `df0725fcf68797c5bf53527eabb6ae2dd64b9f33`
- Assignment state: ready_for_review
- Write scope:
  - `docs/coordination/active_assignments.toml`
  - `docs/coordination/handoffs/active-edge-lcp.md`
  - `docs/literature/index.md`
  - `docs/literature/lcp-solvers.md`
  - `manuscript/notes/README.md`
  - `manuscript/notes/registry.toml`
  - `manuscript/notes/active_edge_lcp/`
- Permitted shared files:
  - `docs/coordination/active_assignments.toml`
  - `docs/coordination/handoffs/active-edge-lcp.md`
  - `docs/literature/index.md`
  - `docs/literature/lcp-solvers.md`
  - `manuscript/notes/README.md`
  - `manuscript/notes/registry.toml`
  - `manuscript/notes/active_edge_lcp/`

## Outcome

- Requested result: Develop a new OP2 research direction through the exact
  obstacle/symmetric M-matrix LCP formulation, with a primary-source audit,
  support-discovery theorem, fully charged resource contract, projected-CG
  verdict, exact verification, and no manuscript promotion.
- Implemented result: In addition to the exact reduction, support-safe nested
  pivots, supplied-support CG bound, and local KKT objective certificate,
  proved a margin-free approximate-face dichotomy.  A residual-derived known
  threshold either certifies a safe pivot or certifies the requested objective
  gap; an overlapping-interval corollary removes finite-precision sign-margin
  assumptions.  Proved a global exact-face energy/slack-motion telescope and
  an exact-real `O(vol(S*))` append-only `LDL^T` solver for endpoint-seeded
  paths.  Preserved the terminal-volume obstruction for naive repeated scans
  and the exact four-vertex projected-CG overshoot.  The end-to-end OP2 result
  is conditional on one fully charged arbitrary-graph changing-face response
  and known-threshold reporter theorem.  Extended the primary-source map with
  global Howard and dynamic Laplacian/matrix-inverse results.
- Deliberately unchanged: The canonical problem-definition note, the active
  manuscript, `docs/literature/local-solvers.md`, every other research
  direction, source/experiment/provider code, and the paper library.

## Evidence

- Tests added or changed: Retained the exact-rational projected-CG audit and
  added `verify_threshold_dichotomy.py` and `verify_path_ldl.py`.  The former
  checks 720 rational threshold cases and 36 exact energy/slack telescopes;
  the latter checks 580 canonical path instances through length 30 against
  direct principal solves and full KKT conditions.
- Commands run:
  - `python3 manuscript/notes/active_edge_lcp/verify_counterexample.py`
  - `python3 manuscript/notes/active_edge_lcp/verify_threshold_dichotomy.py`
  - `python3 manuscript/notes/active_edge_lcp/verify_path_ldl.py`
  - `make -C manuscript/notes/active_edge_lcp`
  - `python3 manuscript/notes/tools/note_inventory.py check`
  - `git diff --check`
  - `make agent-audit`
  - `make test`
  - `make lint`
- Results:
  - All three exact rational audits passed and matched their checked outputs
    byte-for-byte; all three scripts pass Ruff lint and format checks.
  - Focused note build passed: 18-page PDF, resolved citations/references, and
    no undefined reference, fatal, or overfull-box diagnostics.
  - Every final PDF page was rendered to PNG and visually inspected; no
    clipping, overlap, broken table, or unreadable equation was found.
  - Note registry and `git diff --check` passed.
  - Final `make agent-audit` passed after the documented review transition.
  - Final `make test` passed: 213 tests, with 15 temporary-directory cleanup
    warnings from pytest.
  - `ruff check .` and the owned script's format check passed.  Full
    `make lint` remains red only because `ruff format --check .` reports nine
    pre-existing files under
    `experiments/proof_audits/aesp_cd_l1_rppr/`; that path belongs to the
    simultaneous `windowed-spectral-lyapunov-7h` assignment and was left
    untouched.  The first lint run also found the owned script; it was
    formatted before the final run.
  - The resumed full test run initially had the expected active-assignment
    overlap plus one note-local reserved notation failure.  The notation was
    fixed before the final transition and the final full test run passed.

## Review notes

- Provider-owned paths changed: none.
- Shared paths changed: only the explicitly permitted direction,
  coordination, registry, and index paths listed above.
- Branch/worktree exception: the Codex worktree manager kept the checkout on a
  detached HEAD.  To avoid damaging manager state, the checkout was not
  switched; the logical branch ref `agent/codex/active-edge-lcp` was created at
  the actual base and advanced after each coherent detached-HEAD commit.
- Coordination audit transition: an initial `make agent-audit` while this
  assignment was `active` failed because the simultaneously active
  `windowed-spectral-lyapunov-7h` controller also necessarily lists
  `docs/coordination/active_assignments.toml`.  No other assignment was
  modified.  This assignment was moved to `ready_for_review`, as required for
  handoff, before rerunning the audit so only one active writer owns that
  shared registry.
- Open decision: whether to pursue an arbitrary-graph dynamic Schur response
  with the proved known-threshold reporter, or first extend the exact path
  recurrence to a broader structural graph class.  Exact-sign refinement is
  no longer a legitimate missing assumption: the residual threshold already
  removes it.

## Commits and checks

- Research note and literature milestone:
  `d433833c2ed8abe9f7b74db455c0e968c16ce692`.
- Final research/check milestone:
  `465925f05d38b13b06c49ba04b047e76fb28b39c`.
- Strengthened threshold/path/literature milestone:
  `3e8f38a43ff84e9b12848d8fb60490592b002817`.
- Focused PDF: 18 pages, all pages rendered to PNG and visually inspected;
  no clipping, overlap, or unreadable table/equation was found.
- Final repository checks: `make agent-audit` passed; `make test` passed
  213/213; `make lint` has the scoped external formatting failure recorded
  above, while all owned Python lint and format checks pass.
