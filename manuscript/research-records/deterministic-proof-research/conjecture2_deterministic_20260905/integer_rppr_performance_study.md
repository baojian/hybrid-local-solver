# Independent integer-backend performance study

The integer backend completed all eleven deterministic fixtures, including the eight larger/local cases. Three fresh comparisons with the original instrumented Fraction practical solver matched the exact output, objective certificate, all non-diagnostic stage fields, continuation metrics, and six structural graph-work fields. The six previously recorded large/local fixtures also matched their historical exact outputs and local counts. No mathematical or asymptotic claim is inferred from these timings.

## Method and reproduction

The reproducible driver is `study_integer_rppr_performance.py`; the full results and source SHA-256 hashes are in `integer_rppr_performance_study.json`. Run it with the workspace Python, for example:

```sh
/Users/baojian/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 study_integer_rppr_performance.py --phase all --seconds-per-case 120 --entry-limit 1000000
```

Run from this research directory. It executes one timed solve at a time, with alternating backend order for the three paired comparisons. CPU time is `time.process_time`; wall time is `time.perf_counter`. Both include the counting oracle but exclude imports, graph setup, independent verification, and JSON serialization. Each number is one sample. All runs completed under the per-case limits; none is a timeout or partial result. The host was macOS 26.5.2 arm64, Python 3.12.14. No random graph, pivot, balancing rule, or probe was used.

The Fraction reference here is the original **instrumented** implementation, which measures reduced rational sizes and uses Python point maps. The integer solver uses AVL point state. Consequently these paired timings measure those complete implementations, including their unequal diagnostic costs; they are not a clean isolated arithmetic speedup. The separately coordinated ABBA study against the uninstrumented fast Fraction implementation addresses that narrower comparison. Historical large-case timings are not used to compute speedup.

## Fresh exact comparisons

| Fixture | Vertices | Fraction CPU / wall (s) | Integer CPU / wall (s) | Iterations | Counted adjacency reads |
|---|---:|---:|---:|---:|---:|
| path-small | 5 | 0.323 / 0.323 | 0.051 / 0.051 | 160 | 499 |
| barbell-small | 6 | 1.343 / 1.348 | 0.175 / 0.175 | 384 | 2,484 |
| barbell-mid-study | 16 | 4.778 / 4.831 | 0.714 / 0.718 | 608 | 18,069 |

The three pairs used respectively `(alpha,rho,epsilon)=(1/4,1/16,10^-6)`, `(1/8,1/32,10^-6)`, and `(1/16,1/128,10^-6)`. The latter two graphs are two cliques joined by one bridge, with clique sizes 3 and 8. All comparison signatures agree exactly. The measured CPU ratios were 6.30, 7.68, and 6.69, subject to the instrumented-reference caveat above.

## Larger implicit graphs

All eight runs below used `epsilon=10^-8`. “Counted reads” includes repeated accesses to cached adjacency entries in corrector updates and terminal projected-gradient repairs. “Oracle entries” counts actual entries supplied by the virtual oracle, including repeat exposure across continuation stages. It is not the same quantity. The solver's scalar-only rebases made zero adjacency scans in every run.

| Fixture | alpha | rho | CPU / wall (s) | Iterations | Counted reads | Oracle entries | Output records / volume |
|---|---:|---:|---:|---:|---:|---:|---:|
| star-billion | 1/100 | 1/64 | 0.572 / 0.578 | 3,296 | 3,295 | 6 | 1 / 1 |
| star-huge-labels | 1/100 | 1/64 | 0.627 / 0.637 | 3,296 | 3,295 | 6 | 1 / 1 |
| path-local | 1/100 | 1/128 | 4.942 / 4.995 | 3,904 | 59,255 | 99 | 16 / 31 |
| cycle-local | 1/100 | 1/128 | 7.529 / 7.691 | 3,456 | 81,746 | 136 | 25 / 50 |
| grid-local | 1/16 | 1/256 | 2.786 / 2.800 | 736 | 34,572 | 232 | 29 / 116 |
| cube-local | 1/16 | 1/256 | 1.496 / 1.530 | 548 | 11,100 | 80 | 1 / 20 |
| tree-clique-boundary | 1/64 | 1/512 | 20.838 / 21.279 | 2,288 | 159,382 | 486 | 63 / 156 |
| path-alpha-1e3 | 1/1000 | 1/512 | 56.038 / 56.686 | 13,248 | 579,369 | 365 | 55 / 109 |

The path and cycle have one billion vertices. The grid has 100 million vertices; the cube has dimension 20 and 1,048,576 vertices. The stars have `10^9+1` and `2^100+1` vertices, with a leaf seed. Both stars queried the hub degree but scanned only degree-one leaf rows; each exposed only two distinct degree records. Thus the huge-label run also checks that the numerical solver does not enumerate the label range.

The harder path (`alpha=1/1000`) queried only 56 distinct vertex degrees and scanned 55 distinct vertex rows despite its 13,248 iterations. Its emitted support has volume 109 and 55 records. This is a concrete local-work result for this instance, not a worst-case bound or a statement that iteration overhead is negligible.

The tree–clique fixture is a depth-5 binary tree (63 vertices) whose 32 leaves attach to distinct ports of **one shared clique** of size 16,384. It is not the earlier family with private chambers per leaf. It queried 95 distinct degree records and scanned only the 63 tree vertices. The maximum degree queried was 16,384; the maximum degree scanned was 3. This demonstrates degree-only boundary rejection on that fixture; it does not benchmark processing an active large clique.

## Exact-check and certificate provenance

For the five-vertex path and six-vertex barbell, the verifier independently enumerates candidate active sets, solves the dense rational KKT systems, checks containment of the emitted vector below the exact optimum, and compares its exact objective gap with the returned certificate. These checks passed.

For the 16-vertex barbell and all larger graphs, the independent sparse verifier reconstructs the source `b-Q*output`, checks its nonnegativity and upper bound, checks the source-mass identity, and validates positive entries, degree values, mass, support volume, and `0 <= returned_bound <= epsilon`. These checks **do not independently prove objective accuracy or support containment**. Their objective certificates retain the provenance of the solver's fixed-block schedule, perturbed-energy theorem, and exact projected-gradient/grid-repair theorem. The known sparse-source-check counterexample documented in `benchmark_virtual_graphs_independent_audit.md` is why this distinction is necessary. Exact agreement with another implementation is additional transcription evidence, not an independent replacement for that theorem.

The large returned bounds were `1/327680000` (both stars), `1/163840000` (path/cycle), `1/134217728` (grid/cube), `1/268435456` (tree–clique), and `1/1024000000` (harder path), each below the requested `10^-8`. All graph exposure used by verification is recorded separately and was excluded from the solver timing and locality totals. Large-case verification never constructed the full graph.

The driver and JSON record exact fractions and structural counts rather than floating-point acceptance tests. This study did not instrument every internal integer multiplication or memory access, measure peak memory, or validate a machine-word implementation. It establishes reproducible execution and exact agreement on these fixtures; the separate arithmetic and charged-work proofs establish the claimed general model bounds.
