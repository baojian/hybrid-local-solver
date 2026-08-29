# Direction status: aesp_cd_l1_rppr

Last reviewed: 2026-08-29
State: proved-open

## Exact question and contract

- **Question:** Can the actual finite-inner safeguarded recurrence retain a
  net accelerated exponent after every residual, retraction, rekey, and
  terminal-gate charge?
- **Model:** Shared RPPR objective
  `F_rho=f+alpha*rho*||D^(1/2)x||_1` for `0<alpha<=1`, with the oracle-free
  end-to-end target specialized to the point source `s=e_v`. Shifted
  Catalyst/AESP uses `alpha<1/2` and `kappa_A=1-2alpha`; the frozen
  accelerated arm uses `alpha<1/4`, while the unshifted fallback covers
  `1/4<=alpha<=1`.
- **Accuracy namespace:** The terminal requirement is
  `R_KKT,rho(x)/alpha <= eps_kkt`; `eps_kkt` is not `eps_ppr`, `eps_obj`, or
  `rho`.
- **Access and charged work:** A coordinate update and affected-neighbor
  rekey cost `d_i`; envelope growth, retractions, KKT scans, repeated updates,
  validation, state writes, materialization, and output are charged.
- **Intended result:** An implementable point-source oracle-free
  `O_tilde(1/(rho*sqrt(alpha)))` local-work theorem.
