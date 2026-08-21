# Direction status: local_solver_oracle_hierarchy

Last reviewed: 2026-08-21

State: proved-open

## Exact question and contract

- **Question:** Which PPR lower bounds hold at information level, and can a
  budgeted row recurrence be separated from a fully charged persistent
  response on an identical query/output task? Round 007 tightens the endpoint
  path's actual sparse PPR residual certificate to `eps_ppr=1/(10n)` and tests
  the existing broad supported-prefix semantics before introducing any
  narrower lower-bound class.
- **Model:** Single-seed source-aligned PPR under adjacency-list revelation.
  Ambient `Adj` permits arbitrary computation on exposed entries.
  `RowRec[B_pre,B_resp,B_mem]`, persistent `Response`, and the independent
  `MatRestrict` representation property use the exhaustive execution ledger
  in `eq:resource-vector`. The Round-006/007 path class is the deterministic
  exact-cell `CertPrefixPoly` model in `def:cert-prefix-poly`: prefix masks,
  scalar/Jacobi maps, momentum, restart, and scalar reorthogonalization are
  allowed; non-scalar diagonal maps and graph-dependent preconditioners,
  factors, rational maps, and spectral atoms are excluded from its recurrence
  arm. Exact scalar cancellations may leave singleton coordinate directions;
  they are not interior masks.
- **Accuracy namespace:** The information result returns an explicit word-RAM
  sparse vector with note-scoped
  `||D^(-1/2)(x_hat-x^0)||_infinity <= eps_ppr`; no stopping-certificate or
  RPPR/APPR conversion is selected. The Round-006 auxiliary path task instead
  uses exact real-RAM/algebraic-cell arithmetic and explicitly requires the
  actual certificate
  `||D^(-1/2)(b-Q*x_hat)||_infinity <= alpha*eps_ppr` with
  `alpha=n^(-2)`. Round 006 uses `eps_ppr=1/10`; Round 007 uses the stricter
  `eps_ppr=1/(10n)`. Both remain note-scoped and exact-cell only.
- **Access and charged work:** Report adjacency exposure, algorithmic
  adjacency-query adaptivity, external interaction, preprocessing, online
  control, row recurrence, response construction/application/query
  computation, persistent memory, transient workspace, intermediate
  materialization, and emitted replies/final output separately. Precision,
  adversary, randomness, and failure probability are additional clauses.
- **Intended result:** With
  `nu_fin := vol(S_fin) = sum_{i in S_fin} d_i`, prove a same-instance
  `Omega_tilde(nu_fin/sqrt(alpha))` lower bound for a fully specified
  budgeted `RowRec` class and an `O_tilde(nu_fin)` fully charged response
  algorithm. Both arms must have the same adjacency interface, query/certificate
  task, and output obligation. The independent information target is
  `conj:influence-packing`. The concrete budget stress test is
  `B_n = (0,floor(sqrt(nu_n)),32*nu_n)` on an endpoint path with exact
  full-vector output.
  The Round-006 stress test replaces exact full-vector output by the actual
  sparse residual-certificate task on the same endpoint path and gives both
  `CertPrefixPoly` and append-only response arms that exact interface. Round
  007 tests whether forcing full-support accuracy repairs that same candidate,
  again with identical recurrence/response tasks and interfaces.

## Claim ledger

- **Source:** Shared PageRank definitions and algorithm-specific
  APPR/AESP/ASPR/SOR/SDD results are used only in their stated scopes. The comb
  rank obstruction is a proved dependency owned by
  `response_preconditioned_hybrid`, not reproved here.
