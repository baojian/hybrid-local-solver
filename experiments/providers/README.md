# Provider-owned experiments

Implementation-specific experiment drivers live under a directory matching
their provider id in `src/solver_providers.toml`. Shared sweeps and result
schemas stay one level above and consume neutral interfaces.

Only the owning agent family edits its provider directory. Comparisons between
providers belong in shared orchestration or tests and record each provider id
explicitly.
