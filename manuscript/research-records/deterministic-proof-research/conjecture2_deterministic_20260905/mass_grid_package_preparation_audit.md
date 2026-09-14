# Optional mass-grid package preparation and focused checks

The separately audited `mass_scaled_grid_rppr.py` has been transcribed into
`deliverables/deterministic-rppr/deterministic_rppr/_mass_grid.py`. The
optional backend is exported as `solve_mass_scaled_grid`; the additional
named types are `MassScaledGridCorrector`, `MassScaledGridResult`,
`MassHintMetrics`, and `MassHintRecord`. `solve` remains the identical
`solve_fast` function. No existing numerical module, package metadata,
finalizer, or wheel was changed.

## Auditable transformation

`build_mass_grid_solver_package.py` requires the passing independent source
audit at the exact source hash before writing its package module. It makes
three import relocations:

- `combined_certified_dyadic_rppr` -> `._combined`;
- `direct_exception_integer_rppr` -> `._direct`, removing only the research
  `_continuation` import;
- `deterministic_rppr_solver` -> `._types`.

It adds `from . import _integer as reference` and replaces the one call

`_continuation(factory)(oracle, seed, alpha, rho, epsilon)`

with

`reference.solve_rppr_integer(oracle, seed, alpha, rho, epsilon, corrector_class=factory)`.

The builder independently reverses exactly these transformations and checks
whole-module AST equality before writing. No constructor, hint logic,
rescheduling code, metric, result field, or control-flow change is made.
There is no `FunctionType` cloning in the packaged adapter. Its explicit
factory call uses the already audited package continuation injection.

`MASS_GRID_TRANSCRIPTION.json` records the transformations, source audit,
and every preexisting module's hash. At this snapshot:

- Source SHA-256:
  `3b8cfa4a8f0161101147573007e5ac4cbabb4c64e348ec702f90d977a37d7d8f`.
- Package SHA-256:
  `94485eadc2fbbd1b2a9026e58e6c0bd19b792c3271130a12392463bd11da9402`.
- Initializer SHA-256 after the named optional exports:
  `e60fc8213508e8d561938bfb03fb981594243095818ee3d11b7457516d18fe1e`.

All 18 preexisting non-initializer module files still match their snapshots,
including the optional singleton and adaptive wrappers.

## Focused public checks

The self-contained `tests/test_mass_grid.py` passes four groups through the
public package API. It covers complete fixed-continuation KKT validation,
the additional cached mass-hint ledger, actual tolerance restoration, a
grid 32 times coarser than the ordinary grid, zero-step certification,
inherited step/run/rebase method identity, and hash-forbidden large labels
beside a degree-`10^30` inactive hub. The hub's row is forbidden and never
read. Complete outputs also pass the independent sparse certificate.

Command, from the package root:

```
python3 -B -m unittest tests.test_mass_grid -v
```

`examples/mass_grid_path.py` also passes. It reports all six stage grids
and remaining masses, the ten additional hint records/cache lookups, and
the full external oracle counts separately. Its final independent bound
is `399620505518043989/77371252455336267181195264`, below the requested
`1/1000000`. This is an example execution, not a timing study.

The exact source hashes, commands and example output are retained in
`mass_grid_package_verification.json`. That artifact's scope is the
builder's transformation check, unchanged hashes, focused public tests and
example. The independent source/package equivalence and package-only
isolation audit is assigned separately and will be recorded in
`mass_grid_package_independent_verification.json`; these distinct checks
must not be conflated.

## User contract and finalization boundary

The README documents the new optional export, the unchanged requested
tolerance/accuracy guarantee, and the unchanged fixed halving schedule.
It explains `outer.result`, the additive `outer.mass_hint_metrics`, and
`outer.mass_hints`, with convenience output/gap/stage properties. It also
states that ordinary schedule counters already include the relaxed setup
and retargeting work; their displayed subtotals are not an extra charge.
Exact incoming baseline representation is promised, without claiming
strictly nested grid denominators or uniform runtime improvement.

Root retains ownership of `finalize_solver_package.py`, its readiness gates,
and the final current manifest. This task did not edit that file or rebuild
a wheel. The broad 183-case suites were not repeated for this optional
factory/import boundary.