- **Proved here:** The exhaustive eleven-coordinate ledger;
  `lem:free-preconditioner-collapse`, which only rules out making inverse
  construction, encoding, and application all free after complete exposure;
  and `thm:online-path-resource-separation`. At realized stopping time
  `tau_stop`, every exact-materialized path implementation has
  `C_mat = Omega(tau_stop^2)`, this coordinate is tight, and one specified
  append-only response has linear exact-cell work/space except constant
  transient workspace. `lem:finite-krylov-cap` proves exact CG termination
  in at most the active dimension, and
  `thm:path-krylov-counteralgorithm` applies it under `B_n`: at
  `alpha=n^(-4)`, CG uses `O(n^2)` charged work while
  `nu_n/sqrt(alpha)=Theta(n^3)`, and the exact path response uses
  `Theta(nu_n)`. The exhaustive same-task costs are
  `eq:path-cg-resource-vector` and `eq:path-ldl-resource-vector`. Earlier
  information-core, output, corridor-packing, path-completion, and Woodbury
  results remain proved. In the surviving choice `alpha=n^(-2)`,
  `thm:surviving-path-polynomial-obstruction` proves that, for every positive
  diagonal `M`, `h=M^(-1/2)b_n` is cyclic for the symmetric scaling
  `T=M^(-1/2)Q_nM^(-1/2)`. It gives exact degree lower bounds `n-1` without
  deflation and `n-r-1` after `r` named charged spectral atoms;
  under `B_n`, the named subclass's defining full-vector application rule
  converts this to `C_rec=Omega(n*nu_n)`. Degree alone does not give that work
  bound for a supported growing-prefix Krylov execution. Its matching
  eleven-coordinate execution is `eq:surviving-path-cg-resource-vector`.
  For the actual sparse certificate at `n>=8`, `alpha=n^(-2)`, and
  `eps_ppr=1/10`, `thm:five-site-supported-prefix-counteralgorithm` proves
  that the five-coordinate vector with normalized entries
  `alpha*(60,40,24,12,4)/11` is a degree-four polynomial in `Q` applied to
  `b`. Its six possibly nonzero scaled residuals are all positive and below
  `alpha/10`. A charged supported-prefix polynomial execution and a fully
  charged five-row append-only `LDL^T` response both use `O(1)` exact cells
  on the identical task. Their eleven-coordinate ledgers are
  `eq:certificate-prefix-poly-resource-vector` and
  `eq:certificate-path-response-resource-vector`; the realized final exposed
  set is `[6]`, so `nu_fin=11`. At the tighter `eps_ppr=1/(10n)`,
  `thm:tight-certificate-sparse-basis-counteralgorithm` proves that every
  valid output has all `n` coordinates and `nu_fin=2(n-1)`, yet exact sparse
  row actions and scalar cancellations generate the singleton coordinate
  basis and a fixed spatial profile is synthesized in `Theta(n)` work with
  `C_mat=0`. The identical-task append-only response is also `Theta(n)`, while
  `nu_fin/sqrt(alpha)=Theta(n^2)`. Their exhaustive ledgers are
  `eq:tight-sparse-basis-resource-vector` and
  `eq:tight-path-response-resource-vector`.
- **Conditional:** `RowRec[B_pre,B_resp,B_mem]` is a budgeted framework.
  A lower-bound theorem must still fix support masking, precision, allowed
  diagonal maps, row-action cost, adversary, and failure probability.
- **Measured:** None.
- **Refuted:** Adjacency access alone is not a first-order class. A free
  exposed-system inverse oracle defeats recurrence-iteration and
  condition-number lower bounds, but does not erase other costs. The path
  quadratic concerns exact intermediate materialization only, not every
  materialized-arm resource, word/bit complexity, adjacency adaptivity, or
  finite precision. The comb obstruction rules out low-rank banks but not
  implicit tree response. Disjoint corridors and path completions still fail
  as universal product information lower bounds. The concrete endpoint-path
  candidate also fails to establish a uniform-in-`(n,alpha)` product lower
  bound for the budgeted class when `n` is asymptotically below
  `1/sqrt(alpha)`; momentum, Jacobi scaling, or additional permitted response
  actions cannot rescue that path candidate from admissible unpreconditioned
  CG. In the surviving exact regime, positive diagonal PCG, Chebyshev, scalar
  momentum, and polynomial preconditioning within `DiagSpecPoly(0)` with every
  underlying `T` application counted do not yield a sub-product full-vector
  algorithm; endpoint cyclicity forces linear degree. For the different
  sparse-certificate task, supported-prefix polynomial generation by itself
  does not force product work: the five-site degree-four counteralgorithm is
  `O(1)`. Literal ordinary-CG noncertification before step `n` therefore
  cannot be promoted to this recurrence class. Tightening the tolerance until
  all coordinates are mandatory also does not repair the broad class:
  singleton coordinate-basis propagation plus delayed fixed-profile synthesis
  is an admissible `Theta(n)` counteralgorithm. A projected tridiagonal solve,
  factor, or graph-dependent inverse would be response work, but the proved
  counteralgorithm uses none.
