# AESP--local-refinement hybrid research note

This directory contains a standalone LaTeX research note that reconstructs the
project discussion on an AESP/Catalyst burn-in followed by momentum-free local
refinement. It is a curated mathematical synthesis rather than a verbatim chat
transcript: source theorems, new derivations, parameterized results,
conditional statements, empirical observations, corrections, and open claims
are labeled separately.

Build from this directory with:

```bash
make
python3 check_round014.py
python3 check_round015.py
python3 check_round016.py
python3 check_round017.py
python3 check_round018.py
python3 check_round019.py
python3 check_round020.py
python3 check_round021.py
python3 check_round022.py
```

The note embeds its bibliography so that it compiles without a BibTeX
executable. It deliberately does not modify the active manuscript or adopt a
repository-wide residual convention. Its PageRank normalization and stopping
certificates are scoped to the note.

The main established results are:

- finite convergence of AESP-to-LOCSOR after every finite signed handoff;
- objective-gap and weighted-gradient-mass LOCSOR tail bounds;
- a master handoff inequality for arbitrary Phase-I methods;
- a proved, realized-`R`-parameterized
  `O(R / (alpha^(3/4) * epsilon))` inner-plus-tail bound; queue construction,
  outer sparse-state initialization, and handoff work remain separate charges;
- a trajectory-dependent theorem and a confinement-based
  `O_tilde(1 / (sqrt(alpha) * epsilon))` corollary;
- weighted contraction and residual-to-solution certificates for the RPPR
  proximal map, proving convergence of a composite Catalyst-to-ISTA hybrid;
- on the center-seeded unweighted three-arm spider, for `0<alpha<1` and
  `0<rho<1/3` in exact real-cell arithmetic, a fully charged common-state
  conversion from any finite gate-compatible signed Phase-I prefix of cost
  `B_J^full` into the exact affine activation-token response, with incremental
  exact-cell work `O(C(S*(rho))) = O(1/rho)`, separate linear state, and exact
  proximal terminal output. This includes the note's composite Catalyst/AESP
  construction only in its stated range `alpha < 1/2`. The conversion uses
  the actual irreversible prefixes, accepts every legal certified bulk order,
  and does not replay a private numerical trajectory;
- on the unweighted double-Y seeded at branch vertex `o`, `s=e_o`, for
  `0<alpha<1` and `0<rho<1/3`, the same guarantee from any fully charged
  gate-compatible Phase-I prefix: one paid outward pass reconstructs the four
  actual pendant-prefix responses and a scalar core before `h` is admitted or
  an SPD rank-two core afterward, without replaying the Phase-I order. The
  conversion and exact response tail cost `O(C(S*))`, with separately charged
  adjacency, membership/conversion, affine construction, core build/update/
  query, gate/control, state writes, recovery, validation, terminal
  materialization, exact output, persistent cells, and scratch cells. The
  detailed subledger is also mapped in
  `eq:double-y-composite-eleven-vector` to the shared exhaustive order:
  preprocessing and post-handoff row recurrence are zero, conversion/gate/
  validation are control work, affine/core/settlement/recovery are response
  work, and terminal materialization is `O(|S*|)`. The final output has exactly
  `|S*|` cells, while the `J_post+1` external gate/certificate stages each emit
  a constant-size reply, so shared `C_emit=|S*|+Theta(J_post+1)=O(|S*|)`.
  Both adjacency-query and gate-interaction rounds are explicitly bounded.
  The prefix itself has the full vector
  `eq:double-y-composite-prefix-eleven-vector`; `B_J^full` is exactly the sum
  of its seven additive work coordinates under the fixed cell convention,
  while rounds and peak memory remain separate. Across the handoff, additive
  work and round coordinates sum, whereas persistent/scratch storage uses the
  stated retained-arena or released-arena peak rules.
  Every legal order enters the rank-two
  phase only in the stated sufficient range
  `rho < rho_link(alpha)=zeta/(3(3+zeta))`, where
  `zeta=(1-alpha)/(1+alpha)`;
  for larger `rho<1/3` the valid response may remain scalar. The particular
  composite Catalyst/AESP prefix still requires `alpha<1/2`;
