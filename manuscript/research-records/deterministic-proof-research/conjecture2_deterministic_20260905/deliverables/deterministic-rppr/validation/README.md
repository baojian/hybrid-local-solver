# Reproduce the fixed 183-case validation

This directory bundles the exact deterministic case manifest and an independent
integration runner. It needs Python 3.10 or newer, the adjacent
`deterministic_rppr` package, the bundled `tests/test_solver.py` helpers, and the
standard library. No research-directory files, downloaded data, or third-party
runtime dependencies are used.

From the unpacked package directory, run a selected complete suite:

```sh
python3 -I validation/run_full.py --backend fast --output fast-validation.json
python3 -I validation/run_full.py --backend adaptive --output adaptive-validation.json
python3 -I validation/run_full.py --backend mass-grid --output mass-grid-validation.json
```

`fast` is the default backend. `adaptive` is an optional different continuation
schedule; the checks do not require its outputs to equal the fast backend's
outputs. `mass-grid` is an optional mass-weighted grid choice with the fixed
halving schedule; it may also return a different approximation. The same target
objective guarantees are checked independently. No comparison between backends
is required for a successful run.

For a quick installation/import check, use the fixed five-case subset:

```sh
python3 -I validation/run_full.py --backend fast --smoke --output fast-smoke.json
python3 -I validation/run_full.py --backend adaptive --smoke --output adaptive-smoke.json
python3 -I validation/run_full.py --backend mass-grid --smoke --output mass-grid-smoke.json
```

This subset includes an ordinary solve, its large-label/reversed-row counterpart,
the zero branch, the `alpha=1` branch, and an analytic million-leaf star. A smoke
result is explicitly marked `complete_subset`; it does not claim that all 183
cases were rerun. To verify only the bundled manifest and parser:

```sh
python3 -I validation/run_full.py --check-data --output manifest-check.json
```

The manifest's canonical SHA-256 is
`e02485273de4bc1b615530518ac9db60ae5d7beee0140e0e787f6f4320ed0434`.
It is computed with `sha256(json.dumps(data, sort_keys=True).encode())`, matching
the original saved 183-case records. Fraction values are exact strings; JSON
object keys representing vertex labels are restored to integers. The runner
rejects a different manifest.

The runner checks exact optimum KKT conditions, pre-repair and repaired-stage
objective gaps, safe output, source/cap/grid/kinetic guarantees, continuation
rules, strict local discovery and additive oracle accounting, and label/row-order
invariance. For `mass-grid`, the runner additionally checks the weighted error
budget `29*eta*h/theta`, exact baseline representation, exact factory mass hints,
restored horizons at the actual requested tolerance, and additive hint/schedule
ledgers. Observers verify that the hint and final reference-release work makes
no extra graph requests; hint scalar work remains in its separate recorded
ledger. Retargeting counters are subsets of the ordinary accumulated schedule
counters and are not counted twice.

An independent exact subgradient bound is also recorded for each
final output; an inconclusive bound is distinguished from a failed objective
guarantee. Tiny-graph exhaustive calculations belong only to the independent
checker and are never supplied to the local solver. Huge stars use an exact
analytic KKT reference and reject an attempted inactive-hub row scan.

Resource guards are fixed at 250,000 total iterations, 10,000,000 oracle entries,
10,000,000 degree replies, 120 seconds per case, and 1,800 seconds total. On
platforms with `setitimer`, the per-case wall guard is preemptive; otherwise time
is checked cooperatively at guarded steps and oracle operations. Do not use
Python's `-O` option: it disables assertions and is rejected.

The JSON includes complete outputs/stages/candidates, exact comparisons,
structural ledgers, manifest identity, runtime, and source hashes. Completed
records are saved atomically after each case. A full successful suite has
`status: "complete"` and `full_manifest_completed: true`. A failure, interruption,
or reached guard has `status: "incomplete"`, a nonzero exit code, and its completed
records plus available failure observations. `--check-data` reports
`data_verified` and performs no solver run. These checks support reproducibility;
they are separate from the theorem and from comparative timing claims.
