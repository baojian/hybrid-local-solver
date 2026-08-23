# Direction status: hybrid_aesp_locsor

Last reviewed: 2026-08-22
State: proved-open
Review: Round 022 independently audited clean after scope and mechanical checker repairs on 2026-08-22

## Exact question and contract

- **Question:** Can accelerated burn-in followed by a momentum-free local tail
  achieve product-scale PPR or RPPR work, and can a finite signed prefix hand
  off to a common persistent response without replay?
- **Model:** The general note treats single-seed unregularized PPR with AESP
  then omega-one LocSOR, and RPPR with composite Catalyst then proximal ISTA.
  The first structural theorem is exact-real single-seed RPPR on the
  center-seeded unweighted three-arm spider, with `alpha in (0,1)`,
  `rho in (0,1/3)`, and irreversible exact-gate admissions. The Round-007
  extension uses the unweighted double-Y with adjacent degree-three branch
  vertices, two pendant paths at each branch, and the branch seed `s=e_o`,
  again with `alpha in (0,1)` and `rho in (0,1/3)`. Its exact common core is
  scalar before `h` is admitted and SPD rank two afterward. Every legal order
  is forced into the rank-two phase only when
  `rho < rho_link(alpha)=zeta/(3(3+zeta))`,
  `zeta=(1-alpha)/(1+alpha)`; for larger `rho` the representation remains
  valid but can terminate scalar. The note's
  Round-011 extension uses the fixed-`m` branch caterpillar with `m>=2`,
  branch seed `s=e_(b_1)`, `alpha in (0,1)`, exact canonical all-violations
  checkpoints, and the strict family-dependent range
  `0<rho<rho_can(m,alpha)<=rho_cat(m,alpha)<=1/3`. Its support after `k`
  batches is the actual canonical layer union `Uhat_k`, and the reviewed
  balanced tridiagonal reporter owns the remaining `m-k` layers. This is a
  delta/certificate interface and has no positive `rho` range uniform in `m`.
  Round-012 adds the named `Full-BC-AESP_0` policy in the narrower composite
  range `alpha in (0,1/2)`: it fully exposes the promised caterpillar,
  certifies the fixed envelope `U=V=S*` using the strict-range support theorem,
  runs a prescribed `O(1/sqrt(alpha))` number of relative-accuracy AESP-CD
  stages, commits no canonical batch, and hands off at `Uhat_0={b_1}`. The
  Round-013 policy `FirstLayer-BC_1` instead scans only the seed and its actual
  first live boundary, commits the first canonical three-label batch, exactly
  settles and retains the native response at `Uhat_1`, and stops at the
  nonzero checkpoint `k=1`. Its numerical support, irreversible admission,
  and scanned-row set are all `Uhat_1`; only the next layer's labels are known
  lookahead, with no row or coordinate exposure. This policy performs no
  AESP stage and is therefore a response-native local comparator, not an
  accelerated prefix. Round-014 closes the exceptional sharp margin at this
  actual checkpoint: one on-demand scan of the three live rows in `F_1`, plus
  the separately charged four-coordinate exact response, computes
  `underline(mu)_1=mu_1`. The named `MarginCert-BC-AESP_1` policy uses this
  scalar to cap relative-accuracy AESP-CD on the fixed signed face `Uhat_1`
  and carries its numerical endpoint into the second canonical gate. Before
  that interaction, admission and numerical allocation are `Uhat_1`, scanned
  rows are `Uhat_2`, and only the following layer's labels are further
  lookahead. The exact response used for the margin is retired before the
  handoff and remains separately charged, so this is a genuine signed-state
  gate witness but only a comparison, not an acceleration speedup or automatic
  exploration. Round-015 separates that exact margin response from sign
  certification. Initially for `k in {0,1}`, the local lower retraction of any
  signed trial point on the canonical face is a nonnegative subsolution below the
  exact restricted point, so positive boundary demands at the lower point certify the exact
  canonical batch. At `k=1` the incremental certificate keeps the same
  `nu_1`/one-round boundary exposure but has `C_resp=0` and computes no
  coordinate of `x_1`, optimum value, `mu_1`, or future margin table. The
  named `LowerGate-BC-AESP_(0:1)` witness applies the same test from `Uhat_0`,
  commits the first batch without exact settlement, resets to zero on
  `Uhat_1`, and certifies the second batch before building a native response
  on `Uhat_2`. It is response-free through that prefix, but the charged
  row-validation contract forces candidate-row pre-exposure: before the first
  reply `E_row=Uhat_1` while `U_adm=U_num=Uhat_0`. Its online stopping times
  are finite and sign-driven, but their analysis bounds still contain
  `mu_0,mu_1` and the per-stage upper-alpha oracle logarithm. Round-016
  strengthens the lower-map lemma to every canonical `0<=k<m` and proves the
  all-layer transport invariant. If a charged lower point
  `y_k<=x_k` certifies `F_k`, principal Stieltjes face monotonicity makes its
  zero padding on the new coordinates lower than `x_(k+1)`. The anchored map
  `a vee L_U(z)` never decreases an old lower coordinate and still gives
  conservative boundary demands. For every fixed `2<=q<=m`,
  `TransportLower-BC-AESP_(0:q-1)` carries that lower vector through the
  first `q-1` admissions, certifies batch `q`, and remains response-free
  until that interaction. It restarts every accelerated auxiliary record,
  pre-exposes each candidate row set, and charges a full old-face sweep per
  test. Its suffix builds the native response on `Uhat_q`. Round-017 replaces
  those literal diagnostic sweeps by the exact `ImplicitLowerHeap`. The heap
  retains the raw lower residual; a coordinate write rekeys only its closed
  neighborhood, and a gate query reads one maximum plus the three cached
  boundary parents. `ImplicitLowerHeap-BC-AESP_(0:q-1)` evaluates the exact
  same anchored point without a query-time old-face scan. It still charges one
  raw-product initialization and one transported-anchor materialization per
  face admission and restarts every AESP auxiliary. For `q=m` that
  admission/restart shock is quadratic. Its suffix again pays the native
  response on `Uhat_q`. Round-018 removes the fresh raw-product and eager
  anchor-copy parts of that shock. The successful signed endpoint is
  zero-padded, leaving every old residual/heap key literally unchanged; the
  three retained candidate rows generate the three new keys. Successful lower
  endpoints are represented exactly by heap-maximum range-min tags and
  flush-before-write coordinate markers. The named
  `FaceCarryLowerHeap-BC-AESP_(0:q)` policy commits all `q` certified batches
  and carries the lower/heap state through all `q` expansions, including the
  full-support edge at `q=m`, before the native response build. Its prefix has
  exact `C_resp=0`. It still pre-exposes candidates, charges every missing
  bulk product, and restarts fresh dense AESP arrays on every numerical face.
  Their declared representation writes `q(3q-1)/2` coordinate records, which
  remains quadratic at `q=m`; this is a representation-specific accounting
  identity, not an accelerated-method lower bound. Round-019 now tests the
  exact imported auxiliary state at the smallest favorable settled checkpoint.
  Across every canonical admission, the center, zero momentum, and estimate
  point zero-pad algebraically; the proximal map instead appends exactly the
  three strictly positive canonical demands divided by `L_A`. With explicit
  records for those four arrays, `SettledAuxAppend` writes twelve new
  coordinate cells and one scalar reset record, with no old-coordinate write,
  old-face product/query, or response call. The old zero estimate certificate
  has a strictly positive analytical face shock, so an algorithm must restart
  that proof or explicitly bound and charge the shock. The concrete
  `FirstAuxShock-BC-AESP_(1->2)` audit is response-assisted, pre-exposes the
  second canonical batch, runs no accelerated stage after the transition, and
  therefore proves no speedup or class lower bound. Round-020 supplies the
  first charged nonsettled successor, under the narrower condition
  `rho<min(rho_can(m,alpha),1/30)`. One exact shifted AESP stage from zero on
  `Uhat_0` is strictly nonoptimal but already has three explicit positive
  first-batch margins. It commits exactly `F_0`, carries nonzero momentum and
  the extrapolated center, appends twelve auxiliary cells, and charges two
  full stored-row products. The exact KKT scalar
  `B_ns=K_ns^2/(2 alpha)+mu_E D_ns^2+mu_E K_ns^2/alpha^2` is observable and
  upper-bounds the strictly positive enlarged-face estimate certificate.
  Exactly one relative-accuracy AESP-CD stage then runs from the carried
  extrapolated center before the paid native `Uhat_1` suffix. This is a fresh
  estimate-proof reset, not an unchanged carry or shock amortization; no row
  beyond the live first batch is exposed, and the exact margin, both products,
  oracle logarithm, and suffix remain charged. Round-021 locks that first
  fixed-face oracle to the imported greedy normalized-KKT policy. The carried
  center `y+` is lower but does not itself certify `F_1`; its proximal warm
  start has the exact positive margins in
  `eq:branch-caterpillar-second-nonsettled-margins`, and greedy order preserves
  them through the actual strictly nonsettled output `z_1`. Under the sharper
  `rho_2` range, this commits `F_1`, registers a second observable KKT budget
  `B_2` with another two products/twelve appends, and runs a second genuinely
  extrapolated relative stage on `Uhat_2`. This is a second finite
  continuation, not a contraction from `B_ns` to `B_2` or a speedup. The three-arm
  and double-Y structural
  handoffs otherwise accept any fully charged gate-compatible Phase-I prefix;
  the caterpillar handoff accepts only the defined canonical checkpoints.