- on the fixed-`m` branch caterpillar with `m>=2`, seeded at `s=e_(b_1)`, for
  `alpha in (0,1)` and the strict family-dependent range
  `0<rho<rho_can(m,alpha)<=rho_cat(m,alpha)<=1/3`, any fully charged Phase-I
  prefix ending immediately after an actual canonical all-violations
  checkpoint has one paid support-only conversion to the reviewed
  `CaterpillarCanonicalLayerDelta` state. The prefix retains only its actual
  canonical layer/support records; one direct traversal builds the current
  long-arm and leaf absorptions, tridiagonal branch cells, and balanced
  transfer tree without reconstructing, querying, or emitting any earlier
  face. If `k` canonical batches were already committed, the remaining
  `m-k` batches plus terminal return have the exhaustive vector
  `eq:branch-caterpillar-composite-eleven-vector`; its delta labels,
  certificate replies, adjacency and interaction rounds, control, response,
  persistent/scratch memory, terminal materialization, validation, and exact
  output are all charged. Post work is
  `O(C(S*) log(2+C(S*)))`, so the unconditional total is only
  `B_J^full+O(C(S*) log(2+C(S*)))`. The prefix itself reports
  `eq:branch-caterpillar-composite-prefix-eleven-vector`, and additive/round
  coordinates sum while retained/released memory uses the stated peak rules.
  The note's particular composite Catalyst/AESP prefix again separately
  requires `alpha<1/2`;
- in the same strict range with `alpha<1/2`, the named responder-native
  `FirstLayer-BC_1` policy now reaches an actual nonzero checkpoint without
  promised full-support row exposure. It scans exactly
  `Uhat_1={b_1,b_2,a_1,r_1}`, commits the imported first canonical batch
  `{b_2,a_1,r_1}`, exactly settles `Uhat_1`, and retains the constant-size
  native response. Its prefix vector is
  `(9,2,1,0,O(1),0,O(1),O(1),O(1),Theta(1),Theta(1))`; the complete native
  suffix vector is `eq:branch-caterpillar-first-layer-post-eleven-vector`.
  Admitted support, exact numerical support, and scanned rows are all exactly
  `Uhat_1`. The only lookahead is the next layer's labels, whose rows and
  coordinates remain unexposed and unadmitted. Resuming
  `CaterpillarCanonicalLayerDelta` in place gives exact total
  `O(C(S*) log(2+C(S*)))`, hence the product soft scale, with no hidden
  `log(1/(1-2 alpha))` singularity. This is a local response-native RPPR
  execution, not a useful accelerated burn-in;
- `prop:branch-caterpillar-signed-gate-margin` identifies the exact barrier to
  upgrading that response-native splice to a signed AESP splice. At canonical
  checkpoint `Uhat_k`, a boundary demand changes by
  `beta_(k,v)(z_parent-x_parent)`, so a symmetric signed-state certificate must
  have radius below `mu_k=min_v g_(k,v)/beta_(k,v)`. The imported Catalyst
  route has zero-stage success when `Delta_(k,0)=0`; for positive initial gap
  it supplies only the sufficient cap
  `T>(2/sqrt(alpha/(1-alpha)))*log_+(4 Delta_(k,0)/(alpha*mu_k^2))`, while every
  relative-oracle stage retains the explicit `log(1/(1-2 alpha))` factor.
  The old constant half-gap does not supply this comparison. This is a sharp
  norm-ball/gap-interface obstruction, not a lower bound against exact
  settlement or a new one-sided local certificate;
