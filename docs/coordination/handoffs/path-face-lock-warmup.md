# Handoff: path-face-lock-warmup

- Branch: `agent/codex/path-face-lock-warmup`
- Base commit: `4a979a6907880fb2dc76d1c51dbb7d12dc8bd5b3`
- Write scope: `manuscript/notes/path_face_lock_warmup/` and this handoff.
- Shared files changed: this handoff only, as explicitly permitted.

## Current result

The exact Fable entrance gate has been mapped into source-aligned normalized
residual variables. On a fixed face, `y_(t+1)=M u_t` with
`M=kappa(Q_S+kappa I)^(-1)` and
`u_t=(1+beta)y_t-beta*y_(t-1)`; no-triggering is exactly `u_t>=0`.
The existing transported-center path profile uses a different recurrence, so
its estimates cannot be imported without a new entry calculation.

The note-local rational screen gives two proved route stops. On full `P4`
at `q=1/8`, one stable-face prox solve has endpoint trigger
`(U_2)_(00)=-541/48000`. On full `P8` at `q=1/16`, two solves have the exact
negative endpoint fraction in Proposition `prop:path-lock-cone-witnesses`.
Thus neither one nor two solves is sufficient uniformly over every
nonnegative entrance residual. These basis-column witnesses are not claimed
reachable by the changing-face endpoint-seeded RPPR trajectory.

## Claim routing

- Ledger candidate: exact trigger reconstruction and the two cone-uniform
  warmup refutations.
- Refuted route to broadcast: do not infer actual path safety from `Y>=0`
  alone after one or two prox solves.
- Formal dependencies remain `aesp_cd_l1_rppr` and
  `path_terminal_modal_block`; no registry edit is requested.
- Next falsifiable target: calculate the realized prefix-admission residual
  profile and prove or refute an all-time constant warmup on that narrower
  state class. Only then couple arms through a spider center.

## Verification

- Exact: `python3 verify_warmup.py --sizes 4 6 8 10 12 --horizon 32`
- Exact: `python3 verify_warmup.py --sizes 14 16 20 --horizon 64`
- Remaining checks are recorded in `STATUS.md` as they are run.
