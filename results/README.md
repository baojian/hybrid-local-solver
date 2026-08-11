# Results

Experiment programs write machine-readable result bundles here. Transient runs
belong under `results/raw/`, which is intentionally ignored by Git. A result is
committed only when it supports a documented theorem check, manuscript figure,
table, or other reported claim.

New result bundles use the validator in `experiments/result_schema.py`. They
record the schema version, experiment configuration, command-line arguments,
Git commit and dirty-worktree status, and per-run graph, parameters, stopping
rule, work, metrics, and status. A stored `epsilon` is not a project-wide
accuracy guarantee: its `epsilon_name` and exact `stopping_rule` must identify
the certificate used by that solver. Dirty-worktree status is `true` or
`false`, and is `null` rather than falsely reported as clean when Git status is
unavailable. Completed runs must have nonnegative edge work and nonempty
metrics; the schema also distinguishes completed-but-uncertified runs from
completed certified runs.

Figures are generated from structured records by scripts under `experiments/`.
Never edit a generated figure manually.
