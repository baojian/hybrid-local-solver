# Exact validation of the standalone deterministic solver

The fixed validation manifest completed successfully: **183 cases and
60,022 correction iterations**. Its source hashes, parameters, repaired
stage checks, exact objective comparisons, and local-query counts are in
`packaged_solver_validation.json`. The reproducible driver is
`validate_packaged_solver.py`.

The suite covers all 73 connected rooted simple graph types on two through
five vertices, with two fixed parameter choices per type. Root-preserving
isomorphism removes redundant relabelings; this is an exhaustive finite
graph enumeration, not random sampling. Additional cases cover either side
of momentum thresholds, exact support-contact parameters and their nearby
rational perturbations, the zero-optimum threshold, `alpha=1`, very large
integer labels, and reversed adjacency order.

For finite small graphs, an independent reference enumerates KKT supports
and solves each candidate system by exact rational Gaussian elimination.
The reference is used only by the checker and is never supplied to the
solver. Every repaired stage is checked for coordinatewise order below the
exact optimum, monotonicity of baselines, its density error, nonnegative
bounded source, mass identity, correction cap, support volume, and the
stated accuracy certificate. First local discovery is enforced by the
oracle; query counts are reconciled with the solver's counters.

Two virtual-star cases, with one million and `2^100` leaves respectively,
use an analytic seed-only optimum. They do not allocate the graph or pass
its size to the solver. Their source and objective comparisons are exact,
and the center's adjacency list is forbidden by the test oracle. Both
passed. These tests demonstrate the expected local behavior on these
instances; the general work guarantee is the mathematical theorem.

The package's shorter self-contained unittest suite also passed, and
`examples/path.py` ran successfully on a path represented implicitly with
one billion vertices. That example returned two sparse records, queried
degrees nine times across continuation stages, and read seven first
adjacency entries. Its objective certificate is `1/1638400`, below the
requested `1/1000000`.

This record concerns the package hashes in the JSON manifest. Subsequent
integer-state or schedule optimizations require their own equivalence or
objective validation; these results do not automatically transfer to an
edited implementation. No randomized algorithm or randomized test was used.

## Additive integer backends

Both newly packaged integer backends subsequently passed the same 183-case
manifest: **366 additional cases, 1,040 repaired stages, and 100,614 total
correction iterations**. The fixed-schedule backend exactly matched the
original package's sparse outputs, certificates, stage counts, and graph
accesses. The source-energy backend passed independent KKT/analytic accuracy
checks with 40,592 iterations, versus 60,022 for the fixed schedule.
Both suites read 2,760 first adjacency entries. Their complete hash-scoped
results are in `packaged_integer_solver_validation.json`.

The independent additive transcription audit found matching class and method
ASTs, verified the explicit corrector-class injection, compared ten full
backend pairs, exercised hash-forbidden labels, and ran all backends in an
isolated Python process without the research modules. After these checks,
the package's default `solve` export was changed to the verified source-energy
backend. This export change does not alter any implementation body.
