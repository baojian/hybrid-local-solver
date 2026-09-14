# Deterministic local regularized PageRank

This package implements the bounded dyadic version of the deterministic
algorithm accompanying `deterministic_conjecture2.tex`. It queries a graph
through a seed, vertex degrees, and adjacency lists. It does not need the
graph size or a supplied support set.

The mathematical result is a deterministic local-work bound
`O~(1 / (rho * sqrt(alpha)))` in the nontrivial regime
`0 < rho < 1/degree(seed)`, in the supplied exact-real word model, with
polylogarithmic parameter and accuracy factors. The returned sparse vector
is coordinatewise below the regularized PageRank optimum and has additive
objective error at most the requested `epsilon`.

The implementation uses exact rational scalar arithmetic and explicit
downward dyadic rounding. All graph-state maps and sets use deterministic
AVL trees. No randomized algorithm, randomized balancing, or expected-time
hash-table assumption is used by the solver. Python's arbitrary-precision
integer costs are additional to the original word-model theorem.

In that regime, the actual default rounded implementation has the stronger bound
`O~(eta_star / (rho * sqrt(alpha)))`, where
`eta_star = 1 - sum_i sqrt(degree_i) * x_star[i]` is the optimum's mass
deficit. The algorithm never queries this unknown quantity. Its returned
mass deficit estimates it within a factor of `1+alpha`; the existing grids
already suffice for this refinement. The ratio `eta_star/rho` lies between
the optimum's support volume and the smaller of `1/rho` and the whole
graph's volume. These are proved bounds, separate from timing measurements.

The default `solve` function uses integer grid counts, a source-dependent
initial-energy bound, a tighter certified block schedule, and independent
local stopping checks. Those checks use only already cached rows, and
their unsuccessful attempts are counted. A direct replacement of persistent
tree records reduces updates without changing the numerical trajectory.

The comparison backends remain available:

| Function | Behavior |
|---|---|
| `solve`, `solve_fast` | All audited refinements |
| `solve_combined` | Same numerical trajectory, original tree transitions |
| `solve_binomial` | Tighter block schedule, without early checks |
| `solve_early_stop` | Source-energy schedule with early checks |
| `solve_source_energy` | Source-energy schedule with a fixed endpoint |
| `solve_integer` | Original fixed-schedule integer implementation |
| `solve_reference` | Exact rational reference implementation |

## Run the example

Python 3.10 or newer is required. The solver has no runtime dependencies.
From this directory, run:

```sh
python3 examples/path.py
python3 -m unittest discover -s tests -v
```

Alternatively install this directory with `python3 -m pip install .`.

## Minimal use

```python
from fractions import Fraction
from deterministic_rppr import solve

class Path:
    def degree(self, vertex):
        return 1 if vertex in (0, 999) else 2

    def neighbors(self, vertex):
        if vertex > 0:
            yield vertex - 1
        if vertex < 999:
            yield vertex + 1

result = solve(
    Path(), seed=0,
    alpha=Fraction(1, 5),
    rho=Fraction(1, 8),
    epsilon=Fraction(1, 1_000_000),
)

for vertex, density, degree in result.output:
    print(vertex, density, degree)
print("Certified objective gap:", result.objective_gap_bound)
```

The oracle represents a finite connected simple unweighted undirected
graph, with positive integer degrees and integer vertex labels. It must
return exactly `degree(vertex)` distinct neighbors, with symmetric
adjacency. The solver assumes these graph properties; verifying them
globally would defeat local access. Rows are consumed only when the
algorithm needs them. An oracle may generate rows lazily and may represent
a graph much larger than memory.

Supply rational parameters as `Fraction`, integers, or decimal strings.
The parameters must satisfy `0 < alpha <= 1`, `rho > 0`, and `epsilon > 0`.
A Python float is interpreted as its exact binary rational value. Using
`Fraction(1, 10)` expresses one tenth exactly.

## Returned values and guarantee

Each output record is `(vertex, density, degree)`, where
`density = x[vertex] / sqrt(degree)`. The exact mathematical coordinate is
therefore `density * sqrt(degree)`. Keeping this representation avoids
numerically approximating the square root. The PageRank mass represented
by that record is `degree * density`.

For the graph's normalized Laplacian `L`, seed `v`, and degree matrix `D`,
the objective is

```text
Q = alpha I + (1-alpha) L / 2
b = alpha D^(-1/2) e_v
F_rho(x) = x^T Q x / 2 - b^T x + alpha rho ||D^(1/2)x||_1
```

`result.objective_gap_bound` is the proved additive upper bound on
`F_rho(result) - min F_rho`. It is not a difference obtained by computing
the unknown optimum. The theorem also gives `0 <= result <= x*_rho`,
support volume at most `1/rho`, and total mass at most one. If
`rho * degree(seed) >= 1`, the exact optimum is zero. The case `alpha=1`
is returned directly after the seed-degree query.