- the exceptional `k=1` margin is now closed exactly by
  `lem:branch-caterpillar-first-layer-margin-certificate`. One on-demand scan
  of the three live rows in `F_1` costs `nu_1=6` for `m>2` and `nu_1=3` for
  `m=2`; together with the retained four-coordinate response it computes the
  exact sharp scalar `underline(mu)_1=mu_1`. No future margin table is built or
  maintained. The named `MarginCert-BC-AESP_1` splice then runs the exact
  positive-gap cap
  `1+floor((2/sqrt(alpha/(1-alpha)))*log_+(4 Delta_(1,0)/(alpha mu_1^2)))`
  on the fixed numerical face `Uhat_1`; `Delta_(1,0)=0` instead runs zero
  stages. Every stage retains the explicit `log(1/(1-2 alpha))` oracle factor.
  Before the next interaction the admitted and numerical arenas are `Uhat_1`,
  the scanned-row arena is `Uhat_2`, and only the next layer's labels are
  further lookahead. Its full ledgers are
  `eq:branch-caterpillar-first-layer-numerical-prefix-eleven-vector` and
  `eq:branch-caterpillar-first-layer-numerical-post-eleven-vector`. The signed
  endpoint really supplies the carried gate state for positive gap, but the
  exact constant-size response used to certify `mu_1` is separately charged;
  this is a fixed-face numerical comparison witness, not an acceleration
  speedup, automatic exploration, or a certificate for any other `mu_k`;
- Round 015 removes that response from the gate certificate itself. For a
  signed trial point `z` on `Uhat_k`, initially `k in {0,1}`, the charged
  local lower retraction
  `L_U(z)=[z-Delta_U(z) D_U^(1/2)1]_+` is a nonnegative restricted
  subsolution, hence `L_U(z)<=x_k` coordinatewise. Therefore the demand at
  `L_U(z)` is a certified lower bound on every exact tree-boundary demand.
  At `k=1`, one scan of `F_1` and three strict lower-demand tests have vector
  `(nu_1,1,0,0,O(1),0,0,O(1),O(1),O(1),0)`: boundary exposure is unchanged
  from Round 014, but `C_resp` is exactly zero and no coordinate of `x_1`,
  optimum-value scalar, `mu_1`, or future margin table is computed. This is a
  strict response-coordinate improvement; constructing the lower point is
  separately charged numerical work. Round 016 strengthens the same lower-map
  lemma to every canonical `0<=k<m`;
- the named `LowerGate-BC-AESP_(0:1)` witness applies the same test on
  `Uhat_0`, commits the actual first batch without exact settlement, resets to
  a charged zero numerical start on `Uhat_1`, and certifies `F_1` before the
  second interaction. Its complete prefix vector is
  `eq:branch-caterpillar-two-face-lower-prefix-eleven-vector`, whose response
  coordinate is zero, and its direct native continuation has
  `eq:branch-caterpillar-two-face-lower-post-eleven-vector`. Zero restricted
  gap passes with zero stages; positive gap may also pass immediately, while
  the named zero starts fail the initial negative boundary-load test and run
  at least one genuine stage on each face. The online stopping rule reads
  only lower-demand signs; an analysis-side finite bound still contains
  `mu_0,mu_1`, and every relative-oracle stage retains
  `log(1/(1-2 alpha))`;
- the same exploration test does not meet a strict row-unexposed endpoint.
  Under the charged row-validation contract, certifying the complete first
  batch requires the rows/degrees/local incidences of `b_2,a_1,r_1` before
  the reply, so their degree-six scan forces `E_row=Uhat_1` while
  `U_adm=U_num=Uhat_0`. This scoped obstruction is
  `prop:branch-caterpillar-first-layer-row-preexposure-obstruction`; it is not
  a lower bound for an oracle that supplies trusted template metadata for
  free. The two-face witness is response-free only through its
  pre-second-interaction prefix and is pre-exposed; its post phase builds and
  charges the native response on `Uhat_2`. It uses numerical work only as a
  comparison and proves no speedup or monotone correction-debt potential;
