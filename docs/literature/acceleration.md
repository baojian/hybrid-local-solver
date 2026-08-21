# Acceleration

## Scope

This note covers outer acceleration frameworks and accelerated local graph
methods relevant to the proposed hybrid solver. Catalyst and AESP are current
starting points, but their applicability has not yet been established.

## Questions for comparison

- What objective, operator, or monotonicity assumptions are required?
- What inner-solver accuracy schedule is assumed?
- How is inexactness measured and propagated?
- Does acceleration require global work or dense state?
- Can warm starts and local active sets be preserved?
- What condition number or `alpha` dependence is improved?
- Does the theoretical accuracy measure match the implemented stopping rule?

## Source annotations

## Citation key: `martinezrubio2023accelerated`

- Citation: David Martínez-Rubio, Elias Wirth, and Sebastian Pokutta.
  “Accelerated and Sparse Algorithms for Approximate Personalized PageRank and
  Beyond.” *Proceedings of the 36th Conference on Learning Theory*, PMLR
  195:2852-2876, 2023.
- DOI/arXiv/URL: <https://doi.org/10.48550/arXiv.2303.12875>;
  arXiv `2303.12875v1`;
  <https://proceedings.mlr.press/v195/martinez-rubio23b.html>.
- Local PDF:
  `papers/2023-colt-martinez-rubio-accelerated-sparse-algorithms-approximate-personalized-pagerank-beyond.pdf`.
- Source-faithful reader archive:
  `manuscript/archive/colt-2023-accelerated-sparse-appr/`.
- Relevance: The paper proposes an exact conjugate-directions PageRank method
  (CDPR) and an accelerated sparse active-set method (ASPR) for nonnegative
  quadratics with symmetric positive-definite M-matrix Hessians. Its geometry
  and retraction arguments are directly relevant to safe support expansion,
  while its repeated full-gradient scans expose a locality cost that a hybrid
  solver must account for explicitly.
- Exact pointers:
  - arXiv v1 PDF pages 4-5, Section 2 and Equations (1)-(6): define the graph
    volumes, PageRank matrix, ℓ1-regularized objective, nonnegative quadratic
    reformulation, and KKT conditions. The printed expansion in Equation (4)
    is algebraically inconsistent with its defining equality and must not be
    reused without correction and documentation.
  - arXiv v1 PDF pages 6-7, Proposition 2: establish monotone restricted
    minimizers, strict positivity of exposed coordinates, and support
    containment for M-matrix quadratics.
  - arXiv v1 PDF pages 8-9, Algorithm 2 and Theorems 3-4: define CDPR and state
    exact correctness plus
    `O(|S*|^3 + |S*| vol(S*))` time and `O(|S*|^2)` space.
  - arXiv v1 PDF pages 9-11, Algorithm 3, Proposition 5, Lemma 6, Algorithm 4,
    and Theorems 7-8: define the accelerated inner solve and ASPR, prove
    support containment and an objective-gap guarantee, and state the sparse
    accelerated complexity.
  - arXiv v1 PDF pages 18-23, Appendix A: give the deferred proofs; the proof
    of Lemma 6 on pages 19-20 prints a degree denominator inconsistent with
    Equation (1), although that step uses only the off-diagonal sign.
  - arXiv v1 PDF page 23, Appendix B: compare the stated CDPR, ASPR, and ISTA
    complexities. The COLT/arXiv-v1 paper contains no computational
    experiments. A later official Julia repository at
    <https://github.com/ZIB-IOL/AAPPR.jl> contains code, serialized results,
    and plots labeled as journal-version experiments.
- Formulation differences: The source uses ε for objective gap and exact sign
  tests for active-set expansion; it specifies no residual-based stopping
  criterion or finite-precision tolerance. Its volume includes selected-set
  cardinality and its algorithms inspect full gradients. `ASPR` in this paper
  is not AESP. The active project uses a corrected source-aligned RPPR
  objective and distinct accuracy namespaces.
- Open questions: Reverify Equation (4) and the cited support-volume result;
  translate the objective-gap guarantee into any adopted residual convention;
  determine whether negative-gradient discovery can be localized without the
  full-gradient volume charge; and audit the sparse operation counts under an
  executable access model.
- Project audit: `manuscript/notes/aspr23_bound_audit/` repairs the quadratic
  normalization, Equation (4), and the APGD-output distance display, then
  proves an algorithm-specific endpoint-path lower bound. For sufficiently
  small objective-gap tolerance, literal ASPR performs exactly `|S*|`
  restricted solves and requires
  `Omega(|S*|^2 / sqrt(alpha))` work on a path, matching the leading published
  product up to logarithms. The scaling `alpha = |S*|^{-2}`,
  `rho = alpha / 100`, and `eps_obj = 10^{-4} alpha^2` yields a literal
  same-tolerance factor-`|S*|` separation from standard FISTA. The audit also
  proves that the official periodic-gradient implementation deletes the
  active-boundary cross block, making early discovery inert on RPPR, and
  records an in-place retraction defect. The official plots generally favor
  default ASPR over their FISTA/ISTA baselines, with CASPR fastest. This does
  not establish a lower bound for every local first-order method or under the
  repository's unresolved residual.

## Citation key: `fountoulakis2026complexity`

- Citation: Kimon Fountoulakis and David Martínez-Rubio. “Complexity of
  Classical Acceleration for \(\ell_1\)-Regularized PageRank.” arXiv
  `2602.21138v2`, 2026.
- DOI/arXiv/URL: <https://doi.org/10.48550/arXiv.2602.21138>;
  <https://arxiv.org/abs/2602.21138>.
- Local PDF:
  `papers/2026-arxiv-fountoulakis-complexity-classical-acceleration-l1-regularized-pagerank.pdf`.
- Source-faithful reader archive:
  `manuscript/archive/arxiv-2026-classical-acceleration-rppr/`.
- Relevance: The paper gives a source-compatible RPPR objective, classical
  FISTA iteration, degree-weighted work model, conditional locality bound
  under boundary confinement, and a star-graph lower bound showing that
  standard FISTA can be asymptotically worse than ISTA.
- Exact pointers:
  - PDF page 3, Section 3 and equation (RPPR): define graph/set notation,
    \(Q\), \(f\), \(F_\rho\), the optimal support, and coordinatewise KKT
    conditions.
  - PDF page 4, Section 3.1 and equations (FISTA), (2), and (3): define
    \(L,\mu,\eta,\beta\), the FISTA iterates, weighted soft thresholding, and
    degree-weighted per-iteration work.
  - PDF pages 4-5, Sections 4.1-4.2 and equations (4)-(6): define the
    over-regularized A/B problems, spurious active sets, complementarity
    margins, and the work decomposition.
  - PDF pages 5-6, Theorems 4.3-4.4: state the conditional total-work bound
    and the boundary no-percolation condition.
  - PDF pages 18-23, Appendix D: construct the star-graph lower bound where
    FISTA activates a high-degree center while ISTA remains local.
  - PDF page 24, Appendix E, “Stopping criterion”: define the unit-step
    proximal fixed-point residual used in all experiments.
