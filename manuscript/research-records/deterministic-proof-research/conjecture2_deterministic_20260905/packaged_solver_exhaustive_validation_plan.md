# Bounded deterministic validation plan for the packaged solver

Status: prepared, not executed. This plan targets the final packaged solver,
its deterministic maps, continuation, and output contract. It does not
repeat internal projected-waterfill or scalar-rebase trajectory tests already
covered by the dedicated practical-corrector suite. No randomized graph,
parameter, ordering, retry, or numerical oracle is used.

## 1. Exhaust all small rooted topologies without relabeling duplication

Enumerate all edge masks of simple graphs with n=2,...,5. Keep connected
graphs and fix the seed to label 1. Canonicalize each mask under every
permutation of labels 2,...,n, keeping the seed fixed. Retain the minimum
mask in each orbit, in ascending `(n,mask)` order. All labels remain
positive and one-based.

An independent deterministic enumeration performed for this plan gave:

| Vertices | Rooted connected isomorphism classes |
|---|---:|
| 2 | 1 |
| 3 | 3 |
| 4 | 11 |
| 5 | 58 |
| Total | 73 |

Every connected graph topology and every inequivalent seed placement through
five vertices is represented. This avoids rerunning the same mathematical
instance under all labeled permutations, while later tests separately check
the implementation's label handling.

Run exactly two parameter cases per rooted representative, giving 146 full
packaged-solver calls:

| Case | alpha | rho, with seed degree d | epsilon | Purpose |
|---|---|---|---|---|
| A | 1/7 | 3/(8d) | 1/10000 | nonsquare alpha and partial final halving |
| B | 1/16 | 1/(16d) | 1/1000000 | exact dyadic momentum boundary and four-stage continuation |

Dense exact optimality checks use exhaustive support enumeration and rational
linear algebra only. The graph has at most five vertices, so at most 32
supports are considered. Cache the exact optimum for repeated comparisons
at a stage parameter, but do not give that cache to the solver.

## 2. Small targeted boundary cases

Add the following cases, deduplicating identical tuples before execution.
They exercise numerical/branch boundaries rather than adding broad Cartesian
parameter products to all 73 graphs.

1. **Momentum change, 12 calls.** Use path(5) endpoint, star(5) leaf,
   complete graph(5), and a triangle with a two-edge pendant tail seeded
   at the tail endpoint. For each, alpha is `63/1024`, `1/16`, or
   `65/1024`; rho is `3/(10*d_seed)` and epsilon `1/1000000`.
   The value just below 1/16 must select theta=1/8, while equality and
   the value just above select theta=1/4.
2. **Exact support contact, 6 calls.** Use the two-vertex path, seed 1,
   alpha in `{1/4,1/7}`. Its second-coordinate activation threshold is
   exactly `rho_contact=(1-alpha)/2`, obtained from the one-coordinate
   KKT equation. Test contact and contact plus/minus `2^-18`, with
   epsilon `2^-60`. Check the true optimum's support exactly; do not infer
   an implementation support error merely from a small omitted coordinate
   unless the certified objective/containment requirements fail.
3. **Zero-solution threshold, 6 calls.** Use a path endpoint and the center
   of star(5), alpha=1/7, rho equal to `(1-2^-20)/d`, `1/d`, and
   `(1+2^-20)/d`, epsilon `2^-60`. At and above the threshold the solver
   must perform no adjacency scan and return the exact zero certificate.
4. **Alpha-one shortcut, 3 calls.** Use path(2) endpoint, star(5) center,
   and star(5) leaf, alpha=1, rho=`3/(7*d_seed)`, epsilon `2^-60`.
   Verify the exact single-coordinate density `1/d_seed-rho` and no
   accelerated stage or adjacency scan.
5. **Label and order invariance, 8 calls.** Choose the first eight n=5
   rooted canonical representatives, reuse parameter case B, and map
   label i to `2^100+37*i`. Reverse every adjacency-row iteration order.
   After inverse relabeling, require exactly the same rational output and
   certificate as the already completed original case. Tree comparison
   operation counts may differ; numerical trajectory results may not.
6. **Access sentinels, 2 calls.** Use a virtual star with `10^6+1` vertices,
   seed at its last leaf, alpha=1/100, rho=1/64, epsilon=1/1000000;
   repeat with `2^100+1` vertices and its last leaf. The center may be
   queried for degree but must not have its adjacency row scanned.
   Verify the explicit seed-only optimum and exact sparse output source,
   with separate verification counters. These are local-oracle tests,
   not dense graph constructions.

The prescribed total is at most 183 full solver calls. Invalid parameter
tests (`alpha<=0`, `alpha>1`, `rho<=0`, `epsilon<=0`, invalid seed) are
separate immediate API checks, not more numerical iterations.

## 3. What every numerical call must verify

Use a fresh strict one-based counting oracle for each solver call. A
separate dense adjacency object belongs only to the exact reference checker.
Record the packaged-source hash before running the fixed manifest.

- Verify unique output labels, exact positive rational densities, correct
  original degree metadata, and a nonnegative returned certificate.
- Independently check `0<=output<=x*_rho`, exact objective gap no larger
  than the returned certificate, certificate no larger than epsilon,
  support volume at most `1/rho`, and total mass at most one.
- Recompute the sparse final source independently. Check nonnegativity,
  upper density `2*alpha*rho`, and its exact mass identity.
- At each observable repaired stage, check monotone baseline coordinates,
  `0<=baseline<=x*_r`, source cap, and exact mass-cap identity. Check the
  next regularization ratio and unchanged degree interpretation.
- Compare the recorded block iterations, grid inequalities, and dyadic
  momentum with the input-derived budgets. Check the scalar-rebase
  adjacency count is exactly zero.
- Reconcile graph accesses against the wrapper and corrector counters,
  including cached adjacency-entry reads if the corresponding metric
  claims them. Do not compare first accesses with repeated-entry metrics.
- Record binding-cap and box-clipping counts, partial final stages, final
  extra accuracy halvings, rebase counts, integer encoding maxima, and
  final mass deficit. A count of zero means that event was not reached;
  it must not be described as covered by ordinary from-zero trajectories.

The stronger mass-deficit work theorem is for exact trajectories. For the
rounded implementation compare measured kinetic volume only against its
proved rounded bound unless its stronger rounded ledger is separately
established. Do not test an unsupported bound merely because empirical
ratios are small.

## 4. Bounded execution and evidence

Produce the complete deterministic case manifest before solver execution.
Run in sorted batches by vertex count and then by boundary category. Save a
checkpoint after every case with exact rational inputs, pass/fail, metrics,
and hashes. Use compact bit summaries instead of printing enormous integer
numerators when only the exact comparison result is needed.

Use the prescribed block schedule itself as each case's numerical iteration
budget. Additionally cap the complete run at 250,000 corrector iterations
and 10,000,000 adjacency entries, with an external per-case time guard.
An exhausted resource guard is reported as an incomplete case, not a
mathematical failure and not a pass. These are test-execution limits, not
claims about measured wall time. Existing exact component tests remain
separate and should not be rerun unless this integration suite reveals a
new failure or the package changes.

Only after the fixed small suite passes should the already prepared virtual
large-family benchmarks be run. Their sparse verifier checks and returned
objective certificates must retain the distinction documented in
`benchmark_virtual_graphs_independent_audit.md`.
