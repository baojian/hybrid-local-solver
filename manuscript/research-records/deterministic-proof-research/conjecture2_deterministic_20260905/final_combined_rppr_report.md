# Final bounded practical study of the combined deterministic solver

All 14 fixed fixtures completed, and every output passed a separately recomputed exact subgradient-norm certificate at the requested `epsilon=10^-8`. The saved data contain 21 samples: 19 fresh solves plus two reused completed hub runs. No fresh resource guard triggered. All recorded source hashes remained unchanged throughout the study.

The combined backend uses the audited integer state, source-energy initialization, tighter binomial block bound, and independent cached early-stop checkpoints. These measurements support practical execution on the tested instances; they do not establish runtime asymptotics or replace the mathematical work proof.

## Manifest, reproducibility, and timing scope

`final_combined_rppr_manifest.json` fixes the eight prior local/harder fixtures and six alpha-sweep cases before measurements. `study_final_combined_rppr.py` is the driver; `final_combined_rppr_study.json` retains every exact output, stage and continuation record, checkpoint and reporter metrics, independent certificate, oracle counts, and implementation hashes. The tree–clique fixture is one shared clique attached to the binary-tree leaves, as in the independently audited virtual oracle.

Fresh runs used Python 3.12.14 on macOS 26.5.2 arm64. CPU is process time; wall is elapsed time. The timed region includes the solve, counting oracle, checkpoint materialization/metering/checking/discard, and terminal repair. It excludes imports, graph construction, result serialization, hashing, and the separate final-output verifier. There was one timed solve at a time and no overlapping benchmark job.

Each fresh solve had a 120-second wall guard and a one-million-entry limit on actual oracle-supplied adjacency entries. Repeated cached accesses were counted and subject to the wall guard, rather than a separate entry stop. Each independent verification had a separate 30-second wall guard and one-million-entry oracle limit. The completed reused hub samples were not rerun under the fresh solve guards; both were independently recertified under the verification guards.

To reproduce from this directory using the frozen source snapshots:

```sh
/Users/baojian/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 prepare_final_combined_hub_reuse.py
/Users/baojian/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 study_final_combined_rppr.py --reuse-hub-record final_combined_hub_reused_records.json
```

The commands assume this research directory is the working directory. Omit the reuse option to perform a fresh hub solve as well. The reuse normalizer validates all prior source hashes and preserves both source-record indices and runtime provenance.

## Large local fixtures

“Reads” includes all corrector, terminal-PG, and checkpoint cached adjacency visits. “Checkpoint” is the subset spent in independent stopping checks. These values differ from newly supplied oracle entries, which are separately recorded. Times are single samples except the grid comparison and the reused hub pair, for which the table uses medians.

| Fixture | Iterations | CPU / wall (s) | Reads | Checkpoint | Output records / volume | Distinct degree records |
|---|---:|---:|---:|---:|---:|---:|
| star-billion * | 112 | 0.032 / 0.032 | 118 | 7 | 1 / 1 | 2 |
| star-huge-labels | 112 | 0.028 / 0.029 | 118 | 7 | 1 / 1 | 2 |
| path-local | 896 | 1.211 / 1.221 | 15,190 | 379 | 16 / 31 | 17 |
| cycle-local | 912 | 2.498 / 2.511 | 28,970 | 560 | 25 / 50 | 27 |
| grid-local | 104 | 0.463 / 0.464 | 6,452 | 776 | 29 / 116 | 49 |
| cube-local | 64 | 0.196 / 0.199 | 1,660 | 240 | 1 / 20 | 21 |
| tree-clique-boundary | 448 | 3.765 / 3.810 | 32,244 | 1,912 | 63 / 156 | 95 |
| path-alpha-1e3 | 4,096 | 17.420 / 17.587 | 188,695 | 1,768 | 55 / 109 | 56 |

* The `star-billion` samples are reused from `combined_certified_dyadic_study.json`, which used Python **3.14.5**. Their full data and independent recertification are retained. The other rows use Python 3.12.14; do not compare these stars' raw timings as an isolated label-size effect.