- **Accuracy namespace:** PPR uses the note-scoped degree-normalized gradient
  certificate for `eps_ppr`. RPPR uses the weighted fixed-point residual for
  `eps_sol`; all three structural responses return the exact minimizer and have
  zero proximal residual. No RPPR-to-PPR conversion is implicit.
- **Access and charged work:** Coordinate work costs `d_u`; batched work costs
  `vol(S)`. The fully charged prefix `B_J^full` includes initialization, excess
  exposure, repeated row reads, recurrence/outer/queue work, gate and
  certificate work, exact restricted settlement/Schur response, checkpoint
  materialization/recovery, and state reads/writes. Post-handoff accounting
  separates adjacency, conversion, response/query, control, canonical
  recovery, validation, state writes, terminal materialization,
  persistent/scratch cells, and output. The double-Y result additionally gives
  `eq:double-y-composite-eleven-vector` in the shared exhaustive order: it
  bounds adjacency and interaction rounds, has zero preprocessing and zero
  post-handoff row recurrence, and maps every other operation to control,
  response, memory, materialization, or emission. Its `J_post+1` external
  certificate stages emit constant-size replies in addition to the exact
  `|S*|` final-output cells. The prefix vector
  `eq:double-y-composite-prefix-eleven-vector` defines `B_J^full` as the sum of
  all seven additive work coordinates; prefix rounds and persistent/scratch
  peaks remain separate. Additive/round coordinates sum across phases, while
  memory follows the retained/released arena peak rules. The caterpillar
  prefix has the analogous exhaustive vector
  `eq:branch-caterpillar-composite-prefix-eleven-vector`, with exactly `k`
  declared completed-batch interactions and all previously emitted delta
  labels/certificate replies charged. Its direct support-only conversion and
  remaining suffix have
  `eq:branch-caterpillar-composite-eleven-vector`: post preprocessing and row
  recurrence are zero; conversion, membership, gate, tie, and validation work
  is control; absorption/tree construction, queries, settlement, and recovery
  are response; every remaining delta label, constant-size reply, terminal
  materialization cell, and exact output cell is charged. Prefix/post additive
  and round coordinates sum, and both peak-memory coordinates use explicit
  retained/released-arena rules. The named capped prefix has the full vector
  `eq:branch-caterpillar-envelope-aesp-prefix-eleven-vector`:
  `(O(D_*),O(D_*),0,O(C_*),O(H_*),O(D_*),0,O(C_*),O(C_*),O(D_*),0)`.
  Here `D_*` includes initial full exposure plus every warm-start and repeated
  coordinate-row scan over all prescribed stages, while `H_*` adds heap/rekey,
  queue, certificate, and outer control. It has no gate/response/reply work;
  all internal KKT tests, state accesses, full-vector materializations, and
  both memory peaks are charged.
  The responder-native first-layer prefix and suffix have the complete vectors
  `eq:branch-caterpillar-first-layer-prefix-eleven-vector` and
  `eq:branch-caterpillar-first-layer-post-eleven-vector`. The prefix vector is
  `(9,2,1,0,O(1),0,O(1),O(1),O(1),Theta(1),Theta(1))`: nine is exactly the
  degree work of rows `b_1,b_2,a_1,r_1`, and the two adjacency rounds separate
  seed-row discovery from the parallel live-boundary scan. The retained
  response grows in place through the suffix, so memory composes by a single
  peak and no conversion traversal or first-layer replay is charged. The
  Round-014 on-demand margin itself has incremental vector
  `eq:branch-caterpillar-first-layer-margin-certificate-vector`:
  `(nu_1,1,0,0,O(1),0,O(1),O(1),O(1),O(1),0)`, where `nu_1=6` for `m>2` and
  `nu_1=3` for `m=2`. The numerical splice has the complete prefix/post vectors
  `eq:branch-caterpillar-first-layer-numerical-prefix-eleven-vector` and
  `eq:branch-caterpillar-first-layer-numerical-post-eleven-vector`. Its prefix
  charges the original nine row units, the `nu_1` certificate scan, every
  repeated AESP row, recurrence, heap/certificate/state/materialization cell,
  the first interaction and its four emitted cells, and the separately paid
  constant response. Its post does not rescan `F_1`; it charges every later
  row, response update, interaction/reply, terminal materialization, exact
  output, and both memory peaks.
  The Round-015 lower-point certificate has incremental vector
  `eq:branch-caterpillar-local-lower-certificate-vector`:
  `(nu_1,1,0,0,O(1),0,0,O(1),O(1),O(1),0)`. Its response coordinate is
  exactly zero; the lower-retraction sweep that constructs its input is
  charged separately. The two-face witness has the complete vectors
  `eq:branch-caterpillar-two-face-lower-prefix-eleven-vector` and
  `eq:branch-caterpillar-two-face-lower-post-eleven-vector`. The prefix has
  one interaction/four emitted cells, first-exposes rows through `Uhat_2`,
  charges every repeated numerical/lower-map scan and reset, and has exact
  `C_resp=0`. The post consumes the already scanned `F_1`, builds the native
  response directly on `Uhat_2`, and charges every remaining row, response,
  interaction, reply, terminal materialization, exact output, and peak.
  The Round-016 transported policy has the complete vectors
  `eq:branch-caterpillar-transported-lower-prefix-eleven-vector` and
  `eq:branch-caterpillar-transported-lower-post-eleven-vector`. For horizon
  `q`, the response-free prefix has `R_int=q-1`, scans exactly through
  `Uhat_q` before repeated numerical sweeps, emits only the first `q-1`
  three-label batches and their replies, has exact `C_resp=0`, and charges
  every AESP restart, full-face lower sweep, anchor maximum, zero padding,
  row-validation round, state cell, and materialization. The post has
  `R_int=m-q+2`, reuses the rows through `Uhat_q`, explicitly builds and
  settles the native response there, and charges all remaining rows, labels,
  replies, response updates, terminal materialization, exact output, and
  memory peaks. The two interaction coordinates sum to exactly `m+1`.
  The Round-017 implicit policy has the complete vectors
  `eq:branch-caterpillar-implicit-lower-prefix-eleven-vector` and
  `eq:branch-caterpillar-implicit-lower-post-eleven-vector`. Its standalone
  heap initialization vector is
  `eq:branch-caterpillar-implicit-lower-init-vector`. With a paid numerical
  stencil, one coordinate write adds `O(d_j+1)` recurrence/materialization and
  `O((d_j+1) log(2+C(U)))` control, but no adjacency cell or round; a validated
  three-parent query is constant work and has no adjacency, interaction,
  response, materialization, or emission charge. The prefix conservatively
  pays `sum_(k<q) vol(Uhat_k)=3q^2` for one independent raw-product/heap
  initialization per face and
  `sum_(1<=k<q)|Uhat_k|=(q-1)(3q+2)/2` for transported-anchor writes and fresh
  AESP allocations. It keeps `R_int=q-1` and exact `C_resp=0`; its post keeps
  `R_int=m-q+2`, reuses rows through `Uhat_q`, and pays the native response and
  exact terminal output. `prop:branch-caterpillar-literal-dense-lower-sweep-cost`
  is only an accounting identity for its named rebuild-on-every-test
  representation, not a class lower bound.
  The Round-018 face-carried policy has the complete vectors
  `eq:branch-caterpillar-incremental-face-prefix-eleven-vector` and
  `eq:branch-caterpillar-incremental-face-post-eleven-vector`, plus the
  standalone transition vector
  `eq:branch-caterpillar-incremental-face-transition-vector`. It commits all
  `q` batches in the response-free prefix, so `R_int=q`, `C_resp=0`, and
  `C_emit=3q+Theta(q)`; the post has `R_int=m-q+1`, begins with the paid native
  response on `Uhat_q`, and charges all `S* setminus Uhat_q` rows/labels, response
  updates, replies, terminal materialization, exact output, and memory peaks.
  The interaction coordinates sum to exactly `m+1`. First-exposure adjacency
  rounds also sum to `m+1`, but the full adjacency-round coordinate is
  `m+1+O(A_fc)` because all charged numerical row touches and missing endpoint
  products remain present. Each transition uses its already
  exposed three candidate rows, inserts exactly three residual/heap keys, and
  appends one lazy-anchor tag without an old-face row round or anchor copy.
  Missing bulk endpoint products remain charged inside the numerical-stage
  budget. The separate dense fresh-auxiliary term is exactly
  `sum_(k<q)|Uhat_k|=q(3q-1)/2` up to its fixed number of arrays. The
  Round-019 settled transition has standalone vector
  `eq:branch-caterpillar-settled-auxiliary-transition-vector`:
  `(0,0,0,0,O(1),O(1),0,Theta(C_(k+1)^can),O(1),12+Theta(1),0)`.
  Its twelve materialized cells are exactly three appends in each explicit
  center, momentum, estimate-point, and proximal array; the proximal values
  use three already retained candidate-row demands. No old row/product/query
  is hidden, and any numerical evaluation of the analytical estimate shock
  must be added separately. The concrete first-to-second-face audit has full
  vectors `eq:branch-caterpillar-first-auxiliary-prefix-eleven-vector` and
  `eq:branch-caterpillar-first-auxiliary-post-eleven-vector`. Its prefix is
  `(9+nu_1,3,2,0,O(1),O(1),O(1),O(C_2),O(C_2),Theta(C_2),6+Theta(2))`;
  its response coordinate is only the already charged native settlement of
  `x_1`. The post is the paid native suffix from `Uhat_2`. Prefix/post
  interaction counts and structural first-exposure rounds each sum exactly to
  `m+1`, and the total exact-cell work is
  `O(C(S*) log(2+C(S*)))`.
  The Round-020 nonsettled register has standalone vector
  `eq:branch-caterpillar-nonsettled-transition-vector`:
  `(2 V_1,2,0,0,O(1),Theta(V_1),0,Theta(C_1),O(C_1),12+Theta(1),0)`.
  Its products separately form the enlarged-face KKT vector and extrapolated-
  center proximal start. The complete execution uses
  `eq:branch-caterpillar-nonsettled-prefix-eleven-vector` and
  `eq:branch-caterpillar-nonsettled-post-eleven-vector`; the prefix has exact
  `R_int=1`, `C_resp=0`, only `Uhat_1` rows, and the full one-stage oracle
  factor. Prefix/post interaction and structural first-exposure totals are
  `m+1`, while numerical rounds remain explicit in
  `R_adj=m+1+O(A_ns)`.
  The Round-021 second register has standalone vector
  `eq:branch-caterpillar-second-nonsettled-transition-vector`:
  `(2 V_2,2,0,0,O(1),Theta(V_2),0,Theta(C_2),O(C_2),12+Theta(1),0)`.
  The complete two-admission execution uses
  `eq:branch-caterpillar-two-nonsettled-prefix-eleven-vector` and
  `eq:branch-caterpillar-two-nonsettled-post-eleven-vector`; its prefix has
  exact `R_int=2`, `C_resp=0`, and only `Uhat_2` rows. Prefix/post
  interactions total exactly `m+1`; structural first-exposure rounds also
  total `m+1`, while the full adjacency-round coordinate is
  `m+1+O(A_2NS)`.
  Round 022 separates analytical reset size from the cost of the declared
  register. The settled `P_3` obstruction has no execution vector beyond its
  single already exposed face transition: it compares the observable scalar
  `B_1` with the exact Schur drop and does not claim a work lower bound. If the
  existing conservative no-sharing two-product register is instead invoked
  literally at all `m` canonical caterpillar admissions, its stored-row reads
  are exactly `2 sum_(j=1)^m V_j=6m^2+12m-6`. This identity assumes the two
  products remain separately charged; it is not unavoidable because a settled
  zero-momentum implementation may share them.
