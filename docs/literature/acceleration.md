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

These are project-only promoted results, not claims from the source papers
annotated in this file. The direction files remain authoritative for their
per-result review provenance:

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

## Project-only Round-020--021 reweighting, nonsettled-continuation, and causal-ledger boundaries

These are independently reviewed project results, not claims from the source
papers annotated in this file:

- Round 020 leaves the fixed-weight coded-bank regime. On one exact-real
  bucket with codes `00,01,10`, two source histories have identical complete
  retained decoder norms under unit weights but require opposite first-bit
  decisions after the positive inverse-slack refresh `(1,1,1)->(1,3,2)`.
  Proposition `prop:three-label-norm-only-reweight-obstruction` therefore
  makes the named norm-only state reject with vector
  `(0,0,1,0,Theta(1),0,0,Theta(1),Theta(1),0,1)`; a six-old-cell replay
  comparator has vector
  `(0,0,1,0,Theta(1),0,6,Theta(1),Theta(1),12,1)`. Round 021 gives the
  smallest matching repair for this bucket. `ThreeLabelPivotGramRefresh`
  stores canonical unweighted
  `S=(P_0,A_1,C_1,A_2,C_2)`, recovers
  `g_02=(C_1-P_0-A_2)/2` and `g_01=(C_2-P_0-A_1)/2`, and reconstructs every
  decoder norm at arbitrary positive weights. A weighted append first
  recovers its unweighted rows, so induction covers arbitrary positive
  append/refresh interleavings without source replay. The refresh vector is
  `(0,0,1,0,Theta(1),0,0,Theta(1),Theta(1),4,1)`. The repair is already sharp:
  codes `00,01,10,11` and histories `(-6,-5,-5,4)` and `(-6,-5,-5,6)` share
  `P_0=36` and `(A_1,C_1,A_2,C_2)=(1,121,1,121)`, but weights `(1,1,1,3)`
  give `49<121` versus `169>121`. General `CoSideGramRefresh` retains every
  Gram diagonal and an off-diagonal exactly when the two codes share a bit
  side. Only a complement-pair matching of size `c<=floor(k/2)` is omitted,
  so its explicit state dimension is
  `k+binom(k,2)-c=Theta(k^2)`. Necessity is qualified to linear explicit
  Gram-statistic states that reproduce all side norms on an open set; it is
  not an unrestricted real-cell lower bound. For `k>L+1`, the ordinary
  total-plus-`L`-bit measurements do not in general maintain the state:
  richer measurements or per-label reads, `Theta((k^2-c)r_new)` append
  arithmetic, and all response/materialization charges remain required.
  These bucket results prove no graph-work, RPPR chronology, terminal solve,
  finite-precision, word, or bit claim. The proof owner is
  `response_preconditioned_hybrid`, Proposition
  `prop:three-label-norm-only-reweight-obstruction`, Theorems
  `thm:three-label-pivot-gram-refresh` and `thm:co-side-gram-refresh`, and
  Proposition `prop:four-label-one-pivot-refresh-obstruction`.
- Round 020 supplies the first actual nonsettled branch-caterpillar
  continuation for `rho<min(rho_can(m,alpha),1/30)`. One shifted AESP stage
  ends strictly below the first-face optimum but has positive boundary
  margins; the carried primal, nonzero momentum, extrapolated center, and
  estimate point zero-pad across admission. A paid proximal warm start keeps
  its old cell and appends three positive cells. The two-product,
  twelve-cell `NonsettledShockRegister` computes an observable KKT budget
  `B_ns` that bounds the strictly positive enlarged-face estimate shock, and
  one relative-accuracy stage runs on `Uhat_1` before the native suffix.
  Round 021 reaches a second nonsettled admission in the sharper range
  `rho<min(rho_can(m,alpha),rho_2(m,alpha))`, where
  `rho_2=(1+beta_A)/(138+3beta_A)` for `m=2` and
  `(1+beta_A)/(354+3beta_A)` for `m>2`. The zero-padded extrapolated center
  `y+` is a strict lower point but has the wrong boundary signs and does not
  certify `F_1`; its standard proximal warm start `u_1(y+)` does. Locking the
  imported oracle to greedy normalized-KKT AESP-CD preserves
  `u_1(y+)<=z_1<=p_1(y+)<x_1`, so the actual output certifies the second
  batch. A second two-product, twelve-cell register computes fresh `B_2`, and
  one genuine extrapolated stage runs on `Uhat_2`. The exact prefix/post
  ledgers have total `R_int=m+1`, structural first exposure exactly `m+1`,
  and full `R_adj=m+1+O(A_2NS)`. No inequality relates `B_2` to `B_ns`, so
  this is a finite two-admission/two-continuation GO and an accelerated-rate
  STOP: it proves no estimate-shock amortization, multi-face contraction, or
  speedup. The greedy-policy, strict-margin, live-row, four-product,
  oracle-log, native-suffix, fixed-family, branch-seed, exact-real, non-PPR,
  and non-finite-precision restrictions remain. The proof owner is
  `hybrid_aesp_locsor`, Theorems
  `thm:branch-caterpillar-first-nonsettled-continuation` and
  `thm:branch-caterpillar-two-nonsettled-continuation` and their complete
  transition, prefix, and post vectors.
- Round 020 replaces the path-only TightPair bank by the face-general
  observable score `Xi=delta^2`. Its causal one-scalar ledger credits a score
  decrease or exact restricted-optimum drop only after that event is realized
  and charged, and debits every score increase. On the literal `q=1/5` path,
  a balance started at held stage 3 remains solvent through the consecutive
  stage-4 and stage-8 admissions and through stage 12; unused stage-4 Schur
  credit supplies the exact cross-state cancellation. If that earlier credit
  is discarded and the ledger restarts at stage 7, it remains negative
  through stage 11 and first becomes nonnegative at stage 12. The complete
  path vector is unchanged. Round 021 tests the hoped-for recovery-before-
  next-admission rule on the asymmetric six-vertex T tree with edges
  `(0,1),(1,2),(2,3),(2,4),(4,5)`, seed `0`, and
  `q=1/5`, `alpha=rho=tau=1/25`. Admissions occur at stages `1,2,4,9,15`
  and certification at `17`. Restarting at held stage 3 makes the ledger
  negative at stage 5 and still negative immediately before and after the
  next admission at stage 9; stage 13 is the last local STOP and stage 14 the
  first local GO. Thus the named recurrence and complete gate do not guarantee
  per-block recovery before the next admission. The result neither refutes an
  all-history balance nor proves convergence failure, a nonpath response
  vector, a global horizon, logarithmic/asymptotic work, alternate-order
  behavior, or finite precision. The finite no-smaller-witness enumeration is
  computational scaffolding only. The proof owner is
  `volume_gated_acceleration`, Propositions
  `prop:path-causal-two-admission-recovery` and
  `prop:t-tree-causal-next-admission-stop`.

## Project-only Round-027 weighted-reserve and spectral-transfer boundary

These are independently reviewed project results, not claims from the source
papers annotated in this file:

- Lemma `lem:aesp-cd-q-weighted-euclidean-reserve` applies directly to the
  actual finite safeguarded recurrence. Put
  `e_t=x*-x_t`,
  `omega_q^E=(1-q)^2 mu_E/(2q)`,
  `Psi_t^E=Phi_t^fin+omega_q^E||e_(t-1)||_2^2`, and
  `eta_t=2 kappa_A xi_t+kappa_A xi_t^2`. Then
  `Psi_(t+1)^E<=Psi_t^E-q Phi_t^fin+eta_t`. The exact comparison
  `Psi_t^E<=((1+q+q^2)/q)Phi_t^fin` gives only
  `Psi_(t+1)^E<=(1-q^2/(1+q+q^2))Psi_t^E+eta_t`. Thus the reserve absorbs
  every realized Euclidean correction defect without shadowing or deleting
  the finite error, but its graph-uniform drift yields `O(q^(-2))`, not
  accelerated `O(q^(-1))`, stages.
