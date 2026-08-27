# Handoff: path-terminal-modal-block

- Agent family: codex
- Role: direction
- Branch: `agent/codex/path-terminal-static-cone`
- Base commit: `0d6ed658be4aa9bee01e6d520e066d83e3797936`
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
- Exact follow-up reduction: With prefix correction
  `K_n=C_n-(1-q)C_(n-1)/2`, the temporal decrement
  `mathcal T_m=(1-q)K_(m-1)-K_m` obeys
  `d_j=2(1-q)(L mathcal T_m)_j` on `1<=j<=m-4`, and the same identity at
  the seed after exact cancellation of the ideal endpoint atom. The
  comparator `h` has preimage `-4h/(1-q)` on the interior. An interior
  preimage comparison plus the seed and three direct frontier inequalities
  is therefore sufficient. It remains OPEN, is not necessary, and is not
  inferred from a fixed-prefix `q->0` limit because the named family has
  `mq=1/16`.
- Sharper exact interface: The half-ratios cancel to the two-step cone
  `d_j-d_(j+2)/4>=0`, with two endpoint conditions. For `j<=m-6`, this cone
  equals a folded Green-kernel sum of an exact source-free base, the
  derivative packets `epsilon_n(1,2,-3)/4`, and newest-row masses
  `mu_n=-q nu_n`. The scalar window `2/5<nu_n<43/75` is proved uniformly.
  The mass kernel is now proved by exact binomial smoothing, a finite dyadic
  lobe certificate, and an entropy tail. The weakened base kernel `B>-q/16`
  needed by the replacement ledger is also proved by two binomial sign
  regimes, a finite exact certificate, and a Hoeffding tail. The derivative
  kernel and five direct frontier rows remain OPEN; the note does not infer signs of
  individual summands. The proposed derivative constant `-q/16` is now an
  exact asymptotic STOP (already false at fixed endpoint distance seven), while
  the weaker sufficient replacement `-q/8` is reduced to three exact folded
  prefix-lobe estimates; its scalar variation and Abel ledger are proved. An
  exact rational prefix generating function proves all three estimates at
  `D=6,7`, leaving only `D>=8`. The
  base proof exposes an exact five-point binomial stencil, alternating endpoint
  atom, and nonnegative-kernel initial perturbation.
- Deliberately unchanged: The local half-ratios, the early `J_kL` convolution,
  entry profiles, and full projection/envelope regime remain open. The
  logarithmic terminal block remains conditional, and no lower bound is
  claimed for other algorithms or models.

## Evidence

- A new exact preflight checks the rational `3/50` signed-mass ledger,
  `57/200` endpoint ledger, finite alternating-tail endpoint stencil, and
  exact signed-mass formula and temporal smoothing identity at `m=8,12`. It
  also checks the two-step equivalence, mass window, signed smoothing base,
  and one-dimensional lobe certificate. It labels the base/derivative
  folded-kernel ledger, local half-ratios, and temporal preimage comparison
  open.
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
- Next action: Prove the replacement `-q/8` derivative estimate's three
  prefix-lobe bounds for `D>=8` and five
  direct frontier rows, or otherwise prove the explicit local
  half-ratios uniformly for `m>=64`; then lift the endpoint comparator through the exact folded
  binomial-window kernel for the early convolution margin.