The path and cycle have one billion vertices, the grid has 100 million, the cube has `2^20`, and the huge-label star has `2^100+1`. The normal path/cycle use alpha=1/100 and rho=1/128; grid/cube use alpha=1/16 and rho=1/256; both stars use alpha=1/100 and rho=1/64. The harder path uses alpha=1/1000 and rho=1/512. Complete parameters are in the manifest.

The hard path queried 56 distinct degree records, scanned 55 distinct rows, and returned 55 records despite its billion-vertex universe. The tree–clique case queried 95 distinct degree records and scanned only the 63 tree rows. Its maximum queried degree was 16,384 and maximum scanned degree was 3. Both stars queried their hub degree but scanned only degree-one leaf rows. These are concrete locality observations on these fixtures, not claims that every graph behaves similarly.

## Fixed-rho alpha sweep

The sweep uses a 4,096-vertex endpoint-seeded path, `rho=1/256`, and `epsilon=10^-8`. The alpha=1/64 row reports its matched-comparison median; the others are single samples. No fitted rate or asymptotic conclusion is inferred.

| alpha | Iterations | CPU / wall (s) | Reads | Checkpoint reads | Output volume |
|---|---:|---:|---:|---:|---:|
| 1/4 | 64 | 0.053 / 0.054 | 566 | 123 | 9 |
| 1/16 | 176 | 0.194 / 0.198 | 2,303 | 258 | 19 |
| 1/64 | 496 | 0.777 / 0.780 | 9,963 | 486 | 33 |
| 1/256 | 1,120 | 3.028 / 3.080 | 35,380 | 781 | 55 |
| 1/1024 | 3,776 | 12.746 / 12.903 | 142,488 | 1,251 | 87 |
| 1/4096 | 8,896 | 41.931 / 42.368 | 443,339 | 1,707 | 133 |

## Matched comparisons with fixed source-energy scheduling

Only two selected manifest cases were rerun under both backends, in fixed/combined/combined/fixed order. Repeats matched exactly within each backend, including complete stage/continuation metrics. Different backends can return different valid approximations. The comparison includes every combined checkpoint cost and uses the same Python runtime, oracle, parameters, and timing scope.

| Fixture | Fixed / combined iterations | Fixed / combined reads | Fixed CPU / wall (s) | Combined CPU / wall (s) |
|---|---:|---:|---:|---:|
| grid-local | 492 / 104 | 23,548 / 6,452 | 1.900 / 1.919 | 0.463 / 0.464 |
| path-sweep-alpha-1over64 | 1,416 / 496 | 22,733 / 9,963 | 1.881 / 1.905 | 0.777 / 0.780 |

Measured median CPU ratios were 4.10 on the grid and 2.42 on the path. Two samples per backend are a bounded practical comparison, not a statistically broad speedup claim. Prior historical timings from other runs/runtimes are not used in these ratios.

## Independent accuracy and scalar-work provenance

Every completed output was passed to `independent_sparse_certificate.py` through a new verification oracle. This reconstructs a valid subgradient for the original nonnegative obstacle objective and uses strong convexity to certify its gap, rounding the integer squared-norm sum upward. All 21 certificates meet the requested epsilon. This is independent objective-gap evidence, stronger than the earlier source-interval-only checks. It does not independently establish containment below the exact optimum; that property relies on the audited repair proof and its finite KKT tests.

The outputs, returned theorem bounds, independent rational norm bounds, rounding-excess bounds, positive output volume/mass checks, and every verification oracle reply are saved separately. No whole graph was built for any verification. Verification CPU/wall times are not included in the solver table.

Adjacency totals alone do not describe all computation. The JSON also retains source and exception refreshes, integer floors, scalar rebases, reporter point updates/search visits, checkpoint AVL lookups/writes/iterations, materialized and discarded words, and reclaimed checker records. For example, the hard path adds 1,768 checkpoint adjacency visits, 22,727 checkpoint scalar point requests, and 5,531 reclaimed checker records. The alpha=1/4096 sweep adds 1,707, 21,882, and 5,318 respectively. These logical counters carry the existing AVL logarithmic factors; they are not a literal trace of every machine instruction or a peak-memory measurement.

The saved source hashes matched at the end of the run. All arithmetic affecting outputs and certificates was exact integer/Fraction arithmetic; only timing and display formatting used floating-point values. No random graph generation, probes, pivots, or balancing rules were used.