- Round 016 proves that this lower point, unlike the AESP estimate sequence,
  can cross every fixed canonical admission without a whole-vector zero
  reset. Principal Stieltjes face monotonicity gives
  `x_(k+1)|_(Uhat_k)>=x_k`, so zero-padding any charged `y_k<=x_k` on the new
  three coordinates remains below `x_(k+1)`. On the next face the anchored
  retraction
  `T_(k,a)(z)=a vee L_(Uhat_k)(z)` remains below `x_k`, never decreases an old
  anchor coordinate, and supplies conservative tree-boundary demands. The
  named `TransportLower-BC-AESP_(0:q-1)` policy applies this invariant for
  every fixed `2<=q<=m`. It restarts all AESP momentum, proximal, center, and
  estimate-sequence records at each face, but initializes the fresh run from
  the transported nonzero lower anchor. It stops before interaction `q` with
  `U_adm=U_num=Uhat_(q-1)`, `E_row=Uhat_q`, and only
  `Uhat_(min(q+1,m))` labels known. Its response-free prefix and paid suffix
  have the complete vectors
  `eq:branch-caterpillar-transported-lower-prefix-eleven-vector` and
  `eq:branch-caterpillar-transported-lower-post-eleven-vector`; their
  interaction counts are `q-1` and `m-q+2`, respectively. Every candidate
  row is pre-exposed, every lower test pays a full old-face sweep, each
  analysis cap retains `mu_k` and `log(1/(1-2 alpha))`, and the post phase
  explicitly builds the native response on `Uhat_q`. This is all-layer
  lower-vector preservation and a direct exact continuation, not transported
  acceleration, a sublinear diagnostic, or a speedup;
- Round 017 removes the repeated *diagnostic* sweep from that policy. The
  exact `ImplicitLowerHeap` stores the raw lower residual and an indexed
  max-heap for its normalized negative part. A numerical write at coordinate
  `j` changes only `j` and its in-face neighbors, so the diagnostic reuses the
  paid numerical stencil, performs `O(d_j+1)` recurrence/state updates and
  `O((d_j+1) log(2+C(U)))` control work, and reads no additional adjacency
  cell. A complete gate test reads the heap maximum and the three cached
  boundary parents in `O(1)` work; it neither scans nor materializes the old
  lower vector. `lem:branch-caterpillar-implicit-lower-heap` proves exact
  equality with the Round-016 anchored map. The named
  `ImplicitLowerHeap-BC-AESP_(0:q-1)` policy has the full ledgers
  `eq:branch-caterpillar-implicit-lower-prefix-eleven-vector` and
  `eq:branch-caterpillar-implicit-lower-post-eleven-vector`. It conservatively
  charges one raw-product/heap initialization pass on every face,
  `sum_(k<q) vol(Uhat_k)=3q^2`, and one explicit transported-anchor
  materialization at every admission,
  `sum_(1<=k<q)|Uhat_k|=(q-1)(3q+2)/2`; all AESP auxiliaries are restarted.
  The scoped `LiteralDenseLowerSweep` comparison records
  `(N_k+1) vol(Uhat_k)` row work for its declared rebuild-on-every-test
  representation, not a class lower bound. Thus Round 017 is a strict exact
  query/update improvement, but the admission/restart shock remains quadratic
  for `q=m` and the theorem proves no speedup, energy transport, unexposed
  gate, or margin-uniform bound;
- Round 018 removes the raw-product and eager-anchor-copy parts of that
  transition shock. `FaceCarryLowerHeap` zero-pads the successful signed
  numerical endpoint, so every old raw residual and heap key remains exact;
  the three retained candidate rows produce exactly the three new residuals
  and keys. The lower anchor is represented by successful-heap-maximum tags,
  a dynamic range-minimum structure, and per-coordinate flush-before-write
  markers. This is an exact point-query representation of every old anchor
  coordinate without an admission-time old-face visit. The named
  `FaceCarryLowerHeap-BC-AESP_(0:q)` policy commits all `q` certified batches,
  carries the lower/heap state through all `q` expansions including the
  `q=m` full-support edge, and has full prefix/post vectors
  `eq:branch-caterpillar-incremental-face-prefix-eleven-vector` and
  `eq:branch-caterpillar-incremental-face-post-eleven-vector`. Its interaction
  counts are `q` and `m-q+1`, and the prefix response coordinate is exactly
  zero. The structural first-exposure adjacency rounds sum to `m+1`, while
  the full adjacency-round coordinate retains the charged numerical term and
  is only `m+1+O(A_fc)`; only the interaction total is exactly `m+1`.
  Candidate rows remain pre-exposed, every missing bulk endpoint
  product is charged, and all AESP momentum, proximal, center, and
  estimate-sequence records restart. Under the explicitly named
  `DenseFreshAESP` representation those fresh arrays write
  `sum_(k<q)|Uhat_k|=q(3q-1)/2` coordinate records. This scoped accounting
  identity is not a lower bound for another accelerated representation, but
  it stays quadratic at `q=m`; the result proves no speedup, scalar
  energy/potential monotonicity, or graph-uniform theorem;
