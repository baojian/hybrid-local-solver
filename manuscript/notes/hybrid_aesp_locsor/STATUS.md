# Direction status: hybrid_aesp_locsor

Last reviewed: 2026-08-21
State: proved-open

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
  accelerated prefix. The three-arm and double-Y structural
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
  peak and no conversion traversal or first-layer replay is charged.
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
  theorem. Neither result bounds an uncapped or automatically exploring
  signed AESP prefix. Even for the full-envelope policy, the shorthand
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
  must also be below the sharp margin `mu_k`.
- **Open:** A graph-independent early-AESP prefix bound, local RPPR work from
  a retained arbitrary signed warm start, a lower bound and charged local
  certificate for all canonical margins `mu_k`, another seed on the double-Y,
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
before acceleration and discards all numerical progress. The live hybrid
blocker is therefore a capped automatically exploring signed Phase I whose
state either satisfies the sharp margin gate or has a separately charged
one-sided certificate, without paying a margin-dependent repeated-work term
that destroys the target. The remaining canonical range and wider
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
  `thm:branch-caterpillar-canonical-layer-reporter`; the named capped prefix
  also imports `aesp_cd_l1_rppr`, `thm:aesp-cd-relative-oracle` and
  `cor:aesp-cd-certified-envelope`. The expansion-shock and
  safeguarded collateral results delimit excluded numerical-energy routes but
  are not used as amortizations here.
- Supplies to: The synthesis and response-composition directions through a
  proved one-pass common-state conversion for scalar and fixed rank-two cores,
  and now for the strict canonical growing tridiagonal core; exact resource
  ledgers; one locally exposed native `k=1` product-scale execution; one fully
  exposed fixed-family AESP comparison witness; the sharp signed gate margin
  and its margin-dependent stage-cap interface; the uncapped-prefix
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
  `cor:branch-caterpillar-envelope-aesp-product`; finally
  `sec:branch-caterpillar-signed-gate-margin` and
  `prop:branch-caterpillar-signed-gate-margin`. Graph-uniform gates remain
  `conj:early-locality`, `sec:open-gap`, and `sec:composite-hybrid`.
- Next concrete action: Starting from the paid local `k=1` checkpoint, prove a
  lower bound or locally checkable one-sided certificate for `mu_k` that lets a
  capped signed AESP state trigger a later canonical batch within product
  work. Otherwise give an exact family where the margin-dependent stage cap
  forces repeated-prefix work. Separately extend or refute the response beyond
  `rho<rho_can`.
- Stop/go test: Stop any proof that privately replays a canonical order,
  rescans old prefixes per admission, identifies numerical support with safe
  admission, or transports estimate-sequence energy without an explicit
  shock. A direct one-pass build from the actual checkpoint support is allowed;
  reconstructing its historical gate states is not. Also stop any prefix proof
  that leaves its stage count uncapped, calls full-family exposure local
  discovery, infers prefix work from the post-response ledger, or treats a
  constant relative objective gap as an exact gate sign without paying the
  margin or a one-sided certificate.

## Verification

- Source pointers checked: Root and note-level agent rules, shared problem,
  related-work/results/broadcast ledgers, Round-011 through Round-013 assignments,
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
- Known gaps: The structural handoffs deliberately discard all numerical
  progress and therefore prove no shock-free accelerated continuation. They
  are exact-real, fixed-tree-family, RPPR-only statements, not graph-uniform
  solvers or finite-precision theorems. The currently specified composite
  Catalyst/AESP prefix covers only `alpha<1/2`; no such prefix is manufactured
  for the rest of the response theorems' `alpha in (0,1)` range. Its one proved
  caterpillar instantiation pre-exposes all of `S*=V`, remains at `k=0`, and
  discards the proved half-gap progress, so it says nothing about adaptive
  locality or arbitrary finite burn-ins. Its soft-order work statement is also
  nonuniform as `alpha -> 1/2`. The responder-native policy separately reaches
  `k=1` with only local rows and retains exact response progress, but performs
  no accelerated work. The signed-margin proposition shows exactly what is
  still missing to combine those two properties: the old half-gap has no
  certified relation to `mu_k`, and the available refinement adds both a
  margin logarithm and the explicit `log(1/(1-2 alpha))` per-stage factor. The double-Y
  result fixes `s=e_o` and a core of dimension at most two. The caterpillar
  response for a generic prefix remains conditional on an already valid
  canonical checkpoint and proves no bound for constructing such a prefix.
