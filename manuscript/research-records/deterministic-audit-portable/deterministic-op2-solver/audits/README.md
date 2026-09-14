# Reproducing the extended audits

The solver and the seventeen tests in `tests/` require only Python's standard
library. The extended audits here additionally use NetworkX and require
Python 3.11 or later compatible with that dependency. They were run
with Python 3.13.13 and NetworkX 3.6.1. Install that optional dependency in an
isolated environment before running these scripts.

From the package root, useful short checks are:

```sh
python audits/independent_projection_sector_audit.py
python audits/forest_spectral_audit.py
python audits/component_integer_audit.py
python audits/explicit_output_audit.py
python audits/tiny_obstacle_audit.py
python audits/rounding_perturbation_audit.py
```

The independent two-energy and work-bound audit takes an explicit output:

```sh
python audits/independent_continuation_audit.py --output results/reproduced-continuation.json
```

Each remaining `*_audit.py` has a deterministic, finite default campaign and
can be run directly. Some full rational continuation comparisons take
substantially longer than the short tests. Their full-graph optima and dense
linear algebra belong exclusively to the external audit; the local solver
never receives those objects.

Most scripts write their named output into `results/`, replacing an existing
file with the same name. Copy the included result snapshots first if you want
to retain both the original measurement and a new run. The snapshots record
checks performed during development; benchmark times reflect the named
implementation at that point. Current defaults include the integer component
loop, so a new run may take a different time. Exact trajectory comparisons
were repeated after that change and after its inactive-cap shortcut.
Accelerated trajectory comparisons and the boundary-forest benchmark disable
the optional tiny exact solver to retain their intended coverage. Its separate
audit checks 3,699 obstacle cases and eight complete extreme-alpha paths.

The virtual graph benchmarks describe huge graphs through formulas. They do
not allocate or enumerate the ambient vertex sets. Their exact checks cover
the omitted vertices through symbolic KKT row classes. The intentionally
stopped checkpoint-only alpha=1e-12 run has a stop record and no claimed
completed result; the later bounded-pilot run completed that parameter.

`VERIFICATION.md` maps the completed campaigns to their scopes. The report in
`report/` gives the mathematical argument. Neither finite enumeration nor
benchmark performance replaces that proof.