- **Open:** The
  `Omega_tilde(nu_fin/sqrt(alpha))` recurrence versus
  `O_tilde(nu_fin)` response separation. For fully exposed fixed-support
  exact-system candidates with `O(nu_fin)` matrix--vector access and enough
  vector memory, the necessary regime is
  `n=Omega_tilde(1/sqrt(alpha))`; no such condition is claimed for every
  approximate local support-discovery task. The surviving-regime obstruction
  does not cover arbitrary nonlinear/adaptive response maps, rational factors,
  implicit path solves, or supported frontier recurrences. Precision-robust
  representation tradeoffs, optimal variable-`alpha` adjacency-query complexity,
  bounded-overlap killed-Green influence packing, and a valid unknown-completion
  upper envelope. Any next endpoint-style computational lower bound must
  defeat both constant-prefix slack spreading and sparse coordinate-basis
  propagation with delayed coefficient synthesis. It must either impose an
  explicit, independently justified trajectory/materialization condition or
  change the same-task family.

## Central blocker

For another fully exposed fixed-support exact-system candidate, first impose
the applicable dimension regime from `eq:krylov-required-dimension`. The
endpoint path is defeated for `alpha=n^(-4)` and is not a uniform candidate.
At `alpha=n^(-2)`, `thm:surviving-path-polynomial-obstruction` now closes only
the named polynomial/positive-diagonal/spectral-atom routes. The next
falsifiable sparse-output path test cannot use ordinary-CG's `n`-step trace:
`thm:five-site-supported-prefix-counteralgorithm` satisfies the actual
certificate with a degree-four polynomial and constant charged work. The
stronger full-support certificate is also defeated:
`thm:tight-certificate-sparse-basis-counteralgorithm` uses exact singleton
directions and delayed fixed-profile synthesis in linear work. A new test must
either justify an explicit Galerkin/trajectory/materialization restriction
that excludes exact sparse-basis cancellation, or use a different family,
while giving the response arm the identical task. A genuinely local
support-discovery lower bound may instead require a different information argument;
`conj:influence-packing` remains its separate blocker.

## Dependencies and reusable outputs

- Formal taxonomy dependencies: `incremental_active_set_sdd`,
  `delayed_reflection_ladder`,
  `response_preconditioned_hybrid`, `aspr23_bound_audit`, and
  `aesp_locgd_star_lower_bound`. The Round-006/007 counteralgorithms additionally
  import endpoint Krylov triangularity and the exact-CG calibration from
  `evolving_support_cg`, `thm:endpoint-path-exact-cg-certificate`, without
  duplicating its proof.
- Supplies to: all lower-bound directions and the controller: the exhaustive
  resource ledger; the narrow free-inverse-oracle collapse warning; the exact
  stopping-time path materialization analogue; the finite-dimensional exact
  Krylov cap and the condition `n=Omega_tilde(1/sqrt(alpha))` for the scoped
  fully exposed fixed-support exact-system route; endpoint cyclicity and the
  `n-r-1` degree obstruction for the named diagonal/spectral-polynomial
  subclass in the surviving regime; the tight
  PPR output scale; the five-site warning that an actual residual certificate
  can be easier than the literal CG Galerkin trace even within a supported
  polynomial space; the tighter warning that full-support accuracy still does
  not force full-prefix work when the class permits sparse coordinate bases
  and delayed fixed-profile synthesis; the classification of projected solves
  and factors as response rather than free recurrence; the failed-corridor
  warning; and the rule that a comb rank obstruction cannot be generalized to
  implicit response.