- Proposition `prop:aesp-cd-unsplit-q-energy-stagewise-stop` uses the lagged
  indexing that actually pairs a stage-`t` defect with its energy drop:
  `Psi_t^A=Phi_t+(A/q)E_(t-1)^Q`. On the reachable rational `K_8` family,
  direct absorption at harmful persistent stage 2 requires
  `A>14(1-q)kappa_A/197>=A_star`, where
  `A_star=6929307/98509850`.
- The complementary uniform-seed `K_2` family has full support from stage 1,
  so `P_1` is empty and `P_2` is full. The genuine persistent bank comparison
  is therefore `Psi_3^A/Psi_2^A`, for the transition out of stage `t=2`. Its
  exact component drops obey
  `1-Phi_3/Phi_2<=2q` and
  `1-E_2^Q/E_1^Q<=4q^2`, while the potential weight is at most `q/A` of the
  bank weight. Hence, for every `A>=A_star`,
  `0<=1-Psi_3^A/Psi_2^A<=(4+2/A_star)q^2`. No absolute `c>0` gives uniform
  one-step `1-cq` contraction for this bank while its coefficient is large
  enough for the `K_8` payment. The final independent audit returned clean
  after replacing the entry-stage `Psi_2/Psi_1` comparison by this persistent
  one.
- The `K_2` witness is not a net or additive-term obstruction. For `t>=1`,
  it satisfies
  `Psi_t^A/Psi_1^A<=(4/e)exp(-q(t-1))` and
  `Psi_1^A/Phi_0<=1+A/(q(1-q^2))`. An absolute `A` therefore costs only
  `O(log(q^(-1)))` in the startup normalization, within the allowed
  polylogarithmic term.
- The `K_8` obstruction is specifically unsplit. If `E_t^h` is its exact
  high-band energy, then the `mu_E`-weighted pulse payment divided by
  `q^(-1)(E_1^h-E_2^h)` tends to `14641/32256`. This proves compatibility
  only for that one pulse. In the general fixed-face filter, the low spectral
  projector is not positivity preserving and coordinatewise positive part
  does not commute with either spectral projector. Round 027 therefore proves
  no windowed spectral or nonlinear transfer, finite net exponent, exact
  accelerated solver, or resource vector. The live target is only a windowed
  spectrally split, nonlinear-transfer, or differently normalized persistent
  low-Dirichlet Lyapunov retaining every finite and implementation charge.

## Project-only Round-026 persistent energy banks and same-drop boundary

These are independently reviewed project results, not claims from the source
papers annotated in this file:

- Lemma `lem:aesp-cd-persistent-square-ledger` works on the actual finite
  recurrence. For `t>=2`, let
  `P_t=supp(x_t) intersect supp(x_(t-1))`, `e_t=x*-x_t`, `u_t=Qe_t`, and
  `E_t^Q=<e_t,Qe_t>`. On persistent rows the two finite end residuals combine
  into the exact fixed-row controller
  `g_(t,P_t)=[beta_A u_(t-1,P_t)-(1+beta_A)u_(t,P_t)]_+`, with
  `g_(t,P_t)<=beta_A[Qd_t]_(+,P_t)`. Thus every `2<=k<=ell` satisfies
  `sum G_t^per<=(beta_A(1+alpha)/2)m(x_ell-x_(k-1))`
  `<=beta_A(1+alpha)/2` and
  `sum (G_t^per)^2<=beta_A^2(E_(k-1)^Q-E_ell^Q)`. Assigning ties to the
  persistent class gives
  `alpha^2 sum Delta_t^2<=beta_A^2(E_(k-1)^Q-E_ell^Q)` over its
  persistent-dominated stages. These are realized finite-state identities;
  they neither erase residuals nor require exact shadowing or the dual inner
  stop.
- Lemma `lem:aesp-cd-truncation-q-energy` treats the moving cap in
  degree-normalized coordinates. For
  `r_t=D^(1/2)min{beta_A D^(-1/2)d_t,Delta_t 1}` and
  `p_t=beta_A d_t-r_t`, one has separately
  `<r_t,Qr_t><=beta_A^2<d_t,Qd_t>` and
  `<p_t,Qp_t><=beta_A^2<d_t,Qd_t>`. Each windowed sum is separately at most
  `beta_A^2(E_(k-1)^Q-E_ell^Q)`. The two left sides are not added beneath one
  copy of that bank. This is a boundary-aware scalar-truncation argument, not
  an ambient retraction Lipschitz estimate.
- Proposition `prop:aesp-cd-k8-reachable-pulse` realizes the Round-025 mixed
  event. On `K_8`, take `q=1/10`, `alpha=1/101`, `kappa_A=99/101`,
  `beta_A=9/11`, `rho=1/112`, and the normalized dense seed
  `(363437/651088,41093/651088,...,41093/651088)`. The exact recurrence has
  all-time word `N,N,P0,F,N^infinity`; the persistent partial stage 2 and full
  stage 3 both have `gamma_t^fin>1` before the `tau=1/1000` fresh gate, but all
  later corrections vanish. Hence, for `T>=4`,
  `J_T^fin=log(gamma_2^fin)+log(gamma_3^fin)<2log2`. This is a real but
  additive-constant transient, not an additive-resistant or net-rate
  obstruction.
- Proposition `prop:aesp-cd-k8-q-bank-stop` gives a one-window proof-route
  STOP. For rational `0<q<=1/100`, set
  `alpha=q^2/(1+q^2)`, `kappa_A=(1-q^2)/(1+q^2)`,
  `beta_A=(1-q)/(1+q)`, and `rho=1/112`. Its reachable persistent full stage
  satisfies
  `D_2^fin>28q(7/112^2)` and
  `E_1^Q-E_2^Q<197q^4(7/112^2)`. Raw payment by that same unsplit local
  `Q`-energy drop therefore needs more than `28/(197q^3)`, hence
  `Omega(q^(-3))=Omega(alpha^(-3/2))`; after multiplying by
  `mu_E=kappa_A q^2`, the same payment still needs `Omega(q^(-1))`. The
  result does not refute a `q^(-1)`-weighted, spectrally split, or differently
  normalized bank, an additive polylogarithmic allowance, the net exponent,
  or the solver.
- The independent exact audit returned clean after the infinite-tail proof
  was repaired to index later trials as `t=3+k`, `k>=1`. Their exact modal
  ratio is `(11/7)|H_(k+1)/L_(k+1)|`, and the maximal envelope multiplier is
  the checked value `5/6`. Round 026 proves no additive-resistant obstruction,
  graph-uniform `J_T^fin` exponent, exact accelerated solver, or resource
  vector. At the close of that round the target included a plain
  `q^(-1)`-weighted bank; Round 027 above stops its simplest lagged unsplit
  form. The surviving low-Dirichlet target is only a windowed spectrally split,
  nonlinear-transfer, or differently normalized persistent-row Lyapunov that
  retains every residual and implementation charge.

## Project-only Round-025 boundary shielding and post-full spectral filtering

These are independently reviewed project results, not claims from the source
papers annotated in this file:

- Lemma `lem:aesp-cd-support-entry-shield` analyzes the actual finite
  recurrence rather than the raw discontinuous retraction map. For `t>=2`,
  split `A_t=supp(x_t)` into new rows `E_t=A_t\A_(t-1)` and persistent rows
  `P_t=A_t intersect A_(t-1)`. The new-row first-retraction violation obeys
  `0<=g_(t,E_t)<=beta_A a_(t-1,E_t)` and
  `G_t^ent<=beta_A C_end,t-1`, while
  `alpha Delta_t=max(G_t^ent,G_t^per)`. It is exactly zero under exact shifted
  solves. For finite solves, an entry-dominated common correction satisfies
  `alpha Delta_t<=beta_A C_end,t-1`; support entry is controlled only by the
  preceding finite end residual.
- Lemma `lem:aesp-cd-one-sided-correction-excess` compares a finite correction
  to a residual-free driver at the same realized states. With
  `delta_t=(beta_A/alpha)||D_A_t^(-1/2)a_(t-1,A_t)||_infinity`, it gives
  `Delta_t<=bar_Delta_t+delta_t` and
  `0<=[r_t-bar_r_t]_+<=delta_t D^(1/2)1`. Under the combined
  C2-plus-absolute stop and `vol(A_t)<=V`, the corresponding momentum excess
  is at most `((1-q)/q)(mu_t/alpha)xi_(t-1)=O(xi/(alpha q))`.
  This comparison is one-sided: current residual and boundary multiplier
  terms can suppress the correction. It is neither an absolute
  trajectory-distance bound nor a finite-packing theorem.
