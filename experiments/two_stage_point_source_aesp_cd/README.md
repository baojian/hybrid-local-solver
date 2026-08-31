# Certificate-first point-source portfolio benchmark

This experiment asks a deliberately fair question: after a discovery engine
returns both a set and a numerical vector, is the fixed-envelope linear tail
still useful at the same PPR error target?

It records seven lanes:

- direct APPR at normalized residual threshold `alpha * eps`;
- direct priority Gauss--Seidel/SOR on PPR at the same maximum-residual
  threshold;
- a genuinely set-only Green-ball screen with hard volume cap `2 / eps`,
  followed by the linear tail on success and direct APPR on failure;
- APPR discovery at `rho = eps / 2` followed by the optional linear tail;
- an oracle-stopped RPPR objective-gap envelope with an equal three-way
  budget;
- the executable one-heap lower-safe RPPR envelope with that budget; and
- a tuned one-heap lane using the worst-case two-stage proxy
  `rho / delta = alpha^(-1/4)`.

Every numerical handoff is checked directly against the dense PPR reference.
For the four envelope lanes the script also runs ordinary accelerated PPR on
the returned principal set and records that optional refinement separately.
The objective-gap lane uses the exact reference optimum to detect its stopping
time, so it is a diagnostic rather than an implementable certificate.  All
other stopping rules are observable.  Work counts charged coordinate degrees
and terminal principal-matrix applications.

Run:

```bash
uv run python experiments/two_stage_point_source_aesp_cd/portfolio_benchmark.py \
  --output experiments/two_stage_point_source_aesp_cd/results.csv
```

## Deterministic sweep

`results.csv` contains 252 rows: six graph families, three values of `alpha`,
two error targets, and seven lanes.  All numerical direct handoff errors meet the
declared target.  In fact, the largest observed handoff-error ratio is `0.62`
of `eps`.  This confirms the certificate theorem: once APPR or monotone
RPPR/PPR coordinate descent has produced the numerical checkpoint used to
certify the set, Stage II is optional rather than required.

On the 30 nonzero direct-APPR cases, direct priority SOR has median work ratio
`1.00`, range `0.81`--`1.64`, with 2 wins, 24 ties, and 4 losses.  Thus the
priority heap is a viable portfolio peer but not a universal replacement.

If the optional tail is nevertheless forced, the four envelope lanes use
median total work between `4.93` and `5.48` times direct APPR and lose all 30
nonzero comparisons.  Within that artificial two-stage-only comparison, the
executable priority lane remains useful: versus the stricter APPR-envelope
lane it has median total-work ratio `0.94` and wins 20 cases; the tuned lane
has ratio `0.95` and wins 23.  Those figures measure envelope/refinement
tradeoffs, not end-to-end superiority at equal accuracy.

The set-only Green-ball lane succeeds in 10 of 36 cases and safely falls back
in the other 26.  It is correct and genuinely uses Stage II, but its median
work ratio to direct APPR is `3.13` (range `1.31`--`9.00`) and it wins none of
the 30 nonzero comparisons.  This is useful negative evidence: single-source
Green decay creates an executable adaptive screen, yet a conservative whole
ball still retains too many irrelevant rows to beat APPR on this sweep.

The practical conclusion is sharper than the original two-stage proposal:

1. numerical discovery engines should be allowed to return immediately;
2. a fixed-face tail is justified only by a genuinely cheaper **set-only**
   screening certificate, a stricter requested output, or optional polishing;
3. the remaining accelerated breakthrough is therefore set-only screening or
   exposure-local accelerated discovery, not another terminal solver.

## Mass-capturing-envelope diagnostic

`mass_capture_diagnostic.py` tests the alternative AESP--APPR interface.  For
each rooted graph and `alpha`, it solves principal PPR exactly on successive
BFS balls and records the first ball whose mass deficit is at most either
`sqrt(alpha)` (an exact lower checkpoint is cleanup-ready) or
`sqrt(alpha) / 2` (half slack for signed scratch and safe publication).

Run:

```bash
uv run python experiments/two_stage_point_source_aesp_cd/mass_capture_diagnostic.py \
  --output experiments/two_stage_point_source_aesp_cd/mass_capture_results.csv
```

