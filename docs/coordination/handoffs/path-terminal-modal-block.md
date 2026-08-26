# Handoff: path-terminal-modal-block

- Agent family: codex
- Role: direction
- Branch: `agent/codex/path-terminal-regime-static`
- Base commit: `b93b85312a9c06265959f082bbe5102aed44d0c9`
- Assignment state: ready for review
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

- Requested result: Attack terminal projection and unclipped-envelope
  preservation through `floor((1/8)q^-1 log(1/q))`, preserving the sharpest
  exact reduction if the full regime does not close.
- Implemented result: Split the even ideal binomial packet exactly into two
  half-endpoint packets with opposite directed velocities. Their complete
  `K/J` evolution is two nonpositive Markov waves at every time. Proved the
  literal entry correction `c=r_0-g` is coordinatewise nonpositive for every
  `m>=64`. Derived the infinite-line `J_k` coefficient as a binomial
  tail and proved that all cycle aliases have maximum coefficient at most
  `1+(k-1)/(2m)`. Thus every positive terminal residual is bounded by
  this factor times the positive weighted mass of one static directed-velocity
  remainder. Damping makes the whole time factor at most `8e^(-7/8)`.
- Consequence: The former `k||w||_infinity` obstruction and repeated
  reflection loss are removed exactly. The directed remainder is further
  reduced exactly to `u=Ld`, with `d` explicit from the last prefix and a
  lower binomial packet; the `J_kL` kernel is an exact binomial window. The
  remaining regime work is a signed bulk/tail estimate and an early/late
  position lower bound.
- Deliberately unchanged: Those two estimates and both entry-profile
  inequalities remain open. The logarithmic terminal block remains
  conditional, and no lower bound is claimed for other algorithms or models.

## Evidence

- A new exact preflight checks the half-endpoint cycle split, directed wave
  identity, folded `J_k` alias bound, `J_kL` window, entry-correction sign,
  and static `u=Ld` identity at `m=8,12`.
- The existing rational preflights still check chronology identities at
  `m=8,12`, the changing-face entries/final endpoint at `m=8`, and the exact
  leading correction recurrence through prefix 256.
- The floating screen remains evidence only for the two open entry profiles
  and terminal regime.
- Required commands and their final results are recorded in the direction
  `STATUS.md`; the note builds to 29 pages.

## Review notes

- Provider-owned paths changed: only
  `manuscript/notes/path_terminal_modal_block/`.
- Shared paths changed: note registry/README and this scoped coordination
  assignment/handoff.
- Main audit risks: half endpoint weights, opposite direction on the reflected
  packet, the old-row comparison proving `c<=0`, and the factor two in the
  `2m`-cycle alias count.
- Next action: Bound the positive bulk and alternating terminal tail in the
  explicit `d` certificate sharply enough for `21/80`, then use the exact
  folded binomial-window kernel for the early convolution margin.
