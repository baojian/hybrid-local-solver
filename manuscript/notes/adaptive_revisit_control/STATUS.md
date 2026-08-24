# Direction status: adaptive_revisit_control

Last reviewed: 2026-08-21
State: proved-open

## Exact question and contract

- **Question:** What can a causal revisit ledger safely certify or control, and
  can several local policies share one irreversible state with a best-arm work
  guarantee?
- **Model:** For literal SOR traces, `r = b - Q x` under the shared PageRank
  matrix. For exact-settlement results, single-seed RPPR uses nested canonical
  restricted solutions and true-support KKT boundary admissions.
- **Accuracy namespace:** The SOR gate is note-scoped
  `max_u |r_u|/sqrt(d_u) <= g = alpha * eps_ppr`. RPPR results use `rho` and do
  not assert a conversion to `eps_ppr` or other repository tolerances (Section
  `sec:scope`).
- **Access and charged work:** Paid row operations cost `c(u) = 1 + d_u`;
  guarded skips cost zero. Enumeration, ranking, copying, scheduling,
  settlement, and response work must be charged separately when present
  (equation `eq:charge`). RPPR volume bounds use adjacency degree-volume,
  within the stated factor-two conversion. The three-arm and double-Y theorems
  additionally separate adjacency, gate/control, response construction,
  updates and queries, state writes, persistent/transient cells, recovery,
  validation, and exact output. The growing branch-caterpillar obstruction
  and both kinetic/canonical reporters report the shared exhaustive vector
  `(C_adj,R_adj,R_int,C_pre,C_ctl,C_rec,C_resp,M_pers,M_tmp,C_mat,C_emit)`;
  every exact tip query/rekey and every certificate/output cell is charged.
- **Intended result:** Safe diagnostics, switching, and portfolio wrappers that
  inherit a proved arm's work; not an assertion that feedback itself creates a
  graph-uniform accelerated arm.

## Claim ledger

- **Source:** Adaptive restart supplies only global oscillation-based
  motivation. The frontier artifact supplies the measured revisit statistic
  (Section `sec:scope`).
- **Proved here:** Exact multiplicity and causal four-way ledgers
  (`lem:multiplicity`, `prop:causal-ledger`); two-level revisit factorization
  and online bank (`thm:two-level-factorization`, `thm:revisit-bank`);
  absorption-safe arbitrary switching at exact RPPR checkpoints
  (`thm:absorption-safe-switch`); safe bounded-relaxation fallback,
  branchable portfolios, geometric restart, and learned exploration floors
  (`thm:safe-adaptive`, `thm:budgeted-prefix`, `thm:portfolio`,
  `thm:restart-portfolio`, `cor:learned-safe`); endpoint-path activation tokens
  with `kappa = 1` and work at most `4/rho`
  (`thm:path-token-countdown`); and a `kappa = 1` exact common-state token
  system on the center-seeded three-arm spider for every legal certified batch
  order (`thm:three-arm-spider-token-countdown`). The spider uses actual common
  affine transfer records, costs `O(C(S*)) = O(1/rho)` exact-cell work, and
  performs no eager untouched-tip rekey or arm-private simulation. On the
  double-Y seeded at one branch vertex, `s=e_o`, with two adjacent degree-three
  branch vertices, `thm:double-y-two-core-token-countdown` preserves the same
  `kappa = 1` token
  tightness for every legal batch order. Its common response interface is
  scalar before the second branch is admitted and a full-rank `2 x 2` Schur
  core afterward. It has a complete `O(C(S*)) = O(1/rho)` exact-cell ledger;
  for `zeta=(1-alpha)/(1+alpha)` and
  `rho < zeta/[3(3+zeta)]`, every legal order necessarily enters the rank-two
  phase. On the branch caterpillar, eliminating actual pendant prefixes leaves
  an SPD tridiagonal core; a balanced affine-transfer tree supports one named
  append/update or tip query in `O(log(2+m))` exact response work with `O(m)`
  retained cells (`rem:branch-caterpillar-implicit-transfer-comparator`). For
  the backbone-first exact-KKT positive-subset policy,
  `thm:branch-caterpillar-kinetic-delta-reporter` upgrades that comparator to
  the named exact all-positive `CaterpillarKineticDelta` state. It emits each
  newly positive label once, supports membership and proposed-batch checks,
  and has exhaustive vector
  `(Theta(m),Theta(m),J+1,0,O(m log(2+m)),0,O(m log(2+m)),Theta(m),O(m),Theta(m),Theta(m))`
  for `2m-1 <= J <= 3m`. Thus its exact-cell work is
  `O(m log(2+m))`; it is an output-delta theorem, not a canonical
  all-violations, repeated-full-list, or `kappa=1` theorem. The vector includes
  every proposed-label membership test; extra speculative calls and separate
  replies/rounds are additive, not free. On the stricter explicit range
  `0 < rho < rho_can(m,alpha) <= rho_cat(m,alpha)`, the actual canonical
  all-violations chronology has exactly `m` three-label distance-layer batches
  (`thm:branch-caterpillar-canonical-layer-reporter`). The named exact-real
  `CaterpillarCanonicalLayerDelta` state has exhaustive vector
  `(Theta(m),Theta(m),m+1,0,Theta(m),0,O(m log(2+m)),Theta(m),O(m),Theta(m),Theta(m))`.
  Early side leaves, long-arm vertices, and new branch vertices alter only
  constant many transfer cells per batch; at most two exact parent queries
  certify the whole boundary. Positive ties are co-admitted and the strict
  range excludes equality on the trace.
