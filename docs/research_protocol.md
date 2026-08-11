# Research Protocol

## Experiment metadata

Every experiment should record:

- graph dataset;
- teleportation parameter alpha;
- target accuracy epsilon;
- random seed;
- stopping criterion;
- solver parameters;
- git commit hash;
- whether the working tree contained uncommitted changes.

Machine-readable runs should use `experiments/result_schema.py`. Every record
must name its accuracy parameter (for example, `eps_appr`) and store the exact
implemented stopping rule. Recording a numeric field called `epsilon` does not
make certificates from different solvers comparable. Until an explicit
conversion is adopted in `docs/decisions/residual-convention.md`, mixed-
certificate rankings must be labeled exploratory.

When a queue-empty or frontier-empty implementation is intended to realize a
residual certificate, record both the actual termination rule and a post-run
check of the intended certificate. Do not include uncertified runs in
equal-certificate rankings. If a reported error uses a separately computed
reference solution, record its solver, tolerance, norm, and coordinate
conversion.

## Complexity accounting

Report:

- number of outer acceleration iterations;
- local inner iterations;
- edge operations;
- dependence on alpha and epsilon.

## Paper generation

Figures should be generated automatically from experiment outputs.
