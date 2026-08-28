# Direction status: aesp_cd_l1_rppr

Last reviewed: 2026-08-29
State: proved-open

## Exact question and contract

- **Question:** Can the actual finite-inner safeguarded recurrence retain a
  net accelerated exponent after every residual, retraction, rekey, and
  terminal-gate charge?
- **Model:** Shared RPPR objective
  `F_rho=f+alpha*rho*||D^(1/2)x||_1` for `0<alpha<=1`. Shifted
  Catalyst/AESP uses `alpha<1/2` and `kappa_A=1-2alpha`; the frozen
  accelerated arm uses `alpha<1/4`, while the unshifted fallback covers
  `1/4<=alpha<=1`.
- **Accuracy namespace:** The terminal requirement is
  `R_KKT,rho(x)/alpha <= eps_kkt`; `eps_kkt` is not `eps_ppr`, `eps_obj`, or
  `rho`.
- **Access and charged work:** A coordinate update and affected-neighbor
  rekey cost `d_i`; envelope growth, retractions, KKT scans, repeated updates,
  validation, state writes, materialization, and output are charged.
- **Intended result:** An implementable oracle-free
  `O_tilde(1/(rho*sqrt(alpha)))` local-work theorem.

## Claim ledger

- **Source:** RPPR support/KKT facts and the Catalyst/AESP scaffold are source
  ingredients identified in the source map and opening formulation.
- **Proved here:** Weighted KKT contraction and solution certificates; the
  relative local inner oracle; safe lower retraction and fixed-envelope
  locality; exact safeguarded defect and inflation ledgers; collateral-clipping
  bounds; and finite residual interfaces. Exact trajectory results include the
  fixed-P4 infinite inflation cone, support-entry shielding, persistent-row
  square-energy and truncation-energy ledgers, a reachable K8 pulse, the
  actual-finite lagged Euclidean reserve, the K2/K8 boundary for the simplest
  lagged unsplit bank, and a root-potential finite-inner recursion with exact
  additive error `sqrt(kappa_A)*xi_t`. The latter strengthens the conditional
  polish from a `theta` scale to a `sqrt(theta)` scale without a support or
  fixed-face assumption. A direct accelerated terminal result holds on the
  a-posteriori high-Dirichlet class.
- **Conditional:** A graph-uniform net packing inequality for the actual
  finite sequence supplies computable outer horizon, polish, terminal gate,
  and cached-row resource vector. The large-`alpha` fallback is unconditional;
  the accelerated vector is not.
- **Measured:** None; all evidence in this note is analytical or exact
  arithmetic.
- **Refuted:** Raw objective-gap control at the L1 kink, pointwise momentum
  nonexpansion, support-addition-only correction charging, Euclidean-only
  collateral packing with `o(1/q)` coefficient, horizon-uniform inflation on
  the fixed P4 objective, black-box shadowing through retraction, and uniform
  one-step `1-cq` contraction of the simplest lagged unsplit bank.
- **Open:** A graph-uniform net exponent for low-Dirichlet optimal faces using
  a windowed spectral, nonlinear, or differently normalized transfer that
  retains finite residuals and coordinatewise positive-part mixing.

## Central blocker

Entry-dominated corrections and finite-created one-sided excess are charged,
and persistent-row controller, correction, and surviving-momentum energies
telescope. The exact Euclidean collateral reserve nevertheless has only
`q^2` graph-uniform drift. A coefficient large enough to pay the reachable K8
pulse makes the corresponding unsplit lagged bank fail stagewise accelerated
contraction on a reachable K2 low mode. This is not an additive-resistant
obstruction and does not refute global accelerated decay; the K8 high band is
compatible with payment. The missing object is a windowed or nonlinear
low/high transfer. Existing local identities do not supply a bound on that
transfer, so there is no graph-uniform exact accelerated solver yet.

## Dependencies and reusable outputs

- Formal registry dependencies: none.
- Source/shared prerequisites: Shared RPPR support/KKT facts and
  Catalyst/AESP source machinery.
- Supplies to: `volume_gated_acceleration`,
  `hybrid_local_solver_synthesis`, `response_preconditioned_hybrid`, and any
  direction needing safe lower centers or local KKT admission.

## Resume here

- Exact file/section/lemma: Start at
  `lem:aesp-cd-persistent-square-ledger`,
  `lem:aesp-cd-truncation-q-energy`, `prop:aesp-cd-k8-q-bank-stop`,
  `lem:aesp-cd-q-weighted-euclidean-reserve`,
  `eq:aesp-cd-finite-inner-root-potential`,
  `prop:aesp-cd-unsplit-q-energy-stagewise-stop`, and
  `cor:aesp-cd-conditional-finite-acceptance`.
- Next concrete action: Construct a spectrally split, windowed, nonlinear, or
  differently normalized `q^-1`-weighted Lyapunov that pairs persistent
  high-energy decay with Euclidean collateral while preserving accelerated
  low modes.
- Stop/go test: Go if the actual finite sequence has a declared
  graph-uniform net exponent and all residual charges fit the absolute polish.
  Stop if the proof erases the correction, treats the unknown optimum as an
  algorithmic certificate, commutes positive part with spectral projectors,
  or iterates ambient retraction Lipschitzness.

## Verification

- Source pointers checked: `README.md`, `main.tex` and included sections,
  `registry.toml`, `docs/research_notes.md`, the acceleration literature note,
  and shared ledgers.
- Focused checks: Six exact audits with durable `aesp_cd_l1_rppr.*` IDs cover
  the Round-022--027 mechanisms. Run them with `uv run python -m
  experiments.proof_audits.runner --tier full --note aesp_cd_l1_rppr`.
- Review status: Previous independent audits rederived each exact recurrence,
  constant, gate, and scope boundary. This reorganization changes no theorem,
  equation, or evidence classification.
- Known gaps: The abstract countermodel is not a claimed reachable outer
  state. The P4 theorem has no finite-inner work conclusion. The post-full
  filter is not a graph-uniform two-step separation and does not prove finite
  net packing. No graph-uniform exact accelerated solver or finite-precision
  result follows.