- **Conditional:** A one-state `K*kappa` best-arm theorem requires
  interference-monotone and own-service-progress countdowns
  (`thm:mergeable-countdown`). Finite-menu inheritance requires an arm that
  already has the target accelerated bound (`cor:inherit`).
- **Measured:** The fixed two-rung schedule beats the full frontier adaptive
  artifact by 12% on the available campaign; memory has no demonstrated gain
  there (Section `sec:scope`).
- **Refuted:** The scalar ratio alone neither orders work nor chooses relaxation
  direction (`prop:not-order`, `prop:nonidentify`); a support-safe fixed-band
  one-edge handoff has an `Omega(1/alpha)` exact tail
  (`thm:two-vertex-two-rung-obstruction`); legal exact tree batch orders have an
  unbounded full-settlement work gap (`prop:batch-order-obstruction`);
  continuous energy countdowns cannot uniformly pay activation work
  (`prop:no-continuous-activation-countdown`). For the branch-seeded
  degree-three caterpillar and exact
  `0 < rho < rho_cat(m,alpha) <= 1/3`, one legal exact-KKT positive-subset
  singleton order reaches an
  `m`-vertex branch core and forces `m(m+1)` exact old-key writes in the named
  literal `EagerTipKey` state
  (`prop:branch-caterpillar-eager-rekey-obstruction`). At its first long-arm
  append, one new activation cannot pay `m+1` old-key rewrites; pairwise rekey
  tokens have quadratic initial mass. This is not a lower bound against lazy,
  sign-only, kinetic/group, or on-demand implicit reporters. The threshold is
  fixed-`m` and need not be uniform in `m`; the chronology is not the canonical
  all-violations batch, which may co-admit deferred positive leaves.
- **Open:** A charge-comparable implicit reporter for the remaining canonical
  range `rho_can <= rho < rho_cat` or arbitrary pre-backbone positive-subset
  orders on an unbounded branch-core backbone, or for a cycle; a
  forced-spreading accelerated arm; or a
  certified finite reduction of the continuous relaxation family. The spider,
  double-Y, and both caterpillar results are exact real-cell algebra only;
  finite precision and bit complexity are open.

## Central blocker

The core algebra itself extends: a balanced transfer product represents the
growing tridiagonal response and a dense optimum shift without global
coordinate rewrites. CaterpillarKineticDelta closes one explicit
backbone-first positive-subset/delta interface with all named queries charged.
CaterpillarCanonicalLayerDelta additionally closes the actual canonical trace
on `rho < rho_can`, where every boundary is one newly live three-label layer
(its rows are first scanned there even when labels were revealed one layer
earlier) and the heap has no surviving key to repair. The missing component is a
reporter for the rest of the canonical `rho_cat` range or arbitrary
pre-backbone interleavings. Literal eager exact keys are ruled out at linear
work by the caterpillar witness, but those policies and cyclic fronts remain
beyond this test.

## Dependencies and reusable outputs

- **Formal registry dependencies:** `propagate_settle_framework` and
  `delayed_reflection_ladder`.
- **Context/provenance:** `frontier_adaptive_ladder` and `two_rung_sor`
  provide the measured policy ancestry and comparison arms; they are not
  direct proof-import edges.
- **Supplies to:** Safe controller/portfolio designs, no-reset exact-settlement
  switching, revisit banks, and common activation-once response countdowns on
  endpoint paths, the center-seeded three-arm spider, and the adjacent-branch
  double-Y seeded at one branch vertex, `s=e_o`, with response-core rank two;
  also the exact `EagerTipKey` global-rekey obstruction, query-charged
  tridiagonal transfer comparator, and backbone-first
  `CaterpillarKineticDelta` all-positive delta reporter on a growing branch
  caterpillar; plus the fixed-family canonical layer chronology and the
  `CaterpillarCanonicalLayerDelta` reporter with its full eleven-vector.