- **Intended result:** Graph-uniform
  `O_tilde(1/(sqrt(alpha)*eps_ppr))` PPR work and, separately,
  `O_tilde(1/(rho*sqrt(alpha)))` RPPR work.

## Claim ledger

- **Source:** The locally evolving-set, AESP, LocSOR, RPPR/Catalyst, and
  support-volume ingredients are source facts. The exact three-arm affine
  suffix is the reviewed project result
  `adaptive_revisit_control`, `thm:three-arm-spider-token-countdown`; the exact
  double-Y suffix is its reviewed
  `thm:double-y-two-core-token-countdown`. The exact strict-range canonical
  caterpillar chronology and balanced delta reporter are its reviewed
  `thm:branch-caterpillar-canonical-layer-reporter`.
- **Proved here:** The note proves finite SOR convergence from every finite
  signed handoff, omega-one tail and master/trajectory bounds, and weighted
  RPPR proximal contraction/certification. New
  `thm:three-arm-composite-response-handoff` retires the signed numerical
  state, retains the actual irreversible gate prefixes, builds the affine
  response in one charged common-state pass, accepts every legal certified
  bulk order, and returns exact output with incremental
  `O(C(S*))=O(1/rho)` exact-cell work, linear new state, and constant scratch.
  New `thm:double-y-composite-response-handoff` proves the analogous paid
  conversion on the branch-seeded double-Y from every finite fully charged
  gate-compatible prefix. One common outward pass reconstructs the actual
  pendant prefixes and scalar/SPD-rank-two Schur state without private order
  replay; conversion plus the exact reviewed tail costs `O(C(S*))`, with
  adjacency, membership/conversion, affine construction, core build/update/
  query, gate/control, state writes, recovery, validation, terminal
  materialization, exact output, and persistent/scratch cells separately
  charged. Its detailed subledger maps to the canonical eleven-coordinate
  vector in `eq:double-y-composite-eleven-vector`; in particular shared
  `C_rec=0`, while affine/core/settlement/recovery work is `C_resp`. Shared
  post-handoff emission is
  `|S*|+Theta(J_post+1)=O(|S*|)`: exactly `|S*|` final solution cells plus one
  constant-size certificate reply per declared external interaction stage.
  New `thm:branch-caterpillar-composite-response-handoff` proves that every
  fully charged prefix ending after `k` actual canonical caterpillar batches
  can retire its signed numerical/momentum arena and convert directly from
  the retained common layer/support records. One traversal builds the current
  arm and leaf absorptions, tridiagonal branch cells, and balanced product tree
  without replaying or querying any of the first `k` faces. The remaining
  reviewed canonical suffix costs
  `O(C(S*) log(2+C(S*)))`; the complete prefix and post eleven-vectors,
  adjacency/interaction rounds, delta/certificate emissions, recovery,
  validation, terminal materialization, exact output, and memory composition
  are explicit. New `thm:branch-caterpillar-first-layer-prefix` gives a
  locally reached actual `k=1` checkpoint with no promised full-support row
  exposure. It retains the exact native response rather than rebuilding from
  support, and its complete prefix/post vectors compose to
  `O(C(S*) log(2+C(S*)))` exact work. New
  `cor:branch-caterpillar-first-layer-product` records the resulting product
  soft scale; its stronger exact bound has no
  `log(1/(1-2 alpha))` nonuniformity. New
  `prop:branch-caterpillar-signed-gate-margin` proves the sharp symmetric
  signed-state radius
  `mu_k=min_v g_(k,v)/beta_(k,v)` for preserving a canonical batch. The
  imported relative-gap route has only a margin-dependent sufficient Catalyst
  stage cap,
  and each such stage retains its explicit `log(1/(1-2 alpha))` oracle factor;
  the constant half-gap result alone does not meet that gate certificate.
  New `lem:branch-caterpillar-first-layer-margin-certificate` solves the
  exceptional `k=1` certificate exactly. It derives the four restricted
  coordinates in closed form, scans the three current boundary rows once,
  and computes the exact minimum demand-to-coupling ratio with no eager future
  margin state. New `thm:branch-caterpillar-first-layer-numerical-handoff`
  composes that scalar with fixed-face relative-accuracy AESP-CD. For positive
  initial gap it runs exactly
  `1+floor((2/sqrt(alpha/(1-alpha)))*log_+(4 Delta_(1,0)/(alpha mu_1^2)))`
  stages; for zero gap, strong convexity gives the exact point and it runs zero
  stages. The signed endpoint and its strict objective-gap certificate supply
  the next gate, after which a separately charged native response settles the
  committed face and finishes exactly. Both the full margin logarithm and the
  per-stage `log(1/(1-2 alpha))` factor remain visible; the theorem makes no
  uniform product claim in either quantity and explicitly classifies the
  construction as a response-assisted numerical comparison rather than a
  speedup.
  New `lem:branch-caterpillar-local-lower-gate-certificate` proves the
  response-free alternative: principal-face lower retraction yields
  `0<=L_U(z)<=x_k`, so every positive demand at `L_U(z)` is a certified
  positive exact demand. At `k=1` this removes all response work from the
  incremental sign certificate while keeping the same boundary scan. The
  observed lower-sign stopping time is finite by convergence; zero initial
  gap passes at stage zero, positive gap can pass at stage zero or later, and
  the named zero starts run at least one stage. Its explicit analysis-side
  bound contains
  `log_+(4(alpha+sqrt(3))^2 Delta_(k,0)/(alpha^3 mu_k^2))` but no online
  margin computation. New `thm:branch-caterpillar-two-face-lower-handoff`
  composes the tests on `Uhat_0` and `Uhat_1`, commits the first batch without
  exact settlement, has exact prefix `C_resp=0`, then builds the native
  response directly on `Uhat_2` and finishes exactly. New
  `prop:branch-caterpillar-first-layer-row-preexposure-obstruction` proves
  that this does not meet a strict row-unexposed endpoint under the charged
  validation contract: the degree-six candidate rows must be read before the
  first certificate reply.
  New `lem:branch-caterpillar-anchored-lower-transport` extends the
  Stieltjes certificate to every canonical face, proves
  `x_(k+1)|_(Uhat_k)>=x_k`, and shows that zero padding preserves lowerness.
  Its anchored maximum `a vee L_U(z)` stays below the current exact point,
  preserves every old anchor coordinate, and yields conservative boundary
  demands. New `thm:branch-caterpillar-transported-lower-handoff` makes that
  invariant operational for every fixed `2<=q<=m`. It carries the lower
  vector through `q-1` actual admissions, supplies finite sign-driven stage
  caps on all faces through `k=q-1`, has exact prefix `C_resp=0`, then builds
  the native response directly on `Uhat_q` and finishes exactly. The theorem
  explicitly restarts AESP auxiliary state, charges full old-face sweeps and
  candidate-row exposure, and makes no energy or speedup claim.
  New `lem:branch-caterpillar-implicit-lower-heap` observes that the anchored
  lower vector is determined by the maximum normalized negative raw residual
  and the requested coordinate. It maintains that scalar in an indexed exact
  heap: a numerical coordinate write changes residuals only on its closed
  neighborhood, and the three boundary demands are constant-time parent
  queries. The result is exactly equal to the materialized anchored map and
  therefore preserves lowerness and every conservative gate sign. New
  `thm:branch-caterpillar-implicit-lower-handoff` composes the diagnostic on
  every face through an arbitrary fixed horizon `2<=q<=m`, with complete
  prefix/post vectors and exact prefix `C_resp=0`. It removes every
  query-time lower-vector sweep while explicitly charging one full raw-product
  initialization, transported-anchor materialization, and fresh AESP restart
  at each admission. The named `LiteralDenseLowerSweep` cost is stated only
  for that representation. The surviving quadratic shock, candidate
  pre-exposure, analysis margins, and oracle logarithms preclude a speedup
  claim.
  New `lem:branch-caterpillar-lazy-anchor` gives an exact old-coordinate
  representation using successful heap-maximum tags, a dynamic range-minimum
  structure, and flush-before-write markers. New
  `lem:branch-caterpillar-incremental-face-transition` proves that zero-padding
  the signed endpoint leaves all old residuals and keys unchanged and that the
  three new candidate rows determine the only new keys. New
  `thm:branch-caterpillar-incremental-face-handoff` composes these facts through
  every expansion `Uhat_k->Uhat_(k+1)`, including the terminal full-support
  edge, with exact prefix/post ledgers. The named `DenseFreshAESP` comparison
  keeps its `q(3q-1)/2` fresh coordinate records explicit. Thus the theorem
  removes raw-product and eager-anchor-copy transition shocks but leaves a
  representation-specific quadratic dense-auxiliary restart, all numerical
  stages/products, candidate exposure, margins, and oracle logarithms. Its
  coordinatewise lower order is not scalar energy/potential monotonicity.
  New `lem:branch-caterpillar-settled-proximal-append` anchors the favorable
  settled-state transition to the imported composite proximal map and proves
  that every old proximal cell is retained while the three new cells equal
  `g_(k,v)/L_A>0`. The center, zero-momentum, and estimate-point arrays
  zero-pad exactly, so the four-array representation writes twelve new cells
  and no old cell. New `prop:branch-caterpillar-zero-estimate-carry-fails`
  gives the exact enlarged-face objective shock and proves the inherited
  analytical estimate shock is at least
  `(mu_E/2) sum_(v in F_k)(x_(k+1))_v^2>0`. Thus zero-shock reuse of the
  imported exact certificate fails; a restart or explicitly bounded and
  charged shock is mandatory, without implying a lower bound for another
  potential. New `thm:branch-caterpillar-first-auxiliary-shock-handoff`
  realizes one fully charged transition from the actual settled `k=1`
  checkpoint, gives complete prefix/post eleven-vectors, and then uses the
  native suffix. It performs no post-transition accelerated stage and makes
  no speedup claim.
  New `lem:branch-caterpillar-first-nonsettled-admission` gives the exact
  first-face exception: one shifted stage from zero is strictly nonsettled
  yet certifies all of `F_0` whenever `rho<1/30`. New
  `lem:branch-caterpillar-nonsettled-shock-reset` bounds the positive
  enlarged-face estimate certificate by the observable KKT budget `B_ns`.
  New `thm:branch-caterpillar-first-nonsettled-continuation` charges the live
  candidate rows, two products, twelve appends, one extrapolated relative-
  oracle stage with its full logarithm, and the direct native `Uhat_1`
  suffix in three complete eleven-vectors. It proves only a fresh first-face
  reset and one valid continuation, not shock amortization or a rate.
  New `lem:branch-caterpillar-second-nonsettled-safe-center` proves that the
  extrapolated `y+` is a strict principal-face lower center but cannot itself
  certify `F_1`, while the standard warm start and every exact greedy
  normalized-KKT iterate obey `u_1(y+)<=z_1<=p_1(y+)<x_1`. New
  `lem:branch-caterpillar-second-nonsettled-admission` derives the exact
  `m>2` and terminal `m=2` warm-start margins and the sharp `rho_2` threshold,
  so the actual greedy endpoint commits the second canonical batch while
  remaining nonsettled. New
  `lem:branch-caterpillar-second-nonsettled-shock-reset` charges another two
  products and twelve auxiliary appends and bounds the positive second-face
  estimate certificate by the observable `B_2`. New
  `thm:branch-caterpillar-two-nonsettled-continuation` runs a second
  extrapolated relative stage on `Uhat_2` and gives complete prefix/post
  vectors. It proves two-admission/two-continuation feasibility only: no
  inequality connects `B_2` with `B_ns`, so no multi-face rate or speedup is
  claimed.
  New `prop:path-three-settled-reset-drop-obstruction` gives an exact complete
  one-admission trace on the endpoint-seeded three-vertex path at `rho=3/10`,
  `alpha=s/(1+s)`, and `0<s<1/12`. Its settled KKT reset and exact Schur drop
  obey `B_1/Delta_1=3/(4q_r^2)+O(1)`, with
  `q_r=sqrt(alpha/(1-alpha))`. Thus alpha-uniform and `O(1/q_r)` additive
  reset/drop coefficients fail even at zero momentum. The result concerns the
  observable KKT upper budget, not the actual analytical shock: the latter
  satisfies `Sigma^es<2Delta_1`. New
  `lem:settled-reset-optimum-drop-bound` uses `Q<=I` and the feasible
  negative-KKT step to prove the surviving
  `sum B_j<=((3-5alpha)/(alpha(1-alpha)))sum Delta_j` bound for settled
  zero-momentum safe expansions. Its `Theta(1/alpha)` order is sharp on the
  same path, and it makes no statement about nonsettled `D_j^2` terms. New
  `prop:conditional-nested-reset-budget-telescope` records a separate
  face-general algebraic telescope under exact settlement, lower-center,
  ordered-greedy, and live-residual identities. Its corrected coefficient is
  `Theta(q_r^-4)=Theta(alpha^-2)`, not `Theta(q_r^-3)`. Those premises are not
  established on the actual Round-021 nonsettled trajectory. Finally,
  `eq:branch-caterpillar-literal-reset-product-count` gives the exact
  `6m^2+12m-6` row reads only for the conservative declared no-sharing
  two-product register; it is not an implementation or algorithm-class lower
  bound.
  New `thm:branch-caterpillar-envelope-aesp-prefix` proves
  `B_env^full=O_tilde(C(S*)/sqrt(alpha))` for `Full-BC-AESP_0`, using exactly
  `T_*=ceil(2 log(4)/sqrt(alpha/(1-alpha)))` relative-accuracy stages and the
  exact certified-envelope per-stage factor. The precise result is `O(H_*)`;
  its soft-order shorthand hides `log(1/(1-2 alpha))` and is not uniform as
  `alpha -> 1/2`. It also proves a half-gap numerical checkpoint, then
  explicitly discards that progress. New
  `cor:branch-caterpillar-envelope-aesp-product` composes this `k=0` prefix
  with the separately charged response to obtain exact output and product
  work, with exact multivariate total
  `O(H_*+C_* log(2+C_*))`. New
  `prop:branch-caterpillar-uncapped-prefix-obstruction` proves that
  the generic phrase "any finite valid burn-in" supplies no prefix bound:
  for `alpha<1/2`, any reachable pre-gate prefix can be extended by arbitrarily
  many valid exact-inner Catalyst stages, each accumulating at least constant
  control work.
