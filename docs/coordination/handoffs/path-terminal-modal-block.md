# Handoff: path-terminal-modal-block

- Agent family: codex
- Role: direction
- Branch: `agent/codex/path-terminal-static-inequality`
- Base commit: `71bf22f8ab78ebdeb750f953eced410365eec8ed`
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

- Requested result: Prove the static endpoint-path inequality
  `||(w-w_dir)_+||_(1,D) <= 21q^3/80` for every `m>=64`, or preserve the
  sharpest rigorous obstruction.
- Implemented result: Proved the exact signed-mass formula and the uniform
  bound `<3q^3/50`. Proved the normalized endpoint value
  `beta=d_m/q^3` lies in `(-57/200,0)`. Introduced the exact finite geometric
  endpoint comparator `h` and proved that coordinatewise `d>=h` implies the
  requested `21/80` inequality, including the parity-dependent seed-endpoint
  truncation.
- Consequence: The remaining static interface is local and falsifiable.
  With `T_r=d_(m-r)/q^3`, it is enough to prove
  `E_1=T_1+beta/4>=0`, `F_2>=E_1/2`, and
  `F_r>=F_(r-1)/2`, where `F_r=T_r+T_(r-1)/2`. This replaces the former
  undifferentiated signed bulk/tail problem.
- Deliberately unchanged: The local half-ratios, the early `J_kL` convolution,
  entry profiles, and full projection/envelope regime remain open. The
  logarithmic terminal block remains conditional, and no lower bound is
  claimed for other algorithms or models.

## Evidence

- A new exact preflight checks the rational `3/50` signed-mass ledger,
  `57/200` endpoint ledger, finite alternating-tail endpoint stencil, and
  exact signed-mass formula at `m=8,12`. It explicitly labels the local
  half-ratios open.
- The existing rational preflights still check chronology identities at
  `m=8,12`, the changing-face entries/final endpoint at `m=8`, and the exact
  leading correction recurrence through prefix 256.
- The floating screen remains evidence only for the two open entry profiles
  and terminal regime.
- Required commands and their final results are recorded in the direction
  `STATUS.md`; the note builds to 32 pages.

## Review notes

- Provider-owned paths changed: only
  `manuscript/notes/path_terminal_modal_block/`.
- Shared paths changed: note registry/README and this scoped coordination
  assignment/handoff.
- Main audit risks: the weighted telescoping identity for the signed mass,
  the monotonic block bounds at floor endpoints, the endpoint
  `e_m=-q^2(1-q)^m/2^m` correction, and the finite half-stencil tail parity.
- Next action: Prove the explicit local half-ratios uniformly for `m>=64`,
  then lift the same endpoint comparator through the exact folded
  binomial-window kernel for the early convolution margin.
