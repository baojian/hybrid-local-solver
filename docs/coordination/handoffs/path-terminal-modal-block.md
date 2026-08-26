# Handoff: path-terminal-modal-block

- Agent family: codex
- Role: direction
- Branch: `agent/codex/path-terminal-position-profile`
- Base commit: `469758e8c14e3b4c3ed162fb4479dc3e5d7c3eb5`
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

- Requested result: Close the first, position-only entry profile
  asymptotically on the growing even-mode band, without importing the open
  velocity or terminal-regime claims.
- Implemented result: Proved
  `m*abs(C_(2s)-G_(2s))/alpha<=1/256` uniformly for
  `1<=s<=floor(sqrt(m/(64 log(16m))))` and all sufficiently large `m`.
  The exact five-piece split has base and final degree/endpoint terms
  `o(q^2)`. The constant-`U` trace has an exact finite Chebyshev sum and
  limiting absolute bound `1/(240*pi^2)`; total variation of the limiting
  `U-U0` profile gives `1/(360*pi)`; the sharp positive mass bound gives
  `43/(10240*pi)`. Using `pi>3`, their upper ledger is
  `257/92160<1/256`, with rational slack `103/92160`.
- Consequence: Only the entry velocity profile and the terminal
  projection/unclipped-envelope regime remain as assumptions in the
  conditional logarithmic-block theorem.
- Deliberately unchanged: Those two remaining statements are open. Hence the logarithmic
  terminal block remains conditional, and no lower bound is claimed for other
  algorithms, implicit-response implementations, or a broader oracle class.

## Evidence

- A new preflight checks the exact rational position ledger, the strict slack,
  and the finite constant-`U` Chebyshev response against direct recurrence.
- The existing rational preflights still check chronology identities at
  `m=8,12`, the changing-face entries/final endpoint at `m=8`, and the exact
  leading correction recurrence through prefix 256.
- The floating screen agrees with the proved position profile and remains
  evidence only for the open velocity profile and terminal regime.
- Required commands and their final results are recorded in the direction
  `STATUS.md`; the note builds to 30 pages.

## Review notes

- Provider-owned paths changed: only
  `manuscript/notes/path_terminal_modal_block/`.
- Shared paths changed: note registry/README and this scoped coordination
  assignment/handoff.
- Main audit risks: verify the uniform source-to-Riemann remainder, the
  `16*phi` derivative-source normalization, the exact endpoint cancellation,
  and the strict three-constant ledger.
- Next action: Prove the entry velocity bound by signed summation of the five
  source pieces, then prove projection inactivity and unclipped safe
  subtraction through `floor((1/8)q^-1 log(1/q))`.
