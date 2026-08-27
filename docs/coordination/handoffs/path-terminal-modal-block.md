# Handoff: path-terminal-modal-block

- Agent family: codex
- Role: direction
- Branch: `agent/codex/path-terminal-early-combined`
- Base commit: `9f52462`
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

- Integrated the independently proved position profile, velocity profile, and
  static endpoint-tail reduction. The entry profiles are no longer open.
- Proved the uniform full-entry bounds
  `min p* > 1243q/160`, `max p* < 8q`, `e_0 >= -8q`, and
  `f_0 >= -q/8`.
- Extended the finite correction ledger through one hypothetical degree-two
  row to prove that the first actual full-face average residual is strictly
  negative. The old-row margin is at least `1429/115200`; the actual
  degree-one endpoint upper bound is `-46683733/78684160` after scaling.
- Conditional on the open static target `||u_+||_(1,D) <= 21q^3/80`, proved
  that the linear position strictly dominates the global envelope for every
  `qk >= 3/50`. The scalar comparison has exact rational slack
  `1667/625000` at the transition.
- Reduced the whole earlier nonlinear interval exactly to scaled residual
  half-retention `X_k^lin-X_(k-1)^lin/2 >= 0`. This implication bootstraps raw
  positivity, projection inactivity, nonpositive post residual, and zero safe
  correction from the proved first-average sign.
- Proved that the remaining short-window operator
  `(J_k-J_(k-1)/2)L` has line coefficient
  `(1/2)Pr(Bin(k,1/2)>=|r|)`, and gave its exact folded path formula and
  standard moving-source response. A global quarter-mass bound is impossible:
  at `k=2`, reflection gives degree-normalized coefficient `3/8` for path
  target zero and source one.
- Sharpened the final derivative-source variation to `TV(epsilon)<1/300` by
  an exact sixteen-cell rational certificate. This raises the shared final
  correction margin to `16649/230400` and proves the literal entry bound
  `c(j)<-13q^3/100` on every full-face row. Consequently the separate
  sufficient early convolution target is now `T_k d<=13q^3/200` for
  `qk<3/50`; that finite inequality remains open.
- Proved the correlated stopped leading baseline. The exact folded deletion
  coefficient obeys an axis-plus-Pascal inequality
  `Shat_(m,k,r)>=2t_k(r)`; retaining the single antipodal endpoint group gives
  `Q_k^circ>=31/320` on every row for `1<=k<m`.
- The logarithmic terminal block remains conditional. No claim is made for
  other algorithms, recurrences, or implicit response primitives.

## Remaining interfaces

1. Prove the local endpoint half-ratios for `d-h` (or another proof of the
   static `21/80` target).
2. Absorb the finite-`q` source variation, mass, and endpoint remainder into
   the proved correlated `31/320` stopped baseline through `qk<3/50`.

The coordinate-error monotonicity shortcut was checked and refuted: a newly
enlarged restricted optimum can make an old coordinate error more negative.
It is not used anywhere in the package.

## Verification

- `verify_regime_reduction.py` checks every new rational constant with exact
  `Fraction` arithmetic and labels early half-retention open.
- `verify_early_kernel.py` checks the exact Laurent/tail formula, moving-source
  identities, folded-cycle replay, and the `3/8` reflection obstruction. Its
  larger short-window checks are labeled finite measurements.
- `verify_correction_margin.py` checks the sixteen-cell variation certificate,
  the improved final-prefix ledger, the exact two-row entry defect, and every
  rational constant in the `c<-13q^3/100` theorem.
- `verify_stopped_baseline.py` checks the exact folded axis and Pascal
  propagation, the central-binomial coefficient bound, endpoint scalar
  bounds, and stopped-versus-continued leading comparison.
- The consolidated `verify.py` retains the exact chronology, changing-face,
  directional packet, position-profile, velocity-profile, and static-tail
  preflights.
- Final clean build, focused verifier, repository audits, and diff checks are
  recorded in `STATUS.md`.

## Next action

Prove the local static comparator and the early half-retention convolution.
The proved late comparison then closes the remainder of the stated horizon.
