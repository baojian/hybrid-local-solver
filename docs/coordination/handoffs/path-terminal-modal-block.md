# Handoff: path-terminal-modal-block

- Agent family: codex
- Role: direction
- Branch: `agent/codex/path-terminal-semantic-explicit-synthesis`
- Base commit: `f76db2e58193954cd8f8da25c8e5e4b05b3aec88`
- Assignment state: ready_for_review
- Write scope:
  - `docs/coordination/active_assignments.toml`
  - `docs/coordination/handoffs/path-terminal-modal-block.md`
  - `manuscript/notes/README.md`
  - `manuscript/notes/registry.toml`
  - `manuscript/notes/path_terminal_modal_block/`

## Outcome

- Integrated the proved proper-prefix chronology, position and velocity entry
  profiles, static endpoint-tail reduction, correlated early stopped ledger,
  interior folded-source theorem, and five-frontier first-order theorem.
- The interior two-step cone holds for every `m>=64` on `0<=j<=m-6`.
  Each of the five remaining frontier expressions has an exact positive joint
  first-order limit.  An exact finite transfer ledger proves their common
  cutoff `m>=8192`.  Therefore the full cone, local half-ratios, `d>=h`, and
  `||u_+||_(1,D)<21q^3/80` hold throughout that range.
- The early theorem closes `qk<3/50` with margin `1807/115200`; the static
  bound and late position theorem close `qk>=3/50` with transition slack
  `1667/625000`.  The first late integer follows an already-covered early
  integer.  For `m>=8192`, projection inactivity and zero safe subtraction
  persist at every full-face time in the continued named recurrence.
- The modal-band range theorem now gives an unconditional asymptotic
  `Omega(q^-1 log(1/q))` terminal block for the named exact-real recurrence.
  The named nonlinear regime has the explicit cutoff `m>=8192`; the modal
  terminal theorem separately retains its sufficiently-large-`m` scope.
- For the named implementation's prescribed certificate runtime, a full-face
  step costs `vol(P_m)=1/(8q)`.  Thus the terminal ledger is at least
  `(64q^2)^-1 log(1/q)-(8q)^-1`, or
  `Omega(eps_ppr^-2 log(1/eps_ppr))` at `eps_ppr=2q/5`.  This is not a
  semantic-error, general-algorithm, or eleven-resource lower bound.
- For every `m>=8192`, the continued state satisfies
  `||p_k-p*||_inf<q/5` by `k=ceil(15/(4q))`.  Running until the earlier of
  that theorem time and the prescribed certificate returns PPR error below
  `2q/5` with total charged work at most
  `121/(256q^2)+1/(8q)=O(q^-2)`.  The measured crossing near `qk=3.43` is
  labeled float64 evidence only.

## Scope boundaries

- The theorem is only for the named transported-center projected and
  safe-envelope recurrence.  It does not extend to alternative face
  schedules, nonlocal responses, or arbitrary polynomial/Krylov methods.
  Exact CG can solve this finite path in at most `m+1` matvecs.
- The stronger separate convolution `L_k u<=13q^3/200` remains unproved but
  is unnecessary.  The broader `q^3/16`-through-`17/200` claim is false.
- Uniform frontier signs beginning exactly at `m=64` remain optional; the
  proved explicit threshold is `m>=8192`.

## Verification

- `verify.py 64` passes the consolidated exact and floating checks.
- `verify_static_frontier.py` checks the exact frontier reduction, five joint
  limits, and positive polynomial certificates.
- `verify_stopped_baseline.py`, `verify_finite_stopped_ledger.py`, and
  `verify_regime_reduction.py` check the early and late nonlinear pieces.
- `verify_asymptotic_closure.py` checks the exact constant chain and integer
  early/late handoff; the explicit threshold is checked separately.
- `verify_static_frontier_cutoff.py` reconstructs the causal and homogeneous
  transfer certificates and proves the rational `m>=8192` cutoff ledger.
- `verify_semantic_stop.py` checks the exact `15/4` Taylor certificate,
  rational slacks, and charged-work constants, then reports measured crossing
  times separately.
- The note builds warning-free; note, target, and agent audits, focused
  Ruff/format, diff, control-byte, and conflict-marker checks pass before
  promotion.

## Optional next work

Improve the explicit cutoff toward `m>=64` or sharpen the semantic constant
`15/4` toward the measured crossing near `3.43`.  The core theorems have no
remaining proof interface.