- **External regime reduction:** Wei--Yang (August 2026) gives a randomized
  point-source ACL approximation in `O_tilde(1/eps_ppr^2)` work.  Hence the
  intended target is already attained for `eps_ppr >= sqrt(alpha)`; the
  unresolved range is `eps_ppr < sqrt(alpha)`, equivalently
  `rho < sqrt(alpha)/2` under `rho=eps_kkt=eps_ppr/2`.  Their repeated
  active-SDD-solve implementation supplies finite one-sided boundary
  certificates, but the finite-gap radius-one fan proves that this strategy
  can genuinely take `Omega(1/eps_ppr^2)` work.  Dynamic reuse is still open.
  Classical APPR nevertheless returns an RPPR-support-containing envelope
  of volume at most `2/((1-alpha)rho)` by the
  Ha--Fountoulakis--Mahoney support sandwich.  Under a point source that
  envelope also has `O_tilde(1/sqrt(alpha))` radius.  Its worst-case work is
  tightly `Theta(1/(alpha*rho))`.  This separates the remaining question:
  an output-sized envelope exists, while its accelerated construction or
  dynamic reuse is still missing.
  The ordering-independent APPR star calibrates the distinction sharply:
  its envelope has radius at most one and volume `Theta(1/rho)`, yet APPR
  spends `Omega(vol(E)/alpha)` work on it.
  Supplied as an oracle, that APPR envelope immediately supports a standard
  accelerated proximal solve for a general sparse source with semantic work
  `nnz(s)+O_tilde(1/(sqrt(alpha)*eps_ppr))`, without any strict active/dual
  margin.  The same square-root radius holds from a general source set;
  point-source structure is needed to make discovery a single rooted trace.
  Well-separated source components nevertheless decompose exactly at scaled
  thresholds `rho/s_v` and retain total volume at most `1/rho`; only shared
  inactive rows and the mergers they trigger obstruct that additive result.
  Conditional on the same exhaustive route-output locator, those mergers are
  nevertheless handled with only additive source-read work, so this one
  unresolved interface would close the general sparse-source target as well.
  The persistent source-plus-frontier candidate universe is bounded by
  `nnz(s)+2vol(S*)`; only implicit old-coordinate response updates remain.
  Ordinary-PPR screening is likewise source-independent but sharp only at
  the classical `alpha*rho` threshold and `1/(alpha*rho)` volume.
  The response stream remains energy-orthogonal with total energy at most
  `alpha/2` for every source distribution; only the sharper `alpha/(2d_o)`
  constant is point-source-specific.  The normalized response columns form
  an exact inverse factorization of the terminal principal matrix, exposing
  the missing locator as an online thresholded inverse-Cholesky reporter.
  The fixed-envelope terminal branch also bypasses the proper-face
  constant-vector identity that limits the separate Perron-window branch.
  Thus the oracle-free theorem has been reduced exactly to accelerated
  envelope construction (or an equivalent output-sensitive event locator).
  Point-source structure is not closed under residual recursion: even the
  exact root-only solve on `P3` leaves two positive residual sources.
  The apparent stronger point-source literature does not close this range:
  ICDT 2024 restores to linear `1/alpha` dependence and assumes global
  preprocessing; ChebyPush proves `K^2/eps_ppr` work under a stability
  assumption; and the 2026 FISTA result has an accelerated core only under
  confinement plus a `sqrt(vol(B))/(rho*alpha^(3/2))` boundary term.
  Finite KKT hysteresis nevertheless removes the unknown key-margin promise:
  when `rho=eps_kkt`, constant-ratio downward coordinate levels classify
  every boundary row as either a safe positive pivot or already within the
  terminal KKT band.  The explicit event processing is soft-linear; emitting
  those level crossings from compressed changing-face state remains open.
  An exact pivot raises the old solution by a killed hitting-probability
  column, so the missing operation is now a precise harmonic threshold event:
  report every coordinate whose pivot increment crosses its next finite
  level.  The union of original frontier candidates has at most
  `2*vol(S*)` rows and is exposed by one scan of each admitted row.  Hence
  neither candidate count nor frontier incidence discovery is the remaining
  obstacle; the unclosed part is compressed emission of the harmonic level
  events.

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
  `O_tilde(1/(rho*sqrt(alpha)))` terminal work. More generally, a margin-free
  clip-or-pay retraction publishes a lower-safe approximation to a fixed
  envelope's obstacle minimizer after accelerated projected-gradient scratch.
  This implements the speculative-envelope obstacle primitive in
  `O_tilde(vol(U)/sqrt(alpha))` work; explored volume, exact-zero boundary
  decisions, scratch exposure, and dynamic reporting remain separate.  A
  two-coordinate exact witness shows that standard critically tuned projected
  acceleration can activate a coordinate outside the true obstacle support,
  so safe publication does not make unrestricted scratch support-local.  For
  the point-source load, every nonzero obstacle subsolution is nevertheless
  connected and contains the root.  Linear PPR superposition gives a
  general-seed corollary with the sharp allocation factor
  `(sum_v sqrt(s_v))^2`, not the old additive `nnz(s)` target.  This scope
  reduction does not make exact support discovery radius-bounded: a fan
  family whose entire graph has point-source radius one requires
  `m/2-1` nonempty all-positive batches.  A three-vertex point-source witness
  also has an active obstacle coordinate where the unconstrained shifted-PPR
  coordinate is strictly negative, stopping a direct superlevel-set recovery.
  The fan STOP is only for exact support: its root-only point already meets
  the matched finite diagnostic `eps_kkt >= rho`, so it does not obstruct the
  standard finite PPR target at that tuning.  A second exact fan tuning,
  `alpha=1/4` and `rho=eps_kkt=1/(10m)`, restores exactly `m/2` paired
  finite-significance batches.  Re-solving/scanning every growing face then
  costs `Omega(m^2)=Omega(1/epsilon^2)` despite radius one.  This strictly
  stops the repeated-full-SDD-solve implementation, not dynamic reuse.
  Point-source rho-homotopy constrains each face update to a nonnegative
  rank-one mixture of boundary breakpoint pairs; all surviving breakpoints
  move toward the admitted maximum.  Nevertheless an exact six-vertex trace
  reverses two surviving candidates' order, so a stale scalar heap does not
  close the reporter.
  Maintaining the full sparse exterior Schur complement nevertheless yields
  an exact ratio-pivot support homotopy: every support row is scanned and
  admitted once, terminal KKT is exact, and discovery costs
  `O_tilde(vol(S*)+sum_w(1+delta_w)^2)` in the realized Schur-fill degrees.
  Hence bounded homotopy width, followed by the certified final-face
  Chebyshev solve, meets the point-source product target.  This is not
  graph-uniform because explicit root/fill cliques can be quadratic.
  At a fixed target `rho`, the implementation contract is strictly simpler:
  a single exterior residual `g=A-rho*B` obeys the same nonnegative Schur
  pivot update, any certified-positive row may enter, and a one-sided
  `O(alpha*eps_kkt*d_v)` upper interval gives a finite KKT stop.  The
  point-source negative off-root load makes row-on-first-pivot discovery
  complete without a global scan.  Positive exterior residual mass is
  nonincreasing and starts below `alpha`, so at most `1/eps_kkt` rows are
  simultaneously finite-significant.  Its sharpened Schur-row-sum decrease
  also bounds the sum of all admitted block-pivot residuals by
  `(1-alpha)/2`; lifetime update/reporting cost remains open.  In
  degree-unscaled coordinates the point-source obstacle is also
  exactly a dissipative divisible-sandpile odometer: its vector is the
  coordinatewise least stabilizer and every fair legal full-toppling order
  converges monotonically to it.  This provides a rooted Abelian process, but
  its direct work bound remains `O(1/(alpha*eps_kkt))`; the Schur pivot is the
  block-toppling primitive whose compressed maintenance is still missing.
  Equivalently, each Schur residual multiplier is the killed PageRank walk's
  first-exit law through the current active face.  This gives an implicit
  harmonic sampler for dense fill, but literal exit sampling still has
  `O(1/alpha)` expected path length and is not the missing square-root
  acceleration.  The primal response to the same pivot is another exact
  killed-walk object: its old-coordinate increment is the pivot amount times
  the probability of hitting the new row before killing or another exterior
  row.  This converts the finite reporter to a dynamic killed-harmonic level
  query.  The query is exhaustive and margin-free, but no graph-universal
  support-local implementation at square-root dependence is yet proved.
  Reversibility identifies the degree-weighted response with a killed
  excursion's expected occupation vector.  Pure nonnegative walk or push
  representations therefore remain on the classical geometric horizon;
  any square-root implementation must use a signed accelerated response
  internally while retaining one-sided publication.
  Successive exact face increments are pairwise orthogonal in the fixed
  Hessian energy, their total energy is at most `alpha/d_source`, and every
  coordinate obeys a Bessel bound `sum z_i^2/||z||_H^2 <= 1/(alpha*d_i)`.
  This turns the remaining query into heavy-hitter reporting for an
  orthogonal harmonic stream.  It is a structural gain, not yet an
  implementation, because forming the next response vector is itself the
  dynamic inverse problem.  A Chebyshev inverse-polynomial argument further
  shows that a pivot response decays as
  `(2/alpha)*lambda_alpha^(distance-1)` after degree normalization.  Every
  finite-level event is therefore confined to an
  `O_tilde(1/sqrt(alpha))` graph radius, even though literal killed-walk
  simulation has a `Theta(1/alpha)` horizon.  Ball volume and repeated
  overlap are not controlled by this radius, so this is an information-radius
  theorem rather than the missing work theorem.
  Approximate response arithmetic is no longer a separate blocker: a
  degree-weighted response residual gives simultaneous certified intervals
  for every coordinate, and summable per-pivot residual budgets fit inside
  the finite KKT hysteresis with only logarithmic accuracy overhead.  The
  unresolved operation is exhaustive event-coordinate location.
  Ordinary point-source PPR also gives a universal screen
  `S*(rho) subset {i:y0_i>alpha*rho/p}` of volume below
  `p/(alpha*rho)`.  This screen is sharp: on an explicit unweighted
  root--candidate--clique family an active coordinate has
  `y0_i/rho -> alpha/p`.  Thus a `rho*sqrt(alpha)` ordinary-PPR superlevel
  envelope, which would have closed the desired volume bound immediately,
  is false on general graphs.
  Combining the finite-level count with the hitting-radius lemma gives a
  sharp conditional closure: a dynamic locator whose total charge is one
  unit plus pivot-to-event distance per emitted level crossing has
  `O_tilde(vol(S*)/sqrt(alpha))` work.  The contract explicitly includes
  response-state maintenance, rejected queries, and empty outputs.  This is
  the current minimal point-source interface; named-coordinate dynamic
  solves and ordinary spectral vertex sparsifiers do not automatically
  instantiate its exhaustive one-sided reporter.
  Its breakpoint slope satisfies the graph-universal band
  `alpha*d_v <= B_v <= (1+alpha)*d_v/2`; hence a certified additive
  upper envelope on the remaining critical ratios gives a margin-free finite
  KKT stop.  Near-tied breakpoints need not be resolved exactly.  A rigorous
  interval interface now reduces this to coordinatewise pair errors of scale
  `O(alpha*eta*d_v)`.  Ordinary two-sided spectral Schur approximation alone
  is insufficient: an exact two-row witness is spectrally close to the
  identity but a literal approximate pivot erases a positive breakpoint.
  The missing universal bridge is therefore a rowwise one-sided certificate,
  not exact support or exact breakpoint ordering.
  A positive-coefficient
  polynomial theorem proves that requiring all scratch residuals to remain
  coordinatewise nonnegative reverts to condition-number rather than
  square-root dependence. A high-multiplicity Stieltjes cluster also stops
  every graph-independent fixed-rank low-mode deflation of the master-gap
  condition; a two-node exact witness has `Psi=2/25>0`. Forest dynamic-Schur
  messages now have an exact pinned/free audit and a finite-margin interval
  implementation whose precision is logarithmic in the KKT gap, output
  tolerance, message height, and condition number. A constant-condition
  tridiagonal family proves that explicit exact-rational messages can still
  require linearly many bits. Stable one- and two-port frontier responses
  admit near-linear kinetic reporters. Separately, the RPPR support cap yields
  a graph-uniform retained-envelope bound `2/rho` under an exact dynamic
  obstacle interface; the unresolved work is exposed as `W_DS(2/rho)`,
  including all serial updates and frontier reports. After final support
  closure, one same-point restart satisfies
  `C_rst <= 4(F(z)-F(x*))`, so discovery need not transport momentum or pay a
  `q^(-1)` face shock. On a promised single-source tree or unicyclic graph,
  an exact scalar threshold hierarchy closes the named-query term (with
  radius-paid cycle scans in the latter case) and reproduces a legal
  singleton positive-subset trace in
  `O_tilde((1+vol(S*))/sqrt(alpha))` work. The first structural reporter still
  open after the known tree, single-cycle, bounded-productive-site cactus, and
  bounded-block solvers occurs when unbounded ancestor cycles have unbounded
  productive descendant sites, and more generally on variable-port
  series--parallel graphs. Epoch rebuilding nevertheless gives the exact
  adaptive block tradeoff
  `O_tilde(L_B+J_B*min{p_B+1,sqrt(L_B)})`; its remaining
  square-root block factor is the current cactus gap, while the alternative
  route promise
  `max_v sum_{B in P(v)} min{p_B+1,sqrt(L_B)}=O_tilde(R*)` closes another
  strict subclass.  A small-`rho` connected-order lemma realizes the
  square-root gap on a strict legal RPPR singleton trace, so the flat
  scan-all-cuts rebuild proof is genuinely insufficient; this is not a lower
  bound against multilevel reporters or different batching.  A static-cluster
  model makes its square-root interface cost rigorous.  Objective gain alone
  also cannot pay admissions, although a declared Schur-key density gate
  makes accepted batch costs telescope exactly.  Indeed, a
  supplied final weighted HLD plus balanced SP parses closes the post-closure
  cactus route conditionally by rebuilding whole heavy paths; online
  construction is already soft-linear for an immutable contiguous core
  prefix.  Interleaved closure and response mutation, dynamic HLD
  cut/concatenate, and their bulk hull meld remain the exact missing
  interface. Under a uniform relative KKT margin,
  charged coordinate-level events give another soft-linear reporter; the
  event source remains an explicit interface cost.
  A primary-source interface check found logarithmic top-tree/dynamic-
  treewidth structural updates and global-frame dynamic convex-hull queries,
  including restricted simple-path concatenation, but no stated primitive
  combining hierarchical affine pullback, persistent hull meld/split, and
  strict labeled argmax.  Kinetic hulls allow bounded-complexity per-row
  trajectories and flight-plan changes, but not a single bulk update of all
  pulled-back rows in a Schur cluster.  This is a literature boundary, not a
  lower bound.
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

