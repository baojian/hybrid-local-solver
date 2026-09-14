# Portable benchmark harness: independent audit

The bounded audit passed. No implementation defect was found for the documented fixed fixtures on the audited macOS runtime. The portable timer limitation below should be stated when describing the resource guard.

Audited driver: `deliverables/deterministic-rppr/benchmarks/run.py`, SHA256 `15471b15fdb60bc2cf75296396f86ee3abb7aaf899276d2beb2bb7b02d0ccac7`. Reproducible checker: `audit_portable_benchmark.py`. Evidence: `portable_benchmark_independent_verification.json` and full smoke/guard JSON and logs in `portable_benchmark_audit/`. The 20 library modules and final wheel were hash-checked before and after and remain unchanged.

## Graph and oracle checks

All vertices and ordered adjacency rows were checked for 62 deterministic small fixtures: paths of size 2 through 32, square grids of side 2 through 12, and tree-clique graphs of depth 2 through 5 with each clique size from the number of leaves through four more. These cover 2,096 vertices and 12,780 directed adjacency entries.

Every degree and complete ordered row equals the earlier `benchmark_practical_rppr.VirtualGraph` definition. Independent checks verify valid labels, no loops or duplicate neighbors, edge symmetry, degree/row-length equality, exact family edge counts, and connectivity. Invalid endpoint labels were rejected in 248 checks. The portable helper restricts tree depth to at least 2, whereas the earlier broader helper also allowed depth 1; this does not alter any portable manifest fixture.

Separate checks exercise the degree limit, the adjacency-entry limit with a partially consumed row, and an expired oracle deadline. Graph-state metering uses AVL sets. Internal graph-degree evaluations used to generate a row do not pretend to be additional solver degree replies.

## Smoke and isolation checks

Only the three-vertex `smoke` case was solved. Two ABBA blocks used `fast, adaptive, adaptive, fast` and `fast, mass-grid, mass-grid, fast`: eight completed solver calls total. There was no run of the four larger benchmarks.

The runner was copied beside only the 20 package modules. A subprocess launched with `-I -S -B` from `/` allowed absolute imports only from the standard library and `deterministic_rppr`; all 20 package origins had to belong to this isolated copy. No research implementation was available through the import path or permitted by the import guard.

For each completed output, this audit independently solved the full three-vertex linear optimality equations using rational elimination, verified that the optimum was strictly positive, and recomputed the exact objective gap and minimum subgradient norm. The returned gap and separately recomputed certificate both bound the actual gap and meet the requested tolerance. The certificate's upward squared-norm rounding and its degree/adjacency counters also reconcile. Repeated calls to each backend reproduce the complete exact result and oracle metrics, excluding timing fields.

The fast smoke calls use 32 iterations over 4 stages; adaptive uses 28 over 3; mass-grid uses 32 over 4. These are functional smoke observations, not evidence of a runtime improvement or asymptotic claim. Raw CPU and wall samples remain in the test JSON without a speed comparison.

## Timing and work accounting

The timed interval includes the complete solver call, its deterministic oracle-metering updates, internal checkpoint certificates, optional source scheduling or mass hints, and returned output construction. Graph setup, garbage collection before the interval, result serialization, and the separate final certificate lie outside it. CPU and wall clocks are measured separately. Repetition equality compares exact result and structural work, not the inherently varying timing values.

`inspect_result` reconciles external degree replies and adjacency entries with stage setup, terminal repair, initial degree, and optional adaptive-source metrics. Its cumulative scan total includes stage scans, repair scans, internal checkpoint cached adjacency visits, and additional adaptive source scans. The complete exact JSON retains optional mass-hint scalar/cache counts separately, so they are not misreported as new external graph queries. Checkpoint cache misses and container reclamation are checked, and every stage's kinetic-volume bound is asserted. The independent final certificate uses a new oracle with separate counts.

A conservative external certificate that exceeds the target is recorded as inconclusive rather than being converted into a false failure or accuracy claim. The harness records that boolean in each row and summary. All eight smoke certificates met the target.

## Forced failure and scope

The final smoke command used `--oracle-limit 1`. It exited with return code 1 and `RuntimeError: Benchmark degree-reply guard reached`. The output was valid atomic JSON with `status="incomplete"`, `complete=false`, the active case/backend, and no completed runs or summaries. No temporary `.tmp` file remained. Interrupted calls do not acquire fabricated successful timing rows; partial failed-call counters are not presented as completed measurements.

On platforms providing `signal.setitimer`, the context applies an asynchronous wall guard during the solver and final-certificate calls. When that facility is absent, its fallback relies on `CountingOracle` deadline checks at graph callbacks. Thus the fallback is not a hard wall limit for a long scalar-only phase. The exact degree and entry limits still apply. This portability qualification does not affect the audited macOS execution, and does not require changing any numerical library or wheel.
