# Integer-state dyadic corrector and continuation

This is a separately versioned implementation of the already audited practical
dyadic trajectory. It changes representation and deterministic data structures,
not the mathematical recurrence. No reference module or existing package was
edited. The new public APIs in `integer_dyadic_rppr_solver.py` are
`IntegerDyadicCorrector(...)` and `solve_rppr_integer(oracle, seed, alpha, rho, epsilon)`.
The oracle supplies only `degree(i)` and `neighbors(i)`; no graph-size or global
vertex-list operation is used. Vertex labels are integers and degrees are
positive integers.

## Exact representation and recurrence

Write alpha=A/D, theta=1/T, grid=1/H, sigma=S/H. Here T,H are powers of two.
The maps named X,L,z,M store integer counts for normalized primal position,
approximate primal-neighbor sum, kinetic position, and exact kinetic-neighbor
sum, respectively. To avoid confusion with map names, denote their counts by
m_i,j_i,p_i,w_i. The safe baseline count is B_i, so its density is B_i/H.

The two disjoint trees in `integer_clipped_reporter.py` receive

    b_i = (D-A) T^2 j_i - ((D+A) T^2 - 2D) d_i m_i,
    s_i = 2AH 1(seed=i) - (D+A) d_i B_i + (D-A) sum_neighbor B_j,
    e_i = (D-A) T (d_i p_i + w_i) + T(T+1) s_i,
    G   = 2 D H^2 (T+1).

A base-tree record has raw density S*b_i/(G*d_i)-lambda*T. An exception
record stores the **full** numerator S*b_i+H*e_i and therefore has raw density
(S*b_i+H*e_i)/(G*d_i)-lambda*T; no separate base record remains for this vertex.
Expanding these expressions gives exactly the source-shifted practical raw
recurrence, including when theta^2 differs from alpha. In particular,
`s_i/(2*D*H*d_i)` is the source density.

All old exception records are returned to base form before S changes. The
exact projected density is clipped to [0,4rho] with mass cap

    eta = (H - sum_i d_i B_i)/H = source_mass/alpha.

The reporter emits only projected densities at least 1/H, including equality,
and returns their positive integer grid counts. Its point updates and emitted
floors use integers; exact rational work is confined to scalar waterfill
queries. Its independent component audit checks the translated breakpoint
search, exact ties, disparate weights, and rejected-positive locality.

For an emitted count p_i, the new state is computed by

    S_new = ((T-1) S) // T,
    delta_m_i = (H p_i) // (T S_new),
    m_i += delta_m_i.

This is exactly floor_h(X_i+theta*(p_i/H)/sigma_new), since old X is already
on the grid. A single selected-row pass both scatters the actual delta_m into
j and rebuilds exact w from the new p. When 2*S_new<H, independently replace
m_i and j_i by (S_new*value)//H and set S=H. This scalar rebase inspects no
adjacency. Every exposed base key is refreshed, including obsolete response
records, and the new sparse exceptions are then installed.

The previous scalar-neighbor error proof therefore transfers unchanged:
|L_i-sum_neighbor X_j|/d_i <=4h, the raw error is at most 2h/theta, and the
existing conservative stage perturbation bound is Gamma=29h/theta. The fixed
block schedule stores only a dyadic error-bound denominator, never exact a^k.
Only the last projection multiplier is retained; projection history is not
stored. Kinetic work is accumulated as an integer counter.

## Continuation and deterministic maps

Every solver point map/set, including baseline storage, exception/touched
sets, adjacency/degree caches, and terminal PG accumulation, uses the tested
`AVLMap`/`AVLSet` containers. Balancing uses no random primitive and does not
hash vertex labels. A complete solve with labels whose `__hash__` raises
passes the test suite.

The wrapper uses the same dyadic regularization schedule, dyadic momentum,
grid budget, and target tolerance alpha*delta^2/8 as the practical reference.
After each stage it materializes actual candidate density

    (H B_i + S m_i)/H^2.