- Formulation differences: The paper uses plain italic vector/matrix symbols
  and studies undirected unweighted graphs with \(s=e_v\). It overloads
  \(\varepsilon\): theory uses an objective-gap target while experiments use a
  proximal fixed-point residual tolerance. The active manuscript now
  distinguishes these as \(\varepsilon_{\mathrm{obj}}\) and
  \(\varepsilon_{\mathrm{pg}}\). Neither residual nor its conversion to the
  project's PageRank error has yet been adopted implementation-wide.
- Open questions: Prove a conversion between the proximal fixed-point
  residual and the project's eventual PageRank accuracy convention; determine
  whether the hybrid method preserves boundary confinement; and compare the
  paper's degree-weighted work with edge-operation accounting for local inner
  solves.

## Citation key: `lin2018catalyst`

- Citation: Hongzhou Lin, Julien Mairal, and Zaid Harchaoui. “Catalyst
  Acceleration for First-order Convex Optimization: From Theory to Practice.”
  *Journal of Machine Learning Research*, 18(212):1-54, 2018.
- DOI/arXiv/URL: <https://jmlr.org/papers/v18/17-748.html>; preprint
  <https://arxiv.org/abs/1712.05654>.
- Local PDF:
  `papers/2018-jmlr-lin-catalyst-acceleration-first-order-convex-optimization.pdf`.
- Relevance: Catalyst is the principal generic outer-acceleration framework in
  the project's research plan. It approximately solves a sequence of
  regularized auxiliary problems, using explicit inner stopping criteria and
  warm starts to accelerate a base method with linear convergence on strongly
  convex objectives.
- Exact pointers:
  - Pages 5-6, Section 1.2 and Algorithm 1: give the two-loop Catalyst overview,
    auxiliary objective, extrapolation, and outer momentum.
  - Pages 7-10, Section 2 and Proposition 1: interpret Catalyst through the
    Moreau envelope and formulate approximate proximal subproblem solutions.
  - Pages 10-13, Section 3 and Algorithm 2: state the full method, its two inner
    accuracy criteria, warm starts, and parameter choices.
  - Pages 14-20, Section 4.1 and Theorems 3 and 7: analyze outer-loop
    convergence under the two inexactness criteria.
  - Pages 20-29, Sections 4.2-4.3, Corollaries 13 and 16, and Propositions
    17-18: analyze warm-started inner work and combine it with outer
    convergence into global complexity bounds.
  - Pages 30-49, Section 5: compare stopping criteria, warm starts, and Catalyst
    variants experimentally.
- Formulation differences: Catalyst assumes a convex composite objective and
  a base method with a global linear-convergence model on strongly convex
  subproblems. The hybrid local solver must also preserve sparse support,
  locality-sensitive work, and the repository's residual convention; these
  properties are not guaranteed by Catalyst's function-gap or duality-gap
  criteria.
- Open questions: Derive a valid conversion from the hybrid solver's residual
  to Catalyst's inner accuracy criteria, determine whether warm starts preserve
  the active set, and account for outer-loop extrapolation and auxiliary
  regularization without introducing global dense work.
- Project continuation: `manuscript/notes/aesp_cd_l1_rppr/` now instantiates
  the strongly convex relative criterion (C2), the composite proximal warm
  start of Proposition 15, and the outer rate of Proposition 8. On a fixed
  certified graph envelope of degree volume `V`, greedy local coordinate
  descent supplies C2 in `O_tilde(V)` degree work per stage, yielding
  `O_tilde(V / sqrt(alpha))` total work. This closes the inner/start-mass
  interaction. The oracle-free heap implementation also satisfies a
  trajectory-dependent `O_tilde(V_exp_max / sqrt(alpha))` bound; the remaining
  universal question is no longer whether safe lower centers exist. A local
  retraction and a safeguarded outer recurrence keep every complete shifted
  coordinate trajectory inside the optimal RPPR support, and the stage-start
  KKT masses telescope without a `1/alpha` loss. The exact remaining outer
  issue is quantitative: a three-vertex path refutes pointwise momentum
  nonexpansion, and the current multiplicative potential reduces accelerated
  continuation to bounding the positive part of cumulative correction
  log-inflation under the proximal-displacement collapse identity. An exact
  single-edge singleton-support family has a full correction every other stage
  but zero normalized log-inflation, so raw correction count cannot replace
  that ledger or be charged only to support additions. A new analytical lemma
  bounds each `log max(1,gamma_t)` by a normalized collateral-clipping
  fraction; from stage two onward its amplitude has the exact collapse form.
  The fraction uses the unknown optimum and may overcharge a benign collateral
  round. An exact full-support single-edge family now refutes charging this
  analytical fraction to monotone Euclidean log-error with an
  `alpha`-uniform or polylogarithmic coefficient: the stage-two charge is
  `Theta(q)` while the corresponding log-progress is `Theta(q^2)`, where
  `q=sqrt(alpha/(1-alpha))`. This does not refute cumulative control of the
  actual log-inflation, a collapse-history argument, or another potential.
  Those routes, and a locally checkable surrogate, remain the exact open outer
  problem.

## Project-only Round-003 acceleration boundary

The following are internally proved scope boundaries, not claims imported
from the papers annotated above:

- For safeguarded AESP-CD, only Euclidean-log packing of the a-posteriori
  collateral charge is refuted. The multiplicative ledger's actual
  cumulative log-inflation and every genuinely different or multistep
  potential remain open.
- For response-preconditioned continuation, the prescribed notched-double-sun
  epoch rules out rebuilding and storing a fresh explicit dense harmonic
  table at every event. It does not rule out implicit multi-right-hand-side
  solves, batched or compressed row access, dynamic response state, or sparse
  recovery, and the structural trace is not an RPPR admission trajectory or
  reporter lower bound.
- For recurrence lower bounds, the endpoint path at `alpha=n^(-2)` attains
  the target `Omega(nu_n/sqrt(alpha))` obstruction only for the named exact
  full-vector `DiagSpecPoly(r)` subclass, including polynomial
  preconditioning only when every underlying transformed-matrix application
  is counted. Supported growing-prefix Krylov, arbitrary response maps, and
  finite precision remain outside that theorem.

