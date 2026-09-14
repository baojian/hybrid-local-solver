# Supplementary small-mass ABBA comparison

**Grid coarsening occurred, but this four-run measurement did not show a speed
benefit.** On the three-vertex endpoint-seeded path with `alpha=1/4`,
`rho=1/2^20`, and `epsilon=1/2^50`, the prototype used coarser grids in 16 of
20 stages. The final grid was `2^-70` instead of `2^-86`, a factor of 65,536.

The order was **fast, mass-grid, mass-grid, fast**, in the same CPython 3.14.5
process on macOS arm64. Complete process CPU measurements were:

| Backend | First CPU (s) | Second CPU (s) | Median CPU (s) | Median wall (s) |
|---|---:|---:|---:|---:|
| Current fast default | 0.112054 | 0.116814 | 0.114434 | 0.116569 |
| Mass-scaled grid | 0.125655 | 0.119951 | 0.122803 | 0.127336 |

The prototype's median CPU time was 7.31% higher, approximately 8.4 milliseconds.
There are only two short measurements per variant; this is not a statistically
established slowdown or a causal attribution to any particular operation.
Coarser grid denominators alone therefore do not support a performance claim.

Both variants used 20 continuation stages, 176 correction iterations, cumulative
kinetic volume 672, and 1,039 repeated scanned entries. All four final outputs
passed an independent objective-gap certificate outside the timed region.
Repeated runs of each variant agreed in complete exact outputs, ledgers, and
oracle counts. Cross-variant output equality was not assumed.

The full-call timer includes the factory's 20 hint calls and releases, 52 cached
degree lookups/conversions/updates, 19 rational mass hints, relaxed initialization,
retargeting to the actual tolerance, internal stopping checks, and terminal
repair. Retargeting loop counters are already accumulated in the ordinary
schedule ledger and are not added twice. Graph construction, garbage collection
before each call, external certification, and serialization are untimed. The
same fixed guards and instrumentation as the four-fixture benchmark were used;
none was reached.

The stage-grid ratios are `1,1,1,1,2,4,8,...,65536`. The exact final grids and
all intermediate hints, certificates, and timings are preserved in the raw JSON.
No additional cases or repetitions were run after this requested ABBA block.

Artifacts and SHA-256 values:

- `research_mass_scaled_grid_small_mass_abba.json`: full four-run evidence,
  `86c38786153c0c0417ae954621a1a91bbc8b52854ebb2a9f2d6f102c03671fc6`.
- `benchmark_mass_scaled_grid_small_mass_abba.py`: harness,
  `2ce23911a8eccf01cbdfa7080862fcfbcc892c1014da0e55e59130ebe6db2e6d`.
- The prototype source remains
  `3b8cfa4a8f0161101147573007e5ac4cbabb4c64e348ec702f90d977a37d7d8f`.

All recorded source hashes agree before and after these runs. The package,
numerical algorithms, and default were unchanged. This supplemental result is
separate from the preserved sixteen-run four-fixture study, in which no grid
coarsening occurred.