- **Conditional:** Graph-uniform PPR work still needs
  `Lambda_J=O(1/eps_ppr)` or a replacement. The realized-`R` bound excludes
  charges not included in its prefix ledger. The three-arm product conclusion
  in `cor:three-arm-composite-product-conditional` requires an independent
  fully charged bound `B_J^full=O_tilde(C(S*)/sqrt(alpha))`. The same premise
  is required by `cor:double-y-composite-product-conditional`; without it
  either theorem is only `B_J^full+O(C(S*))`. The caterpillar product statement
  for an arbitrary checkpoint prefix in
  `cor:branch-caterpillar-composite-product-conditional` likewise requires
  that independent prefix bound; without it the proved total is only
  `B_J^full+O(C(S*) log(2+C(S*)))`. The premise is discharged for the named
  full-envelope zero-checkpoint AESP policy. Independently,
  `FirstLayer-BC_1` constructs a local actual checkpoint and completes with a
  stronger response-native bound, but it supplies no accelerated-prefix
  theorem. `MarginCert-BC-AESP_1` supplies a capped signed gate only on the
  already reached constant-size face and retains the exact margin-dependent
  multivariate bound; it is not an automatically exploring prefix and does
  not remove either logarithm. `LowerGate-BC-AESP_(0:1)` removes the response
  from two gate-sign certificates and actually commits the first face, but it
  pre-exposes each candidate row set, resets cross-face progress, and its
  analysis retains both logarithms. `TransportLower-BC-AESP_(0:q-1)` removes
  the whole-vector zero resets and preserves a coordinatewise lower anchor
  through every fixed canonical layer. `ImplicitLowerHeap-BC-AESP_(0:q-1)`
  additionally removes the repeated query-time full-prefix sweeps, but still
  restarts all accelerated auxiliary state, pays a full growing-face
  initialization and anchor materialization at each admission, pre-exposes
  candidates, and retains both logarithms.
  `FaceCarryLowerHeap-BC-AESP_(0:q)` further eliminates each admission-time
  old-face product and anchor copy, but it still initializes the named dense
  fresh AESP arrays, charges every bulk product not supplied by a stage,
  pre-exposes candidates, and retains both logarithms. Its lower-anchor order
  is not a scalar energy reserve. `SettledAuxAppend` shows that this named
  dense old-coordinate restart is avoidable at an exactly settled,
  zero-momentum checkpoint, but the proximal append is nonzero and the exact
  estimate certificate incurs a positive analytical shock. The concrete
  audit pays native settlement before the transition and runs no later AESP
  stage, so it does not supply the missing continuation for the non-settled
  signed endpoints of `FaceCarryLowerHeap-BC-AESP_(0:q)`. The Round-020
  `FirstNonsettled-BC-AESP_(0->1)^(+1)` audit closes only the first admission:
  it uses the exact `rho<1/30` one-stage margin, registers the fresh KKT budget
  `B_ns`, and runs one extrapolated stage. It neither proves that `B_ns`
  contracts nor by itself extends the reset to a second nonsettled admission.
  Round 021 supplies that second finite reset, but not a comparison between
  the two budgets. Round 022's nested telescope is conditional on exact
  settlements, lower extrapolated centers, ordered greedy evolution, and the
  displayed live-residual identity; it therefore cannot be applied to the
  two nonsettled endpoints merely because their individual reset bounds are
  valid. Its `Theta(alpha^-2)` coefficient is also not the missing accelerated
  rate. None of these results bounds an uncapped
  or automatically exploring signed AESP prefix. Even for the full-envelope
  policy, the shorthand
  product bound is pointwise on `alpha<1/2`, not uniform at the upper endpoint;
  use the exact `O(H_*)` prefix bound near `alpha=1/2`.
