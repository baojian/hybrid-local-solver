# Source Layout

```text
src/
├── graphs.py              # Pinned Hugging Face access and shared GraphData
├── synthetic_graphs.py    # Shared star, path, and spider constructions
├── baselines/             # Shared, controlled reference implementations
├── hybrid_solver_codex/   # Solver implementation owned by Codex agents
└── hybrid_solver_claude/  # Solver implementation owned by Claude agents
```

The Codex and Claude implementations are intentionally isolated. Agents may
inspect and compare the other implementation, but only the owning agent family
may modify it.

Baseline code is shared for reproducible comparisons. It should remain stable:
agents may use it freely, but existing behavior should change only for a
verified correction or an explicit user request.

Implementation-neutral graph access lives directly under `src/`. Baseline
scripts consume the same `GraphData` interface as the hybrid implementations.
For these symmetric loop-free graphs, `GraphData.m` is the undirected edge
count `adjacency.nnz // 2`; reproducible experiment sources are selected with
`GraphData.sample_sources(...)`.

Detailed source-tree rules are in `src/AGENTS.md`.