The corresponding next targets are, respectively, a collapse-aware packing
or local surrogate, an implicit/batched charged response reporter, and one
further semantically explicit recurrence/response subclass in the surviving
dimension regime.

## Project-only Round-004 composition boundary

These are independently reviewed project results, not source claims from the
papers annotated in this file:

- On a center-seeded unweighted three-arm spider with `0 < rho < 1/3`, exact
  RPPR affine transfer products and two scalar root aggregates give an
  exact-real-cell `kappa = 1` common-state activation-token countdown for
  every legal certified boundary-batch order. Response, exposure, control, state writes
  and storage, terminal recovery, and exact output are all charged in
  `O(C(S*)) = O(1 / rho)` work. This is a one-branch structural result, not a
  graph-uniform accelerated solver or a finite-precision guarantee. The next
  test is the smallest tree with two branching vertices.
- On a simple cycle core, `FACR(p)` handles supplied certified closed pendant
  components whose attachment is one fixed core vertex. Its exact-cell
  kinetic state reports absorption-only upward crossings in
  `O(V_fin + |R| log(2 + |R|) + Z)` work with separate `O(V_fin)` memory,
  including certificate verification/scanning, response construction,
  validation, recovery, and output, and without materializing or globally
  rekeying all boundary keys. It does not discover closure online, maintain a
  post-repair terminal queue, cover varying attachments or response-rank
  growth, or imply finite-precision robustness.
- On one endpoint edge, for `0 < alpha < 1` and
  `rho=tau=r<(1-alpha)/(3+alpha)`, the exact zero-padded safe-gated recurrence
  started at a zero-momentum restricted optimum retains a positive fraction
  of the Schur gain after the first enlarged-face step. This refutes only
  fixed-face-exact, shock-free pointwise carryover. It does not refute a
  continuation inequality with an explicit Schur/transport term, cumulative
  shock packing, or newly-admitted-volume amortization.

The live composition targets are therefore multibranch affine transport,
varying-attachment or online-closure kinetic response, and an expanding-face
energy ledger that explicitly transports and cumulatively charges the Schur
shock.

## Project-only Round-005 trace, recurrence, and handoff boundaries

These are independently reviewed project results, not source claims from the
papers annotated in this file:

- The prescribed notched-double-sun `F`-only structural epoch is not a
  canonical single-seed RPPR trajectory. At every relevant common face, each
  unseeded matched frontier/report pair `f_i,w_i` has the same shifted load,
  degree, face row, and exact demand, so the all-violations KKT gate admits the
  pair together. A single seed can distinguish at most one pair. The related
  finite-band conclusion concerns only one simultaneous uniform point-estimate
  call at that face; it does not constrain asynchronous interval refinement.
  The structural rank and explicit-table audits remain valid, but they are not
  reporter lower bounds on a legal RPPR trace.
- On the endpoint-seeded unweighted path with ambient degrees,
  `alpha=n^(-2)`, and `eps_ppr=1/10`, exact ordinary CG from zero has a positive
  singleton frontier residual and a direction supported on the full visited
  prefix. Its actual degree-normalized residual certificate first holds at
  step `n`. The chosen sequential implementation performs `n^2-1` supported
  row work before the final verifier and has literal rereading and
  materialization cost
  `Theta(n^2)=Theta(nu_n/sqrt(alpha))`. This is specific to that exact-CG
  trajectory and explicit algebraic-cell realization, not a lower bound for
  arbitrary supported recurrences, implicit response, prefetching, or finite
  precision.
- On the center-seeded unweighted three-arm spider with `0<alpha<1` and
  `0<rho<1/3`, any finite fully charged gate-compatible Phase-I prefix can
  discard its signed numerical and momentum state, convert the actual
  irreversible arm prefixes in one exact-real common-state pass, and continue
  with the exact affine activation-token response. The total is
  `B_J^full + O(C(S*))`, including conversion, response, control, state,
  validation, canonical recovery, and output. Product work follows only from
  an independent bound on the fully charged prefix `B_J^full`; the handoff
  retains no estimate-sequence energy and proves no shock-free carryover or
  general-graph theorem. The note's particular composite Catalyst/AESP prefix
  is included only in its stated range `alpha<1/2`.

The next falsifiable targets are an asymmetric legal cyclic witness whose KKT
trace is proved before reporter analysis, a precisely named supported-prefix
recurrence or implicit representation beyond literal ordinary CG, and the
smallest two-branch-vertex handoff together with an independent Phase-I work
bound.

## Project-only Round-006 legality, transport, and certificate boundaries

These are independently reviewed project results, not source claims from the
papers annotated in this file:

- The first asymmetric degree-lift repair of the cyclic trace is still
  KKT-illegal for a long report-free petal epoch. On the even matched-report
  sun, source petals have degree one, reports have degree two, anchors have
  degree four, and the raw anchor--report block has rank `n`. Nevertheless,
  for every `0<alpha<1` and `rho>0`, with
  `vartheta=(1-alpha)/2`, report quietness bounds every anchor by
  `4 alpha rho / vartheta`, while a positive source-petal demand requires its
  anchor to exceed `2 alpha rho / vartheta`; the nonseed anchor equation makes
  that band impossible. Hence every canonical prefix avoiding `W` contains at
  most one `F` petal. This is an exact KKT-legality obstruction, not a
  reporter, response-rank, implementation, or finite-precision lower bound.
  The then-next cyclic witness put an active relay between the anchor and an
  unadmitted report endpoint; Round-007 below records why that repair also
  fails its all-seed chronology test.
- On the double-Y tree seeded at branch vertex `o`, `s=e_o`, with two adjacent
  degree-three branch vertices, exact-real affine pendant-prefix records grow
  from one scalar core to a fixed-size SPD `2 x 2` Schur core after the second
  branch is admitted. For `0<alpha<1` and `0<rho<1/3`, they support every
  legal certified boundary-batch order with activation-token tightness
  `kappa=1` and fully charged `O(C(S*))=O(1/rho)` work. With
  `zeta=(1-alpha)/(1+alpha)` and
  `rho_link(alpha):=zeta/[3(3+zeta)]`, the explicit condition
  `rho<rho_link(alpha)` forces every legal order into the rank-two phase.
  This is a response theorem for one fixed two-branch core, not a growing
  backbone, cycle, finite-precision result, RPPR-to-PPR conversion, or
  graph-uniform accelerated solver. At this round the hybrid composition was
  still open; Round-007 below closes that fixed-core handoff while leaving the
  Phase-I budget independent. The response direction still next tests growing
  branch cores and cycles.