- **Measured:** AESP Figure 4 supports early-stage practical effectiveness;
  it is not a universal locality theorem.
- **Refuted:** Uniform one-coordinate weighted-l1 contraction fails beyond
  `omega=1+alpha`. The new handoff does not retain numerical energy, use raw
  correction counts, or revive Euclidean-log collateral packing. Validity and
  finiteness alone do not bound a composite Catalyst prefix: the uncapped
  algorithm permits arbitrarily many valid exact-inner stages after any
  reachable pre-gate prefix in its `alpha<1/2` range. A signed
  relative-objective state with only a constant half-gap is not, by that fact
  alone, an exact canonical gate certificate: its parent-coordinate radius
  must also be below the sharp margin `mu_k`. Even at a settled canonical
  checkpoint, an all-zero proximal append is not the imported composite warm
  start, and zero-padding the exact old estimate certificate does not preserve
  its zero value on the enlarged face. For the declared observable KKT reset,
  neither an alpha-uniform multiple nor an `O(1/q_r)` multiple of exact
  face-optimum drops can pay all settled zero-momentum resets: the exact
  `P_3` ratio is `3/(4q_r^2)+O(1)`. This refutes only those additive
  reset-budget packings. It does not make the actual settled shock large, does
  not lower-bound stage work, and does not refute logarithmic or nonadditive
  budget use.
- **Open:** A graph-independent early-AESP prefix bound, local RPPR work from
  a retained arbitrary signed warm start, a charged amortization (or a
  nonadditive/logarithmic reset ledger) for the positive analytical face shock
  along the actual nonsettled greedy transitions, a lower bound and charged
  local certificate for the canonical margins `mu_k` with `k>=2`, another seed on the double-Y,
  caterpillar checkpoints for `rho_can<=rho<rho_cat`, other seeds or policies,
  arbitrary pre-backbone interleavings, and repeated complete-positive-list
  output remain open. Arbitrary trees, cycles, finite precision, bit
  complexity, transfer conditioning, and RPPR-to-PPR conversion are outside
  the structural handoff theorems.

## Central blocker

The strict canonical layer chronology now has a paid growing-branch-core
conversion, but only for the fixed-family range `rho<rho_can` and the
delta/certificate interface. `FirstLayer-BC_1` now closes construction of one
actual, locally exposed nonzero checkpoint and retains its exact native
response, but it performs no acceleration. The named full-envelope policy
closes one `k=0` AESP composition, but it discovers the whole realized support
before acceleration and discards all numerical progress. Round-014 now gives
one response-assisted fixed-face numerical gate at `k=1`: its margin is
computed once from seven local rows, its signed endpoint is actually carried,
and its exact prefix/post ledger is complete. This does not solve the live
hybrid blocker because the exact constant-size response already determines
the same boundary and the cap retains both margin and upper-alpha logarithms.
Round-015 removes that response from the sign test and commits the first batch
without exact settlement, but fully charged validation forces candidate-row
pre-exposure, the named resets discard cross-face progress, and the
analysis-side stopping bound still contains the same margins. Round-016
removes the whole-vector resets and extends the coordinatewise lower anchor
through every canonical face, but it restarts all AESP auxiliary state,
pre-exposes the live candidate rows, and pays a full growing-face sweep per
test. Round-017 closes the diagnostic part of that defect: the raw-residual
heap makes every test a constant-size exact query and reuses local numerical
stencils for updates. Round-018 closes the residual/heap and lower-anchor
parts of the face transition: old residuals/keys survive zero padding, only
three new keys are inserted, and lazy successful tags avoid every old-anchor
copy. Round-019 removes dense old-coordinate repopulation as an intrinsic
obstruction only at the specially settled, zero-momentum checkpoint: twelve
new array records suffice. Its first exact obstruction is instead semantic.
The proximal array needs three positive new entries, and the zero old
estimate certificate acquires a strictly positive analytical shock. The
concrete audit resets that proof and then uses the native response, so it
neither transports useful accelerated energy nor improves the Round-018
execution. Round-020 crosses the first face from one explicitly
nonsettled shifted endpoint, registers an optimum-free KKT upper bound, and
runs one extrapolated stage. It pays two products, uses only the live first
candidate batch, and replaces `mu_0` by the exact `rho<1/30` margin. It does
not contract the registered budget. Round-021 now reaches the second
nonsettled transition by exploiting the greedy safe-order theorem: `y+` is
lower but fails the gate, whereas its proximal warm start has a sharp positive
`rho_2` margin that every greedy iterate preserves. The second transition
again pays its live rows, two products, twelve appends, and fresh KKT budget,
then runs a genuine extrapolated stage on `Uhat_2`. No proved relation connects
`B_2` to `B_ns`, and the sharper range is not uniform in `m`.
Round 022 now rules out the simplest additive repair: even one settled
zero-momentum path admission has observable reset/drop ratio
`Theta(1/alpha)`, so neither an alpha-uniform nor an `O(1/q_r)` coefficient
can telescope these declared budgets. The surviving settled bound has sharp
order `1/alpha`, while the only face-general multi-reset telescope proved here
has a conditional `Theta(alpha^-2)` coefficient and assumptions absent from
the Round-021 nonsettled trace. This is not a work lower bound because the
relative inner-stage count sees its initial budget through a logarithm, and
the actual analytical settled shock is still `O(Delta)`.
The blocker is therefore a capped automatically exploring signed Phase I that
uses a nonadditive or logarithmic ledger for these observable reset budgets
over multiple actual transitions,
avoids candidate-row overexposure, and
controls the margin-dependent repeated-work term. The remaining
canonical range and wider
pre-backbone policies are separate blockers. No generic claim may use the
uncapped "any finite burn-in" specification.

## Dependencies and reusable outputs

- Formal taxonomy dependencies: `adaptive_revisit_control` and
  `aesp_cd_l1_rppr`.
- Source/shared prerequisites: source AESP/locally-evolving-set and LocSOR
  analyses and RPPR support facts.
- Imported proof anchors: `adaptive_revisit_control`,
  `thm:three-arm-spider-token-countdown` and
  `thm:double-y-two-core-token-countdown`, and
  `thm:branch-caterpillar-canonical-layer-reporter`; both named capped AESP
  prefixes also import `aesp_cd_l1_rppr`, `thm:aesp-cd-relative-oracle` and
  `cor:aesp-cd-certified-envelope`. The settled auxiliary transition imports
  its `eq:aesp-cd-subproblem`, `eq:aesp-cd-relative-parameters`,
  `eq:aesp-cd-smoothed-start`, `eq:aesp-cd-moreau-envelope`,
  `eq:aesp-cd-momentum-states`, and `eq:aesp-cd-potential-defect`
  definitions exactly. Round-020 additionally imports the minimum-norm KKT
  vector and local relative-oracle work guarantee. Round-021 also imports the
  principal-face safe-center order and requires its exact greedy
  normalized-KKT update policy; relative accuracy alone is insufficient for
  its second gate. The expansion-shock and
  safeguarded collateral results delimit excluded numerical-energy routes but
  are not used as amortizations here.
