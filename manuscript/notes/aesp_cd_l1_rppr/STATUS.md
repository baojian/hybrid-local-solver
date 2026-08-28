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
  square-energy and a joint correction/surviving-momentum truncation-energy
  ledger, a reachable K8 pulse, the
  actual-finite lagged Euclidean reserve, the K2/K8 boundary for the simplest
  lagged unsplit bank, and a root-potential finite-inner recursion with exact
  additive error `sqrt(kappa_A)*xi_t`. The latter strengthens the conditional
  polish from a `theta` scale to a `sqrt(theta)` scale without a support or
  fixed-face assumption. On the exact settled optimal face, the
  cross-normalized bank `B_t=||e_t||^2+(kappa_A+alpha)<u_t,Q_A^-1 u_t>`
  contracts by `1-q` at every correction-free stage and gives constant
  contraction after a `Theta(1/q)` post-full window. A reachable `K_N` family
  proves that high-band net decrease alone needs coefficient `Omega(N)` to
  pay its low forcing. In the positive direction, an exact contract-or-spend
  window pays every correction pattern from a telescoping Stieltjes bank, and
  after multiplication by `mu_E` from the low Euclidean endpoint drop. A
  rational-interval `P24` certificate proves that a split payment using net
  high-band drop plus `6/5` times the starting low bank is still insufficient.
  The certified necessary coefficient exceeds `1.206959416`. A
  Moreau-Hessian event bank has uniformly conditioned forcing and gives an
  exact nested-face epoch-restart ledger: boundary face gains and disjoint
  correction masses enter additively in root potential with geometric epoch
  weights. The protocol expands only at epoch boundaries, keeps the primal
  point fixed, and explicitly restarts momentum; it is not the unchanged
  automatic-admission trajectory. Retaining the correction cross term gives
  an exact signed increment whose positive part has a telescoping Stieltjes
  payment without the geometric `1/q` loss. This refines the epoch ledger to
  count only harmful signed events. A reachable `P3` event makes the signed
  increment positive and increases the bank, while the reachable `K8` family
  makes the signed payment asymptotically tight. A settled `S5` trajectory
  has adjacent positive partial/full events and a strict two-stage bank
  increase, refuting a universal one-step quiet gap.  Conversely, on every
  graph family with a proved clipped-master inequality the mean-free Moreau
  bank contracts by a factor at most `3/8` in `ceil(log(2)/q)` exact
  fixed-face stages, regardless of event density. This high-root recursion
  survives finite inner solves under an explicit geometrically discounted
  residual budget. The constant mode obeys an exact overshoot-or-high-trigger
  dichotomy: the overshoot branch contracts its Moreau bank by `1-q`, and the
  other branch can inject mean only when the mean-free trial residual is
  large in infinity norm. A same-point-restart two-scale potential combining
  the master high root and the forced mean contracts below `0.407` on a quiet
  `ceil(2/q)` epoch, and by `3/4` whenever the observable weighted mean deficit
  is at most one quarter of its starting value. A sharper low-root formulation
  works from arbitrary history: its recorded correction-mean gate halves the
  two-scale potential in `ceil(2/q)` transitions and has a finite-inner
  version with an explicit residual budget. An observable pure-prox alignment
  warmup contracts the high/mean residual ratio by `(1+q)^(-J)`; after a
  computable threshold, a same-point restart launches a permanently
  correction-free exact momentum tail. Its warmup is `O(1/q)` up to
  logarithms and requires no lower eigendata. The reachable `K_N` family
  also gives the exact high-to-low STOP
  `q*Xi_low/C_high>(N-1)/15`, so no graph-uniform high-bank coefficient can
  pay that deficit. A
  direct accelerated terminal result holds on the a-posteriori
  high-Dirichlet class. An exact full-face `P96` trajectory shows that the
  ungated total Moreau bank can retain more than `0.54` after `1/q`
  transitions, so a raw universal half-window cannot replace the accepted
  gate. On a fixed certified face, signed-scratch Chebyshev iteration followed
  by a Stieltjes retraction and maximum with the old lower checkpoint gives a
  safe published point in
  `O_tilde(vol(A)/sqrt(lambda_lower))` work. Once the final RPPR face is
  certified, applying this directly to the unshifted restricted system gives
  `O_tilde(1/(rho*sqrt(alpha)))` terminal work. A positive-coefficient
  polynomial theorem proves that requiring all scratch residuals to remain
  coordinatewise nonnegative reverts to condition-number rather than
  square-root dependence. A high-multiplicity Stieltjes cluster also stops
  every graph-independent fixed-rank low-mode deflation of the master-gap
  condition; a two-node exact witness has `Psi=2/25>0`.
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
  one-step `1-cq` contraction of the simplest lagged unsplit bank, and every
  graph-uniform constant payment of cross-normalized low forcing using only
  signed/net high-band decrease, as well as the coefficient-`6/5` split
  payment using the starting low bank on a settled path window, and raw
  half-contraction of the total Moreau bank in every settled `1/q` window,
  as well as square-root acceleration by residual polynomials whose every
  scratch state preserves the nonnegative cone, and fixed-rank repair of the
  clipped-master spectral gap.