- Round 019 tests the smallest favorable accelerated-state transition against
  the exact imported composite warm start, momentum state, Moreau envelope,
  and estimate potential. At any settled canonical face with zero momentum,
  the center, zero momentum, and estimate point zero-pad without rewriting an
  old coordinate. The proximal array does not: the three new entries are the
  strictly positive canonical demands divided by `L_A`. Thus
  `SettledAuxAppend` writes exactly twelve new coordinate records across the
  four explicit arrays, plus one reset marker, while making no old-coordinate
  write, old-face product, adjacency query, or response call. The old exact
  zero estimate certificate nevertheless acquires the strictly positive
  analytical shock
  `Sigma_k^es >= (mu_E/2) sum_(v in F_k) (x_(k+1))_v^2`. It is not a free
  online scalar: a continuation must restart the estimate proof or explicitly
  bound and charge that shock. The concrete response-assisted
  `FirstAuxShock-BC-AESP_(1->2)` audit has the full vectors
  `eq:branch-caterpillar-first-auxiliary-prefix-eleven-vector` and
  `eq:branch-caterpillar-first-auxiliary-post-eleven-vector`; its total
  interaction and structural first-exposure round counts are both exactly
  `m+1`. It settles `x_1` natively, pre-exposes the actual second batch, runs
  no accelerated stage after the append, and hands directly to the native
  suffix. Hence this is a sparse transition plus a mandatory shock/reset,
  not a response-free speedup, shock amortization, or lower bound for another
  representation or potential. Independent review rederived the imported
  state formulas, all transition charges and vectors, both horizon edges, and
  308 exact transitions through `m=12`; it returned clean without an edit;
- Round 020 closes the smallest nonsettled continuation audit, in the narrowed
  range `rho<min(rho_can(m,alpha),1/30)`. One exact shifted AESP stage from
  zero on `Uhat_0` ends strictly below the restricted optimum yet has the
  explicit positive first-batch margins in
  `eq:branch-caterpillar-first-nonsettled-margin`. Its carried primal,
  nonzero momentum, extrapolated center, and estimate point zero-pad across
  the actual `F_0` admission; the paid proximal warm start retains its old
  cell and appends three positive cells. `NonsettledShockRegister` charges two
  stored-row products, twelve appended array cells, and the observable KKT
  budget `B_ns`; `lem:branch-caterpillar-nonsettled-shock-reset` proves that
  this budget upper-bounds the strictly positive enlarged-face estimate
  certificate without querying an optimum. The policy then runs exactly one
  relative-accuracy AESP-CD stage from the carried extrapolated center and
  hands to the paid native `Uhat_1` suffix. Its full transition, prefix, and
  post vectors are `eq:branch-caterpillar-nonsettled-transition-vector`,
  `eq:branch-caterpillar-nonsettled-prefix-eleven-vector`, and
  `eq:branch-caterpillar-nonsettled-post-eleven-vector`. Only the live
  candidate rows are exposed, every product is charged, the exact `1/30`
  margin and `log(1/(1-2 alpha))` oracle factor remain visible, and structural
  first-exposure/interaction totals are both `m+1`. This is a finite GO for a
  real continuation but only a fresh proof reset: it does not amortize
  `B_ns`, transport an old estimate bound unchanged, or prove a speedup;
