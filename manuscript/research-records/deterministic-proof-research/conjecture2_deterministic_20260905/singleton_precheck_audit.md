# Optional exact singleton-support precheck

The separately versioned `singleton_precheck_rppr.py` exports
`solve_rppr_with_singleton_precheck(oracle, seed, alpha, rho, epsilon, *,
seed_degree_cutoff=32, fallback_solver=solve_rppr_combined)`.
No stable solver or package file is changed. The optimization has a useful
but specific scope: it recognizes when the exact optimum is supported on
the seed alone, particularly a seed leaf adjoining a large inactive hub.
It does not replace the general support-discovery algorithm.

## Exact criterion

Use degree densities `f_i=x_i/sqrt(d_i)`, and put
`q0=(1+alpha)/2`, `c=(1-alpha)/2`, `lambda=alpha*rho`.
The objective on nonnegative densities is

`J(f)=0.5 f^T(q0 D-c A)f-alpha f_seed+lambda sum_i d_i f_i`.

The Hessian is positive definite. If `rho*d_seed>=1`, zero satisfies all
KKT inequalities and is the unique optimum. If `alpha=1`, the coordinates
decouple and the exact nonzero answer is
`f_seed=1/d_seed-rho`; neither direct branch needs an adjacency query.

Assume `0<alpha<1` and `rho*d_seed<1`. The minimizer restricted to the seed
is positive and equals

`f_seed = 2 alpha (1-rho*d_seed)/(d_seed*(1+alpha))`.

Its seed gradient is zero. The gradient at a neighboring zero coordinate
`i` is `lambda*d_i-c*f_seed`; the gradient at every other zero coordinate
is `lambda*d_i>0`. Therefore the seed-only vector satisfies global KKT
conditions **if and only if**

`c*f_seed <= alpha*rho*d_i` for every seed neighbor `i`.

Positive definiteness makes this vector the unique exact optimum whenever
the inequalities pass. Equality is accepted correctly. If one inequality
fails, the trial cannot certify a seed-only optimum and falls back.

For `alpha=A/D` and `rho=P/R`, canceling positive `alpha` transforms the
neighbor test into the integer comparison

`(D-A)*(R-P*d_seed) <= P*d_seed*(D+A)*d_i`.

The code precomputes the left side and the coefficient multiplying `d_i`.
There is no per-neighbor rational arithmetic, root extraction, rounding,
randomization, sort, or dictionary lookup. The exact returned density is
`2*A*(R-P*d_seed)/(R*d_seed*(D+A))`.

The returned vector satisfies all mathematical safety properties used by
the continuation: it equals the optimum, is nonnegative, and has source
density `alpha*rho` at the seed, `c*f_seed/d_i <= alpha*rho` at a neighbor,
and zero elsewhere. Thus `0 <= b-Qx <= alpha*rho*w`. Moreover

`d_seed*f_seed + rho*d_seed <= 1`,

because `2*alpha/(1+alpha)<=1`; its support volume is less than `1/rho`.
This is a final-output shortcut. Its density can be a general rational,
not a dyadic number, so the implementation does not present it as an
already formatted intermediate baseline for the dyadic corrector.

## Trial work and result contract

The trial first requests the seed degree. After the zero/direct branches,
it scans the seed row only if `d_seed<=seed_degree_cutoff`. It obtains the
degree of each encountered neighbor and immediately tests the inequality.
On the first failure it stops reading the row. It never asks for a
neighbor's adjacency row. On success it reads the entire seed row and
checks its length against the supplied degree. As in the original problem,
the oracle input is assumed to be a finite simple undirected graph; the
trial does not attempt global graph validation.

For a tried row, the trial reads at most `d_seed` adjacency entries and
`d_seed+1` degrees, performs `O(d_seed+1)` integer arithmetic operations,
and retains only a constant number of numerical records apart from the
oracle's own row iterator. In the nontrivial regime `d_seed<1/rho`, so this
is `O(1/rho)` prefix word work, stronger than the requested
`O((1/rho) log(2+1/rho))`. A cutoff skip costs `O(1)` word operations and
one degree reply. The fixed default cutoff also bounds the tried prefix
by a constant, independently of graph size.