## Resume here

- Exact file/section/lemma: start at `sec:resource-vector`,
  `lem:free-preconditioner-collapse`, and
  `thm:online-path-resource-separation`; then read
  `sec:finite-krylov-cap`, `lem:finite-krylov-cap`, and
  `thm:path-krylov-counteralgorithm`, followed by
  `sec:surviving-path-polynomial` and
  `thm:surviving-path-polynomial-obstruction`, before continuing at
  `def:cert-prefix-poly` and
  `thm:five-site-supported-prefix-counteralgorithm`, followed by
  `thm:tight-certificate-sparse-basis-counteralgorithm`, then
  `prob:separation`.
  The independent information route starts at `conj:influence-packing`.
- Next concrete action: seek the smallest same-task family or explicitly
  justified Galerkin/materialization subclass that defeats both constant-prefix
  slack spreading and exact singleton-basis propagation. Do not treat response
  work as a rank bound; every response arm must still specify preprocessing,
  control, construction and applications, both memory coordinates,
  materialized cells, verification computation, and emitted output.
- Stop/go test: promote only if both arms answer an identical task,
  `nu_fin` is the declared final charged volume, and every coordinate of
  `eq:resource-vector` plus precision/adversary/failure clauses is explicit.

## Verification

- Source pointers checked: shared problem, related-work, results, and
  broadcast files; project conventions; local-solvers, graph-optimization,
  and acceleration literature notes; complete direction note and taxonomy;
  the companion comb proposition with its qualifier; and
  `evolving_support_cg`, `thm:endpoint-path-exact-cg-certificate`, including
  its exact certificate, ambient-degree path convention, Krylov triangularity,
  and implementation-specific exclusions.
- Focused build/checks run: an independent read-only audit verified the CG
  cap, budget, eleven-coordinate ledgers, Jacobi statement, and asymptotics,
  and required the fixed-support/exposed-system scope and `Theta(n)` emission
  corrections now used here. The surviving-regime proof separately checks
  irreducible-tridiagonal cyclicity, the `n-r-1` interpolation bound, named
  atom charging, and the conversion from full `Q_n` applications to
  recurrence work. A second independent audit confirmed those steps and all
  eleven coordinates, corrected “similarity” to symmetric scaling, and
  required the explicit `DiagSpecPoly(0)` scope for polynomial
  preconditioning. Direction `make`, repository `make note-audit`, and
  direction-scoped `git diff --check` ran on 2026-08-21. For Round 006, the
  six residual identities and the strict `n>=8` inequalities were separately
  checked in exact rational arithmetic; the focused note rebuilt without
  undefined references, `make note-audit` reported 18 notes across 5 tracks,
  and the scoped diff check was clean. For Round 007, the full-support bound,
  profile normalizer, centered-difference residual identity, exact endpoint
  residual, and the two rational constants `1657/21768` and
  `2291/464384` were checked independently in exact rational arithmetic for
  the stated `n>=8` range. Independent review confirmed the theorem and
  requested the now-explicit decomposition of `R_q` before the triangle
  inequality, including the separate `55/54` and `5/18` derivative charges.
  The direction rebuilt without undefined references;
  `make note-audit` again reported 18 notes across 5 tracks, and the scoped
  diff check was clean.
- Known gaps: neither a full-`RowRec` `nu_fin/sqrt(alpha)` computational lower
  bound (including in the surviving dimension regime) nor a precision-robust
  path separation is proved. The surviving-regime theorem covers only its
  named exact full-vector subclass. The sparse-certificate
  `CertPrefixPoly` path candidate is refuted at `eps_ppr=1/10` by a
  constant-work exact-cell algorithm and at `eps_ppr=1/(10n)` by a
  full-support linear-work exact-cell algorithm; no finite-precision
  robustness is claimed. The path analogue bounds only
  every materialized implementation's `C_mat`; it does not bound its other
  resources. `RowRec` remains a framework until a target fixes all remaining
  clauses. No controller-owned taxonomy dependency was changed.