## Resume here

- **Exact pointer:** `thm:mergeable-countdown`, `lem:activation-token-countdown`,
  `thm:path-token-countdown`, `thm:three-arm-spider-token-countdown`, and
  `thm:double-y-two-core-token-countdown` for the common-state interface and its
  exact path, rank-one, and rank-two realizations;
  `prop:branch-caterpillar-eager-rekey-obstruction` and
  `rem:branch-caterpillar-implicit-transfer-comparator` for the growing-core
  STOP boundary, and `thm:branch-caterpillar-kinetic-delta-reporter` for the
  backbone-first positive-subset GO; then
  `thm:branch-caterpillar-canonical-layer-reporter` and
  `eq:branch-caterpillar-canonical-eleven-vector` for the strict canonical GO;
  Section `sec:remaining` for the graph-uniform target.
- **Next action:** Extend or refute the implicit interface on the remaining
  canonical range `rho_can <= rho < rho_cat` or under arbitrary pre-backbone
  positive-subset interleavings, then test a cyclic front. Charge every
  internal tip query, response update, certificate reply, and requested
  full-list output separately.
- **Stop/go test:** Proceed only if the reporter supports every order in its
  explicitly stated policy class and its query schedule plus token mass is
  charge-comparable. Eager exact-key rewrites, repeated full-core sweeps, and
  uncharged repeated full-list emissions are not admissible positive evidence.

## Verification

- **Source pointers checked:** Required context/conventions, adaptive-restart
  and RPPR literature notes, README, claim ledger, and all cited theorem
  sections above.
- **Checks last run:** Focused LaTeX build passed on 2026-08-21 (41 pages, no
  unresolved references or layout warnings); `make note-audit` passed with 18
  notes across 5 tracks; scoped tracked and untracked whitespace checks passed.
  Direct numerical comparisons of both scalar and rank-two Schur readouts with
  dense restricted solves agreed to below `3e-17`, and threshold signs were
  checked on both sides of `rho_link(alpha)`. The earlier three-arm theorem
  retains its independent read-only audit; the double-Y theorem also passed
  independent read-only audit, controller reconciliation, and Round-006
  promotion. For Round 008, direct dense solves checked every prescribed
  positive-subset admission, the affine reach-threshold identity, strict
  block-elimination shift, and full support for
  `alpha in {0.05,0.2,0.7,0.95}` and `m=2,...,8`; exact rational checks matched
  the tridiagonal transfer recurrence for core lengths `1,...,12`. For Round
  009, 100-digit direct restricted solves at
  `alpha in {0.05,0.2,0.7,0.95}` and `m=2,...,12` verified every reach sign and
  the last-column Green factorization, one-parameter update, affine coordinate,
  and crossing-key demand identities to below `1e-80`. For Round 010, exact
  rational restricted solves at
  `alpha in {1/20,1/5,7/10,19/20}` and `m=2,...,8`, with
  `rho=(9/10)rho_can`, reproduced all `m` prescribed canonical three-label
  batches and the terminal full support. The independent Round 010 audit was
  clean; its two wording hardenings now distinguish an appended arm-transfer
  cell from the induced branch-core absorption update and a newly live,
  first-scanned boundary row from a label revealed one layer earlier.
- **Known gaps:** The README states the interference-monotonicity and
  own-service-progress hypotheses behind the general mergeable-countdown
  theorem. The one-edge obstruction is a support-safe handoff/continuation,
  not automatically the literal zero-start benchmark trajectory. The double-Y
  result fixes both one adjacent pair of branch vertices and the branch-vertex
  seed `s=e_o`. The eager caterpillar STOP also fixes the branch seed
  `s=e_{b_1}`, `alpha in (0,1)`, a family-dependent exact range
  `0 < rho < rho_cat(m,alpha)`, and one legal KKT positive-subset singleton
  order; it rules out only literal eager exact demand cells. The kinetic GO
  fixes the same parameter range and the backbone-first policy class with a
  delta-label interface, not the canonical all-violations batch. Neither
  result claims an `m`-uniform positive `rho` range. The canonical layer GO
  fixes the still smaller analysis-side threshold `rho_can`, exactly `m`
  canonical batches, and the delta interface; it does not cover the remaining
  `rho_cat` range. Other seed placements, policy-robust all-positive reporters,
  cycles, finite precision, bit
  complexity, and an RPPR-to-PPR accuracy conversion remain open. No
  graph-uniform accelerated arm is proved here.
