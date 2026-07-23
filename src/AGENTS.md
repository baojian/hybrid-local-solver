# Source Tree Instructions

These rules apply to every file under `src/`.

## Directory responsibilities

### `hybrid_solver_codex/`

- Codex agents may implement and maintain code here.
- Claude agents may read, run, benchmark, and review this code, but must not
  modify it.

### `hybrid_solver_claude/`

- Claude agents may implement and maintain code here.
- Codex agents may read, run, benchmark, and review this code, but must not
  modify it.

### `baselines/`

- This is shared reference code used for scientific comparisons.
- All agents may read, import, execute, test, and benchmark it.
- Do not tune a baseline merely to favor one hybrid implementation.
- Modify existing baseline behavior only to correct a verified defect or when
  the user explicitly requests the change.
- Keep necessary changes minimal and record the reason in the commit or pull
  request.
- Any behavioral baseline change requires focused tests and a check that
  experiment comparability is preserved.
- New baselines may be added one at a time without changing unrelated baseline
  implementations.

### Shared source utilities

Common protocols, data structures, and utility modules may live directly under
`src/`. Keep them implementation-neutral: shared code must not silently favor,
merge, or rewrite either agent-owned solver.

## Cross-boundary work

- Never copy changes into the other agent family's directory.
- Prefer shared, documented interfaces over shared mutable implementation code.
- A review may report defects in another implementation, but the owning agent
  family must make the corresponding source change.
- Tests may compare all implementations and baselines without taking ownership
  of their internal code.