The 36-row deterministic sweep is promising but not universal.  For the
half-slack certificate the median retained-volume fraction is `0.195`; 10 of
18 cases retain at most one quarter of the graph, while 5 require the full
graph.  At `alpha=0.16` the median fraction is `0.056`, but at `alpha=0.01`
it rises to `0.662`.  Paths, cycles, and the broom handle capture mass
locally; the star and low-`alpha` binary tree expose the limitation of blind
balls.  These are oracle principal solves and therefore diagnose the envelope
condition rather than prove a charged discovery algorithm.

`mass_screen_benchmark.py` executes the complete safe lane: geometrically
growing BFS envelopes under cap `2 / eps`, restarted signed CG scratch,
Stieltjes lower publication, priority-APPR cleanup on a mass trigger, and
zero-start APPR fallback otherwise.

```bash
uv run python experiments/two_stage_point_source_aesp_cd/mass_screen_benchmark.py \
  --output experiments/two_stage_point_source_aesp_cd/mass_screen_results.csv
```

It triggers in 17 of 36 cases and falls back in 19.  On the 30 cases with
nonzero direct-APPR work its median work ratio is `5.99` (range
`2.67`--`12.25`), with no win; even successful cases have median `5.17`.
All output errors are at most `0.523 eps`.  Thus the mass interface is a real
new theorem and an executable safe continuation, but naive BFS growth plus
restart-from-zero scratch is not yet a speedup.  Reuse, better envelope
proposals, or a cheaper mass certificate is essential.

`adaptive_mass_screen_benchmark.py` replaces blind balls by the support
exposed by priority APPR, tests mass only when that support volume doubles,
warm-starts the fixed scratch from the monotone checkpoint, and simply
continues the same priority trajectory if no trigger occurs.

```bash
uv run python \
  experiments/two_stage_point_source_aesp_cd/adaptive_mass_screen_benchmark.py \
  --output \
  experiments/two_stage_point_source_aesp_cd/adaptive_mass_screen_results.csv
```

The implementation also maintains the exact residual-mass interval from the
note and runs scratch only when its lower endpoint proves a positive trigger
margin.  This reduces the median ratio to the better of direct FIFO APPR and
direct priority APPR to `1.00` (range `1.00`--`1.64` on nontrivial cases).
It triggers in only 3 of 36 cases; those successful ratios are `1.00`,
`1.00`, and `1.11`, so the coarse sweep has no strict win.  The result is
useful: the scalar screen removes almost all speculative overhead, but it is
conservative and usually lets priority APPR finish directly.

A higher-accuracy sweep is stored in
`adaptive_mass_screen_high_accuracy_results.csv`:

```bash
uv run python \
  experiments/two_stage_point_source_aesp_cd/adaptive_mass_screen_benchmark.py \
  --output \
  experiments/two_stage_point_source_aesp_cd/adaptive_mass_screen_high_accuracy_results.csv \
  --epsilons 0.005 0.01 0.02
```

It contains 54 rows, triggers in 20, and has median ratio `1.00` and range
`0.158`--`2.00` on nontrivial cases.  There are two strict wins, both on the
96-vertex source-centered star at `epsilon=0.005`:

| alpha | adaptive work | best direct work | ratio |
|---:|---:|---:|---:|
| 0.01 | 570 | 3610 | 0.158 |
| 0.04 | 570 | 950 | 0.600 |

The largest semantic error is `0.748 epsilon`.  The mechanism is auditable:
after full-star exposure the source lies in a two-dimensional invariant
subspace, so exact CG needs two matrix applications (`scratch_work=380`) and
the published point needs no cleanup.  This is a real structured two-stage
speedup, not a universal claim; at looser targets direct APPR stops earlier
and the same lane can lose.

`leakage_screen_benchmark.py` implements the still shorter direct-PPR
certificate from the note.  It grows geometric BFS envelopes up to the same
hard cap, runs principal CG, and checks an upper error bar for every exterior
boundary leakage.  No RPPR solve, mass test, or support claim is used.

```bash
uv run python \
  experiments/two_stage_point_source_aesp_cd/leakage_screen_benchmark.py \
  --output \
  experiments/two_stage_point_source_aesp_cd/leakage_screen_high_accuracy_results.csv \
  --epsilons 0.005 0.01 0.02
```

The 54-row high-accuracy sweep passes the boundary gate in 44 cases and keeps
every error below `0.566 epsilon`.  Its nontrivial median ratio is nevertheless
`7.52` (range `0.184`--`22.79`), because blindly resolving every geometric
ball is expensive.  It has the same two strict star wins, at ratios `0.184`
and `0.700`.  Thus the direct leakage gate is a useful theorem and a clean
structured lane, but it does not replace the adaptive mass screen: candidate
envelope generation and response reuse remain decisive.

