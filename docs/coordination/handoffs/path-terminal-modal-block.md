# Handoff: path-terminal-modal-block

- Agent family: codex
- Role: direction
- Branch: `agent/codex/path-terminal-chronology-finite-q`
- Base commit: `b28ed46c0a734aa017ced47e3bbbcf0b167935da`
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

- Requested result: Prove the finite-`q` shared-coordinate correction sign for
  the named terminal path, or preserve the sharpest exact obstruction.
- Implemented result: Proved `K_n(j)>0` on every shared proper-prefix
  coordinate for every `m>=64`. The exact rescaling
  `C_n/q^3=(1-q)^(n-2) bar(c)_n` makes the homogeneous recurrence identical to
  its solved `q=0` limit. The finite perturbation splits into a moving
  derivative packet and a newest-row point mass. Exact binomial coefficients
  show every stopped reflected derivative response lies in `[-4,4]`;
  total-variation control gives derivative loss at most `1/90`. The point
  mass lies in `[-43q/75,0]` and its folded response is at most one. The
  exact initial response costs at most `3q/5`. From prefix six onward the
  sharper leading margin `19/320` therefore leaves
  `19/320-43/1200-1/90=179/14400`. Prefix two is direct; prefixes three
  through five use a self-contained perturbation loss below `3q<1/80`.
- Consequence: The earlier exact reduction now proves raw positivity,
  nonpositive post-step residual, zero safe correction, and exactly the next
  singleton admission at every proper prefix for `m>=64`. The changing-face
  source, its factored transform, and scalar position/velocity reduction are
  unconditional in that range.
- Deliberately unchanged: The two entry-profile inequalities and the terminal
  projection/unclipped-envelope regime remain open. Hence the logarithmic
  terminal block remains conditional, and no lower bound is claimed for other
  algorithms, implicit-response implementations, or a broader oracle class.

## Evidence

- The exact preflight checks the positive Green coefficient formula, the
  stopped derivative-prefix bound through final length 128, folded point-mass
  response, the early `n=2,3` mass identity, the small-prefix perturbation
  ledger, and the final `179/14400` arithmetic.
- The existing rational preflights still check chronology identities at
  `m=8,12`, the changing-face entries/final endpoint at `m=8`, and the exact
  leading correction recurrence through prefix 256.
- The floating screen remains evidence only for the two open entry profiles
  and terminal regime.
- Required commands and their final results are recorded in the direction
  `STATUS.md`; the note builds to 26 pages.

## Review notes

- Provider-owned paths changed: only
  `manuscript/notes/path_terminal_modal_block/`.
- Shared paths changed: note registry/README and this scoped coordination
  assignment/handoff.
- Main audit risks: verify the early reflected overlap at source times two and
  three, chronological reversal `k=N-n`, the `3q/5` initial response, and the
  `43/1200+1/90` loss ledger.
- Next action: Prove the two exact entry-profile bounds by signed summation of
  the five source pieces, then prove projection inactivity and unclipped safe
  subtraction through `floor((1/8)q^-1 log(1/q))`.
