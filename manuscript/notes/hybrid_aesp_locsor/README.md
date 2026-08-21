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
or automatically exploring signed prefix, and the exact margin proposition
shows the additional certificate that its relative-gap state lacks. No
numerical
estimate-sequence energy is retained across these handoffs, so no shock-free
carryover or Euclidean-log collateral packing is claimed. The caterpillar
statement does not cover `rho_can<=rho<rho_cat`, another seed or policy,
repeated complete-positive-list output, a positive `m`-uniform `rho` range,
`kappa=1`, finite precision, bit complexity, transfer conditioning, arbitrary
graphs, or an RPPR-to-PPR conversion. The double-Y statement retains its
separate fixed-seed and fixed-rank-two scope.