`adaptive_leakage_screen_benchmark.py` is the literal
**APPR/SOR discovery, AESP/CG fixed solve** variant.  It maintains the maximum
internal and boundary residual densities in two lazy heaps.  The sufficient
gate

```text
boundary_max + ((1-alpha)/(2 alpha)) * internal_max
    <= alpha * leakage_budget
```

costs one scalar query at a geometric support checkpoint; if it passes, the
algorithm discards the priority history and runs one principal CG solve.

```bash
uv run python \
  experiments/two_stage_point_source_aesp_cd/adaptive_leakage_screen_benchmark.py \
  --output \
  experiments/two_stage_point_source_aesp_cd/adaptive_leakage_screen_high_accuracy_results.csv \
  --epsilons 0.005 0.01 0.02
```

It switches in only 4 of 54 cases, all stars.  The median nontrivial ratio is
`1.061` (range `0.158`--`2.007`), every error is at most `0.748 epsilon`, and
the two strict wins cost `572/3610` and `572/950`.  The extra two units versus
the mass lane are the two explicitly charged heap queries.  This is the
cleanest executable evidence for the requested two-stage architecture:
monotone discovery normally returns directly, while a low-dimensional fixed
envelope can trigger a genuinely faster signed solve.

Changing the leakage/terminal budget split to
`0.50, 0.75, 0.90, 0.99` does not materially improve this lane.  The
216-row sweep in `adaptive_leakage_budget_sweep_results.csv` keeps the same
median ratio `1.061` and the same two meaningful wins.  More permissive
leakage budgets create a few nominal triggers only after the direct endpoint
has essentially been reached.  Budget tuning is therefore not the missing
mechanism.

## One-shot Green ball at high accuracy

`green_ball_high_accuracy_benchmark.py` implements the simplest genuinely
set-only point-source lane.  It computes the certified Green radius, exposes
that one ball under cap `2 / epsilon`, and runs exactly one zero-start
principal CG solve to a residual certificate.  It never solves intermediate
balls and never identifies RPPR support.

```bash
uv run python \
  experiments/two_stage_point_source_aesp_cd/green_ball_high_accuracy_benchmark.py \
  --output \
  experiments/two_stage_point_source_aesp_cd/green_ball_high_accuracy_results.csv
```

The 90-row sweep uses
`epsilon in {1e-4, 5e-4, 1e-3, 0.002, 0.005}`.  The ball completes in 85
cases and the standalone lane strictly beats the better of FIFO APPR and
priority SOR in 22.  Fifteen remain strict total-work wins after charging a
literal one-for-one APPR race (ten stars, four binary trees, and one grid).
The standalone wins comprise 13 stars, six binary trees, one grid, one path,
and one cycle.  Representative non-star ratios are:

| graph | alpha | epsilon | Green--CG / direct |
|---|---:|---:|---:|
| binary tree | 0.01 | 0.0001 | 0.103 |
| grid | 0.01 | 0.0001 | 0.489 |
| path | 0.01 | 0.0001 | 0.882 |
| cycle | 0.01 | 0.0001 | 0.945 |

The best overall ratio is `0.0258` on the star, and every semantic error is
at most `0.605 epsilon`.  The median successful-lane ratio is still `1.95`
and the worst is `24.85`, so the correct algorithm races this lane against
direct APPR; it does not force the ball solve.  With one-for-one charged
scheduling, success costs at most twice the faster lane and a cap failure
costs at most twice direct APPR.

`green_ball_scaling_benchmark.py` repeats three parameter pairs on graphs of
roughly 1,000--2,000 vertices.  Of 18 rows, 17 screens complete and six win.
The high-accuracy wins persist on the 1024-leaf-scale star (`0.0526`), the
depth-10 binary tree (`0.380`), a 1024-vertex path (`0.882`), and a
512-handle broom (`0.882`).  The 32-by-32 grid is a clear loss, reaching ratio
`5.08` at `(alpha, epsilon)=(0.01, 1e-4)`.  This scaling check rules out the
interpretation that the positive results are merely 96-vertex saturation,
while again showing why the fair race is mandatory.