- On the endpoint path with `n>=8`, `alpha=n^(-2)`, and `eps_ppr=1/10`, the
  actual sparse residual-certificate task is easier than the ordinary-CG
  trajectory. A five-coordinate vector supported inside the first six
  exposed vertices is a degree-four polynomial in `Q` applied to `b`, passes
  the strict certificate, and has an admissible `CertPrefixPoly` execution
  using `O(1)` exact cells. A fully charged five-row append-only `LDL^T`
  response emits the same sparse output in `O(1)` exact cells. This refutes a
  product lower bound only for that named class and task. It neither shortens
  ordinary exact CG nor weakens the different exact full-vector
  `DiagSpecPoly(r)` obstruction. Round-007 below shows that even a
  full-support tolerance does not repair the broad supported-prefix class;
  its next candidate must also defeat sparse-basis delayed synthesis.

## Project-only Round-007 chronology, handoff, and full-support boundaries

These are independently reviewed project results, not source claims from the
papers annotated in this file:

- The two-edge active-relay repair of the matched-report sun still cannot
  realize a common preloaded-relay face followed by a long report-free petal
  epoch. At every `W`-free canonical face, the canonical all-violations batch
  containing a nonseed relay `r_i` also contains its degree-one petal `f_i`
  unless that petal is already active. Thus every nonseed relay is preceded or
  co-admitted by its petal, despite full-rank raw anchor--relay and
  relay--report cuts. This exact KKT chronology stop does not exclude paired
  petal--relay batches, arbitrary positive-subset policies, or a different
  legal witness, and it is not a reporter lower bound. Round-008 below tests
  and retires the degree-three petal-cycle option; relays fed from an
  independent active backbone or a different bounded-degree gadget remain,
  with the canonical trace still due before reporter analysis.
- On the branch-seeded double-Y (`s=e_o`), the reviewed scalar/rank-two affine
  response now composes with every finite fully charged gate-compatible
  Phase-I prefix. The prefix and post-handoff ledgers both report all eleven
  resource coordinates; the latter separately charges adjacency,
  conversion/control, affine and Schur response work, recovery, validation,
  memory, terminal materialization, exact output, and one constant-size
  certificate emission at every declared external stage. For `0<alpha<1`
  and `0<rho<1/3`, the exact-real total is
  `B_J^full + O(C(S*))`; it reaches product scale only under an independent
  bound on `B_J^full`. Signed numerical energy is discarded. Other seeds,
  growing branch cores, cycles, finite precision, and graph-uniform
  continuation remain open.
- On the endpoint path with `n>=8`, `alpha=n^(-2)`, and the tighter actual
  residual tolerance `eps_ppr=1/(10n)`, every certified sparse output must
  contain all `n` coordinates. Full support still does not force product work
  in the broad exact-cell `CertPrefixPoly` class: sparse row actions and exact
  cancellations generate singleton coordinate directions, after which a
  fixed degree-six spatial profile is synthesized and verified in
  `Theta(n)` work with no intermediate full-vector materialization. A
  same-task append-only `LDL^T` response is also `Theta(n)`, whereas
  `nu_fin/sqrt(alpha)=Theta(n^2)`. This refutes the product bound only for the
  broad supported-prefix class/task. It does not shorten ordinary CG, weaken
  the exact full-vector `DiagSpecPoly(r)` theorem, or give a finite-precision
  result. A future candidate must defeat both constant-prefix residual
  spreading and sparse-basis delayed synthesis, or justify a narrower
  trajectory/materialization rule.

## Project-only Round-008 chronology, eager-state, and transported-center boundaries

These are independently reviewed project results, not source claims from the
papers annotated in this file:

- The degree-three petal-cycle repair genuinely reverses the isolated local
  relay/petal threshold, but it still cannot realize the intended canonical
  relay-first epoch. For every `0<alpha<1`, `rho>0`, and seed orbit, if a
  report-free canonical face contains all relays and its next
  all-violations batch is also report-free, then at most one petal remains
  inactive. If a report enters with or before the last relay, or in the first
  post-last-relay batch, the required report-free epoch has already failed.
  This is exact KKT chronology for the canonical all-violations gate only. It
  does not cover arbitrary positive-subset policies and is not a reporter,
  response-rank, work, output, stability, or finite-precision lower bound.
  The next witness must activate relays from an independent backbone or use a
  different bounded-degree gadget, and must again prove all seed cases and
  genuinely changing response directions before reporter analysis.
- On the branch-seeded degree-three caterpillar, for each fixed `m` and
  `0<alpha<1`, an explicit family-dependent range
  `0<rho<rho_cat(m,alpha)<=1/3` permits one exact-KKT positive-subset
  singleton order that admits the branch backbone, then a length-`m` endpoint
  arm, and finally the deferred leaves. Every arm append changes all `m+1`
  deferred positive leaf demands. The literal exact-cell `EagerTipKey` state,
  which stores and refreshes one separately addressed exact key per live tip
  with no lazy indirection, therefore performs at least `m(m+1)` old-key
  writes. This is not the canonical all-violations trace, no positive
  `m`-uniform `rho` range is claimed, and the result is not a lower bound for
  lazy affine keys, sign persistence, kinetic/group reporting, on-demand
  implicit response, arbitrary RPPR algorithms, or finite precision. A
  balanced affine-transfer tree still supports a named append/update or tip
  query in `O(log(2+m))` exact work with `O(m)` retained cells; a charge-comparable
  dynamic all-positive reporter for every legal order remains open.
- For one safe face expansion `U` to `U+`, transporting the estimate center by
  the exact restricted-optimum displacement `d` gives the identity
  `E_(U+)(x,v+d)=E_U(x,v)+Delta_B`; the nonnegative Schur gains telescope over
  nested faces. This changes the center recurrence and does not prove the
  literal zero-padded conjecture. On endpoint paths, an append-only exact
  `LDL^T` response stores centered momentum `v-x_U*`, represents the dense
  optimum shift without old-prefix coordinate rewrites, and charges factor,
  Schur, admission, and state appends to newly admitted volume. Its full
  eleven-coordinate ledger still charges every old-face recurrence read and
  response application through the swept-volume term, plus validation,
  materialization, memory, and terminal sparse output. The stated
  implementation is internally gated and has one terminal external
  certificate/output stage; intermediate external emissions are not covered.
  The result gives no bound on the step count, late weighted shocks, or total
  swept volume; it does not extend automatically to branching or cyclic cores
  and makes no finite-precision or bit-complexity claim. PPR conversion still
  requires the terminal one-sided certificate with
  `rho=tau=eps_ppr/2`. The next proof must pack the signed zero-padding defect
  or control those late shocks and old-face sweeps before testing the first
  branching response.

## Project-only Round-009 chronology, kinetic-delta, and weighted-shock boundaries

These are independently reviewed project results, not claims from the source
papers annotated in this file:

- The independently fed double-cycle does not rescue the intended canonical
  cyclic chronology for a backbone-`B` seed. For every `0<alpha<1` and
  `rho>0`, every exact-real canonical all-violations prefix is petal-free as
  long as the prefix and its next batch are report-free; the first petal batch,
  if one occurs, contains a report. The proof uses the report cap and the exact
  inactive-anchor case split: its relay is already active or is co-admitted in
  the same batch. This is only the prescribed backbone-seeded report-free
  petal/attachment STOP, with no claim after `W` enters. The seed restriction
  is necessary: an anchor seed and `0<rho<(1-alpha)/8` give an exact
  report-free first-petal batch. Arbitrary positive-subset policies,
  response-direction claims, reporter/work lower bounds, finite precision, and
  stability remain outside the result. The next chronology test is the full
  canonical continuation of the anchor-seeded counterrange. If that does not
  yield the required epoch, a feed/gadget must escape the anchor--relay
  maximum principle or the canonical cyclic-witness route should be
  deprioritized.
- On the fixed-`m` branch caterpillar with seed `s=e_(b_1)`, fixed
  `0<alpha<1`, and family-dependent
  `0<rho<rho_cat(m,alpha)<=1/3`, the explicit backbone-first exact-KKT
  positive-subset policy now has a charged implicit reporter.
  `CaterpillarKineticDelta` combines the separable last Green column with a
  strict crossing-key heap, retains the exact all-positive live-tip set,
  preserves equality until a demand becomes strictly positive, and emits each
  newly positive label once. After the backbone, arbitrary nonempty subsets of
  currently known positive pendant tips may be committed. For
  `2m-1<=J<=3m`, its exact-cell work is `O(m log(2+m))`, state is `O(m)`, and
  all transfer queries, heap operations, membership checks, certificate
  replies, delta labels, terminal recovery, validation, materialization, and
  output are charged. This is a delta-only theorem: canonical all-violations,
  arbitrary pre-backbone interleavings, repeated full positive lists,
  `kappa=1`, an `m`-uniform positive `rho` range, finite precision, and a
  graph-uniform accelerated arm are not proved. A full list at every
  checkpoint may itself have quadratic output.
- For `q=sqrt(alpha)` and `theta=1-q`, the transported-center weighted Schur
  tail has the exact summation-by-parts identity
  `W_T=theta^(T-1) H_0 + q sum_(t=1)^(T-1) theta^(T-1-t) H_t`, where `H_t` is
  the remaining restricted-face optimum gain. Thus the analytical charge is
  discounted occupancy of remaining gain, not merely the unweighted shock
  telescope. A terminal gate-compatible endpoint-edge family has
  `T=2`, `J=1`, `nu_fin=2`, `mathfrak V_T=3`, and
  `W_T/(q sum_t Delta_t)=(1-q)/q`; it refutes only a universal
  `C q sum_t Delta_t` collapse. It is not a stage-count, swept-volume, or work
  lower bound and does not rule out a terminal-accuracy floor, an
  occupancy-based estimate, or another potential. Bounding or refuting that
  occupancy jointly with the terminal floor, `T`, and total old-prefix swept
  volume is the next endpoint-path target.

## Project-only Round-010 canonical-layer and swept-prefix boundaries

These are independently reviewed project results, not claims from the source
papers annotated in this file:

- The anchor-seed escape on the double-cycle feed is now closed in its exact
  counterrange. For every even `n>=6`, `0<alpha<1`, and
  `0<rho<(1-alpha)/8`, the exact-real canonical all-violations continuation
  either reports earlier or admits at most the three report-free petals at the
  seed and its two neighboring sites; the first `j+/-2` petal batch co-admits
  `w_j`. This retires only that anchor-seeded rescue. Relay seeds, arbitrary
  positive-subset policies, post-report chronology, finite-band reporting,
  response directions, reporter/work lower bounds, stability, and finite
  precision remain open. Round-011 below closes the relay-seed orbit and
  retires this graph family only for the prescribed canonical witness; a new
  candidate must escape the accumulated KKT stops.
- On the fixed-`m` branch caterpillar with branch seed `s=e_(b_1)`, fixed
  `0<alpha<1`, and the family-dependent strict range
  `0<rho<rho_can(m,alpha)<=rho_cat(m,alpha)<=1/3`, the actual canonical
  all-violations trace consists of exactly `m` three-label distance-layer
  batches. `CaterpillarCanonicalLayerDelta` uses localized absorption cells
  and balanced tridiagonal transfers to report this trace in
  `O(m log(2+m))` exact-cell work and `O(m)` state, with every demand test,
  delta/certificate exchange, recovery, validation, materialization, and
  terminal output charged. This is a fixed-family, branch-seeded, exact-real,
  delta-only result. It does not cover `rho_can<=rho<rho_cat`, other seeds or
  policies, arbitrary pre-backbone interleavings, repeated full lists,
  `kappa=1`, finite precision, PPR conversion, or graph-uniform product work.
  In particular, no positive `rho` range uniform in `m` is claimed.
- A zero-start endpoint-path family gives the first exact swept-prefix
  separation for the named literal implementation. Use the endpoint seed and
  ambient path degrees on a finite path with exactly `N=L+1` edges. With
  `q=1/n` for integer `n>=2`, `L=n^2`,
  `rho=tau=(q/3)((1-q)/(1+q))^L`, and `eps_ppr=2rho`, the terminal certificate
  forces at least `L` singleton admissions, `T>=L`,
  `nu_fin=Theta(q^(-2))`, and
  `mathfrak V_T>=L^2=q^(-4)`. Thus literal full-prefix work exceeds the
  realized `nu_fin/q=Theta(q^(-3))` scale by a certified factor `1/q`.
  However, that certified factor is `Theta(log(q/rho))`, and no matching
  swept-volume upper bound is proved. The result refutes only log-free
  accounting for this exact-real literal implementation, not a soft-order or
  implicit bound, branching, or finite precision. Round-011 below proves only
  product-scale constant-ratio floors and a moving-global-correction STOP;
  the observed stage and swept exponents remain open.

## Project-only Round-011 relay-seed, handoff, and constant-ratio boundaries

These are independently reviewed project results, not claims from the source
papers annotated in this file:

- The last candidate seed orbit on the even double-cycle feed is stopped at
  its first step. For every even `n>=4`, relay seed `s=e_(r_j)`,
  `0<alpha<1`, and `rho>0`, the exact canonical all-violations gate either
  does not initialize, terminates on the relay singleton, or admits the
  incident report `w_j` in its first propagating batch, possibly together
  with `b_j`. Combined with the earlier backbone- and anchor-seed results,
  this retires the double-cycle family only for the prescribed canonical long
  report-free later-petal witness. It does not retire all cyclic witnesses,
  cover arbitrary positive-subset policies or post-report chronology, or
  imply a response-direction, reporter/work, stability, or finite-precision
  lower bound. A new legality candidate needs a different coupling or
  bounded-degree settlement gadget.