- **Open:** A graph-uniform net exponent for low-Dirichlet optimal faces using
  a windowed spectral, nonlinear, or differently normalized transfer that
  retains finite residuals and coordinatewise positive-part mixing.

## Central blocker

Entry-dominated corrections and finite-created one-sided excess are charged,
and persistent-row controller, correction, and surviving-momentum energies
telescope. The exact Euclidean collateral reserve nevertheless has only
`q^2` graph-uniform drift. A coefficient large enough to pay the reachable K8
pulse makes the corresponding unsplit lagged bank fail stagewise accelerated
contraction on a reachable K2 low mode. The cross-normalized bank removes that
one-step drift, but the reachable `K_N` family shows that its low forcing
cannot be paid by high-band net decrease with a dimension-free coefficient.
The event-level contract-or-spend theorem pays it from low Euclidean progress,
but freezing that endpoint resource into a static `q^-1` reserve would restore
the K2 slow drift. The missing object is a restart/window accounting that
spends this resource only at correction events and survives face changes and
finite residuals. Equivalently, the remaining transfer must be windowed or nonlinear
rather than a fixed additive reserve. The Moreau epoch ledger removes the
`q^-2` face shock and avoids double counting, but still requires a bound on its
geometrically weighted face-gain and harmful signed-event injections. The
generic signed Stieltjes account improves the correction convolution but can
still permit `O(1/q)` bad windows. The master/mean split removes the high
component of this ambiguity and identifies one precise remaining term: the
discounted mean deficit in the non-overshoot/high-trigger branch. The `K_N`
family rules out paying it by a dimension-free high-energy reserve, so the
missing extra factor must use an infinity/local/volume-sensitive controller
certificate or an adaptive accepted-window rule rather than only
`0<=r_t<=beta*d_t`. Accepted fixed-full-face windows and the exact alignment
tail are now accelerated; what remains graph-uniformly open is the number and
cost of failed gates, changing-face transfer, and relative finite-inner
maintenance. There is
still no graph-uniform exact accelerated solver.

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
  `prop:aesp-cd-cross-normalized-bank`,
  `prop:aesp-cd-kn-cross-bank-stop`,
  `prop:aesp-cd-cross-normalized-contract-spend`, and
  `prop:aesp-cd-p24-low-start-stop`,
  `prop:aesp-cd-moreau-epoch-restart`, and
  `prop:aesp-cd-moreau-signed-event`,
  `prop:aesp-cd-p3-positive-signed-event`, and
  `prop:aesp-cd-psi-high-window`, and
  `cor:aesp-cd-psi-high-finite`,
  `prop:aesp-cd-low-overshoot-trigger`, and
  `prop:aesp-cd-master-mean-epoch`, and
  `prop:aesp-cd-p96-full-face-window-stop`,
  `cor:aesp-cd-observable-two-scale-window`,
  `cor:aesp-cd-finite-two-scale-window`, and
  `prop:aesp-cd-observable-alignment-tail`, and
  `cor:aesp-cd-finite-alignment-tail`,
  `cor:aesp-cd-fixed-face-gate-align`,
  `thm:aesp-cd-safe-chebyshev-face`,
  `cor:aesp-cd-final-face-chebyshev`, and
  `prop:aesp-cd-positive-polynomial-stop`, and
  `cor:aesp-cd-conditional-finite-acceptance`.
- Next concrete action: use the safe accelerated face primitive inside a
  batched active-set discovery protocol, pack proper-face event charges, and
  charge spectral certification and boundary restarts.
- Stop/go test: Go if the actual finite sequence has a declared
  graph-uniform net exponent and all residual charges fit the absolute polish.
  Stop if the proof erases the correction, treats the unknown optimum as an
  algorithmic certificate, commutes positive part with spectral projectors,
  or iterates ambient retraction Lipschitzness.

## Verification

- Source pointers checked: `README.md`, `main.tex` and included sections,
  `registry.toml`, `docs/research_notes.md`, the acceleration literature note,
  and shared ledgers.
- Focused checks: Eleven exact audits with durable `aesp_cd_l1_rppr.*` IDs cover
  the Round-022--032 mechanisms. Run them with `uv run python -m
  experiments.proof_audits.runner --tier full --note aesp_cd_l1_rppr`.
- Review status: Previous independent audits rederived each exact recurrence,
  constant, gate, and scope boundary. This reorganization changes no theorem,
  equation, or evidence classification.
- Known gaps: The P4 theorem has no finite-inner work conclusion. The
  contract-or-spend theorem is exact and restricted to the settled optimal
  face. The Moreau theorem crosses only explicit epoch-boundary admissions and
  still lacks event packing. The high half of the master/mean split has a
  finite-inner transfer; the forced mean and changing-face parts do not yet
  form an end-to-end finite solver theorem.
  No graph-uniform exact accelerated solver or finite-precision result follows.