- Corollary `cor:aesp-cd-entry-inflation-ledger` assumes `alpha<1/2`, a
  pre-gate prefix `H_rho(x_t)>alpha tau`, and
  `eta_gate=2 alpha tau/(1+alpha)`. The locally maintained heap target
  `C_end,t<=delta alpha eta_gate^2 q^2` makes each entry-dominated inflation
  at most `4 delta q` and their prefix sum at most `4 delta q T`, independent
  of the number of support entries. The same increasing greedy heap as C2
  maintains the exact end mass. Over `T=O_tilde(1/q)` stages on volume `V`,
  all updates and cached rekeys remain within `O_tilde(V/q)` charged work
  (`O_tilde(1/(rho q))` when `V<=1/rho`). This result supplies no resource
  vector because persistent-row-dominated stages remain uncontrolled.
- Proposition `prop:aesp-cd-post-full-high-pass` gives an exact local spectral
  identity for exact shifted solves on a settled positive face. If stage `t`
  is full, `ell_t=x_t`, and `Q_A e_t>=0`, then `r_(t+1)=0` and the stage-`t+2`
  collapse driver is
  `Q_A(Q_A+kappa_A I)^(-2)`
  `[beta_A(2+beta_A)Q_A-kappa_A I]e_t`. Its eigenmode coefficient is positive
  only above
  `lambda/kappa_A>(1+q)^2/((1-q)(3+q))`, so a single nonnegative low mode
  cannot retrigger there. Coordinatewise positive parts mix modes, however.
  The exact `K_8`, `q=1/10` vector in the proposition has `Q_Ae>0` and a
  positive filtered coordinate. Round 025 used it only as an algebraic filter
  stress test; Round 026 above realizes the same mixed event on an exact
  dense-seed safeguarded trajectory, but only as a two-pulse transient.
- These results remove entry-dominated inflation and finite-created
  same-state excess from the open low-Dirichlet branch. They do not establish
  a graph-uniform net exponent, graph-uniform solver, or Round-025 cached
  vector. Round 026 above adds residual-retaining persistent and truncation
  `Q`-energy windows, while leaving the weighted or spectrally split net charge
  open.

## Project-only Round-024 stability boundary and structural solver branch

These are independently reviewed project results, not claims from the source
papers annotated in this file:

- Proposition `prop:aesp-cd-retraction-shadowing-stop` gives an exact
  lower-retraction boundary on endpoint-seeded `P_2`. For `0<alpha<1/4`,
  `lambda=(1+alpha)/2`, `nu=(1-alpha)/2`, and `rho=nu/4`, support entry at
  `(alpha/8,0)` is discontinuous: `L(alpha/8,0)=(alpha/8,0)`, whereas
  `L(alpha/8,eta)=0` for every `eta>0`. On a fixed positive full support the
  sharp infinity-norm Lipschitz factor is `1+1/alpha`. Iterating this ambient
  factor in an exact-to-finite shadow proof forces exponentially small local
  tolerances and inserts a `V T^2 log(1/alpha)` term into the certified inner
  ledger. This is a STOP only for ambient black-box trajectory shadowing. It
  proves neither instability of the actual finite recurrence nor failure of
  a direct finite-sequence net exponent.
- Lemma `lem:aesp-cd-full-correction-separation` uses the fixed operator on a
  settled optimal face. Assume
  `A=S*(rho)`, `supp(x_t)=A`, `ell_t=x_t`, and
  `Q_A(x*-x_t)>=0`. With
  `M_A=kappa_A(Q_A+kappa_A I)^(-1)` and
  `S_A=(1+beta_A)M_A-beta_A I`, one has
  `S_A >= q beta_A I` spectrally, `S_A>=0` entrywise, and
  `S_A Q_A=Q_A S_A`. If the solve after that full center is exact,
  `x_(t+1)=p(x_t)`, its next extrapolate needs no correction. For a finite
  shifted output after the same center that remains positive on `A` and zero
  off `A`, any adjacent correction is caused only by its end residual:
  `alpha Delta_(t+1) <= 2(1-q)||D_A^(-1/2)a_(t+1)||_infinity`
  `<=2(1-q)C_end,t+1`. This does not bound the density or cumulative
  inflation of partial corrections.
- Theorem `thm:aesp-cd-high-dirichlet-branch` bypasses inflation packing on a
  promised structural class. Let the optimal support `A` be nonempty and
  define
  `lambda_A=lambda_min(Q_A)` and
  `theta_A=lambda_A/(kappa_A+lambda_A)`. Each actual finite safeguarded stage
  with `||p(ell_t)-x_(t+1)||_2<=xi_t` satisfies
  `||x*-x_(t+1)||_2 <= (1-theta_A)||x*-x_t||_2+xi_t`. If
  `theta_A>=c_0 q` for an absolute `c_0>0`, choose
  `eta_gate=2 alpha tau/(1+alpha)`,
  `xi_t<=c_0 q eta_gate/2`, and
  `T>=(c_0 q)^(-1)log(2/eta_gate)`. Then `x_T` passes the fresh unshifted
  gate `H_rho(x_T)<=alpha tau` and has RPPR error at most `tau`, with no
  assumption on `J_T^fin`.
- In the accelerated arm `alpha<1/4`, setting
  `rho=tau=eps_ppr/2` gives total degree-normalized PPR error at most
  `eps_ppr` on this promised class. The cached implementation has the
  unconditional-on-the-promise vector
  `(O(V_eps),O(V_eps),1,0,O(W_eps),O(W_eps),0,O(V_eps),O(V_eps),`
  `O(W_eps),Theta(k+1))`, where `V_eps=nnz(s)+2/eps_ppr`,
  `W_eps=nnz(s)+O_tilde(1/(sqrt(alpha) eps_ppr))`, `k<=2/eps_ppr`, and
  `C_resp=0`. The promise depends on the unknown optimal face, so it is
  a-posteriori, not algorithmically certified, and not graph-uniform. The
  unresolved Route-B branch was the actual-finite net exponent or an
  equivalent direct rate on low-Dirichlet families `theta_A=o(q)`. Round 025
  above removes entry-dominated stages from that blocker. Round 026 adds exact
  persistent and boundary-aware `Q`-energy windows, but its small-`q` family
  stops alpha-independent payment by the same unsplit drop. Round 027 further
  shows that the exact Euclidean reserve has only `q^2` drift and stops
  uniform one-step accelerated contraction for the simplest lagged unsplit
  `q^(-1)Q` reserve. Only a windowed spectrally split, nonlinear-transfer, or
  differently normalized persistent Lyapunov remains live. No graph-uniform
  exact-real accelerated `eps_ppr` solver is proved.

## Project-only Round-023 infinite-inflation and finite-inner boundaries

These are independently reviewed project results, not claims from the source
papers annotated in this file:

- On endpoint-seeded `P_4` with `q=1/8`, `alpha=1/65`, and `rho=7/40`,
  Proposition `prop:aesp-cd-p4-infinite-inflation` proves an exact rational
  invariant cone for the fixed RPPR operator. From stage 44 the safe recurrence
  repeats `F N N F N^6 P0` on its settled support. The second full correction
  in each eleven-stage word has log inflation at least `315/33280`, and
  therefore `I_(44+11N)>=(315/33280)N` and `I_T=Theta(T)`. Nevertheless, the
  degree-scaled primal error contracts by at most `11/500` per word. This
  project theorem refutes horizon-uniform, fixed-support/fixed-parameter, and
  transient-only bounds on harmful inflation. Because convergence is
  geometric, it does not refute accuracy-logarithmic or polylogarithmic
  dependence on `epsilon^(-1)`. Because `q=1/8` is fixed, it gives no small-`q`
  obstruction and does not refute a net exponent such as
  `I_T<=(1-c)qT+B`. The theorem uses ideal exact shifted minimizers and gives
  no finite-inner implementation or end-to-end work result.
