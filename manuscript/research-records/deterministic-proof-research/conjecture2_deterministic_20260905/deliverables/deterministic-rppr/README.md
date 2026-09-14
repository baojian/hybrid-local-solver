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
| `solve`, `solve_fast` | Certified refinements with the fixed halving schedule |
| `solve_combined` | Same numerical trajectory, original tree transitions |
| `solve_binomial` | Tighter block schedule, without early checks |
| `solve_early_stop` | Source-energy schedule with early checks |
| `solve_source_energy` | Source-energy schedule with a fixed endpoint |
| `solve_integer` | Original fixed-schedule integer implementation |
| `solve_reference` | Exact rational reference implementation |
| `solve_adaptive` | Optional source-based stage jumps; same correction and repair |
| `solve_mass_scaled_grid` | Optional mass-scaled grid precision; fixed halving schedule |

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

## Optional adaptive regularization stages

```python
from deterministic_rppr import solve_adaptive

outer = solve_adaptive(graph_oracle, seed, alpha, rho, epsilon)
result = outer.result
print(result.output, result.objective_gap_bound)
print(outer.adaptive_metrics)
print([record.chosen_regularization for record in outer.schedule])
```

This optional wrapper measures the exact source of each repaired baseline
and chooses the next regularization from that maximum. Nonfinal stages
reduce regularization by a factor between two and four; the final stage
clamps to the requested `rho`. It uses the same fast corrector, independent
stopping checks, terminal repair, and output guarantee. Its stage path and
final output can differ from those of `solve_fast`.

The outer result contains the usual `SolverResult` as `outer.result`, plus
`adaptive_metrics` and exact `schedule` records. Convenience properties
also expose `outer.output`, `outer.objective_gap_bound`, and `outer.stages`.
**Total work includes both the inner result's ledgers and the additional
adaptive ledger.** The latter separately counts retained-row scans, cache
lookups, new adjacency/degree replies, source accumulation, maximum
comparisons, and temporary-record reclamation. A cached scan remains paid
work. Newly retained rows may be read to assemble the next source, but
inactive boundary rows are not scanned merely to evaluate their source.

The initial maximum needs only the seed degree; no additional source pass
runs after the final stage. Even a zero-iteration correction still performs
terminal repair. The helper preserves the proved local-work and exact
accuracy bounds, but does not improve elapsed time on every graph. It stays
optional: `solve` and `solve_fast` retain the fixed halving schedule.

The internal `_adaptive.source_maximum` helper can extend a completed
corrector's caches without registering those new vertices in its reporter.
**Do not resume that corrector after calling this terminal helper.** The
public `solve_adaptive` wrapper respects this rule automatically. It does
not expose a manual continuation interface.

Run `python3 examples/adaptive_path.py` for a self-contained example, and
`python3 -m unittest tests.test_adaptive -v` for the focused exact checks.
`ADAPTIVE_TRANSCRIPTION.json` records the six import relocations used to
package this wrapper; the numerical module bodies remain unchanged.

## Optional mass-scaled grid precision

```python
from deterministic_rppr import solve_mass_scaled_grid

outer = solve_mass_scaled_grid(graph_oracle, seed, alpha, rho, epsilon)
result = outer.result
print(result.output, result.objective_gap_bound)
print(outer.mass_hint_metrics)
```

This backend uses the fixed halving regularization schedule and the same
integer correction, stopping checks, and terminal repair. It chooses the
grid using the exact remaining correction mass. A smaller remaining mass
can permit a coarser grid under the proved error bound. **The requested
objective tolerance and final accuracy guarantee are unchanged.** All
initialization horizons are reset for the actual stage tolerance before
any correction step or checkpoint. At zero iterations the certificate is
the initial-energy bound itself.

The outer `MassScaledGridResult` contains the usual `SolverResult` as
`result`, a separate `mass_hint_metrics` ledger, and `mass_hints` records.
Convenience properties expose output, gap bound and stages. Add the hint
ledger to the inner result's work: each hint scans the incoming repaired
baseline and reads its already cached degrees, without additional graph
queries. The exact assembled source independently verifies that mass hint.
Only the immediately preceding corrector is retained for these cached
lookups, and that extra reference is released after use.

Each stage's `mass_scaled_grid` diagnostics distinguish the temporary
initialization tolerance from the actual tolerance and display the
discarded and restored horizons. The ordinary schedule counters already
include both initialization and rescheduling work; displayed rescheduling
subtotals must not be added twice. The grid represents the incoming
baseline exactly, but may discard unused old precision when all retained
fractions allow it.

Grid changes can produce a different numerical trajectory and final sparse
approximation, with the same proved safety and objective-error guarantees.
The backend remains optional; `solve` and `solve_fast` retain their existing
precision rule. No uniform runtime improvement is implied by a coarser grid.

Run `python3 examples/mass_grid_path.py` or
`python3 -m unittest tests.test_mass_grid -v`. `MASS_GRID_TRANSCRIPTION.json`
records the import relocations and explicit corrector-factory call used by
the package. The package does not clone function globals for this adapter.

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
