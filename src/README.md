# Source Layout

```text
src/
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

Implementation-neutral utilities and common interfaces may be added directly
under `src/`.

Detailed source-tree rules are in `src/AGENTS.md`.