- Lemma `lem:aesp-cd-finite-inner-identities` identifies the exact perturbation
  caused by terminating a monotone shifted coordinate solve. Its positive
  residual `a_t` enters the fixed-row relation, contributes the end mass to
  the next start mass, and forces the following momentum-collapse identity.
  Proposition `prop:aesp-cd-c2-residual-stop` gives a scalar quadratic that
  satisfies the standard relative C2 condition at equality while retaining a
  nonzero residual of relative order `Theta(sqrt(q))`. Thus no exact-tail
  argument transfers to finite inner outputs through C2 alone. Corollary
  `cor:aesp-cd-dual-inner-stop` adds the absolute condition
  `C_end<=mu_t xi/sqrt(V)`; together with C2 it gives shifted-solution error at
  most `xi` and costs only a logarithmic extra inner-work factor.
- The accelerated implementation ledger is explicitly conditional. If the
  **actual finite** trajectory satisfies
  `J_T^fin<=(1-c)qT+B` for declared `c,B`, then computable `T` and `xi` reach
  a fresh unshifted gate. For the displayed product-work vector, additionally
  require the frozen accelerated regime `alpha<1/4`, an absolute
  `c>=c_0>0`, and
  `B=polylog(alpha^(-1),eps_ppr^(-1),V_eps)`. The RPPR bias comparison with
  `rho=tau=eps_ppr/2`, cached adjacency rows, shifted-key rekeys, final gate
  materialization, and output then give the conditional eleven-vector
  `(O(V_eps),O(V_eps),1,0,O(W_eps),O(W_eps),0,O(V_eps),O(V_eps),`
  `O(W_eps),Theta(k+1))`, where `V_eps=nnz(s)+2/eps_ppr`,
  `W_eps=nnz(s)+O_tilde(1/(sqrt(alpha) eps_ppr))`,
  `k<=2/eps_ppr`, and `C_resp=0`.
  Correctness of the fresh gate, the cache accounting, and the
  `1/4<=alpha<=1` zero-start `O(1/eps_ppr)` fallback do not require the
  packing premise; the fallback vector uses
  `W_eps=nnz(s)+O(1/eps_ppr)`. At the close of Round 023 the accelerated rate
  and vector still required the stated premises everywhere. Round 024 above
  removes that premise on the promised high-Dirichlet structural class. Round
  025 above further shields entries and isolates persistent-row mixed-mode
  partial corrections. Round 026 adds exact actual-finite `Q`-energy banks and
  the same-unsplit-drop STOP. Round 027 stops the plain lagged unsplit
  `q^(-1)Q` stagewise proof while showing that its low-mode witness is not a
  net obstruction; only a windowed spectrally split, nonlinear-transfer, or
  differently normalized argument remains live on low-Dirichlet faces. No
  graph-uniform exact-real accelerated `eps_ppr` solver is proved.

## Project-only Round-022 reset-budget and fixed-operator inflation boundaries

These are independently reviewed project results, not claims from the source
papers annotated in this file:

- The frozen end-to-end target is an exact-real adjacency-list algorithm on
  finite simple undirected unweighted graphs without isolates and with a
  sparse nonnegative seed. For `x^0=Q^(-1)b`, `pi=D^(1/2)x^0`, and
  `pi_hat=D^(1/2)x_hat`, it must return sparse `x_hat` with
  `max_i |pi_hat_i-pi_i|/d_i<=eps_ppr`, one complete terminal certificate and
  return, and fully charged work
  `nnz(s)+O_tilde(1/(sqrt(alpha) eps_ppr))`. An RPPR route must state its
  conversion, for example `rho=tau=eps_ppr/2`, and terminal certificate; for
  constant-lower-bounded `alpha`, monotone coordinate descent may be the
  fallback. This is an audit target in the algebraic exact-real model, not a
  proved theorem, exact-minimizer guarantee, or finite-precision/bit result.
- Route A's endpoint-seeded settled `P_3` has
  `B_1/Delta_1=3/(4q_r^2)+O(1)`, where
  `q_r^2=alpha/(1-alpha)`. It therefore refutes alpha-uniform and
  `O(1/q_r)` additive payment of the declared observable reset budget by the
  exact admission drop. The general settled upper coefficient has sharp order
  `Theta(1/alpha)`, while a separate conditional nested telescope has
  coefficient `Theta(alpha^-2)` and assumptions absent from the Round-021
  nonsettled greedy trace. The obstruction is not a shock or work lower bound:
  the actual settled analytical shock is below `2Delta`, and relative stage
  work sees the initial budget logarithmically. If the conservative
  no-sharing two-product caterpillar register is invoked literally at all `m`
  canonical admissions, it reads exactly
  `2 sum_(j=1)^m V_j=6m^2+12m-6` stored-row cells. Sharing or another
  representation may avoid that named-interface cost. The proof owner is
  `hybrid_aesp_locsor`, Proposition
  `prop:path-three-settled-reset-drop-obstruction`, Lemma
  `lem:settled-reset-optimum-drop-bound`, Proposition
  `prop:conditional-nested-reset-budget-telescope`, and
  `eq:branch-caterpillar-literal-reset-product-count`.
- Route B's abstract self-similar sequence satisfies the current scalar safe-
  chain, start-mass, correction-mass, collapse, defect, and defective-
  contraction ledgers but, over `Theta(q^-2)` steps, permits
  `I_T=Omega(q^-1)` with only constant logarithmic potential progress. Hence
  those scalar ledgers alone cannot prove the desired accelerated-scale
  inflation packing. The sequence is not RPPR or an exact-proximal trajectory
  and omits the fixed Stieltjes operator and coupled boundary complementarity.
  Conversely, an exact endpoint `P_4` recurrence has stable optimal support
  from stage 7 and positive inflation through stage 498; an exact
  corroborating `P_7` trace has stable optimal support from stage 9 and
  positive inflation through stage 796. The finite traces refute attribution
  solely to support additions and eventual post-discovery disappearance, but
  prove no infinite recurrence, exponent, asymptotic obstruction, finite-inner
  theorem, or end-to-end lower bound. The proof owner is
  `aesp_cd_l1_rppr`, Propositions
  `prop:aesp-cd-ledger-only-insufficient` and
  `prop:aesp-cd-p4-late-inflation`, with the `P_7` trace retained as exact
  corroborating scaffolding.

At the close of Round 022, the Route-B obligation was a fixed-operator
multistep spectral/boundary packing of cumulative `I_T` using
`Q e_t=kappa_A s_t` and inactive-row complementarity, followed by finite-inner
robustness and a fully charged terminal PPR certificate/output. Round 023
supersedes that live target: the fixed-`P4` exact tail has unbounded harmful
inflation. Round 024 narrows the surviving obligation further by closing the
  promised high-Dirichlet branch, and Round 025 removes entry-dominated stages.
  Round 026 adds the persistent and truncation `Q`-energy windows and proves
  that the same unsplit drop cannot absorb the raw small-`q` defect with an
  alpha-independent coefficient. Round 027 proves that the residual-retaining
  Euclidean reserve has only `q^2` drift and that the simplest lagged unsplit
  `q^(-1)Q` reserve cannot contract every genuine persistent stage at rate
  `cq`, without producing a net obstruction. The current obligation is only
  a windowed spectrally split, nonlinear-transfer, or differently normalized
  persistent-row low-Dirichlet Lyapunov. This route has `C_resp=0`; no
  additive-resistant obstruction, graph-uniform exact-real accelerated
  `eps_ppr` solver, or Round-027 vector is proved.

## Project-only Round-019 batched, settled-auxiliary, and recovery-block boundaries

These are independently reviewed project results, not claims from the source
papers annotated in this file:

- On the frozen notched-double-sun template and the complete declared positive
  per-column schedules of Round 018, a nonempty simultaneous batch may contain
  arbitrary labels and columns and several consecutive occurrences of one
  cell. Each touched cell must provide exactly its next gap-free tagged block,
  and `NotchedSunBatchAmplitudeDelta` validates every header, tag, amplitude,
  cap, stream identity, and same-record signed pair before mutation. At the
  successful boundary it emits exactly
  `{(q,i):c_(q,i)^(h-1)<k*_(q,i)<=c_(q,i)^h}` and one certificate for each
  affected column. No within-batch chronology or subevent crossing is defined.
  With `B` accepted batches,
  `S_Sigma=sum_h |{q:sum_i b_(h,q,i)>0}|`, logical total `L_Sigma`, and
  `b_max=max_h sum_(q,i)b_(h,q,i)`, one has
  `B<=S_Sigma<=L_Sigma` and `b_max<=L_Sigma`, and the vector is
  `(Theta(n),2,B,Theta(n+J+p+L_Sigma),Theta(C_frag+L_Sigma),0,0,`
  `Theta(n+J+p+L_Sigma),O(b_max),0,Theta(S_Sigma+rn))`.
  Nonnegative mode has `(p,C_frag,absolute mass)=(r,L_Sigma,A_Sigma)`;
  signed `2-minus-1` mode has `(2r,2L_Sigma,3A_Sigma)` with atomic
  same-column, same-label, same-tag pairs. An invalid attempted batch of
  `b_hat` supplied records adds its own interaction, staging, validation,
  `O(1+b_hat)` scratch, and rejection-output charge
  without a persistent write. The result retains the fixed graph, face, cut,
  ladder, pairing, fixed `n`, complete declared finite positive schedules,
  per-column margins, exact column separation, exact-real arithmetic, and
  atomic signed pairing. It covers neither hidden within-batch chronology,
  undeclared or unbounded mass, arbitrary signed logical amplitudes, split
  signed pairs, coupled response, arbitrary fragment support, incomplete
  labels, template/ladder mutation, RPPR chronology, fixed-`alpha` uniformity,
  terminal solving, nor finite-precision/word/bit costs. The proof owner is
  `response_preconditioned_hybrid`,
  `thm:notched-sun-batched-columnwise-amplitude-delta-reporter` and
  `eq:notched-sun-batch-eleven-vector`.
- On the fixed strict-range branch caterpillar, Round 019 tests imported
  composite/AESP auxiliary state only at a settled zero-momentum checkpoint.
  The center, momentum, and estimate-point arrays zero-pad exactly. The
  enlarged-face proximal map retains every old entry but appends exactly the
  three strictly positive values `g_(k,v)/L_A`. Thus `SettledAuxAppend` writes
  twelve coordinate cells across the four explicit arrays plus one reset
  marker, with standalone vector
  `(0,0,0,0,O(1),O(1),0,Theta(C_(k+1)^can),O(1),12+Theta(1),0)`;
  it performs no old-coordinate write, old-row/product/query, adjacency
  access, or response call. The inherited analytical estimate certificate
  does not carry for free: its enlarged-face shock satisfies
  `Sigma_k^es>=(mu_E/2) sum_(v in F_k)(x_(k+1))_v^2>0`, so the proof must be
  restarted or the shock explicitly bounded and charged. The concrete
  response-assisted `FirstAuxShock-BC-AESP_(1->2)` prefix is
  `(9+nu_1,3,2,0,O(1),O(1),O(1),O(C_2),O(C_2),Theta(C_2),`
  `6+Theta(2))`, followed by the paid native suffix
  `(vol(S*\Uhat_2),m-2,m-1,0,O(C(S*)),0,`
  `O(C(S*)+(m-2)log(2+m)),Theta(C(S*)),O(C(S*)),Theta(|S*|),`
  `|S*\Uhat_2|+|S*|+Theta(m-1))`. The audit performs no accelerated stage
  after the append. It proves neither a speedup nor amortization of the shock
  along actual nonsettled momentum states, and it retains candidate-row
  pre-exposure, missing products, margins, fixed-family/strict-range,
  branch-seed, delta-interface, exact-real, non-PPR, and non-finite-precision
  restrictions. The proof owner is `hybrid_aesp_locsor`,
  `lem:branch-caterpillar-settled-proximal-append`,
  `prop:branch-caterpillar-zero-estimate-carry-fails`,
  `thm:branch-caterpillar-first-auxiliary-shock-handoff`, and its transition,
  prefix, and post vectors.
- On the literal exact `q=1/5` path, retain the Round-018 held, production,
  reset, and follow-up boundaries and define
  `R_(9:k)^post=Psi_9-Psi_k` only from squared-bank decreases actually realized
  on the fixed face `U_4`. At the tight pair,
  `Psi_9=Psi_10>Psi_11>Psi_12>Psi_7>Psi_13`: the reserve is insufficient
  through stage 12 and first closes the reviewed endpoint deficit at stage 13.
  The rectangle extension uses the repaired variable-bank notation
  `b_7(c_3)=delta_7+c_3 q^(-1)e_7(U_3)` and
  `b_13(c_4)=delta_13+c_4 q^(-1)e_13(U_4)`. Exactly,
  `partial_(c_3)(Psi_13-Psi_7)<0` and
  `partial_(c_4)(Psi_13-Psi_7)>0`, so the tight pair maximizes the endpoint
  change and only the `7->13` GO is uniform over the held-pair-feasible
  rectangle. The two adjacent failures remain rectangle-uniform; the positive
  `7->9` net remains tight-pair-only and is not sign-uniform. The complete
  vector remains
  `(Theta(9),Theta(5),1,0,Theta(114),Theta(114),Theta(114),Theta(9),`
  `O(9),Theta(114),Theta(9))`. The recovery reserve is an analytical
  after-the-fact telescope, not free state or advance credit. This finite
  exact-real single-admission block supplies no pointwise potential, online
  face-general closing rule, multi-admission telescope, global horizon,
  logarithm or asymptotic conclusion, nonpath result, alternate-order claim,
  or finite-precision theorem. The proof owner is
  `volume_gated_acceleration`, `prop:path-tight-pair-recovery-block` and
  `eq:path-tight-pair-recovery-eleven-vector`.

## Project-only Round-018 columnwise, face-carried, and local-chain boundaries

These are independently reviewed project results, not claims from the source
papers annotated in this file:

- On the frozen notched-double-sun template, every logical column `q` may now
  declare its own finite positive label/amplitude schedules. The global input
  may arbitrarily interleave one event from any column, while the two physical
  streams of a signed `2-minus-1` logical column remain atomically paired.
  `NotchedSunColumnAmplitudeDelta` uses a column-specific capacity crossing,
  pre-crossing gap, and local mass horizon
  `F_(q,i)=A_q-A_(q,i)+A_(q,i,k*_(q,i)-1)`, with positive per-column margin
  `m_q`. Unrelated events enlarge only the asynchronous event horizon; they
  do not alter response column `q` or enter its mass bound. Consequently the
  affected column alone receives an updated certificate, and all `rn` cells
  are emitted at their first exact crossings. With
  `L_Sigma=sum_q L_q>=rn`, the vector is
  `(Theta(n),2,L_Sigma,Theta(n+J+p+L_Sigma),Theta(C_frag+L_Sigma),0,0,`
  `Theta(n+J+p+L_Sigma),O(1),0,Theta(L_Sigma))`. Nonnegative mode has
  `p=r,C_frag=L_Sigma` and absolute physical mass `A_Sigma`; atomically paired
  signed mode has `p=2r,C_frag=2L_Sigma` and mass `3A_Sigma`. No response, slack,
  numerical materialization, or other-column recertification is credited.
  The fixed face/cut/ladder/pairing, fixed `n`, declared bounded positive
  mass, complete coverage, per-column schedule-derived band, and exact-real
  model remain. Undeclared or unbounded mass, arbitrary signed logical
  amplitudes, split signed interactions, simultaneous batches, arbitrary
  fragment support, RPPR chronology, fixed-`alpha` uniformity, and finite
  precision remain open. The proof owner is `response_preconditioned_hybrid`,
  `thm:notched-sun-columnwise-amplitude-delta-reporter` and
  `eq:notched-sun-columnwise-amplitude-eleven-vector`.