The added integers have a constant multiple of the input parameter and
encountered degree/label encoding lengths. There is no aggregation of
degree denominators. With `B` bounding those bit lengths, a conservative
naive exact-arithmetic bound is `O((d_seed+1) B^3)` for a trial, including
parameter normalization and the one successful rational output. As with
the main solver, separately expensive oracle internals must be included in
the oracle-access model rather than treated as free.

`SingletonPrecheckResult` has five fields:

- `output` and `objective_gap_bound`;
- `outcome`: `zero`, `alpha_one`, `singleton`, `failed_trial`, or
  `skipped_cutoff`;
- `trial_metrics`, a separate record of seed/neighbor degree queries,
  seed-row requests, entries, inequality checks/failure, cutoff and row
  length checks, fallback calls, and directly produced output words;
- `fallback_result`, either `None` or the **identical object** returned by
  the supplied fallback solver.

The fallback receives the original oracle and exact normalized parameters.
There is deliberately no cache layer: a repeated seed degree or row read
by the fallback remains real work and is counted again. Total work is the
sum of the explicit trial ledger and the untouched fallback ledgers. No
trial operation is inserted into a repair ledger or silently credited as
a cache hit. The named logical counters are not a claim to instrument each
Python bytecode instruction. The supplied fallback is required to obey the
certified-solver result contract; arbitrary callbacks cannot acquire a
correctness guarantee merely by being passed to this wrapper.

## Exact checks

`test_singleton_precheck_rppr.py` and
`singleton_precheck_verification.json` pass five groups, including:

- 664 cases on every connected labeled graph through four vertices, with
  every seed, two rational alpha values, and two regularization scales;
- 493 exact singleton successes and 171 failures, checked against an
  independent exhaustive dense KKT oracle;
- exact equality and both sides of the two-vertex threshold;
- three actual combined-solver fallback cases, preserving the returned
  object, output, stages, certificates, and all fallback graph-query order;
- zero and alpha-one branches, two cutoff skips, and immediate stopping
  after the first failing neighbor in a longer seed row;
- a degree `10^30` inactive boundary with hash-forbidden 258-bit labels:
  two degree replies, one seed adjacency entry, no boundary row.

The exhaustive test's fallback is an independently computed exact dense
solution; it is not used as a local algorithm or claimed as the production
fallback. The three actual-fallback tests separately exercise the real
certified continuation and verify final objective gaps with the dense
oracle. The cutoff-delivery sentinel fixtures test routing only and make
no optimality claim about their artificial callbacks.

## Small paired practical comparison

`study_singleton_precheck.py` and `singleton_precheck_study.json` contain
reference/precheck/precheck/reference runs for three virtual graphs. All
12 outputs pass separate exact sparse objective certificates. Complete
answers, all ledgers, source hashes, Python/platform provenance, CPU/wall
times, and separate verification costs are retained. Only timing clocks
use floating point. The fallback was the unchanged combined prototype.

| Case | Reference iterations | Precheck iterations | Total counted adjacency entries, reference -> precheck | Median CPU seconds, reference -> precheck |
| --- | ---: | ---: | ---: | ---: |
| Billion-leaf hub, leaf seed | 112 | 0 | 118 -> 1 | 0.03609 -> 0.0000595 |
| Billion-vertex path, endpoint seed | 400 | 400 | 3526 -> 3527 | 0.37573 -> 0.36595 |
| Million-by-million grid, corner seed | 512 | 512 | 2682 -> 2683 | 0.33120 -> 0.32193 |

The hub returns the exact optimum with just two degree replies and one
adjacency entry; the reference made 13 degree replies and read six external
row entries across its stages, with 118 total entries including cached
numeric scans. Both failed trials added exactly two degree replies and
one adjacency entry, preserving the full fallback result exactly. Their
small lower observed times are timing variation, not evidence that failed
trials accelerate the unchanged fallback. The concrete benefit is exact
early termination on a common simple support shape; the bounded extra
prefix is the cost on other instances.
