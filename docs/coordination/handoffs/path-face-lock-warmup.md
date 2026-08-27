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

A graph-uniform Neumann-series lemma now proves a narrower positive result:
for `alpha<=1/5`, one stable-face prox solve certifies the immediately next
momentum trigger on every face. It does not certify the tail. More generally,
one prox followed by any fixed safe burst of `L` momentum stages and a reset
has exact full-face Perron multiplier
`(1+(L+1)q)(1-q)^(L+1)=1-Theta_L(q^2)`, so every fixed-burst/reset fallback
loses acceleration.

The note-local rational screen gives exact path and spider route stops. On full `P4`
at `q=1/8`, one stable-face prox solve has endpoint trigger
`(U_2)_(00)=-541/48000`. On full `P8` at `q=1/16`, two solves have the exact
negative endpoint fraction in Proposition `prop:path-lock-cone-witnesses`.
An additional exact `P46,q=1/92` witness has
`(U_4^(3))_(00)<0`, so neither one, two, nor three solves is sufficient
uniformly over every nonnegative entrance residual. These basis-column witnesses are not claimed
reachable by the changing-face endpoint-seeded RPPR trajectory.

The spider extension is now explicit rather than formal: the note gives the
normalized center and arm resolvent rows and the exact charged prefix volume
`B + sum_(r_a>0) (2r_a-1_{r_a=ell_a})`. The first-momentum theorem has no
arm-count loss. The tail does: on the 16-arm unit star at `q=1/34`, the exact
leaf diagonal after four warmups is
`(U_1^(4))_(11)=-17140927690425/914326479306752`. Thus the second consecutive
momentum trigger fails for a nonnegative basis residual.

## Claim routing

- Ledger candidate: exact trigger reconstruction, graph-uniform first-stage
  entrance, fixed-burst/reset rate stop, and path/star cone refutations.
- Refuted route to broadcast: do not infer actual path or spider tail safety
  from `Y>=0` alone after a fixed small number of prox solves.
- Formal dependencies remain `aesp_cd_l1_rppr` and
  `path_terminal_modal_block`; no registry edit is requested.
- Next falsifiable target: calculate the realized prefix-admission residual
  profile and prove or refute an all-time constant warmup on that narrower
  state class; derive the realized center/arm profile after a spider
  admission.

## Verification

- Exact: `python3 verify_warmup.py --sizes 4 6 8 10 12 --horizon 32`
- Exact: `python3 verify_warmup.py --sizes 14 16 20 --horizon 64`
- Exact: `python3 verify_warmup.py --sizes 46 --horizon 4 --max-warmup 3`
- Exact: `python3 verify_warmup.py --spider-arms 16 --spider-length 1 --horizon 2 --max-warmup 4`
- Remaining checks are recorded in `STATUS.md` as they are run.