- Supplies to: The synthesis and response-composition directions through a
  proved one-pass common-state conversion for scalar and fixed rank-two cores,
  and now for the strict canonical growing tridiagonal core; exact resource
  ledgers; one locally exposed native `k=1` product-scale execution; one fully
  exposed fixed-family AESP comparison witness; one exact on-demand `mu_1`
  certificate and response-assisted numerical gate with complete ledgers; one
  response-free lower-point sign certificate, a two-face numerical handoff
  whose pre-second-interaction prefix is response-free, complete prefix/post
  ledgers that charge the later native response, and the scoped charged-row
  pre-exposure obstruction; an all-layer Stieltjes face-monotonicity and
  padded-lower-anchor invariant, plus a `q`-face response-free prefix/direct
  paid-response continuation with full ledgers; an exact residual-heap
  representation whose local write updates and three-parent queries avoid
  every repeated diagnostic sweep, together with a second `q`-face
  prefix/post ledger that keeps the admission and AESP-restart shock explicit;
  an exact three-key/lazy-anchor face transition through the full-support edge,
  a third complete prefix/post ledger, and a scoped dense-fresh-auxiliary
  quadratic accounting identity; a settled-state four-array sparse append,
  first- and second-face nonsettled twelve-cell appends, four charged products,
  two observable KKT estimate-reset budgets, two extrapolated continuation
  stages, sharp second-batch margins, and complete transition/prefix/post
  vectors; an exact settled `P_3` reset/drop obstruction, the sharp-order
  general settled `O(1/alpha)` budget bound, a conditional
  `Theta(alpha^-2)` nested reset telescope, and the literal no-sharing
  caterpillar two-product identity `6m^2+12m-6` with its representation-only
  scope;
  the exact three-cell proximal correction, a positive analytical estimate
  shock requiring reset or explicit charge, and a fully charged one-admission
  audit with complete vectors;
  the
  general sharp signed gate margin and its margin-dependent stage-cap
  interface; the uncapped-prefix
  specification obstruction; and the distinction among irreversible
  admissions, scanned rows, label-only lookahead, and signed trial support.

## Resume here

- Exact file/section/lemma: `sec:three-arm-composite-handoff`, especially
  `def:three-arm-gate-compatible-prefix`,
  `thm:three-arm-composite-response-handoff`, and
  `cor:three-arm-composite-product-conditional`; and
  `sec:double-y-composite-handoff`, especially
  `def:double-y-gate-compatible-prefix`,
  `thm:double-y-composite-response-handoff`, and
  `cor:double-y-composite-product-conditional`; and
  `sec:branch-caterpillar-composite-handoff`, especially
  `def:branch-caterpillar-canonical-checkpoint-prefix`,
  `thm:branch-caterpillar-composite-response-handoff`, and
  `cor:branch-caterpillar-composite-product-conditional`; then
  `sec:branch-caterpillar-first-layer-prefix`, especially
  `def:branch-caterpillar-first-layer-policy`,
  `thm:branch-caterpillar-first-layer-prefix`,
  `eq:branch-caterpillar-first-layer-prefix-eleven-vector`,
  `eq:branch-caterpillar-first-layer-post-eleven-vector`, and
  `cor:branch-caterpillar-first-layer-product`; then
  `sec:branch-caterpillar-envelope-aesp-prefix`, especially
  `prop:branch-caterpillar-uncapped-prefix-obstruction`,
  `def:branch-caterpillar-envelope-aesp-zero-policy`,
  `thm:branch-caterpillar-envelope-aesp-prefix`, and
  `cor:branch-caterpillar-envelope-aesp-product`; then
  `sec:branch-caterpillar-signed-gate-margin` and
  `prop:branch-caterpillar-signed-gate-margin`; finally
  `sec:branch-caterpillar-first-layer-numerical-splice`, especially
  `lem:branch-caterpillar-first-layer-margin-certificate`,
  `def:branch-caterpillar-first-layer-numerical-policy`,
  `thm:branch-caterpillar-first-layer-numerical-handoff`, and its two full
  eleven-vectors; then
  `sec:branch-caterpillar-first-layer-one-sided-splice`, especially
  `lem:branch-caterpillar-local-lower-gate-certificate`,
  `prop:branch-caterpillar-first-layer-row-preexposure-obstruction`,
  `thm:branch-caterpillar-two-face-lower-handoff`, and its prefix/post
  eleven-vectors; then
  `sec:branch-caterpillar-transported-lower-splice`, especially
  `lem:branch-caterpillar-anchored-lower-transport`,
  `def:branch-caterpillar-transported-lower-policy`,
  `thm:branch-caterpillar-transported-lower-handoff`, and its prefix/post
  eleven-vectors; then
  `sec:branch-caterpillar-implicit-lower-heap`, especially
  `lem:branch-caterpillar-implicit-lower-heap`,
  `prop:branch-caterpillar-literal-dense-lower-sweep-cost`,
  `def:branch-caterpillar-implicit-lower-policy`,
  `thm:branch-caterpillar-implicit-lower-handoff`, and its prefix/post
  eleven-vectors; then
  `sec:branch-caterpillar-incremental-face-transition`, especially
  `lem:branch-caterpillar-lazy-anchor`,
  `lem:branch-caterpillar-incremental-face-transition`,
  `prop:branch-caterpillar-fresh-auxiliary-shock`,
  `def:branch-caterpillar-incremental-face-policy`,
  `thm:branch-caterpillar-incremental-face-handoff`, and its transition,
  prefix, and post eleven-vectors; then
  `sec:branch-caterpillar-auxiliary-face-shock`, especially
  `eq:branch-caterpillar-settled-auxiliary-state-append`,
  `lem:branch-caterpillar-settled-proximal-append`,
  `prop:branch-caterpillar-zero-estimate-carry-fails`,
  `eq:branch-caterpillar-settled-auxiliary-transition-vector`,
  `thm:branch-caterpillar-first-auxiliary-shock-handoff`, and its prefix/post
  eleven-vectors; then
  `sec:branch-caterpillar-nonsettled-continuation`, especially
  `lem:branch-caterpillar-first-nonsettled-admission`,
  `lem:branch-caterpillar-nonsettled-shock-reset`,
  `eq:branch-caterpillar-nonsettled-transition-vector`,
  `thm:branch-caterpillar-first-nonsettled-continuation`, and its prefix/post
  eleven-vectors; then
  `sec:branch-caterpillar-second-nonsettled-continuation`, especially
  `lem:branch-caterpillar-second-nonsettled-safe-center`,
  `lem:branch-caterpillar-second-nonsettled-admission`,
  `lem:branch-caterpillar-second-nonsettled-shock-reset`,
  `eq:branch-caterpillar-second-nonsettled-transition-vector`, and
  `thm:branch-caterpillar-two-nonsettled-continuation` with its prefix/post
  vectors; then `sec:settled-reset-budget-amortization`, especially
  `prop:path-three-settled-reset-drop-obstruction`,
  `eq:path-three-reset-drop-ratio`,
  `lem:settled-reset-optimum-drop-bound`,
  `prop:conditional-nested-reset-budget-telescope`, and
  `eq:branch-caterpillar-literal-reset-product-count`. Graph-uniform gates remain
  `conj:early-locality`, `sec:open-gap`, and `sec:composite-hybrid`.
- Next concrete action: Round-022 refutes alpha-uniform and `O(1/q_r)`
  additive reset/drop packing but does not refute accelerated work, because
  the inner oracle uses the reset budget logarithmically. Prove a nonadditive
  or logarithmic two-reset ledger along the exact Round-021 greedy trajectory,
  or exhibit its first exact failure. Do not apply the conditional settled
  telescope until its lower-center/order/residual premises are verified on
  those nonsettled states. A useful extension must avoid
  candidate-row exposure beyond the live certificate batch and must not
  maintain every future margin eagerly. Separately extend or refute
  the response beyond `rho<rho_can`.
- Stop/go test: Stop any efficiency proof that privately replays a canonical
  order, hides rescans of old prefixes per admission, identifies numerical
  support with safe admission, or transports estimate-sequence energy without
  an explicit shock. In particular, an all-zero proximal append is false at a
  settled canonical face, and an analytical value of `Sigma_k^es` is not an
  online scalar unless every solve/query/write used to obtain its bound is
  charged. Fully charged repeated sweeps remain valid comparison
  work but cannot establish the target. Also stop any inference that the
  `P_3` KKT-budget ratio is a shock-size or stage-work lower bound: the actual
  settled shock is below `2Delta`, and the relative stage bound depends on
  `B` logarithmically. The `6m^2+12m-6` product count belongs only to the
  explicitly no-sharing register. A direct one-pass build from the
  actual checkpoint support is allowed;
  reconstructing its historical gate states is not. Also stop any prefix proof
  that leaves its stage count uncapped, calls full-family exposure local
  discovery, infers prefix work from the post-response ledger, or treats a
  constant relative objective gap as an exact gate sign without paying the
  margin or a one-sided certificate.

## Verification