- On the fixed strict-range branch caterpillar,
  `FaceCarryLowerHeap-BC-AESP_(0:q)` zero-pads each successful signed endpoint,
  so every old raw lower residual and heap key survives exactly and the three
  retained candidate rows create exactly three new keys. Heap-maximum
  range-minimum tags and flush-before-write markers represent every old lower
  anchor coordinate without an admission-time old-face read or eager copy.
  For fixed `2<=q<=m`, the response-free prefix vector is
  `(V_q^can+O(A_<q^fc),q+1+O(A_<q^fc),q,0,O(H_<q^fc),`
  `O(A_<q^fc + Q_<q^fc + q),0,O(C_q^can),O(C_(q-1)^can),`
  `O(D_<q^fc),3q+Theta(q))`; the paid post vector is
  `(vol(S*\Uhat_q),m-q,m-q+1,0,O(C(S*)),0,`
  `O(C(S*)+(m-q)log(2+m)),Theta(C(S*)),O(C(S*)),Theta(|S*|),`
  `|S*\Uhat_q|+|S*|+Theta(m-q+1))`. Thus `R_int=m+1` exactly, while
  `R_adj=m+1+O(A_<q^fc)` retains numerical row touches and every missing bulk
  endpoint product. Candidate rows remain pre-exposed and fresh accelerated
  auxiliaries remain charged; the named `DenseFreshAESP` interface writes
  `q(3q-1)/2` coordinate records and is quadratic when `q=m`. This is no
  speedup, accelerated-energy transport, class lower bound, graph-uniform
  theorem, finite-precision result, or PPR conversion. The proof owner is
  `hybrid_aesp_locsor`, `lem:branch-caterpillar-incremental-face-transition`,
  `thm:branch-caterpillar-incremental-face-handoff`, and its prefix/post
  eleven-vectors.
- On the literal exact `q=1/5` path, the complete chain
  `7->8^-->8^+->9` stops the immediate pointwise extension of the Round-017
  squared bank plus remaining-optimum-drop reserve. The account rises on the
  fixed-`U_3` candidate-production step, falls across the paid stage-8 reset,
  rises on the first fixed-`U_4` follow-up, and at the tight endpoints has
  positive net stage-7-to-9 change. Moreover, production nonincrease requires
  `c_3<=2103479690463/41819574955745<c_3^tight`, whereas follow-up nonincrease
  requires
  `c_4>=2617155474971384896/14508305905763575885>c_4^tight`. Hence every pair
  in the held-pair-feasible rectangle passes the reset but fails both adjacent
  fixed-face comparisons; the net sign is not uniform over that rectangle.
  The vector remains
  `(Theta(9),Theta(5),1,0,Theta(114),Theta(114),Theta(114),Theta(9),`
  `O(9),Theta(114),Theta(9))`. This finite exact-real local-chain STOP does
  not refute longer blocks, added production reserves, cross-state
  cancellation, aggregate potentials, other coefficient rules, or any
  global, logarithmic, asymptotic, nonpath, alternate-order, or finite-
  precision claim. The proof owner is `volume_gated_acceleration`,
  `prop:path-tight-pair-local-chain-stop` and
  `eq:path-tight-pair-local-chain-eleven-vector`.

## Project-only Round-017 amplitude, implicit-diagnostic, and squared-reset boundaries

These are independently reviewed project results, not claims from the source
papers annotated in this file:

- On the same frozen notched-double-sun template, fixed `n>=5`,
  `eta in (0,1/8)`, face, cut, pairing, ladder, exact-real cells, and common
  cross-stream interleaving,
  `NotchedSunAmplitudeDelta` replaces unit logical amplitudes by one declared
  finite positive occurrence schedule. Let `k_i*` be the first per-label
  prefix mass above
  `kappa_i=d_(u_i)(1+c_eta)sqrt(vartheta)`, set
  `gamma_i=kappa_i-A_(i,k_i*-1)` and
  `F_i=A-A_i+A_(i,k_i*-1)`, and require
  `m_A=min_i(lambda_i gamma_i-epsilon F_i)>0`. Then every unseen or
  seen-but-unreported label is at most `g-m_A`, while occurrence `k_i*` is its
  first exact strict crossing for every allowed common interleaving. The
  vector is
  `(Theta(n),2,L,Theta(n+J+p+L),Theta(C_frag+rL+L+n),0,0,`
  `Theta(n+J+p+L),O(1),0,Theta(rL))`, with
  `p=r,C_frag=rL` and absolute mass `rA`, or
  `p=2r,C_frag=2rL` and absolute mass `3rA`. There is no response/slack state,
  future-label scan, or numerical materialization. Every fixed finite
  positive schedule passes at sufficiently small positive `vartheta`; failure
  of the displayed margin rejects only this certificate. Undeclared or
  unbounded mass, arbitrary signed logical amplitudes, per-column schedules,
  batches, arbitrary fragment supports, RPPR chronology, fixed-`alpha`
  uniformity, and finite precision remain outside scope. The proof owner is
  `response_preconditioned_hybrid`,
  `thm:notched-sun-amplitude-delta-reporter` and
  `eq:notched-sun-amplitude-eleven-vector`.
- On the fixed strict-range branch caterpillar,
  `ImplicitLowerHeap-BC-AESP_(0:q-1)` stores the raw lower residual and a
  normalized-negative maximum heap. A coordinate write rekeys only its closed
  in-face neighborhood, and a complete query reads that maximum plus the three
  cached boundary parents without an old-face scan or lower-vector
  materialization. The response-free prefix vector is
  `(V_q^can+O(S_<q^row+A_<q^ih),2q+1+O(A_<q^ih),q-1,0,`
  `O(H_<q^ih),O(D_<q^ih),0,O(C_q^can),O(C_(q-1)^can),`
  `O(D_<q^ih),Theta(q))`; its direct suffix pays the same native response and
  exact output as Round 016. The policy nevertheless charges
  `S_<q^row=3q^2` initialization work and
  `S_<q^adm=(q-1)(3q+2)/2` transported-anchor writes, pre-exposes candidates,
  and restarts every AESP auxiliary. This is an exact incremental-diagnostic
  GO, not a class lower bound, accelerated-energy transfer, speedup,
  graph-uniform theorem, finite-precision result, or PPR conversion. The proof
  owner is `hybrid_aesp_locsor`,
  `lem:branch-caterpillar-implicit-lower-heap` and
  `thm:branch-caterpillar-implicit-lower-handoff`.
- On the literal exact `q=1/5` path, the tight coefficients
  `c_3=2978273417354/42112483166425` and
  `c_4=95554102960761584/1567701294665491845` make the scalar bank flat on
  held pairs `6->7` and `9->10`. At the frozen stage-8 reset the raw linear
  switch exceeds the exact restricted-optimum drop
  `Delta_8=175006441/6398713140625`, so the unit linear rule stops. The
  squared-bank switch is strictly smaller, so `Psi=b^2+H_j`, with
  `H_3=Delta_8,H_4=0`, decreases across that isolated reset. The tight pair
  maximizes the reset jump over its locally feasible coefficient rectangle.
  The complete run and vector remain
  `J=4,T=16,nu_fin=9,n_fin=5,V_swept=114` and
  `(Theta(9),Theta(5),1,0,Theta(114),Theta(114),Theta(114),Theta(9),`
  `O(9),Theta(114),Theta(9))`. Held evolution and reset are separate: this is
  no every-held-pair result, online coefficient rule, global potential,
  multi-admission telescope, block horizon, logarithm removal, asymptotic,
  nonpath, or finite-precision claim. The proof owner is
  `volume_gated_acceleration`, `prop:path-tight-pair-schur-bank` and
  `eq:path-tight-pair-schur-bank-eleven-vector`.

## Project-only Round-016 multiplicity, transported-lower, and no-constant boundaries

These are independently reviewed project results, not claims from the source
papers annotated in this file:

- `NotchedSunMultiplicityDelta` removes exactly the no-repetition promise from
  the preceding frozen-template reporter, still with fixed `n>=5` and
  `eta in (0,1/8)`. Declare
  `mu=(mu_1,...,mu_n) in N_(>=1)^n`,
  `L=sum_i mu_i`, and `H=L-min_i mu_i`, then require
  `vartheta=(1-alpha)/2` to satisfy
  `18H sqrt(vartheta)+3vartheta<=1`, equivalently
  `vartheta<=(sqrt(81H^2+3)+9H)^(-2)`. Here `L`, not a maximum
  multiplicity, is the authoritative interaction and fragment horizon, while
  `H` is the exact latest time at which an unseen label can remain. Every
  stream must still name the same label and carry the exact nonnegative unit
  or signed `2-minus-1` amplitude on the verified fixed template. One
  exact-cell counter per label enforces the declared cap atomically. A first
  occurrence emits the matching delta; a repeat emits no delta because its
  label was already reported; every accepted event emits one universal
  future-safe certificate per logical column. The complete vector is
  `(Theta(n),2,L,Theta(n+J+p),Theta(C_frag+rL+n),0,0,`
  `Theta(n+J+p),O(1),0,Theta(rL))`, with `p=r,C_frag=rL` for
  nonnegative columns and `p=2r,C_frag=2rL` for separately checked signed
  streams. There is no response application, future-label scan, response or
  slack state, or numerical materialization. The exact-cell GO still fixes
  the face, cut, label pairing, complete ladder, fixed `n`, unit amplitudes,
  one common declared multiset schedule, multiplicity-dependent near-one
  scale, and exact-real arithmetic. The displayed root is sharp only for this
  uniform scalar Neumann envelope, not a lower bound on every reporter. It
  does not cover unbounded or undeclared
  repetitions, omitted labels in a completed epoch, different per-column
  orders, batches, arbitrary fragments/amplitudes, template mutation, RPPR
  chronology, fixed-`alpha` uniformity as `L` grows, terminal solving, or
  coefficient-bit, word-RAM, rounding, or finite-precision costs. The proof
  owner is `response_preconditioned_hybrid`,
  `thm:notched-sun-multiplicity-delta-reporter` and
  `eq:notched-sun-multiplicity-eleven-vector`.
- On the fixed strict-range branch caterpillar, principal Stieltjes face
  monotonicity proves `x_(k+1)|_(Uhat_k)>=x_k`; therefore zero padding any
  charged lower point `y_k<=x_k` on the newly admitted batch remains below
  `x_(k+1)`. The anchored retraction
  `T_(k,a)(z)=a vee L_(Uhat_k)(z)` preserves every old lower coordinate and
  keeps conservative tree-boundary demands. For fixed `m>=2`, branch seed
  `s=e_(b_1)`, `alpha<1/2`, `rho<rho_can`, and every fixed `2<=q<=m`,
  `TransportLower-BC-AESP_(0:q-1)` uses this invariant through `q-1` actual
  admissions and certifies batch `q`. Before interaction `q`, its exact
  response-free vector is
  `(V_q^can+O(A_<q^tr),q+1+O(A_<q^tr),q-1,0,O(H_<q^tr),`
  `O(A_<q^tr),0,O(C_q^can),O(C_(q-1)^can),O(D_<q^tr),Theta(q))`.
  Response-freedom ends there. The direct suffix consumes the certified
  batch, builds and settles the native response on `Uhat_q`, and has vector
  `(vol(S*\Uhat_q),m-q,m-q+2,0,O(C(S*)),0,`
  `O(C(S*)+(m-q+1)log(2+m)),Theta(C(S*)),O(C(S*)),Theta(|S*|),`
  `|S*\Uhat_(q-1)|+|S*|+Theta(m-q+2))`. The interaction coordinates sum to
  exactly `m+1`, and total work is
  `O(H_<q^tr+C(S*)log(2+C(S*)))`. This transports only a coordinatewise
  lower anchor: every momentum, proximal, center, and estimate-sequence
  record is restarted, every candidate row is pre-exposed, every test pays a
  full growing-face sweep, and the analysis retains its margin and
  `log(1/(1-2alpha))` factors. It is a fully charged comparison, not
  transported acceleration, a sublinear diagnostic, a speedup, automatic
  locality, a graph-uniform or other-range theorem, finite precision, or PPR
  conversion. The proof owner is `hybrid_aesp_locsor`,
  `lem:branch-caterpillar-anchored-lower-transport`,
  `thm:branch-caterpillar-transported-lower-handoff`, and its two vectors.
- On the literal exact `q=1/5`, `alpha=rho=tau=1/25`
  transported-center endpoint-path chronology, consider the entire constant
  family `Phi_t(c;U)=delta_t+c q^(-1)e_t(U)` with the restricted optimum
  reset after each admission. The actual held `U_3` pair `6->7` is
  nonincreasing exactly when
  `c>=c_(6,7)=2978273417354/42112483166425`. After the literal stage-8
  transport, the actual held `U_4` pair `9->10` is nonincreasing exactly when
  `c<=c_(9,10)=95554102960761584/1567701294665491845`. Their exact gap is
  `129004507967154213801509972186/`
  `13203958876316640794781123060825>0`, so the feasible half-lines are
  disjoint: no real constant, and hence no `c>=0`, works on both pairs. The
  actual clipped envelopes, full moving correction, complete gate, and run
  totals remain `J=4,T=16,nu_fin=9,n_fin=5,mathfrak V_T=114`, with vector
  `(Theta(9),Theta(5),1,0,Theta(114),Theta(114),Theta(114),Theta(9),`
  `O(9),Theta(114),Theta(9))`. This is a finite exact-real, pairwise,
  face-local representation STOP in the literal order. It proves no global
  block horizon, asymptotic stage/work lower bound, or logarithm necessity,
  and it does not exclude time- or face-dependent coefficients, longer or
  signed-phase blocks, nonlocal aggregate potentials, or coordinatewise
  lower-point preservation when accelerated auxiliary state is restarted.
  The proof owner is `volume_gated_acceleration`,
  `prop:path-no-constant-coefficient-bank` and
  `eq:path-no-constant-bank-stop-eleven-vector`.

## Project-only Round-015 permutation, lower-gate, and bank boundaries

These are independently reviewed project results, not claims from the source
papers annotated in this file:

- `NotchedSunPermutationDelta` removes exactly the prescribed common event
  order from the Round-014 frozen-template reporter. It retains fixed `n>=5`,
  the verified face, rank-`n` cut, label pairing, complete shifted ladder,
  unit nonnegative or signed `2-minus-1` amplitudes, exact-real arithmetic,
  and `vartheta=(1-alpha)/2<=1/(1296n^2)`. A seen-label set verifies one
  common unused petal across every stream. Because the matching and
  off-matching Neumann estimates are pointwise and order-blind, every unseen
  label has the future-safe bound
  `9t vartheta^3/(1-3vartheta)<=g-m` after interaction `t`, and the complete
  vector remains
  `(Theta(n),2,n,Theta(n+J+p),Theta(C_frag+rn+n),0,0,`
  `Theta(n+J+p),O(1),0,Theta(rn))`, with `p=r,C_frag=rn` for nonnegative
  columns and `p=2r,C_frag=2rn` for separately checked signed streams. The
  reporter stores no response/slack cells and performs no response
  application, future-label scan, or numerical materialization. Repeats,
  missing petals, different per-column schedules, batches, arbitrary
  fragments/amplitudes, template mutation, RPPR chronology, fixed-`alpha`
  uniformity, terminal solving, and finite precision remain open. The proof
  owner is `response_preconditioned_hybrid`,
  `thm:notched-sun-permutation-delta-reporter` and
  `eq:notched-sun-permutation-eleven-vector`.