The terminal PG pass recomputes the candidate response exactly, scans candidate
rows once, immediately clips newly positive PG neighbors, floors the clipped
point to the same grid, and takes its coordinatewise maximum with the old
baseline. It never uses approximate L for this repair and never reads a
newly positive PG neighbor's adjacency. The existing source, safe-order,
monotone-baseline, and final-gap proofs therefore apply unchanged. The final
certificate is 2*delta^2/rho. Zero solutions and alpha=1 retain their direct
constant-support branches.

Counters report adjacency entries, degree replies, source/exception refreshes,
selected updates, integer floors, scalar-rebase passes, and reporter tree
operations. They are logical structural counts, not a full Python operation
trace. Balanced-map point operations add their deterministic logarithmic
factor. Ordinary runs disable bit-size instrumentation. The optional
`integer_size_snapshot()` explicitly charges a scan of state and reporter
moments and reports the largest stored integer at that instant; it does not
claim to measure temporary products or all arithmetic internals.

## Exact verification

`test_integer_dyadic_rppr_solver.py` passes all seven test groups; results are
saved in `integer_dyadic_rppr_verification.json`.

* Four small deterministic stage fixtures give 260 exact state matches against
  both the practical implementation and an independently coded dense rounded
  recurrence. They include nonsquare rational alpha, an asymmetric cyclic
  graph, nonzero baselines, 44 rebases, and actual nonzero scalar-neighbor/raw
  errors satisfying their bounds.
* The source numerators, raw tree values, selected sets, every X/L/z/M value,
  scales, cap flags, final certificates, and graph work agree exactly. The
  two reporters may order emitted records differently; their selected sets
  and resulting trajectories are identical.
* An injected feasible state binds the exact reduced source-mass cap. This is
  a projection/state test, not a claim that the state is reached from zero.
* Seven complete fixtures cover 13 accelerated stages and 1,452 iterations.
  Every repaired stage equals the reference output and satisfies independent
  dense exhaustive KKT order/source checks. Final exact gaps obey the output
  certificates. Cases include non-dyadic final rho, small nonsquare alpha,
  trees, a triangle, a leaf-seeded star, the zero equality branch, and alpha=1.
* An implicit degree-2^80 hub is exposed by degree only. Its row is never
  scanned, including during scalar rebases. Rebase adjacency work is zero.
  The reporter component separately verifies positive sub-grid rejection and
  closed-tail ties, including a large rejected-record set.
* Ten integer-state steps, including rebases, run with this module's Fraction
  constructor disabled. The reporter retains its explicitly permitted scalar
  exact-rational root work. A complete hash-forbidden-label solve also passes.
* An optimum-baseline fixture verifies that terminal maximum repair actually
  preserves two coordinates that the downward shift would otherwise lower.

The largest stored integer seen by the explicit test snapshots was 81 bits,
including the degree-2^80 input. This is a fixture-specific stored-size
measurement, not a uniform bit bound or a trace of intermediate products.

An initial test fixture used a zero baseline with rho below the required
source-interface range; construction correctly rejected it. The fixture was
changed to an admissible rho. No implementation correction was required by
these tests.

## Bounded timing comparison

`benchmark_integer_dyadic_rppr.py` compares the already streamlined exact
Fraction adapter against the integer implementation in ABBA order. The input
is an implicit path with 10^9 vertices, endpoint seed 0, alpha=1/100, rho=1/16,
epsilon=1/1,000,000. The benchmark never traverses this input globally.

| Measurement | Streamlined Fraction | Integer state | Improvement |
|---|---:|---:|---:|
| Median process CPU seconds | 4.8380 | 1.4222 | 3.40x |
| Median wall seconds | 6.3225 | 1.7998 | 3.51x |

All four runs produce exactly the same outputs, nonimplementation stage
summaries, and graph work: four stages, 2,016 iterations, 11,755 corrector
adjacency-entry reads, 22 terminal PG reads, 19 degree replies, 24 first-read
adjacency entries, and six output records. The exact certificate is
1/1,280,000. Full records are in `integer_dyadic_rppr_benchmark.json`.

Timing clocks alone use floating values; all algorithmic arithmetic,
comparisons, and decisions are exact. No optional dependency was added.
These are bounded fixture measurements, not an asymptotic speed theorem or
an extrapolation to other graph families. The host may run concurrent work,
so process CPU is the cleaner comparison.
