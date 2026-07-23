# Agent Instructions

This repository is a research project targeting peer-reviewed publication,
including possible JMLR and ICML submissions.

## Required research context

Before modifying theory, algorithms, solver behavior, or experiments, read:

- `docs/research-context.md`;
- `docs/mathematical-conventions.md`;
- the relevant topic file under `docs/literature/`.

Before changing a residual, normalization, or residual-based stopping rule,
also read `docs/decisions/residual-convention.md`.

Use the literature index to find source papers. Verify theorem statements,
equations, and comparisons against the source PDF and record page or section
pointers in the relevant literature note. Source papers provide evidence, but
the project documentation is authoritative for this repository's conventions.
Whenever papers are added or their publication metadata changes, update
`docs/literature/index.md` and the relevant topic note in the same change.

## Scientific invariants

1. Do not change mathematical definitions without updating documentation and tests.
2. Residual conventions, normalization, and stopping criteria must remain consistent between theory and code.
3. Every experiment must record graph, alpha, epsilon, random seed, stopping rule, and code version.
4. Never manually edit generated figures.

## Source ownership boundaries

Solver implementations are separated by ownership under `src/`:

- `src/hybrid_solver_codex/` is owned by Codex agents.
- `src/hybrid_solver_claude/` is owned by Claude agents.
- `src/baselines/` is shared reference code.

An agent must not modify another agent family's implementation directory.
Cross-implementation comparison must happen through tests, experiments, or stable
interfaces rather than by rewriting the other implementation.

Treat baseline implementations as controlled references. All agents may read,
import, execute, and test them, but should modify them only when the baseline
itself is demonstrably incorrect or an explicitly requested baseline is being
added. Keep such changes narrow, document the reason, and add or update tests.

See `src/AGENTS.md` for the detailed rules that apply within the source tree.

## Required checks

Before finishing code changes:

```bash
make test
make lint
```

Before changing reported experimental results:

```bash
make reproduce
```