- On the fixed-`m` branch caterpillar with `m>=2`, branch seed
  `s=e_(b_1)`, `0<alpha<1`, and
  `0<rho<rho_can(m,alpha)<=rho_cat(m,alpha)<=1/3`, any fully charged Phase-I
  prefix ending at an actual canonical checkpoint has a deterministic
  support-only conversion into `CaterpillarCanonicalLayerDelta`. One direct
  pass builds the current absorptions, tridiagonal core, and balanced transfer
  state without replaying or querying earlier faces. The exact-real total is
  `B_J^full + O(C(S*) log(2+C(S*)))`, with prefix and suffix eleven-coordinate
  ledgers explicit. Product work follows only from an independent fully
  charged prefix bound; no signed estimate-sequence energy, wider parameter
  range or policy, repeated full-list interface, finite precision, PPR
  conversion, or graph-uniform theorem is supplied.
- At the constant ratio `rho=tau=q/5`, `0<q<=1/4`, the zero-start
  endpoint-path execution has
  `J,nu_fin=Theta(1/q)`, `T>=J`, and
  `mathfrak V_T=Omega(q^(-2))=Omega(nu_fin/q)`. This is a product-scale floor,
  not a separation. An exact `q=1/5` trace additionally refutes frontier-only
  gate logic: a correction maximized at the seed suppresses a raw stage-6
  frontier violation, and by stage 9 the maximizer is the old interior vertex
  `v_2`. Neither result proves the observed `T=Theta(q^(-2))` or
  `mathfrak V_T=Theta(q^(-3))` scaling. Exact control of the moving global
  correction, or a redesigned charge-comparable schedule, remains open.

## Project-only Round-012 charged-flush, capped-prefix, and moving-maximum boundaries

These are independently reviewed project results, not claims from the source
papers annotated in this file:

- The aggregate debt theorem is exact-real and freezes one face partition
  `(A,F)`, its exposed cut, and its shifted ladder while additive nonnegative
  fragments arrive. Its scalar sparse-recurrence work is
  `O_tilde_eta(cvol(T)/sqrt(alpha) + C_frag)`, where `C_frag` charges every
  fragment-coordinate event. For `r` nonnegative source columns the actual
  graph work is the sum of the `r` Chebyshev runs; a signed source is split
  into `p=2r` nonnegative streams, with no cancellation credit before the two
  certified results are combined. The energy certificate implies a
  simultaneous mathematical interval for every exterior response, but does
  not materialize any of them. The named non-output-sensitive
  `AllBoundaryFlush` separately scans the cut, computes, materializes,
  classifies, validates, and emits every current boundary interval and records
  all eleven resource coordinates, including fragment and Chebyshev state,
  cut-response applications, full-face writes, rounds, and output. With fixed
  column count, one such fully charged flush per geometrically growing
  fixed-decision face retains the final-volume product bound. This is not an
  online partial reporter, a face-mutating theorem, or a finite-precision,
  bit-complexity, or terminal PPR/RPPR result. The proof owner is
  `response_preconditioned_hybrid`, `thm:aggregate-chebyshev-debt-flush` and
  `cor:geometric-aggregate-debt-flush`.
- Pure geometric sleep still cannot implement the literal gate. On every
  fixed sufficiently long ambient-degree endpoint path, a family-dependent
  positive `rho_n` makes canonical all-violations batching admit one successor
  at a time while consecutive charged-volume ratios tend to one; no positive
  lower bound on `rho_n` uniform in path length is claimed. The named
  append-only exact-real comparator has `R_int=n` and a complete linear
  eleven-vector. Thus `prop:singleton-path-geometric-sleep-obstruction` is a
  scheduling obstruction, not a path work or interaction-round lower bound.
  Output-sensitive partial flushing or another proved safe trace remains open.
- On the promised fixed-`m` branch caterpillar with `m>=2`, branch seed
  `s=e_(b_1)`, `0<alpha<1/2`, and `0<rho<rho_can(m,alpha)`, the named
  `Full-BC-AESP_0` policy pays a complete traversal, uses the imported support
  conclusion to certify `U=V=S*`, runs exactly
  `T_*=ceil(2 log(4)/sqrt(alpha/(1-alpha)))` relative-accuracy AESP-CD stages,
  and invokes no canonical gate before handing off at
  `Uhat_0={b_1}`. Its full prefix vector is
  `(O(D_*),O(D_*),0,O(C_*),O(H_*),O(D_*),0,O(C_*),O(C_*),O(D_*),0)`, and the
  authoritative work is `O(H_*)`. Composing the separately charged canonical
  response gives exact output in `O(H_*+C_* log(2+C_*))`. The soft product
  shorthand hides `log(1/(1-2 alpha))` and is not uniform as
  `alpha` approaches `1/2`. This is a full-realized-support, fixed-family,
  zero-checkpoint witness, not adaptive locality, a general prefix bound,
  graph-uniform work, finite precision, or PPR conversion. Conversely,
  `prop:branch-caterpillar-uncapped-prefix-obstruction` shows that the generic
  phrase “any finite valid burn-in” supplies no work bound: arbitrarily many
  valid exact-inner Catalyst stages can keep the common checkpoint at `k=0`
  while adding `Omega(N)` control work.
- For the exact-real zero-start, internally gated transported-center endpoint
  path at `rho=tau=q/5`, the moving-maximum theorem sets
  `K_q=ceil(log(50(1+q^2)^2 q^(-10))/(-log(1-q)))` and proves
  `T<=(J+1)K_q=O(q^(-2) log(1/q))` and
  `mathfrak V_T=O(q^(-3) log(1/q))`. The literal full-prefix eleven-vector
  is `(Theta(q^-1),Theta(q^-1),1,0,O(q^-3 log(1/q)),`
  `O(q^-3 log(1/q)),O(q^-3 log(1/q)),Theta(q^-1),O(q^-1),`
  `O(q^-3 log(1/q)),Theta(q^-1))`. Thus it charges adjacency exposure, one
  terminal interaction, every old-face control/recurrence/response/
  materialization pass, both memory coordinates, and output. These are one-log
  upper bounds independent of where the global
  correction maximizer moves. They do not prove matching `Theta` laws, lower
  bounds at those powers, logarithm removal, a product separation, the
  zero-padded recurrence, branching or cyclic graphs, intermediate emissions,
  or finite-precision work. Those exact limitations are part of
  `thm:path-moving-max-soft-upper`.