- On the fixed strict-range branch caterpillar, the principal-face Stieltjes
  retraction `L_U(z)=[z-Delta_U^low(z)D_U^(1/2)1]_+` satisfies
  `0<=L_U(z)<=x_k`. Strict positive boundary demands at `L_U(z)` are
  therefore response-free one-sided certificates. At `k=1`, the paid
  three-row scan has incremental vector
  `(nu_1,1,0,0,O(1),0,0,O(1),O(1),O(1),0)`, with `nu_1=6` for `m>2` and
  `nu_1=3` for `m=2`. The named `LowerGate-BC-AESP_(0:1)` policy certifies two
  gates and commits the first batch without exact settlement. With the
  direction note's fully charged `A_<2^low,H_<2^low,D_<2^low` budgets, its
  pre-second-interaction prefix vector is
  `(9+nu_1+O(A_<2^low),3+O(A_<2^low),1,0,O(H_<2^low),`
  `O(A_<2^low),0,O(C_2),O(C_1),O(D_<2^low),Theta(1))`.
  Response-freedom ends there: the direct suffix builds and pays the native
  response on `Uhat_2`, with vector
  `(vol(S*\Uhat_2),m-2,m,0,O(C(S*)),0,`
  `O(C(S*)+(m-1)log(2+m)),Theta(C(S*)),O(C(S*)),Theta(|S*|),`
  `|S*\Uhat_1|+|S*|+Theta(m))`. The exact total is
  `O(H_<2^low+C(S*)log(2+C(S*)))`. Charged validation forces the degree-six
  rows of `b_2,a_1,r_1` to be read before the first complete-batch reply, so
  the policy does not meet a row-unexposed endpoint. This is not an
  information-theoretic lower bound or a claim about free trusted metadata.
  The zero resets discard cross-face progress, the analysis-side bound keeps
  `mu_0,mu_1`, and every relative-oracle stage keeps
  `log(1/(1-2alpha))`; hence this is a comparator, not a speedup. The proof
  owner is `hybrid_aesp_locsor`,
  `lem:branch-caterpillar-local-lower-gate-certificate`,
  `prop:branch-caterpillar-first-layer-row-preexposure-obstruction`,
  `thm:branch-caterpillar-two-face-lower-handoff`, and its two eleven-vectors.
- On the literal exact `q=1/5` transported-center path chronology, the
  face-local coefficient-one bank
  `Phi_t^bank(U)=delta(x^(t))+q^(-1)||D_U^(-1/2)(x^(t)-x_U^*)||_infinity`
  survives the reviewed stages 6--7 correction spike but fails on the
  earliest later held pair. Stages 9 and 10 both hold `U_4`, yet
  `Phi_10^bank-Phi_9^bank=`
  `11777177533637842088/2957905129146728515625>0`, even though the correction
  itself decreases. The actual clipped envelopes, complete gate, run totals
  `J=4,T=16,nu_fin=9,n_fin=5,mathfrak V_T=114`, and complete vector
  `(Theta(9),Theta(5),1,0,Theta(114),Theta(114),Theta(114),Theta(9),`
  `O(9),Theta(114),Theta(9))` are retained. This finite STOP refutes only
  held-pair monotonicity of that coefficient-one bank in the literal stage
  order. Other coefficients, longer blocks, signed phase variables,
  aggregate space--time potentials, other phase origins/orders, logarithm
  removal, and matching/asymptotic lower bounds remain open. The proof owner
  is `volume_gated_acceleration`,
  `prop:path-correction-error-bank-potential-fails` and
  `eq:path-correction-error-bank-stop-eleven-vector`.

## Project-only Round-014 scale, margin, and correction-potential boundaries

These are independently reviewed project results, not claims from the source
papers annotated in this file:

- The frozen notched-double-sun trace admits a narrow output-sensitive
  comparator to the Round-013 eager-vector STOP. Fix `n>=5`,
  `eta in (0,1/8)`, the same face, rank-`n` cut, shifted ladder, unit event
  order and amplitudes, put
  `vartheta=(1-alpha)/2`, and require
  `0<vartheta<=1/(1296 n^2)`. The exact decomposition
  `M=B_0-vartheta R` has an entrywise-nonnegative Neumann kernel with operator
  norm at most three; no positive-semidefinite order is claimed. Its
  length-one term puts the matching response above
  `g=vartheta^(5/2)`, while the cumulative future-label tail is at most
  `9 k vartheta^3/(1-3 vartheta)<=g/2`. The promised-template reporter
  `NotchedSunScaleDelta` therefore stores only the validated template/label
  map, ladder, event counter, and stream metadata, and emits the matching
  delta plus one universal future-safe certificate per logical column without
  a response application, future-label scan, response cell, or slack cell.
  Its complete vector is
  `(Theta(n),2,n,Theta(n+J+p),Theta(C_frag+rn+n),0,0,`
  `Theta(n+J+p),O(1),0,Theta(rn))`, with `p=r,C_frag=rn` for nonnegative
  columns and `p=2r,C_frag=2rn` for separately checked signed `2-minus-1`
  streams. This is exact-real, fixed-template, fixed-order, and fixed-scale;
  it is not RPPR/KKT chronology, a terminal solver, a fixed-`alpha` uniform
  family, arbitrary fragment/order reporting, generic residual debt, or a
  finite-precision, word, or bit result. It proves constructively that the
  `EagerExactSlack` obstruction cannot be extended to this template-aware
  implicit representation; a genuinely dynamic partial flush remains open.
  The proof owner is `response_preconditioned_hybrid`,
  `thm:notched-sun-scale-delta-reporter` and
  `eq:notched-sun-scale-delta-eleven-vector`.
- At the actual strict-range branch-caterpillar checkpoint `Uhat_1`, one paid
  scan of the three live rows plus the retained four-coordinate exact response
  computes the sharp margin `mu_1` exactly. The incremental certificate vector
  is `(nu_1,1,0,0,O(1),0,O(1),O(1),O(1),O(1),0)`, where `nu_1=6` for `m>2`
  and `nu_1=3` for `m=2`. For fixed `m>=2`, branch seed `s=e_(b_1)`,
  `alpha<1/2`, and `rho<rho_can`, `MarginCert-BC-AESP_1` runs zero stages at
  zero gap or
  `T_1=1+floor((2/sqrt(alpha/(1-alpha)))`
  `log_+(4 Delta_(1,0)/(alpha mu_1^2)))` at positive gap on the fixed face.
  With `A_1=T_1*9*L_1^rel`, `C_1=13`, `C_2=16+nu_1`,
  `D_1=C_2+A_1`, and `H_1=C_2+(1+log(2+C_1))A_1`, its prefix vector is
  `(9+nu_1+O(A_1),3+O(A_1),1,0,O(H_1),O(A_1),O(1),O(C_2),O(C_1),`
  `O(D_1),Theta(1))`; the directly proved post vector is
  `(vol(S*\Uhat_2),m-2,m,0,O(C(S*)),0,O(C(S*)+(m-1)log(2+m)),`
  `Theta(C(S*)),O(C(S*)),Theta(|S*|),|S*\Uhat_1|+|S*|+Theta(m))`.
  Total work is `O(H_1+C(S*) log(2+C(S*)))`. The positive-gap endpoint is a
  genuine signed numerical gate state, but the exact constant-size response
  used to obtain `mu_1` could decide the gate itself. Thus this is a
  response-assisted comparison, not a speedup, automatic exploration, a
  `k>=2` certificate, a graph-uniform locality theorem, finite precision, or
  PPR conversion. Both the margin logarithm and the per-stage
  `log(1/(1-2 alpha))` factor remain explicit.
  The proof owner is `hybrid_aesp_locsor`,
  `lem:branch-caterpillar-first-layer-margin-certificate`,
  `thm:branch-caterpillar-first-layer-numerical-handoff`, and its prefix/post
  eleven-vectors.
- The actual `q=1/5`, `alpha=rho=tau=1/25` zero-start transported-center path
  run gives a finite STOP for two proposed pointwise correction potentials.
  Stages 6 and 7 hold the same face `U_3`, yet
  `delta_7-delta_6=1747556648/751181640625>0` and
  `delta_7/e_7=5361340160387/858557821215>5=1/q`, with the actual proximal
  and envelope states strictly unclipped. The complete run has `J=4`,
  `T=16`, `nu_fin=9`, `n_fin=5`, swept volume `114`, and vector
  `(Theta(9),Theta(5),1,0,Theta(114),Theta(114),Theta(114),Theta(9),`
  `O(9),Theta(114),Theta(9))`. This refutes only monotone held-face
  correction debt and the coefficient-one comparison `delta<=q^(-1)e`.
  It does not refute a larger or `q`-dependent coefficient, nonmonotone,
  phase-aware, space--time, or amortized potentials, the reviewed
  `q^(-2)` estimate, the one-log upper theorem, logarithm removal, or any
  matching/asymptotic lower bound. Unlike the quarantined Round-013 route,
  this calculation uses the actual projected execution and no conditional
  root assumption.
  The proof owner is `volume_gated_acceleration`,
  `prop:path-monotone-correction-potential-fails` and
  `eq:path-monotone-correction-stop-eleven-vector`.

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
