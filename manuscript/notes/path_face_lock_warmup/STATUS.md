# Direction status: path_face_lock_warmup

Last reviewed: 2026-08-28
State: proved-open
Agent family: codex
Role: direction

## Exact question and contract

- **Question:** Can the safe proximal warmup after a face lock be bounded
  independently of graph size, or at worst logarithmically, before momentum
  becomes componentwise safe?
- **Model:** Source-aligned RPPR on endpoint paths and symmetric spiders.
- **Accuracy namespace:** Note-scoped componentwise KKT and face-retraction
  certificates; no repository-wide stopping-rule identification.
- **Access and charged work:** Adjacency-list sweeps are charged by scanned
  degree; exact inverse, state-write, and repeated-resolvent costs must be
  reported separately.
- **Intended result:** A proved warmup theorem, a correct weaker structural
  condition, or an explicit counterexample to graph-size-independent warmup.

## Claim ledger

- **Source:** The Fable face-lock construction and project path profiles
  motivate the question. Fable's `Proved-draft` labels are not imported.
- **Proved here:** The exact fixed-face residual recurrence is
  `y_(t+1)=M((1+beta)y_t-beta*y_(t-1))`, with
  `M=kappa(Q_S+kappa I)^(-1)`. For every graph face and `alpha<=1/5`, one
  pure-prox solve certifies the immediately following first momentum trigger
  by the entrywise bound `M>=I/2`. A reset after any fixed safe momentum burst
  has Perron contraction only `1-Theta_L(q^2)` and is not accelerated. Exact
  cone witnesses refute one, two, and three warmups on full endpoint paths and
  four on a full 16-arm star. More strongly, for every fixed integer `J>=1`,
  the leaf-seeded unit-star family
  `q_B=1/[2(B+1)]`, `rho_B=1/(4B)` reaches the full face at state four and has
  a negative seeded-leaf second momentum trigger for every sufficiently large
  `B`. Thus there is no universal constant warmup for this reachable policy.
  Conversely, on any supplied full `B`-star face, the cone-uniform choice
  `J_B=max{3,1+ceil(log_(3/2)(8(B-1)))}` makes every later trigger kernel
  entrywise nonnegative. This is an exact logarithmic full-face theorem.
- **Conditional:** None.
- **Measured:** The finite exact path screens record horizon passes only; they
  are not all-time theorems.
- **Refuted:** Constant post-lock warmup for the specified reachable star
  policy; cone-uniform one-to-three warmups on the registered paths; four on
  full stars; and fixed-burst/reset acceleration of the Perron mode.
- **Open:** A graph-size-independent statement for the realized endpoint-path
  chronology; finite-inner margins for the logarithmic star theorem; unequal
  arms, proper changing faces, and a locally charged resolvent implementation.

## Central blocker

For paths, the actual residual profile after prefix admission is not yet
characterized. For spiders, the exact full-star scale is now logarithmic, but
the entrywise margin may shrink and the resolvent cost is not local merely
because the face is exposed. A finite-inner changing-face theorem must retain
both effects.

## Dependencies and reusable outputs

- Formal registry dependencies: `aesp_cd_l1_rppr`, `path_terminal_modal_block`.
- Source/shared prerequisites: source-aligned RPPR definition.
- Reusable outputs: exact trigger-kernel recurrence; rational path/star cone
  witnesses; exact spider junction and volume formulas; a three-class exact
  reachable-star LCP verifier; a no-constant reachable family; and a
  cone-uniform logarithmic star warmup.
- Supplies to: safeguarded acceleration and spider-generalization directions.

## Resume here

- Exact file/section/lemma: `main.tex`, especially
  `sec:reachable-star-family`, `thm:reachable-star-no-constant`, and
  `thm:star-logarithmic-warmup`.
- Next concrete action: quantify the minimum entrywise margin under the
  logarithmic warmup and compare it with the finite inner residual; separately
  derive the actual endpoint-prefix admission profile.
- Stop/go test: go if a finite-inner margin and charged repeated solve retain
  the logarithmic safeguard; stop if the required margin or state materialism
  costs more than the target local budget.

## Verification

- `verify_warmup.py` reproduces the exact registered path and cone-star
  witnesses.
- `verify_reachable_star.py` uses exact `Fraction` arithmetic and a three-class
  LCP mask enumeration. Its default `B=50,J=6` case reaches full state four,
  has a nonnegative first momentum trigger, and reproduces the exact negative
  seeded-leaf fraction at stage 11. `B=22,J=6` independently fails at stage 12.
- The reachable-family derivation and default exact fraction were independently
  rederived from the three-class recurrence and spectral polynomial.
- Known gaps: the fixed-`J` limit is not a uniform lower bound for `J(B)`;
  finite path horizon passes are not all-time; and the logarithmic theorem is
  exact, full-face, and inverse-cost agnostic.

## Repository handoff

- Provider-owned paths changed: none.
- Shared paths changed: none in this direction update.
- Assignment state: active under `windowed-spectral-lyapunov-7h`.
