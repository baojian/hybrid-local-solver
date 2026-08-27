# Direction status: path_face_lock_warmup

Last reviewed: 2026-08-27
State: proved-open
Agent family: codex
Role: direction
Branch: `agent/codex/path-face-lock-warmup`
Base commit: `4a979a6907880fb2dc76d1c51dbb7d12dc8bd5b3`
Allowed write scope: `manuscript/notes/path_face_lock_warmup/` and `docs/coordination/handoffs/path-face-lock-warmup.md`

## Exact question and contract

- **Question:** Can the safe proximal warmup after a face lock be bounded
  independently of path length, or at worst logarithmically, before momentum
  becomes componentwise safe?
- **Model:** Source-aligned RPPR on endpoint paths, followed by symmetric
  spiders if the path mechanism survives.
- **Accuracy namespace:** Note-scoped componentwise KKT and face-retraction
  certificates; no repository-wide stopping-rule identification.
- **Access and charged work:** Adjacency-list sweeps are charged by scanned
  degree; exact inverse and spectral-oracle costs must be reported separately.
- **Intended result:** A proved warmup theorem, a correct weaker structural
  condition, or an explicit counterexample to graph-size-independent warmup.

## Claim ledger

- **Source:** The Fable face-lock construction and the project path
  position/velocity profiles motivate the question. Fable's `Proved-draft`
  labels are treated as pending independent audit rather than imported proof.
- **Proved here:** The exact normalized fixed-face residual/trigger mapping is
  `y_(t+1)=M u_t`, `u_t=(1+beta)y_t-beta*y_(t-1)`, with
  `M=kappa(Q_S+kappa I)^(-1)`. The Fable sharp componentwise condition is a
  sufficient absolute high-mode bound, stronger than `u_t>=0`. Exact cone
  witnesses refute one stable-face prox solve on `P4,q=1/8`, two on
  `P8,q=1/16`, and three on `P46,q=1/92`. The endpoint trigger entries are
  respectively `-541/48000` at momentum time 2, the exact negative fraction
  displayed in Proposition `prop:path-lock-cone-witnesses` at time 3, and an
  exact negative rational at time 4 whose full reduced value is printed by
  the verifier. For every graph face and `alpha<=1/5`, one stable-face prox
  solve nevertheless certifies the immediately following first momentum
  trigger; this follows from the entrywise Neumann bound
  `M>=I/2`. Repeating one prox and one momentum stage is safe but has full-face
  Perron multiplier `(1-q)^2(1+2q)=1-Theta(q^2)`, hence needs
  `Theta(q^-2)` pairs for constant contraction and is not accelerated.
- **Conditional:** None yet.
- **Measured:** The exact finite screen at `q=1/(2n)` finds first
  horizon-passing values `J=2` on `P4,P6` and `J=3` on
  `P8,P10,P12,P14,P16,P20`, through 32 or 64 momentum stages. A finite exact
  pass is not an all-time theorem.
- **Refuted:** Any proof that claims one, two, or three pure-prox solves make every
  nonnegative path-face residual permanently safe. This is a cone-uniform
  proof-route stop, not a reachability or actual-trajectory counterexample.
- **Open:** A graph-size-independent warmup bound on the realized
  endpoint-seeded changing-face path trajectory; the all-time kernel question
  for larger constants; and the spider junction extension.

## Central blocker

Characterize the actual residual profile after a prefix admission and one
stable-face prox solve. The full nonnegative cone is too broad, while the
existing transported-center path profiles concern a different recurrence and
cannot be imported directly.

## Dependencies and reusable outputs

- Formal registry dependencies: `aesp_cd_l1_rppr`, `path_terminal_modal_block`.
- Source/shared prerequisites: source-aligned RPPR definition.
- Context/provenance: Fable iteration-7 notes are read-only exploratory evidence.
- Reusable outputs: exact trigger-kernel recurrence and a note-local rational
  falsification screen with explicit basis-column witnesses.
- Supplies to: safeguarded acceleration and spider-generalization directions.

## Resume here

- Exact file/section/lemma: `main.tex`, Sections
  `sec:gate-reconstruction`, `sec:cone-screen`, and `sec:path-spider-targets`.
- Next concrete action: derive the actual endpoint-prefix admission residual
  row by row, then test/prove its one-warmup trigger sequence; separately test
  whether the full-cone first-pass constant remains bounded at larger sizes.
- Stop/go test: prove an all-time constant for the realized profile, or give
  an exact reachable family whose minimal safe warmup grows.

## Verification

- Source pointers checked: Fable I6-A2 Sections 1--4 and I7-A Sections 1--2;
  sibling path modal note exact recurrence and claim boundary.
- Focused exact checks: `verify_warmup.py` passed its P4--P20 screens and
  reproduced the P4/P8 fractions and the P46 exact negative sign.
- Known gaps: finite horizon passes are not all-time proofs; the basis-column
  cone witnesses are not claimed reachable; spider coupling has not yet been
  analyzed.

## Repository handoff

- Provider-owned paths changed: none.
- Shared paths changed: none in the direction branch.
- Assignment state: active.
