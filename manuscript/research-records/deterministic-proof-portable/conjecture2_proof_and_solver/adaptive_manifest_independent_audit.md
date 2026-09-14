# Independent exact adaptive integration validation

**Result: all 183 fixed manifest cases passed.** The new adaptive continuation was the only complete solver executed. No package, existing test, corrector, reporter, or implementation source was modified. The saved before/after source hashes agree. This validation supplements the mathematical proof; it is not a timing comparison or a claim of universal practical improvement.

## Coverage and independent checks

The validator uses exactly `validate_packaged_solver.make_manifest()`: 146 rooted connected topology/parameter cases on two through five vertices, 12 momentum-threshold cases, six near-contact cases, six zero-threshold cases, three `alpha=1` cases, eight large-label/reversed-row cases, and two analytic huge stars. It reuses only the independent exhaustive KKT optimum, objective, and source helpers from `tests.test_solver`, not its fixed-halving validation assumptions.

For every one of the **344 completed stages**, the new validator checked:

- The exact source over the entire tiny graph (or all analytically distinct star classes), its maximum and returned maximizing vertex, the rule `r=max(rho,M/(4*alpha))`, the quarter lower bound, nonfinal half upper bound, and final target-clamp semantics.
- The full pre-repair candidate against an independent exact optimum: its actual original-objective gap is nonnegative and at most the reported current-state certificate. Every repaired output is monotone above the preceding baseline, below the exact optimum, within the proved density error, and has the proved objective gap and nonnegative source bound.
- The exact source-mass cap, `eta>=r`, `eta<=4*eta_*(r)`, baseline/source cardinality charges, nested default grids, `Gamma<=alpha^2*r*eta`, and the stronger cumulative kinetic bound `360*eta*K/r`.
- Cached-checkpoint aggregate volume and geometric-prefix accounting, no cache misses, exact terminal candidate scan accounting, and all source-pass temporary-record reclamation. A read-only follow-up on saved records checked all 7,404 checker containers were reclaimed, all 28,336 counted checker records were reclaimed, and all 3,032 scalar rebases respected their frequency bound without adjacency scans.

All **183 final outputs** satisfy the original additive objective target, are below the exact optimum, and have the correct sparse output degrees, mass, and source. In addition, all 183 pass a separately calculated exact original-objective subgradient certificate. The eight relabeled/reversed-row cases match their unrenamed adaptive cases in final output, every repaired stage, regularization, certificate, grid, and iteration count. No equality with any fixed-schedule solver output was assumed or tested.

The analytic star cases have respectively `10^6` and `2^100` leaves. Each made four seed-row requests and inspected four actual oracle entries, with nine degree replies. Neither hub row was queried. The exact seed-only KKT calculation accounts for the unvisited other leaves; it is not a finite enumeration of these stars.

## Local access and additive ledger

An independent strict oracle rejects degree or row access before local discovery and records actual degree replies, row requests, entries, phases, and vertices. A transparent wrapper around the exact source helper also checks its actual oracle deltas against its separate metrics. A guard subclass observes only the returned current stage candidate and counts steps; it does not change any numerical operation.

The recorded totals are:

| Quantity | Count |
|---|---:|
| Complete solver cases | 183 |
| Completed stages | 344 |
| Correction iterations | 9,770 |
| Actual graph-oracle adjacency entries | 2,524 |
| Actual graph-oracle degree replies | 1,616 |
| Corrector scanned entries, including cached reads | 71,008 |
| Terminal PG scanned entries | 2,524 |
| Checkpoint cached entries | 9,559 |
| Additional adaptive-source scanned entries | 1,234 |
| Additional adaptive-source passes | 168 |

The last source passes are additive to the inner solver ledger. In this manifest they use cached rows/degrees and make no additional oracle replies, but their 1,234 entry inspections and scalar/map operations remain charged. There were 1,234 checkpoints: 312 accepted and 922 rejected. The cumulative kinetic volume was 69,774. All 71 nondyadic stage regularizations passed the exact checks.

## Supplemental boundary-source fixture and limits

No post-initial source maximum in the 183 runs occurred strictly outside a nonempty baseline. To exercise that omitted situation, a separate helper-only validator uses the three-vertex path seeded at its center, `alpha=1/3`, old regularization `7/64`, and the certified safe baseline density `7/32` at the center. Its exact optimum is `(11/192,43/192,11/192)`, and its source densities are `(7/96,1/48,7/96)`. Thus the maximum is strictly on the boundary, and the next proposed regularization is `7/128`.

Two helper calls pass: the fresh call reads only the center row (two entries and three degrees); the cached call makes no oracle request while charging its two cached entries. Each reclaims all four temporary records. This supplement does not add a solver case or rerun a backend.

Seven manifest cases used direct branches. **No manifest stage had zero iterations**, so this integration result does not claim additional empirical zero-iteration coverage. The mathematical and separately existing zero-stage results are not inferred from these records. No resource guard was reached. The guards were fixed in advance: 250,000 total iterations, 10,000,000 oracle entries and degree replies each, 120 seconds per case, and 1,800 seconds total. Atomic snapshots preserved completed records after each case and would have preserved partial observations on failure.

## Reproducibility

- `validate_adaptive_manifest_independent.py`: complete independent validator.
- `adaptive_manifest_independent_validation.json`: full fixed manifest, exact outputs, every stage and pre-repair candidate, exact optimum/source comparisons, adaptive schedules and ledgers, strict oracle records, runtime information, and before/after provenance.
- `adaptive_manifest_independent_validation_summary.json`: compact counts and exact maximum diagnostic ratios.
- `adaptive_manifest_saved_ledger_checks.json`: read-only additional accounting checks; no solver reruns.
- `validate_adaptive_boundary_source_independent.py` and `adaptive_boundary_source_independent_validation.json`: separate two-call helper supplement.

Runtime was Python 3.14.5 on macOS arm64. The complete suite took approximately 31 seconds on that host; this is a validation-run observation, not a paired solver benchmark.

Key SHA-256 values:

| File | SHA-256 |
|---|---|
| `adaptive_source_continuation_rppr.py` | `af33cb41872eb834aeabb14f5ec5cc1a45cda7400482884da5576e0358c633ea` |
| `validate_adaptive_manifest_independent.py` | `c5a24953d88fa3c3b40996f6d7f0869c98e7428735af7ebf380b322c6a8cde9b` |
| `adaptive_manifest_independent_validation.json` | `0dc9847ef11a93b0ba3759d10ec45987e0ea570ee9050a625705b797737390d6` |
| `validate_adaptive_boundary_source_independent.py` | `c6b66e158b805301d74f1302d1f31aa520d7538fcf86bd5140aef6c90ee9a544` |
| `adaptive_boundary_source_independent_validation.json` | `0050b25de48cf17fb8d86eae4def70915a00407ad9d572142ab6bcdcbbe58d70` |

No implementation defect was found. All complete adaptive solver cases were run once; subsequent work only inspected saved records and ran the bounded source-helper supplement.
