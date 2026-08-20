# response_preconditioned_hybrid

This standalone note defines a common active-set interface for the project's
iterative and persistent-response solver lines. It does not claim that a mixed
method is universally optimal. Instead, it proves the generic block-response,
boundary-interval, geometric-rebuild, and probe-before-rebuild lemmas and
states a conditional
composition theorem whose two endpoints are the local iterative product scale
and an output-sensitive incremental SDD/Schur solver.

The proposed method stores a response representation for a settled anchor,
uses a frontier buffer for newly admitted vertices, performs aggregate
preconditioned repair, and materializes the old-face correction only at final
output. The unresolved graph-uniform ingredient is certified finite-band
boundary reporting on nonequitable cyclic cores; no uncharged boundary scan or
future-support oracle is hidden in the interface.

The exact diagnostic backend is
`src/hybrid_solver_codex/response_hybrid.py`, with the reproducible comparison
driver `experiments/explore_response_hybrid.py`. It separates adjacency scans,
global boundary reads, dense response arithmetic, Schur construction,
frontier iterations, materialization, and output writes. It is a correctness
and switching oracle, not an output-sensitive implementation.

Build from this directory with:

```bash
make
```
