# Handoff: seed-maximum-principle

- Agent family: codex
- Role: direction
- Branch: `agent/codex/seed-maximum-principle`
- Base commit: `71764c15c5bc2bb92f01d9d807942acf61e4be85`
- Assignment state: ready_for_review
- Write scope:
  - `docs/coordination/active_assignments.toml`
  - `docs/coordination/handoffs/seed-maximum-principle.md`
  - `manuscript/notes/README.md`
  - `manuscript/notes/registry.toml`
  - `manuscript/notes/seed_maximum_principle/`
- Permitted shared files: the same five paths above.

## Outcome

- Proved the strict degree-normalized seed maximum
  `pi_u / d_u <= pi_v / d_v` by a discrete maximum principle.
- Proved the exact reciprocity identity
  `pr(e_u)_v / pi_v = d_v pi_u / (d_u pi_v)` and hence response-row constant
  `Phi_v = 1` on every connected graph.
- Corrected the inverted degree ratio in the earlier campaign transcription.
- Derived the general nonnegative-residual/output-map terminal bound
  `Psi_v <= eps_ppr vol(V) / (1 - gamma_alpha B)` and the corresponding
  monotone seed-operation lower bound.
- Deliberately left the concurrently owned, untracked
  `class_separation_ladder` directory unchanged.

## Evidence

- Focused LaTeX build: passed, five pages, no undefined references, box
  warnings, or other LaTeX warnings.
- Note inventory: passed, 19 notes across five tracks.
- Independent finite screen: 27,120 rooted graph/parameter cases from the
  connected graph atlas through seven vertices; zero normalized-seed or
  reciprocity violations.
- Repository tests: 210/210 passed.
- Coordination audit and branch-scope audit: passed.
- Repository lint: 1,345 pre-existing Ruff findings, all under
  `manuscript/claude-overnight-2026-08-24/`; this assignment adds no Python
  and no lint finding.

## Review notes

- Provider-owned paths changed: none.
- Shared paths changed: assignment/handoff, note registry, and generated note
  index only.
- The proof is independent of the flawed imported transport-cut scaling in
  the class-ladder draft.  Its terminal corollary needs only residual and
  output-map nonnegativity plus the column-mass bound.
- Do not extend the result to signed residuals, signed output maps, block
  elimination, or another response primitive.