`green_appr_warm_hybrid_benchmark.py` couples the two ideas literally.  While
the ball is exposed, priority APPR receives an equal exposure-work budget;
its current vector is then restricted to the ball and used as the sole warm
start for one CG solve.  The accounting includes both BFS and APPR work.  The
90-row result has 19 strict wins, median successful ratio `1.614`, and a
median reduction of four CG iterations.  It preserves all five winning graph
families; representative ratios are `0.217` on the binary tree, `0.421` on
the grid, `0.782` on the path, and `0.870` on the cycle at
`(alpha, epsilon)=(0.01, 1e-4)`.  A warm start can occasionally take more CG
iterations than zero (the residual may have a worse spectral mix), so the
robust fixed-face implementation should race zero-start and warm-start CG or
use an independently certified solver-selection rule.  Correctness never
depends on the warm start because the residual stopping certificate is the
same.

`halo_leakage_diagnostic.py` is an oracle diagnostic, not an algorithmic
claim.  It tries every priority-support checkpoint and several halo depths,
charging one exposure, scan, and warm CG solve.  At `epsilon >= 0.005` it
finds only the same two star wins.  At `epsilon = 1e-4`, path and cycle begin
to cross over.  This explains why the theorem-driven one-shot Green lane is
the cleaner implementation: the high-accuracy regime, not checkpoint
selection, creates the additional wins.

`single_ball_leakage_oracle.py` asks how much could be gained by selecting a
single smaller BFS ball and applying the leakage gate once.  It finds 23
wins, only one more than the fixed Green radius.  The extra case is the
high-accuracy broom: radius 47 stops just before the high-degree hub and has
ratio `0.738`, whereas the Green radius crosses the hub and exposes the whole
broom.  Thus arbitrary multi-radius search has little observed upside, but a
specific high-degree boundary event matters.

`degree_shock_hybrid_benchmark.py` makes that event implementable.  Before
the first BFS layer whose maximum degree is at least eight times the retained
median (and at least eight), it permits one CG-plus-leakage attempt.  If the
gate fails, its candidate warm-starts the final certified Green ball; if it
passes, the algorithm stops.  Exactly one of 90 cases triggers the rule, the
broom attempt passes, and the executable standalone lane matches all 23
oracle wins.  Its extra broom ratio `0.738` is not a fully charged fair-race
win, so the fair count stays 15.
This is not a universal pruning theorem--the constant eight is a transparent
policy choice--but it is a charged, safe example of how a structural Stage 1
event can avoid a high-degree decoy without identifying exact RPPR support.

## Why exact RPPR support is not the default Stage 1

`exact_support_cost_diagnostic.py` compares literal monotone RPPR
Gauss--Seidel discovery at `rho=epsilon/2` with Green--CG and direct PPR on
five graphs of 1,024--2,047 vertices at `epsilon=1e-4`.  The exact RPPR set is
often smaller than the Green envelope, but discovering it numerically is not:
the median RPPR-discovery work is `7.92` times Green--CG and `9.26` times
direct PPR.  Examples include:

| graph, alpha | exact support `(nodes, volume)` | RPPR discovery | Green--CG | direct |
|---|---:|---:|---:|---:|
| path-1024, 0.01 | `(41, 81)` | 45,518 | 5,565 | 6,312 |
| star-1024, 0.01 | `(1024, 2046)` | 1,054,713 | 6,138 | 116,622 |
| tree-depth-10, 0.01 | `(2047, 4092)` | 1,996,082 | 49,104 | 129,100 |
| grid-32x32, 0.01 | `(324, 1254)` | 564,368 | 184,632 | 36,317 |

This is not a lower bound against every accelerated active-set method.  It is
evidence against making exact support a mandatory terminal contract: a
smaller exact set does not compensate for repeated changing-face numerical
work in the current implementation.  The interval face verifier remains
available when a candidate and strict KKT margins are already supplied.

## Coarse APPR proposal plus an exact-face verifier

The structural verifier does not accept raw floating signs.  It computes the
retained residual, uses $Q_A\succeq\alpha I$ to bound the face-solution error,
and propagates that bound to a lower interval for every active coordinate and
an upper interval for every boundary KKT key.  A face is called certified
only when all intervals have the required strict sign.  Re-running the APPR,
SOR, and exact-batch sweeps with this guard leaves all reported counts
unchanged.  The saved-results audit additionally enumerates all 8,096
candidate faces of 36 randomized small tree/unicyclic systems; it observes no
false certificate and certifies the exact support in all 36 cases.