The active-set boundary is now explicit. A margin-certified batch of at
least `gamma*vol(A)` per restricted face yields total
`O_tilde(vol(S*)/(gamma*sqrt(alpha)))` work, but endpoint paths can expose
only one certified vertex at a time and force quadratic cumulative face
volume. Unrestricted full-graph Chebyshev scratch is not a workaround: a
regular-tree frontier can retain constant `l2` mass on exponentially many
coordinates. Same-point nested replay has sharp Moreau root-shock constant
`2` (energy constant `4`). Thus the remaining universal ingredient must
either reuse state across serial admissions, grow a certified speculative
envelope, or provide an incremental propagation primitive between doubling
checkpoints.

The path case now supplies the first option exactly: append-only scalar
`LDL^T` messages process every singleton admission once and materialize only
the final solution.  For a general block expansion, the precise missing
operation is the old-face inverse response `H^(-1)C` plus incremental boundary
refresh.  On forests and supplied bounded-treewidth decompositions, dynamic
top-tree Schur summaries implement each named update/query in polylogarithmic
time, but a condition-free kinetic reporter bounding the total query count is
still missing on general interfaces. Stable fixed ports of dimension at most
two are closed by threshold/planar-hull reporters. A hard inactive-halo guard
proves that retained RPPR volume `2/rho` always suffices, but a universal
accelerated theorem still requires
`W_DS(B)=O_tilde(B/sqrt(alpha))`. A speculative coordinate envelope supplies the second option only
in explored-volume form; strict active/dual margins make its obstacle solve
accelerated, while inactive high-degree halo prevents replacing explored
volume by final support volume without another guard or oracle.

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
  `prop:aesp-cd-polynomial-scratch-spill-stop`,
  `prop:aesp-cd-face-by-face-volume-stop`,
  `prop:aesp-cd-geometric-face-batches`,
  `prop:aesp-cd-incremental-schur-response`,
  `prop:aesp-cd-dynamic-schur-forest`,
  `prop:aesp-cd-dynamic-schur-precision`,
  `cor:aesp-cd-stable-port-reporter`,
  `thm:aesp-cd-tree-singleton-threshold`,
  `cor:aesp-cd-unicyclic-singleton`,
  `cor:aesp-cd-cactus-live-sites`,
  `cor:aesp-cd-cactus-productive-sites`,
  `cor:aesp-cd-cactus-productive-epochs`,
  `lem:aesp-cd-connected-order-small-rho`,
  `prop:aesp-cd-objective-gain-charge-stop`,
  `cor:aesp-cd-schur-gain-batch-payment`,
  `prop:aesp-cd-cactus-static-cluster-stop`,
  `prop:aesp-cd-cactus-offline-hld`,
  `prop:aesp-cd-two-port-direction-stop`,
  `prop:aesp-cd-sp-meld-hull-reduction`,
  `lem:aesp-cd-two-port-projective-pullback`,
  `cor:aesp-cd-slope-separated-projective-meld`,
  `cor:aesp-cd-projective-separation-guard`,
  `cor:aesp-cd-ratio-pivot-finite-stop`,
  `prop:aesp-cd-sparse-source-radius`,
  `prop:aesp-cd-separated-source-decomposition`,
  `cor:aesp-cd-point-source-coarse-regime`,
  `prop:aesp-cd-point-source-appr-envelope`,
  `cor:aesp-cd-point-source-appr-envelope-oracle`,
  `cor:aesp-cd-appr-envelope-oracle`,
  `cor:aesp-cd-sparse-source-route-output-interface`,
  `cor:aesp-cd-point-source-fixed-target-pivot`,
  `prop:aesp-cd-point-source-dissipative-sandpile`,
  `lem:aesp-cd-point-source-residual-mass`,
  `lem:aesp-cd-point-source-frontier-universe`,
  `prop:aesp-cd-point-source-hitting-column`,
  `lem:aesp-cd-point-source-hitting-radius`,
  `cor:aesp-cd-point-source-route-output-interface`,
  `lem:aesp-cd-point-source-response-residual-certificate`,
  `prop:aesp-cd-point-source-orthogonal-pivots`,
  `prop:aesp-cd-point-source-ppr-screening`,
  `cor:aesp-cd-fan-finite-stop`,
  `prop:aesp-cd-fan-finite-linear-batches`,
  `cor:aesp-cd-ratio-pivot-interval-interface`,
  `prop:aesp-cd-spectral-schur-ratio-stop`,
  `thm:aesp-cd-point-source-ratio-pivot`,
  `prop:aesp-cd-point-source-homotopy-reorder`,
  `prop:aesp-cd-point-source-superlevel-stop`,
  `prop:aesp-cd-fan-linear-batches`,
  `prop:aesp-cd-all-positive-radius-stop`,
  `prop:aesp-cd-separated-level-reporter`,
  `prob:aesp-cd-variable-two-port-reporter`,
  `prop:aesp-cd-speculative-envelope-doubling`,
  `prop:aesp-cd-rppr-speculative-decoy`,
  `thm:aesp-cd-hard-cap-dynamic-oracle`,
  `cor:aesp-cd-margin-obstacle-primitive`,
  `prop:aesp-cd-moreau-face-shock-sharp`, and
  `cor:aesp-cd-discover-then-restart`,
  `prop:aesp-cd-positive-polynomial-stop`, and
  `cor:aesp-cd-conditional-finite-acceptance`.
