# Fast exact adapter: equivalence and measured improvement

`fast_exact_dyadic_rppr.py` provides `solve_rppr_fast` and
`FastPracticalDyadicCorrector`. It removes diagnostic measurement overhead
from the verified practical dyadic implementation while retaining exact
standard-library Fraction arithmetic. No optional dependency was installed,
and no floating-point decision or randomized operation was introduced.

On a bounded local-path comparison, the adapter reduced median process CPU
time from 10.864 seconds to 5.689 seconds, a factor of 1.91. Exact outputs,
certificates, stage data, structural counts, and graph-access counts were
identical. These measured results are detailed below.

The verified reference files and the separately generated AVL-backed package
were not edited. This adapter currently targets the Python point-map
reference; its pre-existing point-map complexity limitations remain visible.

## 1. Profile of the smaller representative case

The profiled input was an implicit path on `10^9` vertices, with endpoint
seed, alpha `1/100`, rho `1/16`, and epsilon `1/1000000`. The input oracle
enumerates no global vertex list. The solve performs four continuation
stages, 2,016 rounded correction iterations, and 11,755 corrector adjacency
entry inspections.

The reference cProfile run recorded 49,967,342 calls and 64.903 profiled
seconds. `ArithmeticTracker.measure` was called 2,491,750 times, accounting
for 34.265 cumulative seconds. Diagnostic conversion, wrapper construction,
bit-length collection, and repeated comparison products were substantial
costs. Cumulative profile times overlap; they must not be added together.

The saved `fast_exact_profile_summary.json` gives the top profile entries;
`fast_exact_reference_profile.prof` retains the raw profile. Profiled time
is not used as a timing comparison against an unprofiled run.

## 2. Minimal exact substitution

`LeanRational` carries the same exact Fraction value as `Tracked`, but:

* arithmetic directly operates on exact operand values;
* comparisons delegate to Fraction instead of collecting bit diagnostics
  and separately forming another pair of products;
* already wrapped values need not be wrapped again; and
* no measured numerator/denominator maxima are updated.

`UnmeasuredExactArithmetic` retains the numerical interface expected by the
existing corrector. A property setter injects it at the parent's first
tracker assignment, before raw keys, tree moments, or numerical states are
created. Thus a running tree does not mix observers or require a rebuild.

The original projection tree, exact mass threshold, closed-tail selection,
grid floor, actual-X increment, scalar rebase, source-mass cap, fixed-block
schedule, exact PG scan, and monotone repair code remain in use.

The continuation wrapper reuses the reference function's exact code object
with an isolated globals mapping that substitutes only the corrector class.
It does not mutate the reference module's globals. Concurrent reference
calls therefore continue to use the diagnostic implementation. This avoids
copying and potentially diverging from the verified schedule/repair code.

Unavailable arithmetic diagnostics are returned as `None`, with an explicit
measurement-mode label. They are not reported as zero-bit arithmetic.
Structural counters remain enabled and unchanged.

## 3. Exact equivalence checks

All four groups in `test_fast_exact_dyadic_rppr.py` passed:

* 49 pairs of exact arithmetic values, including negative values, ties,
  large numerators/denominators, and the cancellation example highlighted
  in the earlier internal-size audit.
* Four reporter pairs covering threshold ties, sub-grid entries, a binding
  cap, unequal weights, and a degree-`2^80` record.
* Three stage pairs and 268 exact step-by-step comparisons of X, L, z, M,
  sigma, raw keys, history entries, certificates, all structural counters,
  and degree/adjacency query order.
* Six full continuation pairs with identical final outputs, exact
  certificates, stage data, repair counts, and graph queries, including zero
  and alpha-one branches. The reference module's class binding is verified
  unchanged after every fast solve.

Because every arithmetic value and comparison agrees, induction through the
shared code preserves the bounded dyadic trajectory and AVL behavior. The
previous convergence, locality, and coefficient-size proofs apply to this
same trajectory; the disabled observer does not supply an algorithmic input.

Results are saved in `fast_exact_dyadic_verification.json`.

## 4. Unprofiled ABBA timing

`benchmark_fast_exact_dyadic.py` ran the same smaller path input in the order
reference, fast, fast, reference. It uses wall/process clocks only for
diagnostics; solver inputs and computations remain exact Fractions. Every
run's complete output and structural stage data were compared exactly.

| Mode | Wall times (seconds) | Process CPU times (seconds) |
|---|---|---|
| Reference | 40.273, 44.056 | 10.888, 10.840 |
| Fast exact | 23.784, 21.786 | 5.779, 5.598 |

Median wall time improves from 42.165 to 22.785 seconds (1.85 times).
Median process CPU time improves from 10.864 to 5.689 seconds (1.91 times).
The host was contended, as the wall/CPU difference shows; process CPU time
is the cleaner comparison here. This is a bounded measurement on the
specified fixture, not a universal performance claim or a extrapolation to
the root's larger rho-`1/128` case.

Every run has four stages, 2,016 iterations, 11,755 corrector entry reads,
22 PG entry reads, 19 degree replies, 24 first adjacency entries, and six
output records. The exact final certificate is `1/1280000`.

The complete timing data are saved in `fast_exact_dyadic_benchmark.json`.
`gmpy2` was not installed in the inspected runtime. The concrete improvement
was obtained without adding it or starting a native dependency project.

## 5. Scope

This is the completed diagnostic-free exact adapter. It is intentionally
kept stable while a separate integer-state implementation is investigated.
Removing measurement does not remove rational arithmetic itself; the
remaining Fraction and wrapper overhead is a distinct optimization target.
The reference diagnostic mode remains available when actual reduced-size
measurements are needed.
