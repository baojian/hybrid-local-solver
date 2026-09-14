# Deterministic local regularized PageRank

This is the portable reference implementation accompanying the OP2 proof
audit for the `hybrid-local-solver` project. It uses deterministic local
graph access, exact rational comparisons, bounded dyadic state, and ordered
trees. There is no randomized linear solver, sampling step, or randomized
retry. Python 3.10 or later is required; runtime dependencies are entirely
from the standard library.

The proved work bound in the manuscript's exact-real word model is
`O_tilde(1 / (rho * sqrt(alpha)))`, with polylogarithmic dependence on inverse
objective accuracy. The paper charges repeated graph inspections, state and
response work, certificate checks, materialization, and output. The code also
provides a bounded-rational implementation of those steps.

## Run without installing

From this directory:

```sh
python -m unittest discover -s tests -v
python examples/virtual_path.py
python examples/small_extreme_alpha.py
```

The package can also be installed with `python -m pip install .`.

The research bundle includes the proof report in `report/`, independent
mathematical notes in `notes/`, and reproducible extended checks in `audits/`.
See `audits/README.md` for the optional audit dependency and result snapshots.
`PROOF_TO_CODE.md` maps each proof obligation to the corresponding routines
and their work charges.
Historical notes retain research-workspace paths; the included reproducible
programs are under `audits/` in this bundle.

## Basic use

```python
from fractions import Fraction as F
from pruned_rppr import solve_fast

class PathOracle:
    def __init__(self, length):
        self.length = length

    def degree(self, vertex):
        return 1 if vertex in (0, self.length - 1) else 2

    def neighbors(self, vertex):
        if vertex > 0:
            yield vertex - 1
        if vertex + 1 < self.length:
            yield vertex + 1

answer = solve_fast(
    PathOracle(10**12), seed=0,
    alpha=F(1, 10000), rho=F(1, 64), epsilon=F(1, 10**12),
)
print(answer.route, answer.objective_gap_bound)
for vertex, density, original_degree in answer.output:
    print(vertex, density, original_degree)
```

The example describes a graph through local queries; it does not allocate a
trillion vertices. The solver never asks for the ambient graph size or a
global list of vertices.

## Mathematical convention and output

Use the manuscript's normalization:

`Q = alpha I + (1-alpha)/2 * (I - D^(-1/2) A D^(-1/2))`,
`b = alpha D^(-1/2) e_seed`, and
`F_rho(x) = x^T Q x/2 - b^T x + alpha*rho*||D^(1/2)x||_1`.

`epsilon` is an additive **objective-gap** target. It is separate from a
semantic PPR coordinate tolerance.

Each output triple is `(vertex, density, original_degree)`, where
`x_vertex = sqrt(original_degree) * density`. This is an exact sparse
representation. The corresponding PageRank mass is
`original_degree * density`. Regularized masses can sum to less than one.

For ordinary rational coordinates, call `solve_explicit` with the same
arguments. Its `coordinates` field contains `(vertex, x_value)` pairs, and
its `objective_gap_bound` includes the conversion error. It uses only
arithmetic and comparisons to bound square roots from below, takes no
additional graph queries, and preserves the OP2 bound and safe order.
The underlying density answer is available as `density_result` and conversion
work counters as `conversion`.

For a valid oracle and parameters, the returned vector satisfies
`0 <= x_hat <= x_rho_star`, objective gap at most
`answer.objective_gap_bound <= epsilon`, and original support degree-volume
at most `1/rho`. The bound is a certified upper bound; the solver does not
compute an unknown dense optimum to evaluate the actual gap.

Pass `Fraction`, integer, or rational-string parameters to preserve the
intended exact values. A supplied Python float is converted to its exact
binary rational value.

## Oracle contract

- The graph is finite, connected, simple, undirected, and unweighted, with
  positive original degrees and integer vertex labels.
- `degree(vertex)` returns that positive integer degree.
- `neighbors(vertex)` yields the complete original adjacency list, once per
  neighbor, in a deterministic order consistent with the graph.
- The oracle is stable throughout a solve. Degree normalization always uses
  the original graph, including edges that leave an inspected region.

The implementation checks positive degrees and row lengths as they are
encountered. Global symmetry and simplicity are properties of the input
contract; checking them by enumerating the graph would defeat local access.

## Solver routes and options

`solve_fast` is the recommended entry point. It first handles exact zero and
diagonal cases and a certified loose-accuracy zero answer. It then inspects
a seed region under original scan budget `1/rho`.

If discovery completes with at most sixteen vertices, exact monotone
active-set elimination returns the optimum directly. The fixed size limit
is enforced, so this is a charged constant-size shortcut. Larger completed
components use a deterministic boundary-forest spectral bound. If discovery
is incomplete, it makes one
bounded restricted-region attempt and accepts only a certificate for the
full problem. A rejected attempt falls back to diffuse-source continuation.
Geometric projected-gradient checks may finish a stage before its prescribed
horizon. Newly positive PG rows are never opened just to evaluate a check.

Optional switches are available for comparison and reproducibility:

```python
solve_fast(..., early_certificate=False)  # use prescribed horizons
solve_fast(..., bounded_pilot=False)      # go straight to continuation if incomplete
solve_fast(..., integer_component=False)  # rational component reference trajectory
solve_fast(..., tiny_exact=False)         # accelerate even completed tiny components
```

A partial-region answer always requires a final global certificate, including
when geometric early checks are disabled.

Advanced entry points are `solve_integer` and `solve_with_source_energy`.
They run continuation directly and accept `early_certificate=True` as an
option. The exported `solve` preserves the slower rational continuation
reference. Its trajectory is useful for exact comparisons.

## Work counters

`answer.metrics` reports prepass, region, certificate, and arithmetic-state
counters. If continuation ran, its stages and additional counters are in
`answer.continuation`. A continuation stage's `certified_point` explicitly
identifies whether its gap certificate concerns the candidate or the PG
point used for terminal clipping.

Counters describe individual work categories; they are not a complete Python
instruction trace or a bit-operation profiler. In particular, iteration
count alone is not the local-work measure. The proof document explains the
complete accounting and common-denominator arithmetic.

## Provenance and verification

The core continuation proof and its original solver were developed in the
parallel project task **Prove conjecture 2 deterministically**. This task
independently audited that argument, copied and attributed the implementation,
and added the fixed degree pruning, boundary-forest component solver, global
PG checkpoints, bounded region pilot, integer component transcription,
certified rational-coordinate output, and the size-limited exact component solve.
`pruned_rppr/PROVENANCE.json` records hashes of the copied sources. The original
repository and parallel-task files were not edited.

The accompanying report, `VERIFICATION.md`, and exact-check results distinguish
mathematical proof, finite tests, and structured performance measurements.
This package addresses OP2 for the unit-graph convention above. The separate
nested-SDD reuse conjecture OP3 and weighted-graph extensions are not claimed.