- Next concrete action: attack one of the two explicit remaining interfaces.
  On discovery, either implement the persistent bulk-affine
  `MeldAffineHull` reporter on variable two-port blocks, or prove that its
  cactus productive-site specialization cannot meet the support-radius budget; all
  dynamic obstacle updates, level notifications, and rejected frontier rows
  must remain charged.  On the final certified face, bound the number of
  rejected observable windows and maintain the absolute finite-inner budget,
  then compose this with the proved discover-then-restart bridge when the
  required full-face identities are separately certified.  On a generic
  proper final face, use the safe Chebyshev terminal composition instead.  Do not
  transport momentum through serial admissions merely to obtain this
  composition.
- Stop/go test: Go if the actual finite sequence has a declared
  graph-uniform net exponent and all residual charges fit the absolute polish.
  Stop if the proof erases the correction, treats the unknown optimum as an
  algorithmic certificate, commutes positive part with spectral projectors,
  or iterates ambient retraction Lipschitzness.

## Verification

- Source pointers checked: `README.md`, `main.tex` and included sections,
  `registry.toml`, `docs/research_notes.md`, the acceleration literature note,
  and shared ledgers.
- Focused checks: Twenty-seven exact audits with durable `aesp_cd_l1_rppr.*` IDs
  cover the Round-022--049 mechanisms. Run them with `uv run python -m
  experiments.proof_audits.runner --tier full --note aesp_cd_l1_rppr`.
- Review status: Previous independent audits rederived each exact recurrence,
  constant, gate, and scope boundary. This reorganization changes no theorem,
  equation, or evidence classification.
- Known gaps: The P4 theorem has no finite-inner work conclusion. The
  contract-or-spend theorem is exact and restricted to the settled optimal
  face. The Moreau theorem crosses only explicit epoch-boundary admissions and
  still lacks event packing. The high half of the master/mean split has a
  finite-inner transfer; the forced mean and changing-face parts do not yet
  form an end-to-end finite solver theorem.  The two-phase alternative avoids
  changing-face momentum transfer.  Its fixed-envelope obstacle solve is now
  closed without strict margins, but its discovery phase still assumes a
  dynamic boundary-reporter interface.  That reporter interface is closed
  on trees, unicyclic graphs, stable ports, and bounded-productive-site cactus
  traces; unrestricted productive cactus has the square-root epoch tradeoff,
  not the target product.  General variable-port series--parallel graphs remain
  open.  The final
  face still needs a graph-uniform accounting of failed observable gates (or
  a finite relative alignment schedule) before its accelerated accepted
  windows become an unconditional terminal complexity bound.
  No graph-uniform exact accelerated solver or finite-precision result follows.
