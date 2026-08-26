# Handoff: path-terminal-modal-block

- Agent family: codex
- Role: direction
- Branch: `agent/codex/path-terminal-velocity-profile`
- Base commit: `e68835281f0bb594bff97c37c36915c14d84180e`
- Assignment state: ready_for_review
- Write scope:
  - `docs/coordination/active_assignments.toml`
  - `docs/coordination/handoffs/path-terminal-modal-block.md`
  - `manuscript/notes/README.md`
  - `manuscript/notes/registry.toml`
  - `manuscript/notes/path_terminal_modal_block/`
- Permitted shared files:
  - `docs/coordination/active_assignments.toml`
  - `docs/coordination/handoffs/path-terminal-modal-block.md`
  - `manuscript/notes/README.md`
  - `manuscript/notes/registry.toml`

## Outcome

- Requested result: Close the velocity entry profile asymptotically on the
  growing even-mode band, without importing the open terminal-regime claim.
- Implemented result: Proved
  `m*abs(V_(2s)+G_(2s)/5)/alpha<=1/4` uniformly for
  `1<=s<=floor(sqrt(m/(64 log(16m))))` and all sufficiently large `m`.
  The exact source kernel removes the apparent small-sine loss. A uniform
  continuum limit retains the boundary cancellation among the homogeneous
  base, derivative source, and final endpoint. Rational total-variation bounds
  give `3479/14400<1/4`, with slack `121/14400`.
- Consequence: Only the terminal projection/unclipped-envelope regime remains
  as an assumption in the conditional logarithmic-block theorem.
- Deliberately unchanged: That remaining statement is open. Hence the logarithmic
  terminal block remains conditional, and no lower bound is claimed for other
  algorithms, implicit-response implementations, or a broader oracle class.

## Evidence

- A new preflight checks the exact rational velocity ledger, its strict slack,
  the positive Bernstein certificate, and the continuum normalization.
- The existing rational preflights still check chronology identities at
  `m=8,12`, the changing-face entries/final endpoint at `m=8`, and the exact
  leading correction recurrence through prefix 256.
- The floating screen agrees with both proved entry profiles and remains
  evidence only for the open terminal regime.
- Required commands and their final results are recorded in the direction
  `STATUS.md`; the note builds to 32 pages.

## Review notes

- Provider-owned paths changed: only
  `manuscript/notes/path_terminal_modal_block/`.
- Shared paths changed: note registry/README and this scoped coordination
  assignment/handoff.
- Main audit risks: verify the exact velocity source kernel, the uniform
  source-to-Riemann remainder, base/endpoint cancellation, and both rational
  variation bounds.
- Next action: Prove projection inactivity and unclipped safe subtraction
  through `floor((1/8)q^-1 log(1/q))`.