- Round 021 reaches the second actual nonsettled admission in the sharper
  range `rho<min(rho_can(m,alpha),rho_2(m,alpha))`, where
  `rho_2=(1+beta_A)/(138+3 beta_A)` for `m=2` and
  `(1+beta_A)/(354+3 beta_A)` for `m>2`. The extrapolated zero-padded center
  `y+` is a strict lower point but has negative demands toward `F_1`, so it
  does not certify that batch. Its standard proximal warm start does: the
  exact margins are
  `eq:branch-caterpillar-second-nonsettled-margins` and its `m=2` terminal
  variant. Locking the oracle to the imported greedy normalized-KKT AESP-CD
  rule gives `u_1(y+)<=z_1<=p_1(y+)<x_1`, so the actual relative-oracle output
  preserves those signs and is strictly nonsettled. After committing `F_1`,
  the positive momentum produces a second genuinely extrapolated center;
  another two-product, twelve-cell register computes the observable fresh
  budget `B_2`, and one relative-accuracy stage runs on `Uhat_2` before the
  paid native suffix. The complete vectors are
  `eq:branch-caterpillar-second-nonsettled-transition-vector`,
  `eq:branch-caterpillar-two-nonsettled-prefix-eleven-vector`, and
  `eq:branch-caterpillar-two-nonsettled-post-eleven-vector`. Total
  interactions and structural first-exposure rounds are exactly `m+1`, while
  the full adjacency-round count remains
  `m+1+O(A_2NS)`. This is a two-admission/two-continuation GO and an
  accelerated-rate STOP: no inequality relates `B_2` to `B_ns`, so it proves
  neither shock amortization nor a speedup;
- Round 022 isolates what can and cannot be obtained by paying the observable
  reset budgets additively with exact face-optimum drops. On the endpoint-
  seeded three-vertex path with `rho=3/10`,
  `alpha=s/(1+s)`, and `0<s<1/12`, one settled zero-momentum admission has
  exact normalized demands `g_0>0` and `g_1<0`, so the complete canonical
  trace has one expansion. Its observable KKT reset and Schur drop satisfy
  `B_1/Delta_1=3/(4q_r^2)+O(1)`, where
  `q_r=sqrt(alpha/(1-alpha))`. This refutes alpha-uniform and
  `O(1/q_r)` additive reset/drop coefficients for the declared budget, but
  not accelerated work: the relative stage oracle uses its initial budget
  only logarithmically. The actual analytical settled shock remains below
  `(1+mu_E/alpha)Delta_1<2Delta_1`; the obstruction is to the observable KKT
  upper budget, not to the face shock itself. In general, `Q<=I` gives the
  surviving sharp-order settled bound
  `sum B_j<=((3-5alpha)/(alpha(1-alpha)))sum Delta_j`, namely
  `Theta(1/alpha)`. A separate conditional nested-settlement/lower-center
  telescope has coefficient
  `Theta(q_r^-4)=Theta(alpha^-2)`, not `Theta(q_r^-3)`, but its ordering and
  residual premises are not proved for the actual Round-021 nonsettled
  trajectory. Finally, invoking the existing conservative no-sharing
  two-product register after all `m` canonical caterpillar admissions reads
  exactly `6m^2+12m-6` stored row cells. That last identity belongs only to
  the literal declared interface; product sharing or another representation
  may improve it, so it is not a class lower bound;
- in that strict caterpillar range and with `alpha<1/2`, the named
  `Full-BC-AESP_0` policy supplies one independent fully charged prefix bound.
  It pays a complete traversal of the promised fixed family, uses the imported
  support conclusion `U=V(BC_m)=S*` as a certified fixed envelope, runs exactly
  `T_*=ceil(2 log(4)/sqrt(alpha/(1-alpha)))` relative-accuracy composite AESP-CD
  stages, commits no canonical batch, and hands off at `Uhat_0={b_1}`. Its
  prefix vector is
  `(O(D_*),O(D_*),0,O(C_*),O(H_*),O(D_*),0,O(C_*),O(C_*),O(D_*),0)`,
  where `D_*=C_*+T_* vol(S*) L_*` uses the exact per-stage logarithmic oracle
  factor and `H_*=(1+log(2+C_*))D_*` charges heap/rekey control. Thus
  `B_env^full=O(H_*)=O_tilde(C(S*)/sqrt(alpha))`; composing the separately
  charged canonical response gives exact total
  `O(H_*+C_* log(2+C_*))`, hence the same product scale and exact output.
  This soft order hides `log(1/(1-2 alpha))` and is not uniform as
  `alpha -> 1/2`; the exact `O(H_*)` bound is the authoritative statement. The
  prefix discards its half-gap numerical progress and is a full-realized-support
  fixed-family witness, not adaptive support discovery or a graph-uniform
  result;