`result.stages` records regularization values, target and certified stage
errors, grid sizes, repaired sparse baselines, and structural work counts.
`result.metrics` records continuation and terminal-repair work. The
`checkpoints` entry in each stage's corrector metrics separately counts
cached checks, failed certificates, temporary records, and reclamation. Cached
adjacency scans and first oracle reads are separate quantities; both are
charged in the proof. Diagnostic counters describe logical operations,
not Python instructions or a measured CPU-time complexity theorem.

## Independent optional certificate

```python
from deterministic_rppr import certify_output

check = certify_output(graph_oracle, seed, alpha, rho, result.output)
print(check.objective_gap_bound)
print(check.meets(epsilon))
```

This verifier recomputes a local subgradient from the supplied sparse output
and uses strong convexity to bound its objective gap. It does not inspect
the solver's stages or use its reported certificate. It scans the output
support once and queries its immediate neighbors' degrees; newly encountered
zero-output neighbors have no adjacency scan. These verification costs are
reported separately and are additional to solving.

The independent bound is conservative. `False` from `meets(epsilon)` means
that this separate bound is inconclusive; it does not refute a tighter
solver certificate. `True` certifies the requested accuracy directly. The
verifier accepts the common-denominator density representation returned by
this package and checks the recorded degrees against the oracle.

## Optional exact seed-only check

```python
from deterministic_rppr import solve_with_singleton

trial = solve_with_singleton(graph_oracle, seed, alpha, rho, epsilon)
print(trial.outcome, trial.objective_gap_bound)
print(trial.output)
```

This helper checks whether the exact optimum is supported only on the seed.
It scans the seed row and queries neighboring degrees, without reading any
neighbor's row. Equality in its exact KKT test is accepted. The default
degree cutoff is 32; `seed_degree_cutoff=0` disables the row trial.

The returned `SingletonPrecheckResult` exposes `output`,
`objective_gap_bound`, `outcome`, `trial_metrics`, and `fallback_result`.
On success the gap is exactly zero. On a failed or skipped trial, it invokes
the normal fast solver, and `fallback_result` is that untouched result.
Total work includes both ledgers; repeated fallback reads are counted again.
The outcome is one of `zero`, `alpha_one`, `singleton`, `failed_trial`, or
`skipped_cutoff`. The trial uses constant auxiliary records and at most
one seed row, preserving both proved local work bounds. Its exact successful
density can be a general rational and is accepted by `certify_output`.

Run `python3 examples/star.py` for an exact answer on an implicit
billion-leaf star using two degree replies and one adjacency entry.
The precheck is optional; `solve` itself directly runs the general algorithm.

## Verification

The standalone tests independently enumerate KKT supports on small graphs,
solve each candidate system by exact rational elimination, and compare
the solver's output and repaired stages with the exact optimum. They also
check the source inequalities, mass and support-volume bounds, and the
local discovery order. The dense reference is never passed to the solver.

An independent transcription audit additionally compared the packaged
implementation against the original verified prototype, including integer
labels whose `__hash__` raises an exception. `TRANSCRIPTION.json` records
the source hashes and deterministic container substitutions used to build
this package. Larger external validation and benchmark records are stored
alongside the accompanying proof; they are not required to run the solver.

The optional verifier passed exact arbitrary-output tests and an independent
audit. It also certified all eleven saved integer benchmark outputs below
their requested objective tolerances, including the large virtual graphs,
without rerunning the solver or computing their unknown optima.

The original two integer backends also passed 183 exact integration cases each,
including 520 repaired stages per backend. The source-dependent schedule
used 40,592 correction steps across that suite, compared with 60,022 for
the fixed schedule. Its endpoints can differ while satisfying the same
accuracy guarantee. `INTEGER_TRANSCRIPTION.json` records their source hashes
and the explicit continuation-class injection used by the package.

The final combined and fast backends each passed the same 183-case manifest,
including all 520 repaired stages and 1,508 checkpoints. Both used 12,068
correction steps; fast preserved combined's exact outputs, stage lengths,
graph-access counts, and checkpoint decisions. All 183 outputs independently
certified at their requested accuracy. Separate transcription audits checked
the package without access to its research source files, including very large
integer labels whose hash operation raises an exception.

`ACCELERATED_TRANSCRIPTION.json` and `DIRECT_TRANSCRIPTION.json` record the
audited schedule/checkpoint and direct-transition snapshots. Earlier
transcription files are historical records of their respective package
snapshots; their old initializer hashes need not match the final exports.
`PACKAGE_MANIFEST.json` records every current solver module and the final
default selection. The exported verifier's explicit container factories allow
checkpoint metering without changing its residual arithmetic.

This is a research implementation with conservative certified tolerances.
The exact arithmetic and rich stage records favor reproducibility; runtime
depends on the exposed graph and the requested parameters.