- Source pointers checked: Root and note-level agent rules, shared problem,
  related-work/results/broadcast ledgers, Round-011 through Round-018 assignments,
  direction
  README/status/taxonomy/main and relevant sections, acceleration literature
  notes, and the exact canonical gate, three-arm, branch-seeded double-Y, and
  strict-range canonical caterpillar theorems in
  `adaptive_revisit_control`; the relative-accuracy oracle and certified-
  envelope results in `aesp_cd_l1_rppr` were also checked at their stable
  labels.
- Focused build/checks run: The prior independent read-only audit checked the
  three-arm theorem. The Round-007 independent double-Y audit required
  reconciliation of its
  bespoke operation subledger with the shared exhaustive eleven-coordinate
  vector. The linked re-audit additionally required the full prefix vector and
  certificate-reply emissions. The two stable vectors now record prefix and
  post rounds, all additive work, both memory coordinates, terminal
  materialization, constant-size certificate replies, and exact final output,
  together with their sum/peak composition rules. After that reconciliation,
  the direction build, `make note-audit` (18 notes across 5 tracks), and the
  scoped diff check reran and passed on 2026-08-21. For Round-011, the focused
  direction build, `make note-audit` (18/5), `make note-graph` (18 nodes and
  25 acyclic edges), stable-label/undefined-reference scans, conflict-marker
  scan, and scoped tracked/untracked whitespace checks passed. A separate
  adversarial pass confirmed the `k` prefix interactions and `3k` prior delta
  emissions, and caught two endpoint/summary defects that were repaired: at
  `k=m` there is no next layer and the direct build has `m`, not `m+1`, branch
  cells; README/STATUS now state `m>=2` and `alpha in (0,1)` explicitly.
  Round-012 added the uncapped-prefix obstruction and the capped full-envelope
  theorem. The final focused note build, `make note-audit` (18/5),
  `make note-graph` (18 nodes and the pre-controller 25 acyclic edges),
  duplicate-label/undefined-reference scans, conflict-marker scan, and scoped
  whitespace check passed on 2026-08-21. The new import requires the controller
  to add the formal dependency `aesp_cd_l1_rppr -> hybrid_aesp_locsor`.
  The independent Round-012 audit required three narrow repairs, all now
  reconciled: the uncapped obstruction uses the actual `alpha<1/2` algorithm
  range, starts from an arbitrary reachable prefix and appends exact-inner
  stages rather than assuming a fixed point, and every product summary states
  the nonuniform `log(1/(1-2 alpha))` margin. After reconciliation, the
  focused build, note inventory, pre-controller dependency graph, reference/
  font-warning scan, conflict-marker scan, and scoped diff check reran and
  passed. Round-013 added `FirstLayer-BC_1` and the signed gate-margin
  proposition. The local audit rederived the first-row work
  `3+3+2+1=9`, the two adaptive adjacency rounds, the one gate interaction,
  the `Uhat_1` native response state, the label-only `F_1` lookahead, all
  prefix/post coordinates, total rounds `m+1`, and total adjacency work
  `vol(S*)=6m`. It also checked
  `g_v(z)=g_v(x_k)+beta_(k,v)(z_parent-x_parent)`, the sharp equality witness,
  the strong-convexity gap conversion, the sufficient Catalyst stage cap, and
  the separate `alpha<1/2` scope of the AESP formulas. The focused build,
  `make note-audit` (18/5), `make note-graph` (26 acyclic edges), duplicate-
  label/undefined-reference scans, control/conflict-marker scan, trailing-
  whitespace scan, and scoped diff check passed on 2026-08-21. A transient
  carriage-return defect in two arena subscripts was caught and repaired to
  `\mathrm{adm}` and `\mathrm{num}` before the clean control-character scan.
  Independent Round-013 review required one narrow stage-cap repair:
  `Delta_(k,0)=0` is now handled as immediate zero-stage success, while
  `log_+(4 Delta_(k,0)/(alpha mu_k^2))` is invoked only under the explicit
  assumption `Delta_(k,0)>0`. The README records the same exact formula.
  Round-014 added the exact on-demand `mu_1` certificate and the capped
  `MarginCert-BC-AESP_1` numerical splice. The focused checker independently
  solves the four-by-four restricted system, compares all terminal and
  nonterminal boundary ratios with the displayed formulas, verifies the
  zero-start gap identity, and checks the strict integer stage cap. The
  final direction build produced 52 pages with no undefined reference or new
  overfull-box warning. `check_round014.py` passed its focused checks and Ruff
  lint/format validation. `make note-audit` reported 18 notes across 5 tracks;
  `make note-graph` reported the same 26-edge acyclic graph. Duplicate-label,
  undefined-reference, conflict-marker, control-character, trailing-whitespace,
  and scoped tracked/untracked diff checks all passed on 2026-08-21.
  Round-015 added the local lower-map comparison, response-free first-layer
  certificate, charged row-preexposure obstruction, and two-face numerical
  handoff. `check_round015.py` independently solves the four-row restricted
  system, tests signed lower retractions against the exact point, checks all
  terminal/nonterminal one-sided boundary inequalities, verifies the strict
  analysis-side integer cap, row totals, and stable labels. The focused build
  produced 57 pages with no undefined reference or new overfull-box warning;
  the checker and Ruff lint/format checks passed. Repository note inventory,
  graph, conflict/control/whitespace, and scoped diff checks are rerun by the
  controller after independent review. The independent Round-015 audit
  required one scope repair: every theorem title and summary now states that
  only the pre-second-interaction/two-gate prefix is response-free; the post
  vector retains its nonzero `C_resp` and explicitly charges the native
  response build on `Uhat_2`. Round-016 strengthened the lower map to every
  canonical face, added Stieltjes face monotonicity, the padded/anchored
  transport invariant, and the `q`-face response-free-prefix/direct-response
  handoff. `check_round016.py` uses exact rational arithmetic in
  degree-scaled coordinates for `m=2,...,7` and
  `alpha in {1/20,1/5,49/100}`. It independently solves every canonical
  restricted system, checks strict canonical demands, old-face exact-point
  monotonicity, arbitrary signed lower retractions, anchored lower order,
  conservative strict boundary tests, exact preservation under zero padding,
  face/batch volumes, row/round/interaction/label ledger partitions, the
  strict integer stage cap, and stable labels. All
  three focused Round-014--016 checkers passed; Ruff lint/format checks passed.
  The focused build produced 61 pages with no undefined references or new
  overfull-box warnings. An independent read-only Round-016 audit rederived
  the all-face Stieltjes comparison, padded/anchored order, finite cap,
  nonzero warm anchor, every prefix/post coordinate, and the `q=m` edge; it
  returned clean. Repository-wide inventory/graph reconciliation remains
  controller-owned. Round-017 added the exact `ImplicitLowerHeap`, the scoped
  `LiteralDenseLowerSweep` comparison, and the all-layer implicit-diagnostic
  handoff. `check_round017.py` uses exact rational arithmetic on every
  canonical face for `m=2,...,7` and
  `alpha in {1/20,1/5,49/100}`. After each of a deterministic sequence of
  signed coordinate writes it compares the lazy heap maximum, every implicit
  lower coordinate, and all three boundary demands against a literal dense
  rebuild; it also checks that only the closed neighborhood is rekeyed, that
  the result stays below the exact restricted solution, the exact
  `3q^2`/`(q-1)(3q+2)/2` restart shocks, row/interaction/label partitions, and
  all stable labels. The checker and Ruff lint/format checks passed. The
  focused build produced 65 pages with no undefined references. The
  independent Round-017 audit rederived the residual/heap invariant, local
  rekeys, bulk-product charge, both edge cases and eleven-vectors, interaction
  and emission counts, memory peaks, native suffix, and representation-only
  comparison scope; the checker, Ruff checks, and forced 65-page build passed,
  and the audit returned clean without an edit.
  Round-018 added the exact lazy-anchor tag representation, the three-key
  `FaceCarryLowerHeap` expansion, the scoped `DenseFreshAESP` restart
  accounting identity, and the all-expansion response-free handoff.
  `check_round018.py` uses exact rational arithmetic in degree-scaled
  coordinates for every expansion of every `m=2,...,7` instance and
  `alpha in {1/20,1/5,49/100}`. It uses a physically nested admission order,
  exercises flush-before-write and bulk replacements, finds strict successful
  endpoints with nonzero heap maximum, and compares every maintained raw
  residual, heap maximum, and lazy anchor coordinate with a dense rebuild.
  It verifies that old residuals/keys survive zero padding exactly, precisely
  three keys are inserted per expansion, lower anchors remain below the next
  exact point, the dense fresh-array identity `q(3q-1)/2`, all row/round/
  interaction/label partitions (including exact first-exposure and interaction
  totals but the retained numerical adjacency-round term), both `q=2` and
  `q=m`, and all stable labels.
  All Round-014--018 checkers passed; Ruff lint/format checks passed. The
  focused build produced 70 pages with no undefined references and only the
  three preexisting overfull-box warnings. Independent Round-018 review found
  one exact ledger wording contradiction: numerical adjacency rounds make
  `R_adj=m+1+O(A_fc)`, while only `R_int=m+1` and the structural
  first-exposure component are exact. The theorem, proof, README, STATUS, and
  checker were repaired together. Re-audit of the lazy induction, three-key
  transition, bulk-product/stage charges, dense-auxiliary identity, every
  vector coordinate, both horizon edges, native suffix, memory, and scope was
  clean; extended exact chains through `m=10`, all checkers, Ruff, diff check,
  and the forced 70-page build passed. Repository-wide inventory/graph
  reconciliation remains controller-owned.
  Round-019 added the exact settled center/momentum/estimate-point padding,
  the three-positive-cell proximal append, the objective face-shock identity,
  the positive analytical estimate shock, and the fully charged
  first-to-second-face audit. `check_round019.py` uses exact rational
  degree-scaled coordinates on every admission for `m=2,...,7` and
  `alpha in {1/20,1/5,49/100}`. It independently checks the imported
  composite proximal map, the unchanged old coordinates, all three strict new
  entries, the exact quadratic objective shock, the shifted Moreau solve, the
  positive estimate-shock lower bound, exactly twelve auxiliary records, the
  concrete row/round/interaction/label partitions, and every stable label.
  All Round-014--019 checkers, focused Ruff checks, and repository `make lint`
  passed. The focused build produced 73 pages with no undefined references and
  only the three preexisting overfull-box warnings. `make note-audit` reported
  18 notes across 5 tracks and `make note-graph` remained acyclic. Independent
  Round-019 review rederived the imported parameters, warm start, proximal
  cells, analytical shock, twelve-record/reset charge, all three vectors,
  `nu_1`, `C_2`, the `m=2` edge, and both total-round partitions. It checked
  308 exact transitions for `m=2,...,12`, reran the Round-018/019 checkers,
  Ruff, and a forced 73-page build, and returned clean without an edit.
  Final controller validation then caught one notation-registry issue in the
  new parameter display: the temporary AESP ratio alias `q_A` conflicted with
  the reserved FISTA namespace.  The display now defines
  `mu_E=kappa_A chi_A` directly, with the same mathematical value.  After that
  mechanical repair, all 187 repository tests, the Round-019 checker, Ruff,
  the 73-page build, and scoped diff checks passed.
  Round-020 added the exact one-stage nonsettled seed-face endpoint, its three
  strict first-batch demands, the twelve-cell nonsettled append, the
  optimum-free KKT shock budget, one extrapolated continuation stage, and the
  complete transition/prefix/post ledgers. `check_round020.py` uses exact
  rational degree-scaled arithmetic for `m=2,...,12` at
  `(alpha,sqrt(chi_A)) in {(1/10,1/3),(1/5,1/2)}`. It checks the shifted
  endpoint is nonoptimal, all three displayed margins, old/new proximal
  agreement, three positive appends, the exact Moreau certificate, its strict
  new-coordinate floor and KKT upper bound, nonzero momentum/extrapolation,
  the continuation shifted target, all round/row/label partitions, and every
  stable label. Round-019 and Round-020 checkers, scoped diff checks, and a
  forced 77-page build passed; the build has no unresolved reference and only
  the three preexisting overfull-box warnings. Independent Round-020 review
  rederived the endpoint, sharp range, three demands, KKT reset bound, carried
  relation, continuation stage, every vector, and both edge cases. It required
  one README repair distinguishing the zero-padded carried arrays from the
  three positive proximal appends; focused readback, checker, and diff checks
  then returned clean without an audit edit.
  Round-021 added the strict lower-center/proximal-start distinction, the
  exact `m>2` and terminal `m=2` second-batch margins, greedy safe ordering,
  a second positive KKT reset, two-admission prefix/post ledgers, and the
  explicit rate STOP. `check_round021.py` runs exact rational
  degree-scaled greedy AESP-CD for `m=2,...,12` and six rational values of
  `sqrt(chi_A)` from `1/10` through `9/10`, always at `0.999 rho_2`. It checks
  that `y+` is lower but fails `F_1`, the warm start has the displayed sharp
  margins, every greedy update on the first face is increasing, the output
  remains below the shifted and unshifted optima, all three second-batch signs
  survive, positive momentum drives the next center, the second proximal
  append has exactly twelve cells, `0<Psi_2<=B_2`, the second relative rule,
  exact threshold equality at `rho_2`, all row/round/interaction/label
  partitions, and every stable label. The checker and Ruff format/lint pass.
  The focused build produces 81 pages with no unresolved reference and only
  the three preexisting overfull-box warnings. Independent Round-021 audit
  rederived the center ratio and lower-but-noncertifying distinction, the
  safe-center greedy order, both margin systems and sharp `rho_2`, strict
  momentum, the second twelve-cell append and KKT reset, both oracle budgets,
  every prefix/post partition, and the exact rate STOP. It required one
  provenance repair from the KKT-mass contraction lemma to the imported
  safe-center theorem; focused readback, exact checker, Ruff, diff, and forced
  81-page build checks then returned clean.
  Round-022 added the exact settled `P_3` KKT-budget/Schur-drop obstruction,
  the sharp-order general settled bound, the conditional nested reset
  telescope, the actual-shock disclaimer, and the literal no-sharing
  caterpillar two-product count. `check_round022.py` reconstructs the
  degree-scaled three-vertex Hessian and shifted load in exact rational
  arithmetic, solves both restricted faces, verifies `g_0>0`, `g_1<0`, the
  Schur pivot, objective drop, reset budget, exact ratio decomposition, the
  surviving settled coefficient, the rational dominant term in the
  `Theta(q_r^-4)` conditional coefficient, actual canonical face volumes, the
  row-count identity through `m=24`, and every stable label/scope marker. The
  checker and Ruff lint/format checks pass. The focused build produces 85
  pages with no unresolved reference and only the three preexisting overfull-
  box warnings. Independent review rederived every demand, settlement, Schur,
  reset, inequality, asymptotic, conditional telescope coefficient, and row
  count. It required repair of missing `\qquad` tokens, erroneous stable-text
  strings, and explicit scope statements that `B` is only an observable upper
  budget, the actual settled shock is below `2 Delta`, and the two-product
  count assumes the named conservative no-sharing interface. Post-repair
  checker, Ruff, build/log, and source readback returned clean.