- the unqualified instruction in `alg:rppr-hybrid` to run any finite valid
  burn-in cannot itself imply any bound on `B_J^full`. For `alpha<1/2`, append
  any finite number `N` of exact-inner Catalyst stages to any reachable valid
  prefix before the first gate; every stage is valid and adds at least one
  outer-control operation, while the common state stays at `Uhat_0`. The stable
  obstruction and capped repair are
  `prop:branch-caterpillar-uncapped-prefix-obstruction` and
  `thm:branch-caterpillar-envelope-aesp-prefix`.

The graph-uniform early-AESP locality lemma and the graph-independent RPPR
local-work theorem from an arbitrary accelerated warm start remain open. The
three-arm and double-Y totals are only `B_J^full + O(C(S*))`, and the strict
canonical caterpillar total for an arbitrary checkpoint prefix is only
`B_J^full + O(C(S*) log(2+C(S*)))`; each generic statement reaches product
scale only when an independent theorem bounds the fully charged prefix. The
named first-layer policy supplies a locally exposed actual `k=1` checkpoint
and retains its exact response state, but it is response-native rather than
accelerated. The full-envelope zero-checkpoint policy remains a capped AESP
comparison at its exact interface; no analogous bound follows for an uncapped
or automatically exploring signed prefix. The Round-014 `k=1` witness closes
one constant-size on-demand margin and carries a signed numerical endpoint
into the next gate. Round 015 replaces its response-assisted sign test by a
strictly response-free lower-point certificate and reaches the admitted first
face before any exact response. Its full execution is response-free only
through the pre-second-interaction prefix; the post phase charges the native
response on `Uhat_2`. Round 016 extends the coordinatewise lower certificate
through every fixed canonical face and preserves the old lower coordinates
under padded admissions. Round 017 replaces its literal full lower-map sweep
at each test by an exact residual heap and three-parent query. Round 018
carries that residual/heap through each zero-padded expansion and replaces
eager anchor copies by exact lazy tags. Round 019 shows that dense
old-coordinate repopulation is not intrinsic at the specially settled,
zero-momentum checkpoint: all four imported auxiliary arrays admit a
constant-size coordinate transition. It also identifies the exact boundary
of that observation: the proximal append has three mandatory positive cells
and the inherited estimate certificate has a positive analytical face
shock, so its proof must reset or charge an explicit bound. The Round-018
growing-face execution itself still pre-exposes every candidate layer,
charges all missing bulk products, and retains both the margin and
upper-alpha oracle logarithms. Round 020 gives the first-face KKT reset, and
Round 021 reaches a second nonsettled admission only by using the greedy
safe-order property and a sharper `rho_2` margin. Its second reset is fresh:
there is no contraction from `B_ns` to `B_2`. Round 022 now rules out paying
the declared observable resets by an alpha-uniform or `O(1/q_r)` multiple of
the exact admission drops, while preserving a sharp-order `O(1/alpha)`
settled bound. Its only multi-reset telescope is conditional, costs
`Theta(alpha^-2)`, and does not apply to the actual nonsettled greedy trace.
Because the relative stage work sees a reset budget logarithmically, the
three-vertex obstruction is not an accelerated-work lower bound. Thus none of
these rounds proves a speedup. No unconditional multi-face
estimate-sequence energy bound is
retained beyond a face admission,
so no shock-free carryover or Euclidean-log collateral packing is claimed. The caterpillar
statement does not cover `rho_can<=rho<rho_cat`, another seed or policy,
repeated complete-positive-list output, a positive `m`-uniform `rho` range,
`kappa=1`, finite precision, bit complexity, transfer conditioning, arbitrary
graphs, or an RPPR-to-PPR conversion. The double-Y statement retains its
separate fixed-seed and fixed-rank-two scope.
