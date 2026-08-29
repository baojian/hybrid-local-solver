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

## Outcome

- Requested result: Develop a new OP2 research direction through the exact
  obstacle/symmetric M-matrix LCP formulation, with a primary-source audit,
  support-discovery theorem, fully charged resource contract, projected-CG
  verdict, exact verification, and no manuscript promotion.
- Implemented result: Proved the exact reduction; a nested, coordinatewise
  increasing, true-support-only batched pivot theorem; supplied-support CG
  work at the `sqrt(kappa)` scale; a local minimum-norm KKT objective
  certificate; a path repeated-prefix obstruction; and an exact four-vertex
  counterexample to coordinatewise monotone face/projected CG.  Formulated a
  conditional OP2 theorem with one precise missing aggregate active-edge
  continuation/reporter lemma.  Added a primary-source literature verdict map,
  note registry/index entries, and exact rational verification artifacts.
- Deliberately unchanged: The canonical problem-definition note, the active
  manuscript, `docs/literature/local-solvers.md`, every other research
  direction, source/experiment/provider code, and the paper library.

## Evidence

- Tests added or changed: Added
  `manuscript/notes/active_edge_lcp/verify_counterexample.py`; it uses exact
  rational arithmetic and asserts the graph reduction, old-face and optimum
  solves, four CG step sizes and iterates, positivity, energy decrease,
  conjugacy, the exact overshoot, and terminal solve.
- Commands run:
  - `python3 manuscript/notes/active_edge_lcp/verify_counterexample.py`
  - `make -C manuscript/notes/active_edge_lcp`
  - `python3 manuscript/notes/tools/note_inventory.py check`
  - `git diff --check`
  - `make agent-audit`
  - `make test`
  - `make lint`
- Results:
  - Exact rational audit passed and matched the checked output byte-for-byte.
  - Focused note build passed: 14-page PDF, resolved citations/references, and
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
  - A transient first test run rejected five note-local LaTeX aliases.  They
    were expanded in place, and the final full test run passed.

## Review notes

- Provider-owned paths changed: none.
- Shared paths changed: only the six explicitly permitted documentation,
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
  with an all-negative boundary reporter, or first prove the aggregate
  contract on a structural graph class.  Any continuation must be
  margin-free or explicitly charge sign refinement.

## Commits and checks

- Research note and literature milestone:
  `d433833c2ed8abe9f7b74db455c0e968c16ce692`.
- Final handoff/check milestone: pending this commit.
- Focused PDF: 14 pages, all pages rendered to PNG and visually inspected;
  no clipping, overlap, or unreadable table/equation was found.
- Final repository checks: `make agent-audit` passed; `make test` passed
  213/213; `make lint` has the scoped external formatting failure recorded
  above, while all owned Python lint and format checks pass.