- Known gaps: The structural response handoffs deliberately discard accelerated
  auxiliary state and therefore prove no shock-free accelerated continuation.
  Round-016 preserves a coordinatewise lower vector across admissions, but not
  momentum or estimate-sequence energy. Round-017 makes its gate diagnostic
  incremental. Round-018 also removes its full-anchor copy and raw-product
  rebuild at each admission, but the named dense AESP representation still
  initializes fresh auxiliary records on every numerical face; no accelerated
  energy or scalar monotone potential is carried. The handoffs
  are exact-real, fixed-tree-family, RPPR-only statements, not graph-uniform
  solvers or finite-precision theorems. The currently specified composite
  Catalyst/AESP prefix covers only `alpha<1/2`; no such prefix is manufactured
  for the rest of the response theorems' `alpha in (0,1)` range. Its one proved
  caterpillar instantiation pre-exposes all of `S*=V`, remains at `k=0`, and
  discards the proved half-gap progress, so it says nothing about adaptive
  locality or arbitrary finite burn-ins. Its soft-order work statement is also
  nonuniform as `alpha -> 1/2`. The responder-native policy separately reaches
  `k=1` with only local rows and retains exact response progress, but performs
  no accelerated work. The Round-014 policy carries a genuine signed endpoint
  through the next gate, but only after a separately charged exact
  constant-size response computes `mu_1`; it therefore supplies no speedup and
  no scalable margin mechanism. Round-015 removes that response from the
  sign-certificate coordinate and commits one face without settlement, but
  its required lower-map sweeps and zero resets are comparison work, charged
  validation pre-exposes candidate rows, and its finite analysis still uses
  `mu_0,mu_1`; it proves no product improvement. Round-016 removes those
  whole-vector resets and preserves a lower coordinate anchor through every
  fixed canonical face. Round-017 removes each query-time growing-face scan,
  and Round-018 carries the residual/heap and lazy anchor through each face.
  Round-019 sparsely transports the four explicit auxiliary arrays only from
  an exactly settled, zero-momentum checkpoint; its estimate proof is reset,
  no enlarged-face accelerated stage is run, and the native suffix supplies
  the completion. Round-020 handles one actual nonsettled first-face state by
  a charged KKT reset and runs one continuation stage. Round-021 reaches a
  second nonsettled admission and continuation only in the sharper `rho_2`
  range and only for the exact greedy oracle; it then restarts at `B_2`
  without proving contraction from `B_ns`. Round-022 refutes only the simplest
  additive settled-reset packing below order `1/alpha`; its surviving
  `O(1/alpha)` bound omits nonsettled displacement and its
  `Theta(alpha^-2)` multi-reset telescope assumes exact settlement and ordered
  lower-center identities absent from the actual execution. Since the oracle
  uses `B` inside a logarithm, this is no accelerated-work obstruction.
  Candidate rows
  remain pre-exposed in the general growing-face policy, no face-general
  charged shock amortization is known for its non-settled momentum states,
  missing bulk products remain charged, and each later analysis cap uses
  `mu_k`. Thus the old half-gap still has no
  certified relation to `mu_k`, and the available refinement retains both a
  margin logarithm and the explicit `log(1/(1-2 alpha))` per-stage factor.
  The double-Y
  result fixes `s=e_o` and a core of dimension at most two. The caterpillar
  response for a generic prefix remains conditional on an already valid
  canonical checkpoint and proves no bound for constructing such a prefix.