`appr_exact_face_screen_benchmark.py` implements the most literal hybrid
suggested by the two-stage viewpoint.  A resumable priority-APPR lane is
checkpointed at residual parameters `16*rho`, `8*rho`, `4*rho`, and
`2*rho=epsilon`.  At each checkpoint, its support and the one-hop expansion
are optional candidate faces.  On tree or unicyclic candidates, the
implemented structural solver computes the RPPR face point and a complete
boundary KKT scan either certifies exact `S*` or rejects the snapshot.

The exact-tail benchmark uses `rho=epsilon`; verifier work is raced one-for-one
against the continuing APPR state.  Hence
direct APPR returns before the verifier can make the total exceed twice the
direct work.  Across 90 cases on 1,024--2,047 vertices, 19 nontrivial
exact-support certificates finish before the direct lane and four strictly
win.  Their ratios are `0.132`, `0.276`, `0.590`, and `0.921` (two stars and
two binary trees).
Those four return the exact RPPR verifier point.  The CSV now also runs and
charges a fresh ordinary-PPR solve on every certified face; four cases remain
standalone wins and the two stars remain wins under the conservative fair
race charge.  Every Stage-2 output is checked against full PPR.
The CSV also charges a retained-factor backsolve: it raises the standalone
count to six while preserving the same two fair wins.
This is a concrete safe `APPR proposal -> exact AESP/structural face solve`
algorithm, but the exact KKT margin and structural face remain
instance-selective.

`sor_support_then_solve_benchmark.py` is the corresponding AESP-CD/SOR lane.
It starts from the zero RPPR lower point, adds every newly positive residual
row to a support-safe candidate, and checks that face only at powers of two
in accumulated SOR work.  It never runs a high-accuracy changing-face solve.
The exact-tail benchmark likewise uses `rho=epsilon`.  When the structural
KKT verifier passes, the final face is solved once; when
the direct APPR lane finishes first, all SOR state is discarded.  Six of 90
exact lanes finish before APPR in the half-split baseline; the tuned counts
are eight standalone and five strict wins after charging both sides of the
fair race.  Their total-work ratios are `0.088`, `0.118`, `0.345`, `0.444`,
and `0.593`.  This is the cleanest executable two-stage AESP-CD
variant in this directory.  A separately charged fresh ordinary-PPR solve
preserves all five fair-race wins.
Retaining the verifier factors raises the standalone count from five to seven
and preserves the same five fair wins.

`batch_exact_active_set_benchmark.py` is the exact-refit baseline at
`rho=epsilon`.  It solves
the current structural RPPR face, admits every positive exterior key, and
repeats until global KKT or the direct APPR race wins.  It certifies 75 of 90
cases and beats APPR in 43 standalone; 13 nontrivial wins survive the fair
charge across stars, a binary tree, paths, cycles, and brooms.  These are
early-return counts.  With a fresh ordinary-PPR Stage 2, 33 standalone and 8
fair wins remain; retaining the final factors raises those counts to 37 and
9.  The batch words
are the important negative evidence: the star admits 1,023 leaves at once and
the binary tree doubles, but a path still performs 38 singleton refits.  The lane
is correct and useful in a portfolio, not a universal work theorem.

## Structural Stage 2: factor once instead of iterating

`structured_tail_benchmark.py` uses the same certified Green envelope but
replaces CG by an implemented sparse factorization and back substitution on
trees and unicyclic graphs.  It peels leaves with no fill and solves the
remaining cyclic tridiagonal core by two path sweeps.  The experiment charges
the actual scalar elimination/recovery updates and one residual/materialization
scan after exposure.  Since the solve is exact, the full `epsilon` is assigned
to Green truncation rather than split with a numerical tail.  On
path/cycle/star/binary-tree/broom graphs with 1,024--2,047 vertices, 56 of 75
balls fit the cap, 50 strictly beat the direct baseline standalone, and 35
remain strict wins after charging a one-for-one APPR race.  The median
successful standalone ratio is `0.302`; at
`(alpha, epsilon)=(0.01, 1e-4)` the path, cycle, star, and tree ratios are
`0.0469`, `0.0583`, `0.0526`, and `0.0951`.

`strict_two_stage_summary.py` is the synchronization check for the saved
tables and manuscript counts.  It audits every finite Stage-2 semantic error
and reports:

| Lane | Certified/nontrivial | RPPR early raw/fair | Fresh PPR Stage-2 raw/fair |
|---|---:|---:|---:|
| APPR proposal | 28/19 | 9/4 | 4/2 |
| SOR proposal | 75 | 8/5 | 5/5 |
| Exact batches | 75 | 43/13 | 33/8 |
| Tree messages | 60/51 | -- | 27/14 |
| Green structural | 56 | -- | 50/35 |

