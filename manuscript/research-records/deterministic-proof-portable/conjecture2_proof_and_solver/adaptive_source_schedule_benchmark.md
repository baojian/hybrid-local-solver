# Paired comparison of source-adaptive continuation

The adaptive rule reduced the stage count on all four fixtures, and reduced
measured CPU time on three. It increased CPU time on the grid. The fixed
schedule therefore remains the package default; adaptation is an optional
proved alternative.

Each fixture used the order fixed, adaptive, adaptive, fixed in one Python
3.14.5 process. Both variants used the same integer correction, direct
exception replacement, and terminal repair. Their regularization schedules
and resulting trajectories differ. The table gives medians of the two
runs per variant. These are sixteen runs on four fixtures, not sixteen
different graph instances.

| Fixture | Stages, fixed/adaptive | Iterations, fixed/adaptive | CPU seconds, fixed/adaptive | Fixed/adaptive CPU ratio |
|---|---:|---:|---:|---:|
| Endpoint path | 4 / 3 | 400 / 288 | 0.267 / 0.227 | 1.18 |
| Interior grid | 6 / 4 | 104 / 96 | 0.394 / 0.478 | 0.82 |
| Tree with clique boundary | 8 / 5 | 448 / 344 | 2.940 / 2.329 | 1.26 |
| Path, `alpha=1/1000` | 6 / 4 | 2560 / 2304 | 3.930 / 3.548 | 1.11 |

The endpoint path uses `alpha=1/100`, `rho=1/16`, and `epsilon=1e-6`.
The grid uses `alpha=1/16`, `rho=1/256`, and `epsilon=1e-8`. The
tree/clique fixture uses `alpha=1/64`, `rho=1/512`, and `epsilon=1e-8`.
The harder path uses `alpha=1/1000`, `rho=1/64`, and `epsilon=1e-8`.
All input values were exact rational numbers. Full graph parameters and
runtime provenance are stored in `adaptive_source_schedule_benchmark.json`.

Every returned vector passed a separate local subgradient objective
certificate at its requested tolerance. The two repetitions of each
variant had exactly identical output, stage records, adaptive records, and
graph accesses. No equality between the different variants' trajectories
is asserted.

The timed region includes counting-oracle overhead, internal stopping
checks, every adaptive source pass, and disposal of its temporary maps.
Final independent verification and serialization occur after timing.
All actual oracle replies reconcile exactly with the continuation, repair,
corrector, and extra adaptive ledgers. The additional source passes used
cached rows on these complete runs, and those rereads remain charged.

| Fixture | Charged repeated entries, fixed/adaptive | Extra adaptive source entries |
|---|---:|---:|
| Endpoint path | 3526 / 2959 | 14 |
| Interior grid | 6452 / 7808 | 108 |
| Tree with clique boundary | 32244 / 25762 | 222 |
| Path, `alpha=1/1000` | 55312 / 50666 | 55 |

The grid illustrates why fewer iterations do not by themselves imply less
work: its changed intermediate trajectory scans more degree-weighted
support. The work theorem charges those actual scans. The reported ratios
describe this small paired study; they are not a graph-uniform runtime
improvement claim, and are not multiplied by ratios from other studies.

The driver is `benchmark_adaptive_source_schedule.py`. The saved report
contains the eight numerical-module hashes, complete results for all runs,
independent certificates, integer oracle counters, timing medians, and a
clarification that floating point is used for clocks and displayed aggregate
statistics while solver and certificate arithmetic remains exact.
