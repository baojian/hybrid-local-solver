# Mass-scaled-grid ABBA comparison on the four existing fixtures

**No grid coarsening occurred on these four fixtures.** The mass-grid prototype
and current packaged fast default used identical grids, iterations, cumulative
kinetic volume, and scanned-entry counts. Their exact outputs and every repaired
stage also agree. The small mixed timing differences below therefore do not
demonstrate a benefit from coarser arithmetic.

Each fixture used one paired **fast, mass-grid, mass-grid, fast** block in the
same Python process: two measurements per variant and sixteen complete calls.
The table gives median process CPU time; positive change means the prototype
was slower in this small measurement.

| Fixture | Fast CPU (s) | Mass-grid CPU (s) | CPU change | Iterations each | Repeated scanned entries each |
|---|---:|---:|---:|---:|---:|
| Standard path | 0.2840 | 0.3071 | +8.15% | 400 | 3,526 |
| Local grid | 0.4142 | 0.3981 | −3.89% | 104 | 6,452 |
| Tree–clique boundary | 3.0209 | 3.0813 | +2.00% | 448 | 32,244 |
| Hard-alpha path | 4.1632 | 4.1165 | −1.12% | 2,560 | 55,312 |

All sixteen outputs passed an independent sparse original-objective certificate
computed **outside** the timed region. Repeated runs of each variant agreed in
their complete exact results, stage diagnostics, extra ledgers, and oracle
counters. This is a bounded two-sample-per-variant comparison, not a confidence
interval or a broad performance conclusion. The raw CPU and wall times are
preserved; no measurement from another runtime/study was used in these ratios.

The fixtures and exact parameters are the four `CASES` in
`benchmark_adaptive_source_schedule.py`: the billion-vertex endpoint path, the
100-million-vertex interior grid, the depth-five tree attached to a 16,384-vertex
clique, and the billion-vertex path at `alpha=1/1000`. They are generated through
local virtual-graph oracles, not materialized globally. The canonical fixture
hash is `7fa0a1338a3fc590c72581de4bdc3f9f8710ea55bc4cc36ba6aef393e92a6f55`.

Timing covers the entire solver call, including counting-oracle overhead,
internal checkpoints, the mass-hint factory, both relaxed and restored schedule
setup, terminal repair, and factory reference release. The extra prototype
scalar work is preserved in `mass_hint_metrics`: the per-run cached degree
lookups are respectively 7, 29, 121, and 29 on the four fixtures, and the factory
calls/releases are 4, 6, 8, and 6. These costs are included in the timer. The
retargeting diagnostic subsets are already in the ordinary accumulated schedule
counters and must not be added twice. Actual oracle counts equal the ordinary
solver ledgers; the hint factory introduces no extra graph request.

Graph/oracle construction, `gc.collect()` before each call, independent final
certification, post-run checking, and JSON serialization are untimed. Garbage
collection remained enabled during every call. Fixed guards were one million
oracle entries per solve/check, sixty wall seconds per solve/check, 100,000
iterations per solve, and 600 seconds for the study. No guard was reached.

Runtime: CPython 3.14.5, `/opt/homebrew/opt/python@3.14/bin/python3.14`, macOS
26.5.2 arm64. The default alias was explicitly checked to be `solve_fast`.
Numerical modules, package exports, and defaults were not changed; all source
hashes agree before and after the study.

Artifacts and key SHA-256 values:

- `research_mass_scaled_grid_abba_benchmark.json`: complete raw sixteen-run
  evidence, exact results, certificates, extra ledgers, runtime, and all source
  hashes; `39f9865565b2f971697e83daf9395740880817b4b69e0daecea3d0fc6f52ea0c`.
- `benchmark_mass_scaled_grid_abba.py`: benchmark harness;
  `0c079afa5bc677384c75bb56ef3ef9d9c9049f8eb818cb591fe1e26bfee9e867`.
- Prototype source: `3b8cfa4a8f0161101147573007e5ac4cbabb4c64e348ec702f90d977a37d7d8f`.
- Packaged `_fast.py`: `c4f90de062a2b7e15109a8309b7191ee09987457f113da12196b1795b8a1a8fc`.
- Packaged `__init__.py`: `e60fc8213508e8d561938bfb03fb981594243095818ee3d11b7457516d18fe1e`.

The separately requested three-vertex small-mass comparison has its own raw
evidence and report. It is not merged into these four-fixture timings.