## Project-only Round-013 local-splice and representation boundaries

These are independently reviewed project results and one quarantined proof
attempt, not claims from the source papers annotated in this file:

- Freeze the notched-double-sun face containing all `n` anchors and source
  petals, its rank-`n` anchor--report cut, and the positive shifted ladder.
  For fixed `n` and sufficiently near-one `alpha`, unit first-rung fragments
  have matching response `Theta(vartheta^2)` and off-matching response
  `O_n(vartheta^3)`, where `vartheta=(1-alpha)/2`. At gate
  `g=vartheta^(5/2)` with transition band `g/2`, exactly one new report label
  crosses per event while every response increment is dense. The named
  separately addressed exact-vector policy `EagerExactSlack` therefore pays
  `Theta(p n^2)` response/control/materialization work for only `Theta(r n)`
  delta/certificate output, with `p=r` for nonnegative columns and `p=2r`
  for signed certification. Its complete eleven-vector is
  `eq:notched-sun-eager-eleven-vector`. This is an exact-real fixed-face
  representation/query STOP, not an RPPR chronology or a lower bound against
  implicit cyclic transfer, packed coded queries, scale truncation, on-demand
  validation, or a general output-sensitive partial reporter.
- On the fixed `m>=2`, branch-seeded caterpillar with `alpha<1/2` and
  `rho<rho_can`, `FirstLayer-BC_1` gives one genuinely local actual
  nonzero-checkpoint comparator. It scans exactly
  `Uhat_1={b_1,b_2,a_1,r_1}`, commits the first canonical batch, exactly
  settles and retains the response state at `k=1`, and has prefix vector
  `(9,2,1,0,O(1),0,O(1),O(1),O(1),Theta(1),Theta(1))`. Its post vector is
  `eq:branch-caterpillar-first-layer-post-eleven-vector`; in-place native
  continuation returns the exact RPPR optimum in
  `O(C(S*) log(2+C(S*)))`. This is response-native and makes no acceleration
  claim. For a signed approximate state at checkpoint `k`, the exact demand
  identity yields the sharp norm-ball margin
  `mu_k=min_v g_(k,v)/beta_(k,v)`. The imported relative-gap route needs zero
  stages when `Delta_(k,0)=0`; for positive gap its sufficient cap is
  `T>(2/sqrt(alpha/(1-alpha))) log_+(4 Delta_(k,0)/(alpha mu_k^2))`, and each
  relative-oracle stage still carries `log(1/(1-2 alpha))`. The old constant
  half-gap does not imply this margin comparison. This is an interface
  barrier, not a lower bound against exact settlement or a new one-sided
  certificate.
- The attempted constant-ratio endpoint-path spectral lower proof is
  quarantined. Under an inactive projection, the conditional full-face
  recurrence has the stated damped-cosine roots, but roots alone neither
  determine the actual entry coefficients nor prevent cancellation in the
  moving residual range. The finite exact checks are scaffolding only. No
  terminal logarithmic block, asymptotic lower eleven-vector, or refutation of
  `K_face=O(q^-1)` follows. The Round-012 one-log moving-maximum upper bound
  remains authoritative, and logarithm removal versus necessity is open.

## Citation key: `uschmajew2022note`

- Citation: André Uschmajew and Bart Vandereycken. “A Note on the Optimal
  Convergence Rate of Descent Methods with Fixed Step Sizes for Smooth Strongly
  Convex Functions.” *Journal of Optimization Theory and Applications*,
  194(1):364-373, 2022.
- DOI/arXiv/URL: <https://doi.org/10.1007/s10957-022-02032-z>; preprint
  <https://arxiv.org/abs/2106.08020>.
- Local PDF:
  `papers/2022-jota-uschmajew-optimal-convergence-descent-fixed-step-smooth-strongly-convex.pdf`.
- Relevance: This note derives sharp function-value contraction factors for
  fixed-step descent methods by viewing variable-metric, gradient-related, and
  inexact-gradient steps in suitable inner products. The results offer compact
  tools for analyzing hybrid updates whose directions or gradients differ from
  exact Euclidean gradient descent.
- Exact pointers:
  - Pages 364-366, Section 1 and Equations (1.1)-(1.4): state the optimal
    fixed-step contraction factor for smooth strongly convex objectives and
    motivate function-value analysis.
  - Pages 366-367, Section 2 and Theorem 2.1: give the variable-metric rate in
    terms of objective and metric condition numbers.
  - Pages 368-371, Section 3, Lemma 3.1, and Theorems 3.2 and 3.4: treat
    gradient-related directions under angle and scaling conditions.
  - Pages 371-372, Section 4, Lemma 4.1, and Theorem 4.2: derive the sharp
    fixed-step rate for gradients with bounded relative error.
  - Page 373, Section 5: summarizes the metric-change proof strategy and its
    scope.
- Formulation differences: The analysis assumes a globally smooth,
  strongly-convex objective and measures function-value contraction. The
  project uses graph-structured PageRank objectives, residual stopping, sparse
  active sets, and locality-sensitive work, so smoothness, strong convexity,
  and error bounds must be translated into the repository's normalization and
  residual conventions.
- Open questions: Express local truncation or stale-coordinate effects as the
  relative gradient error in Theorem 4.2, determine whether active-set updates
  satisfy the angle/scaling conditions of Section 3, and compare the resulting
  sharp rate with Catalyst and coordinate-local convergence bounds.

## Citation key: `tseng2009coordinate`

- Citation: Paul Tseng and Sangwoon Yun. “A Coordinate Gradient Descent Method
  for Nonsmooth Separable Minimization.” *Mathematical Programming*,
  117(1-2):387-423, 2009.
- DOI/arXiv/URL: <https://doi.org/10.1007/s10107-007-0170-0>.
- Local PDF:
  `papers/2009-mp-tseng-coordinate-gradient-descent-nonsmooth-separable-minimization.pdf`.
- Relevance: This paper develops block coordinate gradient descent for a
  smooth objective plus a separable convex term. It provides a foundational
  convergence framework for local block choices, Gauss-Seidel or
  Gauss-Southwell selection, and error-bound-based linear convergence.
- Exact pointers:
  - Manuscript pages 4-9, Section 2: define the composite problem, block
    quadratic model, coordinate update, and admissible block-selection rules.
  - Manuscript pages 10-15, Section 3: characterize stationarity through the
    block displacement and establish the core comparison lemmas.
  - Manuscript pages 16-19, Section 4: prove global convergence of the method.
  - Manuscript pages 19-27, Section 5: use a local Lipschitzian error bound to
    derive local linear convergence.
  - Manuscript pages 27-31, Section 6: give error-bound conditions covering
    polyhedral regularizers and structured smooth terms.