On the 51 nontrivial promised-tree rows, racing direct APPR, tree threshold
messages, and structural Green round-robin still leaves 23 wins after the
conservative three-way charge: Green supplies 21 and threshold messages
supply two.

The fresh Stage-2 column deliberately refactors the same principal matrix;
the retained-factor arithmetic model gives APPR, SOR, and exact-batch
raw/fair counts of 6/2, 7/5, and 37/9.
The synchronization check also builds reusable leaf/cyclic factors once and
applies them to both RPPR and ordinary-PPR right-hand sides on independent
path, broom, and cycle cases plus 80 deterministic randomized tree/unicyclic
systems; every solve agrees with a sparse direct solve.

This is the strongest evidence for the two-stage architecture.  Once the
operator stops changing, a supplied width-`w` elimination order solves the
principal system in `O(w^3 * volume)` work.  For fixed `w` and cap
`O(1/epsilon)`, the successful branch is `O(1/epsilon)`, stronger than the
generic `O_tilde(1/(epsilon * sqrt(alpha)))` CG bound.  No analogous claim is
made for arbitrary graphs, where fill and decomposition discovery must be
charged.

## Exact rooted-tree Stage 1

`tree_threshold_hybrid_benchmark.py` implements the point-source tree theorem
rather than treating it as a provider oracle.  Every active subtree exports a
scalar Schur response and the next activation threshold; admitting a strict
positive frontier label changes one handled record on each ancestor.  Rooting
is lazy: the implementation scans an adjacency list only when that vertex is
admitted, so it does not hide a full-tree preprocessing pass.  The final face
is solved once; a separate global KKT verifier audits the implementation.

```bash
uv run python \
  experiments/two_stage_point_source_aesp_cd/tree_threshold_hybrid_benchmark.py \
  --output experiments/two_stage_point_source_aesp_cd/tree_threshold_hybrid_results.csv \
  --random-audit
```

All 60 path/star/binary-tree/broom cases certify.  Excluding nine cases in
which direct APPR itself performs zero work, the exact lane wins 27 of 51
standalone and 14 of 51 after a literal one-for-one APPR charge.  The exact
Stage 2 needs no numerical-error share, so the tuned lane uses `rho=epsilon`.
If Stage 1 exports only `S*`, Stage 2's ordinary principal-PPR solve replaces
the RPPR recovery solve and the counts stay 27 and 14.  At
`(alpha, epsilon)=(0.01, 1e-4)`, that literal version uses `1630/6312` on the
path and broom and `17391/116622` on the full-support star.  At `epsilon=5e-4`
the star support is only the source and the ratio is `2046/34782=0.059`.
Every fixed-face PPR output meets the semantic target.  The independent RPPR
solve/KKT scan is an audit, not part of the algorithmic work.  A randomized
check of 1,890 small trees also passed the structural solve and global KKT
verifier.

## Randomized OP2 inner-face transfer

`randomized_op2_inner_face_benchmark.py` tests the new composition with the
companion OP2 theorem.  It is deliberately **not** an implementation of the
Koutis--Miller--Peng SDD solver.  Each exposed face is solved directly and
then perturbed in a random direction whose active residual passes exactly the
deterministic acceptance test used by the proved randomized wrapper.  This
isolates the post-solver claims: safe threshold admission, cap exit on a
strict inner face, direct RPPR return, and an independent ordinary-PPR
Stage II.

The saved 67-row run covers seven graph families over three `alpha` values and
three accuracy targets, plus four tiny-`rho` stress cases designed to reach
the phase cap before discovering all of `S*`.  All 67 direct outputs and all
67 literal Stage-II outputs meet the semantic PPR target.  The four stress
cases return strict inner faces; the largest normalized error ratios are
`0.500010` for the direct RPPR point and `0.462166` for Stage II.  Both stages
include randomly shaped errors that pass their exact residual acceptance
tests.  The largest face-gap ratio is below `1.09e-8`.

Run it with:

```bash
uv run python experiments/two_stage_point_source_aesp_cd/randomized_op2_inner_face_benchmark.py
```

The independent exact proof audit is
`experiments/proof_audits/two_stage_point_source_aesp_cd/randomized_op2_transfer.py`.
It exhausts 171 positive inner faces on 40 rational graph instances and then
checks four incomplete capped path faces.  It verifies the squared
strong-convexity transfer and the ordinary principal-PPR semantic bound with
exact fractions.