- Formulation differences: The method permits general separable regularizers
  and block rules but does not impose a graph-local access model or count
  explored edges. Its linear rate is asymptotic and error-bound based, whereas
  this project uses an explicit PageRank residual and locality-sensitive work.
- Open questions: Express the hybrid solver's update as the paper's block
  model, determine whether its active-set rule satisfies the generalized
  Gauss-Southwell condition, and translate the local error bound into the
  repository's residual convention.

## Citation key: `tu2017breaking`

- Citation: Stephen Tu, Shivaram Venkataraman, Ashia C. Wilson, Alex Gittens,
  Michael I. Jordan, and Benjamin Recht. “Breaking Locality Accelerates Block
  Gauss-Seidel.” *Proceedings of the 34th International Conference on Machine
  Learning*, PMLR 70:3482-3491, 2017.
- DOI/arXiv/URL: <https://proceedings.mlr.press/v70/tu17a.html>; preprint
  <https://arxiv.org/abs/1701.03863>.
- Local PDF:
  `papers/2017-icml-tu-breaking-locality-accelerates-block-gauss-seidel.pdf`.
- Relevance: The paper shows that random coordinate blocks can outperform any
  fixed partition even without acceleration, then analyzes accelerated random
  block Gauss-Seidel through data-dependent parameters. This directly exposes
  the tradeoff between computational locality, block selection, and momentum.
- Exact pointers:
  - Preprint pages 1-4, Sections 1-2: define fixed-partition and random-block
    sampling and their convergence parameters.
  - Preprint pages 4-6, Section 3.1 and Propositions 3.1-3.3: construct
    instances where breaking the fixed partition gives an arbitrarily better
    rate.
  - Preprint pages 6-9, Section 3.2, Algorithm 1, and Theorems 3.4-3.7: give
    the Lyapunov analysis for accelerated block Gauss-Seidel and Kaczmarz.
  - Preprint pages 9-11, Section 3.3 and Lemma 3.8: specialize the accelerated
    rate to random coordinate sampling and well-conditioned sub-blocks.
  - Preprint pages 14-20, Section 5: compare sampling strategies,
    conjugate-gradient, and block sizes empirically.
- Formulation differences: The paper solves global positive-definite linear
  systems and treats locality primarily as cache locality. The project seeks
  seed-local graph diffusion with sparse state and edge-local work, so random
  blocks that touch the full coordinate universe may violate its locality
  objective.
- Open questions: Separate cache locality from graph locality in the work
  model, test whether random blocks can be sampled inside an evolving active
  set, and determine whether the paper's acceleration parameters can be
  bounded using local graph structure.

## Citation key: `odonoghue2015adaptive`

- Citation: Brendan O'Donoghue and Emmanuel Candès. “Adaptive Restart for
  Accelerated Gradient Schemes.” *Foundations of Computational Mathematics*,
  15(3):715-732, 2015.
- DOI/arXiv/URL: <https://doi.org/10.1007/s10208-013-9150-3>; preprint
  <https://arxiv.org/abs/1204.3982>.
- Local PDF:
  `papers/2015-focm-odonoghue-adaptive-restart-accelerated-gradient-schemes.pdf`.
- Relevance: This paper introduces function-value and gradient-based restart
  tests that reset momentum when observable behavior indicates overshoot. It
  is directly relevant to a hybrid solver that must decide online when
  acceleration is helping without knowing a global or local condition number.
- Exact pointers:
  - Pages 716-719, Sections 1-2 and Algorithms 1-2: review accelerated
    gradient schemes, their momentum parameters, and sensitivity to an
    inaccurate strong-convexity estimate.
  - Pages 719-722, Section 3 and Algorithm 3: derive the fixed restart scale
    and introduce the function and gradient adaptive restart conditions.
  - Pages 722-727, Section 4: analyze quadratic dynamics, observable
    oscillations, and convergence under adaptive restart.
  - Pages 727-731, Section 5 and Algorithms 4-6: demonstrate restart with
    log-sum-exp, FISTA for sparse regression, and projected acceleration for
    quadratic programming.
- Formulation differences: The adaptive rules are heuristic for general
  objectives, use global objective or gradient information, and do not track
  graph support or edge-local work. A local implementation may not have enough
  information to evaluate the published restart tests exactly.
- Open questions: Develop a restart signal from the repository's local
  residual, determine whether a restricted active-set objective is a reliable
  proxy for the global function test, and measure whether restart preserves
  sparse support while improving edge-operation complexity.

## Citation key: `lin2015universal`

- Citation: Hongzhou Lin, Julien Mairal, and Zaid Harchaoui. “A Universal
  Catalyst for First-Order Optimization.” *Advances in Neural Information
  Processing Systems 28*, pages 3384-3392, 2015.
- DOI/arXiv/URL:
  <https://proceedings.neurips.cc/paper/2015/hash/c164bbc9d6c72a52c599bbb43d8db8e1-Abstract.html>;
  preprint <https://arxiv.org/abs/1506.02186>.
- Local PDF:
  `papers/2015-neurips-lin-universal-catalyst-first-order-optimization.pdf`.
- Relevance: This is the original conference presentation of Catalyst. It
  wraps a linearly convergent base method around approximately solved,
  quadratically regularized subproblems and accelerates their outer sequence
  through extrapolation.
- Exact pointers:
  - Preprint pages 1-2, Section 1: define the composite objective and motivate
    acceleration of batch, coordinate, and finite-sum base methods.
  - Preprint pages 3-4, Section 2 and Algorithm 1: specify the auxiliary
    objectives, extrapolation, and inner accuracy schedule.
  - Preprint pages 4-7, Section 3, Theorems 3.1 and 3.3, and Propositions 3.2
    and 3.4: give outer convergence and inner-loop complexity for strongly
    convex and convex objectives.
  - Preprint pages 7-9, Section 4: instantiate Catalyst for existing methods
    and introduce proximal MISO.
- Relationship to other library entries: The 2018 JMLR paper
  `lin2018catalyst` is the expanded journal treatment, with more complete
  stopping-criterion, warm-start, and experimental analysis. This NeurIPS
  article is retained separately as the original formal publication.
- Formulation differences: Catalyst assumes globally defined composite
  subproblems and global inner accuracy certificates. The hybrid local solver
  also requires sparse support, seed locality, residual-based termination, and
  an edge-local work bound.
- Open questions: Determine whether the local solver supplies the required
  linear inner rate, translate its residual into the conference paper's
  function-gap schedule, and bound the work added by extrapolation and
  regularized auxiliary solves.
